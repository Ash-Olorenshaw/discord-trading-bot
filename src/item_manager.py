import os
import datetime
import discord
import matplotlib.pyplot as plt

from payment_utils import price_refactor
from utils import check_list_items_contain


async def gen_items_list(message, price_file_name : str, ref_file_name : str):
    # -s items
    purchaseFile = open(price_file_name, "r+")
    purchase_items = purchaseFile.readlines()
    purchaseFile.close()
    msgBuffer = ""
    emojiFile =  open(ref_file_name, "r")
    emojis = emojiFile.readlines()
    for i in purchase_items:
        item = i.split("-")
        msgBuffer += "\n" + emojis[purchase_items.index(i)][:-1] + " - $" + item[-2]
        if float(item[-2]) < float(item[-3]):
            msgBuffer += " :arrow_down:"
        elif float(item[-2]) > float(item[-3]):
            msgBuffer += " :arrow_up:"
        else:
            msgBuffer += " :arrow_right:"
    emojiFile.close()
    await message.channel.send("All items:" + msgBuffer + "\n'-s shop' to see what's available for purchase today.")

async def gen_shop_items_list(message, available_items : list[str], price_file_name : str, ref_file_name : str):
    # -s shop
    purchaseFile = open(price_file_name, "r+")
    purchase_items = purchaseFile.readlines()
    purchaseFile.close()
    msgBuffer = ""
    emojiFile =  open(ref_file_name, "r")
    emojis = emojiFile.readlines()
    for i in available_items:
        item = i.split("-")
        msgBuffer += "\n" + emojis[purchase_items.index(i)][:-1] + " - $" + item[-2]
    emojiFile.close()
    await message.channel.send("Current items available for purchase are:" + msgBuffer + "\n'-s buy' to purchase an item")

async def reroll_daily_item_vals(message, date_mod : str, price_file_name : str):
    if message.author.name == os.getenv('ADMIN'):
        purchaseFile = open(price_file_name, "r+")
        purchase_items = purchaseFile.readlines()
        purchaseTemp = price_refactor(purchase_items, date_mod, True)

        purchaseFile.seek(0)
        purchaseFile.truncate(0)

        for line in purchaseTemp:
            purchaseFile.write(line)
        purchaseFile.close()

        await message.channel.send("values successfully rerolled")

    else:
        await message.channel.send("Error! You are not a trusted admin.")

async def get_item_val(message, purchase_items : list[str]):
    graphItem = message.content[9:]
    graphItemPos = check_list_items_contain(purchase_items, graphItem)

    if graphItemPos != -1:
        vals = purchase_items[graphItemPos].split("-")
        del vals[0]
        del vals[-1]
        days = []
        today = datetime.datetime.now()
        d = today

        for i in range(8):
            d = today - datetime.timedelta(days = i)
            dayVal = d.strftime("%d")
            days.append(int(dayVal))

        days.reverse()
        newVals = []

        for val in vals:
            newVals.append(float(val))

        plt.clf()
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7], days)
        plt.plot([0, 1, 2, 3, 4, 5, 6, 7], newVals)
        plt.savefig("graph.png", bbox_inches = "tight")

        file = discord.File("graph.png", filename = "graph.png")
        embed = discord.Embed()
        embed.set_image(url = "attachment://graph.png")

        await message.channel.send(graphItem + "'s current value trend:")
        await message.channel.send(file = file, embed = embed)
    else:
        await message.channel.send("Item name not recognised")

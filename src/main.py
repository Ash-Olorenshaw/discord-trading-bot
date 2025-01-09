import os
import random
import discord
import datetime
from dotenv import load_dotenv

from networth_calc import graph_all_networths, graph_user_networth
from payment_utils import price_refactor
from sale_manager import sell_item
from utils import check_list_items_contain
from networth_utils import create_daily_networths
from item_manager import gen_items_list, gen_shop_items_list, reroll_daily_item_vals, get_item_val
from inventory_manager import gen_user_inv_admin
from enrolment_manager import rewind_time, enrol_user
from inventory_manager import gen_user_inv
from buy_manager import buy_item
from globals import default_items, priceFile, refFile, userFile, worthFile
from arg_parser import parse_args


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intentz = discord.Intents.default()
intentz.message_content = True
intentz.members = True

client = discord.Client(intents = intentz)

last_update = ""
available_items = []

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'{member.name} has arrived!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global last_update

    date_mod : str = datetime.date.today().strftime("%d%m%Y")
    random.seed(date_mod)

    usersFile = open(userFile, "r")
    userfile_lines = usersFile.readlines()
    usersFile.close()

    await create_daily_networths(userFile, worthFile, priceFile, date_mod)

    networthFile = open(worthFile, "r")
    networths = networthFile.readlines()
    networthFile.close()

    purchaseFile = open(priceFile, "r+")
    purchase_items = purchaseFile.readlines()

    if last_update != date_mod:
        purchaseTemp = price_refactor(purchase_items, date_mod, False)
        purchaseFile.seek(0)
        purchaseFile.truncate(0)
        
        for line in purchaseTemp:
            purchaseFile.write(line)
        
        temp_purchase_items = []

        #set up current shop items
        temp_purchase_items = purchase_items.copy()
        for _ in range(6):
            addItem = random.choice(temp_purchase_items)
            available_items.append(addItem)
            temp_purchase_items.remove(addItem)

    purchaseFile.close()

    player_line = check_list_items_contain(userfile_lines, message.author.name)

    last_update = date_mod

    if message.content.lower()[:2] == "-s" and player_line == -1 and message.content != "-s enrol":
        await message.channel.send("You are currently not registered. Type '-s enrol' to register yourself!")
    #else:
    #    await parse_args

    elif message.content.lower() == "-s help":
        await message.channel.send("# Currently available commands:\n-s enrol (to begin)\n-s inventory (view your inventory)\n-s value [ITEM NAME] (see the value of an item over the past few days)\n-s shop (see the shop)\n-s buy [ITEM NAME] (buy an item)\n-s sell [ITEM NAME] (sell an item)\n-s items (view all items)\n-s networth me (see your current networth)\n-s networth all (see everyone's networth)\n-s rewind-time (reset your items, cash, etc to user defaults)")

    elif message.content == "-s enrol":
        await enrol_user(message, default_items, player_line, userFile)

    elif message.content == "-s inventory" or message.content == "-s inv":
        await gen_user_inv(message, userfile_lines, priceFile, refFile, networths)

    elif message.content == "-s shop":
        await gen_shop_items_list(message, available_items, priceFile, refFile)

    elif message.content[:6] == "-s buy":
       await buy_item(message, purchase_items, available_items, userfile_lines, player_line, userFile)

    elif message.content[:8] == "-s value":
        await get_item_val(message, purchase_items)

    elif message.content[:7] == "-s sell":
        await sell_item(message, purchase_items, userfile_lines, player_line, userFile)

    elif message.content == "-s items":
        await gen_items_list(message, priceFile, refFile)

    elif message.content == "-s worth me" or message.content == "-s networth me":
        await graph_user_networth(message, networths, userfile_lines, priceFile)

    elif message.content == "-s worth all" or message.content == "-s networth all":
        await graph_all_networths(message, networths)

    elif message.content == "-s rewind-time":
        await rewind_time(message, client, networths, purchase_items, userfile_lines, default_items, player_line, priceFile, userFile)

    elif message.content == "-s admin reroll values":
        await reroll_daily_item_vals(message, date_mod, priceFile)

    elif message.content[:12] == "-s admin inv":
        await gen_user_inv_admin(message, userfile_lines, priceFile, refFile)

client.run(TOKEN)

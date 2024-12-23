import os
import random
import discord
import matplotlib.pyplot as plt
import datetime
import time
from utils import check_list_items_contain, convert_list_to_string, create_chopped_list
from payment_utils import gen_networth, price_refactor
from networth_utils import create_daily_networths

from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

priceFile = "prices.txt"
userFile = "users.txt"
worthFile = "networth.txt"
refFile = "itemEmoji.txt"
default_items = "-100-apple-tent-oil lamp"

intentz = discord.Intents.default()
intentz.message_content = True
intentz.members = True

client = discord.Client(intents = intentz)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'{member.name} has arrived!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    date_mod = datetime.date.today().strftime("%d%m%Y")
    random.seed(date_mod)

    usersFile = open(userFile, "r")
    lines = usersFile.readlines()
    usersFile.close()

    networthFile = open(worthFile, "r")
    networths = networthFile.readlines()
    networthFile.close()

    purchaseFile = open(priceFile, "r+")
    purchase_items = purchaseFile.readlines()
    purchaseTemp = price_refactor(purchase_items, date_mod, False)
    purchaseFile.seek(0)
    purchaseFile.truncate(0)
    for line in purchaseTemp:
        purchaseFile.write(line)
    purchaseFile.close()

    temp_purchase_items = []
    available_items = []

    create_daily_networths(userFile, worthFile, priceFile, date_mod)

    #set up current shop items
    temp_purchase_items = purchase_items.copy()
    for i in range(6):
        addItem = random.choice(temp_purchase_items)
        available_items.append(addItem)
        temp_purchase_items.remove(addItem)
        
    if message.content.lower() == "-s help":
        await message.channel.send("# Currently available commands:\n-s enrol (to begin)\n-s inventory (view your inventory)\n-s value [ITEM NAME] (see the value of an item over the past few days)\n-s shop (see the shop)\n-s buy [ITEM NAME] (buy an item)\n-s sell [ITEM NAME] (sell an item)\n-s items (view all items)\n-s networth me (see your current networth)\n-s networth all (see everyone's networth)\n-s rewind-time (reset your items, cash, etc to user defaults)")
    elif message.content == "-s enrol":
        if not check_list_items_contain(lines, message.author.name) == -1:
            await message.channel.send("<@" + str(message.author.id) + "> already enrolled!")
        else:
            usersFile = open(userFile, "a")
            usersFile.write("\n" + message.author.name + default_items)
            await message.channel.send("<@" + str(message.author.id) + "> enrolled!")
    elif message.content == "-s inventory" or message.content == "-s inv":
        if not check_list_items_contain(lines, message.author.name) == -1:
            choppedList = create_chopped_list(lines, message.author.name)
            lineNum = choppedList.index(message.author.name)
            items = lines[lineNum].split("-")
            purchaseFile = open(priceFile, "r+")
            purchase_items = purchaseFile.readlines()
            purchaseFile.close()
            items[-1] = items[-1][:-1]
            msgBuffer = ""
            emojiFile = open(refFile, "r")
            emojis = emojiFile.readlines()
            for i in items:
                print(i)
                if i != message.author.name:
                    try:
                        float(i)
                        msgBuffer += "\n" + "Wallet: $" + i + "\n"
                    except:
                        if (" " + i.lower()) not in msgBuffer.lower():
                            
                            if items.count(i.lower()) > 1:
                                msgBuffer += " (x" + str(items.count(i.lower())) + ") " + emojis[check_list_items_contain(purchase_items, i)]
                            else:
                                msgBuffer += emojis[check_list_items_contain(purchase_items, i)]
            emojiFile.close()
            await message.channel.send("Your current inventory is as follows:" + msgBuffer)
            netLine = check_list_items_contain(networths, message.author.name)
            if not netLine == -1 and gen_networth(message.author.name, lines, priceFile) < 100:
                await message.channel.send("You are currently poor. Type '-s rewind-time' to restart.")
        else:
            await message.channel.send("You are currently not registered. Type '-s enrol' to register yourself!")
    elif message.content == "-s shop":
        if not check_list_items_contain(lines, message.author.name) == -1:
            purchaseFile = open(priceFile, "r+")
            purchase_items = purchaseFile.readlines()
            purchaseFile.close()
            msgBuffer = ""
            emojiFile =  open(refFile, "r")
            emojis = emojiFile.readlines()
            for i in available_items:
                item = i.split("-")
                msgBuffer += "\n" + emojis[purchase_items.index(i)][:-1] + " - $" + item[-2]
            emojiFile.close()
            await message.channel.send("Current items available for purchase are:" + msgBuffer + "\n'-s buy' to purchase an item")
        else:
            await message.channel.send("You are currently not registered. Type '-s enrol' to register yourself!")
    elif message.content[:6] == "-s buy":
        checkLine = check_list_items_contain(lines, message.author.name)
        if not checkLine == -1:
            
            try:
                int(message.content[-1])
                args = message.content[7:].split(" ")
                buyItem = args[0].lower()
                try:
                    times = float(args[1])
                except:
                    try:
                        buyItem += " " + args[1].lower()
                        times = float(args[2])
                    except:
                        buyItem += " " + args[2].lower()
                        times = float(args[3])
            except:
                buyItem = message.content[7:].lower()
                times = 1.0
            if times < 0:
                await message.channel.send("Processing request...")
                time.sleep(3)
                await message.channel.send("Caught you! Don't try buying negative items!")
            else:
                #check if number to buy is a weird float
                if not times.is_integer():
                    await message.channel.send("Processing request...")
                    time.sleep(3)
                    await message.channel.send("Error! Number of items requested is not a whole number.")
                else:
                    itemCheck = check_list_items_contain(purchase_items, buyItem)
                    if not itemCheck == -1:
                        userItems = lines[checkLine].split("-")
                        itemVals = purchase_items[itemCheck].split("-")
                        if float(userItems[1]) >= (float(itemVals[-2]) * times):
                            if not check_list_items_contain(available_items, buyItem) == -1:
                                usersFile = open(userFile, "a")
                                userItems[-1] = userItems[-1][:-1]
                                for i in range(int(times)):
                                    userItems.append(buyItem)
                                userItems[1] = str(round(float(userItems[1]) - (float(itemVals[-2]) * times), 2))
                                userItems[-1] = userItems[-1] + "\n"
                                lines[checkLine] = convert_list_to_string(userItems)
                                usersFile.truncate(0)
                                for line in lines:
                                    usersFile.write(line)
                                usersFile.close()
                                await message.channel.send("item purchased!")
                            else:
                                await message.channel.send("Item is not currently available for purchase today.")
                        else:
                            await message.channel.send("You have insufficient funds.")
                    elif buyItem == "":
                        await message.channel.send("Please enter item name after command (i.e. '-s buy apple')")
                    else:
                        await message.channel.send("Item name not recognised")
        else:
            await message.channel.send("You are currently not registered. Type '-s enrol' to register yourself!")
    elif message.content[:8] == "-s value":
        checkLine = check_list_items_contain(lines, message.author.name)
        if not checkLine == -1:
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
        else:
            await message.channel.send("You are currently not registered. Type '-s enrol' to register yourself!")
    elif message.content[:7] == "-s sell":
        checkLine = check_list_items_contain(lines, message.author.name)
        if not checkLine == -1:
            if message.content[-1].isdigit():
                args = message.content[7:].split(" ")
                sellItem = args[1].lower()
                try:
                    if args[2].isdigit():
                        times = float(args[2])
                    elif args[3].isdigit():
                        sellItem += " " + args[2].lower()
                        times = float(args[3])
                    else:
                        sellItem += " " + args[3].lower()
                        times = float(args[4])
                except:
                    await message.channel.send("Processing request...")
                    time.sleep(3)
                    await message.channel.send("Item total not understood.")
                    times = 0
            else:
                sellItem = message.content[8:].lower()
                times = 1.0
            if times < 0:
                await message.channel.send("Processing request...")
                time.sleep(3)
                await message.channel.send("Caught you! Don't try selling negative items!")
            elif times != 0:
                if not times.is_integer():
                    await message.channel.send("Processing request...")
                    time.sleep(3)
                    await message.channel.send("Error! Number of items requested is not a whole number.")
                else:
                    userItems = lines[checkLine].split("-")
                    userItems[-1] = userItems[-1][:-1]
                    choppedList = create_chopped_list(lines, message.author.name)
                    lineNum = choppedList.index(message.author.name)
                    items = lines[lineNum].split("-")
                    itemCheck = check_list_items_contain(items, sellItem)
                    items[-1] = items[-1][:-1]
                    if itemCheck != -1 and items.count(sellItem.lower()) >= int(times):
                        purchItemCheck = check_list_items_contain(purchase_items, sellItem)
                        itemVals = purchase_items[purchItemCheck].split("-")
                        newB = float(userItems[1]) + (float(itemVals[-2]) * float(times))
                        userItems[1] = str(round(newB, 2))
                        num = 0
                        for i in userItems:
                            if num >= int(times):
                                break
                            elif i.lower() == sellItem.lower():
                                print("deleting:")
                                print(userItems[userItems.index(i)])
                                userItems[userItems.index(i)] = "~"
                                num += 1
                                print(num)
                        for i in range(num): 
                            userItems.remove("~")
                        userItems[-1] = userItems[-1] + "\n"
                        lines[checkLine] = convert_list_to_string(userItems)
                        usersFile = open(userFile, "a")
                        usersFile.truncate(0)
                        for line in lines:
                            usersFile.write(line)
                        usersFile.close()
                        if int(times) == 1:
                            await message.channel.send("Item sold!")
                        else:
                            await message.channel.send("Items sold!")
                    else:
                        if items.count(sellItem) < times:
                            await message.channel.send("You do not own " + str(int(times)) + " " + str(sellItem) + "s!")
                        else:
                            await message.channel.send("You do not own an item of that name.")
        else:
            await message.channel.send("You are currently not registered. Type '-s enrol' to register yourself!")
    elif message.content == "-s items":
        purchaseFile = open(priceFile, "r+")
        purchase_items = purchaseFile.readlines()
        purchaseFile.close()
        msgBuffer = ""
        emojiFile =  open(refFile, "r")
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
    elif message.content == "-s worth me" or message.content == "-s networth me":
        checkLine = check_list_items_contain(lines, message.author.name)
        if not checkLine == -1:
            #print(gen_networth(message.author.name, lines))
            await message.channel.send("Locating networth...")
            netLine = check_list_items_contain(networths, message.author.name)
            if not netLine == -1:
                maxWorth = 0.0
                a = networths[netLine].split("-")
                del a[0]
                del a[-1]
                for w in a:
                    if float(w) > maxWorth:
                        maxWorth = float(w)
                
                days = []
                today = datetime.datetime.now()
                d = today
                for i in range(14):
                    d = today - datetime.timedelta(days = i)
                    dayVal = d.strftime("%d")
                    days.append(int(dayVal))
                days.reverse()

                graphList = []
                for val in a:
                    graphList.append(float(val))
                plt.clf()
                plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], days)
                plt.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], graphList)
                plt.savefig("graph.png", bbox_inches = "tight")
                file = discord.File("graph.png", filename = "graph.png")
                embed = discord.Embed()
                embed.set_image(url = "attachment://graph.png")

                await message.channel.send("Your current networth is $" + str(gen_networth(message.author.name, lines, priceFile)))
                await message.channel.send(file = file, embed = embed)
            else:
                await message.channel.send("Error! Unable to retrieve your current networth data.")
        else:
            await message.channel.send("You are currently not registered. Type '-s enrol' to register yourself!")
    elif message.content == "-s worth all" or message.content == "-s networth all":
        await message.channel.send("Locating networths...")
        maxWorth = 0.0
        for i in range(len(networths)):
            if len(networths[i]) > 5:
                a = networths[i].split("-")
                del a[0]
                del a[-1]
                for w in a:
                    if float(w) > maxWorth:
                        maxWorth = float(w)
        days = []
        today = datetime.datetime.now()
        d = today
        for i in range(14):
            d = today - datetime.timedelta(days = i)
            dayVal = d.strftime("%d")
            days.append(int(dayVal))
        days.reverse()

        plt.clf()
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], days)
        #plt.set_ylim(bottom=0)
        #plt.ylim(bottom=0, top=maxWorth)
        #plt.Axes.set_ylim(bottom=0, top=maxWorth)
        #plt.yticks([0, maxWorth], [0, maxWorth])
        for i in networths:
            if len(i) > 5:
                a = i.split("-")
                print("name = " + a[0])
                nm = a[0]
                currentGuild = message.author.guild
                #member = currentGuild.get_member(nm)
                member = discord.utils.get(currentGuild.members, name = nm)
                
                del a[0]
                del a[-1]
                graphList = []
                for val in a:
                    graphList.append(float(val))
                print(graphList)
                if not member is None: member = member.display_name
                plt.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], graphList, label = member)
                
        plt.legend(loc = 'best')
        plt.savefig("graph.png", bbox_inches = "tight")
        file = discord.File("graph.png", filename = "graph.png")
        embed = discord.Embed()
        embed.set_image(url = "attachment://graph.png")
        await message.channel.send("Recent networth of all users:")
        await message.channel.send(file = file, embed = embed)
    elif message.content == "-s rewind-time":
        playerLine = check_list_items_contain(lines, message.author.name)
        if not playerLine == -1:
            defaultNetworth = 100.0
            defaultList = ["apple", "tent", "oil lamp"]
            for item in defaultList:
                itemPos = check_list_items_contain(purchase_items, item)
                valu = purchase_items[itemPos].split("-")[-2]
                defaultNetworth += float(valu)
            
            netLine = check_list_items_contain(networths, message.author.name)
            if not netLine == -1 and gen_networth(message.author.name, lines, priceFile) < defaultNetworth:
                await message.channel.send("Good choice. Rewinding time.")

                usersFile = open(userFile, "r+")
                lines[playerLine] = message.author.name + default_items + "\n"
                usersFile.seek(0)
                usersFile.truncate(0)
                for line in lines:
                    usersFile.write(line)
                usersFile.close()
                await message.channel.send("Successfully rewound time.")
            else:
                choiceMsg = await message.channel.send("Are you sure? Your current networth is $" + str(gen_networth(message.author.name, lines, priceFile)) + 
                                           ". \nPerforming this action will lower your networth to $" + str(defaultNetworth) + 
                                           ".\nReact with :white_check_mark: to continue or :x: to cancel this operation.")
                
                await choiceMsg.add_reaction("✅")
                await choiceMsg.add_reaction("❌")

                def check(reaction, user):
                    possibleEmojis = ["✅", "❌"]
                    return user == message.author and str(reaction.emoji) in possibleEmojis and reaction.message == choiceMsg

                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
                    if str(reaction.emoji) == "✅":
                        usersFile = open(userFile, "r+")
                        lines[playerLine] = message.author.name + default_items + "\n"
                        usersFile.seek(0)
                        usersFile.truncate(0)
                        for line in lines:
                            usersFile.write(line)
                        usersFile.close()
                        await message.channel.send("Successfully rewound time.")
                    elif str(reaction.emoji) == "❌":
                        await message.channel.send("Successfully cancelled operation.")

                except TimeoutError:
                    await message.channel.send("No reaction detected, cancelling operation")
    



    elif message.content == "-s admin reroll values":
        if message.author.name == os.getenv('ADMIN'):
            purchaseFile = open(priceFile, "r+")
            purchase_items = purchaseFile.readlines()
            purchaseTemp = price_refactor(purchase_items, date_mod, True)
            purchaseFile.seek(0)
            purchaseFile.truncate(0)
            for line in purchaseTemp:
                purchaseFile.write(line)
            purchaseFile.close()
            usersFile.close()
            await message.channel.send("values successfully rerolled")
        else:
            await message.channel.send("Error! You are not a trusted admin.")
    elif message.content[:12] == "-s admin inv":
        if message.author.name == os.getenv('ADMIN'):
            author = message.content[13:]
            checkLine = check_list_items_contain(lines, author)
            if not checkLine == -1:
                await message.channel.send("User found - fetching inventory.")
                choppedList = create_chopped_list(lines, author)
                lineNum = choppedList.index(author)
                items = lines[lineNum].split("-")
                purchaseFile = open(priceFile, "r+")
                purchase_items = purchaseFile.readlines()
                purchaseFile.close()
                items[-1] = items[-1][:-1]
                del items[0]
                msgBuffer = ""
                emojiFile = open(refFile, "r")
                emojis = emojiFile.readlines()
                for i in items:
                    if i != author:
                        try:
                            float(i)
                            msgBuffer += "\n" + "Wallet: $" + i + "\n"
                        except:
                            if (" " + i.lower()) not in msgBuffer.lower():
                                if items.count(i.lower()) > 1:
                                    msgBuffer += " (x" + str(items.count(i.lower())) + ") " + emojis[check_list_items_contain(purchase_items, i)]
                                else:
                                    msgBuffer += emojis[check_list_items_contain(purchase_items, i)]
                emojiFile.close()
                await message.channel.send(author.capitalize() + "'s current inventory is as follows:" + msgBuffer)
            else:
                await message.channel.send("User " + author.capitalize() + " is not enrolled or doesn't exist.")
        else:
                await message.channel.send("Error! You are not a trusted admin.")
        
            
        
client.run(TOKEN)

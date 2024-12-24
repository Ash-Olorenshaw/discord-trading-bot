import time
from utils import create_chopped_list, check_list_items_contain, convert_list_to_string

async def sell_item(message, purchase_items : list[str], userfile_lines : list[str], userfile_player_line : int, userfile_name : str):
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
            userItems = userfile_lines[userfile_player_line].split("-")
            userItems[-1] = userItems[-1][:-1]
            choppedList = create_chopped_list(userfile_lines, message.author.name)
            lineNum = choppedList.index(message.author.name)
            items = userfile_lines[lineNum].split("-")
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
                userfile_lines[userfile_player_line] = convert_list_to_string(userItems)
                usersFile = open(userfile_name, "a")
                usersFile.truncate(0)
                for line in userfile_lines:
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

from utils import check_list_items_contain, convert_list_to_string
import time

async def buy_item(message, purchase_items : list[str], available_items : list[str], userfile_lines : list[str], userfile_player_line : int, userfile_name : str):
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
                userItems = userfile_lines[userfile_player_line].split("-")
                itemVals = purchase_items[itemCheck].split("-")

                if float(userItems[1]) >= (float(itemVals[-2]) * times):
                    if not check_list_items_contain(available_items, buyItem) == -1:

                        usersFile = open(userfile_name, "a")
                        userItems[-1] = userItems[-1][:-1]

                        for _ in range(int(times)):
                            userItems.append(buyItem)

                        userItems[1] = str(round(float(userItems[1]) - (float(itemVals[-2]) * times), 2))
                        userItems[-1] = userItems[-1] + "\n"
                        userfile_lines[userfile_player_line] = convert_list_to_string(userItems)
                        usersFile.truncate(0)

                        for line in userfile_lines:
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

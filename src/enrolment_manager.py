from utils import check_list_items_contain
from networth_utils import gen_networth

async def rewind_time(message, client, networths : list[str], purchase_items : list[str], userfile_lines : list[str], default_items : str, userfile_player_line : int, price_file_name : str, userfile_name : str):
    defaultNetworth = 100.0
    defaultList = ["apple", "tent", "oil lamp"]
    for item in defaultList:
        itemPos = check_list_items_contain(purchase_items, item)
        valu = purchase_items[itemPos].split("-")[-2]
        defaultNetworth += float(valu)
    
    netLine = check_list_items_contain(networths, message.author.name)
    if not netLine == -1 and gen_networth(message.author.name, userfile_lines, price_file_name) < defaultNetworth:
        await message.channel.send("Good choice. Rewinding time.")

        usersFile = open(userfile_name, "r+")
        userfile_lines[userfile_player_line] = message.author.name + default_items + "\n"
        usersFile.seek(0)
        usersFile.truncate(0)
        for line in userfile_lines:
            usersFile.write(line)
        usersFile.close()
        await message.channel.send("Successfully rewound time.")
    else:
        choiceMsg = await message.channel.send("Are you sure? Your current networth is $" + str(gen_networth(message.author.name, userfile_lines, price_file_name)) + 
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
                usersFile = open(userfile_name, "r+")
                userfile_lines[userfile_player_line] = message.author.name + default_items + "\n"
                usersFile.seek(0)
                usersFile.truncate(0)
                for line in userfile_lines:
                    usersFile.write(line)
                usersFile.close()
                await message.channel.send("Successfully rewound time.")
            elif str(reaction.emoji) == "❌":
                await message.channel.send("Successfully cancelled operation.")

        except TimeoutError:
            await message.channel.send("No reaction detected, cancelling operation")

async def enrol_user(message, default_items : str, userfile_player_line : int, userfile_name : str):
    if userfile_player_line != -1:
        await message.channel.send("<@" + str(message.author.id) + "> already enrolled!")

    else:
        usersFile = open(userfile_name, "a")
        usersFile.write("\n" + message.author.name + default_items)
        usersFile.close()

        await message.channel.send("<@" + str(message.author.id) + "> enrolled!")



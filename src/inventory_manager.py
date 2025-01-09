import os

from utils import check_list_items_contain, create_chopped_list
from networth_utils import gen_networth

async def gen_user_inv(message, lines : list[str], price_file_name : str, ref_file_name : str, networths : list[str]):
    choppedList = create_chopped_list(lines, message.author.name)
    lineNum = choppedList.index(message.author.name)
    items = lines[lineNum].split("-")

    purchaseFile = open(price_file_name, "r+")
    purchase_items = purchaseFile.readlines()
    purchaseFile.close()

    items[-1] = items[-1][:-1]
    msg_buffer = ""
    emojiFile = open(ref_file_name, "r")
    emojis = emojiFile.readlines()

    for i in items:
        if i != message.author.name:
            try:
                float(i)
                msg_buffer += "\n" + "**Wallet: $" + i + "**\n"
            except:
                if (" " + i.lower()) not in msg_buffer.lower():
                    
                    if items.count(i.lower()) > 1:
                        msg_buffer += f"- {emojis[check_list_items_contain(purchase_items, i)].strip()} (x{items.count(i.lower())})\n"
                    else:
                        msg_buffer += f"- {emojis[check_list_items_contain(purchase_items, i)].strip()}\n"
    emojiFile.close()

    await message.channel.send("<@" + str(message.author.id) + "> Your current inventory is as follows:" + msg_buffer)
    netLine = check_list_items_contain(networths, message.author.name)
    if not netLine == -1 and gen_networth(message.author.name, lines, price_file_name) < 100:
        await message.channel.send("<@" + str(message.author.id) + ">  are currently poor. Type '-s rewind-time' to restart.")


async def gen_user_inv_admin(message, userfile_lines : list[str], price_file_name : str, ref_file_name : str):
    if message.author.name == os.getenv('ADMIN'):
        author = message.content[13:]
        checkLine = check_list_items_contain(userfile_lines, author)

        if not checkLine == -1:
            await message.channel.send("User found - fetching inventory.")

            choppedList = create_chopped_list(userfile_lines, author)
            lineNum = choppedList.index(author)
            items = userfile_lines[lineNum].split("-")

            purchaseFile = open(price_file_name, "r+")
            purchase_items = purchaseFile.readlines()
            purchaseFile.close()

            items[-1] = items[-1][:-1]
            del items[0]

            msg_buffer = ""
            emojiFile = open(ref_file_name, "r")
            emojis = emojiFile.readlines()

            for i in items:
                if i != author:
                    try:
                        float(i)
                        msg_buffer += f"\n**Wallet: ${i}**\n"

                    except:
                        if (" " + i.lower()) not in msg_buffer.lower():
                            if items.count(i.lower()) > 1:
                                msg_buffer += f"- {emojis[check_list_items_contain(purchase_items, i)].strip()} (x{items.count(i.lower())})\n"
                            else:
                                msg_buffer += f"- {emojis[check_list_items_contain(purchase_items, i)].strip()}\n"

            emojiFile.close()

            await message.channel.send(author.capitalize() + "'s current inventory is as follows:" + msg_buffer)
        else:
            await message.channel.send("User " + author.capitalize() + " is not enrolled or doesn't exist.")
    else:
            await message.channel.send("Error! You are not a trusted admin.")


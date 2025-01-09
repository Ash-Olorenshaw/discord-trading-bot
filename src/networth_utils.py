from utils import check_list_items_contain, convert_list_to_string, create_chopped_list
from copy import deepcopy

async def create_daily_networths(userFile, worthFile, priceFile, date_mod):
    #create the day's networths
    usersFile = open(userFile, "r")
    lines = usersFile.readlines()
    usersFile.close()

    for i in range(len(lines)):
        if len(lines[i]) > 4:
            networthFile = open(worthFile, "r+")
            networths = networthFile.readlines()
            new_worths = deepcopy(networths)
            messageauth = (lines[i].split("-"))[0]
            netLine = check_list_items_contain(networths, messageauth)

            if not netLine == -1:
                uservals : list[str] = networths[netLine].split("-")
                newser_vals : list[str] = [""] * len(uservals)
                if uservals[-1] != date_mod + "\n":

                    newser_vals[0] = uservals[0]
                    for i in range(13):
                        # does vals 1 -> 2 through to vals 13 -> 14
                        newser_vals[i + 1] = uservals[i + 2]

                    newser_vals[14] = str(gen_networth(messageauth, lines, priceFile))
                    newser_vals[-1] = date_mod + "\n"
                    new_worths[netLine] = "-".join(newser_vals)
                    networthFile.seek(0)
                    networthFile.truncate(0)

                    for line in new_worths:
                        networthFile.write(line)
            else:
                networthFile = open(worthFile, "a")
                networthFile.write(messageauth + "-0-0-0-0-0-0-0-0-0-0-0-0-0-0-2023" + "\n")
                networthFile.close()

                networthFile = open(worthFile, "r+")
                networths = networthFile.readlines()
                netPointer = check_list_items_contain(networths, messageauth)

                uservals = networths[netPointer].split("-")
                uservals[14] = str(gen_networth(messageauth, lines, priceFile))
                uservals[-1] = date_mod + "\n"

                networths[netLine] = convert_list_to_string(uservals)
                networthFile.seek(0)
                networthFile.truncate(0)

                for line in networths:
                    networthFile.write(line)
            networthFile.close()

def gen_networth(author, peoplelines, price_file_loc):
    chopped_list = create_chopped_list(peoplelines, author)
    line_num = chopped_list.index(author)
    items = peoplelines[line_num].split("-")

    price_file = open(price_file_loc, "r+")
    purchase_items = price_file.readlines()
    price_file.close()

    items[-1] = items[-1].strip()
    worth = 0

    distinct = {}
    for i in items:
        if i != author:
            try:
                float(i)
                distinct["worth"] = float(i)
                worth += float(i)
            except:
                item_pos = check_list_items_contain(purchase_items, i)
                if item_pos != -1:
                    vals = purchase_items[item_pos].split("-")
                    if i in distinct:
                        distinct[i] += float(vals[-2])
                    else:
                        distinct[i] = float(vals[-2])
                    worth += float(vals[-2])

    return round(worth, 2)

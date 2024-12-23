from payment_utils import gen_networth
from utils import check_list_items_contain, convert_list_to_string

def create_daily_networths(userFile, worthFile, priceFile, date_mod):
    #create the day's networths
    usersFile = open(userFile, "r")
    lines = usersFile.readlines()
    usersFile.close()

    for i in range(len(lines)):
        if len(lines[i]) > 4:
            networthFile = open(worthFile, "r+")
            networths = networthFile.readlines()
            messageauth = (lines[i].split("-"))[0]
            netLine = check_list_items_contain(networths, messageauth)
            if not netLine == -1:
                uservals = networths[netLine].split("-")
                if uservals[-1] != date_mod + "\n":
                    uservals[1] = uservals[2]
                    uservals[2] = uservals[3]
                    uservals[3] = uservals[4]
                    uservals[4] = uservals[5]
                    uservals[5] = uservals[6]
                    uservals[6] = uservals[7]
                    uservals[7] = uservals[8]
                    uservals[8] = uservals[9]
                    uservals[9] = uservals[10]
                    uservals[10] = uservals[11]
                    uservals[11] = uservals[12]
                    uservals[12] = uservals[13]
                    uservals[13] = uservals[14]
                    uservals[14] = str(gen_networth(messageauth, lines, priceFile))
                    uservals[-1] = date_mod + "\n"
                    networths[netLine] = convert_list_to_string(uservals)
                    networthFile.seek(0)
                    networthFile.truncate(0)
                    for line in networths:
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



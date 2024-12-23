import random
from utils import convert_list_to_string, tenpercentchange, create_chopped_list, check_list_items_contain

def price_refactor(prlist, dateseed, override):
    #random spikes need to be added
    for i in range(len(prlist)):
        vals = prlist[i].split("-")
        if vals[-1] != dateseed + "\n" or override == True:
            vals[1] = vals[2]
            vals[2] = vals[3]
            vals[3] = vals[4]
            vals[4] = vals[5]
            vals[5] = vals[6]
            vals[6] = vals[7]
            vals[7] = vals[8]

            tenper = float(vals[8]) / 10
            if float(vals[8]) < 999.0:
                if float(vals[6]) >= float(vals[7]) and float(vals[5]) >= float(vals[6]):
                    if float(vals[4]) >= float(vals[5]) and float(vals[3]) >= float(vals[4]):
                        pricespike = random.randint(0, 2)
                        if pricespike == 0:
                            vals[8] = str(round(random.uniform(tenper, (float(vals[8]) / 2)) + float(vals[8]), 2))
                        else:
                            vals[8] = tenpercentchange(tenper, vals[8])
                    else:
                        pricespike = random.randint(0, 4)
                        if pricespike == 0:
                            vals[8] = str(round(random.uniform(tenper, (float(vals[8]) / 4)) + float(vals[8]), 2))
                        else:
                            vals[8] = tenpercentchange(tenper, vals[8])
                if float(vals[6]) < float(vals[7]) and float(vals[5]) < float(vals[6]):
                    if float(vals[4]) < float(vals[5]) and float(vals[3]) < float(vals[4]):
                        pricespike = random.randint(0, 2)
                        if pricespike == 0:
                            vals[8] = str(round(random.uniform(-1 * (float(vals[8]) / 2), -1 * tenper) + float(vals[8]), 2))
                        else:
                            vals[8] = tenpercentchange(tenper, vals[8])
                    else:
                        pricespike = random.randint(0, 4)
                        if pricespike == 0:
                            vals[8] = str(round(random.uniform(-1 * (float(vals[8]) / 4), -1 * tenper) + float(vals[8]), 2))
                        else:
                            vals[8] = tenpercentchange(tenper, vals[8])
                else:   
                    vals[8] = tenpercentchange(tenper, vals[8])
            else:   
                vals[8] = tenpercentchange(tenper, vals[8])
            vals[-1] = dateseed + "\n"
        prlist[i] = convert_list_to_string(vals)
    return prlist


def gen_networth(author, peoplelines, priceFile):
    choppedList = create_chopped_list(peoplelines, author)
    lineNum = choppedList.index(author)
    items = peoplelines[lineNum].split("-")
    purchaseFile = open(priceFile, "r+")
    purchase_items = purchaseFile.readlines()
    purchaseFile.close()
    items[-1] = items[-1][:-1]
    worth = 0
    for i in items:
        if i != author:
            try:
                float(i)
                worth += float(i)
            except:
                itemPos = check_list_items_contain(purchase_items, i)
                if itemPos != -1:
                    vals = purchase_items[itemPos].split("-")
                    worth += float(vals[-2])
    return round(worth, 2)


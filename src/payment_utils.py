import random
from utils import convert_list_to_string, tenpercentchange

def price_refactor(prlist, dateseed, override):
    #random spikes need to be added
    for i in range(len(prlist)):
        vals = prlist[i].split("-")
        if vals[-1] != dateseed + "\n" or override == True:
            for i in range(7):
                # does vals 1 -> 2 through to vals 7 -> 8
                vals[i + 1] = float(vals[i + 2])

            tenper = float(vals[8]) / 10

            if vals[8] < 999.0:
                if vals[6] >= vals[7] and vals[5] >= vals[6]:
                    if vals[4] >= vals[5] and vals[3] >= vals[4]:
                        pricespike = random.randint(0, 2)
                        if pricespike == 0:
                            vals[8] = str(round(random.uniform(tenper, (vals[8] / 2)) + float(vals[8]), 2))
                        else:
                            vals[8] = tenpercentchange(tenper, vals[8])
                    else:
                        pricespike = random.randint(0, 4)
                        if pricespike == 0:
                            vals[8] = str(round(random.uniform(tenper, (vals[8] / 4)) + float(vals[8]), 2))
                        else:
                            vals[8] = tenpercentchange(tenper, vals[8])
                if vals[6] < vals[7] and vals[5] < vals[6]:
                    if vals[4] < vals[5] and vals[3] < vals[4]:
                        pricespike = random.randint(0, 2)
                        if pricespike == 0:
                            vals[8] = str(round(random.uniform(-1 * (vals[8] / 2), -1 * tenper) + float(vals[8]), 2))
                        else:
                            vals[8] = tenpercentchange(tenper, vals[8])
                    else:
                        pricespike = random.randint(0, 4)
                        if pricespike == 0:
                            vals[8] = str(round(random.uniform(-1 * (vals[8] / 4), -1 * tenper) + float(vals[8]), 2))
                        else:
                            vals[8] = tenpercentchange(tenper, vals[8])
                else:   
                    vals[8] = tenpercentchange(tenper, vals[8])
            else:   
                vals[8] = tenpercentchange(tenper, vals[8])
            vals[-1] = dateseed + "\n"
        prlist[i] = convert_list_to_string(vals)
    return prlist




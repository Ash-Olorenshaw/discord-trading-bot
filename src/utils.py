import random

def check_list_items_contain(target_list, item):
    #print("checking if {item} in {list}")
    #nameLen = len(item)
    for line in target_list:
        if line.split("-")[0].lower() == item.lower():
            return target_list.index(line)
    return -1

def create_chopped_list(target_list, item):
    newList = []
    itemLen = len(item)
    for i in target_list:
        newList.append(i[:itemLen])
    return newList

def convert_list_to_string(target_list):
    s = ""
    for i in target_list:
        s += str(i)
        if i != target_list[-1]:
            s += "-"
    return s

def tenpercentchange(ten, value):
    newval = str(round(random.uniform(-1 * ten, ten) + float(value), 2))
    return newval



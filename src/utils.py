import random

def check_list_items_contain(list, item):
    nameLen = len(item)
    for line in list:
        if line[:nameLen].lower() == item.lower():
            return list.index(line)
    return -1

def create_chopped_list(list, item):
    newList = []
    itemLen = len(item)
    for i in list:
        newList.append(i[:itemLen])
    return newList

def convert_list_to_string(list):
    s = ""
    for i in list:
        s += str(i)
        if i != list[-1]:
            s += "-"
    return s

def tenpercentchange(ten, value):
    newval = str(round(random.uniform(-1 * ten, ten) + float(value), 2))
    return newval



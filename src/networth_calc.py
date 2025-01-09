import discord
import matplotlib.pyplot as plt
import datetime

from utils import check_list_items_contain, convert_list_to_string, create_chopped_list, tenpercentchange
from networth_utils import gen_networth


async def graph_user_networth(message, networths : list[str], userfile_lines : list[str], price_file_name : str):
    await message.channel.send("Locating networth...")
    netLine = check_list_items_contain(networths, message.author.name)
    if not netLine == -1:
        maxWorth = 0.0
        a = networths[netLine].split("-")
        del a[0]
        del a[-1]
        for w in a:
            if float(w) > maxWorth:
                maxWorth = float(w)
        
        days = []
        today = datetime.datetime.now()
        d = today
        for i in range(14):
            d = today - datetime.timedelta(days = i)
            dayVal = d.strftime("%d")
            days.append(int(dayVal))
        days.reverse()

        graphList = []
        for val in a:
            graphList.append(float(val))

        plt.clf()
        plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], days)
        plt.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], graphList)
        plt.savefig("graph.png", bbox_inches = "tight")

        file = discord.File("graph.png", filename = "graph.png")
        embed = discord.Embed()
        embed.set_image(url = "attachment://graph.png")

        await message.channel.send("Your current networth is $" + str(gen_networth(message.author.name, userfile_lines, price_file_name)))
        await message.channel.send(file = file, embed = embed)
    else:
        await message.channel.send("Error! Unable to retrieve your current networth data. Please contact an admin for further info...")

async def graph_all_networths(message, networths : list[str]):
    await message.channel.send("Locating networths...")
    maxWorth = 0.0

    for i in range(len(networths)):
        if len(networths[i]) > 5:
            a = networths[i].split("-")
            del a[0]
            del a[-1]
            for w in a:
                if float(w) > maxWorth:
                    maxWorth = float(w)

    days = []
    today = datetime.datetime.now()
    d = today

    for i in range(14):
        d = today - datetime.timedelta(days = i)
        dayVal = d.strftime("%d")
        days.append(int(dayVal))

    days.reverse()

    plt.clf()
    plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], days)

    for i in networths:
        if len(i) > 5:
            a = i.split("-")
            print("name = " + a[0])
            nm = a[0]
            currentGuild = message.author.guild
            #member = currentGuild.get_member(nm)
            member = discord.utils.get(currentGuild.members, name = nm)
            
            del a[0]
            del a[-1]
            graphList = []
            for val in a:
                graphList.append(float(val))
            print(graphList)
            if not member is None or not nm == "": member = member.display_name
            plt.plot([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], graphList, label = member)
            
    plt.legend(loc = 'best')
    plt.savefig("graph.png", bbox_inches = "tight")
    file = discord.File("graph.png", filename = "graph.png")
    embed = discord.Embed()
    embed.set_image(url = "attachment://graph.png")

    await message.channel.send("Recent networth of all users:")
    await message.channel.send(file = file, embed = embed)

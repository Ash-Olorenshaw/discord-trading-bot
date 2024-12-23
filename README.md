# Discord Trading Bot

#### written by Asher Olorenshaw

A simple Discord bot that attempts to vaguely emulate a real-world stockmarket.

### NOTE: still WIP since this was originally slapped together quite quickly...

## About

Each day the bot will update item values that are in the `prices.txt` file and then generate a selection of items which are purchasable for that day.
Item values are then graphed for users to see upon request; users can also view their items' total worth calculated in a networth graph.

## Setting up / Running

To get started with the Discord Trading Bot, do the following:

```nu-script
# download this repo
git clone "https://github.com/Ash-Olorenshaw/discord-trading-bot.git"

# cd into 'src'
cd discord-trading-bot/src/

# install dependencies
pip install -r requirements.txt
```

Now that you have the dependencies installed, you'll need the `.env` file to store the admin username and bot token
The `.env` file can be created like so:

```nu-script
touch ./.env
```

Now that the file is created you need to populate it with the correct info:

```nu-script
# *nix systems
vi ./.env

# Windows (open in NotePad)
. ./.env
```

The following fields are required for the .env file:

```pwsh
DISCORD_TOKEN=YourBotDiscordToken
ADMIN=AdminUsername
```

Now that the .env file is created, you can run the server.

```nu-script
# run the server
py main.py
```

And now you should be able to see your bot in any servers you have invited it to!

## Usage

All commands must be preceded by `-s`, here are all your options:

```nu-script
# to begin; if your account hasn't been recorded yet.
-s enrol

# view your inventory
-s inventory

# see the specified item's value graph
-s value <ITEM NAME>

# view all items
-s items 

# see the shop items available for purchase
-s shop

# buy an item
-s buy <ITEM NAME>

# sell an item
-s sell <ITEM NAME>

# see your current user's networth
-s networth me 

# graph all users' networths together
-s networth all

# display help file with all but admin commands
-s help

# ⚠️ USE WITH CAUTION! Reset user's money, items, etc to defaults
-s rewind-time
```

### Admin Commands:

the following commands are only available to the user who is `ADMIN` in the `.env` file

```nu-script
# get a user's inventory
-s admin inv <USERNAME>

# ⚠️ USE WITH CAUTION
# reroll all of the day's values - EVERY item's value will be rerolled!
-s admin reroll values
```

## Known issues

- Currently there are issues with buying names with their shorthand (e.g. buying a `paperplane` with `paper`):
  - Selling said items requires using the original shorthand you used 
  - Sometimes this can cause items with similar shorthands (e.g. `Windows PC` and `Windows Laptop`) to be grouped as the same entry in player's inventory
- Issues with `networth all` being barely readable if one player has greatly inflated networth in comparison to everyone else

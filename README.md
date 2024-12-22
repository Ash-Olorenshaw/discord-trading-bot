# Discord Trading Bot

#### written by Asher Olorenshaw

A simple Discord bot that attempts to vaguely emulate a real-world stockmarket.

## About

Each day the bot will update item values that are in the "prices.txt" file and then generate a selection of items which are purchasable for that day.
Item values are then graphed for users to see upon request.
Users then have their items' overall worth calculated each day in a networth which they can also access and have graphed for them.

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

The following fields are required for the .env file (without '<>'s):

```Python
DISCORD_TOKEN=<Your Bot Discord Token>
ADMIN=<Admin Username>
```

Now that the .env file is created, you can run the server.

```nu-script
# run the server
py main.py
```

And now you should be able to see your bot in any servers you have invited it to!

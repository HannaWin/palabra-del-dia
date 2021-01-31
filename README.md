
# Palabra del día
This Telegram bot sends a Spanish word each day, including its English translation, an example sentence, and an audio of its pronounciation.

You can access it on Telegram via `@palabrita_bot`. Have fun :)


## Building your own Bot
You can use this code to run your own Telegram Bot. To do so, follow the steps below.

### Create a Telegram bot
Go to @BotFather on Telegram and create your bot. You will receive an API token. Save it to a file called `api_token.txt`, it will be loaded automatically in the script.

### Prerequisites
The code was written in Python3.7.3. Install the required packages:
```bash
$ pip3 install -r requirements.txt 
```

### Change path
Lastly, you have to change the variables *path_to_script* and *local* in `Bot.py` to show the directory where you saved this repo.

### Run the Bot
To use the bot, `Bot.py` must be running. 

# Brott
Collaborative Project between friends, a discord bot for whatever   
Current devs: @Loloweb, @Driabo, @Nothooon, @Julowo

## Prerequisites

Python >= 3.8  
Poetry >= 1.2.0

## Installation

### Get your bot token

Create your Discord application [here](https://discord.com/developers/applications)

Click the bot tab on the right and add your bot to your created application

![bot token here](https://i.imgur.com/RJZkLZG.png)

Copy the token and add it as an environment variable

**Linux**

Write in your .bashrc :
```bash
export DISCORD_TOKEN="[long_string_of_characters_and_numbers_that_you_should_keep_somewhere]"
```

**Windows**

```powershell
[Environment]::SetEnvironmentVariable('DISCORD_TOKEN', '[long_string_of_characters_and_numbers_that_you_should_keep_somewhere]', "User")
```

---
Back to the discord dev portal, tick all privileged gateway intents and "Administrator" in the bot permissions.

![enable permissions](https://i.imgur.com/ZVpFdGl.png)

Add your bot to a server where you have administrative privileges by entering this link :

https://discord.com/api/oauth2/authorize?client_id=[YOUR_CLIENT_ID_HERE]&permissions=8&scope=bot%20applications.commands 

### Install Poetry

**Linux**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Windows**
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```
Check that poetry.exe and the poetry environment variable is at the right /Python/Scripts in case you have multiple versions of Python installed

### Use poetry to install packages

At the root of the project:  

```bash
poetry install
```

### Run it using poetry

```bash
poetry run python bot.py
```

## Dev Tips

- To add a new dependancy to the projet, use this command to automatically add the dependancy to the `pyproject.toml` file.
```bash
poetry add {package_name}
```
- [Discord.py Documentation](https://discordpy.readthedocs.io/en/stable/index.html)

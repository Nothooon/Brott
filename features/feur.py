import random
import discord
import json


class FeurController:

    # This class needs two things to work: the discord message (discord.Message class) and some stuff from the config
    # file (feur frequency)
    def __init__(self, message: discord.Message):
        with open("config/config.json") as config_file:
            self.config = json.load(config_file)
        self.message = message

    # "Feur" answer isn't always triggered to avoid Brett's Wrath
    # This function is used to determine if the bot should anwser "feur" or not
    def __trigger_feur_answer(self):
        return random.random() <= self.config["feur_frequency"] or self.message.author.name == "kaytag"

    def __trigger_sticker_answer(self):
        return random.random() <= self.config["feur_sticker_frequency"]

    # Collects every individual word in the message while removing unneeded whitespaces/empty str
    # To do so, we split the message's content around whitespaces, then we construct the list by removing selected
    # characters from the split() result.
    def __parse_message_words(self):
        return {words for words in self.message.content.lower().split(" ") if words not in [" ", "", None]}

    # Builds the str that will be sent by the bot.
    # The str will be different depending on what words were found in the user's message.
    # This function can be extended if new awesome "feur" answers emmerge in the feur metagame
    def __answer_builder(self, words) -> str:
        special_feur_triggers = [word for word in words if word in self.config["feur_special_triggers"]]

        if "pourquoi" in words:
            return "Pour feur " + random.choice(self.config["feur_special_endings"])
        elif special_feur_triggers:
            response = special_feur_triggers[0].capitalize() + " feur"
            return response + " " + random.choice(self.config["feur_special_endings"]) if random.random() <= 0.5 \
                else response + " !"
        else:
            # select a single answer at random
            return random.choice(self.config["feur_options"])

    # Main function, called by the bot to start the answer process.
    # An empty message is returned if we're (un)lucky
    def create_feur_answer(self):
        if self.__trigger_feur_answer():  # Determines if an answer must be sent based on feur_frequency value in config
            if self.__trigger_sticker_answer():
                return None, discord.File(self.config["feur_sticker_path"])
            else:
                words = self.__parse_message_words()  # Parses user's message to send the words to the answer builder
                return self.__answer_builder(words), None  # Builds the anwser and send it to the bot
        return None, None

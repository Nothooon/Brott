import random
import discord
import json


class FeurController:

    # This class needs two things to work: the discord message (discord.Message class) and some stuff from the config
    # file (feur frequency)
    def __init__(self, message: discord.Message):
        with open("config/config.json") as config_file:
            self.config = json.load(config_file)
            self.feur_frequency = self.config["feur_frequency"]
        self.message = message

    # "Feur" answer isn't always triggered to avoid Brett's Wrath
    # This function is used to determine if the bot should anwser "feur" or not
    def __trigger_feur_answer(self):
        return random.random() <= self.feur_frequency

    # Collects every individual word in the message while removing unneeded whitespaces/empty str
    # To do so, we split the message's content around whitespaces, then we construct the list by removing selected
    # characters from the split() result.
    def __parse_message_words(self):
        return {words for words in self.message.content.lower().split(" ") if words not in [" ", "", None]}

    # Builds the str that will be sent by the bot.
    # The str will be different depending on what words were found in the user's message.
    # This function can be extended if new awesome "feur" answers emmerge in the feur metagame
    def __answer_builder(self, words) -> str:
        if "pourquoi" in words:
            return "Pour feur, hop la !"
        else:
            # select a single answer at random
            return random.choice(["Feur", "Feur !", "FEUR mec allez hop la", "bah feur du coup", "feur xD", "https://fr.wiktionary.org/wiki/feur"])

    # Main function, called by the bot to start the answer process.
    # An empty message is returned if we're (un)lucky
    def create_feur_answer(self):
        if self.__trigger_feur_answer():  # Determines if an answer must be sent based on feur_frequency value in config
            words = self.__parse_message_words()  # Parses user's message to send the words to the answer builder
            return self.__answer_builder(words)  # Builds the anwser and send it to the bot
        return ""

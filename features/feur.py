import random
import discord
import json


class FeurController:

    def __init__(self, message: discord.Message):
        with open("config/config.json") as config_file:
            self.config = json.load(config_file)
            self.feur_frequency = self.config["feur_frequency"]
        self.message = message

    # "Feur" answer isn't always triggered to avoid Brett's Wrath
    def __trigger_feur_answer(self):
        return random.random() <= self.feur_frequency

    # Tries to comprehend some of the words around "feur" to customize the answer
    def __parse_message_words(self):
        return {words for words in self.message.content.lower().split(" ") if words not in [" ", "", None]}

    def __answer_builder(self, words) -> str:
        if "pourquoi" in words:
            return "Pour feur, hop la !"
        else:
            return "Feur mec, hop la !"

    def create_feur_answer(self):
        if self.__trigger_feur_answer():
            words = self.__parse_message_words()
            return self.__answer_builder(words)
        return ""

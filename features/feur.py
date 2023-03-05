import random
import discord
import json


class FeurController:

    config = {}
    feur_frequency = 0
    message = None

    def __init__(self, message: discord.Message):
        with open("config/config.json") as config_file:
            self.config = json.load(config_file)
            self.feur_frequency = self.config["feur_frequency"]
        self.message = message

    # "Feur" answer isn't always triggered to avoid Brett's Wrath
    def __trigger_feur_answer(self):
        return random.random() >= self.feur_frequency

    # Tries to comprehend some of the words around "feur" to customize the answer
    def __detect_feur_words(self):
        message_words = self.message.content.split(" ")
        print(f"Mots du message: {message_words}")
        return

    def trigger_feur_answer(self):
        self.__detect_feur_words()
        return

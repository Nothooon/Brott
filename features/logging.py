import datetime as dt # Alias obligé pour pas confondre avec datetime.datetime
from datetime import datetime # Logique.
import pandas as pd  # xDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
import json
import discord


class Logger:

    def __init__(self) -> None:
        with open("config/config.json") as config_file:
            self.config = json.load(config_file)["logging"]
            self.separator = self.config["separator"]
            self.feur_csv_path = self.config["feur_csv_file_path"]

    def _get_column_data_from_file(self, datafile: pd.DataFrame, column: str) -> list:
        """This function extracts all the content of a column of a data file
        Args:
            datafile (pd.DataFrame): The file containing the data to extract to the DataFrame format
            column (str): The name of the column we want to extract data from
        Returns:
            list: The content of the column `column`of the `datafile` file
        """
        column_content = []
        for row in datafile[column]:
            column_content.append(row)
        return column_content
    
    def _convert_datetime_to_discord_timestamp(self, timestamp: datetime) -> str:
        """This function converts a datetime object to a Discord timestamp.
        Args:
            datetime (datetime): The datetime object to convert
        Returns:
            str: The Discord timestamp
        """
        epoch = round(datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f").timestamp()) # Convert String back to DateTime
        discordtimestamp = f"<t:{epoch}:R>" # Convert DateTime to Discord Timestamp
        return discordtimestamp
    
    def get_leaderboard(self) -> None:
        """This function returns the entire csv as a Discord embed.
        This is usually not recommended for big servers, however we are only like what, 20 people?
        Returns:
            discord.Embed: The embed containing the csv data
        """
        # Extracting data from the csv in a DataFrame object
        file_content = pd.read_csv(self.feur_csv_path, sep=self.separator)
        embed=discord.Embed(
            title="Feur leaderboard",
            color=discord.Color.purple()
        )
        # extract the data from the csv file and put it in the embed
        users = []
        countfeurs = []
        lastfeurs = []
        for user, countfeur, lastfeur in zip(file_content["user"], file_content["countfeur"], file_content["lastfeur"]):
            users.append(user)
            countfeurs.append(str(countfeur))
            lastfeurs.append(self._convert_datetime_to_discord_timestamp(lastfeur))
        embed.add_field(name="User", value="\n".join(users), inline=True)
        embed.add_field(name="Feurs", value="\n".join(countfeurs), inline=True)
        embed.add_field(name="Latest", value="\n".join(lastfeurs), inline=True)
        return embed
    
    def get_user(self, user: str) -> None:
        """This function returns the row of a user from the csv as a Discord embed.
        Args:
            user (str): The user to get the data from.
        """
        # Extracting data from the csv in a DataFrame object
        file_content = pd.read_csv(self.feur_csv_path, sep=self.separator)
        # extract the data from the csv file and put it in the embed
        embed = None
        #print(user)
        for username, countfeur, lastfeur in zip(file_content["user"], file_content["countfeur"], file_content["lastfeur"]):
            if username == user:
                embed=discord.Embed(
                    title="User's feurs",
                    color=discord.Color.purple()
                )
                discordtimestamp = self._convert_datetime_to_discord_timestamp(lastfeur)
                embed.add_field(name="User", value=user, inline=True)
                embed.add_field(name="Feurs", value=countfeur, inline=True)
                embed.add_field(name="Latest", value=discordtimestamp, inline=True)
        if embed is None: # If embed is still empty, assume user isnt in the csv
            embed=discord.Embed(
                title="User not found or hasn't been feur'd yet.",
                color=discord.Color.red()
            )
        return embed


    def log_feur(self, message_author: str) -> None:
        """This function is used to update the csv file storing the amount of times each individual user got "feur'd"
        by the bot.
        Args:
            message_author (str): The name of the message's author. It'll be stored in the csv file
                                  and used to find the user inside the file.
        """
        # Extracting data from the csv in a DataFrame object
        file_content = pd.read_csv(self.feur_csv_path, sep=self.separator)

        # Extracting the content of the column `user` from that DataFrame object
        usernames = self._get_column_data_from_file(file_content, 'user')
        # Checking if the message's author has already been logged before
        # If he was, it adds 1 to their `countfeur` value
        if message_author in usernames:
            # We had one to the value of "countfeur" for the row corresponding to the message's author
            file_content.loc[file_content["user"] == message_author, "countfeur"] += 1
            # We also change the value of "lastfeur" to current date
            file_content.loc[file_content["user"] == message_author, "lastfeur"] = dt.datetime.now()
        # If the user has never been logged before, adding a new raw for this user
        else:
            # Adding a new row to the file with `countfleur` value initialized at 1
            new_user_row = pd.DataFrame({'user': [message_author], 'countfeur': [1],
                                         'lastfeur': [dt.datetime.now()]})
            file_content = pd.concat([file_content, new_user_row])

        # After updating the DataFrame, we save the changes in the csv file
        file_content.to_csv(self.feur_csv_path, sep=self.separator, index=False)

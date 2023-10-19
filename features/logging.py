import datetime
import pandas as pd  # xDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
import json


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
            file_content.loc[file_content["user"] == message_author, "lastfeur"] = datetime.datetime.now()
        # If the user has never been logged before, adding a new raw for this user
        else:
            # Adding a new row to the file with `countfleur` value initialized at 1
            new_user_row = pd.DataFrame({'user': [message_author], 'countfeur': [1],
                                         'lastfeur': [datetime.datetime.now()]})
            file_content = pd.concat([file_content, new_user_row])

        # After updating the DataFrame, we save the changes in the csv file
        file_content.to_csv(self.feur_csv_path, sep=self.separator, index=False)

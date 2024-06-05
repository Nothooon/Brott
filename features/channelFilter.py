import pandas as pd
import json
import discord
from features import logging

class Filter:

    def __init__(self) -> None:
        with open("config/config.json") as config_file:
            self.config = json.load(config_file)["channel_filter"]
            self.csv_filepath = self.config["channel_csv_filepath"]

    def add_channel_to_ignore_list(self, channel:str) -> str:

        # Extracting data from the csv in a DataFrame object
        file_content = pd.read_csv(self.csv_filepath)

        # Extracts the channel ids from the csv
        channel_list = logging.Logger()._get_column_data_from_file(file_content, 'channel_id')

        if channel not in channel_list:

            # Adding a new row to the file
            new_channel = pd.DataFrame({'channel_id': [channel]})
            file_content = pd.concat([file_content, new_channel])

            # After updating the DataFrame, we save the changes in the csv file
            file_content.to_csv(self.csv_filepath, index=False)
            return "succesfully blacklisted channel"
        
        else :
            return "channel already blacklisted"

    def remove_channel_from_ignore_list(self, channel:str) -> str:

        # Extracting data from the csv in a DataFrame object
        file_content = pd.read_csv(self.csv_filepath)

        # Extracts the channel ids from the csv
        channel_list = logging.Logger()._get_column_data_from_file(file_content, 'channel_id')

        if channel in channel_list:
            
            # Remove row from the file
            file_content = file_content[file_content.channel_id != channel]

            # After updating the DataFrame, we save the changes in the csv file
            file_content.to_csv(self.csv_filepath, index=False)
            return "succesfully allowed channel"
        
        else :
            return "channel already allowed"

    def get_blacklist(self):
        # Extracting data from the csv in a DataFrame object
        file_content = pd.read_csv(self.csv_filepath)

        # Extracts the channel ids from the csv
        return logging.Logger()._get_column_data_from_file(file_content, 'channel_id')
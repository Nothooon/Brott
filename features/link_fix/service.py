import json
import re
import discord


class LinkInfos:
    def __init__(self, original_link: str, app_name: str, post_id: str) -> None:
        self.original_link = original_link
        self.app_name = app_name
        self.post_id = post_id


class LinkFixService:

    def __init__(self):
        with open("config/config.json") as config_file:
            self.config = json.load(config_file)

    def handle_message(self, message: discord.Message) -> None:
        if not message:
            return

        link_infos = self.detect_inner_links(message.content)

        if link_infos:
            new_link = self.__generate_new_link(link_infos)
            print(f"New link: {new_link}")
            return self.__create_new_message(message, link_infos, new_link)

    def detect_inner_links(self, message: str = "") -> LinkInfos:
        inner_link = re.match("https://(twitter.com|x.com)(/[a-zA-Z0-9_]{5,15}/status/[0-9]{0,20})", message)

        if not inner_link:
            # No link in the message -> we return false
            return None

        return LinkInfos(inner_link[0], inner_link[1], inner_link[2])

    def __generate_new_link(self, link_infos: LinkInfos) -> str:
        app_name = link_infos.app_name.strip(".com")
        replacement = self.config.get("link_fix").get(app_name).get("replacement")

        return "https://" + replacement + link_infos.post_id

    def __create_new_message(self, message: discord.Message, link_infos: LinkInfos, new_link: str) -> str:
        content = f"Lien {link_infos.app_name} détecté. Correction automatique.\n"
        content += f"{new_link}\n"
        content += f"Post original par @{message.author.display_name}\n"

        message_other_content = re.sub(f"{link_infos.original_link}\\S*", "", message.content)
        if message_other_content:
            content += f"> {message_other_content}"
        return content

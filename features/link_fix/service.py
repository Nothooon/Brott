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

        link_infos_list = self.detect_inner_links(message.content)

        if link_infos_list:
            new_links = []
            for link_infos in link_infos_list:
                new_link = self.__generate_new_link(link_infos)
                new_links.append(new_link)
                print(f"New link: {new_link}")
            
            return self.__create_new_message(message, link_infos_list, new_links)

    def detect_inner_links(self, message: str = "") -> list[LinkInfos] | None:
        inner_links = re.finditer(r"https://(twitter.com|x.com)(/[a-zA-Z0-9_]{5,15}/status/[0-9]{0,20})", message)

        if not inner_links:
            # No link in the message -> we return false
            return None
        
        link_infos_list = []
        for match in inner_links:
            link_infos_list.append(LinkInfos(match.group(0), match.group(1), match.group(2)))

        return link_infos_list

    def __generate_new_link(self, link_infos: LinkInfos) -> str:
        app_name = link_infos.app_name.strip(".com")
        replacement = self.config.get("link_fix").get(app_name).get("replacement")

        return "https://" + replacement + link_infos.post_id

    def __create_new_message(self, message: discord.Message, link_infos_list: list[LinkInfos], new_links: list[str]) -> str:
            content = f"{len(link_infos_list)} lien(s) détecté(s). Correction automatique.\n"
            for new_link in new_links:
                content += f"{new_link}\n"
        content += f"Post original par {message.author.mention} ({message.author.display_name})\n"

        message_other_content = message.content
        for link_infos in link_infos_list:
            message_other_content = re.sub(f"{re.escape(link_infos.original_link)}\\S*", "", message_other_content)
        
        message_other_content = message_other_content.strip()
        if message_other_content:
            content += f"- {message_other_content}"
        return content

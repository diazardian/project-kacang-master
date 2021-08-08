import json
import requests
import os
from dotenv import load_dotenv

# local
# API_ENDPOINT = "http://127.0.0.1:8000/api/"
client = requests.session()
load_dotenv()
api = os.getenv("API_ENDPOINT")


class Init:
    def guild_register(aidi, name):
        url = api + "MemberGuild/"
        headers = {"Content-Type": "application/json"}
        data = {"id_guild": aidi, "name": name}
        result = requests.post(url, data=json.dumps(data), headers=headers)
        print(result)
        return result

    def member_register(aidi, name, avatar, user_join, user_create, guild_id):
        url = api + "DiscordMember/"
        headers = {
            "Content-Type": "application/json",
            "Referer": url,
        }
        data = {
            "id_discord": aidi,
            "name": name,
            "avatar": avatar,
            "user_join": user_join,
            "user_create": user_create,
            "guild_id": guild_id,
        }
        result = requests.post(url, data=json.dumps(data), headers=headers)
        return result

    def setup(aidi, name, status):
        url = api + "GuildChannel/"
        headers = {
            "Content-Type": "application/json",
            "Referer": url,
        }
        data = {
            "id_channel": aidi,
            "name": name,
            "status": status,
        }
        result = requests.post(url, data=json.dumps(data), headers=headers)
        return result

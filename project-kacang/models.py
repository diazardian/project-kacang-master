import json
import requests

API_ENDPOINT = "http://127.0.0.1:8000/api/"
client = requests.session()

class Init:
    def guild_register(aidi, name):
        url = API_ENDPOINT + "MemberGuild/"
        headers = {"Content-Type": "application/json"}
        data = {"id_guild": aidi, "name": name}
        result = requests.post(url, data=json.dumps(data), headers=headers)
        return result


    def member_register(aidi, name, avatar, user_join, user_create, guild_id):
        url = API_ENDPOINT + "DiscordMember/"
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
        url = API_ENDPOINT + "GuildChannel/"
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

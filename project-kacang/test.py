from asyncio.windows_events import NULL
import requests

user = str(3934657916740567)

URL = "http://127.0.0.1:8000/api/DiscordMember/" + user
data = requests.get(url=URL).json()
print(data)
# if data == []:
#     print('ok')
# else:
#     print('tidak oke')

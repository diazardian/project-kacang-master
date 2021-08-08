import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
api = os.getenv("API_ENDPOINT")

aidi = str(809785532962832414)
name = "SEJUTA KACANG"

url = api + "MemberGuild/"
headers = {"Content-Type": "application/json"}
data = {"id_guild": aidi, "name": name}
result = requests.post(url, data=json.dumps(data), headers=headers)
print(result)
# if data == []:
#     print('ok')
# else:
#     print('tidak oke')

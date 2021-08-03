from urllib import request
import json
import datetime
url = "https://ibnux.github.io/BMKG-importer/cuaca/501191.json"

today = datetime.date.today()
print(today)
time_param = '18:00:00'
time_param = datetime.datetime.strptime(time_param, '%H:%M:%S')
response = request.urlopen(url)
data = json.loads(response.read())
w_cuaca = ''
for item in data:
	date_time_obj = datetime.datetime.strptime(item['jamCuaca'], '%Y-%m-%d %H:%M:%S')
	date = date_time_obj.date()
	time = date_time_obj.time()
	w_cuaca += f'Date : {date}\n'
	w_cuaca += f'Time : {time}\n\n'
	if time == time_param.time():
		break
print(w_cuaca)
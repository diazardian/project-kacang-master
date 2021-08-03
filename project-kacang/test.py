import json

with open('shop.json', 'r') as myfile:
    data=myfile.read()

obj = json.loads(data)
obj = obj['makanan'] + obj['minuman']
print(obj)

# stock = []
for i in obj:
    if i['name'] == 'ayam':
        stock = ((i['stock']))

print(stock)
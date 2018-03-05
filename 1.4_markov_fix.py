import pykov
import pymongo
from pymongo import MongoClient
client = MongoClient()
database = client.recommender
collection = database.data_lagu
collection2 = database.history_lagu

P = pykov.readmat('matriks.csv')
#print(T)
#print(P)
i = 0
for data in collection.find():
    print(data["index"],data["track name"], ' - ', data["artist name"])
response = input("Lagu yang akan diplay: ")
next = collection2.find_one({"index":int(response)})
if next == None:
    a = 0
else:
    a = next['played']
json = {
                'index': int(response),
                'played': a + 1
                }
collection2.update({'index':int(response)}, json, upsert=True)
next = collection.find_one({"index":int(response)})
print(next['track name'], ' - ', next['artist name'])
i = input("1. Cari lagu, 2. Putar lagu rekomendasi berikutnya, 3. Top 10 list lagu\n")
while i == '1' or i =='2' or i == '3':
    if i == '1':
        for data in collection.find():
            print(data["index"],data["track name"], ' - ', data["artist name"])
        response = input("Lagu yang akan diplay: ")
        next = collection2.find_one({"index":int(response)})
        if next == None:
            a = 0
        else:
            a = next['played']
        json = {
                'index': int(response),
                'played': a + 1
                }
        collection2.update({'index':int(response)}, json, upsert=True)
        next = collection.find_one({"index":int(response)})
        print(next['track name'], ' - ', next['artist name'])
        i = input("1. Cari lagu, 2. Putar lagu rekomendasi berikutnya 3. Top 10 list lagu\n")
    elif i == '2':
        next1 = collection.find_one({"index":int(P.move(str(next["index"])))})
        print(next1['track name'], ' - ', next1['artist name'])
        next = collection2.find_one({"index":next1['index']})
        if next == None:
            a = 0
        else:
            a = next['played']
        json = {
                'index': next1['index'],
                'played': a + 1
                }
        collection2.update({'index':next1['index']}, json, upsert=True)
        next = next1
        i = input("1. Cari lagu, 2. Putar lagu rekomendasi berikutnya 3. Top 10 list lagu\n")
    elif i == '3':
        y = 1
        data3 = []
        for data in collection2.find(limit = 10).sort('played',-1):
            data2 = collection.find_one({"index":data['index']})
            data3.append(data['index'])
            print(y, data2['track name'], ' - ', data2['artist name'], ' Played : ',
                  data['played'])
            y = y + 1
        x = input("\n1. Play from top 10 , 2. Back to menu\n")
        if x == '1':
            response = input("Lagu yang akan diplay: ")
            next = collection2.find_one({"index":data3[int(response)-1]})
            if next == None:
                a = 0
            else:
                a = next['played']
            json = {
                        'index': data3[int(response)-1],
                        'played': a + 1
                        }
            collection2.update({'index':data3[int(response)-1]}, json, upsert=True)
            next = collection.find_one({"index":int(response)})
            print(next['track name'], ' - ', next['artist name'])
        else:
            i = '1'

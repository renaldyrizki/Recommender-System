import math
import random
import pymongo
import csv
import pprint

from pymongo import MongoClient
client = MongoClient()

database = client.recommender
collection = database.data_lagu
cluster = database.data_cluster
matriks = database.data_matriks
with open('matriks.csv', 'w', newline='') as csvfile:
    writers = csv.writer(csvfile)
    for data in cluster.find():
        for data1 in collection.find():
            if data["cluster"] == data1["cluster"]:
                for data2 in collection.find():
                    #print(data1['cluster'])
                    #print(data2)
                    if data1["cluster"] == data2["cluster"]:
                        json = {
                            "cluster" : data["cluster"],
                            "from" : data1["index"],
                            "next" : data2["index"],
                            #"probability" : float("{0:.1f}".format((data2["average"]/data["average"])*100))
                            "probability" : data2["average"]/data["average"]
                            }
                        writers.writerow([data1["index"],data2["index"],
                                          json["probability"],json["cluster"]])
                        matriks.insert(json)
    print("Matriks Selesai")

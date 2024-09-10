import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
dbcl = mydb["cloth"]
dbel = mydb["event"]
dbul = mydb["user"]
print("cloth_______")
for x in dbcl.find():
    print(x) 
print("user_______")
for x in dbul.find():
    print(x) 
print("event_______")
for x in dbel.find():
    print(x) 

import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mydb.drop_collection("cloth")
mydb.drop_collection("event")
mydb.drop_collection("user")
dbcl = mydb["cloth"]
dbel = mydb["event"]
dbul = mydb["user"]

cl={101:{"clothcat":"Pant","clothsubcat":"Casual","clothcolor":"Blue","gender":"male","user":"admin","img":"pantc1.jpg"},
    102:{"clothcat":"Pant","clothsubcat":"Casual","clothcolor":"Brown","gender":"male","user":"admin","img":"pantc2.jpg"},
    103:{"clothcat":"Pant","clothsubcat":"Formal","clothcolor":"Green","gender":"male","user":"admin","img":"pantf1.jpg"},
    104:{"clothcat":"Pant","clothsubcat":"Formal","clothcolor":"Black","gender":"male","user":"admin","img":"pantf2.jpg"},
    105:{"clothcat":"Shirt","clothsubcat":"Casual","clothcolor":"Brown","gender":"male","user":"admin","img":"shirtc1.jpg"},
    106:{"clothcat":"Shirt","clothsubcat":"Casual","clothcolor":"Green","gender":"male","user":"admin","img":"shirtc2.jpg"},
    107:{"clothcat":"Shirt","clothsubcat":"Formal","clothcolor":"Brown","gender":"male","user":"admin","img":"shirtf1.jpg"},
    108:{"clothcat":"Shirt","clothsubcat":"Formal","clothcolor":"Black","gender":"male","user":"admin","img":"shirtf2.jpg"},
    109:{"clothcat":"Shalwar_Kameez","clothsubcat":"Casual","clothcolor":"Blue","gender":"male","user":"admin","img":"shkac1.jpg"},
    110:{"clothcat":"Shalwar_Kameez","clothsubcat":"Casual","clothcolor":"Green","gender":"male","user":"admin","img":"shkac2.jpg"},
    111:{"clothcat":"Shalwar_Kameez","clothsubcat":"Formal","clothcolor":"Brown","gender":"male","user":"admin","img":"shkaf1.jpg"},
    112:{"clothcat":"Shalwar_Kameez","clothsubcat":"Formal","clothcolor":"Black","gender":"male","user":"admin","img":"shkaf2.jpg"}}
for i in cl.keys():
    dbcl.insert_one({"_id":str(i),str(i):cl[i]})

el={101:{"name":"Birthday","casual":"T","formal":"F"},
    102:{"name":"Wedding","casual":"F","formal":"T"},
    103:{"name":"Concert","casual":"T","formal":"F"},
    104:{"name":"Interview","casual":"F","formal":"T"},
    105:{"name":"Engagement","casual":"F","formal":"T"}}
for i in el.keys():
    dbel.insert_one({"_id":str(i),str(i):el[i]})

ul={101:{"uname":"admin","pass":"admin","gender":"male"},
    102:{"uname":"test","pass":"test","gender":"male"}}
for i in ul.keys():
    dbul.insert_one({"_id":str(i),str(i):ul[i]})


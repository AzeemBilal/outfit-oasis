from flask import Flask,request,render_template
from flask import render_template
import random
import os
import pymongo
import pandas as pd
import numpy as np
from numpy.linalg import svd
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.neighbors import NearestNeighbors
from predict_data import predict_top_n_classes_loaded

data = {
    "Store_1": {'name': "Nike", 'price': 120.00, 'category': "Casual", 'url': "https://www.nike.com/"},
    "Store_2": {'name': "Adidas", 'price': 250.00, 'category': "Casual", 'url': "https://www.adidas.com/"},
    "Store_3": {'name': "Puma", 'price': 340.00, 'category': "Casual", 'url': "https://www.puma.com/"},
    "Store_4": {'name': "Under Armour", 'price': 470.00, 'category': "Casual", 'url': "https://www.underarmour.com/"},
    "Store_5": {'name': "Levi's", 'price': 580.00, 'category': "Casual", 'url': "https://www.levi.com/"},
    "Store_6": {'name': "Ralph Lauren", 'price': 600.00, 'category': "Casual", 'url': "https://www.ralphlauren.com/"},
    "Store_7": {'name': "Calvin Klein", 'price': 700.00, 'category': "Casual", 'url': "https://www.calvinklein.com/"},
    "Store_8": {'name': "Tommy Hilfiger", 'price': 880.00, 'category': "Casual", 'url': "https://www.tommy.com/"},
    "Store_9": {'name': "Hugo Boss", 'price': 900.00, 'category': "Formal", 'url': "https://www.hugoboss.com/"},
    "Store_10": {'name': "Diesel", 'price': 1220.00, 'category': "Casual", 'url': "https://www.diesel.com/"},
    "Store_11": {'name': "GAP", 'price': 1330.00, 'category': "Casual", 'url': "https://www.gap.com/"},
    "Store_12": {'name': "J.Crew", 'price': 1560.00, 'category': "Casual", 'url': "https://www.jcrew.com/"},
    "Store_13": {'name': "Banana Republic", 'price': 1560.00, 'category': "Formal", 'url': "https://www.bananarepublic.com/"},
    "Store_14": {'name': "Express", 'price': 1680.00, 'category': "Casual", 'url': "https://www.express.com/"},
    "Store_15": {'name': "American Eagle", 'price': 1800.00, 'category': "Casual", 'url': "https://www.ae.com/"},
    "Store_16": {'name': "Abercrombie & Fitch", 'price': 2300.00, 'category': "Casual", 'url': "https://www.abercrombie.com/"},
    "Store_17": {'name': "Urban Outfitters", 'price': 2700.00, 'category': "Casual", 'url': "https://www.urbanoutfitters.com/"},
    "Store_18": {'name': "Zara", 'price': 4330.00, 'category': "Casual", 'url': "https://www.zara.com/"},
    "Store_19": {'name': "H&M", 'price': 3000.00, 'category': "Casual", 'url': "https://www.hm.com/"},
    "Store_20": {'name': "ASOS", 'price': 2300.00, 'category': "Casual", 'url': "https://www.asos.com/"},
    "Store_21": {'name': "BOSS", 'price': 5500.00, 'category': "Formal", 'url': "https://www.boss.com/"},
    "Store_22": {'name': "Moncler", 'price': 5450.00, 'category': "Casual", 'url': "https://www.moncler.com/"},
    "Store_23": {'name': "Canada Goose", 'price': 5600.00, 'category': "Casual", 'url': "https://www.canadagoose.com/"},
    "Store_24": {'name': "Stone Island", 'price': 7800.00, 'category': "Casual", 'url': "https://www.stoneisland.com/"},
    "Store_25": {'name': "Prada", 'price': 7600.00, 'category': "Formal", 'url': "https://www.prada.com/"},
    "Store_26": {'name': "Gucci", 'price': 7000.00, 'category': "Formal", 'url': "https://www.gucci.com/"},
    "Store_27": {'name': "Burberry", 'price': 8000.00, 'category': "Formal", 'url': "https://www.burberry.com/"},
    "Store_28": {'name': "Balenciaga", 'price': 8900.00, 'category': "Formal", 'url': "https://www.balenciaga.com/"},
    "Store_29": {'name': "Saint Laurent", 'price': 9000.00, 'category': "Formal", 'url': "https://www.ysl.com/"},
    "Store_30": {'name': "Givenchy", 'price': 9200.00, 'category': "Formal", 'url': "https://www.givenchy.com/"},
    "Store_31": {'name': "Louis Vuitton", 'price': 9500.00, 'category': "Formal", 'url': "https://www.louisvuitton.com/"},
    "Store_32": {'name': "Hermès", 'price': 10000.00, 'category': "Formal", 'url': "https://www.hermes.com/"},
    "Store_33": {'name': "Bottega Veneta", 'price': 10200.00, 'category': "Formal", 'url': "https://www.bottegaveneta.com/"},
    "Store_34": {'name': "Fendi", 'price': 15000.00, 'category': "Formal", 'url': "https://www.fendi.com/"},
    "Store_35": {'name': "Mason's", 'price': 12000.00, 'category': "Casual", 'url': "https://www.masons.it/"},
    "Store_36": {'name': "Belstaff", 'price': 13000.00, 'category': "Casual", 'url': "https://www.belstaff.com/"},
    "Store_37": {'name': "Bogner", 'price': 15300.00, 'category': "Casual", 'url': "https://www.bogner.com/"},
    "Store_38": {'name': "Paul Smith", 'price': 20000.00, 'category': "Formal", 'url': "https://www.paulsmith.com/"},
    "Store_39": {'name': "Marni", 'price':14350.00, 'category': "Formal", 'url': "https://www.marni.com/"},
    "Store_40": {'name': "Rick Owens", 'price': 16700.00, 'category': "Formal", 'url': "https://www.rickowens.eu/"},
    "Store_41": {'name': "Alexander McQueen", 'price': 17800.00, 'category': "Formal", 'url': "https://www.alexandermcqueen.com/"},
    "Store_42": {'name': "Dolce & Gabbana", 'price': 19900.00, 'category': "Formal", 'url': "https://www.dolcegabbana.com/"},
    "Store_43": {'name': "Versace", 'price': 19950.00, 'category': "Formal", 'url': "https://www.versace.com/"},
    "Store_44": {'name': "Kenzo", 'price': 20320.00, 'category': "Formal", 'url': "https://www.kenzo.com/"},
    "Store_45": {'name': "Acne Studios", 'price': 20400.00, 'category': "Formal", 'url': "https://www.acnestudios.com/"},
    "Store_46": {'name': "Balmain", 'price': 23800.00, 'category': "Formal", 'url': "https://www.balmain.com/"},
    "Store_47": {'name': "Sandro", 'price': 23250.00, 'category': "Formal", 'url': "https://www.sandro-paris.com/"},
    "Store_48": {'name': "The Kooples", 'price': 25000.00, 'category': "Formal", 'url': "https://www.thekooples.com/"},
    "Store_49": {'name': "Giuseppe Zanotti", 'price': 28500.00, 'category': "Formal", 'url': "https://www.giuseppezanotti.com/"},
    "Store_50": {'name': "Giorgio Armani", 'price': 29200.00, 'category': "Formal", 'url': "https://www.armani.com/"},
    "Store_51": {'name': "Ermenegildo Zegna", 'price': 30500.00, 'category': "Formal", 'url': "https://www.zegna.com/"},
    "Store_52": {'name': "Canali", 'price': 401300.00, 'category': "Formal", 'url': "https://www.canali.com/"},
    "Store_53": {'name': "Kiton", 'price': 35000.00, 'category': "Formal", 'url': "https://www.kiton.com/"},
    "Store_54": {'name': "Corneliani", 'price': 33000.00, 'category': "Formal", 'url': "https://www.corneliani.com/"},
    "Store_55": {'name': "Hickey Freeman", 'price': 35500.00, 'category': "Formal", 'url': "https://www.hickeyfreeman.com/"},
    "Store_56": {'name': "Paul & Shark", 'price': 37350.00, 'category': "Casual", 'url': "https://www.paulshark.com/"},
    "Store_57": {'name': "Tasso Elba", 'price': 40250.00, 'category': "Formal", 'url': "https://www.tassoelba.com/"},
    "Store_58": {'name': "Tom Ford", 'price': 42000.00, 'category': "Formal", 'url': "https://www.tomford.com/"},
    "Store_59": {'name': "Boglioli", 'price': 45400.00, 'category': "Formal", 'url': "https://www.boglioli.com/"},
    "Store_60": {'name': "Loro Piana", 'price': 45000.00, 'category': "Formal", 'url': "https://www.loropiana.com/"},
    "Store_61": {'name': "John Varvatos", 'price': 50050.00, 'category': "Casual", 'url': "https://www.johnvarvatos.com/"},
    "Store_62": {'name': "Maison Margiela", 'price': 50000.00, 'category': "Formal", 'url': "https://www.maisonmargiela.com/"},
    "Store_63": {'name': "Gieves & Hawkes", 'price': 60000.00, 'category': "Formal", 'url': "https://www.gievesandhawkes.com/"},
    "Store_64": {'name': "Richard James", 'price': 70000.00, 'category': "Formal", 'url': "https://www.richardjames.co.uk/"},
    "Store_65": {'name': "Eton Shirts", 'price': 80000.00, 'category': "Formal", 'url': "https://www.etonshirts.com/"},
    "Store_66": {'name': "Huntsman", 'price': 90000.00, 'category': "Formal", 'url': "https://www.huntsmansavilerow.com/"},
    "Store_67": {'name': "Savile Row Company", 'price': 65000.00, 'category': "Formal", 'url': "https://www.savilerowcompany.com/"},
    "Store_68": {'name': "Suitsupply", 'price': 80000.00, 'category': "Formal", 'url': "https://www.suitsupply.com/"},
    "Store_69": {'name': "Moss Bros", 'price': 90000.00, 'category': "Formal", 'url': "https://www.moss.co.uk/"},
    "Store_70": {'name': "Reiss", 'price': 90250.00, 'category': "Formal", 'url': "https://www.reiss.com/"},
    "Store_71": {'name': "Burberry", 'price': 100600.00, 'category': "Formal", 'url': "https://www.burberry.com/"},
    "Store_72": {'name': "Ted Baker", 'price': 100220.00, 'category': "Formal", 'url': "https://www.tedbaker.com/"},
    "Store_73": {'name': "Paul Smith", 'price': 150270.00, 'category': "Formal", 'url': "https://www.paulsmith.com/"},
    "Store_74": {'name': "Ralph Lauren", 'price': 125800.00, 'category': "Formal", 'url': "https://www.ralphlauren.com/"},
    "Store_75": {'name': "Calvin Klein", 'price': 150400.00, 'category': "Formal", 'url': "https://www.calvinklein.com/"},
    "Store_76": {'name': "Tommy Hilfiger", 'price': 150180.00, 'category': "Casual", 'url': "https://www.tommy.com/"},
    "Store_77": {'name': "Diesel", 'price': 175220.00, 'category': "Casual", 'url': "https://www.diesel.com/"},
    "Store_78": {'name': "J.Crew", 'price': 180190.00, 'category': "Casual", 'url': "https://www.jcrew.com/"},
    "Store_79": {'name': "Banana Republic", 'price': 200300.00, 'category': "Formal", 'url': "https://www.bananarepublic.com/"},
    "Store_80": {'name': "Express", 'price': 200150.00, 'category': "Casual", 'url': "https://www.express.com/"},
    "Store_81": {'name': "American Eagle", 'price': 200140.00, 'category': "Casual", 'url': "https://www.ae.com/"},
    "Store_82": {'name': "Abercrombie & Fitch", 'price': 200200.00, 'category': "Casual", 'url': "https://www.abercrombie.com/"},
    "Store_83": {'name': "Urban Outfitters", 'price': 300250.00, 'category': "Casual", 'url': "https://www.urbanoutfitters.com/"},
    "Store_84": {'name': "Zara", 'price': 300280.00, 'category': "Casual", 'url': "https://www.zara.com/"},
    "Store_85": {'name': "H&M", 'price': 300140.00, 'category': "Casual", 'url': "https://www.hm.com/"},
    "Store_86": {'name': "ASOS", 'price': 300200.00, 'category': "Casual", 'url': "https://www.asos.com/"},
    "Store_87": {'name': "BOSS", 'price': 400500.00, 'category': "Formal", 'url': "https://www.boss.com/"},
    "Store_88": {'name': "Moncler", 'price': 400600.00, 'category': "Casual", 'url': "https://www.moncler.com/"},
    "Store_89": {'name': "Canada Goose", 'price': 400700.00, 'category': "Casual", 'url': "https://www.canadagoose.com/"},
    "Store_90": {'name': "Stone Island", 'price': 400500.00, 'category': "Casual", 'url': "https://www.stoneisland.com/"},
    "Store_91": {'name': "Prada", 'price': 400800.00, 'category': "Formal", 'url': "https://www.prada.com/"},
    "Store_92": {'name': "Gucci", 'price': 101000.00, 'category': "Formal", 'url': "https://www.gucci.com/"},
    "Store_93": {'name': "Burberry", 'price': 71200.00, 'category': "Formal", 'url': "https://www.burberry.com/"},
    "Store_94": {'name': "Balenciaga", 'price': 515000.00, 'category': "Formal", 'url': "https://www.balenciaga.com/"},
    "Store_95": {'name': "Saint Laurent", 'price': 518000.00, 'category': "Formal", 'url': "https://www.ysl.com/"},
    "Store_96": {'name': "Givenchy", 'price': 52000.00, 'category': "Formal", 'url': "https://www.givenchy.com/"},
    "Store_97": {'name': "Louis Vuitton", 'price': 63000.00, 'category': "Formal", 'url': "https://www.louisvuitton.com/"},
    "Store_98": {'name': "Hermès", 'price': 83500.00, 'category': "Formal", 'url': "https://www.hermes.com/"},
    "Store_99": {'name': "Bottega Veneta", 'price': 94000.00, 'category': "Formal", 'url': "https://www.bottegaveneta.com/"},
    "Store_100": {'name': "Fendi", 'price': 95000.00, 'category': "Formal", 'url': "https://www.fendi.com/"}
}


def get_recommendations(min_price, max_price):
    df = pd.DataFrame.from_dict(data, orient='index')

    # Extract price data
    price_data = df[['price']].values

    # Apply SVD
    U, S, VT = svd(price_data, full_matrices=False)

    # Reconstruct the matrix
    S_matrix = np.diag(S)
    reconstructed_matrix = np.dot(U, np.dot(S_matrix, VT))

    # Add reconstructed prices back to the DataFrame
    df['Reconstructed_Price'] = reconstructed_matrix

    # Filter stores within the range
    filtered_df = df[(df['Reconstructed_Price'] >= min_price) & (df['Reconstructed_Price'] <= max_price)]

    # Ensure we get at most 3 stores
    if len(filtered_df) > 3:
        filtered_df = filtered_df.sample(3)

    return filtered_df


loaded_pipeline = joblib.load('model.pkl')
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
dbcl = mydb["cloth"]
dbel = mydb["event"]
dbul = mydb["user"]
app = Flask(__name__)

username=""
cevent=""
gender=""
csubcat=""

sll={   "Store_1":["Sapphire","https://pk.sapphireonline.pk/collections/man"],
        "Store_2":["Outfitter","https://outfitters.com.pk"],
        "Store_3":["Deepak Perwani","https://www.deepakperwani.com/suits-and-jackets"],
        "Store_4":["Amir Adnan","https://amiradnan.com/collections/shop?gad_source=1&gclid=CjwKCAjwps-zBhAiEiwALwsVYfmqEsoM0FXE7pNbpaS0mAaIHEo30D0OG9483gdgFnUwq-Z8q_Y_ohoCZIMQAvD_BwE"],
        "Store_5":["Royal","https://royaltag.com.pk/collections/formals"],
        "Store_6":["Ismail Farid","https://www.ismailfarid.com/pages/shirts-collection"],
        "Store_7":["Diners","https://diners.com.pk/collections/diners-ethnic-wear"],
        "Store_8":["Hussain Rehar","https://www.hussainrehar.com/collections/menswear"],
        "Store_9":["Chester Bernard","https://chesterbernard.com/collections/online-shirts-for-men"],
        "Store_10":["Zellbury","https://zellbury.com/collections/men"],
        "Store_11":["AK Galleria","https://akgalleria.com/sale/levi-s-reg.html"],
        "Store_12":["Bonanza","https://bonanzasatrangi.com/collections/men"],
        "Store_13":["Junaid Jamshed","https://www.junaidjamshed.com/mens/kameez-shalwar.html"],
        "Store_14":["Gul Ahmed","https://www.gulahmedshop.com/mens-clothes"],
        "Store_15":["Eden Robe","https://edenrobe.com/collections/men"],
        "Store_16":["Diners","https://diners.com.pk/collections/diners-shalwar-kameez"],
        "Store_17":["Cougar","https://www.cougar.com.pk/collections/men-t-shirts"],
        "Store_18":["Charcoal","https://charcoal.com.pk/collections/limited-edition-shirts"],
        "Store_19":["Leisure Club","https://www.leisureclub.pk/collections/new-arrivals-men?gad_source=1&gclid=CjwKCAjwps-zBhAiEiwALwsVYUnUCCmBzOUqM1lFlTnKD0jct0T-UPlWucMdtjVFJ12slxv1g5zFWRoCgaQQAvD_BwE"],
        "Store_20":["Uni Worth Shop","https://uniworthshop.com/the-white-club"]
        }


cl={}

el={}
for x in dbel.find():
    for y in x.keys():
        if y != "_id":
            el.update({int(y):x[y]})
ul={}
for x in dbul.find():
    for y in x.keys():
        if y != "_id":
            ul.update({int(y):x[y]})

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/login')
def  login():
    username=""
    cl.clear
    return render_template("login.html")

@app.route('/next')
def  next():
    tcl=list(cl.keys())
    fstatus=0
    while(fstatus==0 or fstatus == 1 or fstatus == 2):
        tclid=random.randint(0, len(tcl)-1)
        if fstatus == 0 and cl[tcl[tclid]]["clothsubcat"]==csubcat and cl[tcl[tclid]]["user"]==username:
            pict1=cl[tcl[tclid]]["clothcat"]
            piim1=cl[tcl[tclid]]["img"]
            pict2=""
            piim2="white.jpg"
            if pict1 == "Shalwar_Kameez":
                fstatus=5
                break
            elif pict1 == "Pant":
                fstatus=1    
            elif pict1 == "Shirt":
                fstatus=2    
        elif fstatus == 1 and cl[tcl[tclid]]["clothsubcat"]==csubcat and cl[tcl[tclid]]["user"]==username:
            pict2=cl[tcl[tclid]]["clothcat"]
            piim2=cl[tcl[tclid]]["img"]
            if pict2 == "Shirt":
                fstatus=5
                break
            else:
                fstatus=1    
        elif fstatus == 2 and cl[tcl[tclid]]["clothsubcat"]==csubcat and cl[tcl[tclid]]["user"]==username:
            pict2=cl[tcl[tclid]]["clothcat"]
            piim2=cl[tcl[tclid]]["img"]
            if pict2 == "Pant":
                fstatus=5
                break
            else:
                fstatus=2    
    return render_template("personalinventory.html",se=cevent,pict1=pict1,piim1=piim1,pict2=pict2,piim2=piim2)

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/signupdata')
def signupdata():
    username=request.args.get("u1")
    password=request.args.get("p1")
    cpassword=request.args.get("p2")
    gender=request.args.get("gender")
    if username!="" and password!="" and cpassword!="" and gender!="" and password==cpassword:
        ulid=random.randint(1, 100000)
        ul.update({ulid:{"uname":username,"pass":password,"gender":gender}})
        dbul.insert_one({"_id":str(ulid),str(ulid):ul[ulid]})
        return render_template("login.html")         
    else:
        return render_template("signup.html",error="Invalid Username Or Password!")

@app.route('/logindata')
def logindata():
    global username
    global gender
    username = request.args.get('u1')
    password = request.args.get('p1')
    for i in ul.keys():
        data=ul[i]
        if data["uname"] == username and data["pass"]==password:
            gender=data["gender"]
            cl.clear
            for x in dbcl.find():
                for y in x.keys():
                    if y != "_id":
                        if (x[y]["user"]==username):
                            cl.update({int(y):x[y]})
            return render_template("main.html",un=username,elist=el)
    return render_template("login.html",error="Invalid Username Or Password!")

@app.route('/main')
def main():
    return render_template("main.html",un=username,elist=el)
  
@app.route('/event')
def event():
    return render_template("event.html",elist=el)

@app.route('/cloth')
def cloth():
    return render_template("cloth.html",clist=cl)

@app.route('/onlinepersonalsearch')
def onlinepersonalsearch():
    global cevent
    global csubcat
    se=request.args.get('select')
    cevent=el[int(se)]["name"]
    if el[int(se)]["casual"]=="T":
        csubcat="Casual"
    else:    
        csubcat="Formal"
    if request.args.get('os')=="T":
        return render_template("onlinesearch.html",se=cevent)
    elif request.args.get('pi')=="T":
        tcl=list(cl.keys())
        fstatus=0
        while(fstatus==0 or fstatus == 1 or fstatus == 2):
            tclid=random.randint(0, len(tcl)-1)
            if fstatus == 0 and cl[tcl[tclid]]["clothsubcat"]==csubcat and cl[tcl[tclid]]["user"]==username:
                pict1=cl[tcl[tclid]]["clothcat"]
                piim1=cl[tcl[tclid]]["img"]
                pict2=""
                piim2="white.jpg"
                if pict1 == "Shalwar_Kameez":
                    fstatus=5
                    break
                elif pict1 == "Pant":
                    fstatus=1    
                elif pict1 == "Shirt":
                    fstatus=2    
            elif fstatus == 1 and cl[tcl[tclid]]["clothsubcat"]==csubcat and cl[tcl[tclid]]["user"]==username:
                pict2=cl[tcl[tclid]]["clothcat"]
                piim2=cl[tcl[tclid]]["img"]
                if pict2 == "Shirt":
                    fstatus=5
                    break
                else:
                    fstatus=1    
            elif fstatus == 2 and cl[tcl[tclid]]["clothsubcat"]==csubcat and cl[tcl[tclid]]["user"]==username:
                pict2=cl[tcl[tclid]]["clothcat"]
                piim2=cl[tcl[tclid]]["img"]
                if pict2 == "Pant":
                    fstatus=5
                    break
                else:
                    fstatus=2    
    return render_template("personalinventory.html",se=cevent,pict1=pict1,piim1=piim1,pict2=pict2,piim2=piim2)

@app.route('/onlinesearch')
def onlinesearch():
    return render_template("onlinesearch.html",se=cevent)

@app.route('/searchresult')
def searchresult():
    clothcat=request.args.get('select')
    maxv=request.args.get('mxv')
    minv=request.args.get('mnv')
    price = (int(minv) + int(maxv)) / 2
    # machine learning model
    topresults = predict_top_n_classes_loaded(price, clothcat, n=5) 
    print(topresults[0][0])
    dtl={}
    for i in topresults:
        dtl.update({sll[i[0]][0]:sll[i[0]][1]})
    return render_template("searchresult.html",cc=clothcat,ssl=dtl)

@app.route('/addcloth',methods=['POST'])
def addcloth():
    image = request.files['image']
    if  image.filename != '':
        clid=random.randint(1, 10000)
        ccat = request.form['ccat']
        cscat = request.form['cscat']
        ccolor = request.form['cc']
        image.save('static/images/'+ str(clid)  +".jpg")
        cl.update({clid:{"clothcat":ccat,"clothsubcat":cscat,"clothcolor":ccolor,"gender":gender,"user":username,"img": str(clid) +".jpg"}})
        dbcl.insert_one({"_id":str(clid),str(clid):cl[clid]})
        return render_template("cloth.html",clist=cl)
    else:
        return render_template("cloth.html",clist=cl, imgerror="Invalid Image!")

@app.route('/deletecloth')
def deletecloth():
    delcloth = request.args.get('de')
    for i in cl.keys():
        if i ==int(delcloth):
            os.remove("static/images/"+cl[int(delcloth)]["img"])
            cl.pop(int(delcloth))
            dbcl.delete_one({"_id":delcloth})
            return render_template("cloth.html",clist=cl)
    return render_template("cloth.html",error="Invalid ID!",clist=cl)
    
@app.route('/addevent')
def addevent():
    eventname = request.args.get('en')
    eradio = request.args.get('cfc')
    if eradio == "c":
        check1="T"
        check2="F"
    elif eradio == "f":
        check1="F"
        check2="T"
    elid=random.randint(1, 100000)
    el.update({elid:{"name":eventname,"casual":check1,"formal":check2}})
    dbel.insert_one({"_id":str(elid),str(elid):el[elid]})
    return render_template("event.html",elist=el)

@app.route('/deleteevent')
def deleteevent():
    deleteevent = request.args.get('de')
    for i in el.keys():
        if i ==int(deleteevent) :
            el.pop(int(deleteevent))
            dbel.delete_one({"_id":deleteevent})
            return render_template("event.html",elist=el)
    return render_template("event.html",error="Invalid ID!",elist=el)

@app.route('/image/<img>')
def display_image(img):
    return render_template('display_image.html', image_url=img)


@app.route('/ai_searchresult', methods=['GET'])
def ai_searchresult():
    category = request.args.get('select')
    min_price = float(request.args.get('mnv', 0))
    max_price = float(request.args.get('mxv', float('inf')))


    filtered_stores = get_recommendations(min_price, max_price)

    # Filter stores by category if specified
    if category:
        filtered_stores = filtered_stores[filtered_stores['category'] == category]

    # Convert to dictionary for template
    stores = filtered_stores[['name', 'price', 'url']].to_dict('index')
    return render_template('ai_searchresult.html', stores=stores)


if __name__ == '__main__':
    app.run(debug=True)

def predict_top_n_classes_loaded(price, category, n=3):
    single_record = pd.DataFrame([[price, category]], columns=['price', 'category'])
    probabilities = loaded_pipeline.predict_proba(single_record)
    top_n_indices = np.argsort(probabilities[0])[-n:][::-1]
    top_n_classes = [loaded_pipeline.classes_[i] for i in top_n_indices]
    top_n_probabilities = probabilities[0][top_n_indices]
    return list(zip(top_n_classes, top_n_probabilities))
    
if __name__ == '__main__':
    app.run(debug=True)
    
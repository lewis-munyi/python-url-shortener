import sqlite3
from random import randint
from datetime import datetime
samples = [
    "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/delish-190808-baked-drumsticks-0217-landscape-pf-1567089281.jpg"
    "https://natashaskitchen.com/wp-content/uploads/2020/01/Whole-Chicken.jpg",
    "https://thestayathomechef.com/wp-content/uploads/2020/01/Cajun-Chicken-Drumsticks-1-1.jpg",
    "https://www.simplyrecipes.com/wp-content/uploads/2019/03/HT-Make-Roast-Chicken-LEAD-5v2.jpg",
    "https://s23209.pcdn.co/wp-content/uploads/2019/01/Instant-Pot-Rotisserie-ChickenIMG_8266.jpg",
    "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fimages.media-allrecipes.com%2Fuserphotos%2F389250.jpg",
    "https://recipetineats.com/wp-content/uploads/2018/05/Chicken-Stew_5.jpg",
    "https://www.jessicagavin.com/wp-content/uploads/2014/01/buttermilk-fried-chicken-11-1200.jpg",
    "https://cafedelites.com/wp-content/uploads/2019/09/HERO-Cajun-Butter-Chicken-Breasts-1.jpghttps://food.fnr.sndimg.com/content/dam/images/food/fullset/2012/11/2/0/DV1510H_fried-chicken-recipe-10_s4x3.jpg.rend.hgtvcom.826.620.suffix/1568222255998.jpeg",
    "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/delish-190808-baked-drumsticks-0217-landscape-pf-1567089281.jpg",
    "https://thestayathomechef.com/wp-content/uploads/2020/01/Cajun-Chicken-Drumsticks-1-1.jpg",
    "https://natashaskitchen.com/wp-content/uploads/2020/01/Whole-Chicken.jpg",
    "https://www.simplyrecipes.com/wp-content/uploads/2019/03/HT-Make-Roast-Chicken-LEAD-5v2.jpg",
    "https://s23209.pcdn.co/wp-content/uploads/2019/01/Instant-Pot-Rotisserie-ChickenIMG_8266.jpg",
    "https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fimages.media-allrecipes.com%2Fuserphotos%2F389250.jpg",
    "https://recipetineats.com/wp-content/uploads/2018/05/Chicken-Stew_5.jpg"
]

class Database(object):
    """
    Everything Database
    """
    db = None
    connection = None

    def __init__(self):
        pass

    def Connect(self):
        try:
            self.connection = sqlite3.connect('database.sqlite')
            self.db = self.connection.cursor()
            # print("connection successful")
            return
        except ConnectionError as error:
            return print("Cannot connect to database: " + error)

    def Disconnect(self):
        pass

    def Migrate(self):
        if(self.db == None):
            return print("You are not connected to any Database")

        try:
            self.db.execute('''CREATE TABLE urls ([id] INTEGER PRIMARY KEY AUTOINCREMENT,[short_url] text, [long_url] text, [date] date, UNIQUE(short_url))''')
            self.connection.commit()
            print("Migrated tables successfully")
        except Exception as e:
            print("Error on migration " + e)
            pass

    def Seed(self):
        print("Seeding")
        try:
            for i in range(0, len(samples)):
                x = randint(111111, 999999)
                print (x)
                self.db.execute("""INSERT INTO urls (short_url, long_url, date) VALUES (?, ?, ?)""", (x, samples[i], datetime.now()))
            self.connection.commit()
        except Exception as e:
            print(e)

    def query(self, query):
        # print(query)
        if(query  == None or query == ""):
            return ("No query supplied")

        return self.db.execute('SELECT * FROM urls where long_url = ?', (query,))

    def queryShortCode(self, code):
        # print(query)
        if(code  == None or code == ""):
            return ("No code supplied")

        return self.db.execute('SELECT * FROM urls where short_url = ?', (code,))

    def Create(self, short, url):
        try:
            self.db.execute("""INSERT INTO urls (short_url, long_url, date) VALUES (?, ?, ?)""", (short, url, datetime.now()))
            new_url = self.db.lastrowid
            self.connection.commit()
            return self.db.execute('SELECT * FROM urls where id = ?', (new_url,))
        except Exception as e:
            print("Error while saving")
            print(e)
            pass
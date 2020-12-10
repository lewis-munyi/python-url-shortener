from app.database import Database
from urllib.parse import urlparse
from uuid import uuid4

class Shortener(object):
    long_url = ""
    short_url = ""
    db = None

    def __init__(self):
        self.db = Database()
        self.db.Connect()
        # db.Connect()
        # self.db.Migrate()
        # self.db.Seed()
        # result = db.query(731927)
        # print(result.fetchone()[0])
        pass

    def checkIfExists(self, url):
        result = self.db.query(url)
        try:
            if(result.fetchone()[0]):
                return result.fetchone()
        except Exception as e:
            return False

    def checkIfCodeExists(self, code):
        result = self.db.queryShortCode(code)
        try:
            if(result.fetchone()[0]):
                # Exists
                return True
        except Exception as e:
            return False

    def checkIfURLIsValid(self, url):
        isValid = bool(urlparse(url).scheme)
        # print(isValid)
        return isValid


    def generateShortCode(self):
        loop = True
        while loop:
            rand = str(uuid4())[:6]
            if(not self.checkIfCodeExists(rand)):
                loop = False
        return rand

    def shorten(self, url):
        rand = self.generateShortCode()
        # print(rand)
        new_url = self.save(rand, url)
        print("Your URL shortcode is: " + str(new_url.fetchone()[1]))
        pass

    def resolve(self, url):
        # return a long URL string
        pass

    def save(self, code, url):
        return self.db.Create(code, url)

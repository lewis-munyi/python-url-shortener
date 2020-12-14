import os
from uuid import uuid4
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from urllib.parse import urlparse, quote_plus, unquote
from flask import Flask, request, jsonify, render_template, redirect

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# URL Class/Model
class Url(db.Model):
    code = db.Column(db.String(100), primary_key=True)
    url = db.Column(db.String(200), unique=True)
    date = db.Column(db.Date())

    def __init__(self, code, url, date):
        self.code = code
        self.url = url
        self.date = date

# URL Schema
class UrlSchema(ma.Schema):
    class Meta:
        fields = ('code', 'url')

# Init schema
url_schema = UrlSchema()
urls_schema = UrlSchema(many=True)

# Create a URL
@app.route('/', methods=['GET', 'POST', 'DELETE'])
def add_url():
    # Load Home page
    if request.method == "GET":
        return render_template('index.html', payload = None)

    # Delete URL
    if request.method == "DELETE":
        # Get URL code
        code = request.form['url']
        url = Url.query.get(code)

        # Delete record
        db.session.delete(url)
        db.session.commit()

        return url_schema.jsonify(url)

    try:
        # Delete URL
        if( request.form['delete']):
            # Get URL code
            code = request.form['url']
            url = Url.query.get(code)

            # Delete record
            db.session.delete(url)
            db.session.commit()

            # Return new URL list
            result = urls_schema.dump(Url.query.all())
            return render_template("table.html", payload = result)
    except:
        url = request.form['url']

        # Assert valid link is supplied
        if(not bool(urlparse(url).scheme)):
            return render_template('index.html', payload = "Error")

        # Return Link if exists
        for link in Url.query.all():
            if(link.url == url):
                return render_template('index.html', payload = link)

        # Generate unique identifier
        loop = True
        while(loop):
            code = str(uuid4())[:6]

            # If code already exists create a new one, otherwise break
            exists = Url.query.get(code)
            if(exists == None):
                loop = False

        # Save new URL object
        new_url = Url(code, url, datetime.now())
        db.session.add(new_url)
        db.session.commit()

        return render_template('index.html', payload = new_url)


# Get Single URL
@app.route('/<code>', methods=['GET'])
def get_url(code):
    # Fetch all URLs
    if(code == "urls"):
        all_urls = Url.query.all()
        result = urls_schema.dump(all_urls)
        return render_template("table.html", payload = result)

    # Redirect to link
    url = Url.query.get(code)
    if(url is None):
        return render_template('404.html')
    url = url_schema.dump(url)
    return redirect(url["url"])

# Run Server
if __name__ == '__main__':
    # Run migrations
    try:
        db.create_all()
        print("Migrated tables successfully")
    except:
        print("Error Migrating tables. They might already exist")

    app.run(debug=True)
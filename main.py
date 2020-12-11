import os
import urllib
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

@app.route('/', methods=['GET'])
def load_home():
    return render_template('index.html', payload = None)

# Create a URL
@app.route('/', methods=['POST'])
def add_url():
#   url = request.json['url']
  url = request.form['url']

  if(not bool(urlparse(url).scheme)):
    return render_template('index.html', payload = "Error")

  for link in Url.query.all():
    if(link.url == quote_plus(url)):
      return render_template('index.html', payload = link)

   # Generate unique identifier
  loop = True
  while(loop):
      code = str(uuid4())[:6]
      exists = Url.query.get(code)

      if(exists == None):
        loop = False

  new_url = Url(code, quote_plus(url), datetime.now())

  db.session.add(new_url)
  db.session.commit()

#   x = url_schema.jsonify(new_url)

  return render_template('index.html', payload = new_url)

#   return url_schema.jsonify(new_url)

# Get Single URL
@app.route('/<code>', methods=['GET'])
def get_url(code):
  # Fetch all URLs
  if(code == "urls"):
    all_urls = Url.query.all()
    result = urls_schema.dump(all_urls)
    return jsonify(result)

  # Redirect to link
  url = Url.query.get(code)
  url = url_schema.dump(url)
#   return url_schema.jsonify(url)
  return redirect(unquote(url["url"]), code=200)

# Delete Short URL
@app.route('/<code>', methods=['DELETE'])
def delete_url(code):
  url = Url.query.get(code)
  db.session.delete(url)
  db.session.commit()
  return url_schema.jsonify(url)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)
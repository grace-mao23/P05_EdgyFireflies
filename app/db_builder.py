
from __init__ import app, db
from app import auth, books, friends
from urllib.request import urlopen
import urllib.request as urllib
import json

with app.app_context():
    db.drop_all()
    db.create_all()
    url = "https://openlibrary.org/api/books?bibkeys=ISBN:" + str(isbn) "&jscmd=data&format=json"
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    req = urllib.Request(url, headers=hdr)
    data = json.loads(urllib.urlopen(req).read())

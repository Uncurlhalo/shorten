#!/usr/bin/env python3
import os
import sys
import hashlib
import random
import string
from flask import Flask, jsonify, render_template, redirect, abort
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import urlparse

app = Flask(__name__)
db = SQLAlchemy(app)

class Url(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=True)
    short_id =  db.Column(db.String)

    def __init__(self, url, short_id):
        self.url = url
        self.short_id = short_id

    def __repr__(self):
        """Return string representation"""
        return "<URL(id='%s', short_id='%s', url='%s')>" % (self.id, self.short_id, self.url)

    def valid(self):
        """Check if URL is valid"""
        parsed = urlparse(self.url)
        return parsed[0] in ('http', 'https') \
            and len(parsed[1]) > 0 \
            and '.' in parsed[1]

    def as_dict(self):
        """Return dictionary that can safely be serialized"""
        return {
            'url': self.url,
            'short_id': self.short_id
        }

@app.route('/l/')
def index():
    """Render index template"""
    return render_template('index.html')

@app.route('/l/<string:short_id>')
def get(short_id):
    """Look up the url by short_id"""

    if not short_id.isalnum():
        abort(400)
    try:
        url =  db.session.query(Url).filter_by(short_id=short_id).one()
    except sqlalchemy.orm.exc.NoResultFound:
        print("url key does not exist")
        abort(404)
    except sqlalchemy.orm.exc.MultipleResultsFound:
        print("multiple results when result should be unique or none")
        abort(500)
    return redirect(url.url, 302)

@app.route('/l/', methods=['POST'])
def add():
    """Add a url to the db"""
    u = request.form['url']
    if not u.startswith('http://') and not u.startswith('https://'):
        u = 'http://' + u
    """Check that the url isnt already in the db"""
    url = db.session.query(Url).filter_by(url=u).first()
    if url is not None:
        return jsonify(url.as_dict())
    short_id = gen_short_id()
    url = Url(u, short_id)
    if not url.valid():
        abort(400)
    try:
        db.session.add(url)
        db.session.commit()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    return jsonify(url.as_dict())

def gen_short_id():
    """Generate a random unique short_id"""
    short_id = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(8))
    while db.session.query(Url).filter_by(short_id=short_id).first() is not None:
        short_id = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(8))

    return short_id

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////srv/db/urls.db'
        app.debug = True
        db.drop_all()
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
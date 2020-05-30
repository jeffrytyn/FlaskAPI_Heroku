from db import db

import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #prevents flask-sqlalchemy from tracking changes to the database
                                                    # regular SQLAlchemy does it instead
app.secret_key = 'jeff'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all() #creates the data.db file and all tables

jwt = JWT(app, authenticate, identity)  #/auth endpoint, returns access token

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__': #prevents app from being run if its imported into another file
    db.init_app(app)
    app.run(debug=True)
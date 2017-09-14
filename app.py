from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.month import Month, MonthList
from resources.season import Season
from resources.vegetable import Vegetable, VegetableList

import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Month, '/month/<string:name>')
api.add_resource(MonthList, '/months')
api.add_resource(Vegetable, '/vegetable/<string:name>')
api.add_resource(VegetableList, '/vegetables')
api.add_resource(Season, '/season/<int:vegetable_id>/<int:month_id>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)

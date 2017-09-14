from flask_restful import Resource
from flask_jwt import jwt_required
from models.models import MonthModel


class Month(Resource):
    @jwt_required()
    def get(self, name):
        month = MonthModel.find_by_name(name)

        if month:
            return month.to_json()

        return {'message': 'Month not found.'}, 404


class MonthList(Resource):
    @jwt_required()
    def get(self):
        return {'months': [month.name for month
                           in MonthModel.query.all()]}

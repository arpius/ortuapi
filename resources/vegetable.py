from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.models import VegetableModel


class Vegetable(Resource):
    parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, name):
        vegetable = VegetableModel.find_by_name(name)

        if vegetable:
            return vegetable.to_json()

        return {'message': 'Vegetable not found.'}, 404

    @jwt_required()
    def post(self, name):
        vegetable = VegetableModel.find_by_name(name)

        if vegetable:
            return {'message': "A vegetable with name '{}' already exists."
                    .format(name)}, 400

        data = Vegetable.parser.parse_args()
        vegetable = VegetableModel(name, **data)

        try:
            vegetable.save_to_db()
        except:
            return {"message": "Error inserting data."}, 500

        return vegetable.to_json(), 201

    @jwt_required()
    def put(self, name):
        data = Vegetable.parser.parse_args()
        vegetable = VegetableModel.find_by_name(name)

        vegetable.season = data['season']

        if vegetable is None:
            vegetable = VegetableModel(name, **data)

        vegetable.save_to_db()

        return vegetable.to_json()

    @jwt_required()
    def delete(self, name):
        vegetable = VegetableModel.find_by_name(name)

        if vegetable:
            vegetable.delete_from_db()

        return {'message': 'Vegetable deleted.'}


class VegetableList(Resource):
    @jwt_required()
    def get(self):
        return {'vegetables': [vegetable.to_json() for vegetable
                               in VegetableModel.query.all()]}

from flask_restful import Resource
from flask_jwt import jwt_required
from models.models import SeasonModel
from sqlalchemy.exc import IntegrityError


class Season(Resource):
    @jwt_required()
    def post(self, vegetable_id, month_id):
        season = SeasonModel(vegetable_id, month_id)

        try:
            season.save_to_db()
        except IntegrityError:
            return {'message': 'Season already exists'}, 400

        return {'message': 'Season added succesfully'}, 201

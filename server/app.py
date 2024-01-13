from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# ... (Your existing routes and classes)

class PlantUpdate(Resource):

    def patch(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return make_response(jsonify({"error": "Plant not found"}), 404)

        data = request.get_json()

        # Update plant attributes based on the data received
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']

        db.session.commit()

        return make_response(jsonify(plant.to_dict()), 200)


api.add_resource(PlantUpdate, '/plants/<int:id>/update')


class PlantDestroy(Resource):

    def delete(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return make_response(jsonify({"error": "Plant not found"}), 404)

        db.session.delete(plant)
        db.session.commit()

        return make_response('', 204)


api.add_resource(PlantDestroy, '/plants/<int:id>/destroy')

# ... (Your existing code)

if __name__ == '__main__':
    app.run(debug=True)

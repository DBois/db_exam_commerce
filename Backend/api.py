# Flask dependencies
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

# Other dependencies
import psycopg2
from pprint import pprint

# # Local imports
from mongodb import MongoDB
import neo4j
from postgres import Postgres
from redis_logic import Redis

app = Flask(__name__)
api = Api(app)


class Order(Resource):
    def __init__(self):
        self.redis = Redis()
        self.postgres = Postgres()
        self.mongodb = MongoDB()

    def post(self):

        # Get user_id and shopping_cart
        user_id = request.json.get("user_id")
        redis_shopping_cart = self.redis.get_shopping_cart(user_id)


        # Fetch the items based on the shopping_cart (PSQL)
        items = self.postgres.fetch_shopping_cart_items(redis_shopping_cart)

        # Fetch the user information and credit card if existing (PSQL)


        # Create order on mongoDB

        # Create the graph on neo4j

    def get(self):
        return {'hello': 'world'}


class ShoppingCart(Resource):
    def __init__(self):
        self.redis = Redis()
        self.postgres = Postgres()
        self.mongodb = MongoDB()

    def post(self):

        user_id = request.json.get("user_id")
        product_no = request.json.get("product_no")
        qty = request.json.get("qty")

        shopping_cart = dict(self.redis.update_shopping_cart(user_id, product_no, qty).items())

        return shopping_cart

    def get(self):
        user_id = request.args["user_id"]

        return self.redis.get_shopping_cart(user_id)


api.add_resource(Order, '/order')
api.add_resource(ShoppingCart, '/shoppingcart')

if __name__ == '__main__':
    app.run(debug=True)

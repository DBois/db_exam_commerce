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

# Instantiate databases
redis = Redis()
postgres = Postgres()
mongodb = MongoDB()


class Order(Resource):
    def post(self):
        # Get user_id and shopping_cart
        user_id = request.json.get("user_id")
        redis_shopping_cart = redis.get_shopping_cart(user_id)

        # Fetch the items based on the shopping_cart (PSQL)
        items = postgres.fetch_shopping_cart_items(redis_shopping_cart)

        # Create order on mongoDB
        mongodb.make_order(user_id, items)

        # Create the graph on neo4j

    def get(self):
        return {'hello': 'world'}


class ShoppingCart(Resource):
    def post(self):
        user_id = request.json.get("user_id")
        product_no = request.json.get("product_no")
        qty = request.json.get("qty")

        shopping_cart = dict(redis.update_shopping_cart(user_id, product_no, qty).items())

        return shopping_cart

    def get(self):
        user_id = request.args["user_id"]

        return redis.get_shopping_cart(user_id)


api.add_resource(Order, '/order')
api.add_resource(ShoppingCart, '/shoppingcart')

if __name__ == '__main__':
    app.run(debug=True)

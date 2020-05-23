# Flask dependencies
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

# Other dependencies
import psycopg2
from pprint import pprint

# # Local imports
from mongodb import MongoDB
from neo4j_logic import Neo4jDAO
from postgres import Postgres
from redis_logic import Redis
from utils import build_order

app = Flask(__name__)
api = Api(app)


class Order(Resource):
    def __init__(self):
        # Instantiate databases
        self.redis = Redis()
        # postgres = Postgres()
        self.mongodb = MongoDB()
        self.neo4j_dao = Neo4jDAO()

    def post(self):
        # Get user_id and shopping_cart
        user_id = request.json.get("user_id")
        print(f"user_id: {user_id}")
        redis_shopping_cart = self.redis.get_shopping_cart(user_id)

        # Fetch the items based on the shopping_cart (PSQL)
        items = self.postgres.fetch_shopping_cart_items(redis_shopping_cart)

        # Build order
        order = build_order(items, user_id)

        # Create order on mongoDB
        self.mongodb.insert_order(order)

        # Create the graph on neo4j
        pprint(order)
        self.neo4j_dao.execute_create_order(order)
        self.neo4j_dao.close()

    def get(self):
        return {'hello': 'world'}


class ShoppingCart(Resource):
    def __init__(self):
        # Instantiate databases
        self.redis = Redis()

    def post(self):
        user_id = request.json.get("user_id")
        product_no = request.json.get("product_no")
        qty = request.json.get("qty")

        shopping_cart = dict(self.redis.update_shopping_cart(user_id, product_no, qty).items())

        return shopping_cart

    def get(self):
        user_id = request.args["user_id"]

        return self.redis.get_shopping_cart(user_id)


class RecommendedItems(Resource):
    def get(self):
        args = request.args
        print(args)  # For debugging
        item_num = args['key1']


api.add_resource(Order, '/order')
api.add_resource(ShoppingCart, '/shoppingcart')

if __name__ == '__main__':
    app.run(debug=True)

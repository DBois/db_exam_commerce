# Flask dependencies
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

# Other dependencies
import psycopg2
from pprint import pprint

# # Local imports
from mongodb import MongoDB
from neo4j_dao import Neo4jDAO
from postgres import Postgres
from redis_dao import RedisDAO
from utils import build_order

app = Flask(__name__)
api = Api(app)


class Order(Resource):
    def __init__(self):
        # Instantiate databases
        self.redis = RedisDAO()
        self.postgres = Postgres()
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

    def get(self):
        return {'hello': 'world'}


class ShoppingCart(Resource):
    def __init__(self):
        # Instantiate databases
        self.redis = RedisDAO()
        self.postgres = Postgres()
        self.mongodb = MongoDB()
        self.neo4j_dao = Neo4jDAO()

    def post(self):
        user_id = request.json.get("user_id")
        product_no = request.json.get("product_no")
        qty = request.json.get("qty")

        shopping_cart = dict(self.redis.update_shopping_cart(user_id, product_no, qty).items())

        return shopping_cart

    def get(self):
        user_id = request.args["user_id"]
        return self.redis.get_shopping_cart(user_id)

    def delete(self):
        user_id = request.json.get("user_id")
        product_no = request.json.get("product_no")
        return f"Removed {self.redis.delete_item(user_id, product_no)} item(s)"


class RecommendedItems(Resource):
    def __init__(self):
        # Instantiate databases
        self.neo4j_dao = Neo4jDAO()

        related_items = self.neo4j_dao = Neo4jDAO()
        


    def get(self):
        item_no = request.args["item_no"]
        items = self.neo4j_dao.execute_get_related_items()
        


class MostPopularItems(Resource):
    def __init__(self):
        self.mongodb = MongoDB()
    def post(self):
        days = request.json.get('days');
        return self.mongodb.generate_most_popular_products(days)


api.add_resource(Order, '/order')
api.add_resource(MostPopularItems, '/order/popular_products')
api.add_resource(ShoppingCart, '/shoppingcart')

if __name__ == '__main__':
    app.run(debug=True)

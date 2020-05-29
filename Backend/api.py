# Flask dependencies
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

# Other dependencies

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
        redis_shopping_cart = self.redis.get_shopping_cart(user_id)

        # Fetch the products based on the shopping_cart (PSQL)
        products = self.postgres.fetch_shopping_cart_products(redis_shopping_cart)

        # Build order
        order = build_order(products, user_id)

        # Prepare transaction in postgres to count down qty of bought products
        transaction_id = self.postgres.prepare_update_product_qty(order)

        # Create order on mongoDB
        mongo_id = self.mongodb.insert_order(order)

        # Commit/rollback transaction in postgres
        if mongo_id:
            self.postgres.commit_prepared_transaction(transaction_id)
            # Delete shoppingcart in redis
            self.redis.delete_shopping_cart(user_id)
            # Create the graph on neo4j
            self.neo4j_dao.execute_create_order(order)
        else:
            self.postgres.rollback_prepared_transaction(transaction_id)

        return_order = self.mongodb.get_order(mongo_id)
        del return_order['_id']

        self.postgres.close_connection()
        self.mongodb.close_connection()

        return return_order


class ShoppingCart(Resource):
    def __init__(self):
        # Instantiate databases
        self.redis = RedisDAO()

    def post(self):
        user_id = request.json.get("user_id")
        product_no = request.json.get("product_no")
        qty = request.json.get("qty")

        shopping_cart = dict(self.redis.update_shopping_cart(user_id, product_no, qty).products())

        return shopping_cart

    def get(self):
        user_id = request.args["user_id"]
        return self.redis.get_shopping_cart(user_id)

    def delete(self):
        user_id = request.json.get("user_id")
        product_no = request.json.get("product_no")
        return f"Removed {self.redis.delete_product(user_id, product_no)} product(s)"


class RecommendedProducts(Resource):
    def __init__(self):
        # Instantiate databases
        self.neo4j_dao = Neo4jDAO()

    def get(self):
        product_no = request.args["product_no"]
        products = self.neo4j_dao.execute_get_related_products(product_no)
        return jsonify(products)


class MostPopularProducts(Resource):
    def __init__(self):
        self.mongodb = MongoDB()

    def get(self):
        return self.mongodb.get_most_popular_products_30days()

    def post(self):
        days = request.json.get('days');
        return self.mongodb.generate_most_popular_products(days)


api.add_resource(Order, '/order')
api.add_resource(MostPopularProducts, '/order/popular_products')
api.add_resource(ShoppingCart, '/shoppingcart')
api.add_resource(RecommendedProducts, '/recommended_products')

if __name__ == '__main__':
    app.run(debug=True)

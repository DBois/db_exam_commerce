# Flask dependencies
from flask import Flask, request
from flask_restful import Resource, Api

# # Local imports
import mongodb
import neo4j
import postgres
from redis import Redis

app = Flask(__name__)
api = Api(app)


# class Order(Resource):
#     def post(self):
#         user_id = request.json.get("user_id")
#         product_no = request.json.get("product_no")
#         qty = request.json.get("qty")
#         redis = Redis()
#
#         return redis.update_shopping_cart(user_id, product_no, qty)
#
#     def get(self):
#         return {'hello': 'world'}

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')
# api.add_resource(Order, '/order')

if __name__ == '__main__':
    app.run(debug=True)
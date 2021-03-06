from pymongo import MongoClient
from bson.code import Code
from datetime import datetime, timedelta


class MongoDB:
    def __init__(self):
        self.client = MongoClient("mongodb://dboisAdmin:dbois@127.0.0.1")

    def insert_order(self, order):
        try:
            orders = self.client.db_exam_orders.orders
            inserted_id = orders.insert_one(order).inserted_id
            return inserted_id
        except Exception as ex:
            raise ex

    def generate_most_popular_products(self, days=30):
        try:
            map = Code("function () {"
                       "const products = this.Products;"
                       "products.forEach((product) => {"
                       "emit(product.ProductNo, product.Quantity);"
                       "});}")
            reduce = Code("function (key, values) {"
                          "return Array.sum(values);}")
            current_date = datetime.now()
            new_date = current_date - timedelta(days=days)
            results = self.client.db_exam_orders.orders.map_reduce(map, reduce, f"mostPopularProducts{days}",
                                                                   query={"InvoiceDate": {"$gte": new_date}})
            return "mostPopularProducts table created succesfully"
        except Exception as ex:
            raise ex

    def get_most_popular_products_30days(self):
        try:
            result = self.client.db_exam_orders.mostPopularProducts30.find().sort([("value", -1)]).limit(10)
            products = [product for product in result]
            return products
        except Exception as ex:
            raise ex

    def get_order(self, id):
        orders = self.client.db_exam_orders.orders
        return orders.find_one({"_id": id})

    def close_connection(self):
        self.client.close()

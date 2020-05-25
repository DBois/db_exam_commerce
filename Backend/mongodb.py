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
            self.client.close()
            return inserted_id

        except:
            raise print("Something went wrong when making order on MongoDB")
    
    def generate_most_popular_products(self, days):
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
            results = self.client.db_exam_orders.orders.map_reduce(map, reduce, f"mostPopularProducts{days}", query={"InvoiceDate": {"$gte": new_date}})
            return "mostPopularProducts table created succesfully"
        except Exception as ex:
            raise ex
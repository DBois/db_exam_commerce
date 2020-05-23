from pymongo import MongoClient
from utils import build_order


class MongoDB:
    def __init__(self):
        self.client = MongoClient()

    def insert_order(self, order):
        try:
            orders = self.client.db_exam_orders.orders
            return orders.insert_one(order).inserted_id
        except:
            raise print("Something went wrong when making order on MongoDB")

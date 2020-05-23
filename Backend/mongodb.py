from pymongo import MongoClient


class MongoDB:
    def __init__(self):
        self.client = MongoClient()

    def insert_order(self, order):
        try:
            orders = self.client.db_exam_orders.orders
            inserted_id = orders.insert_one(order).inserted_id
            self.client.close()
            return inserted_id

        except:
            raise print("Something went wrong when making order on MongoDB")

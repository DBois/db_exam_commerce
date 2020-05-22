from pymongo import MongoClient
from pprint import pprint


class MongoDB:
    def __init__(self):
        self.client = MongoClient()

    def make_order(self, user_id, items):
        orders = self.client.db_exam_orders.orders

        for item in items:
            pprint(item.__dict__)

        for item in items:
            order = {
                "InvoiceNo" : item,
                "ProductNo" :"",
                "Quantity" :"",
                "InvoiceDate" :"",
                "Name" : "",
                "Description" :"",
                "UnitPrice" : "",
                "CustomerID": user_id,
            }

            orders.insert_one(order)







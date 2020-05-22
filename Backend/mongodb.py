import string
import random

from pymongo import MongoClient
from pprint import pprint
from datetime import datetime


class MongoDB:
    def __init__(self):
        self.client = MongoClient()

    def make_order(self, user_id, items):
        try:
            orders = self.client.db_exam_orders.orders
            invoice_number = u''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            invoice_date = datetime.now().strftime("%Y-%m-%d")

            order = dict()
            order["CustomerID"] = user_id
            order["InvoiceNo"] = invoice_number
            order["InvoiceDate"] = invoice_date
            order["items"] = items
            return orders.insert_one(order).inserted_id
        except:
            raise print("Something went wrong when making order on MongoDB")

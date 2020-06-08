import string
from datetime import datetime
import random


def build_order(products, user_id):
    invoice_number = u''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    invoice_date = datetime.now()
    order = dict()
    order["CustomerID"] = user_id
    order["InvoiceNo"] = invoice_number
    order["InvoiceDate"] = invoice_date
    order["Products"] = products
    return order

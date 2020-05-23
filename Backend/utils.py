import string
from datetime import datetime
import random


def build_order(items, user_id):
    invoice_number = u''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    invoice_date = datetime.now().strftime("%Y-%m-%d")
    order = dict()
    order["CustomerID"] = user_id
    order["InvoiceNo"] = invoice_number
    order["InvoiceDate"] = invoice_date
    order["items"] = items
    return order

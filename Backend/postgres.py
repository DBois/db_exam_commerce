import psycopg2
import gorilla


class Postgres:
    def __init__(self):
        # Define our connection string
        conn_string = f"host='localhost' dbname='db_exam_logistics' user='postgres' password='{gorilla.POSTGRES_PASSWORD}'"

        # print the connection string we will use to connect
        # print("Connecting to database\n	->%s" % conn_string)

        # get a connection, if a connect cannot be made an exception will be raised here
        self.conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        self.cursor = self.conn.cursor()
        print("Connected!\n")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def fetch_shopping_cart_items(self, shopping_cart):
        product_numbers = ""
        items = []

        if(len(shopping_cart) == 0):
            raise ValueError("No items in shopping cart")
        for product_number in list(shopping_cart.keys()):
            product_numbers += f"\'{product_number}\',"


        print("test"+ product_numbers)

        self.cursor.execute(f"SELECT * FROM item WHERE product_number in ({product_numbers[:-1]});")
        fetched_items = self.cursor.fetchall()

        for fetched_item in fetched_items:
            item = {
                "ProductNo": fetched_item[0],
                "Name": fetched_item[1],
                "Description": fetched_item[2],
                "UnitPrice": fetched_item[3],
                "Quantity": shopping_cart[fetched_item[0]]
            }
            items.append(item)

        self.conn.commit()
        return items

    def prepare_update_item_qty(self, order):
        query_str = "BEGIN; "
        from pprint import pprint
        for item in order.get('items'):
            pprint(item)
            query_str += f"UPDATE department_item SET qty = (qty - {item['ProductNo']}) " \
                         f"WHERE item_fk =\'{item['ProductNo']}\' AND department_fk = (SELECT id FROM department LIMIT 1); "

        query_str += f"PREPARE TRANSACTION \'{order.get('InvoiceNo')}\';"
        print(order.get('InvoiceNo'))
        self.cursor.execute(query_str)
        return order.get('InvoiceNo')

    def commit_prepared_transaction(self, transaction_id):
        query_str = f"COMMIT PREPARED '{transaction_id}';"
        self.cursor.execute(query_str)

    def rollback_prepared_transaction(self, transaction_id):
        query_str = f"ROLLBACK PREPARED '{transaction_id}';"
        self.cursor.execute(query_str)


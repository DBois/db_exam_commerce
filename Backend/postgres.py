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

    def fetch_shopping_cart_items(self, shopping_cart):
        product_numbers = tuple(shopping_cart)
        items = []

        self.cursor.execute(f"SELECT * FROM item WHERE product_number in {product_numbers};")
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
        self.cursor.close()
        self.conn.close()
        return items

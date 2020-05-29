import psycopg2
import gorilla


class Postgres:
    def __init__(self):
        # Define our connection string
        conn_string = f"host='localhost' dbname='db_exam_logistics' user='admin_user' password='admin'"

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

    def fetch_shopping_cart_products(self, shopping_cart):
        product_numbers = ""
        products = []

        if len(shopping_cart) == 0:
            raise ValueError("No products in shopping cart")
        for product_number in list(shopping_cart.keys()):
            product_numbers += f"\'{product_number}\',"

        self.cursor.execute(f"SELECT * FROM product WHERE product_number in ({product_numbers[:-1]});")
        fetched_products = self.cursor.fetchall()

        for fetched_product in fetched_products:
            product = {
                "ProductNo": fetched_product[0],
                "Name": fetched_product[1],
                "Description": fetched_product[2],
                "UnitPrice": fetched_product[3],
                "Quantity": shopping_cart[fetched_product[0]]
            }
            products.append(product)

        self.conn.commit()
        return products

    def prepare_update_product_qty(self, order):
        query_str = "BEGIN; "
        for product in order.get('products'):
            query_str += f"UPDATE department_product SET qty = (qty - {product['ProductNo']}) " \
                         f"WHERE product_fk =\'{product['ProductNo']}\' AND department_fk = (SELECT id FROM department LIMIT 1); "

        invoice_no = order.get('InvoiceNo')
        query_str += f"PREPARE TRANSACTION \'{invoice_no}\';"
        self.cursor.execute(query_str)
        return invoice_no

    def commit_prepared_transaction(self, transaction_id):
        query_str = f"COMMIT PREPARED '{transaction_id}';"
        for notice in self.conn.notices:
            if(notice.startswith('NOTICE:')):
                print(notice)

        self.cursor.execute(query_str)

    def rollback_prepared_transaction(self, transaction_id):
        query_str = f"ROLLBACK PREPARED '{transaction_id}';"
        self.cursor.execute(query_str)

import psycopg2
import gorilla

class Postgres:
    def __init__(self):
        # Define our connection string
        conn_string = f"host='localhost' dbname='db_exam_logistics' user='postgres' password='{gorilla.password}'"

        # print the connection string we will use to connect
        #print("Connecting to database\n	->%s" % conn_string)

        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        self.cursor = conn.cursor()
        print("Connected!\n")

    def get_shopping_cart_info(self, user_id, shopping_cart):
        

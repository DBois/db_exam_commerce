from neo4j import GraphDatabase
from settings import NEO4J_URI, NEO4J_USER


class Neo4jDAO:
    def __init__(self):
        # driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
        self._driver = GraphDatabase.driver(NEO4J_URI, auth=("admin_user", "dbois"), max_connection_lifetime=3600)

    def close(self):
        self._driver.close()

    def execute_create_order(self, order):
        with self._driver.session() as session:
            session.read_transaction(create_order, order)

    def execute_create_product(self, product):
        with self._driver.session() as session:
            session.read_transaction(create_product, product)

    def execute_get_related_products(self, product_no):
        related_products = []
        with self._driver.session() as session:
            for product in session.read_transaction(get_related_products, product_no):
                related_products.append(product[0]) # product[0] is product, product[1] is count

        return related_products



def create_order(tx, order):
    query_str_create_order = f"CREATE (a:Order {{ InvoiceNo: '{order.get('InvoiceNo')}'}})"
    query_str_match = "MATCH (a:Order)"
    query_str_where = f"WHERE a.InvoiceNo = '{order.get('InvoiceNo')}'"
    query_str_create = ""
    for i, product in enumerate(order.get('Products')):
        var = chr(ord('b') + i)
        query_str_match += f" ,({var}:Product)"
        query_str_where += f" AND {var}.ProductNo = '{product.get('ProductNo')}'"
        query_str_create += f"CREATE (a)-[:contains]->({var}) "

    query_str = f"{query_str_match} {query_str_where} {query_str_create}"

    # Print query strings
    print("Neo4j create order string: ")
    print(query_str_create_order)
    print("Neo4j create relations string")
    print(query_str)

    # Execute queries
    tx.run(query_str_create_order)
    tx.run(query_str)


def create_product(tx, product):
    query_str = f"CREATE (a:Products {{ Name: '{product.get('Name')}', ProductNo: '{product.get('ProductNo')}'}}) "
    tx.run(query_str)


def get_related_products(tx, product_no):
    query_str = f"MATCH (i:Product)<--(:Order)-->(ii:Product) WHERE i.ProductNo = '{product_no}' " \
                f"MATCH (ii)<-[r:contains]-(:Order) " \
                f"return properties(ii), COUNT(distinct r) AS count ORDER BY count DESC LIMIT 10"
    return tx.run(query_str)
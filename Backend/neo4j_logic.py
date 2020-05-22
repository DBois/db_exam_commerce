from neo4j import GraphDatabase
from settings import NEO4J_URI, NEO4J_USER
from gorilla import NEO4J_PASSWORD


class Neo4j:
    def __init__(self):
        # driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
        self._driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self._driver.close()

    def execute_transaction(self):
        with self._driver.session() as session:
            session.read_transaction(create_order, "Alice")


def create_order(tx, order):
    query_str_create_order = ""
    query_str_match = "MATCH (a:Order)"
    query_str_where = f"WHERE a.invoicenum = {order.invoicenum}"
    query_str_create = ""
    for i, item in enumerate(order.lineitems):
        var = chr(bytes('b', 'utf-8') + i)
        query_str_match += f" ,({var}:Item)"
        query_str_where += f" AND {var}.productnum = {item.productnum}"
        query_str_create += f"CREATE (a)-[:contains]->({var}) "

    tx.run("CREATE (a:Order { invoicenum: '1234'})")


def create_item(tx, item):
    tx.run("CREATE (a:Item { name: 'toiletpapir', productnum: '1234'}) "
            "RETURN a.name", name=item)
    print()


def random_stuff(tx, name):
    for record in tx.run("MATCH (a:Person)-[:KNOWS]->(f) "
                         "WHERE a.name = {name} "
                         "RETURN f.name", name=name):
        print(record["f.name"])

from pprint import pprint

from neo4j import GraphDatabase
from settings import NEO4J_URI, NEO4J_USER
from gorilla import NEO4J_PASSWORD


class Neo4jDAO:
    def __init__(self):
        # driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))
        self._driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD), max_connection_lifetime=3600)

    def close(self):
        self._driver.close()

    def execute_create_order(self, order):
        with self._driver.session() as session:
            session.read_transaction(create_order, order)

    def execute_create_item(self, item):
        with self._driver.session() as session:
            session.read_transaction(create_item, item)


def create_order(tx, order):
    query_str_create_order = f"CREATE (a:Order {{ InvoiceNo: '{order.get('InvoiceNo')}'}})"
    query_str_match = "MATCH (a:Order)"
    query_str_where = f"WHERE a.InvoiceNo = '{order.get('InvoiceNo')}'"
    query_str_create = ""
    for i, item in enumerate(order.get('items')):
        var = chr(ord('b') + i)
        query_str_match += f" ,({var}:Item)"
        query_str_where += f" AND {var}.ProductNo = '{item.get('ProductNo')}'"
        query_str_create += f"CREATE (a)-[:contains]->({var}) "

    query_str = f"{query_str_match} {query_str_where} {query_str_create}"
    tx.run(query_str_create_order)
    tx.run(query_str)


def create_item(tx, item):
    query_str = f"CREATE (a:Item {{ Name: '{item.get('Name')}', ProductNo: '{item.get('ProductNo')}'}}) "
    print(query_str)
    tx.run(query_str)

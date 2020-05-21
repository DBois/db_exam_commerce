from redis import Redis
from settings import *


class Redis:
    # def __init__(self):
    conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

    def update_shopping_cart(self, user_id, product_no, qty):
        shopping_cart = {product_no: qty}
        self.conn.hmset(f"{user_id}_cart", shopping_cart)

        return self.conn.hgetall(f"{user_id}_cart")

    def get_shopping_cart(self, user_id):
        return self.conn.hgetall(f"{user_id}_cart")

    def delete_shopping_cart(self, user_id):
        self.conn.delete(f"{user_id}_cart")
import redis
from settings import *

class Redis:
    def __init__(self):
        self.conn = redis.Redis(REDIS_CONNECTION)

    def update_shopping_cart(self, user_id, product_no, qty):
        shopping_cart = {product_no:qty}
        self.conn.hmset(f"{user_id}_cart", shopping_cart)

        return self.conn.hgetall(user_id)


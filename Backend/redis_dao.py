from datetime import datetime, timedelta

from redis import Redis
from rediscluster import RedisCluster
from settings import *


class RedisDAO:
    # def __init__(self):

    # conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True, password=REDIS_PASSWORD)
    startup_nodes = [{"host": "127.0.0.1", "port": "7000"},{"host": "127.0.0.1", "port": "7001"},{"host": "127.0.0.1", "port": "7002"},{"host": "127.0.0.1", "port": "7003"},{"host": "127.0.0.1", "port": "7004"},{"host": "127.0.0.1", "port": "7005"},]
    conn = RedisCluster(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, startup_nodes=startup_nodes, decode_responses=True)
    
    def update_shopping_cart(self, user_id, product_no, qty):

        # Update shoppingcart with new product and qty
        shopping_cart = {product_no: qty}
        self.conn.hmset(f"{user_id}_cart", shopping_cart)

        # Set shoppingcart to expire in 60 days
        ttl = timedelta(days=60)
        self.conn.expire(f"{user_id}_cart", ttl)

        return self.conn.hgetall(f"{user_id}_cart")

    def get_shopping_cart(self, user_id):
        # Set shoppingcart to expire in 60 days
        ttl = timedelta(days=60)
        self.conn.expire(f"{user_id}_cart", ttl)

        # Return shopping_cart
        return self.conn.hgetall(f"{user_id}_cart")

    def delete_shopping_cart(self, user_id):
        self.conn.delete(f"{user_id}_cart")

    def delete_product(self, user_id, product_id):
        deleted_product = self.conn.hdel(f"{user_id}_cart", product_id)

        # Set shoppingcart to expire in 60 days
        ttl = timedelta(days=60)
        self.conn.expire(f"{user_id}_cart", ttl)

        return deleted_product

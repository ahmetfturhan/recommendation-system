import redis
from redis_namespace import StrictRedis

# try:
#     r = redis.Redis(host='localhost', port=6379, db=0)
#     r.ping()
#     print("Redis server is running")
# except redis.ConnectionError:
#     print("Redis server is not running")

redis_connection = redis.StrictRedis()
namespaced_redis = StrictRedis(namespace='Trendyol:')
namespaced_redis.set('foo', 'bar')  # redis_connection.set('ns:foo', 'bar')

print("namescpaced get foo", namespaced_redis.get('foo').decode('utf-8'))
print("connection get trendyol foo", redis_connection.get('Trendyol:foo').decode('utf-8'))

namespaced_redis.delete('foo')
print("after deleteion namescpaced get foo", namespaced_redis.get('foo'))
print("connection get trendyol foo", redis_connection.get('Trendyol:foo'))
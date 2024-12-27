from redis import Redis
from pywebio.input import input
from pywebio.output import put_text, put_markdown

redis_client = Redis(
    host="localhost", port=6379, db=0, password=None, decode_responses=True
)

put_markdown("### Redis Usage")

put_text("We will use the Redis client to store and retrieve data.")

while True:
    key = input("Enter the key to store data: ")
    if key.lower() == "stop" or key.lower() == "":
        put_text("Bye..")
        break
    value = input("Enter the value to store: ")
    put_text(f"Using redis_client.set({key}, {value})")
    redis_client.set(key, value)
    put_text("Data stored successfully!")

    get_key = input("Enter the key to retrieve data: ")

    put_text("Using redis_client.get(key)")
    data = redis_client.get(get_key)

    put_text(f"Data retrieved is: {data}")

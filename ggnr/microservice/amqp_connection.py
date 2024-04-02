import time
import pika
from os import environ

hostname = environ.get("rabbit_host") or "localhost"
port = environ.get("rabbit_port") or 5672


# function to create a connection to the broker
def create_connection(max_retries=12, retry_interval=5):
    print("amqp_connection: Create_connection")

    retries = 0
    connection = None

    # loop to retry connection upto 12 times with a retry interval of 5 seconds
    while retries < max_retries:
        try:
            print("amqp_connection: Trying connection")
            # connect to the broker
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=hostname,
                    port=port,
                    heartbeat=3600,
                    blocked_connection_timeout=3600,
                )
            )
            print("amqp_connection: Connection established successfully")
            break  # Connection successful, exit the loop
        except pika.exceptions.AMQPConnectionError as e:
            print(f"amqp_connection: Failed to connect: {e}")
            retries += 1
            print(f"amqp_connection: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
            # Retry the connection

    if connection is None:
        raise Exception(
            "Unable to establish a connection to RabbitMQ after multiple attempts"
        )

    return connection


# function to check if the exchange exists
def check_exchange(channel, exchangename, exchangetype):
    try:
        # check if the exchange exists
        channel.exchange_declare(exchangename, exchangetype, durable=True, passive=True)
    except Exception as e:
        print("Exception:", e)
        return False
    return True


if __name__ == "__main__":
    create_connection()

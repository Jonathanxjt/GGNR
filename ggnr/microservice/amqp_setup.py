import time
import pika
from os import environ

# non-hardcoding the values
hostname = environ.get("hostname")
port = environ.get("port")
exchangename = environ.get("exchangename")
exchangetype = environ.get("exchangetype")
notif_queue_name = environ.get("notif_queue_name") #Notification_Log

# default (hardcoded)
# hostname = "localhost"
# port = 5672
# exchangename = "order_topic"
# exchangetype = "topic"


def create_connection(max_retries=12, retry_interval=5):
    print("amqp_setup:create_conncetion")

    retries = 0
    connection = None

    # loop to retry connection up to 12 times with a retry interval of 5 seconds
    # can change the retry_interval
    while retries < max_retries:
        try:
            print("amqp_setup: Trying connection")
            # connect to the broker and set up a communication channel in the connection
            connection = pika.BlockingConnection(pika.ConnectionParameters
                                (host=hostname, port=port,
                                 heartbeat=3600, blocked_connection_timeout=3600)) # these parameters to prolong the expiration time (in seconds) of the connection
                # Note about AMQP connection: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
                # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls.
                # If see: Stream connection lost: ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None)
                # - Try: simply re-run the program or refresh the page.
                # For rare cases, it's incompatibility between RabbitMQ and the machine running it,
                # - Use the Docker version of RabbitMQ instead: https://www.rabbitmq.com/download.html
            print("amqp_setup: Connection established successfully")
            break  # Connection successful, exit the loop
        except pika.exceptions.AMQPConnectionError as e:
            print(f"amqp_setup: Failed to connect: {e}")
            retries += 1
            print(f"amqp_setup: Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)

    if connection is None:
        raise Exception("amqp_setup: Unable to establish a connection to RabbitMQ after multiple attempts.")

    return connection

def create_channel(connection):
    print('amqp_setup:create_channel')
    channel = connection.channel()
    # Set up the exchange if the exchange doesn't exist
    print('amqp_setup:create exchange')
    channel.exchange_declare(exchange=exchangename, exchange_type=exchangetype, durable=True) # 'durable' makes the exchange survive broker restarts
    return channel 

def create_queues(channel):
    print("amqp_setup:create queues")
    # create_error_queue(channel)
    create_notif_log_queue(channel)

def create_notif_log_queue(channel):
    print("amqp_setup:create_notif_log_queue")
    a_queue_name = "Notification_Log"
    channel.queue_declare(queue=a_queue_name, durable=True)
    channel.queue_bind(exchange=exchangename, queue=a_queue_name, routing_key="#")
    # routing_key = "#"

if __name__ == "__main__":
    connection = create_connection()
    channel = create_channel(connection)
    create_queues(channel)
#!/usr/bin/env python3
import amqp_connection
import json
import pika
#from os import environ


a_queue_name = 'Notification_Log' # queue to be subscribed by Notification_Log microservice

# Instead of hardcoding the values, we can also get them from the environ as shown below
# a_queue_name = environ.get('Notification_Log') #Notification_Log

def receiveOrderLog(channel):
    try:
        # set up a consumer and start to wait for coming messages
        channel.basic_consume(queue=a_queue_name, on_message_callback=callback, auto_ack=True)
        print('Notification_Log: Consuming from queue:', a_queue_name)
        channel.start_consuming()  # an implicit loop waiting to receive messages;
             #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.
    
    except pika.exceptions.AMQPError as e:
        print(f"Notification_Log: Failed to connect: {e}") # might encounter error if the exchange or the queue is not created

    except KeyboardInterrupt:
        print("Notification_Log: Program interrupted by user.") 


def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nNotification_Log: Received an order log by " + __file__)
    processOrderLog(json.loads(body))
    print()

def processOrderLog(order):
    print("Notification_Log: Recording an order log:")
    print(order)

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("Notification_Log: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("Notification_Log: Connection established successfully")
    channel = connection.channel()
    receiveOrderLog(channel)
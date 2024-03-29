#!/usr/bin/env python3
import amqp_connection
import json
import pika
#from os import environ


a_queue_name = 'Notification_Log' # queue to be subscribed by Notification_Log microservice

# Instead of hardcoding the values, we can also get them from the environ as shown below
# a_queue_name = environ.get('Notification_Log') #Notification_Log

# import twilio client
import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)
# end of twilio setup

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

    print("Starting to process order log...")
    print(order)
    
    if 'users' in order:
        print("Extracted Contact Information:")
        for user in order['users']:
            contact = user['contact']
            print(f"User ID: {user['UID']}, Contact: {user['contact']}, Email: {user['email']}, Username: {user['username']}")
            message_body = order['notification']
            send_sms(contact, message_body)
    else:
        print("No users found in the order.")

def send_sms(contact, message_body):
    try:
        message = client.messages.create(
            body=message_body,
            from_='+19287560401',  
            to=contact
        )
        print(f"Message sent to {contact}, SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send message to {contact}: {e}")  


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("Notification_Log: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("Notification_Log: Connection established successfully")
    channel = connection.channel()
    receiveOrderLog(channel)
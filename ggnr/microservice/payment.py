#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

import stripe
#load environment variables
load_dotenv()

# importing api key
stripe.api_key = os.getenv('STRIPE_API_KEY')

app = Flask(__name__)
CORS(app)

YOUR_DOMAIN = 'http://localhost:3000'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # Retrieve priceId from the request body
        price_id = request.json['priceId']
        print(price_id)
        # Create new Checkout Session for the order
        session = stripe.checkout.Session.create(
            ui_mode='embedded',
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            return_url = f"{YOUR_DOMAIN}/return?session_id={{CHECKOUT_SESSION_ID}}"
        )
    except Exception as e:
        return jsonify(error=str(e)), 400

    return jsonify(clientSecret=session.client_secret)

@app.route('/session-status', methods=['GET'])
def session_status():
    session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    return jsonify(status=session.payment_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011, debug=True)

#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, jsonify, redirect, request
from flask_cors import CORS

import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51OuvQH2LfOffQtXeCwFG6wFjZAbQC5PVeBjQiVRx0QabJ7Y9cZM46fgBBVmBAKN1xdVt9oVRmMjouRHjSUVrvQzn00HHTHM3Q7'

app = Flask(__name__)
CORS(app)

YOUR_DOMAIN = 'http://127.0.0.1:5011'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            ui_mode = 'embedded',
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1OvbmM2LfOffQtXeTeo65xEs',
                    'quantity': 1,
                },
            ],
            mode='payment',
            return_url=YOUR_DOMAIN + '/return?session_id={CHECKOUT_SESSION_ID}',
        )
    except Exception as e:
        return str(e)

    return jsonify(clientSecret=session.client_secret)

@app.route('/session-status', methods=['GET'])
def session_status():
  session = stripe.checkout.Session.retrieve(request.args.get('session_id'))

  return jsonify(status=session.status, customer_email=session.customer_details.email)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011, debug=True)

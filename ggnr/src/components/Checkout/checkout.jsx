import React, { useState, useEffect } from "react";
import { loadStripe } from '@stripe/stripe-js';
import { EmbeddedCheckoutProvider, EmbeddedCheckout } from '@stripe/react-stripe-js';
import { useLocation } from "react-router-dom";

const stripePromise = loadStripe("pk_test_51OuvQH2LfOffQtXergftoxL0CtUh2brY7a5jhtBucRIN250k0Q1OLDKyEk142rUfEbwU4SE4kR8qq6duHXH8hrJD00Qkj6ZBfD");

const CheckoutForm = () => {
  const location = useLocation();
  const priceId = new URLSearchParams(location.search).get('priceId');
  const [clientSecret, setClientSecret] = useState('');

  useEffect(() => {
    if (priceId) {
      fetch("http://localhost:5011/create-checkout-session", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ priceId: priceId }), // Pass priceId to backend
      })
      .then((res) => res.json())
      .then((data) => setClientSecret(data.clientSecret))
      .catch((error) => console.error('Error fetching client secret:', error));
    }
  }, [priceId]);

  return (
    <div id="checkout">
      {clientSecret && (
        <EmbeddedCheckoutProvider
          stripe={stripePromise}
          options={{clientSecret}}
        >
          <EmbeddedCheckout />
        </EmbeddedCheckoutProvider>
      )}
    </div>
  )
}

export default CheckoutForm;

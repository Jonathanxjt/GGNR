import React, { useState, useEffect } from "react";
import { loadStripe } from '@stripe/stripe-js';
import { EmbeddedCheckoutProvider, EmbeddedCheckout } from '@stripe/react-stripe-js';
import { useLocation } from "react-router-dom";

const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLIC_KEY);

const CheckoutForm = () => {
  const location = useLocation();
  const priceId = new URLSearchParams(location.search).get('priceId');
  const [clientSecret, setClientSecret] = useState('');

  useEffect(() => {
    if (priceId) {
      // Fetch the client secret from the backend
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

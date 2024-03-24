import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import "./Return.css";

const Return = () => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const sessionId = searchParams.get("session_id");

  const [status, setStatus] = useState(null);
  const [customerEmail, setCustomerEmail] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!sessionId) return;

    fetch(`/session-status?session_id=${sessionId}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error('Failed to fetch session status');
        }
        return res.json();
      })
      .then((data) => {
        setStatus(data.status);
        setCustomerEmail(data.customer_email);
      })
      .catch((error) => {
        setError(error.message);
      });
  }, [sessionId]);

  if (sessionId) {
    // Render the success div if sessionId exists in the URL
    return (
      <div id="success">
        <p>
          We appreciate your business! A confirmation email will be sent to your email.
          If you have any questions, please contact an admin. 
        </p>
      </div>
    );
  }

  return null; // Render nothing if sessionId doesn't exist
}

export default Return;

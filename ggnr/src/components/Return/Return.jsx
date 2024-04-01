import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Return.css";
import axios from 'axios';

const Return = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const sessionId = searchParams.get("session_id");

  const [status, setStatus] = useState(null);
  const [customerEmail, setCustomerEmail] = useState('');
  const [error, setError] = useState(null);
  const [countdown, setCountdown] = useState(10); // Initial countdown time in seconds
  const [isStatusChecked, setIsStatusChecked] = useState(false); // State to indicate if the status check is completed

  useEffect(() => {
    const fetchSessionStatus = async () => {
      if (!sessionId) return;

      try {
        const response = await axios.get(`http://localhost:5011/session-status?session_id=${sessionId}`);
        console.log(response.data);
        setStatus(response.data.status);
        console.log("Payment status:", response.data.status); // Print the status
        setIsStatusChecked(true); // Set status check to completed
      } catch (error) {
        console.error("Error fetching session status:", error);
        setError(error.message);
      }
    };

    fetchSessionStatus();
  }, [sessionId]);

  useEffect(() => {
    if (isStatusChecked) {
      // Start countdown timer only if the status check is completed
      const countdownInterval = setInterval(() => {
        setCountdown((prevCountdown) => prevCountdown - 1);
      }, 1000);

      // Redirect to homepage after countdown reaches 0
      if (countdown === 0) {
        navigate('/');
      }

      // Clear interval on component unmount
      return () => clearInterval(countdownInterval);
    }
  }, [isStatusChecked, countdown, navigate]);

  return (
    <div id="return">
      {status === "paid" ? (
        <div id="success">
          <p>
            Payment was successful! A confirmation email will be sent to you.
            If you have any questions, please contact support.
          </p>
          <p>Redirecting in {countdown} seconds...</p>
        </div>
      ) : (
        <div id="error">
          <p>Payment failed or was canceled. Please try again.</p>
          <p>Redirecting in {countdown} seconds...</p>
        </div>
      )}
    </div>
  );
};


export default Return;

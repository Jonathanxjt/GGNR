import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { toast, ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./Return.css";
import axios from "axios";

const Return = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const sessionId = searchParams.get("session_id");

  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);
  const [paymentintent, setPaymentIntent] = useState(null);
  const [countdown, setCountdown] = useState(10); // Initial countdown time in seconds
  const [isStatusChecked, setIsStatusChecked] = useState(false); // State to indicate if the status check is completed
  const [soldOut, setSoldOut] = useState(false);
  const storedRegistrationData = JSON.parse(
    sessionStorage.getItem("registrationData")
  );

  useEffect(() => {
    const fetchSessionStatus = async () => {
      if (!sessionId) return;

      try {
        const response = await axios.get(
          `http://localhost:5011/session-status?session_id=${sessionId}`
        );
        console.log("response data:", response.data);
        setStatus(response.data.status);
        setPaymentIntent(response.data.payment_intent);
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
      (async () => {
        try {
          await axios.post(
            "http://localhost:5006/register",
            storedRegistrationData
          );
          // Registration successful, proceed with your logic
          localStorage.setItem(
            "toastMessage",
            "Ticket is issued to your account!"
          );
        } catch (error) {
          // Registration failed, attempt to refund
          try {
            setSoldOut(true);
            await refundPayment(paymentintent);
            // Refund successful, handle accordingly
            toast.error("Tickets SOLD OUT 😭!", {
              position: "top-center",
              autoClose: 10000,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: true,
              draggable: true,
              progress: undefined,
              theme: "dark",
              transition: Flip,
            });
            toast.info("Your payment has been refunded!", {
              position: "top-center",
              autoClose: 10000,
              hideProgressBar: false,
              closeOnClick: true,
              pauseOnHover: true,
              draggable: true,
              progress: undefined,
              theme: "dark",
              transition: Flip,
            });
            // Start countdown timer only after refund is successful
            const countdownInterval = setInterval(() => {
              setCountdown((prevCountdown) => prevCountdown - 1);
            }, 1500);

            // Redirect to homepage after countdown reaches 0
            if (countdown === 0) {
              navigate("/events");
            }

            // Clear interval on component unmount
            return () => clearInterval(countdownInterval);
          } catch (refundError) {
            // Handle refund error
          }
        }
      })();
    }
  }, [
    isStatusChecked,
    storedRegistrationData,
    paymentintent,
    countdown,
    navigate,
  ]);

  // Function to refund a payment upo ticket sold out scenario.
  const refundPayment = async (paymentIntentId) => {
    try {
      const response = await axios.post("http://localhost:5011/refund", {
        paymentIntentId: paymentIntentId,
      });
      console.log("Refund successful:", response.data);
      return response.data;
    } catch (error) {
      console.error(
        "Refund error:",
        error.response ? error.response.data : error.message
      );
      throw error;
    }
  };

  return (
    <div id="return">
      {soldOut ? (
        <div id="sold-out">
          <div class="return_custom-loader"></div>
          <p>Tickets are sold out. Redirecting you to the events page.</p>
          <p>Redirecting in {countdown} seconds...</p>
        </div>
      ) : status === "paid" ? (
        <div id="success">
          <div class="return_custom-loader"></div>
          <p>
            Payment was successful! Please check your profile for your ticket.
            If you have any questions, please contact support.
          </p>
          <p>Redirecting in {countdown} seconds...</p>
        </div>
      ) : (
        <div id="error">
          <div class="return_custom-loader"></div>
          <p>Payment failed or was canceled. Please try again.</p>
          <p>Redirecting in {countdown} seconds...</p>
        </div>
      )}
    </div>
  );
};

export default Return;

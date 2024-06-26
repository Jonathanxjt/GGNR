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
	const [countdown, setCountdown] = useState(10); 
	const [isStatusChecked, setIsStatusChecked] = useState(false); 
	const [soldOut, setSoldOut] = useState(false);
	const [isRegistrationAttempted, setRegistrationAttempted] = useState(false);
	const storedRegistrationData = JSON.parse(
		sessionStorage.getItem("registrationData")
	);

	useEffect(() => {
		const fetchSessionStatus = async () => {
			if (!sessionId) return;

			try {
				const response = await axios.get(
					`http://localhost:8000/api/v1/session-status?session_id=${sessionId}`
				);
				setStatus(response.data.status);
				setPaymentIntent(response.data.payment_intent);
				setIsStatusChecked(true); // Set status check to completed
			} catch (error) {
				console.error("Error fetching session status:", error);
				setError(error.message);
			}
		};

		fetchSessionStatus();
	}, [sessionId]);

	useEffect(() => {
		if (isStatusChecked && !isRegistrationAttempted) {
			(async () => {
				setRegistrationAttempted(true); // Set to true to prevent multiple attempts
				try {
					await axios.post(
						"http://localhost:8000/api/v1/register",
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
							autoClose: 5000,
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
							autoClose: 5000,
							hideProgressBar: false,
							closeOnClick: true,
							pauseOnHover: true,
							draggable: true,
							progress: undefined,
							theme: "dark",
							transition: Flip,
						});
					} catch (refundError) {
						// Handle refund error
					}
				}
			})();
		}
	}, [isStatusChecked, storedRegistrationData, paymentintent, navigate]);

	useEffect(() => {
		// Start countdown timer only if the status check is completed
		let countdownInterval;
		if (isStatusChecked) {
			countdownInterval = setInterval(() => {
				setCountdown((prevCountdown) => prevCountdown - 1);
			}, 1000);
		}

		// Redirect to homepage after countdown reaches 0
		if (countdown === 0) {
			window.location.href = "/events";
		}

		// Clear interval on component amount or when isStatusChecked changes
		return () => clearInterval(countdownInterval);
	}, [countdown, isStatusChecked, navigate]);

	// Function to refund a payment for ticket sold out scenario.
	const refundPayment = async (paymentIntentId) => {
		try {
			const response = await axios.post("http://localhost:8000/api/v1/refund", {
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

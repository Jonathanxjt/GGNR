import React from "react";
import { Navbar, Nav, Form } from "react-bootstrap";
import { BsPerson } from "react-icons/bs";
import { LuLogOut } from "react-icons/lu";
import { LuLogIn } from "react-icons/lu";

import "./MyNavbar.css";

export const MyNavbar = () => {
	const profileIconStyle = {
		fontSize: "20px", // Adjust size as needed
		color: "#FFFFFF", // Adjust color as needed
		marginLeft: "5px", // Adjust spacing as needed
		cursor: "pointer",
	};

	// Check if user is logged in
	const isLoggedIn = sessionStorage.getItem("user");

	// Function to handle logout
	const handleLogout = () => {
		sessionStorage.clear(); // Clear all sessionStorage
		localStorage.setItem("toastMessage", "Logged out successfully!");
		window.location.href = "/"; // Redirect to home page
	};

	return (
		<Navbar
			variant="dark"
			expand="lg"
			className="px-4 sticky-top custom-navbar"
		>
			<Navbar.Brand href="/">GGNR.</Navbar.Brand>
			<Navbar.Toggle aria-controls="basic-navbar-nav" />
			<Navbar.Collapse id="basic-navbar-nav">
				<Nav className="mx-auto">
					<Nav.Link href="/">Home</Nav.Link>
					<Nav.Link href="/events">Events</Nav.Link>
				</Nav>
				{!isLoggedIn && (
					<Form inline>
						<Nav.Link href="/login" style={profileIconStyle}>
							<LuLogIn /> Login
						</Nav.Link>
					</Form>
				)}
				{isLoggedIn && (
					<>
						<Nav.Link href="/profile" style={profileIconStyle}>
							<BsPerson /> Profile
						</Nav.Link>
						<Nav.Link onClick={handleLogout} style={profileIconStyle}>
							<LuLogOut />
						</Nav.Link>
					</>
				)}
			</Navbar.Collapse>
		</Navbar>
	);
};

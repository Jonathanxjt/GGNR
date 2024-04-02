import React from "react";
import "./CreateEventButton.css"; // Import the CSS file

// CircleButton component
const CircleButton = ({ url }) => {
	const redirectToURL = () => {
		// Redirect to the specified URL
		window.location.href = url; // Alternatively, you can use history.push(url) if using React Router
	};

	return (
		<div className="circleButton" onClick={redirectToURL}>
			{/* Plus symbol inside the circle */}
			<span className="circleButtonContent">&#43;</span>
		</div>
	);
};

export default CircleButton;

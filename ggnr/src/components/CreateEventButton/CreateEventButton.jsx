import React from 'react';
// import { useHistory } from 'react-router-dom'; // If using React Router for navigation
import './CreateEventButton.css'; // Import the CSS file

// CircleButton component
const CircleButton = ({ url }) => {
//   const history = useHistory();

  const redirectToURL = () => {
    // Redirect to the specified URL
    window.location.href = url; // Alternatively, you can use history.push(url) if using React Router
  };

  return (
    <div className="circleButton" onClick={redirectToURL}>
      {/* Plus symbol inside the circle */}
      <span className="circleButtonContent">+</span>
    </div>
  );
};

export default CircleButton
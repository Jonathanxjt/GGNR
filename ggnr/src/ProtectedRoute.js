import React from "react";
import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children }) => {
    const checkLoginAndRole = () => {
      const user = JSON.parse(sessionStorage.getItem("user"));
      console.log("Parsed user object:", user); // Output the parsed user object
  
      if (!user || user.organiser === false) {
        console.log("User is not logged in or not an organiser");
        return false;
      }
      console.log("User is logged in and is an organiser");
      return true;
    };

    const isLoggedInAndOrganiser = checkLoginAndRole();
    localStorage.setItem(
      "toastErrorMessage",
      "Login as a valid organiser to create an event!"
    );
    return isLoggedInAndOrganiser ? children : <Navigate to="/login" />;
};

export default ProtectedRoute;

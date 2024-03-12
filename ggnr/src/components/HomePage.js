import React from "react";
import { MyNavbar } from "./MyNavbar/MyNavbar";
import background from "../assets/background.mp4";
import "./Home.css";

const HomePage = () => {
  return (
    <div className="main">
      <MyNavbar />
      <div className="overlay"></div>
      <video src={background} autoPlay loop muted />
      <div className="content">
        <h1>Welcome to Our Website</h1>
        <p>This is the home page. Explore our site to learn more about us.</p>
      </div>
    </div>
  );
};

export default HomePage;

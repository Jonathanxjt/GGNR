import React from "react";
import { MyNavbar } from "./MyNavbar/MyNavbar";
import background from "../assets/background.mp4";
import MyFooter from "./MyFooter/MyFooter";
import "./Home.css";

const HomePage = () => {
  return (
    <div className="main">
      <MyNavbar />
      <div className="overlay"></div>
      <video src={background} autoPlay loop muted />
      <div className="content">
        <h1>Welcome to Our Website</h1>
        <p>Home of gamers</p>
      </div>
      <MyFooter />
    </div>
  );
};

export default HomePage;

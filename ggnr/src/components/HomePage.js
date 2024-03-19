import React from "react";
import { MyNavbar } from "./MyNavbar/MyNavbar";
import background from "../assets/background.mp4";
import MyFooter from "./MyFooter/MyFooter";
import Button from "react-bootstrap/Button";
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
        <Button
          href="/events"
          variant="outline-light"
          style={{ display: "inline-flex", alignItems: "center" }}
        >
          Browse Events{" "}
        </Button>
        
      </div>
      <MyFooter />
    </div>
  );
};

export default HomePage;

import React from "react";
import { MyNavbar } from "./MyNavbar/MyNavbar";
import background from "../assets/background.mp4";
import MyFooter from "./MyFooter/MyFooter";
import Button from "react-bootstrap/Button";
import { useHistory } from "react-router-dom";
import CircleButton from "./CreateEventButton/CreateEventButton";
import "./Home.css";

const HomePage = () => {
  return (
    <div className="main">
      <MyNavbar />
      <div className="overlay"></div>
      <video src={background} autoPlay loop muted />
      <div className="content">
        <h1>Welcome to GGNR</h1>
        <p>Home of Gamers</p>
        <Button
          href="/events"
          variant="outline-light"
          style={{ display: "inline-flex", alignItems: "center" }}
        >
          Browse Events{" "}
        </Button>
        <div>
        <CircleButton url="http://localhost:3000/create_event" />
        </div>
      </div>
      <MyFooter />
    </div>
  );
};

export default HomePage;

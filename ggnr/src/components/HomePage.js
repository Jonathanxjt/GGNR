import React from "react";
import { MyNavbar } from "./MyNavbar/MyNavbar";
import background from "../assets/background.mp4";

import Button from "react-bootstrap/Button";
import { useHistory } from "react-router-dom";
import CircleButton from "./CreateEventButton/CreateEventButton";
import Typewriter from "typewriter-effect";
import "./Home.css";
import MyFooter from "./MyFooter/MyFooter";

const HomePage = () => {
	return (
		<div className="main">
			<MyNavbar />
			<div className="overlay"></div>
			<video src={background} autoPlay loop muted />
			<div className="content">
				<Typewriter
					options={{
						strings: ["Welcome to GGNR"],
						autoStart: true,
						loop: true,
            pausefor: 15,
					}}
				/>
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

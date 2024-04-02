import React, { useState, useEffect } from "react";
import { Row, Col } from "react-bootstrap";
import Carousel from "react-bootstrap/Carousel";
import { FaCalendar } from "react-icons/fa";
import { MyNavbar } from "../MyNavbar/MyNavbar";
import Card from "react-bootstrap/Card";
import placeholder from "../../assets/placeholder.jpg";
import { FaUser } from "react-icons/fa";
import { FaLocationDot } from "react-icons/fa6";
import image1 from "../../assets/image1.png";
import image2 from "../../assets/image2.png";
import image3 from "../../assets/image3.png";
import "./EventPage.css";
import axios from "axios";
import CircleButton from "../CreateEventButton/CreateEventButton";
import "../CreateEventButton/CreateEventButton.css";

function EventPage() {
	const [eventData, setEventData] = useState([]);

	useEffect(() => {
		axios
			.get("http://localhost:8000/event") // Fetch events from the backend
			.then((response) => {
				const formattedEvents = response.data.data.events.map((event) => {
					// Map through the events
					const now = new Date();
					const eventStart = new Date(event.Time);
					const timeDifference = eventStart - now;

					// Make sure to calculate only for future events
					if (timeDifference > 0) {
						// Calculate days, hours, minutes
						let days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
						let hours = Math.floor(
							(timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
						);
						let minutes = Math.floor(
							(timeDifference % (1000 * 60 * 60)) / (1000 * 60)
						);
						// Add StartingIn attribute
						event.StartingIn = `Starting in ${days}D ${hours}H ${minutes}M`;
					} else {
						// For past events or events that have already started
						event.StartingIn = "Event has Ended";
					}

					// Format the date and time here
					const formattedDateTime = new Date(event.Time).toLocaleString(
						"en-SG",
						{
							day: "numeric",
							month: "long",
							year: "numeric",
							hour: "numeric",
							minute: "numeric",
							hour12: true,
						}
					);

					// Initialize capacities
					let audienceCap = 0;
					let vipCap = 0;
					let competitorCap = 0;

					// Calculate the capacity of each category
					event.event_types.forEach((type) => {
						if (type.TierID === 1) {
							audienceCap += type.Capacity;
						} else if (type.TierID === 2) {
							vipCap += type.Capacity;
						} else if (type.TierID === 3) {
							competitorCap += type.Capacity;
						}
					});

					// Add formatted time and capacities to the event object
					return {
						...event,
						FormattedTime: formattedDateTime,
						AudienceCap: audienceCap,
						VIPCap: vipCap,
						CompetitorCap: competitorCap,
					};
				});

				formattedEvents.sort((a, b) => {
					return new Date(a.Time) - new Date(b.Time);
				});

				setEventData(formattedEvents);
				console.log(formattedEvents);
			})
			.catch((error) => {
				console.error("There was an error!", error);
			});
	}, []);
	// Function to create cards for each event
	const createCards = (events) => {
		return events.map((event, index) => (
			<Col key={index} lg={3} md={4} sm={6} xs={12} className="mb-3">
				<Card
					key={index}
					className="card"
					onClick={() => {
						// Store the event data in local storage
						localStorage.setItem("selectedEvent", JSON.stringify(event));
						// Redirect to the registration page
						window.location.href = `/registration?title=${encodeURIComponent(
							event.Title
						)}&eid=${encodeURIComponent(event.EID)}`;
					}}
				>
					<Card.Img
						variant="top"
						src={event.EventLogo}
						onError={(e) => {
							e.target.src = placeholder;
						}} // Set a placeholder image on error
					/>
					<Card.Body>
						<Card.Title>{event.Title}</Card.Title>
						<Card.Text>{event.GameName}</Card.Text>
						<Card.Text className="small-text">
							<p>
								<FaCalendar />
								&nbsp;
								{event.FormattedTime}
							</p>
							<p>
								<FaLocationDot />
								&nbsp;
								{event.Location}
							</p>
							<p>
								<FaUser />
								&nbsp;
								{event.AudienceCap + event.VIPCap + event.CompetitorCap} Tickets
								Left
							</p>
							{/* {event.AudienceCap > 0 && (<p>
                <FaUser />
                &nbsp;
                {event.AudienceCap} Tickets Left
              </p>)}
              {event.VIPCap > 0 && (
                <p>
                  <RiVipFill />
                  &nbsp;
                  {event.VIPCap} VIP Tickets Left
                </p>
              )}

              {event.CompetitorCap > 0 && (
                <p>
                  <IoGameController />
                  &nbsp;
                  {event.CompetitorCap} Competitor Tickets Left
                </p>
              )} */}
						</Card.Text>
					</Card.Body>
					<Card.Footer>
						<small className="text-muted">{event.StartingIn}</small>
					</Card.Footer>
				</Card>
			</Col>
		));
	};

	return (
		// Navbar and Carousel
		<div>
			<MyNavbar />
			<Carousel>
				<Carousel.Item>
					<img src={image1} alt="First slide" width="100%" height="600" />
					<Carousel.Caption>
						<h3></h3>
						<p></p>
					</Carousel.Caption>
				</Carousel.Item>
				<Carousel.Item>
					<img src={image2} alt="Second slide" width="100%" height="600" />
					<Carousel.Caption>
						<h3></h3>
						<p></p>
					</Carousel.Caption>
				</Carousel.Item>
				<Carousel.Item>
					<img src={image3} alt="Third slide" width="100%" height="600" />
					<Carousel.Caption>
						<h3></h3>
						<p></p>
					</Carousel.Caption>
				</Carousel.Item>
			</Carousel>
			{/* Events carousel */}
			<div className="container">
				<Row className="py-2">{createCards(eventData)}</Row>
			</div>
			<div>
				<CircleButton url="http://localhost:3000/create_event" />
			</div>
		</div>
	);
}

export default EventPage;

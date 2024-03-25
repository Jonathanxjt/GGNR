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
      .get("http://localhost:5000/event")
      .then((response) => {
        // .data.data is because json data sends code and data due to the microservice json response
        // Remove duplicate events based on the Title property
        const uniqueEvents = response.data.data.events.reduce(
          (acc, current) => {
            const isDuplicate = acc.find((event) => event.EID === current.EID);
            if (!isDuplicate) {
              // Format the date and time here
              const formattedDateTime = new Date(current.Time).toLocaleString(
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
              current.FormattedTime = formattedDateTime;
              acc.push(current);
            }
            return acc;
          },
          []
        );
        // Add a hasDuplicate variable to each event
        uniqueEvents.forEach((event) => {
          const duplicateCount = response.data.data.events.filter(
            (e) => e.EID === event.EID
          ).length;
          event.hasDuplicate = duplicateCount > 1;
        });

        setEventData(uniqueEvents);
        console.log(uniqueEvents);
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
            window.location.href = "/registration";
          }}
        >
          <Card.Img
            variant="top"
            src={event.EventLogo}
            onError={(e) => {
              e.target.src = { placeholder };
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
                {event.Capacity}
              </p>
            </Card.Text>
          </Card.Body>
          <Card.Footer>
            <small className="text-muted">Last updated mins ago</small>
          </Card.Footer>
        </Card>
      </Col>
    ));
  };

  // Function to create carousel items with cards
  const createCarouselItems = () => {
    const items = [];
    for (let i = 0; i < eventData.length; i += 4) {
      const eventsSlice = eventData.slice(i, i + 4);
      items.push(
        <Carousel.Item key={i}>
          <div className="d-flex">{createCards(eventsSlice)}</div>
        </Carousel.Item>
      );
    }
    return items;
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
    
    // Cards
  );
}

export default EventPage;

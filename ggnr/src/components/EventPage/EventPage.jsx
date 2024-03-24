import React, { useState, useEffect } from "react";
import { Row, Col } from "react-bootstrap";
import Carousel from "react-bootstrap/Carousel";
import PlaceHolderImage from "../PlaceHolderImage/PlaceHolderImage";
import { MyNavbar } from "../MyNavbar/MyNavbar";
import Card from "react-bootstrap/Card";
import image1 from "../../assets/image1.png";
import image2 from "../../assets/image2.png";
import image3 from "../../assets/image3.png";
import "./EventPage.css";
import axios from "axios";

function EventPage() {
  const [eventData, setEventData] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/event")
      .then((response) => {
        // .data.data is because json data sends code and data due to the microservice json response
        setEventData(response.data.data.events);
        console.log(response.data.data.events);
      })
      .catch((error) => {
        console.error("There was an error!", error);
      });
  }, []);

  // Function to create cards for each event
const createCards = (events) => {
  return events.map((event, index) => (
    <Col key={index} lg={3} md={4} sm={6} xs={12} className="mb-3">
    <Card key={index} className="card" onClick={() => {
      // Store the event data in local storage
      localStorage.setItem('selectedEvent', JSON.stringify(event));
      // Redirect to the registration page
      window.location.href = '/registration';
    }}>
      <Card.Img variant="top" src={event.EventLogo} />
      <Card.Body>
        <Card.Title>{event.Title}</Card.Title>
        <Card.Text>{event.Description}</Card.Text>
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
            <p>
              
            </p>
          </Carousel.Caption>
        </Carousel.Item>
      </Carousel>
      {/* Events carousel */}
      <div className="container">
      <Row className="py-2">
          {createCards(eventData)}
        </Row>
      </div>
    </div>
    // Cards
  );
}

export default EventPage;

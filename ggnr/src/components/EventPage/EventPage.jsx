import React, { useState, useEffect } from "react";
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
      <Card key={index} className="card">
        <Card.Img variant="top" src={event.EventLogo} />
        <Card.Body>
          <Card.Title>{event.Title}</Card.Title>
          <Card.Text>{event.Description}</Card.Text>
        </Card.Body>
        <Card.Footer>
          <small className="text-muted">Last updated mins ago</small>
        </Card.Footer>
      </Card>
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
          <img
            src={image1}
            alt="First slide"
            width="100%"
            height="400"
          />
          <Carousel.Caption>
            <h3>First slide label</h3>
            <p>Nulla vitae elit libero, a pharetra augue mollis interdum.</p>
          </Carousel.Caption>
        </Carousel.Item>
        <Carousel.Item>
          <img
            src={image2}
            alt="Second slide"
            width="100%"
            height="400"
          />
          <Carousel.Caption>
            <h3>Second slide label</h3>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
          </Carousel.Caption>
        </Carousel.Item>
        <Carousel.Item>
          <img
            src={image3}
            alt="Third slide"
            width="100%"
            height="400"
          />
          <Carousel.Caption>
            <h3>Third slide label</h3>
            <p>
              Praesent commodo cursus magna, vel scelerisque nisl consectetur.
            </p>
          </Carousel.Caption>
        </Carousel.Item>
      </Carousel>
      {/* Events carousel */}
      <div className="container">
        <Carousel indicators={false} interval={null}>
          {createCarouselItems()}
        </Carousel>
      </div>
    </div>
    // Cards
  );
}

export default EventPage;

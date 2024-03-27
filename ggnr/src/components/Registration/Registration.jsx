import React, { useState, useEffect } from "react";
import { Form, Button, Col, Row, Card } from "react-bootstrap";
import { useLocation } from "react-router-dom";
import { MyNavbar } from "../MyNavbar/MyNavbar";
import axios from "axios";

function Registration() {
  const [eventData, setEventData] = useState(null);
  const [selectedPriceId, setSelectedPriceId] = useState('');
  const location = useLocation();

  useEffect(() => {
    // Extract the title from the URL
    const title = new URLSearchParams(location.search).get("title");
    if (title) {
      axios
        .get(`http://localhost:5000/get_event/${title}`)
        .then((response) => {
          // Assuming the response contains the event data directly
          const event = response.data.data;

          // Format the time
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
          event.FormattedTime = formattedDateTime;

          setEventData(event);
          console.log(event);
        })
        .catch((error) => {
          console.error("There was an error!", error);
        });
    }
  }, [location.search]); // Re-run the effect if the search part of the URL changes

  const handleRegistrationSubmit = (e) => {
    e.preventDefault();
    if (selectedPriceId) {
      window.location.href = `/checkout?priceId=${encodeURIComponent(selectedPriceId)}`;
    } else {
      alert('Please select a ticket tier.');
    }
  };

  return (
    <div>
      <MyNavbar />
      <div className="container pt-3">
        <Row>
          <Col md={1}></Col>
          <Col
            md={4}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <div
              style={{
                textAlign: "center",
                justifyContent: "center",
                display: "flex",
                width: "1000px",
                height: "300px",
                backgroundColor: "#f0f0f0",
              }}
            >
              {eventData && (
                <img
                  src={eventData.EventLogo}
                  alt="Event"
                  style={{ width: "100%", height: "100%" }}
                />
              )}
            </div>
          </Col>
          <Col md={6}>
            <Card
              style={{
                background: "#003049",
                color: "white",
                padding: "0 20px",
                paddingBottom: "20px",
              }}
            >
              <Card.Header>{eventData && eventData.Title}</Card.Header>
              {/* Description */}
              {eventData && <p>{eventData.Description}</p>}
              {/* Location */}
              {eventData && <p>{eventData.Location}</p>}
              {/* Date/Time */}
              {eventData && <p>{eventData.FormattedTime}</p>}
              {/* Capacity */}
              {eventData &&
                eventData.event_types &&
                eventData.event_types.map((eventType, index) => (
                  <div key={index}>
                    <p>
                      {eventType.Category} - Slots left: {eventType.Capacity}
                    </p>
                  </div>
                ))}

              {/* Price */}
              {eventData && <p>{eventData.Price}</p>}

              <Form>
                <Form.Group className="mb-3">
                  <Form.Label>Select Ticket Tier</Form.Label>
                  <Form.Select onChange={(e) => setSelectedPriceId(e.target.value)}>
                    <option>Select a tier...</option>
                    {eventData &&
                      eventData.event_types &&
                      eventData.event_types.map((eventType, index) => (
                        <option key={index} value={eventType.PriceID}>
                          {eventType.Price === 0
                            ? `${eventType.Category} Ticket - Free Entry`
                            : `${
                                eventType.Category
                              } Ticket - ${eventType.Price.toFixed(2)} SGD`}
                        </option>
                      ))}
                  </Form.Select>
                </Form.Group>
                {/* Add more form fields here */}
                <Button variant="primary" type="submit" onClick={handleRegistrationSubmit}>
                  Register
                </Button>
              </Form>
            </Card>
          </Col>
        </Row>
      </div>
    </div>
  );
}

export default Registration;

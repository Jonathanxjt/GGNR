import React, { useState, useEffect } from "react";
import { Form, Button, Col, Row, Card } from "react-bootstrap";
import { MyNavbar } from "../MyNavbar/MyNavbar";
import axios from "axios";

function Registration() {
  const [eventData, setEventData] = useState(null);
  const selectedEvent = JSON.parse(localStorage.getItem("selectedEvent"));

  console.log(selectedEvent); // Use these values as needed

  useEffect(() => {
    axios
      .get("http://localhost:5000/event/1")
      .then((response) => {
        // .data.data is because json data sends code and data due to the microservice json response
        setEventData(response.data.data);
        console.log(response.data.data);
      })
      .catch((error) => {
        console.error("There was an error!", error);
      });
  }, []);

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
              {selectedEvent && (
                <img
                  src={selectedEvent.EventLogo}
                  alt="Event"
                  style={{ width: "100%", height: "100%" }}
                />
              )}
            </div>
          </Col>
          <Col md={6}>
            <Card style={{ background: "#003049", color: "white", padding:"0 20px", paddingBottom: "20px"}}>
              <Card.Header>{selectedEvent && selectedEvent.Title}</Card.Header>
              {/* Description */}
              {selectedEvent && <p>{selectedEvent.Description}</p>}
              {/* Location */}
              {selectedEvent && <p>{selectedEvent.Location}</p>}
              {/* Date/Time */}
              {selectedEvent && <p>{selectedEvent.FormattedTime}</p>}
              {/* Capacity */}
              {selectedEvent && <p>{selectedEvent.Capacity}</p>}
              {/* Price */}
              {selectedEvent && <p>{selectedEvent.Price}</p>}

              <Form>
                <Form.Group className="mb-3">
                  <Form.Label>Select Ticket Tier</Form.Label>
                  <Form.Select>
                    <option>Select a tier...</option>
                    <option value="tier1">Attendee Ticket - Free</option>
                    {selectedEvent.hasDuplicate && <option value="tier2">Competitor Ticket - 10.00 SGD</option>}
                  </Form.Select>
                </Form.Group>
                {/* Add more form fields here */}
                <Button variant="primary" type="submit">
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

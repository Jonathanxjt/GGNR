import React, { useState, useEffect } from "react";
import { Form, Button, Col, Row } from "react-bootstrap";
import { MyNavbar } from "../MyNavbar/MyNavbar";
import axios from "axios";

function Registration() {
  const [eventData, setEventData] = useState(null);

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
          md={3}
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <div
            style={{
              width: "300px",
              height: "600px",
              backgroundColor: "#f0f0f0",
            }}
          >
            {eventData && (
              <img
                src={`path/to/your/images/${eventData.EventLogo}`}
                alt="Event"
                style={{ width: "100%", height: "100%" }}
              />
            )}
          </div>
        </Col>
        <Col md={6}>

        {/* Description */}
          {eventData && (
            <p>{eventData.Description}</p>
            
          )}
          {/* Location */}
          {eventData && (
            <p>{eventData.Location}</p>
            
          )}
        {/* Date/Time */}
        {eventData && (
            <p>{eventData.Time}</p>
            
          )}
        {/* Capacity */}
        {eventData && (
            <p>{eventData.Capacity}</p>
            
          )}
          {/* Price */}
          {eventData && (
            <p>{eventData.Price}</p>
            
          )}

          <Form>
            <Form.Group className="mb-3">
              <Form.Label>Select Ticket Tier</Form.Label>
              <Form.Select>
                <option>Select a tier...</option>
                <option value="tier1">Tier 1</option>
                <option value="tier2">Tier 2</option>
                <option value="tier3">Tier 3</option>
              </Form.Select>
            </Form.Group>
            {/* Add more form fields here */}
            <Button variant="primary" type="submit">
              Register
            </Button>
          </Form>
        </Col>
        <Col md={1}></Col>
      </Row>
    </div>
  </div>
  );
}

export default Registration;

import React, { useState } from "react";
import { Form, Button, Col, Row } from "react-bootstrap";
import "./CreateEvent.css";
import { MyNavbar } from "../MyNavbar/MyNavbar";
import axios from "axios";

const CreateEvent = () => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [date, setDate] = useState("");
  const [location, setLocation] = useState("");
  const [image, setImage] = useState(null);
  const [time, setTime] = useState("");
  const [capacity, setCapacity] = useState(0);
  const [previewImage, setPreviewImage] = useState(null);
  const [gameName, setGameName] = useState("");
  const [gameResults, setGameResults] = useState([]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post("http://localhost:5000/search", {
        game_name: "Counter Strike",
      });
      setGameResults(response.data);
      console.log(response.data);
    } catch (error) {
      console.error("Error fetching game data:", error);
    }
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewImage(reader.result);
      };
      reader.readAsDataURL(file);
      setImage(file);
    }
  };



  return (
    <div>
      <MyNavbar />
      <div className="container">
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="title">
            <Form.Label>Title</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </Form.Group>

          <Form.Group controlId="description">
            <Form.Label>Description</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              placeholder="Enter description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </Form.Group>
          <Row className="g-2">
            <Col md>
              <Form.Group controlId="date">
                <Form.Label>Date</Form.Label>
                <Form.Control
                  type="date"
                  placeholder="Enter date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                />
              </Form.Group>
            </Col>
            <Col md>
              <Form.Group controlId="time">
                <Form.Label>Time</Form.Label>
                <Form.Control
                  type="time"
                  placeholder="Select time"
                  value={time}
                  onChange={(e) => setTime(e.target.value)}
                />
              </Form.Group>
            </Col>
          </Row>

          <Form.Group controlId="location">
            <Form.Label>Location</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
          </Form.Group>

          <Form.Group controlId="image">
            <Form.Label>Upload Image</Form.Label>
            <Form.Control
              type="file"
              accept="image/*"
              onChange={handleImageChange}
            />
            {previewImage && (
              <img
                src={previewImage}
                alt="Preview"
                style={{ marginTop: "10px", width: "300px", height: "300px" }}
              />
            )}
          </Form.Group>

          <Form.Group controlId="capacity">
            <Form.Label>Capacity</Form.Label>
            <Form.Control
              type="number"
              placeholder="Enter capacity"
              value={capacity}
              onChange={(e) => setCapacity(parseInt(e.target.value))}
            />
          </Form.Group>

          <Button variant="primary" type="submit">
            Create Event
          </Button>
        </Form>
      </div>
    </div>
  );
};

export default CreateEvent;

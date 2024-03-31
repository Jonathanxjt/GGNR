import React, { useState, useEffect} from "react";
import { Form, Button, Col, Row } from "react-bootstrap";
import "./CreateEvent.css";
import { toast, ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { MyNavbar } from "../MyNavbar/MyNavbar";
import axios from "axios";

const CreateEvent = () => {

  const [title, setTitle] = useState("");
  const [selectedTiers, setSelectedTiers] = useState(["Free Entry"]);
  const [freeEntryCapacity, setFreeEntryCapacity] = useState("");
  const [vipCapacity, setVipCapacity] = useState("");
  const [competitorCapacity, setCompetitorCapacity] = useState("");
  const [description, setDescription] = useState("");
  const [date, setDate] = useState("");
  const [location, setLocation] = useState("");
  const [image, setImage] = useState(null);
  const [eventLogo, setEventLogo] = useState("");
  const [time, setTime] = useState("");
  const [previewImage, setPreviewImage] = useState(null);
  const [gameName, setGameName] = useState("");
  const [organiser_company, setOrganiserCompany] = useState("");
  const [gameLogo, setGameLogo] = useState("");
  const [gameResults, setGameResults] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [isLoading, setIsLoading] = useState(false); // New state for loading status

  useEffect(() => {
    const user = JSON.parse(sessionStorage.getItem('user'));
    if (user) {
      setOrganiserCompany(user.organiser_company); // Assuming company is a property of the user object
    }
  }, []);
  
  const handleKeyDown = async (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      setIsLoading(true); // Set loading to true
      try {
        const response = await axios.post("http://localhost:5100/search", {
          game_name: gameName,
        });
        setGameResults(response.data);
        console.log(response.data);
        setShowDropdown(true);
      } catch (error) {
        console.error("Error fetching game data:", error);
      }
      setIsLoading(); // Set loading to false
    }
  };

  const handleCheckboxChange = (e) => {
    const { value, checked } = e.target;
    if (checked) {
      setSelectedTiers([...selectedTiers, value]);
    } else {
      setSelectedTiers(selectedTiers.filter((tier) => tier !== value));
    }
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreviewImage(reader.result);
        setEventLogo(reader.result); // Set the data URL for previewing and submitting the file
      };
      reader.readAsDataURL(file);
      setImage(file);
    }
  };
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Construct the EventTypes array based on the selected tiers and their capacities
    const eventTypes = [];
    if (selectedTiers.includes("Free Entry")) {
      eventTypes.push({
        TierID: 1,
        Category: "Audience",
        Price: 0,
        Capacity: parseInt(freeEntryCapacity, 10),
        PriceID: null,
      });
    }
    if (selectedTiers.includes("VIP")) {
      eventTypes.push({
        TierID: 2,
        Category: "VIP",
        Price: 10,
        Capacity: parseInt(vipCapacity, 10),
        PriceID: "price_1OxkTz2LfOffQtXe2Amrcy0e",
      }); 
    }
    if (selectedTiers.includes("Competitor")) {
      eventTypes.push({
        TierID: 3,
        Category: "Competitor",
        Price: 15,
        Capacity: parseInt(competitorCapacity,10),
        PriceID: "price_1OxkUn2LfOffQtXeGLBwfvyu",
      });
    }

    const eventData = {
      Title: title,
      Description: description,
      EventLogo: eventLogo, 
      GameName: gameName,
      GameLogo: gameLogo, 
      Location: location,
      Time: `${date} ${time}`,
      organiser_company: organiser_company,
      EventTypes: eventTypes
    };
    console.log('Submitting event data:', eventData); // Print the JSON data

    try {
      const response = await axios.post(
        "http://localhost:5100/create",
        eventData
      );
      console.log(response.data);
      // Handle success (e.g., redirect to another page or show a success message)
      console.log("Event Created!:", response.data.data);
      localStorage.setItem('toastMessage', 'Event Created!');
      window.location.href = "/events";

    } catch (error) {
      console.error("Error creating event:", error);
      console.error("Event creation error:", error.response.data.message);
      toast.error("Event Creation Failed!", {
        position: "top-center",
        autoClose: 3000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "dark",
        transition: Flip,
        });
      
      // Handle error (e.g., show an error message)
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

          <Form.Group>
            <Form.Label>Select Ticket Tiers</Form.Label>
            <Form.Check
              type="checkbox"
              label="Free Entry"
              value="Free Entry"
              checked={selectedTiers.includes("Free Entry")}
              onChange={(e) => handleCheckboxChange(e)}
            />
            {selectedTiers.includes("Free Entry") && (
              <Form.Control
                type="number"
                placeholder="Enter capacity for Free Entry"
                value={freeEntryCapacity}
                onChange={(e) => setFreeEntryCapacity(e.target.value)}
                max="10000"
              />
            )}

            <Form.Check
              type="checkbox"
              label="VIP"
              value="VIP"
              checked={selectedTiers.includes("VIP")}
              onChange={(e) => handleCheckboxChange(e)}
            />
            {selectedTiers.includes("VIP") && (
              <Form.Control
                type="number"
                placeholder="Enter capacity for VIP"
                value={vipCapacity}
                onChange={(e) => setVipCapacity(e.target.value)}
                max="1000"
              />
            )}

            <Form.Check
              type="checkbox"
              label="Competitor"
              value="Competitor"
              checked={selectedTiers.includes("Competitor")}
              onChange={(e) => handleCheckboxChange(e)}
            />
            {selectedTiers.includes("Competitor") && (
              <Form.Control
                type="number"
                placeholder="Enter capacity for Competitor"
                value={competitorCapacity}
                onChange={(e) => setCompetitorCapacity(e.target.value)}
                max="100"
              />
            )}
          </Form.Group>

          <Form.Group controlId="gameName" className="mt-2">
            <Form.Label>Game Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter game name"
              value={gameName}
              onChange={(e) => setGameName(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            {isLoading && <div style={{ height: "50px", width: "100%" }}></div>}
            {isLoading && <div className="custom-loader"></div>}

            {isLoading && (
              <div style={{ height: "750px", width: "100%" }}></div>
            )}

            {showDropdown && gameResults.length > 0 && (
              <ul
                style={{ listStyleType: "none", padding: "10px 0", margin: 0 }}
              >
                {gameResults.map((game) => (
                  <li
                    key={game.id}
                    style={{ cursor: "pointer", padding: "5px" }}
                    onClick={() => {
                      setGameName(game.name); // Update gameName with the selected game
                      setGameLogo(game.cover_url); // Update gameLogo with the selected game's cover URL
                      setShowDropdown(false); // Hide the dropdown
                    }}
                  >
                    <img
                      src={game.cover_url} // Use the .cover_url property for the image source
                      alt={game.name}
                      style={{
                        width: "150px",
                        height: "150px",
                        marginRight: "10px",
                      }} // Set the size of the thumbnail
                    />
                    {game.name}
                  </li>
                ))}
              </ul>
  
            )}
          </Form.Group>
          <div> </div>
          <Button variant="primary" type="submit" className="mt-3" >
            Create Event
          </Button>
        </Form>
      </div>
    </div>
  );
};

export default CreateEvent;

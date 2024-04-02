import React, { useState, useEffect } from "react";
import { Form, Button, Col, Row, Card } from "react-bootstrap";
import { useLocation } from "react-router-dom";
import { toast, ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { MyNavbar } from "../MyNavbar/MyNavbar";
import axios from "axios";
import MyFooter from "../MyFooter/MyFooter";

function Registration() {
  const [eventData, setEventData] = useState(null);
  const [selectedPriceId, setSelectedPriceId] = useState("");
  const [selectedTierId, setSelectedTierId] = useState("");
  const [hasTicket, setHasTicket] = useState(false); // State to store if the user has a ticket
  const user = JSON.parse(sessionStorage.getItem("user"));
  const location = useLocation();
  const [toastShown, setToastShown] = useState(false);

  useEffect(() => {
    // Extract the title from the URL
    const title = new URLSearchParams(location.search).get("title");
    const EID = new URLSearchParams(location.search).get("eid");
    if (EID) {
      axios
        .get(`http://localhost:5000/event/${EID}`)
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
      // Check if the user already has a ticket for the event
      axios
        .post("http://localhost:5008/check_event", { EID, UID: user.UID })
        .then((response) => {
          if (response.data.code === 200) {
            setHasTicket(true); // User has a ticket
          } else {
            setHasTicket(false); // User does not have a ticket
          }
        })
        .catch((error) => {
          console.error("Error checking event ticket:", error);
        });
    }
  }, [location.search]); // Re-run the effect if the search part of the URL changes
  
    // Show the toast message only once when the user has a ticket
    useEffect(() => {
      if (hasTicket && !toastShown) {
        setToastShown(true);
        toast.info('You are already registered for this event', {
          position: "top-center",
          autoClose: 6000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: "dark",
          transition: Flip,
        });
      }
    }, [hasTicket, toastShown]);

  const handleRegistrationSubmit = async (e) => {
    e.preventDefault();
    if (selectedTierId) {
      const registrationData = {
        EID: eventData.EID,
        TierID: selectedTierId,
        PriceID: selectedPriceId,
        UID: user.UID,
      };
      if (selectedPriceId === "null" || selectedPriceId === null) {
        try {
          await axios.post("http://localhost:5006/register", registrationData);
          // Registration successful, redirect to checkout
          toast.success("Ticket issued to your account!", {
            position: "top-center",
            autoClose: 2000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "dark",
            transition: Flip,
          });
        } catch (error) {
          // Handle registration error
          console.error("Registration error:", error);
          alert("Registration failed.");
        }
      } else {
        sessionStorage.setItem(
          "registrationData",
          JSON.stringify(registrationData)
        );
        window.location.href = `/checkout?priceId=${encodeURIComponent(
          selectedPriceId
        )}`;
      }
    } else {
      alert("Please select a ticket tier.");
    }
  };

  return (
    <div>
      <MyNavbar />
      <ToastContainer />
      <div className="container mt-5">
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
          <Col md={7}>
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
              {/* Organiser */}
              {eventData && <p>Organiser: {eventData.organiser_company}</p>}
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
                      {eventType.Category} -{" "}
                      {eventType.Capacity === 0
                        ? "Sold Out"
                        : `Slots left: ${eventType.Capacity}`}
                    </p>
                  </div>
                ))}

              {/* Price */}
              {eventData && <p>{eventData.Price}</p>}

              <Form>
                <Form.Group className="mb-3">
                  <Form.Label>Select Ticket Tier</Form.Label>
                  <Form.Select
                    disabled={hasTicket} // Disable the select if the user has a ticket
                    onChange={(e) => {
                      const [tierId, priceId] = e.target.value.split("-");
                      setSelectedTierId(tierId);
                      setSelectedPriceId(priceId === "null" ? null : priceId);
                    }}
                  >
                    <option>Select a tier...</option>
                    {eventData &&
                      eventData.event_types &&
                      eventData.event_types.map((eventType, index) => (
                        <option
                          key={index}
                          value={`${eventType.TierID}-${eventType.PriceID}`}
                          disabled={eventType.Capacity === 0 || hasTicket} // Disable the option if capacity is zero
                        >
                          {eventType.Capacity === 0
                            ? `${eventType.Category} Ticket - Sold Out` // Show "Sold Out" if capacity is zero
                            : eventType.Price === 0
                            ? `${eventType.Category} Ticket - Free Entry`
                            : `${
                                eventType.Category
                              } Ticket - ${eventType.Price.toFixed(2)} SGD`}
                        </option>
                      ))}
                  </Form.Select>
                </Form.Group>
                {/* Add more form fields here */}
                <Button
                  variant="primary"
                  type="submit"
                  disabled={hasTicket} // Disable the button if the user has a ticket
                  onClick={handleRegistrationSubmit}
                >
                  Register
                </Button>
              </Form>
            </Card>
          </Col>
        </Row>
      </div>
      <MyFooter />
    </div>
  );
}

export default Registration;

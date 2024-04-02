import React, { useState, useEffect } from "react";
import { Form, Button,Card, Table } from "react-bootstrap";
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
  // Check if the user is an organizer
  const isOrganiser = user && user.organiser;

	useEffect(() => {
		// Extract the title from the URL
		const title = new URLSearchParams(location.search).get("title");
		const EID = new URLSearchParams(location.search).get("eid");
		if (EID) {
			axios
				.get(`http://localhost:8000/event/${EID}`)
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
      toast.info("You are already registered for this event", {
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
					await axios.post("http://localhost:8000/api/v1/register", registrationData);
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
		<Card
			style={{
				background: "#003049",
				color: "white",
				padding: "0 20px",
				paddingBottom: "20px",
				alignSelf: "center",
			}}
		>
			<Card.Header
				style={{
					textAlign: "center",
					fontSize: 45,
					marginBottom: 10,
				}}
			>
				{eventData && eventData.Title}
			</Card.Header>
			{eventData && (
				<img
					src={eventData.EventLogo}
					alt="Event"
					style={{ width: "100%", height: "100%" }}
				/>
			)}
			<br></br>
			<Table hover border responsive variant="dark">
				<tbody style={{ margin: 5 }}>
					{eventData && (
						<thead>
							<tr>
								<th style={{ padding: "10px", minWidth:300 }}>Description</th>
								<td style={{ padding: "10px", minWidth:1000 }}>{eventData.Description}</td>
							</tr>
							<tr>
								<th style={{ padding: "10px" }}>Organiser</th>
								<td style={{ padding: "10px" }}>
									{eventData.organiser_company}
								</td>
							</tr>
							<tr>
								<th style={{ padding: "10px" }}>Location</th>
								<td style={{ padding: "10px" }}>{eventData.Location}</td>
							</tr>
							<tr>
								<th style={{ padding: "10px" }}>Time</th>
								<td style={{ padding: "10px" }}>
									{eventData.FormattedTime}
								</td>
							</tr>
							{eventData.event_types &&
								eventData.event_types.map((eventType, index) => (
									<tr key={index}>
										<th
											style={{ padding: "10px" }}
											className="bg-secondary"
										>
											{eventType.Category}
										</th>
										<td
											style={{ padding: "10px" }}
											className="bg-secondary"
										>
											Slots left: {eventType.Capacity}
										</td>
									</tr>
								))}
						</thead>
					)}
				</tbody>
			</Table>

              <Form>
                <Form.Group className="mb-3">
                  <Form.Label>Select Ticket Tier</Form.Label>
                  <Form.Select
                    disabled={hasTicket}
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
                <Button
                  variant="primary"
                  type="submit"
                  disabled={hasTicket || isOrganiser}
                  onClick={handleRegistrationSubmit}
                >
                  Register
                </Button>
              </Form>
            </Card>
			</div>
      <MyFooter />
    </div>
  );
}

export default Registration;

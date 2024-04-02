import React, { useState, useEffect } from "react";
import { Tab, Tabs, Form, Button, Table, Card } from "react-bootstrap";
import { toast, ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { MyNavbar } from "../MyNavbar/MyNavbar";
import axios from "axios";
import "./UserProfile.css";
import MyFooter from "../MyFooter/MyFooter";

const UserProfile = () => {
	const [key, setKey] = useState("tickets");
	const [username, setUsername] = useState("");
	const [password, setPassword] = useState("");
	const [contact, setContact] = useState(""); 
	const [email, setEmail] = useState(""); 
	const [preferences, setPreferences] = useState("");
	const [gameName, setGameName] = useState("");
	const [showDropdown, setShowDropdown] = useState(false);
	const [isLoading, setIsLoading] = useState(false); 
	const [gameResults, setGameResults] = useState([]);
	const [userPreferences, setUserPreferences] = useState([]);
	const [UID, setUID] = useState(null);
	const [userTickets, setUserTickets] = useState([]);

	useEffect(() => {
		const fetchData = async () => {
			const user = JSON.parse(sessionStorage.getItem("user"));
			if (user) { // Check if user is logged in
				setUID(user.UID);
				setUsername(user.username);
				setEmail(user.email);
				setContact(user.contact);
				if (user.preferences) {
					setUserPreferences(user.preferences.split(","));
					setPreferences(user.preferences.split(","));
				}
				try {
					const response = await axios.get(
						`http://localhost:5008/ticket/${user.UID}`
					);
					const tickets = response.data.data;

					const eventDetailsPromises = tickets.map(async (ticket) => {
						const eventResponse = await axios.get(
							`http://localhost:5000/event/${ticket.EID}`
						);
						// Format the date and time
						const formattedDateTime = new Date(
							eventResponse.data.data.Time
						).toLocaleString("en-SG", {
							day: "numeric",
							month: "long",
							year: "numeric",
							hour: "numeric",
							minute: "numeric",
							hour12: true,
						});

						// Find the matching category based on PriceID
						const matchingEventType = eventResponse.data.data.event_types.find(
							(eventType) => eventType.PriceID === ticket.PriceID
						);
						const category = matchingEventType
							? matchingEventType.Category
							: "Unknown";
						return {
							...ticket,
							eventName: eventResponse.data.data.Title,
							eventLogo: eventResponse.data.data.EventLogo,
							eventDateTime: formattedDateTime, // Use the formatted date and time
							category: category,
						};
					});

          const ticketsWithEventDetails = await Promise.all(
            eventDetailsPromises
          );
          setUserTickets(ticketsWithEventDetails);
          console.log(ticketsWithEventDetails);
        } catch (error) {
          console.error("Error fetching user tickets or event details:", error);
        }
      }
      else
      {
        localStorage.setItem('toastErrorMessage', 'Please Login first!');
        window.location.href = "/login";
      }
    };

		fetchData();
	}, []);

	const handlePreferenceChange = (preference) => {
		setPreferences((prevPreferences) => {
			if (prevPreferences.includes(preference)) {
				return prevPreferences.filter((pref) => pref !== preference);
			} else {
				return [...prevPreferences, preference];
			}
		});
	};

	const handleKeyDown = async (event) => {
		if (event.key === "Enter") {
			event.preventDefault();
			setIsLoading(true); // Set loading to true
			try {
				const response = await axios.post("http://localhost:5009/search", {
					game_name: gameName, // Send the game name to the backend 
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

	const handleSave = (section) => {
		if (section === "Preferences") {
			console.log(UID);
			console.log(preferences);
			let preferencesString = preferences.join(",");
			console.log(preferencesString);
			axios
				.put(`http://localhost:5005/user/edit_preference/${UID}`, {
					preferences: preferencesString,
				})
				.then((response) => {
					toast.success("Preferences Updated!", {
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
					// Update the user object in sessionStorage
					const user = JSON.parse(sessionStorage.getItem("user"));
					user.preferences = preferencesString;
					sessionStorage.setItem("user", JSON.stringify(user));
				})
				.catch((error) => {
					console.error("Error updating preferences:", error);
					toast.error("Failed to update preferences!", {
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
				});
		} else {
			// Implement save logic for other sections (username, password, etc.)
			alert(`${section} updated!`);
		}
	};

  return (
    <div>
      <MyNavbar />
      <div className="container user-profile py-3">
        <Card>
          <Card.Body className="user-profile-card">
            <h2>Welcome {username}!</h2>
            <Table variant="light" bordered responsive>
              <tbody>
                <tr>
                  <th>Username</th>
                  <td>{username}</td>
                </tr>
                <tr>
                  <th>Email</th>
                  <td>{email}</td>
                </tr>
                <tr>
                  <th>Contact</th>
                  <td>{contact}</td>
                </tr>
              </tbody>
            </Table>
          </Card.Body>
        </Card>
        <Tabs activeKey={key} onSelect={(k) => setKey(k)} className="mb-3">
          <Tab eventKey="tickets" title="My Tickets">
            <div className="user-card-container">
              <Card>
                <Card.Body className="user-card-body">
                  {userTickets.length > 0 ? (
                    <Table striped bordered hover responsive>
                      <thead>
                        <tr>
                          <th>Event Logo</th>
                          <th>Event Title</th>
                          <th>Date/Time</th>
                          <th>Category</th>
                          <th>Ticket ID</th>
                          <th>Event ID</th>
                        </tr>
                      </thead>
                      <tbody>
                        {userTickets.map((ticket, index) => (
                          <tr key={index}>
                            <td>
                              <img
                                src={ticket.eventLogo}
                                alt="Event Logo"
                                style={{ width: "150px", height: "100px" }}
                              />
                            </td>
                            <td>{ticket.eventName}</td>
                            <td>{ticket.eventDateTime}</td>
                            <td>{ticket.category}</td>
                            <td>{ticket.TicketID}</td>
                            <td>{ticket.EID}</td>
                          </tr>
                        ))}
                      </tbody>
                    </Table>
                  ) : (
                    <p>You do not have any tickets.</p>
                  )}
                </Card.Body>
              </Card>
            </div>
          </Tab>
          <Tab eventKey="preferences" title="Preferences">
            <div className="user-card-container">
              <Card>
                <Card.Body className="user-card-body">
                  <Form>
                    {userPreferences.map((preference, index) => (
                      <Form.Check
                        key={index}
                        type="checkbox"
                        label={preference}
                        checked={preferences.includes(preference)}
                        onChange={() => handlePreferenceChange(preference)}
                      />
                    ))}

                    <Form.Group className="mb-3">
                      <Form.Label>Preferences</Form.Label>
                      <Form.Control
                        type="text"
                        placeholder="Enter your preferences"
                        value={preferences}
                        onChange={(e) => setPreferences(e.target.value)}
                        disabled
                      />
                    </Form.Group>

                    <Form.Group controlId="gameName" className="mt-2">
                      <Form.Label>Game Name</Form.Label>
                      <Form.Control
                        type="text"
                        placeholder={
                          userPreferences.length >= 6
                            ? "You can only have a maximum of 6 preferences"
                            : "Enter game name"
                        }
                        value={gameName}
                        onChange={(e) => setGameName(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={preferences.length >= 6}
                        className={
                          userPreferences.length >= 6 ? "red-placeholder" : ""
                        }
                      />
                      {isLoading && (
                        <div style={{ height: "50px", width: "100%" }}></div>
                      )}
                      {isLoading && <div className="user-custom-loader"></div>}

                      {isLoading && (
                        <div style={{ height: "750px", width: "100%" }}></div>
                      )}

                      {showDropdown && gameResults.length > 0 && (
                        <ul
                          style={{
                            listStyleType: "none",
                            padding: "10px 0",
                            margin: 0,
                          }}
                        >
                          {gameResults.map((game) => (
                            <li
                              key={game.id}
                              style={{ cursor: "pointer", padding: "5px" }}
                              onClick={() => {
                                // Add the selected game name to the user preferences array
                                setUserPreferences((prevPrefs) => {
                                  if (!prevPrefs.includes(game.name)) {
                                    return [...prevPrefs, game.name];
                                  }
                                  return prevPrefs;
                                });
                                setPreferences((prevPrefs) => {
                                  if (!prevPrefs.includes(game.name)) {
                                    return [...prevPrefs, game.name];
                                  }
                                  return prevPrefs;
                                });
                                setGameName(""); // Reset the gameName state to blank
                                setShowDropdown(false); // Hide the dropdown
                              }}
                            >
                              <img
                                src={game.cover_url}
                                alt={game.name}
                                style={{
                                  width: "150px",
                                  height: "150px",
                                  marginRight: "10px",
                                }}
                              />
                              {game.name}
                            </li>
                          ))}
                        </ul>
                      )}
                    </Form.Group>
                    <Button
                      className="mt-3"
                      variant="primary"
                      onClick={() => handleSave("Preferences")}
                    >
                      Save Preferences
                    </Button>
                  </Form>
                </Card.Body>
              </Card>
            </div>
          </Tab>
				</Tabs>
			</div>
      <MyFooter />
		</div>
	);
};

export default UserProfile;

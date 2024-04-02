import React, { useState, useEffect } from "react";
import { Tab, Tabs, Form, Button } from "react-bootstrap";
import { MyNavbar } from "../MyNavbar/MyNavbar";
import axios from "axios";

const UserProfile = () => {
  const [key, setKey] = useState("preferences");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [preferences, setPreferences] = useState("");
  const [gameName, setGameName] = useState("");
  const [showDropdown, setShowDropdown] = useState(false);
  const [isLoading, setIsLoading] = useState(false); // New state for loading status
  const [gameResults, setGameResults] = useState([]);
  const [userPreferences, setUserPreferences] = useState([]);
  const [UID, setUID] = useState(null);

  useEffect(() => {
    const user = JSON.parse(sessionStorage.getItem('user'));
    if (user) {
      setUID(user.UID); // Assuming UID is a property of the user object
      if (user.preferences) {
        setUserPreferences(user.preferences.split(','));
        setPreferences(user.preferences.split(','));
      }
    }
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
        const response = await axios.post("http://localhost:8000/api/v1/search", {
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

  const handleSave = (section) => {
    if (section === 'Preferences') {
      console.log(UID)
      console.log(preferences)
      let preferencesString = preferences.join(',');
      console.log(preferencesString)
      axios
        .put(`http://localhost:8000/edit_preference/${UID}`, {
          preferences: preferencesString,
        })
        .then((response) => {
          alert('Preferences updated successfully!');
          // Update the user object in sessionStorage
          const user = JSON.parse(sessionStorage.getItem('user'));
          user.preferences = preferencesString;
          sessionStorage.setItem('user', JSON.stringify(user));
        })
        .catch((error) => {
          console.error('Error updating preferences:', error);
          alert('Failed to update preferences.');
        });
    } else {
      // Implement save logic for other sections (username, password, etc.)
      alert(`${section} updated!`);
    }
  };

  return (
    <div>
      <MyNavbar />
      <div className="user-profile py-3">
        <h2>User Profile</h2>
        <Tabs activeKey={key} onSelect={(k) => setKey(k)} className="mb-3">
          <Tab eventKey="preferences" title="Preferences">
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
                  placeholder={userPreferences.length >= 6 ? "You can only have a maximum of 6 preferences" : "Enter game name"}
                  value={gameName}
                  onChange={(e) => setGameName(e.target.value)}
                  onKeyDown={handleKeyDown}
                  disabled={preferences.length >= 6}
                  className={userPreferences.length >= 6 ? "red-placeholder" : ""}
                />
                {isLoading && (
                  <div style={{ height: "50px", width: "100%" }}></div>
                )}
                {isLoading && <div className="custom-loader"></div>}

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
          </Tab>
          <Tab eventKey="username" title="Username">
            <Form>
              <Form.Group className="mb-3">
                <Form.Label>Username</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter new username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                />
              </Form.Group>
              <Button variant="primary" onClick={() => handleSave("Username")}>
                Save Username
              </Button>
            </Form>
          </Tab>
          <Tab eventKey="password" title="Password">
            <Form>
              <Form.Group className="mb-3">
                <Form.Label>Password</Form.Label>
                <Form.Control
                  type="password"
                  placeholder="Enter new password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </Form.Group>
              <Button
                className="mt-3"
                variant="primary"
                onClick={() => handleSave("Password")}
              >
                Save Password
              </Button>
            </Form>
          </Tab>
        </Tabs>
      </div>
    </div>
  );
};

export default UserProfile;

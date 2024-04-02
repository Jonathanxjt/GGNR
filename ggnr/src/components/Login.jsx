import React, { useState, useEffect } from "react";
import { Form, Row, Col } from "react-bootstrap";
import axios from "axios"; // Import Axios
import "./Login.css";
import { toast, ToastContainer, Flip } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { MyNavbar } from "./MyNavbar/MyNavbar";
import logo from "../assets/logo.png";
import { useNavigate } from "react-router-dom";


const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const [confirmPassword, setConfirmPassword] = useState("");
  const [username, setUsername] = useState("");
  const [contact, setContact] = useState("");
  const [preferences, setPreferences] = useState("");
  const [isOrganiser, setIsOrganiser] = useState(false);
  const [organiserCompany, setOrganiserCompany] = useState(null);

  const handleEmailChange = (e) => setEmail(e.target.value);
  const handlePasswordChange = (e) => setPassword(e.target.value);
  const handleConfirmPasswordChange = (e) => setConfirmPassword(e.target.value);
  const handleUsernameChange = (e) => setUsername(e.target.value);
  const handleContactChange = (e) => setContact(e.target.value);
  const handlePreferencesChange = (e) => setPreferences(e.target.value);
  const handleOrganiserChange = (e) => setIsOrganiser(e.target.checked);
  const handleOrganiserCompanyChange = (e) =>
    setOrganiserCompany(e.target.value);

  const navigate = useNavigate();

  useEffect(() => {
    const user = JSON.parse(sessionStorage.getItem("user"));
    if (user) {
      navigate('/');
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isLogin) {
      try {
        const response = await axios.get(
          `http://localhost:8000/user/check-password/${email}/password/${password}`
        );
        if (
          response.data.code === 200 &&
          response.data.message === "Correct password"
        ) {
          // Login successful
          console.log("Login successful:", response.data.data);
          sessionStorage.setItem("user", JSON.stringify(response.data.data));
          toast.success("Login Successful!", {
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
            localStorage.setItem('toastMessage', 'Login Successful!');
            window.location.href = "/events";
        } else {
          // Login failed
          console.log("Login failed:", response.data.message);
          toast.error("Login failed: Incorrect email or password!", {
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

        }
      } catch (error) {
        console.error("Login error:", error.response.data.message);
        toast.error("Login failed: Incorrect email or password!", {
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

      }
    } else {
      // Handle registration
      try {
        const response = await axios.post("http://localhost:8000/user/create_user", {
          username,
          password,
          preferences,
          email,
          contact,
          organiser: isOrganiser,
          organiser_com: organiserCompany,
        });
        if (response.data.code === 201) {
          // Registration successful
          console.log("Registration successful:", response.data.data);
          localStorage.setItem('toastMessage', 'Registration Successful!');
          window.location.href = "/login";

        } else {
          // Registration failed
          console.log("Registration failed:", response.data.message);

        }
      } catch (error) {
        console.error("Registration error:", error.response.data.message);
        // Handle other errors, such as network errors or server errors
      }
    }
  };

  return (
    <div>
  <MyNavbar />
  <ToastContainer />
  <div className="login-page">
  <div className="login-container">
    <div className="logincard">
      <form onSubmit={handleSubmit}>
        <div className="box">
          <div className="loginhead">
            <span>{isLogin ? "Login" : "Register"}</span>
          </div>
          <div className="loginhead">
            <span>{isLogin ? "Login" : "Register"}</span>
          </div>
        </div>
        <Form.Floating className="mb-3">
          <Form.Control
            id="floatingInputEmail"
            type="email"
            placeholder="name@example.com"
            value={email}
            onChange={handleEmailChange}
            required
          />
          <label htmlFor="floatingInputEmail">Email address</label>
        </Form.Floating>
        <Form.Floating className="mb-3">
          <Form.Control
            id="floatingPassword"
            type="password"
            placeholder="Password"
            value={password}
            onChange={handlePasswordChange}
            required
          />
          <label htmlFor="floatingPassword">Password</label>
        </Form.Floating>
        {!isLogin && (
          <>
            <Form.Floating className="mb-3">
              <Form.Control
                id="floatingConfirmPassword"
                type="password"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={handleConfirmPasswordChange}
                required={!isLogin}
              />
              <label htmlFor="floatingConfirmPassword">
                Confirm Password
              </label>
            </Form.Floating>
            <Row>
              <Col>
                <Form.Floating className="mb-3">
                  <Form.Control
                    id="floatingUsername"
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={handleUsernameChange}
                    required={!isLogin}
                  />
                  <label htmlFor="floatingUsername">Username</label>
                </Form.Floating>
              </Col>
              <Col>
                <Form.Floating className="mb-3">
                  <Form.Control
                    id="floatingContact"
                    type="text"
                    placeholder="Contact Number"
                    value={contact}
                    onChange={handleContactChange}
                    required={!isLogin}
                  />
                  <label htmlFor="floatingContact">Contact Number</label>
                </Form.Floating>
              </Col>
            </Row>

            <Form.Check
              type="checkbox"
              id="organiserCheck"
              label="Are you an Organiser?"
              checked={isOrganiser}
              onChange={handleOrganiserChange}
            />
            {isOrganiser && (
              <Form.Floating className="mb-3">
                <Form.Control
                  id="floatingOrganiserCompany"
                  type="text"
                  placeholder="Organiser Company"
                  value={organiserCompany}
                  onChange={handleOrganiserCompanyChange}
                  required={isOrganiser}
                />
                <label htmlFor="floatingOrganiserCompany">
                  Organiser Company
                </label>
              </Form.Floating>
            )}
          </>
        )}
        <button type="submit" className="submitbutton">
          {isLogin ? "Login" : "Register"}
        </button>
        <button
          type="button"
          className="switch-button"
          onClick={() => setIsLogin(!isLogin)}
        >
          {isLogin ? "Switch to Register" : "Switch to Login"}
        </button>
      </form>
    </div>
  </div>
</div>
</div>
  );
};

export default Login;

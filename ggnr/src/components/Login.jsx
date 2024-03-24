import React, { useState } from 'react';
import { Form } from 'react-bootstrap';
import axios from 'axios'; // Import Axios
import './Login.css';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isLogin, setIsLogin] = useState(true);

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.get(
                `http://localhost:5005/user/check-password/${email}/password/${password}`
            );
            if (response.data.code === 201 && response.data.message === 'Correct password') {
                // Login successful
                console.log('Login successful:', response.data.data);
                // You can now redirect the user or set the user data in your state
            } else {
                // Login failed
                console.log('Login failed:', response.data.message);
                // You can show an error message to the user
            }
        } catch (error) {
            console.error('Login error:', error.response.data.message);
            // Handle other errors, such as network errors or server errors
        }
    };

    return (
        <div className="login-container">
            <div className="card">
                <h2>{isLogin ? 'Login' : 'Register'}</h2>
                <form onSubmit={handleSubmit}>
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
                    <button type="submit">{isLogin ? 'Login' : 'Register'}</button>
                    <button type="button" className="switch-button" onClick={() => setIsLogin(!isLogin)}>
                        {isLogin ? 'Switch to Register' : 'Switch to Login'}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;

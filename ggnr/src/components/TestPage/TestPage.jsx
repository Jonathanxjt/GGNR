import React from 'react';
import placeholder from "../../assets/placeholder.jpg";

const TestPage = () => {
    return (
        <div>
            <h1>Test Page</h1>
            <p>This is a test page for React.</p>
            <img src="https://i.ibb.co/VLB3xff/fn.png"></img>
            <img src={placeholder}></img>
        </div>
    );
};

export default TestPage;
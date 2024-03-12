import React from 'react';
import {MyNavbar} from './MyNavbar/MyNavbar';

const HomePage = () => {
  return (
    <div style={{ textAlign: 'center' }}>
      <MyNavbar/>
      <h1>Welcome to Our Website</h1>
      <p>This is the home page. Explore our site to learn more about us.</p>
    </div>
  );
};

export default HomePage;

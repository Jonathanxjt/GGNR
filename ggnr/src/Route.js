import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import EventPage from './components/EventPage/EventPage';
import NotFoundPage from './components/NotFoundPage';

const RouteConfig = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/event" element = {<EventPage/>}/>
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
};

export default RouteConfig;
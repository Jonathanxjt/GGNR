import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/HomePage';
import EventPage from './components/EventPage/EventPage';
import CreateEvent from './components/CreateEvent/CreateEvent';
import NotFoundPage from './components/NotFoundPage';
import Registration from './components/Registration/Registration';

const RouteConfig = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/events" element = {<EventPage/>}/>
        <Route path="/create_event" element = {<CreateEvent/>}/>
        <Route path="/event/:id" element={<EventPage />} />
        <Route path="/registration" element={<Registration/>} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Router>
  );
};

export default RouteConfig;
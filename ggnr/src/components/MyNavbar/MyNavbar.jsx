import React from "react";
import { Navbar, Nav, Form } from "react-bootstrap";
import { BsPerson } from "react-icons/bs";
import "./MyNavbar.css";

export const MyNavbar = () => {

  const profileIconStyle = {
    fontSize: '20px', // Adjust size as needed
    color: '#FFFFFF', // Adjust color as needed
    marginLeft: '15px', // Adjust spacing as needed
    cursor: 'pointer',
  };
  
  return (
    <Navbar variant='dark' expand="lg" className="px-4 sticky-top custom-navbar" >
      <Navbar.Brand href="/">GGNR.</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mx-auto">
          <Nav.Link href="/">Home</Nav.Link>
          <Nav.Link href="/events">Events</Nav.Link>
          <Nav.Link href="#games">Games</Nav.Link>
        </Nav>
        <Nav.Link href="/login" style={profileIconStyle}>
          <BsPerson />
        </Nav.Link>
      </Navbar.Collapse >
    </Navbar>
  );
};

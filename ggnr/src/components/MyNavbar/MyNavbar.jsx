import React from "react";
import { Navbar, Nav, Form, FormControl} from "react-bootstrap";
import { BsPerson } from "react-icons/bs";
import { BiSearch } from "react-icons/bi";

export const MyNavbar = () => {
  const searchContainerStyle = {
    display: 'flex',
    alignItems: 'center',
    background: 'light', // This should match the bg-light color
    border: '1px solid #ddd', // Adjust as needed
    padding: '5px 10px',
    borderRadius: '30px', // Makes it pill-shaped
  };

  const searchIconStyle = {
    marginRight: '10px',
    color: '#495057', // Adjust as needed
  };

  const profileIconStyle = {
    fontSize: '20px', // Adjust size as needed
    color: '#495057', // Adjust color as needed
    marginLeft: '15px', // Adjust spacing as needed
    cursor: 'pointer',
  };
  
  return (
    <Navbar bg="light" expand="lg" className="px-4">
      <Navbar.Brand href="#home">GGNR.</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mx-auto">
          <Nav.Link href="#home">Home</Nav.Link>
          <Nav.Link href="#events">Events</Nav.Link>
          <Nav.Link href="#games">Games</Nav.Link>
          <Nav.Link href="#about-us">About Us</Nav.Link>
        </Nav>
        <Form inline className="d-flex align-items-center">
          <div style={searchContainerStyle}>
            <BiSearch style={searchIconStyle} />
            <FormControl
              type="text"
              placeholder="Search anything..."
              className="border-0"
              style={{ outline: 'none', boxShadow: 'none' }} // Removes the default focus styles
            />
          </div>
          <BsPerson style={profileIconStyle} />
        </Form>
      </Navbar.Collapse>
    </Navbar>
  );
};

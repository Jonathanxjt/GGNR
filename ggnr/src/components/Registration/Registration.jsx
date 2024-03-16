import React from 'react';
import { Form, Button, Col, Row } from "react-bootstrap";
import { MyNavbar } from "../MyNavbar/MyNavbar";

function Registration() {
  return (
    <div>
      <MyNavbar />
      <div className="container pt-3">
        <Row>
          <Col
            md={6}
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <div
              style={{
                width: "300px",
                height: "600px",
                backgroundColor: "#f0f0f0",
              }}
            >
              {/* Place your image here */}
              <img
                src="path/to/your/image.jpg"
                alt="Placeholder"
                style={{ width: "100%", height: "100%" }}
              />
            </div>
          </Col>
          <Col md={6}>
            <p> Lorem ipsum dolor sit amet consectetur adipisicing elit. Atque, tempore ex? Enim, voluptatibus nam sequi temporibus officiis, quod aperiam accusantium quaerat natus non distinctio beatae qui sapiente delectus animi culpa.
                Lorem ipsum dolor, sit amet consectetur adipisicing elit. Esse illum qui natus minima voluptate repudiandae, delectus possimus laboriosam reiciendis libero quasi modi est aliquam iusto magni sapiente aut animi quibusdam?
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Impedit quaerat alias in cum perspiciatis nisi quo laborum? Repellendus quis illum, eos vitae eligendi rem, in eius consequuntur et esse perspiciatis.
                Lorem ipsum dolor sit amet consectetur adipisicing elit. Minus laboriosam libero, obcaecati illo, aliquam pariatur sit vel hic officia accusantium voluptate explicabo voluptas quibusdam sint, quae tempore itaque voluptatem quaerat?
            </p>
            <Form>
              <Form.Group className="mb-3">
                <Form.Label>Select Ticket Tier</Form.Label>
                <Form.Select>
                  <option>Select a tier...</option>
                  <option value="tier1">Tier 1</option>
                  <option value="tier2">Tier 2</option>
                  <option value="tier3">Tier 3</option>
                </Form.Select>
              </Form.Group>
              {/* Add more form fields here */}
              <Button variant="primary" type="submit">
                Submit
              </Button>
            </Form>
          </Col>
        </Row>
      </div>
    </div>
  );
}

export default Registration;

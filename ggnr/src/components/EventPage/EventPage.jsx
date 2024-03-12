import React from "react";
import Carousel from "react-bootstrap/Carousel";
import PlaceHolderImage from "../PlaceHolderImage/PlaceHolderImage";
import { MyNavbar } from "../MyNavbar/MyNavbar";
import Card from 'react-bootstrap/Card';
import './EventPage.css'; 

function EventPage() {
  return (
    // Navbar and Carousel
    <div> 
      <MyNavbar />
      <Carousel>
        <Carousel.Item>
          <PlaceHolderImage />
          <Carousel.Caption>
            <h3>First slide label</h3>
            <p>Nulla vitae elit libero, a pharetra augue mollis interdum.</p>
          </Carousel.Caption>
        </Carousel.Item>
        <Carousel.Item>
          <PlaceHolderImage />
          <Carousel.Caption>
            <h3>Second slide label</h3>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
          </Carousel.Caption>
        </Carousel.Item>
        <Carousel.Item>
          <PlaceHolderImage />
          <Carousel.Caption>
            <h3>Third slide label</h3>
            <p>
              Praesent commodo cursus magna, vel scelerisque nisl consectetur.
            </p>
          </Carousel.Caption>
        </Carousel.Item>
      </Carousel>
      {/* Events carousel */}
    <div className="container">
    <Carousel indicators={false} interval={null}>
        <Carousel.Item>
          <div className="d-flex">
            <Card className="card">
              <Card.Img variant="top" src="holder.js/100px160" />
              <Card.Body>
                <Card.Title>Card title 1</Card.Title>
                <Card.Text>
                This card has supporting text below as a natural lead-in to
                  additional content.
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Last updated 3 mins ago</small>
              </Card.Footer>
            </Card>
            <Card className="card">
              <Card.Img variant="top" src="holder.js/100px160" />
              <Card.Body>
                <Card.Title>Card title 2</Card.Title>
                <Card.Text>
                This card has supporting text below as a natural lead-in to
                  additional content.
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Last updated 3 mins ago</small>
              </Card.Footer>
            </Card>
            <Card className="card">
              <Card.Img variant="top" src="holder.js/100px160" />
              <Card.Body>
                <Card.Title>Card title 3</Card.Title>
                <Card.Text>
                This card has supporting text below as a natural lead-in to
                  additional content.
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Last updated 3 mins ago</small>
              </Card.Footer>
            </Card>
            <Card className="card">
              <Card.Img variant="top" src="holder.js/100px160" />
              <Card.Body>
                <Card.Title>Card title 4</Card.Title>
                <Card.Text>
                This card has supporting text below as a natural lead-in to
                  additional content.
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Last updated 3 mins ago</small>
              </Card.Footer>
            </Card>
          </div>
        </Carousel.Item>
        <Carousel.Item>
          <div className="d-flex">
            <Card className="card">
              <Card.Img variant="top" src="holder.js/100px160" />
              <Card.Body>
                <Card.Title>Card title 5</Card.Title>
                <Card.Text>
                  This card has supporting text below as a natural lead-in to
                  additional content.
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Last updated 3 mins ago</small>
              </Card.Footer>
            </Card>
            <Card className="card">
              <Card.Img variant="top" src="holder.js/100px160" />
              <Card.Body>
                <Card.Title>Card title 6</Card.Title>
                <Card.Text>
                  This card has supporting text below as a natural lead-in to
                  additional content.
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Last updated 3 mins ago</small>
              </Card.Footer>
            </Card>
            <Card className="card">
              <Card.Img variant="top" src="holder.js/100px160" />
              <Card.Body>
                <Card.Title>Card title 7</Card.Title>
                <Card.Text>
                This card has supporting text below as a natural lead-in to
                  additional content.
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Last updated 3 mins ago</small>
              </Card.Footer>
            </Card>
            <Card className="card">
              <Card.Img variant="top" src="holder.js/100px160" />
              <Card.Body>
                <Card.Title>Card title 8</Card.Title>
                <Card.Text>
                This card has supporting text below as a natural lead-in to
                  additional content.
                </Card.Text>
              </Card.Body>
              <Card.Footer>
                <small className="text-muted">Last updated 3 mins ago</small>
              </Card.Footer>
            </Card>
          </div>
        </Carousel.Item>
      </Carousel>

    </div>
  
    </div>
    // Cards
    

  );
}

export default EventPage;

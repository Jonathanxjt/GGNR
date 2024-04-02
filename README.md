# GGNR

GGNR is a React-based platform designed for organizers to host various events such as esports tournaments or gatherings. Interested parties can use GGNR to sign up and pay for events as spectators or competitors.

## Features

- Event creation and management for organizers.
- Different roles and capacities can be set for each event.
- Users can browse available events and register based on their preferred role (audience, VIP, competitor).
- Payment processing for event tickets using Stripe.

## Getting Started

### Prerequisites

- Node.js
- Docker

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/Jonathanxjt/GGNR.git
   ```

2. Navigate to the project directory:

   ```sh
   cd ggnr
   ```

3. Install NPM packages:

   ```sh
   npm install
   ```

### Running the Application

1. Start the React application:

   ```sh
   npm start
   ```

2. Open a new terminal window and navigate to the microservices directory:

   ```sh
   cd ggnr/microservice
   ```

3. Run the microservices using Docker Compose:

   This will start all the required microservices for the application to function correctly.

   ```sh
   docker-compose up --build
   ```

   

   To stop the microservices, press `Ctrl+C` twice to exit, then run:

   ```sh
   docker-compose down
   ```


## External APIs Used

- **Internet Games Database (IGDB)**
  - [Link to documentation](https://api-docs.igdb.com/#getting-started)
  - This API was used to query games for the events on GGNR.

- **Stripe Payment**
  - [Link to documentation](https://stripe.com/docs)
  - Stripe was used to handle payment for the event tickets.

## Usage

- **For Organizers:**
  - Create and manage events.

- **For Users:**
  - Browse available events.
  - Register for events based on the preferred catagories (Audience, VIP, Competitor).

## Contact

Project Link: [https://github.com/Jonathanxjt/GGNR](https://github.com/Jonathanxjt/GGNR)

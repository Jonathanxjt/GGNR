# GGNR

GGNR is a React-based platform designed for organisers to host various events such as esports tournaments or gatherings. Interested parties can make use of GGNR to sign up and pay for events as spectators or competitors. 

## Features

## Getting Started

### Prerequisites

- Node.js
- Docker

### Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your_username_/GGNR.git
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

2. To run the microservices, use Docker Compose:

   ```sh
   cd ggnr/microservice
   docker-compose up --build
   ```

   This will start all the required microservices for the application to function correctly.

## External APIs used

- **Internet Games Database (IGDB)**
   - [Link to documentation](https://api-docs.igdb.com/#getting-started)
   - This API was used to query games for the events on GGNR. 

- **Stripe Payment**
   - [Link to documentation](https://docs.stripe.com/)
   - Stripe was used to handle payment for the event tickets. 

## Usage

- **For Organizers:**
  - Create and manage events.
  - Set different roles and capacities for each event.

- **For Users:**
  - Browse available events.
  - Register for events based on the preferred role (audience, VIP, competitor).



## Contact

Project Link: [https://github.com/Jonathanxjt/GGNR] (https://github.com/Jonathanxjt/GGNR)


# GGNR

GGNR is a React-based platform designed for organizers to host various events such as esports tournaments, gatherings.
Users can register for these events in different capacities such as audience, VIP, or competitor.

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

4. Import kong_config.yml to overwrite configuration in Kong container:

   ```sh
   docker compose up --build
   docker cp kong_config.yml microservice-kong-1:/tmp/kong_config.yml
   docker exec microservice-kong-1 kong config db_import /tmp/kong_config.yml
   docker compose down
   docker compose up --build
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

## Usage

- **For Organizers:**
  - Create and manage events.
  - Set different roles and capacities for each event.

- **For Users:**
  - Browse available events.
  - Register for events based on the preferred role (audience, VIP, competitor).



## Contact

Project Link: [https://github.com/Jonathanxjt/GGNR] (https://github.com/Jonathanxjt/GGNR)


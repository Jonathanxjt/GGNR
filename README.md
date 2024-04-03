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

## Initialising the database

   To initialise the database, run ggnr.sql in your mySQLWorkbench or equivalent

   ```sh
   |-- ggnr
   |  |-- microservice
   |  |  |-- ggnr.sql  
   ```
   The following user data can be used for testing

   ```sh
   og1@gmail.com, password #organiser account
   user1@gmail.com, password
   user2@gmail.com, password
   user3@gmail.com, password
   ```

   Change the dbURL variable within the ggnr.env file to your own root user

   ```sh
   |-- ggnr
   |  |-- microservice
   |  |  |-- ggnr.env  
   ```

## External APIs Used

- **Internet Games Database (IGDB)**
  - [Link to documentation](https://api-docs.igdb.com/#getting-started)
  - This API was used to query games for the events on GGNR.

- **Stripe Payment**
  - [Link to documentation](https://stripe.com/docs)
  - Stripe was used to handle payment for the event tickets.

- **Twilio**
   -[Link to documentation](https://www.twilio.com/docs)
   - Twilio was used to send notifications to users.

## API keys (FOR IS213 instructors)

   Attached in the project submission will be two .env files which contain our Stripe, Igdb and Twilio API keys. 
 
   microservice/.env should be placed in the following folder in the repo. 

   ```sh
   |-- ggnr
   |  |-- microservice
   |  |  |-- .env
   |  |  |-- amqp_connection.py
         #etc
   ```

   react/.env should be placed in the root folder of the repo.

   ```sh
   |-- ggnr
   |  |-- .env
   |  |-- package.json
      # etc
   ```

## Usage

- **For Organizers:**
  - Create and manage events.

- **For Users:**
  - Browse available events.
  - Register for events based on the preferred catagories (Audience, VIP, Competitor).

## Contact

Project Link: [https://github.com/Jonathanxjt/GGNR](https://github.com/Jonathanxjt/GGNR)

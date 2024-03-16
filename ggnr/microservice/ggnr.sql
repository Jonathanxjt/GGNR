DROP DATABASE IF EXISTS ggnr_database;
CREATE DATABASE ggnr_database;
USE ggnr_database;

CREATE TABLE events (
    EID INT,
    TierID SMALLINT,
    Title VARCHAR(255),
    Description TEXT,
    EventLogo TEXT,
    GameName VARCHAR(255),
    GameLogo TEXT,
    Location VARCHAR(255),
    Time DATETIME,
    GameCompany VARCHAR(255),
    Capacity INT,
    Price FLOAT,
    PRIMARY KEY (EID, TierID)
);

CREATE TABLE users (
    UID INT PRIMARY KEY,
    preferences TEXT
);

CREATE TABLE attendees (
    AID INT AUTO_INCREMENT PRIMARY KEY,
    EID INT,
    UID INT,
    ticketID INT,
    transactionID INT,
    FOREIGN KEY (EID) REFERENCES events(EID),
    FOREIGN KEY (UID) REFERENCES users(UID)
);

CREATE TABLE tickets (
    TicketID INT PRIMARY KEY,
    EID INT,
    UID INT,
    Tier TINYINT,
    Price FLOAT,
    FOREIGN KEY (EID) REFERENCES events(EID),
    FOREIGN KEY (UID) REFERENCES users(UID)
);

INSERT INTO events (EID, TierID, Title, Description, EventLogo, GameName, GameLogo, Location, Time, GameCompany, Capacity, Price)
VALUES
(1, 1, 'Event 1', 'Description for Event 1', 'event1.jpg', 'Game 1', 'game1.jpg', 'Location 1', '2024-03-17 10:00:00', 'Company 1', 100, 10.99),
(2, 1, 'Event 2', 'Description for Event 2', 'event2.jpg', 'Game 2', 'game2.jpg', 'Location 2', '2024-03-18 11:00:00', 'Company 2', 150, 15.99),
(3, 2, 'Event 3', 'Description for Event 3', 'event3.jpg', 'Game 3', 'game3.jpg', 'Location 3', '2024-03-19 12:00:00', 'Company 3', 200, 20.99);

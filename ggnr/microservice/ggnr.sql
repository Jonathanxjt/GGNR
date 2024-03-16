CREATE DATABASE ggnr_database;
USE ggnr_database;

CREATE TABLE events (
    EID INT,
    TierID SMALLINT,
    GameName VARCHAR(255),
    GameLogo VARCHAR(255),
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

INSERT INTO events (EID, TierID, GameName, GameLogo, Location, Time, GameCompany, Capacity, Price) VALUES
(1, 1, 'Super Fun Game', 'logo.png', 'Convention Center', '2024-01-01 10:00:00', 'Gaming Co', 100, 49.99);
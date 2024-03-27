DROP DATABASE IF EXISTS ggnr_database;
CREATE DATABASE ggnr_database;
USE ggnr_database;

CREATE TABLE events (
    EID INT AUTO_INCREMENT,
    Title VARCHAR(255),
    Description TEXT,
    EventLogo TEXT,
    GameName VARCHAR(255),
    GameLogo TEXT,
    Location VARCHAR(255),
    Time DATETIME,
    GameCompany VARCHAR(255),
    PRIMARY KEY (EID)
);

CREATE TABLE events_type (
    EID INT,
    TierID SMALLINT,
    Category VARCHAR(255),
    PriceID VARCHAR(255),
    Price FLOAT,
    Capacity INT,
    PRIMARY KEY (EID, TierID),
    FOREIGN KEY (EID) REFERENCES events(EID)
);

CREATE TABLE users (
    UID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    preferences TEXT,
    email VARCHAR(255) NOT NULL,
    contact VARCHAR(20) NOT NULL,
    organiser TINYINT(1),
    organiser_company VARCHAR(255)
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
    TicketID INT AUTO_INCREMENT PRIMARY KEY,
    EID INT,
    TierID SMALLINT,
    PriceID VARCHAR(255),
    FOREIGN KEY (EID) REFERENCES events(EID)
);

CREATE TABLE user_tickets (
    UID INT,
    TicketID INT,
    PRIMARY KEY (UID, TicketID),
    FOREIGN KEY (UID) REFERENCES users(UID),
    FOREIGN KEY (TicketID) REFERENCES tickets(TicketID)
);
-- Delete price ID and Tier ID, remove capacity
INSERT INTO events (EID, Title, Description, EventLogo, GameName, GameLogo, Location, Time, GameCompany)
VALUES

(1, 'Palworld Grand Tournament', "Join us for an electrifying day of competition and camaraderie at the Palworld Grand Tournament! Assemble your team of loyal pals and prepare to face off against challengers from across the realm in a series of thrilling contests. 
Whether you're a seasoned trainer or a newcomer to the world of Pal breeding and battling, this event promises excitement for all! Witness jaw-dropping battles, showcase your Pal's unique abilities, and cheer on your favorites as they strive for victory. 
With exclusive merchandise, food stalls, and interactive experiences, the Palworld Grand Tournament is an event not to be missed! Grab your tickets now and get ready to experience the thrill of Pal battling like never before!", 
'https://i.ibb.co/P1MGhsJ/palworld.png', 'Palworld', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co7n02.png', 
'Marina Bay Sands Expo and Convention Centre', '2024-05-15 12:00:00', 'PocketPair'),

(2, 'Tekken 8 World Championship', "Prepare for the ultimate showdown in the world of fighting games at the Tekken 8 World Championship! Assemble your favorite fighters, hone your skills, and compete against the best players from around the globe 
in an adrenaline-fueled tournament that will determine the next champion of the Iron Fist. Witness jaw-dropping battles, heart-stopping comebacks, and epic clashes as competitors unleash their signature moves and strategies in pursuit of glory. 
With multiple stages, live commentary, and opportunities to meet Tekken developers and gaming celebrities, the Tekken 8 World Championship promises an unforgettable experience for fans and players alike.Don't miss your chance to be part of gaming history!
Secure your tickets now and prepare to enter the fray at the Tekken 8 World Championship.",
'https://i.ibb.co/DtcXmqV/tekken8.png', 'Tekken 8', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co7lbb.png',
'Suntec Singapore Convention & Exhibition Centre', '2024-06-28 10:00:00', 'Bandai Namco Studios'),

(3, 'Helldivers 2: Galactic Invasion Rally', "Attention, brave Helldivers! Join us for the Helldivers 2: Galactic Invasion Rally, where the fate of humanity hangs in the balance against the relentless onslaught of alien forces. 
Gear up, rally your squad, and embark on a mission to defend our galaxy from the encroaching menace. Engage in intense cooperative gameplay as you drop into hostile environments, unleash devastating firepower, and coordinate strategic strikes with fellow Helldivers. 
With immersive simulations, live demonstrations, and special guest appearances from the game developers, the Galactic Invasion Rally offers an unparalleled experience for fans of the Helldivers franchise. Don't miss your chance to fight for the future of humanity! 
Secure your tickets now and enlist in the Helldivers 2: Galactic Invasion Rally. Victory awaits, Helldivers!",
'https://i.ibb.co/r4YGfMp/helldivers2.png', 'Helldivers 2', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co741o.png', 
'Singapore Expo', '2024-10-12 09:00:00', 'Arrowhead Game Studios'),

(4, 'Portal:Revolution - PortalCon 2024', "Prepare to be transported to a world of mind-bending puzzles and innovative gameplay at PortalCon 2024, the ultimate celebration of the Portal: Revolution universe! Immerse yourself in the groundbreaking technology of 
Aperture Science and embark on a journey through portals, challenges, and mysteries. Explore immersive exhibits showcasing the latest advancements in portal technology, participate in hands-on workshops led by Aperture Science engineers, and test your problem-solving skills 
in live multiplayer challenges inspired by the game. With special guest appearances, cosplay contests, and exclusive merchandise, PortalCon 2024 promises an unforgettable experience for fans of all ages. Don't miss your chance to step into the world of Portal: Revolution 
and join the revolution! Secure your tickets now and prepare for an adventure unlike any other at PortalCon 2024.",
'https://i.ibb.co/pw82rmx/portal.png', 'Portal:Revolution', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co6118.png',
'Sands Expo & Convention Centre', '2024-11-08 10:30:00', 'Second Face Software'),

(5, 'Shield Showdown: Pokémon Shield Championship', "Prepare for an epic clash of trainers and Pokémon at the Shield Showdown: Pokémon Shield Championship! Dive into the vibrant Galar region and showcase your skills in battles that will determine who reigns supreme as the ultimate Pokémon Trainer. 
Whether you're a seasoned veteran or a newcomer to the world of Pokémon, this championship promises excitement and thrills for all. Engage in intense battles using your carefully crafted teams of Pokémon, strategically selecting moves and tactics to outsmart your opponents. 
With multiple divisions catering to different skill levels, trainers of all abilities will have the chance to test their mettle and prove themselves as champions. Immerse yourself in the world of Pokémon with interactive exhibits, special guest appearances, and opportunities to meet fellow trainers and exchange tips and strategies.
With prizes, bragging rights, and the title of Pokémon Shield Champion on the line, the Shield Showdown promises an unforgettable experience for fans of the Pokémon series. Don't miss your chance to become a Pokémon Master! Secure your tickets now and join the excitement at the Shield Showdown: Pokémon Shield Championship.",
'https://i.ibb.co/YBHmSmY/pshield.png', 'Pokémon Shield', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co1zk1.png',
'OCBC Arena', '2024-07-20 14:00:00', 'Game Freak'),

(6, 'Melty Blood Act Cadenza Ver. B: Clash of Arcane Warriors', "Dive into the mesmerizing world of Tsukihime and Fate/Stay Night and join fellow magi, vampires, and heroic spirits in epic battles filled with magic, combat finesse, and supernatural abilities. Whether you're a seasoned veteran or a newcomer to the realm of Melty Blood, 
this event promises excitement, strategy, and awe-inspiring moments for all. Witness top Melty Blood players and Fate/Stay Night enthusiasts battle it out in exhilarating matches filled with fast-paced combat, intricate combos, and breathtaking special moves. From fierce one-on-one duels to epic team battles, experience the full spectrum of 
Melty Blood action as the best of the best compete for supremacy.",
'https://i.ibb.co/c3ktFyH/mblood.png', 'Melty Blood Act Cadenza Ver. B', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2wp1.png',
'Marina Bay Sands Grand Ballroom', '2024-08-11 12:30:00', 'French Bread'),

(7, 'Valorant: Champions Clash', "Prepare for an epic showdown of tactical skill and precision at the Valorant: Champions' Clash! Step into the high-stakes world of tactical shooter gaming and compete against the top teams from around the world in this thrilling tournament. Whether you're a seasoned veteran or a newcomer to the genre, 
this event promises intense action, strategic gameplay, and unforgettable moments for all. Immerse yourself in the world of Valorant with live commentary, exclusive merchandise, and opportunities to meet your favorite players and streamers. Whether you're cheering on your favorite team or experiencing the excitement firsthand, the Champions' Clash 
promises an unforgettable weekend of gaming action. Don't miss your chance to witness the intensity of Valorant esports at its finest! Secure your tickets now and prepare to experience the thrill of the Champions' Clash at the Staples Center.",
'https://i.ibb.co/1qSsR1T/val.png', 'Valorant', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2mvt.png',
'Nanyang Technological University (NTU) The Hive', '2024-10-5 11:30:00', 'Riot Games'),

(8, 'Lethal League Blaze: Smash Ball', "Gear up for a high-octane showdown like no other at the Lethal League Blaze: Smash Ball Championship! Enter the neon-lit arenas of the future and unleash your skills in intense, high-speed battles where every hit counts. Whether you're a seasoned competitor or new to the world of Lethal League Blaze, 
this event promises adrenaline-pumping action, fierce competition, and unforgettable moments for all. Watch as top Lethal League Blaze players go head-to-head in electrifying matches filled with lightning-fast reflexes, mind-bending trick shots, and gravity-defying aerial maneuvers. From intense one-on-one showdowns to chaotic free-for-alls, 
experience the full spectrum of Lethal League Blaze action as competitors vie for supremacy.",
'https://i.ibb.co/pbj0DjQ/llb.png', 'Lethal League Blaze', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2toi.png', 
'Bugis+ Atrium', '2024-07-09 09:00:00', 'Team Reptile'),

(9, 'League of Legends: World Championship Finals', "Step into the legendary Summoner's Rift and witness the world's top teams clash in epic battles for glory, fame, and the coveted title of world champion. Whether you're a die-hard fan or a newcomer to the world of League of Legends, this event promises excitement, strategy, and unforgettable moments for all. 
Watch as the best teams from across the globe compete in intense matches filled with strategic gameplay, clutch plays, and thrilling team fights. From daring solo outplays to coordinated team strategies, experience the full spectrum of League of Legends action as the world's top players showcase their skills on the grandest stage.",
'https://i.ibb.co/ZBcBSMm/lol.png', 'League of Legends', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co49wj.png', 
'SCAPE', '2024-09-24 11:00:00', 'Riot Games'),

(10, 'Granblue Fantasy Versus:Rising Gathering', "Prepare to soar to new heights in the fantastical world of Granblue Fantasy at Relink Fest: Granblue Fantasy Gathering! Embark on a thrilling adventure through the skies of the mystical realm of Skydom as you join forces with legendary heroes, uncover ancient mysteries, and battle powerful foes in this action-packed RPG experience. 
Whether you're a seasoned skyfarer or a newcomer to the world of Granblue, this event promises excitement, exploration, and camaraderie for all. Embark on epic quests across the vast and enchanting world of Skydom, where adventure awaits around every corner and the promise of treasure beckons from the depths of ancient ruins and towering citadels. Join forces with iconic characters 
from the Granblue Fantasy universe, each with their own unique abilities and personalities, as you journey to unlock the secrets of the mysterious primal beasts and restore balance to the realm.", 
'https://i.ibb.co/kH7K02w/gblue.png', 'Granblue Fantasy Versus:Rising', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co6wn2.png', 
'Suntec City Atrium', '2024-06-13 13:00:00', 'Arc System Works'),

(11, 'Fortnite: Battle Royale Royale Extravaganza', "Whether you're a seasoned player or new to the island, this event promises excitement, creativity, and non-stop action for all. Experience the thrill of Battle Royale in epic tournaments and challenges, as players compete for victory royale and exclusive prizes. Whether you prefer solo showdowns, duo duels, 
or squad skirmishes, there's something for everyone to enjoy in the world of Fortnite. Unleash your creativity in the Creative Zone, where you can design your own custom islands, build towering structures, and craft intricate worlds with friends and fellow players. Show off your creations, explore unique creations from the community, and discover new ways to express 
yourself in the Fortnite universe.", 
'https://i.ibb.co/VLB3xff/fn.png', 'Fortnite', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co2ekt.png', 
'Orchard Central', '2024-05-02 09:00:00', 'Epic Games'),

(12, 'Street Fighter 6: World Championship Showdown', "Get ready for an electrifying clash of fighters and champions at the Street Fighter IV: World Championship Showdown! Enter the iconic world of Street Fighter and immerse yourself in heart-pounding battles, lightning-fast combos, and fierce competition that have defined this legendary fighting game franchise. 
Whether you're a seasoned veteran or a newcomer to the world of Street Fighter, this event promises excitement, skill, and adrenaline-fueled action for all. Witness the world's best Street Fighter players face off in intense battles of skill and strategy as they execute precise combos, unleash devastating special moves, and outmaneuver their opponents in epic showdowns. 
From classic characters like Ryu and Chun-Li to newcomers like Seth and C. Viper, experience the thrill of seeing your favorite fighters in action on the big stage.",
'https://i.ibb.co/9hMxg1v/street6.png', 'Street Fighter IV', 'https://images.igdb.com/igdb/image/upload/t_cover_big/co5vst.png', 
'Downtown East', '2024-11-19 10:00:00', 'Capcom');

INSERT INTO users (username, password_hash, preferences, email, contact, organiser, organiser_company)
VALUES
('john_doe', 'password_hash_1', '"preference1", "preference2"', 'john.doe@example.com', '1234567890', 1, 'Company A'),
('jane_smith', 'password_hash_2', '"preference1", "preference2"', 'jane.smith@example.com', '0987654321', 0, NULL),
('sam_jackson', 'password_hash_3', '"preference1", "preference2"', 'sam.jackson@example.com', '9876543210', 1, 'Company B'),
('sarah_connor', 'password_hash_4', '"preference1", "preference2"', 'sarah.connor@example.com', '0123456789', 0, NULL);

INSERT INTO attendees (EID, UID, ticketID, transactionID)
VALUES
(1, 1, 1, 123),
(1, 2, 2, 124),
(2, 3, 3, 125),
(2, 4, 4, 126);

INSERT INTO tickets (EID, TierID, PriceID)
VALUES
(1, 1, 'price_1OxkTz2LfOffQtXe2Amrcy0e'),
(1, 2, 'price_1OxkUn2LfOffQtXeGLBwfvyu'),
(2, 1, 'price_1OxkTz2LfOffQtXe2Amrcy0e'),
(2, 2, 'price_1OxkUn2LfOffQtXeGLBwfvyu');

INSERT INTO user_tickets (UID, TicketID)
VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);

INSERT INTO events_type (EID, TierID, Category, PriceID, Price, Capacity)
VALUES
(1, 1, 'Audience', NULL, 0, 2000),
(1, 2, 'VIP', 'price_1OxkTz2LfOffQtXe2Amrcy0e', 10.00, 12000),
(1, 3, 'Competitor', 'price_1OxkUn2LfOffQtXeGLBwfvyu', 15.00, 50),
(2, 1, 'Audience', NULL, 0, 2000),
(2, 2, 'VIP', 'price_1OxkTz2LfOffQtXe2Amrcy0e', 10.00, 10000),
(2, 3, 'Competitor', 'price_1OxkUn2LfOffQtXeGLBwfvyu', 15.00, 50),
(3, 1, 'Audience', NULL, 0, 1000),
(3, 2, 'VIP', 'price_1OxkTz2LfOffQtXe2Amrcy0e', 10.00, 8000),
(3, 3, 'Competitor', 'price_1OxkUn2LfOffQtXeGLBwfvyu', 15.00, 60),
(4, 1, 'Audience', NULL, 0, 8000),
(5, 1, 'Audience', NULL, 0, 500),
(5, 2, 'VIP', 'price_1OxkTz2LfOffQtXe2Amrcy0e', 10.00, 2500),
(5, 3, 'Competitor', 'price_1OxkUn2LfOffQtXeGLBwfvyu', 15.00, 50),
(6, 1, 'Audience', NULL, 0, 200),
(6, 2, 'VIP', 'price_1OxkTz2LfOffQtXe2Amrcy0e', 10.00, 1000),
(6, 3, 'Competitor', 'price_1OxkUn2LfOffQtXeGLBwfvyu', 15.00, 50),
(7, 1, 'Audience', NULL, 0, 500),
(7, 2, 'VIP', 'price_1OxkTz2LfOffQtXe2Amrcy0e', 10.00, 2000),
(7, 3, 'Competitor', 'price_1OxkUn2LfOffQtXeGLBwfvyu', 15.00, 60),
(8, 1, 'Audience', NULL, 0, 500),
(9, 1, 'Audience', NULL, 0, 1000),
(9, 2, 'VIP', 'price_1OxkTz2LfOffQtXe2Amrcy0e', 10.00, 13000),
(9, 3, 'Competitor', 'price_1OxkUn2LfOffQtXeGLBwfvyu', 15.00, 60),
(10, 1, 'Audience', NULL, 0, 1000),
(10, 2, 'VIP', 'price_1OxkTz2LfOffQtXe2Amrcy0e', 10.00, 13000),
(10, 3, 'Competitor', 'price_1OxkUn2LfOffQtXeGLBwfvyu', 15.00, 60),
(11, 1, 'Audience', NULL, 0, 1000),
(11, 2, 'VIP', 'price_1OxkTz2LfOffQtXe2Amrcy0e', 10.00, 5000),
(11, 3, 'Competitor', 'price_1OxkUn2LfOffQtXeGLBwfvyu', 15.00, 60),
(12, 1, 'Audience', NULL, 0, 500),
(12, 2, 'VIP', 'price_1OxkTz2LfOffQtXe2Amrcy0e', 10.00, 5500),
(12, 3, 'Competitor', 'price_1OxkUn2LfOffQtXeGLBwfvyu', 15.00, 30);
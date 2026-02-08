/*******************
Create the schema
********************/

------------------------------------------------------
-- Countries
------------------------------------------------------

CREATE TABLE IF NOT EXISTS countries (
 name VARCHAR(64),
 subregion VARCHAR(64),
 region VARCHAR(64),
 PRIMARY KEY (name)
);


------------------------------------------------------
-- Seasons
------------------------------------------------------

CREATE TABLE IF NOT EXISTS seasons (
 year INTEGER PRIMARY KEY,
 url VARCHAR (255) NOT NULL
);


------------------------------------------------------
-- Circuits
------------------------------------------------------

CREATE TABLE IF NOT EXISTS circuits (
 name VARCHAR(64),
 location VARCHAR(64) NOT NULL,
 country VARCHAR(64) NOT NULL,
 lat NUMERIC NOT NULL CHECK (lat BETWEEN -90 AND 90),
 lng NUMERIC NOT NULL CHECK (lng BETWEEN -180 AND 180),
 alt INTEGER NOT NULL,
 url VARCHAR (255) NOT NULL,
 PRIMARY KEY (name),
 CONSTRAINT fk_country FOREIGN KEY (country) REFERENCES countries (name) DEFERRABLE
);


------------------------------------------------------
-- Drivers
------------------------------------------------------

CREATE TABLE IF NOT EXISTS drivers (
 forename VARCHAR(32),
 surname VARCHAR(32),
 code CHAR(3),
 number INTEGER,
 dob DATE NOT NULL,
 country VARCHAR(64) NOT NULL,
 url VARCHAR (255) NOT NULL,
 PRIMARY KEY (forename, surname),
 CONSTRAINT fk_country FOREIGN KEY (country) REFERENCES countries (name) DEFERRABLE
);


------------------------------------------------------
-- Constructors
------------------------------------------------------

CREATE TABLE IF NOT EXISTS constructors (
 name VARCHAR(64),
 country VARCHAR(64) NOT NULL,
 url VARCHAR (255) NOT NULL,
 PRIMARY KEY (name),
 CONSTRAINT fk_country FOREIGN KEY (country) REFERENCES countries (name) DEFERRABLE
);


------------------------------------------------------
-- Statuses
------------------------------------------------------

CREATE TABLE IF NOT EXISTS statuses (
 id INTEGER PRIMARY KEY,
 text VARCHAR(64) NOT NULL
);


------------------------------------------------------
-- Races
------------------------------------------------------

CREATE TABLE IF NOT EXISTS races (
 date DATE PRIMARY KEY,
 season INTEGER NOT NULL,
 name VARCHAR(64) NOT NULL,
 circuit VARCHAR(64) NOT NULL,
 url VARCHAR (255) NOT NULL,
 CONSTRAINT fk_season FOREIGN KEY (season) REFERENCES seasons (year) DEFERRABLE,
 CONSTRAINT fk_circuit FOREIGN KEY (circuit) REFERENCES circuits (name) DEFERRABLE
);


------------------------------------------------------
-- Results
------------------------------------------------------

CREATE TABLE IF NOT EXISTS results (
 race DATE,
 driver_forename VARCHAR(32),
 driver_surname VARCHAR(32),
 constructor VARCHAR(64),
 number INTEGER,
 position INTEGER,
 position_text CHAR(3),
 position_order INTEGER NOT NULL,
 points NUMERIC NOT NULL,
 laps INTEGER NOT NULL,
 time INTEGER,
 fastest_lap INTEGER,
 fastest_lap_time INTEGER,
 fastest_lap_speed NUMERIC,
 status INTEGER NOT NULL,
 PRIMARY KEY (race, driver_forename, driver_surname),
 CONSTRAINT fk_race FOREIGN KEY (race) REFERENCES races (date) DEFERRABLE,
 CONSTRAINT fk_driver FOREIGN KEY (driver_forename, driver_surname) REFERENCES drivers (forename, surname) DEFERRABLE,
 CONSTRAINT fk_constructor FOREIGN KEY (constructor) REFERENCES constructors (name) DEFERRABLE,
 CONSTRAINT fk_status FOREIGN KEY (status) REFERENCES statuses (id) DEFERRABLE
);


------------------------------------------------------
-- Constructor Results
------------------------------------------------------

CREATE TABLE IF NOT EXISTS constructor_results (
 race DATE,
 constructor VARCHAR(64),
 points NUMERIC NOT NULL,
 PRIMARY KEY (race, constructor),
 CONSTRAINT fk_race FOREIGN KEY (race) REFERENCES races (date) DEFERRABLE,
 CONSTRAINT fk_constructor FOREIGN KEY (constructor) REFERENCES constructors (name) DEFERRABLE
);


------------------------------------------------------
-- Pit Stops
------------------------------------------------------

CREATE TABLE IF NOT EXISTS pit_stops (
 race DATE,
 driver_forename VARCHAR(32),
 driver_surname VARCHAR(32),
 lap INTEGER NOT NULL,
 duration INTEGER NOT NULL,
 PRIMARY KEY (race, driver_forename, driver_surname, lap),
 CONSTRAINT fk_race FOREIGN KEY (race) REFERENCES races (date) DEFERRABLE,
 CONSTRAINT fk_driver FOREIGN KEY (driver_forename, driver_surname) REFERENCES drivers (forename, surname) DEFERRABLE
);


------------------------------------------------------
-- Qualifyings
------------------------------------------------------

CREATE TABLE IF NOT EXISTS qualifyings (
 race DATE,
 driver_forename VARCHAR(32),
 driver_surname VARCHAR(32),
 number INTEGER NOT NULL,
 constructor VARCHAR(64) NOT NULL,
 position INTEGER NOT NULL,
 q1 INTEGER,
 q2 INTEGER,
 q3 INTEGER,
 PRIMARY KEY (race, driver_forename, driver_surname),
 CONSTRAINT fk_race FOREIGN KEY (race) REFERENCES races (date) DEFERRABLE,
 CONSTRAINT fk_driver FOREIGN KEY (driver_forename, driver_surname) REFERENCES drivers (forename, surname) DEFERRABLE,
 CONSTRAINT fk_constructor FOREIGN KEY (constructor) REFERENCES constructors (name) DEFERRABLE
);


------------------------------------------------------
-- Sprint Results
------------------------------------------------------

CREATE TABLE IF NOT EXISTS sprint_results (
 race DATE,
 driver_forename VARCHAR(32),
 driver_surname VARCHAR(32),
 number INTEGER NOT NULL,
 constructor VARCHAR(64) NOT NULL,
 position INTEGER,
 position_text CHAR(3),
 position_order INTEGER NOT NULL,
 points NUMERIC NOT NULL,
 laps INTEGER NOT NULL,
 time INTEGER,
 fastest_lap INTEGER,
 fastest_lap_time INTEGER,
 status INTEGER NOT NULL,
 PRIMARY KEY (race, driver_forename, driver_surname),
 CONSTRAINT fk_race FOREIGN KEY (race) REFERENCES races (date) DEFERRABLE,
 CONSTRAINT fk_driver FOREIGN KEY (driver_forename, driver_surname) REFERENCES drivers (forename, surname) DEFERRABLE,
 CONSTRAINT fk_constructor FOREIGN KEY (constructor) REFERENCES constructors (name) DEFERRABLE,
 CONSTRAINT fk_status FOREIGN KEY (status) REFERENCES statuses (id) DEFERRABLE
);

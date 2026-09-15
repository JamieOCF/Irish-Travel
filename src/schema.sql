PRAGMA foreign_keys = ON;

-- =====================================================================
-- USERS
-- =====================================================================
CREATE TABLE users
(
  user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
  username      VARCHAR(50) NOT NULL UNIQUE,
  password      TEXT NOT NULL,
  access_level  INTEGER NOT NULL CHECK (access_level IN (0, 1)),

  CHECK (length(username) > 0)
);


-- =====================================================================
-- DESTINATIONS
-- =====================================================================
CREATE TABLE destinations
(
  city_id         INTEGER PRIMARY KEY AUTOINCREMENT,
  city_name       VARCHAR(50) NOT NULL,
  country         VARCHAR(50) NOT NULL,
  rating          DECIMAL(2,1) NOT NULL DEFAULT 0 CHECK (rating BETWEEN 0 AND 5),
  ratings         INTEGER NOT NULL DEFAULT 0
);


-- =====================================================================
-- LOOKUP TABLES
-- =====================================================================
CREATE TABLE room_types
(
  room_type_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  type            VARCHAR(10) UNIQUE NOT NULL,
  label           VARCHAR(50) NOT NULL,
  max_occupancy   INTEGER NOT NULL
);

CREATE TABLE fare_classes
(
  fare_class_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  class            VARCHAR(10) UNIQUE NOT NULL,
  label            VARCHAR(50) NOT NULL
);


-- =====================================================================
-- COMPANIES
-- =====================================================================
CREATE TABLE companies
(
  company_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  company_name    VARCHAR(50) UNIQUE NOT NULL,
  transport_mode  VARCHAR(50) NOT NULL,
  rating          DECIMAL(2,1) DEFAULT 0 NOT NULL CHECK (rating BETWEEN 0 AND 5),
  ratings         INTEGER NOT NULL DEFAULT 0
);


-- =====================================================================
-- HOTELS
-- =====================================================================
CREATE TABLE hotels
(
  hotel_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  hotel_name  VARCHAR(50) NOT NULL,
  rating      DECIMAL(2,1) NOT NULL DEFAULT 0 CHECK (rating BETWEEN 0 AND 5),
  ratings     INTEGER NOT NULL DEFAULT 0,
  city_id     INTEGER NOT NULL,

  FOREIGN KEY (city_id) REFERENCES destinations(city_id)
    ON DELETE RESTRICT
);

CREATE TABLE hotel_inventory
(
  hotel_id      INTEGER NOT NULL,
  room_type_id  INTEGER NOT NULL,
  price         INTEGER NOT NULL,
  available     INTEGER NOT NULL CHECK (available >= 0),

  PRIMARY KEY (hotel_id, room_type_id),
  FOREIGN KEY (hotel_id)     REFERENCES hotels(hotel_id)         ON DELETE CASCADE,
  FOREIGN KEY (room_type_id) REFERENCES room_types(room_type_id) ON DELETE RESTRICT
);

CREATE INDEX idx_hotel_inventory_hotel ON hotel_inventory(hotel_id);


-- =====================================================================
-- ROUTES  (point 2: company_id fixed to INTEGER; point 3: from/to are direct
-- FKs replacing goes_to_and_from and operates junctions)
-- =====================================================================
CREATE TABLE routes
(
  route_id      INTEGER PRIMARY KEY AUTOINCREMENT,
  from_city_id  INTEGER NOT NULL,
  to_city_id    INTEGER NOT NULL,
  duration      INTEGER NOT NULL,
  dep_time      VARCHAR(50) NOT NULL,
  company_id    INTEGER NOT NULL,

  FOREIGN KEY (from_city_id) REFERENCES destinations(city_id) ON DELETE RESTRICT,
  FOREIGN KEY (to_city_id)   REFERENCES destinations(city_id) ON DELETE RESTRICT,
  FOREIGN KEY (company_id)   REFERENCES companies(company_id) ON DELETE RESTRICT,

  CHECK (from_city_id <> to_city_id)
);

-- Replaces routes.price_eco/price_bus/price_fc/available_eco/available_bus/available_fc columns
CREATE TABLE route_inventory
(
  route_id       INTEGER NOT NULL,
  fare_class_id  INTEGER NOT NULL,
  price          INTEGER NOT NULL,
  available      INTEGER NOT NULL CHECK (available >= 0),

  PRIMARY KEY (route_id, fare_class_id),
  FOREIGN KEY (route_id)      REFERENCES routes(route_id)             ON DELETE CASCADE,
  FOREIGN KEY (fare_class_id) REFERENCES fare_classes(fare_class_id)  ON DELETE RESTRICT
);

CREATE INDEX idx_route_inventory_route ON route_inventory(route_id);
CREATE INDEX idx_routes_from ON routes(from_city_id);
CREATE INDEX idx_routes_to ON routes(to_city_id);


-- =====================================================================
-- TRIPS
-- Groups one or more bookings (transport and/or hotel) made together in
-- the same checkout. Optional — a standalone booking just leaves its
-- trip_id NULL.
-- =====================================================================
CREATE TABLE trips
(
  trip_id  INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id  INTEGER NOT NULL,

  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);


-- =====================================================================
-- TRANSPORT BOOKINGS
-- =====================================================================
CREATE TABLE transport_bookings
(
  transport_booking_num  INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id                INTEGER NOT NULL,
  route_id               INTEGER NOT NULL,
  dep_date               VARCHAR(50) NOT NULL,
  total_cost             INTEGER NOT NULL,
  trip_id                INTEGER,

  FOREIGN KEY (user_id)  REFERENCES users(user_id)   ON DELETE RESTRICT,
  FOREIGN KEY (route_id) REFERENCES routes(route_id) ON DELETE RESTRICT,
  FOREIGN KEY (trip_id)  REFERENCES trips(trip_id)    ON DELETE SET NULL
);

CREATE TABLE transport_booking_items
(
  transport_booking_num  INTEGER NOT NULL,
  fare_class_id          INTEGER NOT NULL,
  quantity                INTEGER NOT NULL CHECK (quantity > 0),
  price_at_booking        INTEGER NOT NULL,

  PRIMARY KEY (transport_booking_num, fare_class_id),
  FOREIGN KEY (transport_booking_num) REFERENCES transport_bookings(transport_booking_num) ON DELETE CASCADE,
  FOREIGN KEY (fare_class_id)         REFERENCES fare_classes(fare_class_id)               ON DELETE RESTRICT
);

CREATE INDEX idx_transport_bookings_user ON transport_bookings(user_id);
CREATE INDEX idx_transport_bookings_route ON transport_bookings(route_id);
CREATE INDEX idx_transport_bookings_trip ON transport_bookings(trip_id);


-- =====================================================================
-- HOTEL BOOKINGS
-- =====================================================================
CREATE TABLE hotel_bookings
(
  hotel_booking_num  INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id            INTEGER NOT NULL,
  hotel_id           INTEGER NOT NULL,
  arr_date           VARCHAR(50) NOT NULL,
  dep_date           VARCHAR(50) NOT NULL,
  total_cost         INTEGER NOT NULL,
  trip_id            INTEGER,

  FOREIGN KEY (user_id)  REFERENCES users(user_id)   ON DELETE RESTRICT,
  FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id) ON DELETE RESTRICT,
  FOREIGN KEY (trip_id)  REFERENCES trips(trip_id)   ON DELETE SET NULL
);

CREATE TABLE hotel_booking_items
(
  hotel_booking_num  INTEGER NOT NULL,
  room_type_id       INTEGER NOT NULL,
  quantity           INTEGER NOT NULL CHECK (quantity > 0),
  price_at_booking   INTEGER NOT NULL,

  PRIMARY KEY (hotel_booking_num, room_type_id),
  FOREIGN KEY (hotel_booking_num) REFERENCES hotel_bookings(hotel_booking_num) ON DELETE CASCADE,
  FOREIGN KEY (room_type_id)      REFERENCES room_types(room_type_id)         ON DELETE RESTRICT
);

CREATE INDEX idx_hotel_bookings_user ON hotel_bookings(user_id);
CREATE INDEX idx_hotel_bookings_hotel ON hotel_bookings(hotel_id);
CREATE INDEX idx_hotel_bookings_trip ON hotel_bookings(trip_id);


-- =====================================================================
-- FLIES TO AND FROM
-- =====================================================================
CREATE TABLE flies_to_and_from
(
  company_id  INTEGER NOT NULL,
  city_id     INTEGER NOT NULL,

  PRIMARY KEY (company_id, city_id),
  FOREIGN KEY (company_id) REFERENCES companies(company_id)   ON DELETE CASCADE,
  FOREIGN KEY (city_id)    REFERENCES destinations(city_id)   ON DELETE CASCADE
);


-- =====================================================================
-- DREAMS ABOUT (users <--> destinations)
-- =====================================================================
CREATE TABLE dreams_about
(
  user_id  INTEGER NOT NULL,
  city_id  INTEGER NOT NULL,

  PRIMARY KEY (user_id, city_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)         ON DELETE CASCADE,
  FOREIGN KEY (city_id) REFERENCES destinations(city_id)  ON DELETE CASCADE
);


-- =====================================================================
-- FEEDBACK
-- =====================================================================
CREATE TABLE reviews
(
  review_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id VARCHAR(50) NOT NULL,
  trip_id INTEGER NOT NULL,
  rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
  review TEXT NOT NULL,

  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT,
  FOREIGN KEY (trip_id) REFERENCES trips(trip_id) ON DELETE CASCADE
);

CREATE TABLE reports
(
  report_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id VARCHAR(50) NOT NULL,
  report TEXT NOT NULL,

  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE RESTRICT
);
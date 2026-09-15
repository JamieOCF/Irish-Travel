--users: user_id PK, password, is_admin(0/1)
--hotels: hotel_id PK AI, rating, prices/availability[2s, 3s, 1d, 2d, 1d1s]
--destinations: city_id PK AI, city_name, country, image_link
--routes: route_id PK AI, to, from, duration, dep_time, prices/availability[eco, bus, fc]
--airlines: airline_id PK AI, airline_name, airline_rating


--flight_bookings: user_id{users}, route_id{flights}, flight_booking_num PK AI, dep_date, dep_time, arr_time, num_eco, num_bus, num_fc, cost
--hotel_bookings: user_id{users}, hotel_id{flights}, hotel_booking_num PK AI, arr_date, dep_date, num_2s, num_3s, num_1d, num_2d, num_1d1s, cost
--is_located_in: hotelid{hotels}, city_id{destinations}
--goes_to_and_from: route_id{routes}, city_id{destinations}
--flies_to_and_from: airline_id{airlines}, city_id{destinations}
--operates: route_id{routes}, airline_id{airlines}

--dreams_about: user_id{users}, city_id{destinations}


--users: user_id PK, password, is_admin(0/1)
DROP TABLE IF EXISTS users;

CREATE TABLE users
(
  user_id TEXT PRIMARY KEY,
  password TEXT NOT NULL,
  is_admin INTEGER NOT NULL
);



--hotels: hotel_id PK AI, hotel_name, rating, prices/availability[2s, 3s, 1d, 2d, 1d1s]
-- DROP TABLE IF EXISTS hotels;

CREATE TABLE hotels
(
  hotel_id INTEGER PRIMARY KEY AUTOINCREMENT,
  hotel_name TEXT NOT NULL, 

  rating INTEGER NOT NULL,
  price_2s INTEGER NOT NULL,
  price_3s INTEGER NOT NULL,
  price_1d INTEGER NOT NULL,
  price_2d INTEGER NOT NULL,
  price_1d1s INTEGER NOT NULL,

  available_2s INTEGER NOT NULL,
  available_3s INTEGER NOT NULL,
  available_1d INTEGER NOT NULL,
  available_2d INTEGER NOT NULL,
  available_1d1s INTEGER NOT NULL
);




--destinations: city_id PK AI, city_name, country, image_link
-- DROP TABLE IF EXISTS destinations;

CREATE TABLE destinations
(
  city_id INTEGER PRIMARY KEY AUTOINCREMENT,
  city_name TEXT NOT NULL, 
  country TEXT NOT NULL,
  image_link NOT NULL
);




--routes: route_id PK AI, to, from, duration, prices/availability[eco, bus, fc]
-- DROP TABLE IF EXISTS routes;

CREATE TABLE routes
(
  route_id INTEGER PRIMARY KEY AUTOINCREMENT,
  from_city TEXT NOT NULL,
  to_city TEXT NOT NULL,
  duration INTEGER NOT NULL,
  airline_name TEXT NOT NULL,

  price_eco INTEGER NOT NULL,
  price_bus INTEGER NOT NULL,
  price_fc INTEGER NOT NULL,

  available_eco INTEGER NOT NULL,
  available_bus INTEGER NOT NULL,
  available_fc INTEGER NOT NULL,

  FOREIGN KEY (airline_name) REFERENCES airlines(airline_name)
);

-- DELETE FROM goes_to_and_from;
-- DELETE FROM flies_to_and_from;
-- DELETE FROM operates;




--airlines: airline_id PK AI, airline_name, airline_rating
-- DROP TABLE IF EXISTS airlines;

CREATE TABLE airlines
(
  airline_id INTEGER PRIMARY KEY AUTOINCREMENT,
  airline_name TEXT UNIQUE NOT NULL,
  airline_rating INTEGER NOT NULL
);








--flight_bookings: user_id{users}, route_id{flights}, flight_booking_num PK AI, dep_date, num_eco, num_bus, num_fc, cost
-- DROP TABLE IF EXISTS flight_bookings;

CREATE TABLE flight_bookings
(
  flight_booking_num INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT NOT NULL,
  route_id INTEGER NOT NULL,
  dep_date TEXT NOT NULL,

  num_eco_tix INTEGER NOT NULL,
  num_bus_tix INTEGER NOT NULL,
  num_fc_tix INTEGER NOT NULL,

  flight_cost INTEGER NOT NULL,

  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (route_id) REFERENCES routes(route_id)
);



--hotel_bookings: user_id{users}, hotel_id{flights}, hotel_booking_num PK AI, arr_date, dep_date, num_2s, num_3s, num_1d, num_2d, num_1d1s, cost
-- DROP TABLE IF EXISTS hotel_bookings;

CREATE TABLE hotel_bookings
(
  hotel_booking_num INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT NOT NULL,
  hotel_id INTEGER NOT NULL,
  arr_date TEXT NOT NULL,
  dep_date TEXT NOT NULL,
  
  num_2s_rooms INTEGER NOT NULL,
  num_3s_rooms INTEGER NOT NULL,
  num_1d_rooms INTEGER NOT NULL,
  num_2d_rooms INTEGER NOT NULL,
  num_1d1s_rooms INTEGER NOT NULL,

  hotel_cost INTEGER NOT NULL,

  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id)
);



--is_located_in: hotel_id{hotels}, city_id{destinations}
-- DROP TABLE IF EXISTS is_located_in;

CREATE TABLE is_located_in
(
  hotel_id INTEGER NOT NULL,
  city_id INTEGER NOT NULL,

  FOREIGN KEY (hotel_id) REFERENCES hotels(hotel_id),
  FOREIGN KEY (city_id) REFERENCES destinations(city_id)
);




--goes_to_and_from: route_id{routes}, city_id{destinations}
-- DROP TABLE IF EXISTS goes_to_and_from;

CREATE TABLE goes_to_and_from
(
  route_id INTEGER NOT NULL,
  city_id INTEGER NOT NULL,

  FOREIGN KEY (route_id) REFERENCES routes(route_id),
  FOREIGN KEY (city_id) REFERENCES destinations(city_id)
);




--flies_to_and_from: airline_id{airlines}, city_id{destinations}
-- DROP TABLE IF EXISTS flies_to_and_from;

CREATE TABLE flies_to_and_from
(
  airline_id INTEGER NOT NULL,
  city_id INTEGER NOT NULL,

  FOREIGN KEY (airline_id) REFERENCES airlines(airline_id),
  FOREIGN KEY (city_id) REFERENCES destinations(city_id)
);



--operates: route_id{routes}, airline_id{airlines}
-- DROP TABLE IF EXISTS operates;

CREATE TABLE operates
(
  airline_id INTEGER NOT NULL,
  route_id INTEGER NOT NULL,

  FOREIGN KEY (airline_id) REFERENCES airlines(airline_id),
  FOREIGN KEY (route_id) REFERENCES routes(route_id)
);








--dreams_about: user_id{users}, city_id{destinations}
-- DROP TABLE IF EXISTS dreams_about;

CREATE TABLE dreams_about
(
  user_id TEXT NOT NULL,
  city_id INTEGER NOT NULL,

  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (city_id) REFERENCES destinations(city_id)
);





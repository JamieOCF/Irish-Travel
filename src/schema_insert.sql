-- UPDATE users SET is_admin = 1 WHERE user_id = 'poopzya';
SELECT * FROM hotels;
SELECT * FROM destinations;

-- DELETE FROM is_located_in WHERE hotel_id = ;
SELECT * FROM is_located_in;

-- DELETE FROM hotel_bookings;
-- DELETE FROM flight_bookings;
SELECT * FROM hotel_bookings;
SELECT * FROM flight_bookings;

SELECT * FROM flight_bookings AS fb JOIN hotel_bookings AS hb JOIN routes AS r JOIN hotels AS h
    ON fb.user_id = hb.user_id 
    AND fb.flight_booking_num = hb.hotel_booking_num
    AND fb.route_id = r.route_id
    AND hb.hotel_id = h.hotel_id
WHERE fb.user_id = 'useradmin';

-- DELETE FROM routes WHERE from_city = 'Dublin';
-- UPDATE routes SET available_eco = 3, available_bus = 3, available_fc = 0 WHERE route_id = 4;
SELECT * FROM routes;
SELECT * FROM operates;
SELECT * FROM airlines;

SELECT * FROM users;

-- DELETE FROM users;

-- UPDATE operates SET airline_id = 11 WHERE route_id = 44;

-- DELETE FROM airlines WHERE airline_id IN (9);
SELECT * FROM airlines;

SELECT airline_name, COUNT(*) FROM routes
GROUP BY airline_name
ORDER BY COUNT(*) DESC;

SELECT * FROM routes AS r JOIN operates AS op JOIN airlines AS a
    ON r.route_id = op.route_id AND op.airline_id = a.airline_id
WHERE r.route_id in (SELECT DISTINCT route_id FROM routes;)
ORDER BY r.from_city;

SELECT * FROM routes AS r JOIN airlines AS a
WHERE r.from_city = 'Dublin' AND r.to_city = 'London' AND a.airline_name = 'Air Bingus';

SELECT * FROM hotels AS h JOIN is_located_in AS isi JOIN destinations AS d
    ON h.hotel_id = isi.hotel_id AND isi.city_id = d.city_id
WHERE d.city_name = (SELECT d.city_name FROM hotels AS h JOIN is_located_in AS isi JOIN destinations AS d
                        ON h.hotel_id = isi.hotel_id AND isi.city_id = d.city_id
                    WHERE h.hotel_id = 3);


-- INSERT INTO hotels (hotel_name, rating, price_2s, price_3s, price_1d, price_2d, price_1d1s, available_2s, available_3s, available_1d, available_2d, available_1d1s)
-- VALUES
-- ('The London',            3,    75,90,80,100,95,        4,3,4,4,5),
-- ('HotelPro London',       4,    80,90,85,100,95,        4,3,2,5,4),
-- ('Brighton Bay Hotel',    3,    60,70,66,74,72,         3,2,5,4,2),
-- ('Manchester Motel',      2,    40,45,55,60,48,         4,1,2,3,1),
-- ('Hotel Paris',           5,    150,170,160,180,175,    2,2,3,1,2),
-- ('HotelPro Paris',        4,    80,90,85,100,95,        3,4,4,3,1),
-- ('Alps View Nice',        4,    80,85,83,94,90,         2,3,1,4,5),
-- ('Meilleure Monaco',      5,    200,225,210,230,220,    3,4,5,5,4),
-- ('Malaga Hotel',          3,    67,73,70,80,75,         4,3,2,1,4),
-- ('Resort of Barcelona',   4,    100,107,105,115,110,    2,3,4,5,3),
-- ('Madrid Seasons Hotel',  4,    105,110,110,120,115,    4,1,2,3,4),
-- ('HotelPro Madrid',       4,    80,90,85,100,95,        2,3,1,2,4),
-- ('Istanbul Hotel',        3,    68,74,70,79,75,         3,4,4,5,4),
-- ('HotelPro Ankara',       4,    80,90,85,100,95,        4,5,3,4,3),
-- ('Hotel of Athens',       3,    72,75,75,80,77,         5,1,2,4,3),
-- ('Thessaloniki Hotel',    3,    57,63,60,70,65,         5,4,3,1,3),
-- ('Alps View Verona',      4,    80,85,83,94,90,         1,4,3,5,4),
-- ('The Roman Spa & Hotel', 5,    130,140,135,150,145,    3,5,4,5,3),
-- ('HotelPro Rome',         4,    80,90,85,100,95,        2,4,3,5,4),
-- ('The View of Venice',    3,    70,80,80,85,75,         4,4,5,3,4),
-- ('The Palace of Porto',   5,    220,235,230,250,240,    2,1,1,2,3),
-- ('HotelPro Porto',        4,    80,90,85,100,95,        3,3,4,4,5),
-- ('Lisbon Hotel Resort',   4,    110,120,110,125,115,    3,4,2,4,3),
-- ('Alps View Munich',      4,    80,85,83,94,90,         5,2,1,2,3),
-- ('HotelPro Munich',       4,    80,90,85,100,95,        1,2,3,3,4),
-- ('HotelPro Dortmund',     3,    75,85,80,95,90,         3,4,1,2,5),
-- ('HotelPro Berlin',       4,    80,90,85,100,95,        1,4,4,2,3),
-- ('Berlin Hotel',          5,    100,110,105,120,115,    4,1,4,5,2),
-- ('Hotel Amsterdam',       4,    95,100,95,110,105,      5,4,1,2,3),
-- ('The Red Hotel',         3,    50,55,65,70,60,         2,4,1,3,2),
-- ('Rotterdam Spa & Hotel', 5,    140,150,150,160,155,    4,2,3,4,5),
-- ('HotelPro Lurenberg',    4,    80,90,85,100,95,        5,1,3,4,3)
-- ;


-- INSERT INTO destinations (city_name, country, image_link)
-- VALUES
-- ('London',      'England',      ''),
-- ('Brighton',    'England',      ''),
-- ('Manchester',  'England',      ''),
-- ('Paris',       'France',       'paris.jpg'),
-- ('Nice',        'France',       ''),
-- ('Monte-Carlo', 'Monaco',       ''),
-- ('Malaga',      'Spain',        ''),
-- ('Barcelona',   'Spain',        ''),
-- ('Madrid',      'Spain',        'madrid.jpg'),
-- ('Istanbul',    'Turkiye',      ''),
-- ('Ankara',      'Turkiye',      ''),
-- ('Athens',      'Greece',       ''),
-- ('Thessaloniki','Greece',       ''),
-- ('Verona',      'Italy',        ''),
-- ('Rome',        'Italy',        ''),
-- ('Venice',      'Italy',        ''),
-- ('Porto',       'Portugal',     'porto.jpg'),
-- ('Lisbon',      'Portugal',     ''),
-- ('Munich',      'Germany',      ''),
-- ('Dortmund',    'Germany',      ''),
-- ('Berlin',      'Germany',      ''),
-- ('Amsterdam',   'Netherlands',  ''),
-- ('Rotterdam',   'Netherlands',  ''),
-- ('Lurenberg',   'Listenbourg',  '')
-- ;


-- INSERT INTO routes (from_city, to_city, duration, price_eco, price_bus, price_fc, available_eco, available_bus, available_fc)
-- VALUES     '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','',''),
-- ('','',     '',     '','','',       '','','')
-- ;

-- INSERT INTO airlines (airline_name, airline_rating)
-- VALUES
-- ('Air Bingus',          10),
-- ('Interval Airlines',   8),
-- ('Divided Airlines',    7),
-- ('hardJet',             9),
-- ('RianAir',             7)
-- ;





-- INSERT INTO is_located_in (hotel_id, city_id)
-- VALUES
-- (1,1),
-- (2,1),
-- (3,2),
-- (4,3),
-- (5,4),
-- (6,4),
-- (7,5),
-- (8,6),
-- (9,7),
-- (10,8),
-- (11,9),
-- (12,9),
-- (13,10),
-- (14,11),
-- (15,12),
-- (16,13),
-- (17,14),
-- (18,15),
-- (19,15),
-- (20,16),
-- (21,17),
-- (22,17),
-- (23,18),
-- (24,19),
-- (25,19),
-- (26,20),
-- (27,21),
-- (28,21),
-- (29,22),
-- (30,22),
-- (31,23),
-- (32,24)
-- ;



-- INSERT INTO goes_to_and_from (route_id, city_id)
-- VALUES
-- (,1),
-- (,2),
-- (,3),
-- (,4),
-- (,5),
-- (,6),
-- (,7),
-- (,8),
-- (,9),
-- (,10),
-- (,11),
-- (,12),
-- (,13),
-- (,14),
-- (,15),
-- (,16),
-- (,17),
-- (,18),
-- (,19),
-- (,20),
-- (,21),
-- (,22),
-- (,23),
-- (,24)
-- ;



-- INSERT INTO flies_to_and_from ()
-- VALUES
-- (SELECT airline_id FROM airlines),
-- (SELECT city_id FROM destinations)
-- ;



-- INSERT INTO operates ()
-- VALUES
-- (SELECT airline_id FROM airlines),
-- (SELECT route_id FROM routes)
-- ;





-- INSERT INTO dreams_about ()
-- VALUES
-- (SELECT user_id FROM users),
-- (SELECT city_id FROM destinations)
-- ;

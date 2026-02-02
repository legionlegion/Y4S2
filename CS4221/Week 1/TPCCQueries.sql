CREATE TABLE warehouses (
   w_id INTEGER PRIMARY KEY,
   w_name VARCHAR(16) NOT NULL,
   w_street VARCHAR(32) NOT NULL,
   w_city VARCHAR(32) NOT NULL,
   w_country CHAR(16) NOT NULL);
 
 INSERT INTO warehouses 
 (w_id, w_name, w_street, w_city, w_country) 
 VALUES 
 (301, 'Schmedeman', 'Sunbrook', 'Singapore', 'Singapore');
 
CREATE TABLE items (
   i_id INTEGER PRIMARY KEY,
   i_im_id CHAR(8) UNIQUE NOT NULL,
   i_name VARCHAR(64)  NOT NULL,
   i_price NUMERIC NOT NULL CHECK(i_price >0));

INSERT INTO items 
(i_id, i_im_id, i_name, i_price) 
VALUES 
(1, '35356226', 'Indapamide', 95.23);

CREATE TABLE stocks (
   w_id INTEGER REFERENCES warehouses(w_id),
   i_id INTEGER REFERENCES items(i_id),
   s_qty SMALLINT CHECK(s_qty > 0),
   PRIMARY KEY (w_id, i_id));

INSERT INTO stocks VALUES (301, 1, 338);
INSERT INTO stocks VALUES (301, 1, 12);
INSERT INTO stocks VALUES (301, 4, 938);

DROP TABLE stocks;
DROP TABLE items;
DROP TABLE warehouses;

% Create and populate the database using the TPCCSchema.sql, TPCCitems.sql, TPCCwarehouses.ql and TPCCstocks.sql

SELECT w.w_name
FROM warehouses w
WHERE w.w_id = 123;

SELECT w.w_name
FROM warehouses w
WHERE w.w_city = 'Singapore';

SELECT s.i_id
FROM stocks s
WHERE s.s_qty BETWEEN 0 AND 10;

SELECT s.i_id
FROM stocks s
WHERE s.s_qty <= 10;

SELECT w.w_city, w.w_name
FROM warehouses w
WHERE w.w_city LIKE 'Si%';

SELECT s1.i_id
FROM stocks s1
WHERE s1.s_qty = ALL (
 SELECT MAX(s2.s_qty) 
 FROM stocks s2);
 
SELECT w.w_id, w.w_name, w.w_city
FROM warehouses w
ORDER BY w.w_name;

SELECT w.w_id, w.w_name, w.w_city 
FROM warehouses w
ORDER BY w.w_city, w.w_name;

SELECT w.w_id, w.w_name
FROM warehouses w
ORDER BY w.w_city;

SELECT s.i_id 
FROM stocks s 
GROUP BY s.i_id;

SELECT s.i_id, FLOOR(AVG(s.s_qty)) AS average_qty
FROM stocks s
GROUP BY s.i_id;

SELECT s.i_id, FLOOR(AVG(s.s_qty)) AS average_qty
FROM stocks s
GROUP BY s.i_id, s.w_id;

SELECT s.w_id
FROM stocks s
GROUP BY s. w_id
HAVING AVG(s.s_qty) >= 550;

SELECT s.i_id
FROM stocks s, warehouses w
WHERE s.w_id = w.w_id
 AND w.w_city = 'Singapore';
 
SELECT s.i_id
FROM stocks s CROSS JOIN warehouses w
WHERE s.w_id = w.w_id
 AND w.w_city = 'Singapore';

SELECT s.i_id
FROM stocks s JOIN warehouses w
ON s.w_id = w.w_id
WHERE w.w_city = 'Singapore';

SELECT DISTINCT s.i_id
FROM stocks s, warehouses w
WHERE s.w_id = w.w_id
   AND w.w_city = 'Singapore';

SELECT  s.i_id
FROM stocks s, warehouses w
WHERE s.w_id = w.w_id
  AND w.w_city = 'Singapore'
UNION
SELECT  1
WHERE FALSE;

SELECT  s.i_id
FROM stocks s, warehouses w
WHERE s.w_id = w.w_id
   AND w.w_city = 'Singapore'
UNION
SELECT  s.i_id
FROM stocks s, warehouses w
WHERE s.w_id = w.w_id
   AND w.w_city = 'Singapore';

SELECT s.i_id
FROM stocks s NATURAL JOIN warehouses w
WHERE w.w_city = 'Singapore';

SELECT s.i_id
FROM stocks s INNER JOIN warehouses w ON s.w_id = w.w_id
WHERE w.w_city = 'Singapore';


SELECT i.i_id, s.w_id
FROM items i LEFT OUTER JOIN stocks s 
ON i.i_id=s.i_id;

SELECT i.i_id, s.w_id
FROM items i LEFT OUTER JOIN stocks s 
ON i.i_id = s.i_id
WHERE s.w_id IS NULL;

SELECT i.i_id, s.w_id
FROM  stocks s RIGHT OUTER JOIN  items i
ON i.i_id=s.i_id;

SELECT i.i_id, s.w_id
FROM  stocks s FULL OUTER JOIN  items i
ON i.i_id=s.i_id;

SELECT (SELECT s.i_id
FROM stocks s
WHERE s.w_id = w.w_id
 AND w.w_city = 'Singapore'
 AND s.i_id = s1.i_id)
FROM warehouses w, stocks s1
WHERE w.w_city = 'Singapore'
AND s1.w_id = w.w_id

SELECT s.i_id
FROM stocks s, (
 SELECT w.w_id 
 FROM warehouses w 
 WHERE w.w_city = 'Singapore') AS w1
WHERE s.w_id = w1.w_id;

SELECT s.i_id
FROM stocks s 
WHERE s.w_id IN (
 SELECT w.w_id 
 FROM warehouses w 
 WHERE w.w_city = 'Singapore');

SELECT s.i_id
FROM stocks s 
WHERE s.w_id = ANY (
 SELECT w.w_id 
 FROM warehouses w 
 WHERE w.w_city = 'Singapore');

SELECT s.i_id
FROM stocks s 
GROUP BY s.w_id, s.i_id
HAVING s.w_id IN (
 SELECT w.w_id 
 FROM warehouses w 
 WHERE w.w_city = 'Singapore');
 
SELECT s.i_id
FROM stocks s 
WHERE EXISTS (
 SELECT * 
 FROM warehouses w 
 WHERE s.w_id = w.w_id 
 AND w.w_city = 'Singapore');

CREATE TABLE singapore_warehouses AS 
    SELECT w.w_id 
    FROM warehouses w 
    WHERE w.w_city = 'Singapore';

SELECT s.i_id
FROM stocks s,  singapore_warehouses  w
WHERE s.w_id = w.w_id;
 
DROP TABLE singapore_warehouses;

CREATE TEMPORARY TABLE singapore_warehouses AS 
    SELECT w.w_id 
    FROM warehouses w 
    WHERE w.w_city = 'Singapore';

SELECT s.i_id
FROM stocks s,  singapore_warehouses  w
WHERE s.w_id = w.w_id;
 
DROP TABLE singapore_warehouses;

CREATE VIEW singapore_warehouses AS 
    SELECT w.w_id 
    FROM warehouses w 
    WHERE w.w_city = 'Singapore';

SELECT s.i_id
FROM stocks s,  singapore_warehouses  w
WHERE s.w_id = w.w_id;
 
DROP VIEW singapore_warehouses;

WITH singapore_warehouses AS (
    SELECT w.w_id 
    FROM warehouses w 
    WHERE w.w_city = 'Singapore'
    )
SELECT s.i_id
FROM stocks s,  singapore_warehouses  w1
WHERE s.w_id = w1.w_id;

SELECT i.i_id
FROM items i 
WHERE NOT EXISTS (
   SELECT *
   FROM warehouses w 
   WHERE NOT EXISTS (
      SELECT * 
      FROM stocks s 
      WHERE s.w_id=w.w_id AND s.i_id=i.i_id));

%%%

CREATE INDEX i_i_price ON items(i_price);

GRANT UPDATE ON stocks TO john;

CREATE OR REPLACE FUNCTION myage(dob DATE) 
RETURNS INTEGER AS $$
BEGIN
RETURN DATE_PART('year', current_date) - DATE_PART('year', dob)::INTEGER;
END; $$
LANGUAGE PLPGSQL;

SELECT myage('1965-04-03');

CREATE TABLE IF NOT EXISTS log (
    ltimestamp TIMESTAMPTZ NOT NULL,
    laction VARCHAR(10) NOT NULL,
    ltable VARCHAR(100) NOT NULL,
    lnew TEXT);

CREATE OR REPLACE FUNCTION log_change()
RETURNS TRIGGER AS $$
DECLARE
    action_text TEXT;
BEGIN
    IF TG_OP = 'INSERT' THEN
        action_text := 'INSERT';
    ELSIF TG_OP = 'DELETE' THEN
        action_text := 'DELETE';
        NEW := OLD;
    ELSE
        RETURN NEW;
    END IF;
    INSERT INTO log
    VALUES (current_timestamp, action_text, TG_TABLE_NAME,  NEW::TEXT);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DELETE FROM stocks WHERE w_id = 301 AND i_id  = 1;
SELECT * FROM stocks WHERE w_id = 301 AND i_id  = 1;
INSERT INTO stocks VALUES (301, 1, 338);
SELECT * FROM log;
DELETE FROM stocks;
SELECT * FROM log;



/* Matric Number: A0251802N */
/* Q01 */
WITH season_w_count AS (
	SELECT s.year AS season, SUM(CASE WHEN rs.position_text = 'W' THEN 1 ELSE 0 END) AS count
	FROM seasons s, races r, results rs
	WHERE s.year = r.season 
		AND r.date = rs.race
	GROUP BY s.year
), min_withdrawal AS (
	SELECT MIN(season_w_count.count) AS min_count
	FROM season_w_count
)
SELECT sw.season, sw.count
FROM season_w_count sw, min_withdrawal mw
WHERE sw.count = mw.min_count
ORDER BY sw.season ASC;

/* Q02 */
WITH losers AS (
	SELECT name
	FROM constructors
	WHERE name NOT IN (
		SELECT constructor 
		FROM results
		WHERE position <= 3
	) AND name IN (
		SELECT constructor FROM results
	)
) 
SELECT rs.constructor, MIN(s.year) AS first, MAX(s.year) AS last
FROM results rs, races r, seasons s, losers
WHERE rs.race = r.date
AND r.season = s.year
AND rs.constructor = losers.name
GROUP BY rs.constructor
ORDER BY rs.constructor ASC;

/* Q03 */
SELECT d.forename, d.surname, SUM(CASE WHEN q.position = 1 THEN 1 ELSE 0 END) AS count
FROM drivers d LEFT JOIN qualifyings q
ON d.forename = q.driver_forename
AND d.surname = q.driver_surname
GROUP BY d.forename, d.surname
ORDER BY count DESC, surname ASC, forename ASC;

/* Q04 */
SELECT rs.race, rs.driver_forename AS forename, rs.driver_surname AS surname, q.position AS pole
FROM results rs, qualifyings q
WHERE rs.race = q.race
AND rs.driver_forename = q.driver_forename
AND rs.driver_surname = q.driver_surname
AND rs.position = 1
AND q.position != 1
ORDER BY race ASC;

/* Q05 */
WITH wins AS (
SELECT s.year AS season, rs.driver_forename, 
rs.driver_surname, 
SUM(CASE WHEN rs.position=1 THEN 1 ELSE 0 END) AS sum_wins,
SUM(rs.points) as points
FROM results rs, races r, seasons s
WHERE rs.race = r.date AND s.year = r.season
GROUP BY s.year, driver_forename, driver_surname
), max_points AS (
	SELECT season, MAX(points) AS max_points
	FROM wins
	GROUP BY season
)
SELECT w.season, w.driver_forename AS forename, w.driver_surname AS surname, w.sum_wins AS wins
FROM wins w, max_points mp
WHERE w.points = mp.max_points
AND w.season = mp.season
ORDER BY season ASC;
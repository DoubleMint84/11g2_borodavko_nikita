UPDATE users SET birthdate = SUBSTR(birthdate, 7, 4) || '-' || SUBSTR(birthdate, 4, 2) || '-' || SUBSTR(birthdate, 1, 2);

SELECT "login" FROM users ORDER BY id DESC LIMIT 1;

SELECT DISTINCT(SUBSTR(birthdate, 1, 4)) as unique_years FROM users;

SELECT COUNT(*) as total_items FROM items;

SELECT avg((julianday('now') - julianday(birthdate)) / 365) FROM users WHERE (strftime('%m','now') - strftime('%m',registration_date)) <= 2;
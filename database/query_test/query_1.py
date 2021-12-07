import sqlite3

db = sqlite3.connect('../extrud3r_database.db')
cursor = db.cursor()

cursor.execute(
    '''
    SELECT "id" as 'order ID',
    date,
    total, 
    state, 
    (SELECT country FROM address WHERE address.id = customer_id) as 'country', 
    (SELECT city FROM address WHERE address.id = customer_id) as 'city', 
    (SELECT street FROM address WHERE address.id = customer_id) as 'street', 
    (SELECT house FROM address WHERE address.id = customer_id) as 'house', 
    (SELECT floor FROM address WHERE address.id = customer_id) as 'floor',
    (SELECT flat FROM address WHERE address.id = customer_id) as 'flat',
    (SELECT postcode FROM address WHERE address.id = customer_id) as 'postcode'
    FROM orders WHERE orders.customer_id = 2;
    '''
)
print(cursor.fetchall())
db.close()
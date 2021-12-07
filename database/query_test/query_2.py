import sqlite3

db = sqlite3.connect('../extrud3r_database.db')
cursor = db.cursor()

cursor.execute(
    '''
    SELECT (SELECT name FROM items WHERE items.id = item_id) as 'item name',
    (SELECT photo FROM items WHERE items.id = item_id) as 'item photo address',
    price_per_item as 'price per item',
    count as 'count'
    FROM order_list WHERE order_list.order_id = 1;
    '''
)
print(cursor.fetchall())
db.close()
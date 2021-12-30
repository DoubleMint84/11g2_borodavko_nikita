import sqlite3


class DB:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)
        self.new_cursor()

    def new_cursor(self):
        self.cursor = self.connection.cursor()

    def order_list(self, par):
        self.cursor.execute(
            '''
            SELECT "id" as 'order ID',
            date,
            total, 
            state, 
            (SELECT country FROM address WHERE address.id = address_id) as 'country', 
            (SELECT city FROM address WHERE address.id = address_id) as 'city', 
            (SELECT street FROM address WHERE address.id = address_id) as 'street', 
            (SELECT house FROM address WHERE address.id = address_id) as 'house', 
            (SELECT floor FROM address WHERE address.id = address_id) as 'floor',
            (SELECT flat FROM address WHERE address.id = address_id) as 'flat',
            (SELECT postcode FROM address WHERE address.id = address_id) as 'postcode'
            FROM orders WHERE orders.customer_id = :par;
            ''', {'par': par}
        )
        return self.cursor.fetchall()

    def order_info(self, par):
        self.cursor.execute(
            '''
            SELECT (SELECT name FROM items WHERE items.id = item_id) as 'item name',
            (SELECT photo FROM items WHERE items.id = item_id) as 'item photo address',
            price_per_item as 'price per item',
            count as 'count'
            FROM order_list WHERE order_list.order_id = :par;
            ''', {'par': par}
        )
        return self.cursor.fetchall()

    def address_list(self, par):
        self.cursor.execute(
            '''
            SELECT 
            address_id as 'address id',
            (SELECT country FROM address WHERE address.id = address_id) as 'country', 
            (SELECT city FROM address WHERE address.id = address_id) as 'city', 
            (SELECT street FROM address WHERE address.id = address_id) as 'street', 
            (SELECT house FROM address WHERE address.id = address_id) as 'house', 
            (SELECT floor FROM address WHERE address.id = address_id) as 'floor',
            (SELECT flat FROM address WHERE address.id = address_id) as 'flat',
            (SELECT postcode FROM address WHERE address.id = address_id) as 'postcode'
            FROM user_address WHERE user_address.customer_id = :par;
            ''', {'par': par}
        )
        return self.cursor.fetchall()

    def __del__(self):
        self.connection.close()

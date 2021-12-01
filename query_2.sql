1) Запрос истории заказов определенного пользователя(например, показ истории заказов в личном кабинете).
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

2) Запрос списка позиций в определенном заказе (например, для показа пользователю списка позиций заказа в личном кабинете)
 SELECT (SELECT name FROM items WHERE items.id = item_id) as 'item name',
(SELECT photo FROM items WHERE items.id = item_id) as 'item photo address',
 price_per_item as 'price per item',
 count as 'count'
 FROM order_list WHERE order_list.order_id = 1;

3) Запрос списка привязанных адресов к определенному пользователю(например, для выбора адреса доставки при оформлении заказа)
SELECT 
address_id as 'address id',
 (SELECT country FROM address WHERE address.id = customer_id) as 'country', 
 (SELECT city FROM address WHERE address.id = customer_id) as 'city', 
 (SELECT street FROM address WHERE address.id = customer_id) as 'street', 
 (SELECT house FROM address WHERE address.id = customer_id) as 'house', 
 (SELECT floor FROM address WHERE address.id = customer_id) as 'floor',
 (SELECT flat FROM address WHERE address.id = customer_id) as 'flat',
 (SELECT postcode FROM address WHERE address.id = customer_id) as 'postcode'
 FROM user_address WHERE user_address.customer_id = 2;
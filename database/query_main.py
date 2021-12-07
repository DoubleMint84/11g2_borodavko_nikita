import sqlite3

def order_list(par):
    global cursor
    cursor.execute(
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
        ''',{'par':par}
    )
    return cursor.fetchall()

def order_info(par):
    global cursor
    cursor.execute(
        '''
        SELECT (SELECT name FROM items WHERE items.id = item_id) as 'item name',
        (SELECT photo FROM items WHERE items.id = item_id) as 'item photo address',
        price_per_item as 'price per item',
        count as 'count'
        FROM order_list WHERE order_list.order_id = :par;
        ''', {'par':par}
    )
    return cursor.fetchall()

def address_list(par):
    global cursor
    cursor.execute(
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
        ''', {'par':par}
    )
    return cursor.fetchall()

db = sqlite3.connect('extrud3r_database.db')
cursor = db.cursor()
print('''
    Добро пожаловать в среду взаимодействия с БД интернет-магазина!
    -> Для вызова списка команд введите help
    -> Для закрытия приложение введите exit
''')
command = input('?> ')
while command != "exit":
    if command == "help":
        print('''-> order list <id> - вывести историю заказов пользователя под номером id
-> order info <order_id> - вывести список позиций в заказе order_id
-> address list <id> - список привязанных адресов к пользователю id''')
    else:
        arg = command.split()
        try:
            if arg[0] == 'order':
                if arg[1] == 'list':
                    num = int(arg[2])
                    res = order_list(num)
                    print(*res, sep='\n')
                elif arg[1] == 'info':
                    num = int(arg[2])
                    res = order_info(num)
                    print(*res, sep='\n')
                else:
                    raise BaseException
            elif arg[0] == 'address':
                if arg[1] == 'list':
                    num = int(arg[2])
                    res = address_list(num)
                    print(*res, sep='\n')
                else:
                    raise BaseException
            else:
                raise BaseException

        except:
            print('!!!> Некорректная команда, попробуйте еще раз')
    command = input('?> ')
print('-> Завершение работы...')

db.close()
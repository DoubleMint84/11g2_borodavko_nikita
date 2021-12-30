import unittest
from query_class import DB


class test_db(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.database = DB("extrud3r_database.db")

    def test_list_of_orders_customer_3(self):
        res = self.database.order_list(3)
        self.assertEqual(res,
                         [(2, '20.11.2021', 150, 0, 'РФ', 'Москва', 'Балаклавский пр-кт', '6', '4', '418', '117639')])

    def test_list_of_items_order_id_1(self):
        res = self.database.order_info(1)
        self.assertEqual(res, [('Голодный кот', None, 200, 1), ('Калибровочный кубик 20x20', None, 100, 3)])

    def test_address_list_id_2(self):
        res = self.database.address_list(2)
        self.assertEqual(res, [(1, 'US', 'Los Santos', 'Groove St', '4', '1', '1', '87ZP32')])


if __name__ == '__main__':
    unittest.main()

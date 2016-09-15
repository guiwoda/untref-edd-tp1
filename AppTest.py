import unittest
from unittest.mock import Mock

from cursesmenu import CursesMenu

from MotorDeRutas import MotorDeRutas
from app import App

class AppTest(unittest.TestCase):

    def test_main(self):
        menu_mock = Mock(spec=CursesMenu)
        motor_mock = Mock(spec=MotorDeRutas)

        App(motor_mock, menu_mock).main()

        self.assertEqual(menu_mock.append_item.call_count, 11)
        self.assertFalse(menu_mock.show_exit_option)
        self.assertEqual(menu_mock.show.call_count, 1)

if __name__ == '__main__':
    unittest.main()
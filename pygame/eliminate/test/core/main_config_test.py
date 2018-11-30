import unittest
from core.main_config import MainConfig


class TestMainConfig(unittest.TestCase):

    def test_read_json(self):
        configs = MainConfig()
        self.assertEqual(len(configs.monsters), 3)

        print(configs.monsters)

    def test_string(self):
        configs = MainConfig()
        configs.string()


if __name__ == '__main__':
    unittest.main()

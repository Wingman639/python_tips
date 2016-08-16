# test.py
import mock
import unittest

import mock_func


class MyTestCase(unittest.TestCase):

    @mock.patch('mock_func.multiply')
    def test_add_and_multiply(self, mock_multiply):

        x = 3
        y = 5

        mock_multiply.return_value = 15

        addition, multiple = mock_func.add_and_multiply(x, y)

        mock_multiply.assert_called_once_with(3, 5)

        self.assertEqual(8, addition)
        self.assertEqual(15, multiple)

if __name__ == "__main__":
    unittest.main()
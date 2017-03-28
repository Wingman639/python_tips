#-*- coding: utf-8 -*-


def is_ascii(text):
    try:
        text.decode('ascii')
    except UnicodeEncodeError:
        return False
    return True

if __name__ == '__main__':
    import unittest

    class TestIsAscii(unittest.TestCase):
        def test_is_ascii_true(self):
            text = 'abcdeABCDE012345 ./]};,'
            self.assertTrue(is_ascii(text))

        def test_is_ascii_false_unicode_chinese(self):
            text = u'汉字'
            self.assertFalse(is_ascii(text))

        def test_is_ascii_false_unicode_french(self):
            text = u'Allô'
            self.assertFalse(is_ascii(text))

    unittest.main()
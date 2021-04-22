import unittest


class TestCase(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_ok(self):
        self.assertEqual("foo".upper(), "FOO")
        for i in range(int(10e3)):
            for j in range(int(10e3)):
                print(i)


suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)

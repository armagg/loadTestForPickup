import unittest


class DevCallTest(unittest.TestCase):
    def test_argument_adder(self):
        from common import commands_call
        self.assertEqual(commands_call.argument_adder('omid.mesgarha', '12345678', '9732331122'),
                         'omid.mesgarha%2012345678%209732331122%20')


if __name__ == '__main__':
    unittest.main()

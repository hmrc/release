import sys, os
this_file = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_file, "../src/universal/bin"))
import unittest
from lib import call, read_user_preferred_version_with_input_function


class LibTestCase(unittest.TestCase):
    def test_call(self):
        result = call("echo Expected")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.read().strip(), "Expected")
        self.assertNotEqual(call("Thisisnotabashscript").returncode, 0)

    def test_update_bugfix_version(self):
        bugfix = lambda x: "3"
        new_version = read_user_preferred_version_with_input_function("service_name", "2.3.4", bugfix)
        self.assertEqual(new_version, "2.3.5")

    def test_update_minor_version(self):
        minor = lambda x: "2"
        new_version = read_user_preferred_version_with_input_function("service_name", "2.3.4", minor)
        self.assertEqual(new_version, "2.4.0")

    def test_update_major_version(self):
        major = lambda x: "1"
        new_version = read_user_preferred_version_with_input_function("service_name", "2.3.4", major)
        self.assertEqual(new_version, "3.0.0")

    def test_should_not_update_on_invalid_input(self):
        user_input = [0, 3, 0]
        major = lambda x: user_input.pop()
        new_version = read_user_preferred_version_with_input_function("service_name", "2.3.4", major)
        self.assertEqual(new_version, "2.3.5")
        self.assertEqual(len(user_input), 1,
                         "User should have been asked again for input after giving an invalid answer")

if __name__ == '__main__':
    unittest.main()

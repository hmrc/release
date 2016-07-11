import sys
import os
this_file = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_file, "../src/universal/bin"))
import lib
import json
import shutil
import unittest

from config import Configuration

class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.conf_1 = "/tmp/release_config_test_file_1.config"

        with open(self.conf_1, "w") as fh:
            json.dump({}, fh)

        self.conf_2 = "/tmp/release_config_test_file_2.config"

        with open(self.conf_2, "w") as fh:
            json.dump({'jenkins_user': 'brian'}, fh)

        self.conf_3 = "/tmp/release_config_test_file_3.config"

        with open(self.conf_3, "w") as fh:
            json.dump({'jenkins_user': 'brian', 'jenkins_key': '987fed', 'jenkins': 'http://my-real-jenkins.com'}, fh)

    def tearDown(self):
        map(lambda x: os.remove(x), [
            self.conf_1, self.conf_2, self.conf_3
        ])

    def test_no_config_file_no_env_var(self):
        config = Configuration("~/no_such_file", {})

        jenkins = config.jenkins
        jenkins_user = config.jenkins_user
        jenkins_key = config.jenkins_key

        self.assertTrue(jenkins_user == None)
        self.assertTrue(jenkins_key == None)
        self.assertTrue(jenkins == 'https://ci.example.com')

    def test_empty_config_file_no_env_var(self):
        config = Configuration(self.conf_1, {})

        jenkins = config.jenkins
        jenkins_user = config.jenkins_user
        jenkins_key = config.jenkins_key

        self.assertTrue(jenkins_user == None)
        self.assertTrue(jenkins_key == None)
        self.assertTrue(jenkins == 'https://ci.example.com')

    def test_no_config_file_with_env_var(self):
        config = Configuration('nothing_to_see', {'jenkins_user': 'bob'})

        jenkins = config.jenkins
        jenkins_user = config.jenkins_user
        jenkins_key = config.jenkins_key

        self.assertTrue(jenkins_user == 'bob')
        self.assertTrue(jenkins_key == None)
        self.assertTrue(jenkins == 'https://ci.example.com')

    def test_empty_config_file_with_env_var(self):
        config = Configuration(self.conf_1, {'jenkins_user': 'bob'})

        jenkins = config.jenkins
        jenkins_user = config.jenkins_user
        jenkins_key = config.jenkins_key

        self.assertTrue(jenkins_user == 'bob')
        self.assertTrue(jenkins_key == None)
        self.assertTrue(jenkins == 'https://ci.example.com')

    def test_config_file_overrides_env_var(self):
        config = Configuration(self.conf_2, {'jenkins_user': 'bob'})

        jenkins = config.jenkins
        jenkins_user = config.jenkins_user
        jenkins_key = config.jenkins_key

        self.assertTrue(jenkins_user == 'brian')
        self.assertTrue(jenkins_key == None)
        self.assertTrue(jenkins == 'https://ci.example.com')


    def test_config_file_overrides_everything(self):
        config = Configuration(self.conf_3, {'jenkins_user': 'bob', 'jenkins_key': 'abc123'})

        jenkins = config.jenkins
        jenkins_user = config.jenkins_user
        jenkins_key = config.jenkins_key

        self.assertTrue(jenkins_user == 'brian')
        self.assertTrue(jenkins_key == '987fed')
        self.assertTrue(jenkins == 'http://my-real-jenkins.com')


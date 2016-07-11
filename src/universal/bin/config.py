import argparse
import os
import json
import lib
import sys
from os.path import expanduser


class Configuration:
    def __init__(self, config_file_path="~/.hmrc/release.conf", env=os.environ):
        legacy_hosts_file = 'conf/hosts.json'
        self.config_file = expanduser(config_file_path)
        out = {}
        try:
            hosts_json = lib.open_as_json(legacy_hosts_file)
            out.update(hosts_json)
        except RuntimeError, ex:
            print("Config file %s is probably not valid JSON: %s" % (legacy_hosts_file, ex.msg))

        if os.path.exists(self.config_file):
            try:
                out.update(json.load(open(self.config_file)))
            except RuntimeError, ex:
                print("Config file %s is probably not valid JSON: %s" % (self.config_file, ex.msg))

        if (not out.has_key('jenkins_user')):
            out['jenkins_user'] = env.get("jenkins_user", None)
        if (not out.has_key('jenkins_key')):
            out['jenkins_key'] = env.get("jenkins_key", None)

        self.__dict__.update(out)

    def validate(self):
        expected = ["jenkins", "jenkins_user", "jenkins_key"]
        out = [key for key in expected if not self.__dict__[key]]
        if out:
            print "Warning: The following keys need adding to your JSON config file %s." % out
            sys.exit(1)




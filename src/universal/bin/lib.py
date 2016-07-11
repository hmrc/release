#
#  Copyright 2015 HM Revenue & Customs
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#!/usr/bin/env python

import subprocess
import os
import json
import signal
import sys


def open_as_json(source):
    this_file = os.path.realpath(__file__)
    path = os.path.join(os.path.dirname(this_file), os.pardir, source)
    with open(path) as f:
        return json.load(f)


def call(command, quiet=True):
    if not quiet: print "calling: '" + command + "' from: '" + os.getcwd() + "'"
    ps_command = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ps_command.wait()
    return ps_command


def call_and_exit_if_failed(command):
    ps_command = call(command)
    if ps_command.returncode != 0:
        print 'The command ' + command + ' failed, exiting'
        sys.exit(ps_command.returncode)
    return ps_command


def interrupted():
    print 'No response from user, exiting.'


def read_user_preferred_version(service_name, current_version):
    return read_user_preferred_version_with_input_function(service_name, current_version, raw_input)


def read_user_preferred_version_with_input_function(service_name, current_version, input_function):
    version_array = current_version.split('.')
    new_patch_version = version_array[0] + '.' + version_array[1] + '.' + str(int(version_array[2]) + 1)
    new_minor_version = version_array[0] + '.' + str(int(version_array[1]) + 1) + '.0'
    new_major_version = str(int(version_array[0]) + 1) + '.0.0'
    new_version = ""
    print "The current version: '" + current_version + "' for: '" + service_name + "' has changed and requires a new version number.\n \
[1] major: " + new_major_version + "\n \
[2] minor: " + new_minor_version + "\n \
[3] patch: " + new_patch_version + "\n"
    while 1:
        try:
            choice = int(input_function('Please choose next version: '))
        except ValueError:
            print "Please enter a number between 1 and 3"
            continue
        if choice == 1:
            new_version = new_major_version
            break
        if choice == 2:
            new_version = new_minor_version
            break
        if choice == 3:
            new_version = new_patch_version
            break

        print "Please enter a number between 1 and 3"

    print 'New version of ' + service_name + ' is ' + new_version
    return new_version


signal.signal(signal.SIGALRM, interrupted)

#!/usr/bin/env python
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

import argparse
import os
import json
import lib
import sys
from os.path import expanduser
import shutil

from jenkins import Jenkins
from git import Git
from config import Configuration

parser = argparse.ArgumentParser(description='Library release tagger - tag non-snapshot libraries')
parser.add_argument('-v', '--verbose', action='store_true', help='Print debug output')
parser.add_argument('projectName', type=str, help='The jenkins build of the repo we want to tag')
parser.add_argument('buildNumber', type=str, help='The jenkins build number we want to tag')
args = parser.parse_args()

WORKSPACE = expanduser("~/.release")

if os.path.exists(WORKSPACE):
    shutil.rmtree(WORKSPACE)
os.mkdir(WORKSPACE)

conf = Configuration()
conf.validate()

jenkins = Jenkins(conf.jenkins, conf.jenkins_user, conf.jenkins_key)


def verbose(message):
    if args.verbose:
        print(message)


def run():
    jenkins_project = args.projectName
    jenkins_build_number = args.buildNumber

    if not jenkins.find_if_build_is_green(jenkins_project, jenkins_build_number):
        print("Build #" + jenkins_build_number + " of '" + jenkins_project + "' is not a green build.")
        sys.exit(1)

    repo_url = jenkins.find_github_repo_url_from_build(jenkins_project)

    git = Git(WORKSPACE, repo_url)

    commit_id = jenkins.find_commit_id_from_build(jenkins_project, jenkins_build_number)
    verbose("commit_id=" + commit_id)

    repo_name = git.repo_name()
    verbose("repo_name=" + repo_name)

    git.clone()
    verbose("Git repo '" + repo_name + "' cloned to " + WORKSPACE)

    most_recent_tag = git.describe(commit_id)
    verbose("Most recent release: " + most_recent_tag)

    new_version_number = lib.read_user_preferred_version(repo_name, most_recent_tag)

    git.tag(commit_id, "release/" + new_version_number)

run()

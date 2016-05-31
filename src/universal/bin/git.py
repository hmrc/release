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

import os
import lib


branch = 'master'


class Git:
    def __init__(self, root_dir, repo_url, verbose=False):
        self.root_dir = root_dir
        self.repo_url = repo_url
        self.verbose = verbose

    def repo_name(self):
        return os.path.splitext(os.path.basename(self.repo_url))[0]

    def path(self):
        return os.path.join(self.root_dir, self.repo_name())

    def clone(self):
        path = self.path()
        if not os.path.exists(path):
            if not os.path.exists(self.root_dir):
                os.mkdir(self.root_dir)
            os.chdir(self.root_dir)
            if self.verbose:
                print 'cloning into ' + path
            lib.call_and_exit_if_failed('git clone -q %s' % self.repo_url)
        os.chdir(path)
        lib.call_and_exit_if_failed('git fetch -q')

    def update(self):
        path = self.path()
        os.chdir(path)
        lib.call_and_exit_if_failed('git checkout -q ' + branch)
        lib.call_and_exit_if_failed('git pull -q origin ' + branch)

    def describe(self, ref=''):
        path = self.path()
        os.chdir(path)
        tag_query = lib.call('git describe --abbrev=0 --match release/* %s' % ref)
        last_tag = "0.0.0"
        if tag_query.returncode == 0:
            last_tag = tag_query.stdout.read().strip()
        last_version_number = last_tag.split('/')[-1]
        return last_version_number

    def tag(self, commit_id, tag):
        path = self.path()
        os.chdir(path)
        lib.call_and_exit_if_failed('git tag -a ' + tag + ' -m \'releasing version '
                                    + tag + ' of ' + self.repo_name() + '\' ' + commit_id)
        print 'Pushing new tag ' + tag + ' to origin'
        lib.call_and_exit_if_failed('git push -q origin ' + tag)

    def latest_commit_id(self):
        query = lib.call_and_exit_if_failed('git log -1 --pretty="%H"')
        return query.stdout.read().strip()


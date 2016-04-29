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

import os
import ast
import requests
import xml.etree.ElementTree as ET


def find_commit_id(jenkins_job_info):
    json = ast.literal_eval(jenkins_job_info)
    out = [obj["lastBuiltRevision"]['SHA1'] for obj in json['actions'] if
            (obj.get("buildsByBranchName"))]

    return out.pop()

def is_build_green(jenkins_job_info):
    json = ast.literal_eval(jenkins_job_info)
    return json.get('result') == 'SUCCESS'


class Jenkins:

    jenkins_git_hub_url_property_name = "scm/userRemoteConfigs/hudson.plugins.git.UserRemoteConfig/url"

    def __init__(self, host, user=os.environ["jenkins_user"], key=os.environ["jenkins_key"]):
        self.host = host
        self.auth = (user, key)

    def find_commit_id_from_build(self, jenkins_project, build_number):
        return find_commit_id(self._get_job_info(build_number, jenkins_project))

    def find_github_repo_url_from_build(self, jenkins_project):
        config_url = self.host + '/job/' + jenkins_project + '/config.xml'
        config_xml = requests.get(config_url, auth=self.auth).text.strip()
        return ET.fromstring(config_xml).find(self.jenkins_git_hub_url_property_name).text

    def find_if_build_is_green(self, jenkins_project, build_number):
        return is_build_green(self._get_job_info(build_number, jenkins_project))

    def _get_job_info(self, build_number, jenkins_project):
        jenkins_info_url = self.host + '/job/' + jenkins_project + '/' + build_number + '/api/python'
        return requests.get(jenkins_info_url, auth=self.auth).text.strip()

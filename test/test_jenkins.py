import sys
import os
this_file = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_file, "../src/universal/bin"))

import unittest
from jenkins import find_commit_id, is_build_green

lastBuiltRevision = {
    "SHA1": "c9308e1146cc4245b859792627c76e8fe81da7ef",
    "branch": [{
        "SHA1": "c9308e1146cc4245b859792627c76e8fe81da7ef",
        "name": "origin/master"
    }]
}

buildsByBranchName = {
    "origin/master": {
        "revision": {
            "SHA1": "697f4751d32b975ae34f0f6dc3a67eccbca1b078"
        }
    }
}

jenkins_job_with_builds_second = str({
    "actions": [
        {},
        {
            "buildsByBranchName": buildsByBranchName,
            "lastBuiltRevision": lastBuiltRevision
        }
    ]
})

jenkins_job_with_builds_third = str({
    "actions": [
        {},
        {},
        {
            "buildsByBranchName": buildsByBranchName,
            "lastBuiltRevision": lastBuiltRevision
        }
    ]
})

green_jenkins_job = str({
    "result": "SUCCESS"
})

red_jenkins_job = str({
    "result": "FAILURE"
})

running_jenkins_job = str({

})

class JenkinsTestCase(unittest.TestCase):
    def test_can_find_commit_id(self):
        self.assertEqual(find_commit_id(jenkins_job_with_builds_second), "c9308e1146cc4245b859792627c76e8fe81da7ef")
        self.assertEqual(find_commit_id(jenkins_job_with_builds_third), "c9308e1146cc4245b859792627c76e8fe81da7ef")

    def test_can_find_if_given_build_is_successful(self):
        self.assertTrue(is_build_green(green_jenkins_job), "Jenkins job was not green")
        self.assertFalse(is_build_green(red_jenkins_job), "Jenkins job has failed but was reported as green")
        self.assertFalse(is_build_green(running_jenkins_job), "Jenkins job is running or has no result but was reported as green")


if __name__ == '__main__':
    unittest.main()

import sys
import os
this_file = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_file, "../src/universal/bin"))
import lib
import shutil
import unittest

from git import Git

WORKSPACE = "/var/tmp/release-git-test"
root_dir_remote = os.path.join(WORKSPACE, "remote")
root_dir_local = os.path.join(WORKSPACE, "local")
git_server = "file:///" + root_dir_remote
test_repo = "test-repo"
test_repo_dir = os.path.join(root_dir_remote, test_repo)


class GitTestCase(unittest.TestCase):
    def setUp(self):
        # This is setting up a local git server with a test project
        if not os.path.exists(root_dir_remote):
            os.makedirs(test_repo_dir)
        os.chdir(test_repo_dir)
        lib.call_and_exit_if_failed('git init')
        with open('README.md', 'a') as the_file:
            the_file.write('Hello')
        lib.call_and_exit_if_failed('git add .')
        lib.call_and_exit_if_failed('git commit -m "test"')

    def tearDown(self):
        if os.path.exists(WORKSPACE):
            shutil.rmtree(WORKSPACE)

    def test_clone(self):
        git = Git(root_dir_local, test_repo_dir)
        git.clone()
        self.assertTrue(os.path.exists(os.path.join(test_repo_dir, "README.md")) == 1)

    def test_describe_never_tagged_before(self):
        git = Git(root_dir_local, test_repo_dir)
        git.clone()
        latest_tag = git.describe()
        self.assertEqual(latest_tag, "0.0.0")

    def test_describe_never_tagged_before(self):
        git = Git(root_dir_local, test_repo_dir)
        git.clone()
        lib.call_and_exit_if_failed('git tag -a release/0.1.1 -m \'releasing version\'')
        latest_tag = git.describe()
        self.assertEqual(latest_tag, "0.1.1")

    def test_tag(self):
        git = Git(root_dir_local, test_repo_dir)
        git.clone()
        git.tag(git.latest_commit_id(), "release/1.2.3")
        tag_query = lib.call('git describe --abbrev=0 --match release/*')
        self.assertEqual(tag_query.stdout.read().strip(), "release/1.2.3")

    def test_update(self):
        git = Git(root_dir_local, test_repo_dir)
        git.clone()
        self.assertTrue(os.path.exists(os.path.join(test_repo_dir, "ANOTHER_FILE.txt")) != 1)
        os.chdir(test_repo_dir)
        with open('ANOTHER_FILE.txt', 'a') as the_file:
            the_file.write('Another file')
        lib.call_and_exit_if_failed('git add .')
        lib.call_and_exit_if_failed('git commit -m "another commit"')
        git.update()
        self.assertTrue(os.path.exists(os.path.join(test_repo_dir, "ANOTHER_FILE.txt")) == 1)


if __name__ == '__main__':
    unittest.main()

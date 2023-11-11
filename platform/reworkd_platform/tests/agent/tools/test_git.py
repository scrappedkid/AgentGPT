import unittest
from unittest import mock
from reworkd_platform.web.api.agent.tools.git import GitTool

class TestGitTool(unittest.TestCase):
    def setUp(self):
        self.git_tool = GitTool()
        self.run_patch = mock.patch('reworkd_platform.web.api.agent.tools.git.subprocess.run')
        self.mock_run = self.run_patch.start()

    def tearDown(self):
        self.run_patch.stop()

    def test_git_clone(self):
        repository_url = 'https://github.com/test/repo.git'
        self.git_tool.git_clone(repository_url)
        self.mock_run.assert_called_once_with(f'git clone {repository_url}', shell=True)
        self.assertEqual(self.git_tool.git_clone(repository_url), 'Git clone successful!')

    def test_git_pull(self):
        repository_url = 'https://github.com/test/repo.git'
        self.git_tool.git_pull(repository_url)
        self.mock_run.assert_called_once_with(f'git -C {repository_url} pull', shell=True)
        self.assertEqual(self.git_tool.git_pull(repository_url), 'Git pull successful!')

    def test_git_push(self):
        repository_url = 'https://github.com/test/repo.git'
        self.git_tool.git_push(repository_url)
        self.mock_run.assert_called_once_with(f'git -C {repository_url} push', shell=True)
        self.assertEqual(self.git_tool.git_push(repository_url), 'Git push successful!')

if __name__ == '__main__':
    unittest.main()

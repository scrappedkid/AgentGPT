import os
import shutil
import subprocess
from git import Repo
from reworkd_platform.web.api.agent.tools.tool import Tool

class FileGitCodeTool(Tool):
    description = "Handle file operations, Git functionalities, and code execution."
    public_description = "Read and write Python, Markdown, and Text files, handle Git operations, and execute code."

    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def write_file(self, file_path, content):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    def clone_repo(self, repo_url, dir_path):
        Repo.clone_from(repo_url, dir_path)

    def pull_repo(self, dir_path):
        repo = Repo(dir_path)
        origin = repo.remotes.origin
        origin.pull()

    def push_repo(self, dir_path):
        repo = Repo(dir_path)
        origin = repo.remotes.origin
        origin.push()

    def execute_code(self, file_path):
        subprocess.run(["python", file_path])

    async def call(self, goal, task, input_str, *args, **kwargs):
        # TODO: Implement the logic to perform the appropriate file operation, Git functionality, or code execution based on the task.
        pass
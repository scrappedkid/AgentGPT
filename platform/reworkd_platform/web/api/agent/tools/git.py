from typing import Any
from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from reworkd_platform.web.api.agent.stream_mock import stream_string
from reworkd_platform.web.api.agent.tools.tool import Tool
import subprocess

class GitTool(Tool):
    description = "Tool for Git operations."
    public_description = "Git Tool allows you to perform Git operations on repositories."
    arg_description = "Git Tool requires a repository URL as input_str.  task can be one of: 'clone', 'pull', 'push'"
    image_url = "./images/git.png"

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        # Implement Git Tool logic here
        if task == 'clone':
            result = await self.git_clone(input_str)
        elif task == 'pull':
            result = await self.git_pull(input_str)
        elif task == 'push':
            result = await self.git_push(input_str)
        else:
            result = "Invalid task"

        # Return the result as a FastAPIStreamingResponse
        return FastAPIStreamingResponse(result)

    async def git_clone(self, repository_url: str) -> str:
        # Implement Git clone logic here
        cmd = f"git clone {repository_url}"
        subprocess.run(cmd, shell=True)
        return "Git clone successful!"

    async def git_pull(self, repository_url: str) -> str:
        # Implement Git pull logic here
        cmd = f"git -C {repository_url} pull"
        subprocess.run(cmd, shell=True)
        return "Git pull successful!"

    async def git_push(self, repository_url: str) -> str:
        # Implement Git push logic here
        cmd = f"git -C {repository_url} push"
        subprocess.run(cmd, shell=True)
        return "Git push successful!"

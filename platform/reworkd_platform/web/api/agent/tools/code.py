from typing import Any

from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from lanarky.responses import StreamingResponse
from langchain import LLMChain

from reworkd_platform.web.api.agent.tools.tool import Tool


class Code(Tool):
    description = "Should only be used to write code, refactor code, fix code bugs, and explain programming concepts."
    public_description = "Write and review code."

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        from reworkd_platform.web.api.agent.prompts import code_prompt

        chain = LLMChain(llm=self.model, prompt=code_prompt)

        # generated code
        code = # generated code
        self.write_to_shared_folder(f'{goal}_{task}.py', code)
        tags = self.generate_tags(code)
        self.write_to_shared_folder(f'{goal}_{task}_tags.txt', ', '.join(tags))

        return StreamingResponse.from_chain(
            chain,
            {"goal": goal, "language": self.language, "task": task},
            media_type="text/event-stream",
        )

    def write_to_shared_folder(self, filename: str, content: str) -> None:
        with open(f'shared_folder/{filename}', 'w') as f:
            f.write(content)

    def generate_tags(self, code: str) -> list:
        # Implement your tag generation logic here
        return []
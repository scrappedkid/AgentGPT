
from typing import Any
from datetime import datetime

from fastapi.responses import StreamingResponse
from lanarky.responses import StreamingResponse as LanarkyStreamingResponse
from langchain import LLMChain
from reworkd_platform.web.api.agent.tools.tool import Tool


class Code(Tool):
    """
    This class is used to generate, refactor, and fix code, as well as explain programming concepts. 
    It generates a stream of code using the LLMChain model, parses the code from the stream, 
    writes the code and associated tags to a shared folder, and returns the code stream as a StreamingResponse.
    """
    description = "Should only be used to write code, refactor code, fix code bugs, and explain programming concepts."
    public_description = "Write and review code"

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> StreamingResponse:
        from reworkd_platform.web.api.agent.prompts import code_prompt

        chain = LLMChain(llm=self.model, prompt=code_prompt)

        code_stream = await self.generate_code_stream(chain)

        # Create an instance of LLMChain with the current model and the code prompt, generate a stream of code, 
        # parse the code from the stream, write the code and associated tags to a shared folder, 
        # and return the code stream as a StreamingResponse.
        code = self.parse_code_from_stream(code_stream)

        filename = f"{goal}_{task}_{datetime.now().strftime('%Y%m%d%H%M%S')}.py"
        self.write_to_shared_folder(filename, code)

        # Generate tags
        tags = self.generate_tags(code)
        tags_filename = f"{goal}_{task}_{datetime.now().strftime('%Y%m%d%H%M%S')}_tags.txt"
        self.write_to_shared_folder(tags_filename, ", ".join(tags))

        return StreamingResponse(
            code_stream,
            media_type="text/event-stream",
        )

    async def generate_code_stream(self, chain: LLMChain) -> bytes:
        # Generate code using LLMChain and return as a byte stream
        # Example implementation:
        code = await chain.generate_text(prompt="Generate code")
        return code.encode("utf-8")

    def parse_code_from_stream(self, code_stream: bytes) -> str:
        # Parse the code from the byte stream
        code = code_stream.decode("utf-8")
        # Implement code parsing logic based on the specific format in the streaming response
        # Example implementation:
        code = code.strip().replace("```python", "").replace("```", "").strip()
        return code

    def write_to_shared_folder(self, filename: str, content: str) -> None:
        with open(f"shared_folder/{filename}", "w") as f:
            f.write(content)

    def generate_tags(self, code: str) -> list:
        # Implement tag generation logic based on the requirements or specifications
        return []

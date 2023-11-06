import os
from abc import ABC, abstractmethod
from typing import Optional, List

from lanarky.responses import StreamingResponse
from langchain.chat_models.base import BaseChatModel

from reworkd_platform.db.crud.oauth import OAuthCrud
from reworkd_platform.schemas.user import UserBase


class Tool(ABC):
    """
    The Tool class is an abstract base class that provides a blueprint for creating different types of tools.
    Each tool has a description, a public description, an argument description, and an image URL.
    The class also contains a model and a language attribute, which are initialized in the constructor.
    The class provides methods to check if a tool is available, to write and read from a shared folder, 
    to check if a code is relevant to a task, and to generate tags for a code.
    """
    description: str = ""
    public_description: str = ""
    arg_description: str = "The argument to the function."
    image_url: str = "/tools/openai-white.png"

    model: BaseChatModel
    language: str

    def __init__(self, model: BaseChatModel, language: str):
        self.model = model
        self.language = language

    @staticmethod
    def available() -> bool:
        return True

    @staticmethod
    async def dynamic_available(user: UserBase, oauth_crud: OAuthCrud) -> bool:
        return True

    @abstractmethod
    async def call(
        self,
        goal: str,
        task: str,
        input_str: str,
        user: UserBase,
        oauth_crud: OAuthCrud,
    ) -> StreamingResponse:
        pass

    def read_from_shared_folder(self, file_name: str) -> str:
        with open(f'SharedFolder/{file_name}', 'r') as file:
            return file.read()

    def write_to_shared_folder(self, file_name: str, content: str) -> None:
        if os.path.exists(f'SharedFolder/{file_name}'):
            version = 1
            while os.path.exists(f'SharedFolder/{file_name}_{version}'):
                version += 1
            file_name = f'{file_name}_{version}'
        with open(f'SharedFolder/{file_name}', 'w') as file:
            file.write(content)

    def is_code_relevant(self, code: str, task: str) -> bool:
        keywords = task.split(' ')
        for keyword in keywords:
            if keyword not in code:
                return False
        return True

    def generate_tags(self, code: str) -> List[str]:
        function_name = # This line extracts the function name from the code
        parameters = # This line extracts the parameters from the code
        summary = # This line generates a one-sentence summary of the code
        return [function_name, parameters, summary]
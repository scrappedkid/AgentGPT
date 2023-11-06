import os
from abc import ABC, abstractmethod
from typing import Optional, List

from lanarky.responses import StreamingResponse
from langchain.chat_models.base import BaseChatModel

from reworkd_platform.db.crud.oauth import OAuthCrud
from reworkd_platform.schemas.user import UserBase


class Tool(ABC):
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
        """
        Reads and returns the content of a file from a shared folder, given the file name.
        """
        with open(f'SharedFolder/{file_name}', 'r') as file:
            return file.read()

    def write_to_shared_folder(self, file_name: str, content: str) -> None:
        """
        Writes content to a file in a shared folder, given the file name and content. 
        If a file with the same name already exists, the method will create a new file 
        with a version number appended to the name.
        """
        if os.path.exists(f'SharedFolder/{file_name}'):
            version = 1
            while os.path.exists(f'SharedFolder/{file_name}_{version}'):
                version += 1
            file_name = f'{file_name}_{version}'
        with open(f'SharedFolder/{file_name}', 'w') as file:
            file.write(content)

    def is_code_relevant(self, code: str, task: str) -> bool:
        """
        Checks if all keywords from a task are present in a given code string and 
        returns a boolean value.
        """
        keywords = task.split(' ')
        for keyword in keywords:
            if keyword not in code:
                return False
        return True

    def generate_tags(self, code: str) -> List[str]:
        """
        Generates and returns a list of tags for a given code string, including the 
        function name, parameters, and a one-sentence summary of the code.
        """
        function_name = # extract function name from code
        parameters = # extract parameters from code
        summary = # generate a one-sentence summary of the code
        return [function_name, parameters, summary]
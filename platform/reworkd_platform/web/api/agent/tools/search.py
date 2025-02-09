from typing import Any, List
from urllib.parse import quote

import aiohttp
from aiohttp import ClientResponseError
from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from loguru import logger

from reworkd_platform.settings import settings
from reworkd_platform.web.api.agent.stream_mock import stream_string
from reworkd_platform.web.api.agent.tools.reason import Reason
from reworkd_platform.web.api.agent.tools.tool import Tool
from reworkd_platform.web.api.agent.tools.utils import (
    CitedSnippet,
    summarize_with_sources,
)

# Search google via serper.dev. Adapted from LangChain
# https://github.com/hwchase17/langchain/blob/master/langchain/utilities


async def _google_serper_search_results(
    search_term: str, search_type: str = "search"
) -> dict[str, Any]:
    headers = {
        "X-API-KEY": settings.serp_api_key or "",
        "Content-Type": "application/json",
    }
    params = {
        "q": search_term,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
                    f"https://google.serper.dev/{search_type}", headers=headers, params=params
                ) as response:
            response.raise_for_status()
            return await response.json()


class Search(Tool):
    description = (
        "Search Google for short up to date searches for simple questions about public information "
        "news and people.\n"
    )
    public_description = "Search google for information about current events."
    arg_description = "The query argument to search for. This value is always populated and cannot be an empty string."
    image_url = "/tools/google.png"

    @staticmethod
    def available() -> bool:
        return settings.serp_api_key is not None and settings.serp_api_key != ""

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        try:
            return await self._call(goal, task, input_str, *args, **kwargs)
        except ClientResponseError:
            logger.exception("Error calling Serper API, falling back to reasoning")
            return await Reason(self.model, self.language).call(
                goal, task, input_str, *args, **kwargs
            )

    async def _call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        results = await _google_serper_search_results(
            input_str,
        )

        k = 5  # Number of results to return
        snippets: List[CitedSnippet] = []

        if results.get("answerBox"):
            answer_values = []
            answer_box = results.get("answerBox", {})
            if answer_box.get("answer"):
                answer_values.append(answer_box.get("answer"))
            elif answer_box.get("snippet"):
                answer_values.append(answer_box.get("snippet").replace("\n", " "))
            elif answer_box.get("snippetHighlighted"):
                answer_values.append(", ".join(answer_box.get("snippetHighlighted")))

            if answer_values:
                return stream_string("\n".join(answer_values), True)
        for i, result in enumerate(results["organic"][:k]):
            texts = []
            link = ""
            if "snippet" in result:
                texts.append(result["snippet"])
            if "link" in result:
                link = result["link"]
            texts.extend(
                f"{attribute}: {value}."
                for attribute, value in result.get("attributes", {}).items()
            )

            snippets.append(CitedSnippet(i + 1, "\n".join(texts), link))

        if not snippets:
            return stream_string("No good Google Search Result was found", True)

        return summarize_with_sources(self.model, self.language, goal, task, snippets)

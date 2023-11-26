from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from pydantic import BaseModel
from reworkd_platform.schemas.agent import (AgentChat, AgentRun,
                                            AgentSummarize, AgentTaskAnalyze,
                                            AgentTaskCreate, AgentTaskExecute,
                                            NewTasksResponse)
from reworkd_platform.web.api.agent.agent_service.agent_service import \
    AgentService
from reworkd_platform.web.api.agent.agent_service.agent_service_provider import \
    get_agent_service
from reworkd_platform.web.api.agent.analysis import Analysis
from reworkd_platform.web.api.agent.dependancies import (
    agent_analyze_validator, agent_chat_validator, agent_create_validator,
    agent_execute_validator, agent_start_validator, agent_summarize_validator)
from reworkd_platform.web.api.agent.tools.tools import (get_external_tools,
                                                        get_tool_name)

router = APIRouter()


start_tasks_req_body = Depends(agent_start_validator)
start_tasks_agent_service = Depends(get_agent_service(agent_start_validator))

@router.post("/start")
async def start_tasks(
    req_body: AgentRun = start_tasks_req_body,
    agent_service: AgentService = start_tasks_agent_service,
) -> NewTasksResponse:
    new_tasks = await agent_service.start_goal_agent(goal=req_body.goal)
    return NewTasksResponse(newTasks=new_tasks, run_id=req_body.run_id)


@router.post("/analyze")
analyze_tasks_agent_service = Depends(get_agent_service(agent_analyze_validator))

@router.post("/analyze")
async def analyze_tasks(
    req_body: AgentTaskAnalyze = analyze_tasks_req_body,
    agent_service: AgentService = analyze_tasks_agent_service,
) -> Analysis:
    return await agent_service.analyze_task_agent(
        goal=req_body.goal,
        task=req_body.task or "",
        tool_names=req_body.tool_names or [],
    )


@router.post("/execute")
execute_tasks_agent_service = Depends(get_agent_service(validator=agent_execute_validator, streaming=True))

@router.post("/execute")
async def execute_tasks(
    req_body: AgentTaskExecute = execute_tasks_req_body,
    agent_service: AgentService = execute_tasks_agent_service,
) -> FastAPIStreamingResponse:
    return await agent_service.execute_task_agent(
        goal=req_body.goal or "",
        task=req_body.task or "",
        analysis=req_body.analysis,
    )


@router.post("/create")
create_tasks_agent_service = Depends(get_agent_service(agent_create_validator))

@router.post("/create")
async def create_tasks(
    req_body: AgentTaskCreate = create_tasks_req_body,
    agent_service: AgentService = create_tasks_agent_service,
) -> NewTasksResponse:
    new_tasks = await agent_service.create_tasks_agent(
        goal=req_body.goal,
        tasks=req_body.tasks or [],
        last_task=req_body.last_task or "",
        result=req_body.result or "",
        completed_tasks=req_body.completed_tasks or [],
    )
    return NewTasksResponse(newTasks=new_tasks, run_id=req_body.run_id)


@router.post("/summarize")
summarize_agent_service = Depends(get_agent_service(validator=agent_summarize_validator, streaming=True, llm_model="gpt-3.5-turbo-16k"))

@router.post("/summarize")
async def summarize(
    req_body: AgentSummarize = summarize_req_body,
    agent_service: AgentService = summarize_agent_service,
) -> FastAPIStreamingResponse:
    return await agent_service.summarize_task_agent(
        goal=req_body.goal or "",
        results=req_body.results,
    )


@router.post("/chat")
chat_agent_service = Depends(get_agent_service(validator=agent_chat_validator, streaming=True, llm_model="gpt-3.5-turbo-16k"))

@router.post("/chat")
async def chat(
    req_body: AgentChat = chat_req_body,
    agent_service: AgentService = chat_agent_service,
) -> FastAPIStreamingResponse:
    return await agent_service.chat(
        message=req_body.message,
        results=req_body.results,
    )


@router.patch("/tasks/{task_id}/status")

@router.patch("/tasks/{task_id}/status")
async def update_task_status(
    task_id: str,
    status: str,
    agent_service: AgentService = update_task_status_agent_service,
) -> dict:
    updated_task = await agent_service.update_task_status(task_id, status)
    return {"updated_task": updated_task}


class ToolModel(BaseModel):
    name: str
    description: str
    color: str
    image_url: Optional[str]


class ToolsResponse(BaseModel):
    tools: List[ToolModel]


@router.get("/tools")
async def get_user_tools() -> ToolsResponse:
    tools = get_external_tools()
    formatted_tools = [
        ToolModel(
            name=get_tool_name(tool),
            description=tool.public_description,
            color="TODO: Change to image of tool",
            image_url=tool.image_url,
        )
        for tool in tools
        if tool.available()
    ]

    return ToolsResponse(tools=formatted_tools)
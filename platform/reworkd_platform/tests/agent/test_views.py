import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from reworkd_platform.schemas.agent import AgentTaskCreate, NewTasksResponse
from reworkd_platform.web.api.agent.views import (app, create_tasks,
                                                  get_user_tools)
from reworkd_platform.web.api.agent.views import router as agent_router


class TestCreateTasks(TestCase):
    @patch("reworkd_platform.web.api.agent.views.get_agent_service")
    @patch("reworkd_platform.web.api.agent.views.agent_create_validator")
    @patch(
        "reworkd_platform.web.api.agent.agent_service.agent_service.AgentService.create_tasks_agent"
    )
    async def test_create_tasks(
        self,
        mock_create_tasks_agent,
        mock_agent_create_validator,
        mock_get_agent_service,
    ):
        # Arrange
        mock_agent_create_validator.return_value = AgentTaskCreate(
            goal="test_goal",
            tasks=["task1", "task2"],
            last_task="last_task",
            result="result",
            completed_tasks=["completed_task1", "completed_task2"],
            run_id="run_id",
        )
        mock_get_agent_service.return_value = MagicMock()
        mock_create_tasks_agent.return_value = ["new_task1", "new_task2"]

        # Act
        response = await create_tasks()

        # Assert
        self.assertIsInstance(response, NewTasksResponse)
        self.assertEqual(response.newTasks, ["new_task1", "new_task2"])
        self.assertEqual(response.run_id, "run_id")

    @patch("reworkd_platform.web.api.agent.views.get_agent_service")
    @patch("reworkd_platform.web.api.agent.views.agent_create_validator")
    @patch(
        "reworkd_platform.web.api.agent.agent_service.agent_service.AgentService.create_tasks_agent"
    )
    async def test_create_tasks_exception(
        self,
        mock_create_tasks_agent,
        mock_agent_create_validator,
        mock_get_agent_service,
    ):
        # Arrange
        mock_agent_create_validator.return_value = AgentTaskCreate(
            goal="test_goal",
            tasks=["task1", "task2"],
            last_task="last_task",
            result="result",
            completed_tasks=["completed_task1", "completed_task2"],
            run_id="run_id",
        )
        mock_get_agent_service.return_value = MagicMock()
        mock_create_tasks_agent.side_effect = Exception("Test exception")

        # Act and Assert
        with self.assertRaises(Exception) as context:
            await create_tasks()
        self.assertTrue("Test exception" in str(context.exception))


class TestAgentViews(TestCase):
    def setUp(self):
        self.client = TestClient(agent_router)

    @patch(
        "reworkd_platform.web.api.agent.agent_service.agent_service.AgentService.summarize_task_agent"
    )
    @patch("reworkd_platform.web.api.agent.dependancies.agent_summarize_validator")
    def test_summarize(self, mock_agent_summarize_validator, mock_summarize_task_agent):
        mock_agent_summarize_validator.return_value.goal = "mock goal"
        mock_agent_summarize_validator.return_value.results = "mock results"
        mock_summarize_task_agent.return_value = "mock response"

        response = self.client.post(
            "/summarize", json={"goal": "mock goal", "results": "mock results"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "mock response")

    @patch(
        "reworkd_platform.web.api.agent.agent_service.agent_service.AgentService.summarize_task_agent"
    )
    @patch("reworkd_platform.web.api.agent.dependancies.agent_summarize_validator")
    def test_summarize_exception(
        self, mock_agent_summarize_validator, mock_summarize_task_agent
    ):
        mock_agent_summarize_validator.return_value.goal = "mock goal"
        mock_agent_summarize_validator.return_value.results = "mock results"
        mock_summarize_task_agent.side_effect = Exception("mock exception")

        response = self.client.post(
            "/summarize", json={"goal": "mock goal", "results": "mock results"}
        )

        self.assertEqual(response.status_code, 500)
        self.assertIn("mock exception", response.text)


class TestGetUserTools(TestCase):
    @patch("reworkd_platform.web.api.agent.tools.tools.get_external_tools")
    def test_get_user_tools(self, mock_get_external_tools):
        mock_tool = MagicMock()
        mock_tool.available.return_value = True
        mock_tool.public_description = "mock description"
        mock_tool.image_url = "mock image url"
        mock_get_external_tools.return_value = [mock_tool]

        response = get_user_tools()

        self.assertEqual(len(response.tools), 1)
        self.assertEqual(response.tools[0].description, "mock description")
        self.assertEqual(response.tools[0].image_url, "mock image url")

    @patch("reworkd_platform.web.api.agent.tools.tools.get_external_tools")
    def test_get_user_tools_with_no_tools(self, mock_get_external_tools):
        mock_get_external_tools.return_value = []

        response = get_user_tools()

        self.assertEqual(len(response.tools), 0)


class TestStartTasks(TestCase):
    @patch("current_module.agent_start_validator")
    @patch("current_module.get_agent_service")
    @patch("agent_service.AgentService.start_goal_agent")
    def test_start_tasks(
        self, mock_start_goal_agent, mock_get_agent_service, mock_agent_start_validator
    ):
        mock_req_body = MagicMock()
        mock_req_body.goal = "mock goal"
        mock_req_body.run_id = "mock run_id"
        mock_agent_start_validator.return_value = mock_req_body

        mock_agent_service = MagicMock()
        mock_get_agent_service.return_value = mock_agent_service

        mock_start_goal_agent.return_value = "mock new_tasks"

        client = TestClient(app)
        response = client.post(
            "/start_tasks", json={"goal": "mock goal", "run_id": "mock run_id"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"newTasks": "mock new_tasks", "run_id": "mock run_id"}
        )

    @patch("current_module.agent_start_validator")
    @patch("current_module.get_agent_service")
    @patch("agent_service.AgentService.start_goal_agent")
    def test_start_tasks_exception_handling(
        self, mock_start_goal_agent, mock_get_agent_service, mock_agent_start_validator
    ):
        mock_req_body = MagicMock()
        mock_req_body.goal = "mock goal"
        mock_req_body.run_id = "mock run_id"
        mock_agent_start_validator.return_value = mock_req_body

        mock_agent_service = MagicMock()
        mock_get_agent_service.return_value = mock_agent_service

        mock_start_goal_agent.side_effect = Exception("mock exception")

        client = TestClient(app)
        response = client.post(
            "/start_tasks", json={"goal": "mock goal", "run_id": "mock run_id"}
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.json(), {"detail": "An error occurred while starting tasks."}
        )


from sqlalchemy import DateTime, String, Text, func, Column
from sqlalchemy.orm import mapped_column

from reworkd_platform.db.base import Base


class AgentRun(Base):
    __tablename__ = "agent_run"

    user_id = mapped_column(String, nullable=False)
    goal = mapped_column(Text, nullable=False)
    create_date = mapped_column(
        DateTime, name="create_date", server_default=func.now(), nullable=False
    )


class AgentTask(Base):
    __tablename__ = "agent_task"

    run_id = Column(String, nullable=False)
    type_ = Column(String, nullable=False, name="type")
    result = Column(Text, nullable=True)  # Store the outcome of the task
    create_date = Column(
        DateTime, name="create_date", server_default=func.now(), nullable=False
    )
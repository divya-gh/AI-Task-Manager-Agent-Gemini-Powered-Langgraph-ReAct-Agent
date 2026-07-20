from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# -----------------------------
# User Profile
# -----------------------------
class UserProfile(BaseModel):

    user_name: Optional[str] = Field(
        default="User",
        description="Preferred name of the user"
    )

    age: Optional[int] = Field(
        default=None,
        description="Age of the user"
    )

    location: Optional[str] = Field(
        default=None,
        description="Where the user lives"
    )

    job: Optional[str] = Field(
        default=None,
        description="The user's job"
    )

    connections: list[str] = Field(
        default_factory=list,
        description="Family, friends, coworkers, etc."
    )

    interests: list[str] = Field(
        default_factory=list,
        description="User interests, likes, loves, wants, hobbies"
    )


# -----------------------------
# Todo Memory
# -----------------------------
class ToDo(BaseModel):

    task: str = Field(
        description="Task to complete"
    )

    time_taken: Optional[str] = Field(
        default=None,
        description="Estimated time such as '30 minutes' or '2 hours'"
    )

    deadline: Optional[str] = Field(
        default=None,
        description="Deadline in ISO format when possible (YYYY-MM-DD or ISO datetime)"
    )

    instruction: Optional[str] = Field(
        default=None,
        description="User instructions for completing the task"
    )

    desired_solution: Optional[str] = Field(
        default=None,
        description="Desired outcome"
    )

    status: Literal[
        "not started",
        "in progress",
        "done",
        "archived"
    ] = Field(default="not started")


# -----------------------------
# Instruction Memory
# -----------------------------
class LLM_Instructions(BaseModel):

    instructions: str = Field(
        description="Instructions for managing the todo list"
    )
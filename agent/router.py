

from typing import Literal
from langgraph.graph import END
from langgraph.store.base import BaseStore
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState
from agent.nodes import LLM_chatbot, update_profile, agent_learning_resoning, todo_update



# define router node
def router(state: MessagesState) -> str:
    ''' based on the tool call route the workflow to proper node'''

    last = state["messages"][-1]

    if not last.tool_calls:
        return END

    tool = last.tool_calls[0]["name"]

    if tool == "search_tavily":
        return "search_tavily"

    if tool == "Updatememory":

        update = last.tool_calls[0]["args"]["update_type"]

        if update == "update_profile":
            return "update_profile"

        if update == "todo_update":
            return "todo_update"

        if update == "agent_learning_resoning":
            return "agent_learning_resoning"

    return END



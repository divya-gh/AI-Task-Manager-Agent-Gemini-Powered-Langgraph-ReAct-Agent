

from typing import Literal
from langgraph.graph import END
from langgraph.store.base import BaseStore
from langchain_core.runnables import RunnableConfig
from langgraph.graph import MessagesState
from agent.nodes import LLM_chatbot, update_profile, agent_learning_resoning, todo_update



# define router node
def router(state: MessagesState) -> str:
    ''' based on the tool call route the workflow to proper node'''

    # get tool message
    tool_message = state['messages'][-1]    
    #print("Tool Call: ",tool_message)

    # No tool call → go back to chatbot
    if not tool_message.tool_calls:
        return END
    
    else:
        # get tool calls
        tool_calls = tool_message.tool_calls[0]
        if tool_calls['args']['update_type'] == 'update_profile':
            print("6. PROFILE")
            return 'update_profile'
        elif tool_calls['args']['update_type'] == 'todo_update':
            print("6. TODO")
            return 'todo_update'
        elif tool_calls['args']['update_type'] == 'agent_learning_resoning':
            print("6. REASONING")
            return 'agent_learning_resoning'
        else:
            raise ValueError("Unknown update_type") 




from langgraph.graph import MessagesState ,StateGraph, START, END
from agent.nodes import LLM_chatbot, agent_learning_resoning , update_profile, todo_update
from agent.memory_store import session_memory , store_memory
from agent.router import router


workflow = StateGraph(MessagesState)

# add nodes
workflow.add_node('LLM_chatbot' , LLM_chatbot)
workflow.add_node('update_profile' , update_profile)
workflow.add_node('todo_update' , todo_update)
workflow.add_node('agent_learning_resoning' , agent_learning_resoning)

# add flow
workflow.add_edge(START, 'LLM_chatbot')
workflow.add_conditional_edges('LLM_chatbot', router)
workflow.add_edge('update_profile' , 'LLM_chatbot')
workflow.add_edge('todo_update' , 'LLM_chatbot')
workflow.add_edge('agent_learning_resoning' , 'LLM_chatbot')
workflow.add_edge('LLM_chatbot', END)



# compile graph
graph = workflow.compile(checkpointer=session_memory , store=store_memory)




import os
from dotenv import load_dotenv
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict , Literal , Optional
from pydantic import BaseModel, Field
import streamlit as st


load_dotenv()
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = st.secrets.get("TAVILY_API_KEY") or os.getenv("TAVILY_API_KEY")


os.environ["GOOGLE_API_USE_V1"] = "true"

# create genai client and llm
client = genai.Client(api_key = GOOGLE_API_KEY)

# create a llm using any of the above models
llm = ChatGoogleGenerativeAI( model= "gemini-3.1-flash-lite-preview" , 
                              temperature = 0.2 )

#llm.invoke("What day is this?").content

# 1. define a router class to select type of memory to update in the function
class Updatememory(TypedDict):
    update_type : Literal['update_profile', 'todo_update', 'agent_learning_resoning']

# Tavily seach class
class search_tavily(BaseModel):
    search_query: str = Field(
        description=" LLM generated seach query for Tavily search engine"
        )



# bind the class a stool to LLM
llm_with_tool = llm.bind_tools([Updatememory], search_tavily)

#------------------------------------------------------------
#Configure Tavily
#-----------------------------------------------------------

from tavily import TavilyClient
tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])


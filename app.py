from altair import value
import streamlit as st
#from streamlit_chat import message
from datetime import datetime

from agent.graph import graph
from agent.memory_store import store_memory
from agent.HTML_todo_dashboard import render_html_dashboard
from agent.HTML_patch_viewer import render_patch_html
from langchain_core.messages import HumanMessage, AIMessage
import random

st.set_page_config(page_title="My Task Manager — Gemini LangGraph Agent", layout="wide")

# -------------------------------
# LOGIN SCREEN (Centered & Professional)
# -------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if st.session_state.user_id == "":
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(
            "<h1 style='text-align: center;'>👋 Welcome to Your AI Task Manager</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; font-size:19px;'>Please enter your name to begin.</p>",
            unsafe_allow_html=True
        )

        with st.form("login_form"):

            st.markdown(
                "<label style='font-size:18px; font-weight:600;'>Your Name:</label>",
                unsafe_allow_html=True
            )

            name = st.text_input(
                "Your Name",
                key="login_name",
                placeholder="Type your name here...",
                label_visibility="collapsed"
            )

            submitted = st.form_submit_button(
                "🚀 Start",
                use_container_width=True
            )

        if submitted:
            if name.strip():
                st.session_state.user_id = name.strip()
                st.rerun()

    st.stop()

# -------------------------------
# Sidebar Navigation
# -------------------------------
with st.sidebar:
    st.header("📌 Navigation")
    page = st.radio("Go to:", 
        [        
        "💬 Chat",
        "📋 Task Dashboard",
        "🧠 Memory Store",
        "🔍 Agent Learning & Reasoning"
        ])

user_id = str(st.session_state.user_id)
config = {"configurable": {"thread_id": user_id, "user_id": user_id}}


# ✅ DEBUG (place here)
#st.write("DEBUG: page loaded")
#st.write("DEBUG history:", st.session_state.get("history", []))

# -------------------------------
# Global Session State Initialization
# -------------------------------

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "patches" not in st.session_state:
    st.session_state.patches = None

if "processing" not in st.session_state:
    st.session_state.processing = False

# Wrapper for Streamlit
# -------------------------------
def run_agent_streamlit(user_message):

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=user_message)
            ]
        },
        config=config
    )
    #print("result:", result)
    
    return (
        result["messages"]
    )

# -------------------------------
# Chat Page
# -------------------------------
if page == "💬 Chat":

    # -------------------------
    # Add Markdown for Instructions
    # -------------------------
    st.markdown("""
                        <style>

                        .hero-title {
                            font-size: 33px;
                            font-weight: 700;
                            color: #EAEAEA;
                            margin-bottom: 8px;
                        }

                        .hero-subtitle {
                            font-size: 16px;
                            color: #C0C0C0;
                            margin-bottom: 21px;
                            line-height: 1.6;
                        }

                        .section-header {
                            font-size: 21px;
                            font-weight: 800;
                            color: #D6D6D6;
                            margin-top: 20px;
                            margin-bottom: 12px;
                        }


                        .feature-card {

                            background-color:#2B2B2B;

                            padding:15px 14px;

                            border-radius:9px;

                            margin-bottom:4px;

                            border-left:5px solid #8A8A8A;

                        }


                        .feature-title {

                            font-size:18px;
                            font-weight:600;
                            color:#F0F0F0;

                        }

                        .feature-text {

                            font-size:15px;
                            color:#D0D0D0;
                            margin-top:6px;
                            line-height:1.5;

                        }


                        .nav-box {

                            background-color:#333333;

                            padding:10px;

                            border-radius:10px;

                            margin-top:7px;

                            color:#E5E5E5;

                        }


                        .ready-box {
                            background-color:#3B3B3B;
                            padding:10px 15px;
                            border-radius:10px;
                            margin-top:5px;
                            margin-bottom:-25px;
                            color:#E5E5E5;
                            text-align:center;
                            font-size:19px;
                            font-weight:700;
                            line-height:1;
                        }


                        /* Pull chat input closer */
                        div[data-testid="stChatInput"] {
                            margin-top:-20px;
                        }
                
                        </style>
                        <div class="hero-title">

                        🧠 Your Personal AI Task Manager Agent

                        </div>

                        <div class="hero-subtitle">

                        An intelligent productivity partner powered by Gemini + LangGraph.<br>
                        More than a simple to-do list, I'm an AI-powered productivity partner that learns how you work, adapts to your preferences, and helps you stay organized and focused.

                        </div>

                        <div class="section-header">
                        🚀 Agent Capabilities
                        </div>

                        <div class="feature-card">
                        <div class="feature-title">

                        ✅ Autonomous Task Management

                        </div>

                        <div class="feature-text">
                        Create, update, prioritize, organize, and track tasks through natural conversation.
                        </div>
                        </div>

                        <div class="feature-card">
                        <div class="feature-title">

                        🧠 Long-Term Memory

                        </div>
                        <div class="feature-text">
                        Learns your preferences, goals, interests, and working style to provide personalized assistance.

                        </div>
                        </div>

                        <div class="feature-card">
                        <div class="feature-title">

                        📝 Intelligent Planning & Reasoning

                        </div>
                        <div class="feature-text">
                        Breaks complex goals into actionable steps, identifies missing information,
                        and recommends next actions.

                        </div>
                        </div>

                        <div class="feature-card">
                        <div class="feature-title">

                        🤝 Human-in-the-Loop Control

                        </div>

                        <div class="feature-text">
                        Keeps you in control by allowing review and approval before important decisions.

                        </div>
                        </div>

                        <div class="feature-card">
                        <div class="feature-title">
                        🔍 Transparent AI Operations

                        </div>

                        <div class="feature-text">
                        Understand how the agent works through memory visibility and tool execution tracking.

                        </div>
                        </div>
                        <div class="nav-box">
                        <b>Explore Your AI Workspace</b><br>
                          📋 <b>Task Dashboard</b> — Manage your active goals and tasks<br>
                          🧠 <b>Memory Store</b> — View what your AI assistant remembers<br>
                          🔍 <b>Patch Viewer</b> — Inspect agent actions and decisions
                        </div>

                        <div class="ready-box">

                        💬 Ready to collaborate with your AI assistant?
                        <br><br>
                        Ask me about your tasks, goals, projects, travel plans, learning objectives, or anything you'd like help organizing.
                        </div>
                        """, unsafe_allow_html=True)

    # -------------------------
    # Display Previous Messages
    # -------------------------
    for role, message in st.session_state.history:
        with st.chat_message(role):
            st.markdown(message)

    # -------------------------
    # Chat Input
    # -------------------------

    examples = [
        "EX: I'm planning a trip to London this Saturday, I love coffee. Suggest places to visit.",
        "I need to renew my passport before July 31st.",
        "My next meeting with the team is on Friday at 3 PM. Can you remind me?",
        "What's in my agenda for today?",
        "When is my next meeting with the team?",
        "Organize my tasks by priority and deadline."
    ]

    st.caption(
    "💡 Try asking: " + random.choice(examples)
    
    )

    prompt = st.chat_input(
    "What can i do for you?",
    disabled=st.session_state.processing
    )
    #st.write("DEBUG prompt:", repr(prompt))

    if prompt:

        st.session_state.processing = True

        st.session_state.history.append(
            ("user", prompt)
        )

        with st.chat_message("user"):
            st.markdown(prompt)


        try:

            with st.spinner("🤖 Thinking..."):

                response= run_agent_streamlit(prompt)


            final_msg = "⚠️ No response generated."


            for msg in reversed(response):

                if isinstance(msg, AIMessage):

                    if isinstance(msg.content, str):

                        final_msg = (
                            msg.content
                            .replace("AI_response:", "")
                            .strip()
                        )

                        break


            with st.chat_message("assistant"):

                st.markdown(final_msg)


            st.session_state.history.append(
                ("assistant", final_msg)
            )

        except Exception as e:
            st.exception(e)

        finally:
            st.session_state.processing = False



# -------------------------------
# Task Dashboard Page
# -------------------------------
elif page == "📋 Task Dashboard":
    st.subheader("📋 Task Dashboard")
    #----------------------------
    # Show all tasks toggle
    #----------------------------

    st.markdown(
    """
    <style>
    /* Toggle label */
    div[data-testid="stToggle"] label {
        font-size: 16px;
        font-weight: 600;
    }

    /* Toggle ON color */
    div[data-testid="stToggle"] div[role="switch"][aria-checked="true"] {
        background-color: #2e7d32 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    show_all = st.toggle(
        "📚 Show All Tasks",
        value=False
    )

    html = render_html_dashboard(
        user_id,
        store_memory,
        #show_all=show_all
    )

    if show_all:
        scrolling = True
    else:
        scrolling = False

    st.components.v1.html(
        html,
        height=800,
        scrolling=scrolling
    )

# -------------------------------
# Memory Store Page
# -------------------------------
elif page == "🧠 Memory Store":
    st.subheader("🧠 Long‑Term Memory Store")

    namespaces = [
        ("UserProfile", user_id),
        ("ToDo", user_id)
    ]

    for ns in namespaces:
        st.markdown(f"### 📌 Store: `{ns[0]}` — User: `{ns[1]}`")
        items = store_memory.search(ns)

        if not items:
            st.info("No memory found.")
            continue

        for m in items:
            st.json(m.value)

# -------------------------------
# Agent Learning & Reasoning Viewer
# -------------------------------
elif page == "🔍 Agent Learning & Reasoning":

    st.title("🔬 Agent Learning & Reasoning")

    st.caption(
        "🌟 View how the AI agent interpreted your request, learned from the conversation, "
        "updated long-term memory, and planned its next actions."
    )

    namespace = ("reasoning_memory", user_id)

    memory_items = store_memory.search(namespace)
    if not memory_items:
        st.info(
            "No reasoning available yet. Start chatting with the AI assistant to see its learning and reasoning process."
        )
    else:
        latest_memory = memory_items[-1]
        st.markdown(latest_memory.value["reasoning_summary"], unsafe_allow_html=True)
    

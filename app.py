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
        st.markdown("<h1 style='text-align: center;'>👋 Welcome to Your AI Task Manager</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size:19px;'>Please enter your name to begin.</p>", unsafe_allow_html=True)

        st.markdown(
            "<label style='font-size: 18px; font-weight: 600;'>Your Name:</label>",
            unsafe_allow_html=True
        )

        name = st.text_input(
            "Your Name",
            key="login_name",
            placeholder="Type your name here...",
            label_visibility="collapsed"
        )


        st.write("")
        st.write("")

        if st.button("Start", use_container_width=True):
            if name.strip():
                st.session_state.user_id = name.strip()
                st.rerun()

    st.stop()

# -------------------------------
# Sidebar Navigation
# -------------------------------
with st.sidebar:
    st.header("📌 Navigation")
    page = st.radio("Go to:", ["Chat", "Task Dashboard", "Memory Store", "Patch Viewer"])

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

    return (
        result["messages"],
        result.get("patches")
    )

# -------------------------------
# Chat Page
# -------------------------------
if page == "Chat":

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
                            padding:8px 12px;
                            border-radius:10px;
                            margin-top:5px;
                            margin-bottom:-25px;
                            color:#E5E5E5;
                            text-align:center;
                            font-size:16px;
                            font-weight:600;
                            line-height:1.3;
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
                        <br>
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
        "EX: Plan my trip to London this Saturday. I love coffee. Suggest places to visit and remind me when I arrive.",
        "Remind me to renew my passport before July 31st.",
        "Help me create a study plan for Ethics in AI.",
        "Track my job applications and suggest next steps.",
        "I need to book a dental cleaning appointment tomorrow at 2 PM.",
        "Organize my tasks by priority and deadline."
    ]

    st.caption(
    "💡 Try asking: " + random.choice(examples)
    
    )

    prompt = st.chat_input(
    "What can i do for you?",
    disabled=st.session_state.processing
    )


    if prompt:

        st.session_state.processing = True

        st.session_state.history.append(
            ("user", prompt)
        )

        with st.chat_message("user"):
            st.markdown(prompt)


        try:

            with st.spinner("🤖 Thinking..."):

                response, patches = run_agent_streamlit(prompt)


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


            if patches:

                st.session_state.patches = patches


        except Exception as e:

            st.exception(e)


        finally:

            st.session_state.processing = False



# -------------------------------
# Task Dashboard Page
# -------------------------------
elif page == "Task Dashboard":
    st.subheader("📋 Task Dashboard")
    html = render_html_dashboard(user_id, store_memory)
    st.components.v1.html(html, height=600, scrolling=True)

# -------------------------------
# Memory Store Page
# -------------------------------
elif page == "Memory Store":
    st.subheader("🧠 Long‑Term Memory Store")

    namespaces = [
        ("UserProfile", user_id),
        ("ToDo", user_id),
        ("Instructions", user_id)
    ]

    for ns in namespaces:
        st.markdown(f"### 📌 Namespace: `{ns[0]}` — User: `{ns[1]}`")
        items = store_memory.search(ns)

        if not items:
            st.info("No memory found.")
            continue

        for m in items:
            st.json(m.value)

# -------------------------------
# Patch Viewer Page
# -------------------------------
elif page == "Patch Viewer":
    st.subheader("🔍 Patch Viewer (Tool Call Visibility)")
    if "patches" in st.session_state:
        html = render_patch_html(st.session_state.patches)
        st.components.v1.html(html, height=600, scrolling=True)
    else:
        st.info("No patches yet. Chat with the agent first.")

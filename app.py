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

    st.markdown("""
    <style>

    /* Background */
    .stApp{
        background:
            radial-gradient(circle at top left,#1e293b,#0f172a 40%,#020617 100%);
    }

    /* Make page narrower */
    .main .block-container{
        max-width:720px;
        padding-top:70px;
    }

    /* Glass card */
    div[data-testid="stVerticalBlock"]:has(form){
        background:rgba(255,255,255,0.08);
        backdrop-filter:blur(18px);
        border:1px solid rgba(255,255,255,.15);
        border-radius:24px;
        padding:35px;
        box-shadow:0 30px 80px rgba(0,0,0,.45);
    }

    /* Title */

    h1{
        
        color:#80ced6 !important;
        text-align:center;
        font-size:54px !important;
        margin-bottom:10px;
    }

    /* Subtitle */

    .subtitle{
        text-align:center;
        color:#d5f4e6;
        font-size:20px;
        margin-bottom:30px;
    }

    /* Input */

    div[data-testid="stTextInput"] input{
        background:#0f172a;
        color:white;
        border:1px solid #334155;
        border-radius:14px;
        height:56px;
        font-size:18px;
    }

    div[data-testid="stTextInput"] input:focus{
        border:2px solid #22c55e;
    }

    /* Button */

    div.stButton > button{
        width:100%;
        height:56px;
        border-radius:14px;
        background:linear-gradient(90deg,#22c55e,#16a34a);
        color:d5f4e6 !important;
        border:none;
        font-size:18px;
        font-weight:700;
    }

    div.stButton > button:hover{
        transform:translateY(-2px);
    }

    /* Hide Streamlit decoration */

    header{
        visibility:hidden;
    }

    #MainMenu{
        visibility:hidden;
    }

    footer{
        visibility:hidden;
    }

    </style>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1,2,1])

    with center:

        st.markdown("<h1> 🤖 AI Task Manager</h1>", unsafe_allow_html=True)

        st.markdown(
            "<p class='subtitle'>Your intelligent personal productivity assistant</p>",
            unsafe_allow_html=True,
        )
        st.write("")

        with st.form("login"):

                name = st.text_input(
                    "",
                    placeholder="👤 Enter your name...",
                    label_visibility="collapsed"
                )

                submitted = st.form_submit_button(
                    "🚀 Get Started",
                    use_container_width=True
                )

                if submitted:
                    if name.strip():
                        st.session_state.user_id = name.strip()
                        st.rerun()
                    else:
                        st.warning("Please enter your name.")

        st.markdown(
                            """
                            <div style="
                            text-align:center;
                            color:#94A3B8;
                            font-size:12px;
                            font: Times New Roman;                                                   
                            "> &nbsp;&nbsp&nbsp;&nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp&nbsp; Powered by
                            </div>
                            <div style="
                            text-align:center;
                            color:#94A3B8;
                            font-size:16px;
                            margin-top:2px;
                            "> &nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp 🧠 Gemini &nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp
                            🌐 Tavily Search &nbsp;&nbsp;
                            ⚡ LangGraph &nbsp;&nbsp&nbsp;&nbsp&nbsp;&nbsp
                            💾 Long-Term Memory
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

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
        "🌐 Search History",
        "🧠 Memory Store",
        "🔍 Agent Learning & Reasoning",
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
                            color: #80ced6;
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
                            color: #f4e1d2;
                            margin-top: 20px;
                            margin-bottom: 12px;
                        }


                        .feature-card {

                            background-color:#2B2B2B;

                            padding:18px 10px;

                            border-radius:9px;

                            margin-bottom:4px;

                            border-left:5px solid #8A8A8A;

                        }


                        .feature-title {

                            font-size:18px;
                            font-weight:600;
                            color:#d5f4e6;

                        }

                        .feature-text {

                            font-size:15px;
                            color:#D0D0D0;
                            margin-top:3px;
                            line-height:1;

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
                            padding:10px 20px;
                            border-radius:10px;
                            margin-top:20px;
                            margin-bottom:-10px;
                            color:#ADD8E6;
                            text-align:center;
                            font-size:17px;
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

                        More than a traditional to-do app, this AI agent understands your goals, remembers what matters, searches the web when needed, and helps you stay organized through natural conversation.

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
                        Remembers your preferences, goals, deadlines, and past conversations to personalize every interaction.

                        </div>
                        </div>
                        <div class="feature-card">
                        <div class="feature-title">
                        📝 Intelligent AI Planning & Reasoning

                        </div>
                        <div class="feature-text">
                        Breaks down complex goals, recommends next steps, and explains its reasoning transparently.

                        </div>
                        </div>
                        <div class="feature-card">
                        <div class="feature-title">
                        🌐 Live Web Search

                        </div>

                        <div class="feature-text">
                        Uses Tavily Search to retrieve current information whenever your question requires up-to-date answers.

                        </div>
                        </div>
                        <div class="feature-card">
                        <div class="feature-title">
                        🤝 Human-in-the-Loop Control

                        </div>

                        <div class="feature-text">
                        Keeps you in control by requesting approval before important actions or changes.

                        </div>
                        </div>
                        <div class="feature-card">
                        <div class="feature-title">
                        🔍 Transparent AI Operations

                        </div>

                        <div class="feature-text">
                        Inspect the agent's memory, reasoning process, and tool usage to understand how decisions are made..

                        </div>
                        </div>
                        <div class="nav-box">
                        <b>Explore Your AI Workspace</b><br>
                          📋 <b>Task Dashboard</b> — Manage your active goals and tasks<br>
                          🧠 <b>Memory Store</b> — View what your AI assistant remembers<br>
                          🔍 <b>Agent Learning & Reasoning</b> — Inspect agent actions and decisions<br>  
                          🌐 <b>Search History</b> — Review previous web searches
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
            "I'm planning a trip to London this Saturday. I love coffee—can you suggest some top-rated specialty coffee spots to visit?",
            "I need to renew my passport before July 31st. What steps do I need to take?",
            "Can you set a reminder for my next team meeting on Friday at 3:00 PM?",
            "What is on my agenda for today?",
            "Inform the team about the delivery meeting this evening at 4:30 PM, or let me know when my next meeting with the team is.",
            "Please organize all my active tasks by priority and upcoming deadlines.",
            "My niece is visiting this Friday—what are some fun, memorable activities we can do together?",
            "Create a project plan for launching a new website, break it into 4 sub-tasks with deadlines, and update my task dashboard."
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

    st.markdown("""
                <style>

                /* Label */
                div[data-testid="stToggle"] label{
                    font-size:16px;
                    font-weight:600;
                }

                /* Toggle track ON */
                div[data-testid="stToggle"] input:checked + div{
                    background-color:#00FF00 !important;
                }

                /* Toggle thumb */
                div[data-testid="stToggle"] div{
                    transition:all .2s ease;
                }

                </style>
                """, unsafe_allow_html=True)

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
        height=900,
        scrolling=scrolling
    )

#-----------------------------------
# Search History
#----------------------------------

elif page == "🌐 Search History":

    st.title("🌐 Search History")

    namespace = ("search_history", user_id)

    searches = store_memory.search(namespace)

    if not searches:
        st.info("No internet searches yet.")

    else:

        searches = sorted(
            searches,
            key=lambda x: x.value["DateTime"],
            reverse=True,
        )

        for item in searches:

            with st.expander(
                f"🔎 {item.value['Query']}",
                expanded=False,
            ):
                dt = datetime.fromisoformat(item.value["DateTime"])
                st.caption(dt.strftime("%b %d, %Y • %I:%M %p"))
                st.markdown("### Answer")
                st.write(item.value["Answer"])
                st.markdown(f"**Source:** {item.value['Cite']}")


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
        reasoning = latest_memory.value["reasoning_summary"]
        reasoning = reasoning.replace("####", "\n\n####")
        
        with st.expander("🧠 Agent Reasoning", expanded=True):
            st.markdown(reasoning)
    

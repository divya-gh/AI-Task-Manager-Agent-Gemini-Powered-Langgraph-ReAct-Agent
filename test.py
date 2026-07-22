import streamlit as st

st.title("Chat Input Test")

msg = st.chat_input("Type something")

st.write("msg =", repr(msg))

if msg:
    st.success(f"You typed: {msg}")


#save chat input:
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
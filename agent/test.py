import streamlit as st

st.title("Chat Input Test")

msg = st.chat_input("Type something")

st.write("msg =", repr(msg))

if msg:
    st.success(f"You typed: {msg}")
from typing import Set
import streamlit as st
from langchain.memory import ConversationBufferMemory
from backend.core import run_query  # Assuming this imports your query execution logic
from dotenv import load_dotenv

load_dotenv()

memory = ConversationBufferMemory(max_len=5)



st.header("LangChain🦜🔗 Chat with the Brain")

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

prompt = st.text_input("Prompt", placeholder="Enter your message here...") or st.button("Submit")

if prompt:
    st.session_state["user_prompt_history"].append(prompt)
    with st.spinner("Generating response..."):
        generated_response = run_query(query=prompt, memory=memory)
        #memory.save_context({'input':f'{prompt}'}, {'output': f'{generated_response[0]}'})
        memory.save_context({"input": f"{prompt}"}, {"output": f"{generated_response[0]}"})
        #st.write(memory)
        st.session_state["chat_answers_history"].append(generated_response)
        st.session_state["chat_history"].append((prompt, generated_response))

for user_prompt, generated_response in st.session_state["chat_history"]:
    st.write(f"Question: {user_prompt}")
    st.write(f"AI Answer: {generated_response[0]}")

# if prompt:
#     st.write(f"User: {st.session_state['user_prompt_history'][-1]}")
#     st.write(f"Bot: {st.session_state['chat_answers_history'][-1][0]}")

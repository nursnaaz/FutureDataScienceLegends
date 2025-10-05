from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import streamlit as st
from streamlit_chat import message
# loading the OpenAI api key from .env (OPENAI_API_KEY="sk-********")
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

st.set_page_config(
    page_title='Your Custom Assistant',
    page_icon='🤖'
)

st.subheader('Your Custom ChatGPT 🤖')

chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)

# Initialize the messages in the session state
if 'messages' not in st.session_state:
    st.session_state.messages = [SystemMessage(content='You are a helpful assistant.')]

# creating the sidebar
with st.sidebar:
    # streamlit text input widget for the system message (role)
    system_message = st.text_input(label='System role')
    # streamlit text input widget for the user message
    user_prompt = st.text_input(label='Send a message')
    
    if system_message:
        if not any(isinstance(x, SystemMessage) for x in st.session_state.messages):
            st.session_state.messages.append(
                SystemMessage(content=system_message)
            )
    
    if user_prompt:
        st.session_state.messages.append(
            HumanMessage(content=user_prompt)
        )
        with st.spinner('Working on your request ...'):
            # creating the ChatGPT response
            response = chat(st.session_state.messages)
        # adding the response's content to the session state
        st.session_state.messages.append(AIMessage(content=response.content))

# Display chat messages
if len(st.session_state.messages) > 1:
    for i, msg in enumerate(st.session_state.messages[1:]):
        if isinstance(msg, HumanMessage):
            message(msg.content, is_user=True, key=f'{i} + 🤓')  # user's question
        elif isinstance(msg, AIMessage):
            message(msg.content, is_user=False, key=f'{i} +  🤖')  # ChatGPT response
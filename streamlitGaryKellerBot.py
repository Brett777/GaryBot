import os
import datarobotx as drx
import pandas as pd
import streamlit as st
import requests
import openai
#prompt = "What is wholesale investing?"
deployment = drx.Deployment(deployment_id="6537cdc70bfca349f2b368f5")

#Configure the page title, favicon, layout, etc
st.set_page_config(page_title="Ask Gary")

# def createVectorStore():
#     from langchain.document_loaders import DirectoryLoader
#     from langchain.text_splitter import MarkdownTextSplitter
#     from langchain.embeddings.openai import OpenAIEmbeddings
#     from langchain.text_splitter import CharacterTextSplitter
#     from langchain.vectorstores import FAISS
#     Load the document, split it into chunks, embed each chunk and load it into the vector store.
    # loader = DirectoryLoader(r'Books', glob="**/*.pdf",show_progress=True)
    # data = loader.load()
    # splitter = MarkdownTextSplitter(
    #     chunk_size=2000,
    #     chunk_overlap=1000,
    # )
    # documents = splitter.split_documents(data)
    # db = FAISS.from_documents(documents, OpenAIEmbeddings())

def mainPage():
    container1 = st.container()
    col1, col2, col3 = container1.columns([1,3,1])
    container2 = st.container()
    col4, col5, col6, col7 = container2.columns([1.7,1,1,1])

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with col2:
        st.image("Keller-3.jpg")

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # Accept user input
    if prompt := st.chat_input("What is up?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            full_response += deployment.predict_unstructured(
                {
                    "question": prompt,
                    "openai_api_key": os.environ["OPENAI_API_KEY"],
                }
            )
            message_placeholder.markdown(full_response + "▌")
            st.session_state.messages.append({"role": "assistant", "content": full_response})

#Main app
def _main():
    hide_streamlit_style = """
    <style>
    # MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) # This let's you hide the Streamlit branding
    mainPage()

if __name__ == "__main__":
    _main()


def modelTest():
    API_URL = 'https://mlops.dynamic.orm.datarobot.com/predApi/v1.0/deployments/{deployment_id}/predictionsUnstructured'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': 'Bearer {}'.format(os.environ['DATAROBOT_API_TOKEN']),
        'DataRobot-Key': os.environ['DATAROBOT_KEY'],
    }
    data = {
            "question": "What is wholesale investing",
            "openai_api_key": os.environ["OPENAI_KEY"],
        }

    url = API_URL.format(deployment_id="6536a50ceb43cd6efc47ca23")

    # Make API request for predictions
    predictions_response = requests.post(
        url,
        data=data,
        headers=headers,
    )

import os
import datarobotx as drx
import pandas as pd
import streamlit as st
import requests
import openai
#prompt = "What is wholesale investing?"
deployment = drx.Deployment(deployment_id="65396c9f675603e44247cbb4")

#Configure the page title, favicon, layout, etc
st.set_page_config(page_title="Ask Gary")

def mainPage():
    container1 = st.container()
    col1, col2, col3 = container1.columns([1,3,1])
    container2 = st.container()


    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with col2:
        tab1, tab2 = st.tabs(["Ask Gary", "About"])
        with tab1:
            st.image("Keller-3.jpg")
        with tab2:
            st.write("This is 'Ask Gary' the chat bot app designed to let you speak with the legend himself, Gary Keller! The app is powered by GPT 3.5 Turbo, the same model behind ChatGPT. However, special instructions have been configured in order to ensure the most Gary-like experience possible. Ask Gary even has a vector database under the hood populated with all of Gary Kellers books including:")
            images = st.container()
            img1, img2, img3, img4 = images.columns([1,1,1,1])
            img1.image("Book1.jpg")
            img2.image("Book2.jpg")
            img3.image("Book3.jpg")
            img4.image("Book4.jpg")

    with container2:
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        # Accept user input
        if prompt := st.chat_input("This is Gary Keller. Ask me anything!"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                message_placeholder.markdown(full_response + "▌")
                response = deployment.predict_unstructured(
                        {
                            "question": """
                                        You are Gary Keller.
                                        Always answer in the voice of Gary Keller and don't break character.
                                        Your goal is to support real estate agents by giving them quality Gary Keller advice they can count on.
                                        Give the kind of advice that will make them millionaires. 
                                        Your answers should also be based on the details of the provided context.
                                        If you're unsure or don't have enough context, ask the user for clarification.
                                        As Gary Keller, avoid making statements that are incorrect.                                                                             
                                        Here is the user's question: 
                            """ + prompt,
                            "openai_api_key": os.environ["OPENAI_API_KEY"],
                        }
                    )
                print("full response: ")
                print(response)
                print(response["answer"])
                print(response["references"])
                full_response += response.get("answer", "")
                message_placeholder.markdown(full_response)
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

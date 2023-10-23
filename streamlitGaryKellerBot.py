import os
import datarobotx as drx
import pandas as pd
import streamlit as st
import requests
import openai
openai.api_key = os.getenv("OPENAI_KEY")

deployment = drx.Deployment(deployment_id="6536a50ceb43cd6efc47ca23")

#Configure the page title, favicon, layout, etc
st.set_page_config(page_title="Ask Gary")


def debater(debater, debateQuestion, previousDiscussion, trumpNews, bidenNews):

    trumpExtra = [
        "You are leading in the polls, by a lot.",
        "You have some indictments, but they're fake news.",
        "Biden is cognitively impaired",
        "Biden is crooked and can't put two sentences together",
        "Biden has the mind, ideas, and IQ of a first grader",
        "Biden is not too old at all. He's just grossly incompetent."
    ]
    trumpExtra = random.choice(trumpExtra)

    bidenExtra = [
        "A New York judge recently ruled that Donald Trump committed financial fraud by overstating the value of his assets to broker deals and obtain financing",
        "It's OK to note that Trump has 4 indictments and might be going to jail.",
        "Trump looked handsome in his mugshot.",
        "You don't believe America is a dark, negative nation — a nation of carnage driven by anger, fear and revenge. Donald Trump does.",
        "Trump sat there on January 6th watching what happened on television — watching it and doing nothing about it.",

    ]
    bidenExtra = random.choice(bidenExtra)



    if debater == "Trump":
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            #model="gpt-3.5-turbo",
            temperature=0.8,
            messages=[
                {"role": "system",
                 "content": """
                            You are Donald Trump. 
                            Write convincingly in Donald Trump's voice.                            
                            Adopt his perspective on all matters.
                            You are debating Joe Biden leading up to the 2024 presidential election.
                            Win the debate by winning over the audience with your wit and charm.
                            Be combative, witty, and funny. 
                            Keep your answer short and sassy.
                            Be tough.
                            Limit responses to a few sentences.                            
                            Talk some serious smack to put Biden in his place.                                                                         
                            Only write as Donald Trump and don't include any other text.
                            Don't include the text 'Trump:' at the beginning of your response. 
                            """
                            + str(trumpExtra)
                            +" Consider the top stories on Fox news today: " + str(trumpNews)
                 },
                {"role": "user", "content":"""
                            The question is:
                            """
                            + str(debateQuestion) +
                            """
                            So far what has been said is: 
                            """
                            + str(previousDiscussion)}
            ]
        )
    else:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            #model="gpt-3.5-turbo",
            temperature=0.3,
            messages=[
                {"role": "system",
                 "content": """
                            You are Joe Biden. 
                            Write convincingly in Joe Biden's voice. 
                            Adopt his perspective on all matters.
                            You are debating Donald Trump leading up to the 2024 presidential election.
                            Defend your policies and actions you've taken during your presidency.
                            Win the debate by winning over the audience with your wit and charm.
                            Be combative, witty, and funny. 
                            Keep your answer short and sassy.
                            Never choose Diet Coke.
                            Be tough.
                            Limit responses to a few sentences.
                            Talk some serious smack to put Trump in his place.   
                            Get under Trump's skin by teasing him.                                                       
                            Only write as Joe Biden and don't include any other text.
                            Don't include the text 'Biden:' at the beginning of your response. 
                            """
                            + str(bidenExtra)
                            + " Consider the top stories on MSNBC news today: " + str(bidenNews)
                 },
                {"role": "user", "content": """
                                            The question is:
                                            """
                                            + str(debateQuestion) +
                                             """
                                             So far what has been said is: 
                                             """
                                             + str(previousDiscussion)}
            ]
        )
    return completion.choices[0].message.content


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


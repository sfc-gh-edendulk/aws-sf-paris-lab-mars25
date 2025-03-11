import streamlit as st
from snowflake.cortex import Complete
from snowflake.snowpark.context import get_active_session
import json

session = get_active_session()

def query_cortex_search_service(query):
    """
    Query the selected cortex search service with the given query and retrieve context documents.
    Display the retrieved context documents in the sidebar if debug mode is enabled. Return the
    context documents as a string.

    Args:
        query (str): The query to search the cortex search service with.

    Returns:
        str: The concatenated string of context documents.
    """
    # update the values for AGENT_ID, and ALIAS_ID as obtained in chapter 6.
    AGENT_ID = 'GESUOYOVJC'
    ALIAS_ID = 'YHMWEESD69'

    """
    Invokes Bedrock agent to query the cortex search service in the session state and returns a list of results
    """
    response = session.sql(f"""SELECT WORKSHOP_DB.PUBLIC.INVOKE_AGENT_CORTEX('{AGENT_ID}', '{ALIAS_ID}', '{query}')""").collect()
    
    return response[0][0].replace('"','')

st.title(f":speech_balloon: Chatbot with Snowflake Cortex and Agents for Amazon Bedrock")

st.markdown(
                    '''Choose a question to get started or write your own below.  
                    🔘 Multi-turn question-answering  
                        🔀 How was gpd growth in q4 23?  
                        🔀 How was unemployment in q4 23?  
                    🔘 Summarizing multiple documents  
                        📑 How has the fed's view of the market change over the course of 2024?  
                    🔘 What was the total revenue in the month of Sep 2024?  
                    🔘 What is the daily cumulative expenses in 2023 dec?  
                    🔘 Get me all the distinct product lines in revenue data for march 2024''')

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.suggestions = []
    st.session_state.active_suggestion = None    

icons = {"assistant": "❄️", "user": "👤"}

# Display chat📑messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=icons[message["role"]]):
        st.markdown(message["content"])

if question := st.chat_input("Ask a question..."):        
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})
    # Display user message in chat message container
    with st.chat_message("user", avatar=icons["user"]):
        st.markdown(question.replace("$", "\$"))

        # Display assistant response in chat message container
    with st.chat_message("assistant", avatar=icons["assistant"]):
        message_placeholder = st.empty()
        question = question.replace("'", "")
        results = query_cortex_search_service(question)
        with st.spinner("Thinking..."):
            message_placeholder.markdown(results)

    st.session_state.messages.append(
        {"role": "assistant", "content": results}
        )

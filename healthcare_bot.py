# Importing the libraries.
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv

# Loading the API key and authenticating to Gemini.
load_dotenv(find_dotenv(), override=True)

# Configuring the API key.
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

# Initialize the model and start a chat session with an initial system message for healthcare.
system_message = (
    "You are an AI-powered healthcare assistant. Your purpose is to provide accurate, "
    "helpful, and relevant health-related information. You will not respond to any queries "
    "that are not related to healthcare. Please provide information about symptoms, treatments, "
    "medical conditions, preventive care, and healthy lifestyle choices. Do not provide any other type of response."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction=system_message
)
chat = model.start_chat()

# Initialize a conversation history in Streamlit session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Streamlit app layout
st.title("Healthcare Assistant Chatbot")
st.image(r"healthcarebot.png")  
st.subheader("Ask me anything about healthcare!")

# User input
prompt = st.text_input("Your question:")

if st.button("Submit"):
    if prompt.lower() not in ['exit', 'quit', 'bye']:
        # Send message to the chat model
        response = chat.send_message(prompt)
        
        # Get the latest input and response
        user_input = f'**User:** {prompt}'
        #bot_response = f'**Healthcare Assistant:** {chat.history[-1].parts[0].text}'  # Access the latest response text
        bot_response = f'**Healthcare Assistant:** {chat.history[-1].role.capitalize()}: {chat.history[-1].parts[0].text}'
        # Add the latest input and response to the conversation history
        
        st.session_state.conversation_history.append(user_input)
        st.session_state.conversation_history.append(bot_response)

        # Display the updated conversation history
        for line in st.session_state.conversation_history:
            st.markdown(line)
            st.markdown('\n' + '-' * 100 + '\n')

    else:
        st.write("I am always here to help you regarding your Health. Bye for now...")

# Run the Streamlit app using the command: streamlit run your_script.py

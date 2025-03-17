import streamlit as st
import requests
import uuid
import base64

# Constants
WEBHOOK_URL = "https://1769-186-158-145-9.ngrok-free.app/webhook-test/invoke_agent"
BEARER_TOKEN = "Grupo1des"

def generate_session_id():
    return str(uuid.uuid4())

def get_base64_from_file(file_path):
    """Convert image file to base64 string for embedding in HTML"""
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def send_message_to_llm(session_id, message):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "sessionId": session_id,
        "chatInput": message
    }
    try:
        # Add debug information
        st.sidebar.write("Sending request to:", WEBHOOK_URL)
        st.sidebar.write("Payload:", payload)
        
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        
        # Add response debugging
        st.sidebar.write("Response status:", response.status_code)
        st.sidebar.write("Response headers:", dict(response.headers))
        
        if response.status_code == 200:
            if not response.text.strip():
                return "Error: Received empty response from server"
            try:
                json_response = response.json()
                st.sidebar.write("JSON Response:", json_response)
                if "output" in json_response:
                    return json_response["output"]
                else:
                    return f"Error: Response missing 'output' field. Full response: {json_response}"
            except ValueError as e:
                return f"Error parsing JSON: {str(e)}\nRaw response: {response.text[:200]}"
        else:
            return f"Error: {response.status_code} - {response.text[:200]}"
    except Exception as e:
        return f"Connection error: {str(e)}"

def main():
    # Add CSS for perfect centering and animated glowing effect for the logo
    st.markdown(
        """
        <style>
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 0;
        }
        .logo-container img {
            border-radius: 20px;
            animation: glow 2s ease-in-out infinite alternate;
            box-shadow: 0 0 10px #d13c3c;
        }
        
        @keyframes glow {
            from {
                box-shadow: 0 0 10px #d13c3c;
            }
            to {
                box-shadow: 0 0 20px #d13c3c, 0 0 30px #d13c3c;
            }
        }
        
        .title-container {
            text-align: center;
            margin-top: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Display logo with CSS centering
    st.markdown(
        f'<div class="logo-container"><img src="data:image/png;base64,{get_base64_from_file("logo.png")}" width="150"></div>',
        unsafe_allow_html=True
    )
    
    # Display title with CSS centering
    st.markdown('<h1 class="title-container">Grupo 1 Desarrollos</h1>', unsafe_allow_html=True)
    
    # Add some space between logo and chat
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Get LLM response
        llm_response = send_message_to_llm(st.session_state.session_id, user_input)

        # Add LLM response to chat history
        st.session_state.messages.append({"role": "assistant", "content": llm_response})
        with st.chat_message("assistant"):
            st.write(llm_response)

if __name__ == "__main__":
    main()
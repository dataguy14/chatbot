
import streamlit as st
from openai import OpenAI

# Hardcoded API Key (replace with your actual NVIDIA API key)
API_KEY = "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"

# Initialize client
def init_client(api_key):
    return OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )





# Configure Streamlit UI
st.title("💬 Dataguy Chatbot")
st.caption("Powered by NVIDIA NIM API")

# Sidebar for settings
with st.sidebar:
    st.markdown("### Settings")
    
    # Slider for temperature
    temperature = st.slider(
        "Temperature",
        min_value=0.1,
        max_value=1.5,
        value=0.7,
        step=0.1,
        help="Controls creativity. Lower values = more deterministic, higher values = more creative."
    )
    
    # Slider for max tokens
    max_tokens = st.slider(
        "Max Tokens",
        min_value=100,
        max_value=4096,
        value=1024,
        step=100,
        help="Controls the length of the response. Higher values = longer responses."
    )
    
    # Toggle for Deep Think mode
    deep_think = st.toggle(
        "Deep Think Mode",
        help="Enable for more detailed and thoughtful responses."
    )
    
    # Adjust parameters if Deep Think mode is enabled
    if deep_think:
        temperature = min(temperature + 0.2, 1.5)  # Increase temperature slightly
        max_tokens = min(max_tokens + 500, 4096)  # Increase max tokens
    
    # Clear chat history button
    if st.button("Clear Chat History"):
        st.session_state.messages = []

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Hello! I'm DeepSeek R1. How can I help you today?"
    }]

# Display chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input handling
if prompt := st.chat_input():
    client = init_client(API_KEY)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Show a "thinking" message or spinner
    with st.spinner("DeepSeek is thinking..." if deep_think else "Thinking..."):
        # API call with streaming
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            response = client.chat.completions.create(
                model="deepseek-ai/deepseek-r1",
                messages=st.session_state.messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })

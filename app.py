import streamlit as st
from  run import Run
run_ = Run()
import tempfile
import os
# Configure the page settings
st.set_page_config(page_title="AI Chatbot with Document Upload", layout="centered")
st.title("🤖 Chatbot with Document Upload")

# 1. Sidebar for Document Upload
with st.sidebar:
    st.header("📁 Upload Your Document. After closing the website, the doc will be lost. If you" \
    "you want you can use my mock story from github.")
    uploaded_file = st.file_uploader(
        "Supported files: TXT", 
        type=["txt"]
    )
    
    if uploaded_file is not None:
        # Avoid re-writing/re-indexing the exact same file during UI reruns
        if "indexed_file" not in st.session_state or st.session_state["indexed_file"] != uploaded_file.name:
            with st.spinner("Writing temp file & indexing into ChromaDB..."):
                
                # Create a temporary file on disk so chrom.load_and_index_txt can read a path string
                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
                    temp_file.write(uploaded_file.getbuffer())
                    temp_filepath = temp_file.name
                
                # Save the temp path to session state and run backend indexer
                st.session_state["temp_filepath"] = temp_filepath
                run_.add_file(temp_filepath)
                
                st.session_state["indexed_file"] = uploaded_file.name
                
            st.success(f"File '{uploaded_file.name}' indexed successfully!")
        else:
            st.sidebar.info(f"📁 '{uploaded_file.name}' is already loaded in Vector DB.")

# 2. Initialize Chat History (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Upload a document on the left sidebar and ask me anything."}
    ]

# 3. Display previous messages from history on rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle new user input (Chat Input)
if user_input := st.chat_input("Type your message here..."):
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 5. Generate Response (Connect your LLM here: OpenAI, Gemini, LangChain, etc.)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        with st.spinner("Searching Vector DB & generating answer..."):
            #call the method to get LLM's response
            bot_response = run_.main_run(user_question=user_input)
                
        response_placeholder.markdown(bot_response)
        
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

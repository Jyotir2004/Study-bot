import streamlit as st
import requests
import json
import time
from datetime import datetime
import os
from typing import List, Dict, Optional

# Configuration
API_BASE_URL = "http://localhost:3001/api"
DEFAULT_CONVERSATION_TITLE = "New Study Session"

class StudyBotClient:
    """Client to interact with the Study Bot backend API"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
    
    def send_message(self, message: str, conversation_id: Optional[str] = None) -> Dict:
        """Send a message to the Study Bot and get response"""
        try:
            response = requests.post(
                f"{self.base_url}/chat/send",
                json={"message": message, "conversationId": conversation_id},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to send message: {str(e)}"}
    
    def get_conversations(self) -> List[Dict]:
        """Get all conversations"""
        try:
            response = requests.get(f"{self.base_url}/chat/conversations", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch conversations: {str(e)}")
            return []
    
    def get_conversation(self, conversation_id: str) -> Dict:
        """Get specific conversation details"""
        try:
            response = requests.get(f"{self.base_url}/chat/conversation/{conversation_id}", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch conversation: {str(e)}"}
    
    def create_conversation(self, title: str = DEFAULT_CONVERSATION_TITLE) -> Dict:
        """Create a new conversation"""
        try:
            response = requests.post(
                f"{self.base_url}/chat/conversation",
                json={"title": title},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to create conversation: {str(e)}"}
    
    def ask_critical_thinking(self, concept: str, conversation_id: Optional[str] = None) -> Dict:
        """Ask a critical thinking question"""
        try:
            response = requests.post(
                f"{self.base_url}/chat/critical-thinking",
                json={"concept": concept, "conversationId": conversation_id},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to ask critical thinking question: {str(e)}"}
    
    def get_summary(self, conversation_id: str) -> Dict:
        """Get conversation summary"""
        try:
            response = requests.get(f"{self.base_url}/chat/summary/{conversation_id}", timeout=20)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to get summary: {str(e)}"}

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'client' not in st.session_state:
        st.session_state.client = StudyBotClient()
    
    if 'current_conversation' not in st.session_state:
        st.session_state.current_conversation = None
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'conversations' not in st.session_state:
        st.session_state.conversations = []

def load_conversations():
    """Load conversations from backend"""
    conversations = st.session_state.client.get_conversations()
    st.session_state.conversations = conversations

def start_new_conversation():
    """Start a new conversation"""
    with st.spinner("Creating new conversation..."):
        result = st.session_state.client.create_conversation()
        if "error" not in result:
            st.session_state.current_conversation = result
            st.session_state.messages = []
            load_conversations()
            st.success("New conversation started!")
        else:
            st.error(result["error"])

def load_conversation(conversation_id: str):
    """Load an existing conversation"""
    with st.spinner("Loading conversation..."):
        result = st.session_state.client.get_conversation(conversation_id)
        if "error" not in result:
            st.session_state.current_conversation = result.get("conversation")
            st.session_state.messages = result.get("messages", [])
            st.success("Conversation loaded!")
        else:
            st.error(result["error"])

def send_message():
    """Send user message and get AI response"""
    if not st.session_state.user_input.strip():
        return
    
    # Add user message to display
    user_message = {
        "role": "user",
        "content": st.session_state.user_input,
        "timestamp": datetime.now().isoformat()
    }
    st.session_state.messages.append(user_message)
    
    # Send to backend
    with st.spinner("Thinking..."):
        conversation_id = st.session_state.current_conversation.get("id") if st.session_state.current_conversation else None
        result = st.session_state.client.send_message(st.session_state.user_input, conversation_id)
        
        if "error" not in result:
            # Update conversation if it was created
            if not st.session_state.current_conversation and "conversationId" in result:
                # Load the new conversation
                load_conversation(result["conversationId"])
            else:
                # Add AI response to display
                ai_message = {
                    "role": "assistant",
                    "content": result["aiResponse"]["content"],
                    "timestamp": datetime.now().isoformat()
                }
                st.session_state.messages.append(ai_message)
        else:
            st.error(result["error"])
    
    # Clear input
    st.session_state.user_input = ""

def main():
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Study Bot - AI Academic Assistant",
        page_icon="📚",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("📚 Study Bot")
        st.markdown("---")
        
        # API Status
        try:
            response = requests.get(f"{API_BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                st.success("✅ Backend Connected")
            else:
                st.warning("⚠️ Backend Issues")
        except:
            st.error("❌ Backend Disconnected")
            st.info("Make sure the backend server is running on port 3001")
        
        st.markdown("---")
        
        # Conversation Management
        st.subheader("Conversations")
        
        # New conversation button
        if st.button("➕ New Conversation", use_container_width=True):
            start_new_conversation()
        
        # Load conversations
        if st.button("🔄 Refresh", use_container_width=True):
            load_conversations()
        
        st.markdown("---")
        
        # Conversation list
        if st.session_state.conversations:
            for conv in st.session_state.conversations:
                conv_title = conv.get("title", "Untitled")
                conv_id = conv.get("id")
                conv_date = conv.get("updated_at", conv.get("created_at", ""))
                
                # Format date
                if conv_date:
                    try:
                        date_obj = datetime.fromisoformat(conv_date.replace('Z', '+00:00'))
                        formatted_date = date_obj.strftime("%Y-%m-%d %H:%M")
                    except:
                        formatted_date = conv_date[:19] if len(conv_date) > 19 else conv_date
                else:
                    formatted_date = "Unknown"
                
                # Check if current conversation
                is_current = (st.session_state.current_conversation and 
                            st.session_state.current_conversation.get("id") == conv_id)
                
                button_label = f"{'📌 ' if is_current else ''}{conv_title}"
                
                if st.button(button_label, key=f"conv_{conv_id}", use_container_width=True):
                    load_conversation(conv_id)
        else:
            st.info("No conversations yet. Start a new one!")
    
    # Main content area
    if st.session_state.current_conversation:
        st.title(st.session_state.current_conversation.get("title", "Study Session"))
        
        # Critical thinking section
        with st.expander("🧠 Critical Thinking Tools", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                concept = st.text_input("Enter a concept to analyze critically:")
                if st.button("Analyze Concept"):
                    if concept.strip():
                        with st.spinner("Generating critical thinking response..."):
                            conversation_id = st.session_state.current_conversation.get("id")
                            result = st.session_state.client.ask_critical_thinking(concept, conversation_id)
                            if "error" not in result:
                                st.success("Critical thinking response generated!")
                                # Add to messages
                                ct_message = {
                                    "role": "assistant",
                                    "content": f"**Critical Thinking Analysis: {concept}**\n\n{result['criticalThinkingResponse']}",
                                    "timestamp": datetime.now().isoformat()
                                }
                                st.session_state.messages.append(ct_message)
                            else:
                                st.error(result["error"])
                    else:
                        st.warning("Please enter a concept to analyze")
            
            with col2:
                if st.button("Generate Summary"):
                    with st.spinner("Generating conversation summary..."):
                        conversation_id = st.session_state.current_conversation.get("id")
                        result = st.session_state.client.get_summary(conversation_id)
                        if "error" not in result:
                            st.info("**Conversation Summary:**\n\n" + result.get("summary", "No summary available"))
                        else:
                            st.error(result["error"])
        
        # Chat interface
        st.markdown("---")
        
        # Display messages
        chat_container = st.container()
        with chat_container:
            if st.session_state.messages:
                for i, message in enumerate(st.session_state.messages):
                    if message["role"] == "user":
                        with st.chat_message("user"):
                            st.markdown(message["content"])
                            if "timestamp" in message:
                                st.caption(f"🕒 {message['timestamp'][:19]}")
                    else:
                        with st.chat_message("assistant"):
                            st.markdown(message["content"])
                            if "timestamp" in message:
                                st.caption(f"🕒 {message['timestamp'][:19]}")
            else:
                st.info("👋 Welcome! Ask me anything about your studies to get started.")
        
        # Message input
        st.markdown("---")
        user_input = st.text_input(
            "Your question:",
            key="user_input",
            placeholder="Ask me anything about your studies...",
            on_change=send_message
        )
        
        # Send button
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("Send 📤", use_container_width=True):
                send_message()
        
    else:
        # Welcome screen
        st.title("📚 Welcome to Study Bot!")
        st.markdown("""
        I'm your AI academic assistant designed to help you learn and understand complex concepts.
        
        **Features:**
        - 💬 Interactive chat with step-by-step explanations
        - 📝 Conversation history and management
        - 🧠 Critical thinking analysis tools
        - 📊 Conversation summaries
        - 📱 Responsive interface
        
        **Get Started:**
        1. Click "➕ New Conversation" in the sidebar
        2. Ask me questions about any academic subject
        3. Try critical thinking prompts for deeper understanding
        
        **Example questions:**
        - "Explain photosynthesis step by step"
        - "Help me understand calculus derivatives"
        - "What are the causes of World War I?"
        """)
        
        # Quick start button
        if st.button("🚀 Start New Conversation", type="primary", use_container_width=True):
            start_new_conversation()

if __name__ == "__main__":
    main()

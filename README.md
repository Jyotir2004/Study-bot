# Study Bot - Streamlit UI

This is a Streamlit-based user interface for Study Bot, an AI academic assistant.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Streamlit
- Running Study Bot backend server

### Installation
```bash
# Install required packages
pip install streamlit requests

# Or install from requirements.txt (if available)
pip install -r requirements.txt
```

### Running the Application

1. **Start the backend server first:**
   ```bash
   cd backend
   npm start
   ```
   The backend should be running on `http://localhost:3001`

2. **Start the Streamlit UI:**
   ```bash
   # Method 1: Using the batch file
   start-streamlit.bat
   
   # Method 2: Direct command
   streamlit run streamlit_app.py --server.port 8501
   ```

3. **Access the application:**
   Open your browser and go to `http://localhost:8501`

## 🎯 Features

### Main Interface
- **Sidebar Navigation**: Easy conversation management
- **Real-time Chat**: Interactive messaging with AI responses
- **Conversation History**: Save and revisit learning sessions
- **Status Indicators**: Backend connection status

### Conversation Management
- **New Conversations**: Start fresh learning sessions
- **Conversation List**: Browse all past sessions
- **Quick Loading**: One-click access to previous conversations
- **Auto-refresh**: Keep conversation list up to date

### Advanced Learning Tools
- **Critical Thinking Analysis**: Deep dive into concepts
- **Conversation Summaries**: Quick overview of learning sessions
- **Timestamp Tracking**: See when interactions occurred

### User Experience
- **Responsive Design**: Works on desktop and mobile
- **Loading Indicators**: Visual feedback during operations
- **Error Handling**: Clear error messages and recovery
- **Intuitive Layout**: Clean, organized interface

## 📚 Usage Examples

### Starting a New Session
1. Click "➕ New Conversation" in the sidebar
2. Type your question in the input field
3. Press Enter or click "Send"

### Example Questions
- "Explain photosynthesis step by step"
- "Help me understand calculus derivatives"
- "What are the main themes in Hamlet?"
- "How does machine learning work?"

### Using Critical Thinking Tools
1. Expand the "🧠 Critical Thinking Tools" section
2. Enter a concept to analyze
3. Click "Analyze Concept" for deep insights
4. Use "Generate Summary" for session overview

## 🛠️ Technical Details

### API Integration
The Streamlit app communicates with the Node.js backend through:
- REST API endpoints
- JSON data exchange
- Error handling and timeout management

### Session Management
- Uses Streamlit's session state
- Maintains conversation context
- Persists user interactions

### Requirements
- **Streamlit**: >= 1.28.0
- **Requests**: >= 2.31.0
- **Backend**: Study Bot Node.js server running on port 3001

## 🤝 Troubleshooting

### Common Issues

**Backend Connection Failed**
- Ensure backend is running: `cd backend && npm start`
- Check if port 3001 is available
- Verify API endpoints are accessible

**Streamlit Won't Start**
- Check Python version (3.8+)
- Install required packages: `pip install streamlit requests`
- Try: `streamlit hello` to test installation

**No Conversations Showing**
- Click "🔄 Refresh" in the sidebar
- Check backend connection status
- Verify database is accessible

### Need Help?
- Check the backend console for errors
- Verify all required files exist
- Ensure environment variables are set correctly

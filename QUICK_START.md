# Quick Start Guide - Cognos Web Application

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: (Optional) Set Up OpenAI API Key
```bash
# Create .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

Or set environment variable:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Step 3: Run the Application
```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

## 📱 What You'll See

1. **Header**: Cognos logo and tagline
2. **Disclaimer Banner**: Important safety information (can be closed)
3. **Chat Interface**: 
   - AI greeting message
   - Input field for your symptoms
   - Send button
   - Character counter
4. **Footer**: Emergency contact information

## 💬 How to Use

1. **Describe Your Symptoms**: Type your health concerns in the input field
2. **Send**: Press Enter or click the send button
3. **Get Response**: AI will respond with assessment and recommendations
4. **Emergency Detection**: Emergency responses are highlighted in red
5. **Clear Chat**: Click "Clear Chat" to start a new conversation
6. **Exit**: Type 'exit', 'quit', or 'bye' to end

## 🎨 Features

- ✅ Modern, clean interface
- ✅ Mobile-responsive design
- ✅ Real-time typing indicators
- ✅ Emergency response highlighting
- ✅ Auto-scrolling messages
- ✅ Character counter
- ✅ Keyboard shortcuts (Enter to send, Shift+Enter for new line)

## 🔧 Troubleshooting

**Port already in use?**
```bash
export PORT=5001
python app.py
```

**No API key?**
- The app will work in rule-based mode (no LLM)
- Still fully functional for demonstrations

**Can't see the page?**
- Make sure Flask is running
- Check the terminal for errors
- Try a different browser

## 📚 More Information

- See `FRONTEND_README.md` for detailed documentation
- See `README.md` for system overview
- See `SYSTEM_DESIGN.md` for design specifications


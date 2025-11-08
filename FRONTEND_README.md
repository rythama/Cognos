# Cognos Frontend - Web Application

A modern, responsive web interface for the Cognos AI Primary Care Consultation System.

## Features

- **Modern Chat Interface**: Clean, conversational UI with real-time messaging
- **Responsive Design**: Mobile-first design that works on all devices
- **Emergency Detection**: Visual indicators for emergency responses
- **Accessibility**: WCAG-compliant design with keyboard navigation support
- **Real-time Typing Indicators**: Shows when AI is processing
- **Auto-scrolling**: Automatically scrolls to latest messages
- **Character Counter**: Tracks message length (1000 character limit)

## Project Structure

```
Cognos/
├── app.py                 # Flask web application
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Stylesheet
│   └── js/
│       └── app.js        # Frontend JavaScript
└── requirements.txt      # Python dependencies
```

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up OpenAI API Key** (optional, for LLM mode):
   ```bash
   # Option 1: Set environment variable
   export OPENAI_API_KEY="your-api-key-here"
   
   # Option 2: Create .env file
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

## Running the Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your browser**:
   Navigate to `http://localhost:5000`

The application will automatically:
- Use **LLM mode** if `OPENAI_API_KEY` is set (more natural conversations)
- Fall back to **rule-based mode** if no API key is found (still fully functional)

## Usage

1. **Start a Conversation**: Type your symptoms or concerns in the input field
2. **Send Messages**: Press Enter or click the send button
3. **Emergency Responses**: Emergency scenarios are highlighted with red borders
4. **Clear Chat**: Click "Clear Chat" to start a new conversation
5. **Exit**: Type 'exit', 'quit', or 'bye' to end the conversation

## API Endpoints

### `POST /api/consult`
Process a consultation message.

**Request**:
```json
{
  "message": "I've been having headaches for the past few days"
}
```

**Response**:
```json
{
  "response": "I understand you're experiencing headaches...",
  "success": true
}
```

### `GET /api/health`
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "llm_enabled": true,
  "service": "Cognos AI Primary Care Consultation"
}
```

## Design Features

### Color Scheme
- **Primary**: Blue (#2563eb) - Trust and professionalism
- **Emergency**: Red (#ef4444) - Urgency and alerts
- **Success**: Green (#10b981) - Positive actions
- **Neutral**: Gray scale - Clean, medical aesthetic

### Typography
- **Font**: Inter (Google Fonts)
- **Sizes**: Responsive scaling from mobile to desktop
- **Accessibility**: High contrast ratios for readability

### Responsive Breakpoints
- **Mobile**: < 480px
- **Tablet**: 481px - 768px
- **Desktop**: > 768px

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development

### Running in Development Mode
The Flask app runs in debug mode by default. To disable:
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

### Customizing the Port
Set the `PORT` environment variable:
```bash
export PORT=8080
python app.py
```

## Security Notes

- This is a prototype for demonstration purposes
- In production, implement:
  - HTTPS/SSL encryption
  - Rate limiting
  - Input validation and sanitization
  - Authentication/authorization
  - HIPAA compliance measures
  - Secure session management

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```bash
export PORT=5001
python app.py
```

### CORS Issues
CORS is enabled by default. If you encounter issues, check the `flask-cors` configuration in `app.py`.

### API Errors
Check the browser console (F12) for detailed error messages. The backend will return error responses in JSON format.

## Future Enhancements

- Voice input/output support
- Multi-language support
- Dark mode toggle
- Message history persistence
- File upload for medical documents
- Integration with healthcare systems
- Real-time notifications
- User authentication


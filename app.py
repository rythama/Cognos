#!/usr/bin/env python3
"""
Flask web application for Cognos AI Primary Care Consultation System
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from ai_consultant import AIConsultant

app = Flask(__name__)
CORS(app)  # Enable CORS for API endpoints

# Initialize the AI consultant
consultant = AIConsultant(use_llm=True)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/consult', methods=['POST'])
def consult():
    """Handle consultation requests from the frontend."""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Process the message through the AI consultant
        response = consultant.process_input(user_message)
        
        return jsonify({
            'response': response,
            'success': True
        })
        
    except Exception as e:
        print(f"Error processing consultation: {e}")
        return jsonify({
            'error': 'An error occurred while processing your request',
            'response': 'I apologize, I encountered an issue processing your message. Please try rephrasing your concern or try again in a moment. How does this sound to you?',
            'success': False
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'llm_enabled': consultant.use_llm,
        'service': 'Cognos AI Primary Care Consultation'
    })

if __name__ == '__main__':
    # Get port from environment variable or default to 5001
    # (5000 is often used by macOS AirPlay Receiver)
    port = int(os.environ.get('PORT', 5001))
    
    # Run the app
    # Set debug=False for production
    print(f"\n🚀 Starting Cognos web application on http://localhost:{port}")
    print(f"   Open your browser to view the application\n")
    app.run(host='0.0.0.0', port=port, debug=True)


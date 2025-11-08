// Cognos Frontend Application
class CognosApp {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.chatForm = document.getElementById('chatForm');
        this.sendButton = document.getElementById('sendButton');
        this.typingIndicator = document.getElementById('typingIndicator');
        this.charCount = document.getElementById('charCount');
        
        this.isProcessing = false;
        this.conversationStarted = false;
        
        this.init();
    }
    
    init() {
        // Set up event listeners
        this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
        this.userInput.addEventListener('input', () => this.handleInputChange());
        this.userInput.addEventListener('keydown', (e) => this.handleKeyDown(e));
        
        // Auto-resize textarea
        this.userInput.addEventListener('input', () => this.autoResizeTextarea());
        
        // Load initial greeting
        this.loadInitialGreeting();
        
        // Focus input on load
        setTimeout(() => this.userInput.focus(), 100);
    }
    
    loadInitialGreeting() {
        // Show initial greeting from AI
        this.addMessage('ai', 'Hello, I\'m here to help you with your health concerns today. I understand you\'re looking for some guidance about how you\'re feeling.\n\nWhat\'s bringing you in today? Please describe what you\'re experiencing.');
    }
    
    handleInputChange() {
        const length = this.userInput.value.length;
        this.charCount.textContent = `${length} / 1000`;
        
        // Update character count color
        if (length > 900) {
            this.charCount.style.color = 'var(--emergency-color)';
        } else if (length > 750) {
            this.charCount.style.color = 'var(--warning-color)';
        } else {
            this.charCount.style.color = 'var(--text-muted)';
        }
    }
    
    handleKeyDown(e) {
        // Allow Enter to submit, but Shift+Enter for new line
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!this.isProcessing && this.userInput.value.trim()) {
                this.chatForm.dispatchEvent(new Event('submit'));
            }
        }
    }
    
    autoResizeTextarea() {
        this.userInput.style.height = 'auto';
        this.userInput.style.height = Math.min(this.userInput.scrollHeight, 150) + 'px';
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        const message = this.userInput.value.trim();
        
        if (!message || this.isProcessing) {
            return;
        }
        
        // Check for exit commands
        const exitCommands = ['exit', 'quit', 'bye', 'goodbye', 'q', 'stop', 'end', 'done'];
        if (exitCommands.includes(message.toLowerCase())) {
            this.addMessage('user', message);
            this.addMessage('ai', 'I understand you\'re ending our conversation. Take care, and remember - if your symptoms worsen or you have concerns, please don\'t hesitate to seek medical attention. How does this sound to you?');
            this.userInput.value = '';
            this.handleInputChange();
            this.autoResizeTextarea();
            return;
        }
        
        // Add user message to chat
        this.addMessage('user', message);
        this.userInput.value = '';
        this.handleInputChange();
        this.autoResizeTextarea();
        
        // Disable input while processing
        this.setProcessing(true);
        
        try {
            // Show typing indicator
            this.showTypingIndicator();
            
            // Send message to backend
            const response = await this.sendMessage(message);
            
            // Hide typing indicator
            this.hideTypingIndicator();
            
            // Check if response indicates emergency
            const isEmergency = this.detectEmergency(response);
            
            // Add AI response
            this.addMessage('ai', response, isEmergency);
            
            this.conversationStarted = true;
            
        } catch (error) {
            console.error('Error:', error);
            this.hideTypingIndicator();
            this.addMessage('ai', 'I apologize, I encountered an issue processing your message. Please try rephrasing your concern or try again in a moment. How does this sound to you?');
        } finally {
            this.setProcessing(false);
        }
    }
    
    async sendMessage(message) {
        const response = await fetch('/api/consult', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data.response;
    }
    
    detectEmergency(response) {
        // Check for emergency indicators in response
        const emergencyPhrases = [
            'immediate medical attention',
            'call 911',
            'emergency room',
            'beyond what I can safely assess',
            'immediate medical care'
        ];
        
        return emergencyPhrases.some(phrase => 
            response.toLowerCase().includes(phrase.toLowerCase())
        );
    }
    
    addMessage(type, content, isEmergency = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}${isEmergency ? ' emergency' : ''}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Format message content (preserve line breaks)
        const formattedContent = this.formatMessage(content);
        contentDiv.innerHTML = formattedContent;
        
        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.getCurrentTime();
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        
        this.chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        this.scrollToBottom();
    }
    
    formatMessage(content) {
        // Convert line breaks to <br>
        let formatted = content.replace(/\n/g, '<br>');
        
        // Format numbered lists (1. 2. 3.)
        formatted = formatted.replace(/(\d+)\.\s+(.+?)(?=\d+\.|$)/g, '<strong>$1.</strong> $2<br>');
        
        // Format bold text (text between **)
        formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        
        // Format italic text (text between *)
        formatted = formatted.replace(/\*(.+?)\*/g, '<em>$1</em>');
        
        return formatted;
    }
    
    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString('en-US', { 
            hour: 'numeric', 
            minute: '2-digit',
            hour12: true 
        });
    }
    
    showTypingIndicator() {
        this.typingIndicator.style.display = 'flex';
        setTimeout(() => this.scrollToBottom(), 50);
    }
    
    hideTypingIndicator() {
        this.typingIndicator.style.display = 'none';
    }
    
    setProcessing(processing) {
        this.isProcessing = processing;
        this.userInput.disabled = processing;
        this.sendButton.disabled = processing;
        
        if (processing) {
            this.sendButton.style.opacity = '0.5';
            this.sendButton.style.cursor = 'not-allowed';
        } else {
            this.sendButton.style.opacity = '1';
            this.sendButton.style.cursor = 'pointer';
        }
    }
    
    scrollToBottom() {
        setTimeout(() => {
            const chatMessages = document.getElementById('chatMessages');
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 100);
    }
}

// Clear chat function
function clearChat() {
    if (confirm('Are you sure you want to clear the conversation? This cannot be undone.')) {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = '';
        
        // Reload initial greeting
        const app = window.cognosApp;
        if (app) {
            app.loadInitialGreeting();
            app.conversationStarted = false;
        }
    }
}

// Close disclaimer function
function closeDisclaimer() {
    const disclaimerBanner = document.getElementById('disclaimerBanner');
    disclaimerBanner.classList.add('hidden');
    
    // Store in localStorage to remember user preference
    localStorage.setItem('disclaimerClosed', 'true');
}

// Check if disclaimer was previously closed
if (localStorage.getItem('disclaimerClosed') === 'true') {
    document.getElementById('disclaimerBanner').classList.add('hidden');
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.cognosApp = new CognosApp();
});


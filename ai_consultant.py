#!/usr/bin/env python3
"""
AI Primary Care Consultation System
A prototype that handles mild and emergency scenarios with appropriate escalation.
Now with LLM integration for natural conversations.
"""

import re
import os
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# Try to import dotenv for .env file loading
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    pass  # dotenv is optional

# Try to import OpenAI - fall back to rule-based if not available
try:
    from openai import OpenAI
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("Warning: OpenAI library not installed. Using rule-based mode. Install with: pip install openai")


class AIConsultant:
    """AI system for primary care consultations with LLM integration."""
    
    # Emergency symptom keywords
    EMERGENCY_KEYWORDS = [
        'chest pain', 'chest pressure', 'heart attack', 'cardiac',
        'difficulty breathing', 'trouble breathing', 'shortness of breath', 'can\'t breathe', 
        'cannot breathe', 'choking', 'breathing problem', 'hard to breathe',
        'severe pain', 'excruciating', 'unbearable pain',
        'stroke', 'facial droop', 'slurred speech', 'weakness', 'numbness',
        'severe allergic reaction', 'anaphylaxis', 'throat closing',
        'severe headache', 'worst headache', 'sudden severe',
        'severe abdominal pain', 'severe stomach pain',
        'mental health crisis', 'suicidal', 'self harm'
    ]
    
    # Emergency severity indicators
    EMERGENCY_SEVERITY = ['severe', 'terrible', 'awful', 'worst', 'extreme', 'critical', 'emergency']
    
    # Mild symptom keywords
    MILD_KEYWORDS = [
        'fatigue', 'tired', 'headache', 'mild', 'minor',
        'cold', 'cough', 'sneezing', 'runny nose',
        'mild pain', 'ache', 'sore',
        'digestive', 'upset stomach', 'mild nausea',
        'skin irritation', 'rash', 'itchy'
    ]
    
    def __init__(self, use_llm: bool = True, api_key: Optional[str] = None):
        """Initialize the AI consultant.
        
        Args:
            use_llm: Whether to use LLM API (default: True)
            api_key: OpenAI API key (default: from OPENAI_API_KEY env var)
        """
        self.conversation_state = {
            'stage': 'greeting',
            'symptoms': [],
            'symptom_description': '',
            'timeline': None,
            'severity': None,
            'concerns': None,
            'assessed': False,
            'questions_asked': set(),
            'information_gathered': {}
        }
        
        # LLM setup
        self.use_llm = use_llm and LLM_AVAILABLE
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        self.conversation_history = []
        self.system_instructions = self._load_system_instructions()
        
        if self.use_llm:
            if not self.api_key:
                print("Warning: No OPENAI_API_KEY found. Falling back to rule-based mode.")
                print("Set OPENAI_API_KEY environment variable or create a .env file with:")
                print("  OPENAI_API_KEY=your-api-key-here")
                self.use_llm = False
            else:
                try:
                    # Check if API key looks valid (starts with sk-)
                    if not self.api_key.startswith('sk-'):
                        print(f"Warning: API key format looks incorrect (should start with 'sk-').")
                        print("Falling back to rule-based mode.")
                        self.use_llm = False
                    else:
                        self.client = OpenAI(api_key=self.api_key)
                        print("✓ LLM mode enabled (API key detected)")
                except Exception as e:
                    print(f"Warning: Failed to initialize OpenAI client: {e}")
                    print("Falling back to rule-based mode.")
                    self.use_llm = False
    
    def _load_system_instructions(self) -> str:
        """Load system instructions from SYSTEM_INSTRUCTIONS.md"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            instructions_path = os.path.join(script_dir, 'SYSTEM_INSTRUCTIONS.md')
            with open(instructions_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            # Fallback to embedded instructions
            return """You are an AI primary care consultant conducting patient consultations. Your role is to assess symptoms, provide guidance for mild cases, and escalate emergencies appropriately.

Always use "I understand" (never "I see" or "I hear") when acknowledging patient concerns.
Before recommendations, ask: "What concerns you most about this?"
After recommendations, end with: "How does this sound to you?"
For pain: "That sounds really uncomfortable"
For worry: "It's completely understandable that you're concerned about [specific symptom]"
Never say "don't worry" - use "let's work through this together"
No medical jargon - use lay terms (e.g., "high blood pressure" not "hypertension")
Always include disclaimer: "I can provide guidance, but I cannot replace an in-person examination"
"""
    
    def detect_emergency(self, text: str, check_severity: bool = True) -> bool:
        """Detect if patient input suggests emergency symptoms."""
        text_lower = text.lower()
        
        # Check for emergency keywords
        if any(keyword in text_lower for keyword in self.EMERGENCY_KEYWORDS):
            return True
        
        # Check for high fever (emergency temperature thresholds)
        # 105°F (40.5°C) or higher is a medical emergency
        fever_patterns = [
            r'10[5-9]\s*f',  # 105-109°F (emergency)
            r'1[1-9]\d\s*f',  # 110+°F (emergency)
            r'40\.5\s*c',  # 40.5°C (emergency)
            r'4[1-2]\.?\d*\s*c',  # 41.0-42.9°C (emergency)
            r'4[3-9]\.?\d*\s*c',  # 43+°C (emergency)
            r'10[5-9]\s*degrees',  # 105-109 degrees (emergency)
            r'1[1-9]\d\s*degrees',  # 110+ degrees (emergency)
        ]
        
        if 'fever' in text_lower or 'temperature' in text_lower or 'temp' in text_lower:
            for pattern in fever_patterns:
                if re.search(pattern, text_lower):
                    return True
            # Also check for explicit high fever mentions
            if any(phrase in text_lower for phrase in ['high fever', 'very high fever', 'dangerous fever']):
                return True
        
        # Check for severe symptoms combined with emergency indicators
        if check_severity:
            has_severity = any(severity in text_lower for severity in self.EMERGENCY_SEVERITY)
            has_breathing = any(breath in text_lower for breath in ['breathing', 'breathe', 'breath'])
            has_pain = any(pain in text_lower for pain in ['pain', 'hurting', 'hurt'])
            
            # If user mentions severe breathing issues or severe pain
            if has_severity and (has_breathing or has_pain):
                return True
            
            # Check if symptoms are getting worse with severity
            if has_severity and ('worse' in text_lower or 'worsening' in text_lower):
                return True
        
        return False
    
    def detect_mild_symptoms(self, text: str) -> bool:
        """Detect if patient input suggests mild symptoms."""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.MILD_KEYWORDS)
    
    def extract_symptoms(self, text: str) -> List[str]:
        """Extract symptom mentions from patient input."""
        symptoms = []
        # Simple extraction - in production, use NLP
        for keyword in self.EMERGENCY_KEYWORDS + self.MILD_KEYWORDS:
            if keyword in text.lower():
                symptoms.append(keyword)
        return symptoms
    
    def get_greeting(self) -> str:
        """Initial greeting message."""
        return """Hello, I'm here to help you with your health concerns today. I understand you're looking for some guidance about how you're feeling.

What's bringing you in today? Please describe what you're experiencing."""
    
    def handle_emergency(self, text: str) -> str:
        """Handle emergency scenario with structured response."""
        symptoms = self.extract_symptoms(text)
        text_lower = text.lower()
        
        # Determine symptom description - check fever first as it's common
        if 'fever' in text_lower or 'temperature' in text_lower or 'temp' in text_lower:
            # Extract temperature if mentioned
            temp_match = re.search(r'(\d+\.?\d*)\s*[fc°]', text_lower)
            if temp_match:
                temp = temp_match.group(1)
                # Check if it's Fahrenheit or Celsius
                if 'c' in text_lower or '°c' in text_lower:
                    temp_float = float(temp)
                    if temp_float >= 40.5:  # 40.5°C = 105°F
                        symptom_desc = f"a fever of {temp}°C"
                    else:
                        symptom_desc = f"a high fever of {temp}°C"
                else:
                    temp_float = float(temp)
                    if temp_float >= 105:
                        symptom_desc = f"a fever of {temp}°F"
                    else:
                        symptom_desc = f"a high fever of {temp}°F"
            else:
                symptom_desc = "a high fever"
        elif 'breathing' in text_lower or 'breathe' in text_lower:
            symptom_desc = "difficulty breathing"
        elif 'chest' in text_lower or 'cardiac' in text_lower or 'heart' in text_lower:
            symptom_desc = "chest pain or cardiac symptoms"
        elif 'pain' in text_lower:
            symptom_desc = "severe pain"
        else:
            symptom_desc = ', '.join(symptoms[:2]) if symptoms else "your symptoms"
        
        response = f"""Based on what you've told me, {symptom_desc} suggest this may need immediate medical attention. This is beyond what I can safely assess remotely.

Here's what I recommend: Please seek immediate medical care. If you're experiencing severe symptoms right now, call 911 or go to your nearest emergency room immediately. If symptoms are less severe but still concerning, consider urgent care or contact your primary care provider right away.

I can provide guidance, but I cannot replace an in-person examination, especially for symptoms like these. Your safety is the priority.

How does this sound to you? Do you have any questions about where to seek care?"""
        
        # Mark as emergency handled
        self.conversation_state['stage'] = 'emergency_handled'
        return response
    
    def _get_llm_response(self, user_input: str, is_emergency: bool = False) -> Optional[str]:
        """Get response from LLM API."""
        if not self.use_llm or not self.client:
            return None
        
        try:
            # Build conversation context
            messages = [{"role": "system", "content": self.system_instructions}]
            
            # Add conversation history
            for entry in self.conversation_history[-6:]:  # Last 6 exchanges for context
                messages.append(entry)
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            # Add emergency context if needed
            if is_emergency:
                messages.append({
                    "role": "system",
                    "content": "IMPORTANT: The patient has described emergency symptoms (chest pain, difficulty breathing, severe pain, high fever 105°F/40.5°C or higher, stroke signs, etc.). You must follow the emergency protocol exactly: Use 'Based on what you've told me...' format, state 'This is beyond what I can safely assess remotely', and recommend immediate medical care. Do NOT provide self-care recommendations for emergencies."
                })
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Using cost-effective model
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            llm_response = response.choices[0].message.content.strip()
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": llm_response})
            
            return llm_response
            
        except Exception as e:
            print(f"Error calling LLM API: {e}")
            return None
    
    def _get_recommendations(self, symptoms: List[str]) -> List[str]:
        """Generate appropriate self-care recommendations based on symptoms."""
        symptom_str = ' '.join(symptoms).lower()
        
        if any(s in symptom_str for s in ['headache', 'pain', 'ache']):
            return [
                "Rest in a quiet, dark room and try to stay hydrated with water",
                "Consider over-the-counter pain relief like acetaminophen or ibuprofen, following package instructions",
                "Apply a cool compress to your forehead or the area of discomfort for 15-20 minutes"
            ]
        elif any(s in symptom_str for s in ['fatigue', 'tired']):
            return [
                "Ensure you're getting 7-9 hours of sleep per night and maintain a regular sleep schedule",
                "Stay hydrated throughout the day and eat balanced meals with plenty of fruits and vegetables",
                "Take short breaks during the day and avoid overexertion - listen to your body's signals"
            ]
        elif any(s in symptom_str for s in ['cold', 'cough', 'sneezing', 'runny nose']):
            return [
                "Get plenty of rest and stay well-hydrated with water, herbal tea, or warm broth",
                "Use a humidifier or take steamy showers to help with congestion, and consider saline nasal spray",
                "Wash your hands frequently and cover your mouth when coughing to prevent spreading to others"
            ]
        elif any(s in symptom_str for s in ['digestive', 'stomach', 'nausea']):
            return [
                "Stick to bland, easy-to-digest foods like toast, rice, bananas, and avoid spicy or fatty foods",
                "Stay hydrated with small sips of water or electrolyte drinks, and avoid large meals",
                "Rest and avoid strenuous activity - if symptoms persist, consider over-the-counter remedies following package instructions"
            ]
        else:
            return [
                "Get adequate rest and maintain a regular sleep schedule",
                "Stay well-hydrated with water throughout the day",
                "Monitor your symptoms and note any changes or worsening"
            ]
    
    def process_input(self, user_input: str) -> str:
        """Process user input and generate appropriate response."""
        user_input = user_input.strip()
        
        if not user_input:
            return "I understand you might be hesitant. Please feel free to share what's on your mind - I'm here to help."
        
        # Always check for emergency first (safety-critical, rule-based)
        is_emergency = self.detect_emergency(user_input, check_severity=True)
        
        # Also check if we have context that makes this an emergency
        if not is_emergency and self.conversation_state.get('symptom_description'):
            combined_text = self.conversation_state['symptom_description'] + ' ' + user_input
            is_emergency = self.detect_emergency(combined_text, check_severity=True)
            if is_emergency:
                user_input = combined_text
        
        # Handle emergency with rule-based response (safety-critical)
        if is_emergency:
            return self.handle_emergency(user_input)
        
        # Try LLM for non-emergency responses
        if self.use_llm:
            llm_response = self._get_llm_response(user_input, is_emergency=False)
            if llm_response:
                # Update conversation state based on user input
                self._update_conversation_state(user_input)
                return llm_response
        
        # Fall back to rule-based response
        return self._rule_based_response(user_input)
    
    def _update_conversation_state(self, user_input: str):
        """Update conversation state based on user input."""
        text_lower = user_input.lower()
        
        if self.conversation_state['stage'] == 'greeting':
            self.conversation_state['stage'] = 'assessment'
            self.conversation_state['symptom_description'] = user_input
            self.conversation_state['symptoms'] = self.extract_symptoms(user_input)
            self.conversation_state['information_gathered']['initial_symptoms'] = user_input
        
        elif self.conversation_state['stage'] == 'assessment':
            if any(sev in text_lower for sev in ['severe', 'terrible', 'awful', 'worst', 'extreme']):
                self.conversation_state['severity'] = 'severe'
                self.conversation_state['information_gathered']['severity'] = user_input
            
            if any(word in text_lower for word in ['started', 'began', 'start', 'days', 'hours', 'weeks', 'ago']):
                self.conversation_state['timeline'] = user_input
                self.conversation_state['information_gathered']['timeline'] = user_input
            
            if any(word in text_lower for word in ['worse', 'worsening', 'getting worse', 'deteriorating']):
                self.conversation_state['information_gathered']['progression'] = 'worsening'
            
            if 'concern' in text_lower or 'worry' in text_lower or 'worried' in text_lower:
                self.conversation_state['concerns'] = user_input
                self.conversation_state['information_gathered']['concerns'] = user_input
    
    def _rule_based_response(self, user_input: str) -> str:
        """Fallback rule-based response generation."""
        # Handle conversation flow dynamically
        if self.conversation_state['stage'] == 'greeting':
            # First user input - gather initial symptom description
            self.conversation_state['stage'] = 'assessment'
            self.conversation_state['symptom_description'] = user_input
            self.conversation_state['symptoms'] = self.extract_symptoms(user_input)
            self.conversation_state['information_gathered']['initial_symptoms'] = user_input
            
            # Check if it's clearly mild
            if self.detect_mild_symptoms(user_input) and not any(sev in user_input.lower() for sev in self.EMERGENCY_SEVERITY):
                return f"""I understand you're experiencing {self.conversation_state['symptoms'][0] if self.conversation_state['symptoms'] else 'these symptoms'}. That sounds really uncomfortable. Let's work through this together.

When did this first start, and has it been getting better, worse, or staying the same?"""
            else:
                return """I understand you're experiencing some concerns. That sounds really uncomfortable.

Could you help me understand more about what you're feeling? When did this first start, and has it been getting better, worse, or staying the same?"""
        
        elif self.conversation_state['stage'] == 'assessment':
            # Update information gathered
            text_lower = user_input.lower()
            
            # Extract severity
            if any(sev in text_lower for sev in ['severe', 'terrible', 'awful', 'worst', 'extreme']):
                self.conversation_state['severity'] = 'severe'
                self.conversation_state['information_gathered']['severity'] = user_input
            
            # Extract timeline
            if any(word in text_lower for word in ['started', 'began', 'start', 'days', 'hours', 'weeks', 'ago']):
                self.conversation_state['timeline'] = user_input
                self.conversation_state['information_gathered']['timeline'] = user_input
            
            # Extract concerns
            if 'concern' in text_lower or 'worry' in text_lower or 'worried' in text_lower:
                self.conversation_state['concerns'] = user_input
                self.conversation_state['information_gathered']['concerns'] = user_input
            
            # Check if we have enough information
            has_timeline = self.conversation_state.get('timeline') is not None
            has_symptoms = len(self.conversation_state.get('symptoms', [])) > 0
            
            if has_timeline and has_symptoms:
                # Provide recommendations
                symptoms = self.conversation_state['symptoms']
                recommendations = self._get_recommendations(symptoms)
                symptom_desc = symptoms[0] if symptoms else "these symptoms"
                
                response = f"""I understand you're experiencing {symptom_desc}. That sounds really uncomfortable. Let's work through this together.
"""
                
                if self.conversation_state.get('concerns'):
                    concern_topic = self._extract_concern_topic(self.conversation_state['concerns'])
                    response += f"\nIt's completely understandable that you're concerned about {concern_topic}.\n"
                
                response += f"""
Based on what you've told me, here are some things that might help:

1. {recommendations[0]}
2. {recommendations[1]}
3. {recommendations[2]}

What concerns you most about this?

If this isn't improving in 3-5 days, please contact your primary care provider or seek medical attention. I can provide guidance, but I cannot replace an in-person examination.

How does this sound to you?"""
                
                self.conversation_state['stage'] = 'completed'
                return response
            
            # Still need more information
            if not has_timeline:
                return """I understand. When did this first start, and has it been getting better, worse, or staying the same?"""
            else:
                if not self.conversation_state.get('concerns'):
                    return """I understand. What concerns you most about this?"""
        
        # Default response
        return """I understand. Let's work through this together. Could you tell me more about when this started and how it's been progressing? What concerns you most about this?"""
    
    def _extract_concern_topic(self, text: str) -> str:
        """Extract the topic of concern from patient input."""
        symptoms = self.extract_symptoms(text)
        if symptoms:
            return symptoms[0]
        return "your symptoms"


def main():
    """Main interactive loop for the AI consultant."""
    print("=" * 70)
    print("AI Primary Care Consultation System")
    print("=" * 70)
    print("\nNote: This is a prototype for demonstration purposes.")
    print("For real medical concerns, please consult with a healthcare provider.")
    print("\nTip: Type 'exit', 'quit', 'q', or 'bye' at any time to end the conversation.")
    print("=" * 70)
    print()
    
    # Initialize consultant (will use LLM if API key is available)
    consultant = AIConsultant()
    
    if not consultant.use_llm:
        print("Running in rule-based mode (no LLM API key found).")
        print("To enable LLM mode, set OPENAI_API_KEY environment variable.")
        print()
    
    print(consultant.get_greeting())
    print()
    
    # Exit commands that users can use
    exit_commands = ['exit', 'quit', 'bye', 'goodbye', 'q', 'stop', 'end', 'done']
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            # Check for exit commands
            if user_input.lower() in exit_commands:
                print("\nAI: I understand you're ending our conversation. Take care, and remember - if your symptoms worsen or you have concerns, please don't hesitate to seek medical attention. How does this sound to you?")
                break
            
            # Check for help command
            if user_input.lower() in ['help', '?', 'commands']:
                print("\nAI: I understand you'd like some help. You can type 'exit', 'quit', 'q', or 'bye' at any time to end our conversation. Otherwise, just describe your symptoms or concerns, and I'll help you work through them. How does this sound to you?")
                continue
            
            response = consultant.process_input(user_input)
            print(f"\nAI: {response}")
            
        except KeyboardInterrupt:
            print("\n\nAI: I understand you're ending our conversation. Take care, and remember - if your symptoms worsen or you have concerns, please don't hesitate to seek medical attention. How does this sound to you?")
            break
        except Exception as e:
            print(f"\nAI: I apologize, I encountered an issue. Please try rephrasing your concern. How does this sound to you?")
            if consultant.use_llm:
                print(f"(Error details: {e})")


if __name__ == "__main__":
    main()

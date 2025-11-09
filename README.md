# CareBot: AI Primary Care Consultation System

An AI system designed to conduct primary care consultations, handling both routine mild symptoms and emergency scenarios with appropriate escalation protocols.

## Overview

This system provides a prototype AI consultant that can:
- Handle mild symptoms with self-care recommendations
- Detect and escalate emergency symptoms appropriately
- Follow strict linguistic and empathy protocols
- Provide natural, comfortable patient interactions

## Files

- **SYSTEM_DESIGN.md**: Comprehensive system design document covering appointment flow, mild vs. emergency handling, escalation logic, and patient experience
- **SYSTEM_INSTRUCTIONS.md**: System instructions/prompt for LLM (500 words)
- **ai_consultant.py**: Working prototype implementation with LLM integration
- **requirements.txt**: Python dependencies (OpenAI API for LLM mode)
- **.env.example**: Example environment file for API key setup

## Quick Start

### Prerequisites
- Python 3.7 or higher
- (Optional) OpenAI API key for LLM mode

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Set up OpenAI API key for LLM mode:
```bash
# Option 1: Set environment variable
export OPENAI_API_KEY="your-api-key-here"

# Option 2: Create .env file (recommended)
# Copy .env.example to .env and add your API key
```

Get your API key from: https://platform.openai.com/api-keys

### Running the Prototype

```bash
python ai_consultant.py
```

The system will automatically:
- Use **LLM mode** if `OPENAI_API_KEY` is set (more natural conversations)
- Fall back to **rule-based mode** if no API key is found (still fully functional)

Type your symptoms or concerns, and the AI will respond following all linguistic constraints and empathy protocols.

**To exit the conversation:** Type `exit`, `quit`, `q`, `bye`, `stop`, `end`, or `done` at any time. You can also press `Ctrl+C` to exit. Type `help` or `?` for assistance.

### Example Interactions

**Mild Symptoms:**
```
You: I've been having headaches for the past few days
AI: [Provides assessment and 3 self-care recommendations]
```

**Emergency Symptoms:**
```
You: I'm having chest pain and difficulty breathing
AI: [Immediately escalates with structured emergency response]
```

## Key Features

### Linguistic Constraints
- Uses "I understand" (not "I see" or "I hear")
- No medical jargon - uses lay terms
- Always asks "What concerns you most about this?" before recommendations
- Ends recommendations with "How does this sound to you?"

### Empathy Protocols
- Validates worry: "It's completely understandable that you're concerned about [symptom]"
- Validates pain: "That sounds really uncomfortable"
- Uses "let's work through this together" (never "don't worry")

### Structured Responses
- Emergency: "Based on what you've told me..." + assessment + "Here's what I recommend..."
- Mild symptoms: Exactly 3 numbered self-care recommendations
- Timeline question: "When did this first start, and has it been getting better, worse, or staying the same?"

### Safety Language
- Escalations include: "This is beyond what I can safely assess remotely"
- Specific timeframes: "If this isn't improving in [X days], please contact..."
- Disclaimer: "I can provide guidance, but I cannot replace an in-person examination"

## System Design

See **SYSTEM_DESIGN.md** for complete documentation of:
- Primary care appointment flow
- Mild vs. emergency scenario handling
- Escalation logic and triggers
- Patient experience design
- System architecture

## Testing Scenarios

Try these scenarios to see the system in action:

1. **Mild Headache**: "I've had a mild headache for 2 days"
2. **Fatigue**: "I've been feeling really tired lately"
3. **Emergency**: "I'm experiencing chest pain"
4. **Emergency**: "I can't breathe properly"
5. **Cold Symptoms**: "I have a runny nose and cough"

## Limitations

This is a prototype for demonstration purposes. In production, this system would:
- Require integration with healthcare systems
- Need physician oversight for all recommendations
- Require compliance with healthcare regulations (HIPAA, etc.)
- Need extensive testing and validation
- Require continuous learning and improvement

## LLM Integration

The system now supports LLM integration using OpenAI's API:

- **LLM Mode**: Uses GPT-4o-mini for natural, conversational responses while maintaining all linguistic constraints
- **Rule-Based Mode**: Falls back to deterministic rule-based responses if no API key is provided
- **Safety Layer**: Emergency detection remains rule-based for safety (always checked first)
- **System Instructions**: Uses `SYSTEM_INSTRUCTIONS.md` as the system prompt (exactly 500 words)

### Features:
- Automatic fallback to rule-based mode if API key is missing
- Conversation history maintained for context
- Emergency symptoms always handled with rule-based safety layer
- Cost-effective model (gpt-4o-mini) for production use

## Notes

- The system follows all specified linguistic constraints
- Emergency detection is rule-based for safety (always checked first)
- LLM responses are guided by system instructions to maintain protocols
- Self-care recommendations are symptom-specific
- All interactions include appropriate safety disclaimers

<img width="4534" height="4284" alt="CareBotUPDATED-2025-11-09-042811" src="https://github.com/user-attachments/assets/26e5a38c-0362-45c2-ac1d-a1de1a7305c0" />

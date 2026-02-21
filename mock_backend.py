from flask import Flask, jsonify, request
from datetime import datetime
import json
import os

app = Flask(__name__)

# In-memory storage for conversations
conversations = []
messages_storage = {}
next_conversation_id = 1
next_message_id = 1

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "message": "Study Bot mock backend is running"
    })

@app.route('/api/chat/send', methods=['POST'])
def send_message():
    global next_conversation_id, next_message_id
    
    data = request.get_json()
    message = data.get('message', '')
    conversation_id = data.get('conversationId')
    
    if not message.strip():
        return jsonify({"error": "Message is required"}), 400
    
    # Create new conversation if needed
    if not conversation_id:
        conversation = {
            "id": next_conversation_id,
            "title": "New Study Session",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        conversations.insert(0, conversation)
        conversation_id = next_conversation_id
        messages_storage[conversation_id] = []
        next_conversation_id += 1
    
    # Add user message
    user_message = {
        "id": next_message_id,
        "conversation_id": conversation_id,
        "role": "user",
        "content": message,
        "created_at": datetime.now().isoformat()
    }
    messages_storage[conversation_id].append(user_message)
    next_message_id += 1
    
    # Generate AI response (mock)
    ai_response_content = generate_mock_response(message)
    
    # Add AI response
    ai_message = {
        "id": next_message_id,
        "conversation_id": conversation_id,
        "role": "assistant",
        "content": ai_response_content,
        "created_at": datetime.now().isoformat()
    }
    messages_storage[conversation_id].append(ai_message)
    next_message_id += 1
    
    # Update conversation timestamp
    for conv in conversations:
        if conv["id"] == conversation_id:
            conv["updated_at"] = datetime.now().isoformat()
            break
    
    return jsonify({
        "conversationId": conversation_id,
        "userMessage": {"role": "user", "content": message},
        "aiResponse": {"role": "assistant", "content": ai_response_content}
    })

@app.route('/api/chat/conversations', methods=['GET'])
def get_conversations():
    return jsonify(conversations)

@app.route('/api/chat/conversation/<int:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    conversation = next((c for c in conversations if c["id"] == conversation_id), None)
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404
    
    messages = messages_storage.get(conversation_id, [])
    return jsonify({
        "conversation": conversation,
        "messages": messages
    })

@app.route('/api/chat/conversation', methods=['POST'])
def create_conversation():
    global next_conversation_id
    
    data = request.get_json()
    title = data.get('title', 'New Study Session')
    
    conversation = {
        "id": next_conversation_id,
        "title": title,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    conversations.insert(0, conversation)
    messages_storage[next_conversation_id] = []
    conversation_id = next_conversation_id
    next_conversation_id += 1
    
    return jsonify(conversation), 201

@app.route('/api/chat/critical-thinking', methods=['POST'])
def critical_thinking():
    data = request.get_json()
    concept = data.get('concept', '')
    
    if not concept.strip():
        return jsonify({"error": "Concept is required"}), 400
    
    response = f"""**Critical Thinking Analysis: {concept}**

Here's a structured analysis of this concept:

**Core Principles:**
• Fundamental concepts that underlie {concept}
• Key definitions and terminology
• Basic assumptions and premises

**Different Perspectives:**
• Historical viewpoints on {concept}
• Modern interpretations and applications
• Alternative approaches and methodologies

**Common Misconceptions:**
• Frequently misunderstood aspects
• Oversimplifications to avoid
• Areas where intuition might be misleading

**Deeper Understanding:**
• Connections to related concepts
• Real-world applications and examples
• Questions for further exploration

**Thought-Provoking Questions:**
1. What would happen if we changed a fundamental assumption?
2. How does this concept apply in different contexts?
3. What are the limitations of our current understanding?
4. How might this evolve in the future?

This analysis provides a framework for thinking more deeply about {concept}."""
    
    return jsonify({
        "concept": concept,
        "criticalThinkingResponse": response
    })

@app.route('/api/chat/summary/<int:conversation_id>', methods=['GET'])
def get_summary(conversation_id):
    messages = messages_storage.get(conversation_id, [])
    if not messages:
        return jsonify({"error": "No messages found for summary"}), 404
    
    # Generate mock summary
    user_messages = [m for m in messages if m["role"] == "user"]
    topics = list(set([m["content"].split()[0].lower() for m in user_messages[:3]]))
    
    summary = f"""**Conversation Summary**

This learning session covered {len(user_messages)} main topics:
{'• ' + chr(10) + '• '.join(topics) if topics else '• Various academic subjects'}

**Key Learning Points:**
• Structured explanations with step-by-step breakdowns
• Critical thinking approaches to complex concepts
• Real-world applications and examples
• Connections between related ideas

**Areas for Further Study:**
• Advanced applications of discussed concepts
• Related topics that build on this foundation
• Practical exercises to reinforce learning

**Overall Progress:**
This conversation demonstrates good engagement with academic material and shows effective use of questioning techniques for deeper understanding."""

    return jsonify({
        "conversationId": conversation_id,
        "summary": summary
    })

def generate_mock_response(message):
    """Generate mock AI responses based on message content"""
    message_lower = message.lower()
    
    if 'photosynthesis' in message_lower:
        return """**Photosynthesis: Step-by-Step Process**

Photosynthesis is the process by which plants convert light energy into chemical energy. Here's how it works:

**1. Light Absorption**
• Chlorophyll in chloroplasts captures sunlight
• Light energy excites electrons in chlorophyll molecules
• This energy drives the photosynthetic reactions

**2. Water Splitting (Photolysis)**
• Water molecules (H₂O) are split into:
  - Oxygen gas (O₂) - released as waste
  - Hydrogen ions (H⁺) - used in next steps
  - Electrons - replace those lost by chlorophyll

**3. Carbon Fixation (Calvin Cycle)**
• Carbon dioxide (CO₂) from air enters through stomata
• CO₂ combines with RuBP (5-carbon sugar)
• Through enzyme RuBisCO, glucose is produced

**4. Energy Storage**
• Glucose is converted to starch for storage
• Some glucose used immediately for cellular respiration
• Oxygen released improves air quality

**Key Equation:**
6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂

This process is fundamental to life on Earth, providing oxygen and food for nearly all organisms."""

    elif 'calculus' in message_lower or 'derivative' in message_lower:
        return """**Calculus Derivatives: Fundamental Concepts**

Derivatives measure how functions change - they're the mathematical way to describe rates of change.

**What is a Derivative?**
• Instantaneous rate of change at a specific point
• Slope of the tangent line to a curve
• How much y changes when x changes by a tiny amount

**Basic Derivative Rules:**

**1. Power Rule**
If f(x) = xⁿ, then f'(x) = nx^(n-1)
• Example: If f(x) = x³, then f'(x) = 3x²

**2. Constant Rule**
If f(x) = c (constant), then f'(x) = 0
• Derivative of any constant is zero

**3. Sum Rule**
(f + g)' = f' + g'
• Derivative of sum equals sum of derivatives

**4. Product Rule**
(fg)' = f'g + fg'
• For multiplying functions

**5. Chain Rule**
f(g(x))' = f'(g(x)) × g'(x)
• For composite functions

**Geometric Interpretation:**
• Positive derivative = function increasing
• Negative derivative = function decreasing
• Zero derivative = horizontal tangent (possible maximum/minimum)

**Applications:**
• Physics: velocity is derivative of position
• Economics: marginal cost/revenue
• Biology: population growth rates
• Engineering: optimization problems

Understanding derivatives is crucial for advanced mathematics and sciences!"""

    elif 'world war' in message_lower:
        return """**World War I: Main Causes and Overview**

World War I (1914-1918) was a global conflict with complex causes:

**Immediate Trigger:**
• Assassination of Archduke Franz Ferdinand of Austria-Hungary (June 28, 1914)
• This activated a web of alliances and tensions

**Underlying Causes:**

**1. Alliance System**
• Triple Alliance: Germany, Austria-Hungary, Italy
• Triple Entente: Britain, France, Russia
• Created two opposing camps that pulled countries into conflict

**2. Imperialism**
• Competition for colonies and resources
• National pride and prestige conflicts
• Economic rivalries between major powers

**3. Militarism**
• Arms race, especially between Britain and Germany
• Military planning that made war seem inevitable
• Cult of military strength in European societies

**4. Nationalism**
• Ethnic tensions in multi-ethnic empires
• Desire for national self-determination
• Competitive national pride

**Key Events:**
• July 1914: Austria-Hungary declares war on Serbia
• August 1914: Germany invades Belgium, bringing Britain into war
• 1915-1917: Stalemate on Western Front
• 1917: Russia exits, US enters
• November 1918: Armistice signed

**Consequences:**
• 16+ million deaths
• Fall of empires (German, Austro-Hungarian, Ottoman, Russian)
• Treaty of Versailles (1919)
• Set stage for World War II

This conflict reshaped the modern world order fundamentally."""

    else:
        return f"""**Study Response to: {message}**

I understand you're asking about "{message}". Here's a structured approach to learning about this topic:

**Step 1: Define Key Terms**
Let's clarify the fundamental concepts involved in your question.

**Step 2: Provide Context**
Understanding the background and significance of this topic.

**Step 3: Break Down Components**
Analyzing the different aspects systematically.

**Step 4: Give Examples**
Concrete illustrations to make abstract concepts clearer.

**Step 5: Connect to Broader Concepts**
How this relates to other areas of knowledge.

**Step 6: Identify Applications**
Real-world uses and implications.

**Questions to Consider:**
• What specifically would you like to understand better?
• Do you have a particular aspect of this topic in mind?
• What's your current level of familiarity with this subject?

Feel free to ask follow-up questions or request more detailed explanations about any particular aspect!"""

if __name__ == '__main__':
    print("🚀 Starting Study Bot Mock Backend...")
    print("📊 API available at: http://localhost:3001/api")
    print("✅ Health check: http://localhost:3001/api/health")
    print("🔄 Press Ctrl+C to stop the server")
    app.run(host='localhost', port=3001, debug=True)

require('dotenv').config();
const OpenAI = require('openai');

class OpenAIConfig {
  constructor() {
    this.apiKey = process.env.OPENAI_API_KEY;
    
    if (!this.apiKey) {
      console.warn('OPENAI_API_KEY not found in environment variables. AI features will be disabled.');
      this.openai = null;
    } else {
      this.openai = new OpenAI({
        apiKey: this.apiKey,
      });
    }
  }

  async generateResponse(messages, conversationContext = []) {
    if (!this.openai) {
      return "I'm sorry, but I'm not configured to use AI capabilities. Please set up your OpenAI API key in the environment variables.";
    }

    try {
      // Build the prompt with context and instructions
      const systemPrompt = this.buildSystemPrompt(conversationContext);
      
      const chatMessages = [
        { role: "system", content: systemPrompt },
        ...messages
      ];

      const response = await this.openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: chatMessages,
        temperature: 0.7,
        max_tokens: 1000,
      });

      return response.choices[0].message.content;
    } catch (error) {
      console.error('OpenAI API error:', error);
      return "I'm sorry, I'm having trouble processing your request right now. Please try again later.";
    }
  }

  buildSystemPrompt(conversationContext) {
    let prompt = `You are Study Bot, an AI academic assistant designed to support student learning.

Your primary goals:
1. Help students understand concepts deeply
2. Provide structured and step-by-step explanations
3. Offer practical examples and code snippets when relevant
4. Encourage critical thinking

When responding:
- Use markdown formatting for clarity
- Use bullet points or numbered steps for explanations
- Provide short summaries at the end of complex answers
- If the user seems confused, simplify the explanation
- Do not fabricate information
- If unsure, say you are not certain and suggest reliable learning resources

Previous conversation context:
${conversationContext.length > 0 
  ? conversationContext.map(msg => `${msg.role}: ${msg.content}`).join('\n')
  : 'No previous context available'
}`;

    return prompt;
  }

  extractTopics(text) {
    // Simple topic extraction - in a real implementation, you might use NLP
    const topicKeywords = [
      'math', 'science', 'history', 'literature', 'programming', 'biology', 
      'chemistry', 'physics', 'calculus', 'algebra', 'geometry', 'statistics',
      'computer science', 'economics', 'psychology', 'philosophy', 'language'
    ];
    
    const topics = [];
    const textLower = text.toLowerCase();
    
    topicKeywords.forEach(keyword => {
      if (textLower.includes(keyword)) {
        topics.push(keyword);
      }
    });
    
    return topics;
  }
}

module.exports = new OpenAIConfig();

# Code Examples - Level Switching Implementation

## Frontend Level Switching Logic

### Switch Level Function
```javascript
// Switch level for current chat
function switchLevel(newLevel) {
  if (!currentChatId || !['L1', 'L2', 'L3'].includes(newLevel)) return;
  
  currentLevel = newLevel;
  
  // Store level with chat
  if (chats[currentChatId]) {
    chats[currentChatId].level = newLevel;
    localStorage.setItem('chats', JSON.stringify(chats));
  }
  
  updateLevelButtonUI();
  
  // Show level change notification in chat
  removeHero();
  const notificationDiv = document.createElement('div');
  notificationDiv.className = 'message system-message';
  notificationDiv.innerHTML = `<em>Analyst level switched to <strong>${newLevel}</strong>. Responses will now reflect ${newLevel === 'L1' ? 'basic guidance' : newLevel === 'L2' ? 'investigation details' : 'advanced threat hunting'} depth.</em>`;
  chatHistory.appendChild(notificationDiv);
  chatHistory.scrollTop = chatHistory.scrollHeight;
}
```

### Level Command Detection
```javascript
// Check for level switching commands in sendMessage()
async function sendMessage() {
  const question = queryInput.value.trim();
  if (!question) return;

  // Check for level switching commands
  const levelSwitchMatch = question.match(/^switch\s+to\s+(l[123]|L[123])/i);
  if (levelSwitchMatch) {
    const newLevel = levelSwitchMatch[1].toUpperCase();
    queryInput.value = '';
    switchLevel(newLevel);
    return;
  }

  // Alternative syntax: just "L1", "L2", or "L3"
  if (/^l[123]$/i.test(question)) {
    const newLevel = question.toUpperCase();
    queryInput.value = '';
    switchLevel(newLevel);
    return;
  }

  // ... rest of message sending logic
}
```

### Sending Level with Query
```javascript
// In sendMessage() when making API call
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    question: question,
    level: currentLevel  // <-- Send current level
  })
});
```

## Backend Implementation

### Request Model
```python
from pydantic import BaseModel

class ChatQuery(BaseModel):
    question: str
    level: str = "L1"  # Default level if not provided
```

### API Endpoint
```python
@app.post("/api/chat")
async def chat(query: ChatQuery):
    """API endpoint for chatbot queries"""
    try:
        # Pass both question and level to chatbot
        response = get_chatbot_response(query.question, query.level)
        return JSONResponse({"success": True, "response": response})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)
```

### LLM Response Function
```python
def get_chatbot_response(question: str, user_level: str = None) -> str:
    """Get chatbot response for a given question.
    
    If user_level is provided, use that. Otherwise, auto-detect the question level.
    """
    # Use provided level or auto-detect
    if user_level and user_level in ["L1", "L2", "L3"]:
        level = user_level
    else:
        level = detect_question_level(question)  # Fallback
    
    template = """
    You are 'Netty', a SOC AI Assistant supporting L1, L2, and L3 analysts.

    Analyst level: {level}

    [Rest of prompt template with level-specific rules...]
    """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    # Retrieve context
    docs = retriever.invoke(question)
    context_api = "\n\n".join(d.page_content for d in docs)
    
    # Build final prompt with level
    result = chain.invoke({
        "level": level,          # <-- Level variable in prompt
        "context": context_api,
        "question": question
    })
    
    return result
```

## HTML Structure

### Level Selector Component
```html
<div class="controls">
  <div class="level-selector">
    <span class="level-label">Analyst Level:</span>
    <div class="level-buttons">
      <button class="level-btn" data-level="L1" id="levelL1">L1</button>
      <button class="level-btn" data-level="L2" id="levelL2">L2</button>
      <button class="level-btn" data-level="L3" id="levelL3">L3</button>
    </div>
  </div>
  <div class="input-row">
    <input type="text" id="queryInput" 
           placeholder="What would you like to know?" />
    <button class="send" id="sendBtn">➤</button>
  </div>
</div>
```

## CSS Styling

### Level Buttons
```css
.level-selector {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  max-width: 980px;
}

.level-label {
  color: rgba(255,255,255,0.7);
  font-size: 14px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.level-buttons {
  display: flex;
  gap: 8px;
}

.level-btn {
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.7);
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.2s ease;
  text-transform: uppercase;
}

.level-btn:hover {
  background: rgba(255,255,255,0.12);
  color: rgba(255,255,255,0.9);
  border-color: rgba(255,255,255,0.2);
}

.level-btn.active {
  background: rgba(34,139,34,0.6);
  border-color: rgba(34,139,34,0.9);
  color: #ffffff;
  box-shadow: 0 0 12px rgba(34,139,34,0.4);
}
```

### System Notification Message
```css
.system-message {
  background: rgba(100,149,237,0.15) !important;
  border: 1px solid rgba(100,149,237,0.4) !important;
  color: rgba(200,200,255,0.9) !important;
  max-width: 100% !important;
  margin: 12px 0 !important;
  padding: 12px 16px !important;
}
```

## State Management

### Chat Object with Level
```javascript
chats[chatId] = {
  id: chatId,                        // Unique chat ID
  name: 'Chat 1',                    // Display name
  timestamp: '1/22/2026 2:30 PM',   // When created
  level: 'L1',                       // <-- Current level (NEW)
  messages: [                        // Chat messages
    {
      type: 'user-message',
      content: 'What is phishing?'
    },
    {
      type: 'bot-message',
      content: 'Phishing is...'
    }
  ]
}
```

### Level Persistence
```javascript
// On page load
let currentLevel = chats[currentChatId].level || 'L1';

// When switching levels
chats[currentChatId].level = newLevel;
localStorage.setItem('chats', JSON.stringify(chats));

// When loading different chat
function loadChat(chatId) {
  currentLevel = chats[chatId].level || 'L1';
  updateLevelButtonUI();
  // ... rest of load logic
}
```

## Usage Flow Diagram

```javascript
// User clicks level button
document.querySelectorAll('.level-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const newLevel = btn.getAttribute('data-level');
    switchLevel(newLevel);  // L1, L2, or L3
  });
});

// User types level command
const levelSwitchMatch = question.match(/^switch\s+to\s+(l[123]|L[123])/i);
if (levelSwitchMatch) {
  switchLevel(levelSwitchMatch[1].toUpperCase());
}

// switchLevel() then:
// 1. Updates currentLevel variable
// 2. Saves to localStorage
// 3. Updates button UI (active state)
// 4. Shows notification in chat
// 5. Future queries use new level
```

## Error Handling

### Level Validation
```python
# In get_chatbot_response()
if user_level and user_level in ["L1", "L2", "L3"]:
    level = user_level
else:
    # Falls back to auto-detection if invalid
    level = detect_question_level(question)
```

### Frontend Validation
```javascript
// In switchLevel()
if (!currentChatId || !['L1', 'L2', 'L3'].includes(newLevel)) {
    return;  // Silently ignore invalid input
}
```

---

## Integration Points

### Adding to Existing Code

**No breaking changes!** The level parameter is optional:
- Old calls: `get_chatbot_response(question)` → Still works (auto-detects)
- New calls: `get_chatbot_response(question, 'L2')` → Uses specified level

### Testing Level Logic

```python
# Test auto-detection fallback
response = get_chatbot_response("What is MITRE ATT&CK?")  # L1
response = get_chatbot_response("How to threat hunt?")    # L3

# Test with explicit level
response = get_chatbot_response("What is phishing?", "L2")  # Always L2
response = get_chatbot_response("Any question", "L3")       # Always L3
```

---

This implementation provides complete level-switching functionality while maintaining backward compatibility and clean code organization.

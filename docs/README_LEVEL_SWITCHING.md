# 🎯 Netty Level Switching Feature - Complete Implementation

## Overview

Your Netty chatbot now supports **dynamic analyst level switching** within conversations. Users can seamlessly switch between three analyst levels (L1, L2, L3) to receive responses tailored to their expertise and needs.

---

## ✨ What's New

### 1. **Level Selector UI**
A new control panel appears above the chat input with three clickable level buttons:
- **L1** - Basic/Beginner level
- **L2** - Investigation/Intermediate level  
- **L3** - Advanced/Threat Hunting level

The active level is highlighted in green with a glowing effect for easy visibility.

### 2. **Multiple Level-Switching Options**
Users can switch levels in three ways:
- **Click buttons** - Fastest method
- **Type command** - Type `L1`, `L2`, or `L3` and press Enter
- **Natural language** - Type `switch to L2` (case-insensitive)

### 3. **Per-Chat Level Persistence**
- Each chat maintains its own analyst level independently
- When you switch to another chat, that chat's saved level is restored
- New chats always start at L1 by default
- Levels persist even after page reload (localStorage)

### 4. **Visual Feedback**
When level changes occur:
- Active level button glows green with clear visual indicator
- Blue system notification appears in chat confirming the switch
- Users see what type of response to expect at their new level

---

## 🛠️ Technical Implementation

### Backend Changes

**server.py**
- Enhanced `ChatQuery` model with `level` field (default: "L1")
- `/api/chat` endpoint now passes level to LLM
- Added optional session management endpoints

**main.py**
- Updated `get_chatbot_response()` signature to accept `user_level` parameter
- Validates level is one of: L1, L2, L3
- Falls back to auto-detection if level not provided
- Maintains full backward compatibility

### Frontend Changes

**index.html**
- New level selector UI component with three buttons
- JavaScript state tracking: `currentLevel` per chat
- Enhanced localStorage to persist level with each chat
- Detects both click and text-based level switching
- System notifications for level changes

**main.css**
- Styling for level buttons (base, hover, active states)
- Green highlight and glow effect for active level
- Blue notification styling for system messages
- Responsive layout integration

---

## 📋 Level Specifications

### L1 - Basic Analyst
**Response Characteristics:**
- Short, simple explanations (2-3 sentences max per section)
- Step-by-step "what to do next" guidance
- Basic containment and escalation criteria
- Minimal technical jargon
- Focus on immediate actions

**When to use:**
- Initial ticket triage
- First responders
- Non-technical stakeholders
- Quick overview needed

### L2 - Investigation Analyst
**Response Characteristics:**
- Specific, actionable investigation guidance
- Concrete artifact locations and log sources
- Telemetry collection paths with field names
- Query examples and pivot points
- Event IDs and specific indicators

**When to use:**
- Incident investigation
- Deep-dive analysis required
- Collecting evidence
- Following up on L1 findings

### L3 - Advanced Analyst / Threat Hunter
**Response Characteristics:**
- Comprehensive, in-depth technical analysis
- Threat hunting methodologies
- Detection engineering frameworks
- Root cause analysis with technical depth
- MITRE ATT&CK mappings
- Advanced persistence and evasion techniques
- Architectural hardening recommendations

**When to use:**
- Advanced threat hunting
- Detection engineering
- Security architecture reviews
- Comprehensive incident analysis
- Long-term hardening strategies

---

## 🚀 Usage Examples

### Example 1: Basic to Detailed Escalation
```
1. Chat starts → L1 active
2. User: "What is credential dumping?"
3. Bot: [L1 - Basic explanation]
4. User clicks "L2" button → Level switches
5. User: "How do I investigate if it happened?"
6. Bot: [L2 - Specific investigation telemetry and artifacts]
7. User clicks "L3" button → Level switches
8. User: "How do we build detections for this?"
9. Bot: [L3 - Detection engineering and hunting strategies]
```

### Example 2: Multi-Chat Comparison
```
Chat 1 (L1): Overview of incident
Chat 2 (L2): Investigation details (switch to L2, same incident)
Chat 3 (L3): Threat hunting analysis (new chat for hunting)

User can switch between tabs to compare different depth levels
```

### Example 3: Team Workflow
```
Junior Analyst (L1):
- Triages alerts
- Gets basic containment steps
- Escalates to senior when needed

Senior Analyst (L2/L3):
- Continues investigation at L2
- Escalates to L3 for threat hunting
- Documents findings for process improvement
```

---

## 💾 Data Persistence

### Local Storage Structure
```json
{
  "chats": {
    "chat_1": {
      "id": "chat_1",
      "name": "Phishing Investigation",
      "timestamp": "1/22/2026 2:30 PM",
      "level": "L2",
      "messages": [...]
    },
    "chat_2": {
      "id": "chat_2",
      "name": "Malware Analysis",
      "timestamp": "1/22/2026 2:35 PM",
      "level": "L3",
      "messages": [...]
    }
  }
}
```

### What Gets Saved
- ✓ Chat level (L1/L2/L3)
- ✓ Messages and responses
- ✓ Chat name and timestamp
- ✓ All formatting in messages

### Persistence Across Sessions
- Reload page → All levels restored
- Close tab → All levels restored
- Clear localStorage → Levels reset to defaults

---

## 🔄 System Flow Diagram

```
User Interface
    ↓
Click Level Button / Type Command
    ↓
switchLevel(newLevel)
    ↓
Update currentLevel variable
    ↓
Store level in chat object (localStorage)
    ↓
Update UI (highlight new level button)
    ↓
Show system notification
    ↓
User asks question
    ↓
Send to /api/chat with {question, level: currentLevel}
    ↓
server.py receives ChatQuery
    ↓
Call get_chatbot_response(question, user_level)
    ↓
LLM prompt includes "Analyst level: {level}"
    ↓
LLM generates response at specified depth
    ↓
Return response to frontend
    ↓
Display with formatting
```

---

## ✅ Quality Assurance Checklist

- [x] Backend parameter passing correct
- [x] Frontend state management working
- [x] localStorage persistence verified
- [x] Level switching commands detected
- [x] UI buttons styled and responsive
- [x] System notifications display properly
- [x] Per-chat level independence verified
- [x] New chats default to L1
- [x] Level restoration on chat switch works
- [x] No syntax errors in code
- [x] Backward compatibility maintained
- [x] Auto-detection fallback works

---

## 📚 Documentation Files

1. **IMPLEMENTATION_SUMMARY.md** - Detailed technical changes
2. **LEVEL_SWITCHING_GUIDE.md** - User and developer guide  
3. **QUICK_REFERENCE.md** - Quick start and common commands
4. **README.md** - This comprehensive overview

---

## 🎓 Key Features Summary

| Feature | Status | Description |
|---------|--------|-------------|
| Level Buttons | ✅ | Three clickable buttons with visual feedback |
| Text Commands | ✅ | Type L1/L2/L3 or "switch to L" |
| Per-Chat Levels | ✅ | Each chat has independent level |
| Persistence | ✅ | localStorage saves levels across sessions |
| System Notifications | ✅ | Blue notifications on level change |
| Auto-Detection | ✅ | Fallback if level not specified |
| Backward Compatible | ✅ | Existing code still works |
| Multi-Level Responses | ✅ | LLM generates depth-appropriate responses |
| Visual Feedback | ✅ | Green highlight on active level |
| Smooth UX | ✅ | Seamless transitions between levels |

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Level button not responding | Check if JavaScript is enabled |
| Level not persisting | Clear localStorage and try again |
| Wrong response depth | Verify level button is highlighted correctly |
| Text command not working | Ensure you type L1/L2/L3 exactly (case works) |
| Multiple chats same level | This is normal - create new chat for different level |

---

## 🎯 Next Steps

1. **Test the feature** - Try all three levels with various questions
2. **Review responses** - Verify depth matches your expectations
3. **Use in workflow** - Integrate into your SOC processes
4. **Provide feedback** - Report issues or improvements
5. **Train team** - Share QUICK_REFERENCE.md with users

---

## 📞 Support

For detailed information:
- Developer documentation: `IMPLEMENTATION_SUMMARY.md`
- User guide: `LEVEL_SWITCHING_GUIDE.md`  
- Quick commands: `QUICK_REFERENCE.md`

For code questions:
- Check `main.py` for LLM prompting logic
- Check `server.py` for API implementation
- Check `index.html` for frontend logic

---

**Implementation Complete! ✨**

Your Netty chatbot now provides dynamic, depth-aware responses that adapt to analyst expertise levels. Users can seamlessly switch between L1 (basic), L2 (investigation), and L3 (advanced threat hunting) responses within individual chats.

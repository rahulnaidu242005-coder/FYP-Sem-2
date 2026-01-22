# Level Switching Feature Guide

## Overview
The Netty chatbot now supports dynamic analyst level switching within individual chats. Users can switch between L1 (basic), L2 (investigation), and L3 (advanced threat hunting) to receive responses tailored to their expertise level.

## Features

### 1. Level Selector UI
- **Location**: Above the message input area
- **Display**: Three clickable buttons labeled "L1", "L2", and "L3"
- **Visual Feedback**: The active level is highlighted in green with a glowing effect
- **Default Level**: Each new chat starts at L1

### 2. How to Switch Levels

#### Method 1: Click Level Buttons
Simply click one of the level buttons (L1, L2, L3) above the input field to switch the current chat's analyst level.

#### Method 2: Text Commands
Users can also type level switching commands:
- Type `L1`, `L2`, or `L3` and press Enter to switch
- Or type `switch to L1`, `switch to L2`, or `switch to L3` (case-insensitive)

### 3. Per-Chat Level Persistence
- Each chat maintains its own analyst level independently
- When you switch to a different chat, the level switches to that chat's saved level
- When you create a new chat, it always starts at L1

### 4. Response Depth by Level

**L1 - Basic Analyst**
- Short but useful explanations (2-3 sentences max per section)
- Step-by-step "what to do next" guidance
- Basic containment guidance and escalation criteria
- Simple language, minimal technical jargon

**L2 - Investigation Analyst**
- Specific, operational, actionable investigation guidance
- Concrete artifact locations and log sources
- Specific telemetry to collect and pivot points
- Query examples and field names to search for
- NO threat hunting or detection engineering

**L3 - Advanced/Threat Hunting Analyst**
- Comprehensive, in-depth analysis with technical depth
- Threat hunting methodologies and behavioral analysis
- Detection engineering frameworks and correlation logic
- Root cause analysis and architectural hardening
- MITRE ATT&CK mappings and attack variants
- Advanced evasion techniques and persistence mechanisms

## System Features

### Level Change Notifications
When you switch levels, a system notification appears in the chat showing the new level and what to expect from responses.

### Level Persistence
- Levels are saved with each chat in local storage
- When you reload the page, your chat levels are maintained

### Auto-Detection (Fallback)
If no level is explicitly set, the system can auto-detect question complexity based on keywords:
- L3 keywords: "threat hunt", "root cause", "detection engineering", "hunting", "advanced"
- L2 keywords: "investigate", "artifact", "telemetry", "pivot", "evidence"
- L1: Default for basic questions

## Backend Implementation

### Updated Files:
1. **server.py**: 
   - Now accepts and passes `level` parameter to the chatbot
   - Extended API endpoints for level management

2. **main.py**: 
   - `get_chatbot_response()` now accepts optional `user_level` parameter
   - Falls back to auto-detection if level not provided

3. **index.html**: 
   - Added level selector UI buttons
   - JavaScript handles level switching and persistence
   - Detects both click and text-based level switching commands
   - Stores level with each chat in localStorage

4. **main.css**: 
   - New styles for level buttons
   - Green highlight for active level
   - System message styling for level change notifications

## Example Usage

1. **Start a chat** → Begins at L1
2. **Ask a question** → Receives L1-depth response
3. **Click L2 button** → Level switches, notification shows in chat
4. **Ask another question** → Receives L2-depth response with investigation details
5. **Type "L3" in input** → Alternatively, switch to L3
6. **Ask a question** → Receives comprehensive L3-depth analysis
7. **Switch chats** → New chat loads with its saved level
8. **Create new chat** → Always starts at L1

## Technical Details

### Level Parameter Flow:
```
Frontend (currentLevel) 
    → JSON payload to /api/chat 
    → server.py (ChatQuery.level) 
    → main.get_chatbot_response(question, level) 
    → LLM with level-specific prompt
```

### Storage:
- **localStorage**: Chat metadata including level, messages, name
- **In-memory**: Chat levels dictionary in server (optional, for future expansion)

### Compatibility:
- Works with existing auto-detection fallback
- No breaking changes to existing API
- Fully backward compatible

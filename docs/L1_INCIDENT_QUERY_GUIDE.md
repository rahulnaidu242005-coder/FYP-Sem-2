# L1 Incident Query Access Control - Implementation Guide

## Overview

The system has been updated to support **tier-aware incident query access control**. This means:

- **L1 analysts** can now ask **L1-level incident questions** (e.g., "What does this incident mean? Should I escalate it?")
- **L1 analysts** are **blocked from L2/L3 incident questions** with clear escalation messages
- **L2/L3 analysts** can query incidents at their authorized tier levels

This enables L1 analysts to get immediate, actionable insights about incidents while maintaining security through proper escalation for deeper analysis.

---

## How It Works

### 1. Incident Question Detection

The system automatically detects if a question is asking about an incident using keywords:

```python
incident_keywords = [
    "incident", "alert", "what do", "what does", "meaning", "mean",
    "escalate", "severity", "risk", "should i", "should we", 
    "do i need", "what should", "urgent", "priority", "happen"
]
```

**Example:**
- ✅ "What does this incident mean?" → Recognized as incident question
- ✅ "Should I escalate this alert?" → Recognized as incident question
- ❌ "What is MITRE ATT&CK?" → Regular question (not incident-specific)

### 2. Incident Question Tier Detection

Once an incident question is detected, the system determines what tier level is required:

#### L1 Keywords (Basic Understanding)
```
"what do", "what does", "meaning", "mean", "escalate", 
"severity", "should i", "should we", "urgent", "priority"
```
**Use case:** Understanding the incident overview and escalation decision

#### L2 Keywords (Investigation)
```
"investigate", "investigation", "how to investigate", "validate",
"evidence", "check logs", "telemetry", "artifacts", "step by step",
"what to check", "where to look", "timeline"
```
**Use case:** Detailed investigation and evidence collection

#### L3 Keywords (Advanced Hunting)
```
"threat hunt", "how to hunt", "hunting strategy", "root cause",
"detection strategy", "persistence", "evasion", "forensic",
"containment", "remediation", "hardening"
```
**Use case:** Threat hunting, root cause analysis, detection engineering

### 3. Privilege Enforcement

The system checks if the user's current level allows them to query at the required tier:

```
User Level >= Required Tier → Allow
User Level < Required Tier → Show Escalation Message
```

**Example Flow:**
- L1 user asks L1 incident question → ✅ Allow, provide analysis
- L1 user asks L2 incident question → ❌ Block, show escalation message
- L2 user asks L2 incident question → ✅ Allow, provide analysis

---

## API Usage

### POST /api/chat

The `/api/chat` endpoint now accepts optional incident data:

#### Request Format
```json
{
  "question": "What do these incidents mean? Should I escalate them?",
  "level": "L1",
  "incident": {
    "id": "INC-126",
    "title": "Suspicious PowerShell Activity",
    "priority": "HIGH",
    "riskScore": 8.7,
    "status": "ACTIVE",
    "categories": ["Malware", "Persistence"],
    "alertMeta": {
      "user": "CORP\\jsmith",
      "hostname": "DESKTOP-ABC123"
    }
  }
}
```

#### Success Response (L1 asking L1 question)
```json
{
  "success": true,
  "response": "[L1 incident analysis from IncidentAnalyzer]\n\n**What This Incident Means:**\n- Suspicious PowerShell activity detected..."
}
```

#### Escalation Response (L1 asking L2 question)
```json
{
  "success": true,
  "response": "**Authorization Required for Incident Analysis**\n\nYour current analyst level is **L1**, but this incident question requires **L2** access..."
}
```

#### Python Usage Example
```python
from main import get_chatbot_response

incident = {
    "id": "INC-126",
    "title": "Suspicious Activity",
    "priority": "HIGH"
}

# L1 user asking L1 incident question (succeeds)
response = get_chatbot_response(
    question="What does this incident mean?",
    user_level="L1",
    incident_data=incident
)
print(response)  # Prints L1 analysis

# L1 user asking L2 incident question (escalation)
response = get_chatbot_response(
    question="How do I investigate this incident?",
    user_level="L1",
    incident_data=incident
)
print(response)  # Prints escalation message
```

---

## Question Examples by Tier

### L1 Questions (Allowed for L1 analysts)
- "What do these incidents mean?"
- "What does this alert mean and should I escalate it?"
- "Is this incident urgent? What priority is it?"
- "What should I do with this incident?"
- "What are the main risks in this incident?"

### L2 Questions (Escalation required for L1)
- "How do I investigate this incident?"
- "What evidence should I collect?"
- "Where should I look for more data?"
- "What artifacts should I validate?"
- "Can you walk me through investigation steps?"

### L3 Questions (Escalation required for L1)
- "Show me a threat hunting strategy for this incident"
- "How would you approach root cause analysis?"
- "What hardening recommendations would you suggest?"
- "How could an attacker evade detection?"
- "What's the detection strategy for this type of incident?"

---

## Escalation Message Format

When a user doesn't have sufficient privileges, they see a clear escalation message:

```
**Authorization Required for Incident Analysis**

Your current analyst level is **L1**, but this incident question requires **L2** access.

**What you're asking about**: L2 tier incident analysis

**Incident**: INC-126

**Action Required:**
- Contact your SOC manager or team lead
- Request escalation to **L2** analyst level
- Once approved, you'll be able to access this incident analysis

**Current Access:**
- Level L1: Basic incident overview and escalation guidance
- Level L2+: Restricted - requires escalation
```

---

## Implementation Details

### Modified Files

#### `main.py`
**New Functions Added:**
- `is_incident_question(question)`: Detects if question is about incidents
- `detect_incident_question_level(question)`: Determines required tier (L1/L2/L3)

**Modified Functions:**
- `get_chatbot_response()`: Now accepts optional `incident_data` parameter
  - Checks if question is incident-related
  - Validates user's tier against required tier
  - Routes to incident analyzer or regular chatbot

#### `UI2/server.py`
**Modified Models:**
- `ChatQuery`: Added optional `incident: Optional[Dict[str, Any]]` field

**Modified Endpoints:**
- `/api/chat`: Now passes incident data to `get_chatbot_response()`

### Keyword Configuration

To customize what keywords trigger each tier, edit the keyword lists in `main.py`:

```python
# Line ~22: L3 keywords for incidents
l3_incident_keywords = [
    "threat hunt", "how to hunt", "how would you hunt", "hunting strategy",
    # ... add more here
]

# Line ~37: L2 keywords for incidents
l2_incident_keywords = [
    "investigate", "investigation", "how to investigate", "validate", 
    # ... add more here
]
```

---

## Testing

### Run Example Script
```bash
python incident_query_example.py
```

This demonstrates all scenarios:
- L1 asking L1 incident questions (success)
- L1 asking L2/L3 incident questions (escalation)
- L2/L3 asking their authorized tier questions (success)
- Regular questions (no incident data)

### Quick Python Test
```python
from main import get_chatbot_response

incident = {"id": "INC-126", "title": "Test", "priority": "HIGH"}

# Test 1: L1 user, L1 question, with incident
response = get_chatbot_response(
    "What does this incident mean?",
    user_level="L1",
    incident_data=incident
)
assert "Authorization Required" not in response  # Should succeed

# Test 2: L1 user, L2 question, with incident
response = get_chatbot_response(
    "How do I investigate this incident?",
    user_level="L1",
    incident_data=incident
)
assert "Authorization Required" in response  # Should be escalated
```

---

## Backward Compatibility

**Non-incident queries work exactly as before:**
- Regular questions (no incident data) use the original tier detection
- Original escalation logic still applies for L2/L3 non-incident questions
- Existing API clients work without changes (incident field is optional)

---

## Troubleshooting

### Issue: L1 user can't query L1 incident questions

**Solution:** Verify the question contains incident keywords:
```python
from main import is_incident_question
print(is_incident_question("Your question here"))  # Should be True
```

### Issue: Question being classified as wrong tier

**Solution:** Check which keywords matched:
```python
from main import detect_incident_question_level
print(detect_incident_question_level("Your question here"))  # Shows detected tier
```

### Issue: Incident data not being passed to API

**Solution:** Ensure ChatQuery includes incident field:
```json
{
  "question": "What does this mean?",
  "level": "L1",
  "incident": { "id": "INC-126" }
}
```

---

## Summary

| Feature | Before | After |
|---------|--------|-------|
| L1 incident queries | ❌ Blocked | ✅ L1 questions allowed |
| L2 escalation | ❌ Not incident-aware | ✅ Incident-aware escalation |
| API support | ❌ No incident field | ✅ Accepts incident data |
| User experience | ❌ Confusing blocks | ✅ Clear tier-based access |


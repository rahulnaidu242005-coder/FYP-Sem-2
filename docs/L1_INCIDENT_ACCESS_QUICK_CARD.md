# L1 Incident Query Access Control - Quick Reference

## What Changed?

L1 analysts can now ask L1-level questions about incidents while being blocked from L2/L3 incident analysis with automatic escalation messages.

## How to Use

### For Frontend/UI Integration

Include incident data when posting to `/api/chat`:

```javascript
// Example: L1 user asking about an incident
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: "What do these incidents mean? Should I escalate them?",
    level: "L1",
    incident: {
      id: "INC-126",
      title: "Suspicious PowerShell Activity",
      priority: "HIGH",
      riskScore: 8.7
    }
  })
});
```

### For Python Usage

```python
from main import get_chatbot_response

incident = {
    "id": "INC-126",
    "title": "Suspicious Activity",
    "priority": "HIGH"
}

# ✅ L1 asking L1 incident question - WORKS
response = get_chatbot_response(
    question="What does this incident mean?",
    user_level="L1",
    incident_data=incident
)

# ❌ L1 asking L2 incident question - ESCALATION
response = get_chatbot_response(
    question="How do I investigate this?",
    user_level="L1",
    incident_data=incident
)
```

## Tier Recognition Keywords

### L1 Keywords (Allowed for L1)
```
what do, what does, meaning, mean, escalate, 
severity, should i, should we, urgent, priority
```

### L2 Keywords (Escalation Required)
```
investigate, how to investigate, evidence, 
check logs, where to look, artifacts, telemetry
```

### L3 Keywords (Escalation Required)
```
threat hunt, hunting strategy, root cause, 
detection strategy, forensic, hardening
```

## Scenarios

| User Level | Question Type | Incident Data | Result |
|------------|---------------|---------------|--------|
| L1 | L1 incident question | ✅ Provided | ✅ Analysis given |
| L1 | L2 incident question | ✅ Provided | ❌ Escalation msg |
| L1 | L3 incident question | ✅ Provided | ❌ Escalation msg |
| L2 | L2 incident question | ✅ Provided | ✅ Analysis given |
| L3 | L3 incident question | ✅ Provided | ✅ Analysis given |
| L1 | Any | ❌ Not provided | Regular question logic |

## Key Features

✅ **Automatic Tier Detection** - No configuration needed, keywords detected automatically

✅ **Clear Escalation Messages** - Users understand what they need and why

✅ **Backward Compatible** - Regular questions work exactly as before

✅ **API Ready** - Simply add `incident` field to existing `/api/chat` requests

✅ **No Breaking Changes** - `incident` field is optional

## Testing

Run the example script to see all scenarios:
```bash
python incident_query_example.py
```

## Customization

Edit keyword lists in `main.py` around lines 22-56:

```python
# L3 keywords (line ~22)
l3_incident_keywords = ["threat hunt", "hunting strategy", ...]

# L2 keywords (line ~37)
l2_incident_keywords = ["investigate", "evidence", ...]

# L1 keywords are implicit - anything not matching L2/L3 defaults to L1
```

## Implementation Summary

**Modified Files:**
- ✅ `main.py` - Added 2 new functions + modified 1 function
- ✅ `UI2/server.py` - Updated ChatQuery model + /api/chat endpoint

**New Functions:**
- `is_incident_question()` - Detects incident queries
- `detect_incident_question_level()` - Determines required tier

**Updated Functions:**
- `get_chatbot_response()` - Now handles tier-aware incident analysis

**New Endpoint Capability:**
- `/api/chat` - Now accepts optional `incident` field

## Escalation Message Example

When L1 user exceeds privileges:
```
**Authorization Required for Incident Analysis**

Your current analyst level is **L1**, but this incident question 
requires **L2** access.

**Action Required:**
- Contact your SOC manager or team lead
- Request escalation to **L2** analyst level
- Once approved, you'll be able to access this analysis
```

## Notes

- Non-incident questions use original tier detection
- Works with all existing incident data structures
- Can be easily extended with new keyword patterns
- No database changes required
- Compatible with existing FastAPI middleware

---

**Status:** ✅ Ready for production  
**Test Coverage:** All scenarios validated  
**Documentation:** L1_INCIDENT_QUERY_GUIDE.md  
**Example Script:** incident_query_example.py

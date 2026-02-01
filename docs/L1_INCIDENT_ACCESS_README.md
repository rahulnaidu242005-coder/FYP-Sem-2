# L1 Incident Query Access Control - Complete Setup & Usage

## Overview

**Problem Solved:**
- ❌ **Before:** L1 users couldn't ask ANY incident questions (blocked from all incident analysis)
- ✅ **After:** L1 users CAN ask L1-level incident questions while being escalated from L2/L3

**Key Improvement:**
L1 analysts can now get immediate, actionable insights about incidents ("What does this mean?" / "Should I escalate?") while maintaining security through proper escalation for deeper analysis.

---

## Quick Start (5 Minutes)

### 1. Verify Files Are Updated
```bash
# Check main.py has new functions
grep -n "is_incident_question\|detect_incident_question_level" main.py

# Check server.py has updated ChatQuery
grep -n "incident: Optional" UI2/server.py
```

### 2. Test Locally
```bash
# Test the functions directly
python incident_query_example.py

# Expected: All 8 scenarios should work
```

### 3. Test via API
```bash
# Start server (if not already running)
python UI2/server.py

# In another terminal, run API tests
python test_api_incident_queries.py

# Expected: All 8 API tests should pass
```

---

## Implementation Details

### What Was Changed

#### **File 1: main.py**
Added 2 new functions and modified 1 function:

```python
# NEW: Detect if question is about incidents
def is_incident_question(question: str) -> bool

# NEW: Determine tier (L1/L2/L3) for incident questions
def detect_incident_question_level(question: str) -> str

# MODIFIED: Now accepts optional incident_data parameter
def get_chatbot_response(
    question: str, 
    user_level: str = None, 
    incident_data: Union[Dict[str, Any], str] = None
) -> str
```

#### **File 2: UI2/server.py**
Modified API model and endpoint:

```python
# MODIFIED: ChatQuery now accepts optional incident field
class ChatQuery(BaseModel):
    question: str
    level: str = "L1"
    incident: Optional[Dict[str, Any]] = None

# MODIFIED: /api/chat endpoint passes incident data
@app.post("/api/chat")
async def chat(query: ChatQuery):
    response = get_chatbot_response(
        query.question,
        query.level,
        incident_data=query.incident  # NEW: Pass incident
    )
```

### How It Works

**Tier Detection for Incidents:**
- L1: "what do", "what does", "meaning", "escalate", "should i", "priority"
- L2: "investigate", "evidence", "check logs", "artifacts", "telemetry"
- L3: "threat hunt", "hunting strategy", "root cause", "detection strategy"

**Access Logic:**
```
If incident question:
    If user_level >= required_tier:
        Return incident analysis
    Else:
        Return escalation message
Else:
    Use regular question logic (existing behavior)
```

---

## Testing

### 1. Direct Python Testing
```python
from main import get_chatbot_response

incident = {"id": "INC-126", "title": "Alert", "priority": "HIGH"}

# Test 1: L1 asking L1 (should work)
r1 = get_chatbot_response(
    "What does this incident mean?",
    user_level="L1",
    incident_data=incident
)
assert "Authorization Required" not in r1  # ✅ Pass

# Test 2: L1 asking L2 (should be escalated)
r2 = get_chatbot_response(
    "How do I investigate this?",
    user_level="L1",
    incident_data=incident
)
assert "Authorization Required" in r2  # ✅ Pass
```

### 2. Example Script
```bash
python incident_query_example.py

# Shows all 8 scenarios with expected outcomes
```

### 3. API Testing
```bash
# Start server
python UI2/server.py

# Run comprehensive API tests
python test_api_incident_queries.py
```

### 4. Manual API Testing
```bash
# L1 user, L1 incident question (should work)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What does this incident mean?",
    "level": "L1",
    "incident": {"id": "INC-126", "title": "Alert"}
  }'

# Should return 689+ char analysis response

# L1 user, L2 incident question (should escalate)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do I investigate this?",
    "level": "L1",
    "incident": {"id": "INC-126", "title": "Alert"}
  }'

# Should return "Authorization Required..." message
```

---

## Usage Examples

### Python API
```python
from main import get_chatbot_response

# Prepare incident data
incident = {
    "id": "INC-126",
    "title": "Suspicious PowerShell Activity",
    "priority": "HIGH",
    "riskScore": 8.7,
    "categories": ["Malware", "Persistence"]
}

# Example 1: L1 user asking L1 incident question
response = get_chatbot_response(
    question="What do these incidents mean? Should I escalate them?",
    user_level="L1",
    incident_data=incident
)
print(response)
# Output: [L1 incident analysis, ~700 chars]

# Example 2: L1 user asking L2 incident question  
response = get_chatbot_response(
    question="How would I investigate this incident?",
    user_level="L1",
    incident_data=incident
)
print(response)
# Output: "Authorization Required for Incident Analysis..."
```

### REST API
```javascript
// Frontend example: Send incident query
const response = await fetch('/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    question: "What do these incidents mean?",
    level: "L1",
    incident: {
      id: "INC-126",
      title: "Suspicious PowerShell Activity",
      priority: "HIGH"
    }
  })
});

const data = await response.json();
console.log(data.response);  // L1 analysis or escalation message
```

---

## Response Examples

### Success Response (L1 asking L1)
```
**What This Incident Means:**
- Suspicious PowerShell activity detected on endpoint
- Typically associated with malware execution or post-compromise activity
- High risk indicator that requires attention

**Your Action:**
1. Check if the user (CORP\jsmith) initiated this activity
2. If no legitimate reason for PowerShell execution, escalate immediately
3. Isolate the endpoint (DESKTOP-ABC123) if suspicious

**When to Escalate:**
- Escalate to L2 if: User denies activity OR suspicious command detected
- Contact: SOC Lead/Manager
- Priority: HIGH (high risk score: 8.7)
```

### Escalation Response (L1 asking L2)
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

## Customization

### Add Custom Keywords
Edit `main.py` lines 22-56:

```python
def detect_incident_question_level(question: str) -> str:
    question_lower = question.lower()
    
    # Add L3 keywords
    l3_incident_keywords = [
        "threat hunt", "how to hunt",  # existing
        "anomaly", "baseline",  # ADD NEW HERE
    ]
    
    # Add L2 keywords
    l2_incident_keywords = [
        "investigate", "evidence",  # existing
        "trace", "tracking",  # ADD NEW HERE
    ]
```

### Adjust Keyword Matching
Current implementation uses substring matching. To use exact word matching:

```python
# Current (substring)
return any(keyword in question_lower for keyword in keywords)

# Exact word matching (modify both functions)
import re
pattern = r'\b(' + '|'.join(keywords) + r')\b'
return bool(re.search(pattern, question_lower))
```

---

## Troubleshooting

### Issue: L1 user still can't query incidents
**Check:**
1. Is question detected as incident question?
   ```python
   from main import is_incident_question
   print(is_incident_question("Your question"))  # Should be True
   ```

2. Is tier correctly detected?
   ```python
   from main import detect_incident_question_level
   print(detect_incident_question_level("Your question"))  # Should be L1, L2, or L3
   ```

3. Is incident data being passed?
   ```python
   # Check incident_data is not None
   ```

### Issue: Wrong tier classification
**Solution:** Check keyword lists in `main.py` lines 22-56. Add/remove keywords as needed.

### Issue: API returning error
**Check:**
1. Server running: `curl http://localhost:8000/`
2. Incident data valid JSON: `json.loads(incident_str)`
3. Query format correct:
   ```json
   {
     "question": "string",
     "level": "L1" or "L2" or "L3",
     "incident": { "id": "string", ... }
   }
   ```

---

## Test Scenarios

### ✅ Expected to Work (L1 Allowed)
- "What do these incidents mean?"
- "Should I escalate this alert?"
- "What is the priority of this incident?"
- "What happened in this alert?"
- "Is this urgent?"

### ❌ Expected to Escalate (L1 Blocked)
- "How do I investigate this?"
- "What evidence should I look for?"
- "Show me threat hunting steps"
- "What's the root cause?"
- "How would you approach this?"

### ✅ L2 Allowed (Investigation Level)
- All L1 questions (they have higher access)
- "What logs should I check?"
- "Where are the artifacts?"
- "What telemetry should I collect?"

### ✅ L3 Allowed (Advanced Level)
- All L1 and L2 questions (they have higher access)
- "Show me threat hunting methodology"
- "What detection strategies apply?"
- "How would you engineer detection?"

---

## Documentation Files

| File | Purpose |
|------|---------|
| `L1_INCIDENT_QUERY_GUIDE.md` | Comprehensive implementation guide |
| `L1_INCIDENT_ACCESS_QUICK_CARD.md` | Quick reference for developers |
| `L1_INCIDENT_ACCESS_IMPLEMENTATION.md` | Technical implementation details |
| `incident_query_example.py` | Example script with all 8 scenarios |
| `test_api_incident_queries.py` | API integration test suite |

---

## Deployment Checklist

- ✅ `main.py` updated with 2 new functions
- ✅ `UI2/server.py` ChatQuery model updated
- ✅ `UI2/server.py` /api/chat endpoint updated
- ✅ All syntax errors checked (no errors found)
- ✅ Backward compatibility verified (no breaking changes)
- ✅ Tests created and passing
- ✅ Documentation complete

**Ready for Production:** YES ✅

---

## Performance Impact

- **Response Time:** No degradation (only adds keyword matching: O(n) where n=number of keywords)
- **Memory Usage:** Negligible (adds 2 small functions + static keyword lists)
- **Scalability:** No issues (stateless operation, no database queries)

---

## Support & Questions

**For Implementation Issues:**
1. Check `test_api_incident_queries.py` for working examples
2. Review keyword lists in `main.py` lines 22-56
3. See `L1_INCIDENT_QUERY_GUIDE.md` troubleshooting section

**For Feature Requests:**
- Add keywords to tier lists in `main.py`
- Modify tier detection logic in `detect_incident_question_level()`
- Update documentation to reflect changes

---

## Summary

| Aspect | Status |
|--------|--------|
| Implementation | ✅ Complete |
| Testing | ✅ All tests passing |
| Documentation | ✅ Comprehensive |
| Backward Compatibility | ✅ No breaking changes |
| API Ready | ✅ Ready to use |
| Production Ready | ✅ Deployment ready |

**Key Achievement:** L1 users can now ask L1-level incident questions while maintaining security through escalation for deeper analysis.


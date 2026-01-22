# 🔐 Privilege Escalation Testing Guide

## What Was Implemented

**Access Control System**: Users can only ask questions at or below their current analyst level. Attempting to ask higher-level questions triggers a privilege escalation message.

---

## 📊 Access Matrix

```
                L1 Questions    L2 Questions    L3 Questions
                
L1 Analyst      ✅ Answer       ❌ Escalate     ❌ Escalate
L2 Analyst      ✅ Answer       ✅ Answer       ❌ Escalate
L3 Analyst      ✅ Answer       ✅ Answer       ✅ Answer
```

---

## 🧪 Testing Scenarios

### Scenario 1: L1 User Asking L2 Question

**Setup**: Click L1 button
**Question**: "How do I investigate lateral movement?" (L2-level question)
**Result**: 
```
❌ BLOCKED

**Privilege Escalation Required**

Your current analyst level is **L1**, but this question requires **L2** access.

**What you're asking about**: This topic requires L2 analyst permissions to discuss.

**Action Required:**
- Contact your SOC manager or team lead
- Request escalation to **L2** analyst level
- Once approved, you'll be able to access this information

**Current Access:**
- Level L1: You can ask questions that match this level
- Level L2+: Restricted - requires escalation
```

---

### Scenario 2: L1 User Asking L1 Question

**Setup**: Click L1 button
**Question**: "What is phishing?" (L1-level question)
**Result**: 
```
✅ ALLOWED

[Normal L1 response about phishing]
```

---

### Scenario 3: L2 User Asking L2 Question

**Setup**: Click L2 button
**Question**: "What telemetry shows credential dumping?" (L2-level question)
**Result**: 
```
✅ ALLOWED

[L2 response with specific telemetry sources, event IDs, log fields]
```

---

### Scenario 4: L2 User Asking L3 Question

**Setup**: Click L2 button
**Question**: "How do I hunt for credential dumping?" (L3-level question)
**Result**: 
```
❌ BLOCKED

**Privilege Escalation Required**

Your current analyst level is **L2**, but this question requires **L3** access.

[Escalation message with action items]
```

---

### Scenario 5: L2 User Asking L1 Question

**Setup**: Click L2 button
**Question**: "What is malware?" (L1-level question)
**Result**: 
```
✅ ALLOWED

[L1 response - accessible to all levels]
```

---

### Scenario 6: L3 User Asking Any Question

**Setup**: Click L3 button
**Question**: Any question (L1, L2, or L3)
**Result**: 
```
✅ ALLOWED - ALWAYS

[Response at L3 depth]
```

---

## 🧬 Question Classification

The system auto-detects what level a question requires based on keywords:

### L1 Questions (Basic Info)
```
"What is phishing?"
"What is malware?"
"What is ransomware?"
"What is lateral movement?"
"What is credential dumping?"
"What should I do if I see a suspicious email?"
```

### L2 Questions (Investigation)
```
"How do I investigate phishing?"
"How do I detect lateral movement?"
"What telemetry shows credential dumping?"
"What artifacts indicate malware?"
"How do I pivot on this attack?"
"What event IDs should I look for?"
```

### L3 Questions (Advanced)
```
"How do I hunt for phishing?"
"What's the root cause of lateral movement?"
"How do I build detections for credential dumping?"
"What evasion techniques does this malware use?"
"How do I implement threat hunting?"
"What behavioral patterns indicate this attack?"
```

---

## ✅ Complete Test Checklist

### Test 1: L1 Access Control
- [ ] Set level to L1
- [ ] Ask L1 question (e.g., "What is phishing?") → Should get answer ✅
- [ ] Ask L2 question (e.g., "How to investigate?") → Should get escalation ❌
- [ ] Ask L3 question (e.g., "How to hunt?") → Should get escalation ❌

### Test 2: L2 Access Control
- [ ] Set level to L2
- [ ] Ask L1 question → Should get answer ✅
- [ ] Ask L2 question → Should get answer ✅
- [ ] Ask L3 question → Should get escalation ❌

### Test 3: L3 Access Control
- [ ] Set level to L3
- [ ] Ask L1 question → Should get answer ✅
- [ ] Ask L2 question → Should get answer ✅
- [ ] Ask L3 question → Should get answer ✅

### Test 4: Level Switching
- [ ] Start at L1, try L3 question → Blocked
- [ ] Switch to L3, ask same question → Allowed
- [ ] Switch back to L1 → Blocked again

### Test 5: Multiple Chats
- [ ] Chat 1 at L1
- [ ] Chat 2 at L2
- [ ] Chat 3 at L3
- [ ] Each should enforce its own level access

---

## 📋 Example Escalation Message

When a user lacks sufficient privilege:

```
**Privilege Escalation Required**

Your current analyst level is **L1**, but this question requires **L2** access.

**What you're asking about**: This topic requires L2 analyst permissions to discuss.

**Action Required:**
- Contact your SOC manager or team lead
- Request escalation to **L2** analyst level
- Once approved, you'll be able to access this information

**Current Access:**
- Level L1: You can ask questions that match this level
- Level L2+: Restricted - requires escalation
```

---

## 🎯 How It Works Behind the Scenes

```
1. User asks question at their current level
2. System detects REQUIRED level of question
3. Compare: user_level >= required_level?
   
   IF YES → Answer normally ✅
   IF NO → Show escalation message ❌
```

**Example**:
- User level: L1 (numeric: 1)
- Question requires: L2 (numeric: 2)
- 1 < 2 → BLOCKED, show escalation message

---

## 💡 Key Points

✅ **L1 analysts** can only access L1 content
✅ **L2 analysts** can access L1 and L2 content  
✅ **L3 analysts** can access everything (L1, L2, L3)
✅ **Escalation message** is clear and actionable
✅ **Auto-detection** uses same keyword matching as before
✅ **Per-chat levels** mean each chat enforces its own access

---

## 🔄 What Happens at Each Level

### At L1:
```
User Question
    ↓
Detect: Is this L1, L2, or L3?
    ↓
If L1 → Answer ✅
If L2 → Escalation ❌
If L3 → Escalation ❌
```

### At L2:
```
User Question
    ↓
Detect: Is this L1, L2, or L3?
    ↓
If L1 → Answer ✅
If L2 → Answer ✅
If L3 → Escalation ❌
```

### At L3:
```
User Question
    ↓
Detect: Is this L1, L2, or L3?
    ↓
If L1 → Answer ✅
If L2 → Answer ✅
If L3 → Answer ✅
```

---

## 🎓 Training Workflows

### Workflow 1: Progressive Access
```
1. New analyst starts at L1
2. Can ask basic questions
3. Tries L2 question → Gets escalation
4. Learns they need to request access
5. Gets approved, switches to L2
6. Now can ask investigation questions
7. Eventually escalates to L3 as expert
```

### Workflow 2: SOC Onboarding
```
1. Junior analyst joins → L1 only
2. Senior analyst joins → L2/L3 access
3. Each can only access their level
4. Escalation messages guide them
5. Clear security boundary
```

---

## 🚀 Ready to Test!

Try this simple test:

1. **Click L1 button**
2. **Ask**: "How do I hunt for phishing?" (L3 question)
3. **Expected**: Escalation message
4. **Click L3 button**
5. **Ask same question**
6. **Expected**: Full detailed L3 response

The difference is clear! 🎉

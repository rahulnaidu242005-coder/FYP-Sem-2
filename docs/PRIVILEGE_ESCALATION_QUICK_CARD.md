# 🔐 Privilege Escalation - Quick Reference Card

## The Rule

```
┌──────────────────────────────────────────────────────┐
│ Users can ONLY ask questions at or BELOW their level │
└──────────────────────────────────────────────────────┘

L1 can ask:   L1 questions only
L2 can ask:   L1 and L2 questions
L3 can ask:   L1, L2, and L3 questions (ALL)
```

---

## Access Matrix

```
                L1 Question         L2 Question         L3 Question
                                    
L1 Analyst      ✅ ALLOWED          ❌ BLOCKED          ❌ BLOCKED
L2 Analyst      ✅ ALLOWED          ✅ ALLOWED          ❌ BLOCKED
L3 Analyst      ✅ ALLOWED          ✅ ALLOWED          ✅ ALLOWED
```

---

## Question Type Examples

### 🟢 L1 Questions (Basic)
```
"What is phishing?"
"What is malware?"
"What is lateral movement?"
"Tell me about credential dumping"
"Explain ransomware"
```
**Who can ask**: L1, L2, L3 ✅
**Who gets blocked**: Nobody

---

### 🟡 L2 Questions (Investigation)
```
"How do I investigate phishing?"
"What telemetry shows lateral movement?"
"How do I detect malware?"
"What artifacts indicate credential dumping?"
"How do I pivot on this attack?"
```
**Who can ask**: L2, L3 ✅
**Who gets blocked**: L1 ❌

---

### 🔴 L3 Questions (Advanced)
```
"How do I hunt for phishing?"
"What's the root cause of lateral movement?"
"How do I build detections for malware?"
"What evasion techniques does this use?"
"How do I implement threat hunting?"
```
**Who can ask**: L3 ✅
**Who gets blocked**: L1, L2 ❌

---

## What Happens When Blocked

```
User at L1 asks: "How do I hunt for phishing?" (L3 question)
                    ↓
System says: ❌ BLOCKED
                    ↓
Shows: "Privilege Escalation Required"
                    ↓
Displays: "Your current level is L1, but this requires L3"
                    ↓
Tells them: "Contact your SOC manager for escalation"
```

---

## Real Examples

### Example 1: L1 Analyst, Basic Question
```
Input:  SET to L1
Input:  "What is phishing?"

Output: ✅ ALLOWED
Output: [L1 answer with basic explanation]
```

### Example 2: L1 Analyst, Investigation Question
```
Input:  SET to L1
Input:  "How do I investigate phishing?"

Output: ❌ BLOCKED
Output: "Privilege Escalation Required - your L1 level cannot ask L2 questions"
```

### Example 3: L2 Analyst, Both Basic AND Investigation
```
Input:  SET to L2
Input:  "What is phishing?"

Output: ✅ ALLOWED (L1 question, L2 can ask)
Output: [Answer]

---

Input:  "How do I investigate phishing?"

Output: ✅ ALLOWED (L2 question, L2 can ask)
Output: [Investigation details]
```

### Example 4: L3 Analyst, Everything
```
Input:  SET to L3
Input:  "What is phishing?" (L1)

Output: ✅ ALLOWED
Output: [Answer]

---

Input:  "How do I investigate?" (L2)

Output: ✅ ALLOWED
Output: [Answer]

---

Input:  "How do I hunt?" (L3)

Output: ✅ ALLOWED
Output: [Answer]
```

---

## Testing Checklist

```
☐ At L1:
  ☐ Ask "What is phishing?" → ✅ GET ANSWER
  ☐ Ask "How to investigate?" → ❌ GET BLOCKED

☐ At L2:
  ☐ Ask "What is phishing?" → ✅ GET ANSWER
  ☐ Ask "How to investigate?" → ✅ GET ANSWER
  ☐ Ask "How to hunt?" → ❌ GET BLOCKED

☐ At L3:
  ☐ Ask "What is phishing?" → ✅ GET ANSWER
  ☐ Ask "How to investigate?" → ✅ GET ANSWER
  ☐ Ask "How to hunt?" → ✅ GET ANSWER
```

---

## Escalation Message Template

When blocked:

```
**Privilege Escalation Required**

Your current analyst level is **L1**, 
but this question requires **L2** access.

**What you're asking about**: 
This topic requires L2 analyst permissions.

**Action Required:**
- Contact your SOC manager or team lead
- Request escalation to **L2** analyst level
- Once approved, you can access this

**Current Access:**
- Level L1: ✅ Allowed
- Level L2+: ❌ Restricted
```

---

## Numeric Comparison (Behind the Scenes)

```
L1 = 1
L2 = 2  
L3 = 3

When user asks question:
1. Detect required level (e.g., L2 = 2)
2. Check user level (e.g., L1 = 1)
3. Compare: 1 >= 2?
   NO → ❌ BLOCKED
   YES → ✅ ALLOWED
```

---

## Hierarchy

```
         ▲ Can ask
         │ everything
      L3 ┌─────────────────────────────┐
         │ ✅ L1, L2, L3 questions     │
      L2 ├─────────────────────────────┤
         │ ✅ L1, L2 questions         │
         │ ❌ L3 questions             │
      L1 ├─────────────────────────────┤
         │ ✅ L1 questions only        │
         │ ❌ L2, L3 questions         │
         └─────────────────────────────┘
         Can only ask
         basic questions ▼
```

---

## Key Points

✅ **Simpler than it sounds**: If your level >= question level, you can ask
✅ **L3 is superuser**: Can ask anything
✅ **Clear messages**: When blocked, users know why and what to do
✅ **Auto-detection**: No manual configuration needed
✅ **Per-chat**: Each chat has its own level enforcement

---

## Quick Decision Tree

```
                        ┌─ Your Level?
                        │
        ┌───────────────┼───────────────┐
        │               │               │
       L1              L2              L3
        │               │               │
        ▼               ▼               ▼
     Can ask:       Can ask:        Can ask:
     L1 only        L1 & L2         ALL (L1,L2,L3)
        │               │               │
        ├─ L1 Q ✅      ├─ L1 Q ✅     ├─ L1 Q ✅
        ├─ L2 Q ❌      ├─ L2 Q ✅     ├─ L2 Q ✅
        └─ L3 Q ❌      └─ L3 Q ❌     └─ L3 Q ✅
```

---

## Copy-Paste Test Questions

**L1 Question**:
```
"What is phishing?"
```

**L2 Question**:
```
"How do I investigate phishing?"
```

**L3 Question**:
```
"How do I hunt for phishing?"
```

→ Try at each level to see the escalation in action!

---

**That's it!** Simple, clear, and easy to understand. 🚀

# 📋 Privilege Escalation - Cheat Sheet

## TL;DR (Too Long; Didn't Read)

```
L1 can ask L1 questions
L2 can ask L1 and L2 questions  
L3 can ask ANYTHING

Try to ask above your level → Get blocked with helpful message
```

---

## Test Right Now

### Copy-Paste These

**At L1 - Should Work** ✅
```
What is phishing?
```

**At L1 - Should Block** ❌
```
How do I hunt for phishing?
```

**At L3 - Should Work** ✅
```
How do I hunt for phishing?
```

---

## What Gets Blocked

```
L1 asking L2 question      ❌ NO
L1 asking L3 question      ❌ NO
L2 asking L3 question      ❌ NO

L1 asking L1 question      ✅ YES
L2 asking L1 question      ✅ YES
L2 asking L2 question      ✅ YES
L3 asking anything         ✅ YES
```

---

## The Message

When blocked, users see:

```
**Privilege Escalation Required**

Your current level is L1, but this needs L2.

Contact your manager to request escalation.
```

---

## Visual

```
   Your Level    Question Level   Result
   ───────────────────────────────────────
   L1     >=     L1          ✅ OK
   L1     >=     L2          ❌ BLOCKED
   L1     >=     L3          ❌ BLOCKED
   L2     >=     L1          ✅ OK
   L2     >=     L2          ✅ OK
   L2     >=     L3          ❌ BLOCKED
   L3     >=     L1          ✅ OK
   L3     >=     L2          ✅ OK
   L3     >=     L3          ✅ OK
```

---

## Question Level = Keyword Detection

| Level | Keywords | Example |
|-------|----------|---------|
| L1 | What, define, explain | "What is phishing?" |
| L2 | How investigate, telemetry | "How to investigate?" |
| L3 | Hunt, root cause, evasion | "How to hunt?" |

---

## One Line Summary

**Users can only ask questions at or below their assigned level.**

---

## Numeric Logic

```
L1 = 1, L2 = 2, L3 = 3

If your_level >= question_level → ✅ Answer
If your_level < question_level  → ❌ Block
```

---

## That's It!

- Simple hierarchy
- Auto-detects question level  
- Blocks if under-privileged
- Shows helpful escalation message

🔐 Done!

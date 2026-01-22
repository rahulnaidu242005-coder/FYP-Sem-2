# 🎯 Level Switching - Visual Quick Start

## 🔘 The Buttons

```
┌─────────────────────────────┐
│ Analyst Level:              │
│  [L1]  [L2]  [L3]          │  ← Click any button to switch
│  ✓ (active = green glow)    │
└─────────────────────────────┘
```

## 📝 What Each Level Means

```
╔════════════════════════════════════════════════════════════╗
║ L1 - BASIC                                                 ║
║ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║ • Simple explanations (2-3 sentences max)                 ║
║ • Easy to understand                                       ║
║ • What to do next steps                                   ║
║ ✓ Good for: Ticket triage, first responders              ║
╚════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════╗
║ L2 - INVESTIGATION                                         ║
║ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║ • Specific artifacts and log sources                       ║
║ • Event IDs and field names                               ║
║ • Query examples                                           ║
║ ✓ Good for: SOC investigation, evidence collection       ║
╚════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════╗
║ L3 - ADVANCED                                              ║
║ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║ • Root cause analysis                                      ║
║ • Threat hunting strategies                                ║
║ • Detection engineering                                    ║
║ • MITRE ATT&CK mappings                                   ║
║ ✓ Good for: Threat hunting, security architecture        ║
╚════════════════════════════════════════════════════════════╝
```

## 🎮 3 Ways to Switch Levels

### Method 1: Click Button ⭐ FASTEST
```
Simply click any level button
L1 button → switch to basic
L2 button → switch to investigation  
L3 button → switch to advanced
```

### Method 2: Type Level
```
Type in chat input:
  L1 [Enter] → switches to L1
  L2 [Enter] → switches to L2
  L3 [Enter] → switches to L3
```

### Method 3: Say It
```
Type in chat input:
  switch to L1 [Enter]
  switch to L2 [Enter]
  switch to L3 [Enter]
  
(case doesn't matter - works with: L1, l1, SWITCH TO L1, etc.)
```

## 🔄 Example Usage

```
Step 1: Chat opens
        └─ L1 is active (default)

Step 2: You ask "What is phishing?"
        └─ Get basic, simple explanation

Step 3: You click the L2 button
        └─ Green light moves to L2
        └─ Blue notification appears

Step 4: You ask "How do I investigate phishing?"
        └─ Get specific artifacts, log sources, queries

Step 5: You click the L3 button
        └─ Green light moves to L3
        └─ Blue notification appears

Step 6: You ask "How do we hunt for this?"
        └─ Get threat hunting strategies, detection engineering
```

## 💚 How to Know Your Current Level

```
┌──────────────────────────┐
│ Analyst Level:           │
│ [L1] [L2] [L3 ✓ GLOW]   │  ← Green glowing button = current
└──────────────────────────┘

Also: Blue message in chat shows when you switched
"Analyst level switched to L2. Responses will now 
 reflect investigation details depth."
```

## 📊 Response Depth Example

**Same Question Asked at Different Levels:**

```
Q: "What is credential dumping?"

L1 Answer (BASIC):
  "It's when attackers steal user passwords. 
   If you see this, contact your manager immediately."

L2 Answer (INVESTIGATION):
  "Look in Windows Event IDs 4688 (Process Creation), 
   Sysmon Event 10 (ProcessAccess), or EDR telemetry.
   Check for lsass.exe, mimikatz, or similar tools.
   Pivot on source process name and source user."

L3 Answer (ADVANCED):
  "Use behavioral correlation: Process Tree Analysis 
   (lsass.exe access spike), Memory Pattern Detection 
   (SEC_IMAGE flag absent), Cross-telemetry (Process + 
   Registry + File + Network). Implement ML baseline 
   for legitimate LSA access patterns. Hunting strategy: 
   Correlate access spike with authentication events 
   in AD logs..."
```

## ✅ Quick Checklist

After level switch, you should see:

- [ ] Level button highlighted in green
- [ ] All other buttons appear normal (gray)
- [ ] Blue notification in chat (if switching)
- [ ] Next response is at new level's depth
- [ ] Level is saved if you switch chats

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Button not responding | Try refreshing the page |
| Level not changing | Click button again or type L1/L2/L3 |
| Wrong response depth | Check which button is green (that's current level) |
| Commands not working | Make sure you press Enter after typing L1/L2/L3 |

## 💡 Pro Tips

1. **Try all three levels** for the same question to see difference
2. **Start at L1** if new to Netty, progress to L2/L3
3. **Use L2 for investigation**, L3 for advanced analysis
4. **Switch levels mid-conversation** to explore different depths
5. **Each chat remembers its level** - set it once, stays set
6. **Open multiple chats** at different levels to compare

## 🎓 Common Workflows

```
TRIAGE WORKFLOW:
  Chat @ L1 → Get basic alert info
  Click L2 → Investigate deeper

TEAM HANDOFF:
  Junior @ L1 → Triage
  Senior @ L2 → Investigate  
  Hunter @ L3 → Hunt

LEARNING PATH:
  Start @ L1 → Understand basics
  Move to L2 → Learn investigation
  Advance to L3 → Advanced techniques
```

## 📱 Controls Location

```
┌─────────────────────────────────────┐
│           CHAT HISTORY              │
│                                     │
│  • Message 1 (bot)                 │
│  • Message 2 (user)                │
│  • Message 3 (bot)                 │
│                                     │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│ Analyst Level: [L1] [L2] [L3] ← HERE│  ← LEVEL BUTTONS
│ [Input box: "Ask a question..."] [➤]│  
└─────────────────────────────────────┘
```

## 🎯 Bottom Line

- **Click L1/L2/L3** to pick your level
- **Level changes how responses sound**
- **Each chat remembers** its own level
- **Level persists** even after refresh
- **You're in control** - switch anytime

---

**That's it!** You're ready to use the level-switching feature. 🚀

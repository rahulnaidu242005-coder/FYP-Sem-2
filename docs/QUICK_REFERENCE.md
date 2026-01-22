# Quick Reference: Level Switching in Netty

## 🎯 Quick Start

**New users**: Your chat starts at **L1** by default. Switch levels anytime!

## 🔘 Ways to Switch Levels

| Method | How To | Example |
|--------|--------|---------|
| **Click Button** | Click L1, L2, or L3 button above input | Click the green "L2" button |
| **Type Level** | Type the level name and press Enter | Type `L2` then press Enter |
| **Say It** | Use natural language command | Type `switch to L3` |

## 📊 Response Depths

### L1 - Analyst Beginner
- **Best for**: First-time responders, ticket triage
- **Get**: Simple explanations, basic steps, when to escalate
- **NOT getting**: Technical deep-dives, specific log fields

### L2 - Investigator
- **Best for**: SOC analysts investigating incidents
- **Get**: Specific artifacts, telemetry sources, query examples
- **NOT getting**: Threat hunting strategies, architectural changes

### L3 - Threat Hunter / Architect
- **Best for**: Advanced analysts, threat hunters, SecArch reviews
- **Get**: Root cause analysis, hunting strategies, detection engineering
- **Include**: MITRE mappings, evasion techniques, hardening ideas

## 💾 How It Works

✓ **Per-chat**: Each chat remembers its own level
✓ **Persistent**: Reload page → level is still there
✓ **Independent**: Other chats keep their own levels
✓ **Fresh start**: New chat always starts at L1

## 🔔 What to Look For

When you switch levels, you'll see a **blue notification message** confirming the change. This notification shows:
- The new level you switched to
- What kind of responses to expect

## 🎓 Example Workflows

### Triage Workflow
1. Start at **L1** (default)
2. Get basic info about suspicious file
3. Click **L2** button → Need to investigate
4. Ask follow-up questions for investigation details

### Incident Deep-Dive
1. Create new chat → Starts at **L1**
2. Get overview of attack
3. Switch to **L2** → Collect investigation data
4. Switch to **L3** → Threat hunt and hardening

### Escalation Scenario
1. Junior analyst at **L1** → Tickets assignment
2. Senior analyst reads transcripts
3. Switches to **L2** or **L3** → Adds investigation notes

## ❓ Frequently Used Commands

```
L1          → Switch to basic level
L2          → Switch to investigation level
L3          → Switch to advanced level
switch to L1 → Alternative syntax
Switch to L2 → Works too (case-insensitive)
SWITCH TO L3 → Also works!
```

## 🔍 Recognizing Your Current Level

- **Green button** = Your current level (glowing green)
- Other buttons = Not currently active
- **Blue notification** = Just switched levels

## 💡 Pro Tips

1. **Multi-chat comparison**: Open multiple chats at different levels to compare depth
2. **Knowledge progression**: Start at L1, move to L2, then L3 as you learn
3. **Team workflows**: L1 for initial analysis, L2 for investigation, L3 for hardening
4. **Searching**: Ctrl+F in chat to search for details in responses
5. **Share findings**: Copy formatted responses (bold/text preserved)

---

**Need help?** Type "help" or check the LEVEL_SWITCHING_GUIDE.md for detailed documentation.

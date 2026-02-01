#!/usr/bin/env python3
"""
Incident Query Example with Tier-Aware Access Control

This script demonstrates how L1 users can now ask L1-level incident questions
while being blocked from L2/L3 incident questions with escalation messages.

Usage:
    python incident_query_example.py
"""

import json
from main import get_chatbot_response

# Example incident data
sample_incident = {
    "id": "INC-126",
    "title": "Suspicious PowerShell Activity Detected",
    "description": "Unusual PowerShell invocation with encoded script execution",
    "status": "ACTIVE",
    "priority": "HIGH",
    "riskScore": 8.7,
    "source": "EDR/Endpoint Detection",
    "timestamp": "2024-01-15T14:32:00Z",
    "categories": ["Malware", "Persistence", "Command & Control"],
    "alertMeta": {
        "user": "CORP\\jsmith",
        "hostname": "DESKTOP-ABC123",
        "process": "powershell.exe",
        "command_line": "powershell.exe -NoP -W Hidden -EncodedCommand..."
    },
    "tactics": ["Execution", "Persistence"],
    "techniques": ["PowerShell", "Obfuscated Files or Information"],
    "source_ip": "192.168.1.100",
    "destination_ip": "10.0.0.50"
}

def print_section(title):
    """Print a formatted section title"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def test_query(question, user_level, incident):
    """Test a query and display results"""
    print(f"User Level: {user_level}")
    print(f"Question: {question}\n")
    
    response = get_chatbot_response(
        question=question,
        user_level=user_level,
        incident_data=incident
    )
    
    print(f"Response:\n{response}\n")
    print("-" * 70)

# ============================================================================
# DEMONSTRATION
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                 INCIDENT QUERY - TIER-AWARE ACCESS CONTROL                  ║
║                                                                              ║
║  This demonstrates L1 users can now:                                        ║
║  1. Ask L1-level incident questions (What, meaning, should I escalate)       ║
║  2. Get blocked from L2/L3 incident questions with escalation messages      ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

# SCENARIO 1: L1 USER ASKING L1 INCIDENT QUESTION (SUCCESS)
print_section("SCENARIO 1: L1 User Asking L1 Incident Question - ALLOWED")
print("Incident ID: INC-126")
print(f"Incident Title: {sample_incident['title']}\n")

test_query(
    question="What do these incidents mean? Should I escalate them?",
    user_level="L1",
    incident=sample_incident
)

# SCENARIO 2: L1 USER ASKING L1 QUESTION - ALLOWED
print_section("SCENARIO 2: L1 User Asking Another L1 Incident Question - ALLOWED")

test_query(
    question="What is the meaning of this alert and what should I do?",
    user_level="L1",
    incident=sample_incident
)

# SCENARIO 3: L1 USER ASKING L2 INCIDENT QUESTION (ESCALATION REQUIRED)
print_section("SCENARIO 3: L1 User Asking L2 Incident Question - ESCALATION REQUIRED")

test_query(
    question="How would I investigate this incident? What evidence should I look for?",
    user_level="L1",
    incident=sample_incident
)

# SCENARIO 4: L1 USER ASKING L3 INCIDENT QUESTION (ESCALATION REQUIRED)
print_section("SCENARIO 4: L1 User Asking L3 Incident Question - ESCALATION REQUIRED")

test_query(
    question="Show me a threat hunting strategy for this incident. How would you detect similar patterns?",
    user_level="L1",
    incident=sample_incident
)

# SCENARIO 5: L2 USER ASKING L2 INCIDENT QUESTION (SUCCESS)
print_section("SCENARIO 5: L2 User Asking L2 Incident Question - ALLOWED")

test_query(
    question="How do I investigate this incident and what artifacts should I collect?",
    user_level="L2",
    incident=sample_incident
)

# SCENARIO 6: L3 USER ASKING L3 INCIDENT QUESTION (SUCCESS)
print_section("SCENARIO 6: L3 User Asking L3 Incident Question - ALLOWED")

test_query(
    question="What threat hunting methodology should I use for this incident?",
    user_level="L3",
    incident=sample_incident
)

# SCENARIO 7: REGULAR QUESTION (NO INCIDENT) - L1
print_section("SCENARIO 7: Regular Question (No Incident) - L1 User")

test_query(
    question="What is MITRE ATT&CK?",
    user_level="L1",
    incident=None
)

# SCENARIO 8: REGULAR QUESTION (NO INCIDENT) - L1 ASKING L2 QUESTION
print_section("SCENARIO 8: Regular L2 Question - L1 User - ESCALATION REQUIRED")

test_query(
    question="How do I investigate credential dumping attacks?",
    user_level="L1",
    incident=None
)

print(f"\n{'='*70}")
print("  SUMMARY")
print(f"{'='*70}\n")

print("""
KEY TAKEAWAYS:

1. L1 Users CAN Query L1 Incident Questions:
   - "What do these incidents mean?"
   - "Should I escalate this incident?"
   - "What is the meaning of this alert?"
   - "What should I do with this incident?"

2. L1 Users CANNOT Query L2/L3 Incident Questions:
   - L2: "How do I investigate..." -> Escalation Required
   - L3: "Show me a threat hunting strategy..." -> Escalation Required

3. Escalation Messages Include:
   - Current analyst level
   - Required level for the question
   - Incident ID (if applicable)
   - Clear action items

4. Non-Incident Questions Still Work:
   - Regular L2 and L3 escalations still apply
   - No change to non-incident question flow

5. API Integration:
   - POST /api/chat endpoint now accepts optional 'incident' field
   - ChatQuery model updated to support: question, level, incident
   - Same tier-aware logic applies to REST API calls
""")

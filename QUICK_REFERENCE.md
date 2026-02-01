## Incident Analysis - Quick Reference Guide

### What Was Implemented

Your incident analysis system now supports three analysis tiers for security incidents:

### L1 - Basic Overview (Tier 1)
**For**: Frontline SOC analysts who need quick understanding
**Includes**:
- What happened (plain English)
- Risk classification
- Alert category
- Basic next steps
- Who to contact

**Example Output**: "This is a HIGH risk incident about data being exported to an unknown external IP. Contact your SOC lead."

### L2 - Technical Investigation (Tier 2)
**For**: Incident handlers and investigators
**Includes**:
- Incident metadata (IDs, timestamps, sources)
- Network indicators (IPs, ports)
- MITRE tactic/technique mapping
- Root cause hypotheses
- Specific validation steps:
  - Which logs to check
  - What to search for
  - How to correlate
- Evidence collection checklist

**Example Output**: "Check firewall logs for 192.168.70.79 -> 85.214.28.69. Verify authentication logs. Timeline all events from 2024-09-16T22:27:40Z..."

### L3 - Threat Hunting (Tier 3)
**For**: Senior analysts and threat hunters
**Includes**:
- Everything in L2, PLUS:
- 5-phase investigation methodology
- IP reputation/threat intel strategies
- User behavior analysis
- NetWitness query templates
- SIEM query examples
- 3 detailed threat hunting hypotheses
- Evasion and persistence hunting
- Forensic preservation steps
- Containment options
- Decision tree for escalation

**Example Output**: Comprehensive 15-30 section analysis with specific queries, pivots, and investigation hypotheses

---

## How to Use It

### Option 1: Direct Python Import
```python
from main import analyze_incident

incident = {
    "id": "INC-126",
    "title": "File Upload...",
    "priority": "High",
    "riskScore": 70,
    # ... other fields
}

# Get analysis
analysis_l1 = analyze_incident(incident, "L1")
analysis_l2 = analyze_incident(incident, "L2")
analysis_l3 = analyze_incident(incident, "L3")

print(analysis_l1)
```

### Option 2: FastAPI REST API
```bash
# Single incident analysis
curl -X POST http://localhost:8000/api/analyze-incident \
  -H "Content-Type: application/json" \
  -d '{
    "incident": {...},
    "level": "L2"
  }'

# Response
{
  "success": true,
  "incident_id": "INC-126",
  "tier": "L2",
  "analysis": "... analysis text ..."
}
```

### Option 3: Batch Analysis
```bash
curl -X POST http://localhost:8000/api/batch-analyze-incidents \
  -H "Content-Type: application/json" \
  -d '[
    {"incident": {...}, "level": "L1"},
    {"incident": {...}, "level": "L2"},
    {"incident": {...}, "level": "L3"}
  ]'
```

---

## Incident Data Format

Your incident JSON should include:

```json
{
  "id": "INC-126",
  "title": "File Upload from Critical Systems to Dynamic DNS",
  "priority": "High",
  "riskScore": 70,
  "status": "InProgress",
  "alertCount": 1,
  "assignee": "sam",
  "created": "2024-09-16T22:27:44.971Z",
  "firstAlertTime": "2024-09-16T22:27:40Z",
  "categories": [
    {"parent": "Malware", "name": "Export data"},
    {"parent": "Misuse", "name": "Data mishandling"}
  ],
  "alertMeta": {
    "SourceIp": ["192.168.70.79"],
    "DestinationIp": ["85.214.28.69"]
  },
  "ruleId": "650cdaff4121d46c953d4dcb",
  "eventCount": 1,
  "sources": ["Reporting Engine"],
  "tactics": ["TA0007"],
  "techniques": ["T1016"]
}
```

**Required fields**:
- `id` - Incident ID
- At least one of: `title`, `categories`, `alertMeta`

**Recommended fields**:
- `riskScore` - Numeric risk (0-100)
- `priority` - High/Medium/Low
- `categories` - Attack categories
- `alertMeta` - Network indicators
- `tactics` - MITRE tactics
- `techniques` - MITRE techniques

---

## Files Created

1. **incident_analyzer.py** - Main module (424 lines)
   - `IncidentAnalyzer` class
   - `_analyze_l1()`, `_analyze_l2()`, `_analyze_l3()` methods
   - Helper methods for IP classification, MITRE mapping, etc.

2. **incident_demo.py** - Demo/test script
   - Example incidents
   - Usage demonstrations
   - Output samples

3. **INCIDENT_ANALYSIS_SETUP.md** - Detailed setup guide

4. **QUICK_REFERENCE.md** - This file

## Files Modified

1. **main.py**
   - Added import: `from incident_analyzer import IncidentAnalyzer`
   - Added function: `analyze_incident(incident_data, analysis_level)`
   - Maintains all existing functionality

2. **UI2/server.py**
   - Added import: `from main import analyze_incident`
   - Added endpoint: `POST /api/analyze-incident`
   - Added endpoint: `POST /api/batch-analyze-incidents`
   - Maintains all existing functionality

---

## Response Examples

### L1 Response (732 chars)
```
**INCIDENT OVERVIEW - INC-126**

**What Happened:**
File Upload from Critical Systems to Dynamic DNS

**Key Information:**
- Priority: High
- Risk Level: 70/100 (High Risk)
- Status: InProgress
- Alert Count: 1
- Category: Export data, Data mishandling

**Why This Matters:**
This incident has been flagged by the detection system with a High priority. 
A risk score of 70 indicates this requires immediate attention.

**What You Should Do:**
1. Review the incident summary and assigned owner (sam)
2. Check if any immediate action is needed based on the status (InProgress)
3. If priority is High, escalate to your SOC lead if this is urgent

**Who to Contact:**
- Assigned Analyst: sam
- Need escalation? Contact your SOC Team Lead
```

### L2 Response (2000+ chars)
Includes incident metadata, network indicators, attack classification, root causes, validation steps, correlation queries, evidence checklist

### L3 Response (8000+ chars)
Comprehensive analysis with 5 investigation phases, threat hunting hypotheses, SIEM/NetWitness queries, pivot strategies, forensics, containment options

---

## Testing

Run the demo script:
```bash
cd "c:\RP Y3S2\C300_Project\FYP-Sem-2"
python incident_demo.py
```

Or use the provided test code with Python:
```python
from incident_analyzer import IncidentAnalyzer
analyzer = IncidentAnalyzer()
result = analyzer.analyze_incident({...}, "L1")
print(result)
```

---

## Supported MITRE Mappings

**Tactics**:
- TA0001 - Initial Access
- TA0002 - Execution
- TA0003 - Persistence
- TA0004 - Privilege Escalation
- TA0005 - Defense Evasion
- TA0006 - Credential Access
- TA0007 - Discovery
- TA0008 - Lateral Movement
- TA0009 - Collection
- TA0010 - Exfiltration
- TA0011 - Command and Control
- TA0013 - Impact

**Techniques** (sample):
- T1016 - System Network Configuration Discovery
- T1021 - Remote Services
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel
- T1020 - Automated Exfiltration
- T1048 - Exfiltration Over Alternative Protocol

---

## Key Features

✓ Three-tier analysis (L1/L2/L3)
✓ Automatic tier adjustment based on incident data
✓ MITRE ATT&CK mapping
✓ IP classification (Internal/External)
✓ Incident metadata parsing
✓ Validation step generation
✓ Threat hunting methodology
✓ Query template generation
✓ Batch processing support
✓ JSON serializable output
✓ Error handling with clear messages
✓ Stateless (no data storage)

---

## Next Steps

1. **Start the server**: `fastapi dev UI2/server.py`
2. **Send test incident**: POST to `/api/analyze-incident`
3. **Integration**: Use `analyze_incident()` function in your existing workflow
4. **Feedback**: Adjust MITRE mappings or analysis templates as needed

---

## Support

For questions or customizations:
- Check `incident_analyzer.py` for the core logic
- Modify MITRE mappings in `__init__` method
- Customize analysis templates in the `_analyze_*` methods
- Add new fields to analysis by editing the helper functions

"""
Incident Analysis Demo
Demonstrates how to use the incident analyzer with L1/L2/L3 tiers
"""

from main import analyze_incident
import json

# Example incidents from the user's data
incidents = [
    {
        "id": "INC-126",
        "title": "File Upload from Critical Systems to Dynamic DNS",
        "summary": "",
        "priority": "High",
        "riskScore": 70,
        "status": "InProgress",
        "alertCount": 1,
        "averageAlertRiskScore": 70,
        "sealed": True,
        "totalRemediationTaskCount": 0,
        "openRemediationTaskCount": 0,
        "created": "2024-09-16T22:27:44.971Z",
        "lastUpdated": "2024-09-16T22:29:05.859Z",
        "lastUpdatedBy": "admin",
        "assignee": "sam",
        "sources": ["Reporting Engine"],
        "ruleId": "650cdaff4121d46c953d4dcb",
        "firstAlertTime": "2024-09-16T22:27:40Z",
        "categories": [
            {"id": "59b2af0f9a32f06e1305302d", "parent": "Malware", "name": "Export data"},
            {"id": "59b2af0f9a32f06e1305303e", "parent": "Misuse", "name": "Data mishandling"}
        ],
        "journalEntries": None,
        "createdBy": "File Upload from Critical Systems to Dynamic DNS",
        "deletedAlertCount": 0,
        "eventCount": 1,
        "alertMeta": {"SourceIp": ["192.168.70.79"], "DestinationIp": ["85.214.28.69"]},
        "tactics": [],
        "techniques": []
    },
    {
        "id": "INC-125",
        "title": "Suspicious Configuration Activity for Detects Router Configuration Attempts",
        "summary": "",
        "priority": "Medium",
        "riskScore": 50,
        "status": "InProgress",
        "alertCount": 23,
        "averageAlertRiskScore": 50,
        "sealed": True,
        "totalRemediationTaskCount": 0,
        "openRemediationTaskCount": 0,
        "created": "2024-09-16T22:23:32.913Z",
        "lastUpdated": "2024-09-16T22:28:26.197Z",
        "lastUpdatedBy": "admin",
        "assignee": "sam",
        "sources": ["Event Stream Analysis"],
        "ruleId": "650cdaff4121d46c953d4dcd",
        "firstAlertTime": "2024-09-16T22:23:32.779Z",
        "categories": [
            {"id": "59b2af0f9a32f06e13053040", "parent": "Misuse", "name": "Net misuse"}
        ],
        "journalEntries": None,
        "createdBy": "Suspicious Configuration Activity",
        "deletedAlertCount": 0,
        "eventCount": 23,
        "alertMeta": {"SourceIp": [""], "DestinationIp": [""]},
        "tactics": ["TA0007"],
        "techniques": ["T1016"]
    },
    {
        "id": "INC-106",
        "title": "Outbound FTP by Admin User",
        "summary": None,
        "priority": "Medium",
        "riskScore": 30,
        "status": "Closed",
        "alertCount": 1,
        "averageAlertRiskScore": 30,
        "sealed": True,
        "totalRemediationTaskCount": 0,
        "openRemediationTaskCount": 0,
        "created": "2024-09-16T21:59:57.450Z",
        "lastUpdated": "2024-09-16T22:28:31.358Z",
        "lastUpdatedBy": "admin",
        "assignee": "sam",
        "sources": ["Event Stream Analysis"],
        "ruleId": "650cdaff4121d46c953d4dd5",
        "firstAlertTime": "2024-09-16T21:59:53.045Z",
        "categories": [],
        "journalEntries": None,
        "createdBy": "Outbound FTP by Admin User",
        "deletedAlertCount": 0,
        "eventCount": 1,
        "alertMeta": {"SourceIp": ["192.168.11.98"], "DestinationIp": ["86.57.246.177"]},
        "tactics": [],
        "techniques": []
    }
]

def demo_analysis():
    """Demonstrate incident analysis at different tiers"""
    
    print("=" * 80)
    print("INCIDENT ANALYSIS DEMO - L1/L2/L3 TIER EXAMPLES")
    print("=" * 80)
    
    for incident in incidents:
        incident_id = incident.get("id")
        title = incident.get("title")
        
        print(f"\n{'='*80}")
        print(f"INCIDENT: {incident_id} - {title}")
        print(f"{'='*80}")
        
        # Analyze at L1
        print("\n" + "▬" * 80)
        print("L1 ANALYSIS (Simple Overview)")
        print("▬" * 80)
        l1_analysis = analyze_incident(incident, "L1")
        print(l1_analysis)
        
        # Analyze at L2
        print("\n" + "▬" * 80)
        print("L2 ANALYSIS (Technical Investigation)")
        print("▬" * 80)
        l2_analysis = analyze_incident(incident, "L2")
        print(l2_analysis)
        
        # Analyze at L3
        print("\n" + "▬" * 80)
        print("L3 ANALYSIS (Advanced Threat Hunting)")
        print("▬" * 80)
        l3_analysis = analyze_incident(incident, "L3")
        print(l3_analysis)
        
        print("\n")

if __name__ == "__main__":
    demo_analysis()
    
    print("\n" + "=" * 80)
    print("USAGE VIA API:")
    print("=" * 80)
    print("""
POST /api/analyze-incident
Content-Type: application/json

{
    "incident": {
        "id": "INC-126",
        "title": "File Upload from Critical Systems to Dynamic DNS",
        ...
    },
    "level": "L1"
}

Response:
{
    "success": true,
    "incident_id": "INC-126",
    "tier": "L1",
    "analysis": "... analysis content ..."
}

Available levels: L1, L2, L3
""")

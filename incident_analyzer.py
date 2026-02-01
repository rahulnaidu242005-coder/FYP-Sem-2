"""
Incident Analyzer Module
Provides L1/L2/L3 tier-based incident analysis for security incidents
"""

from typing import Dict, Any, List, Optional
import json


class IncidentAnalyzer:
    """Analyzes security incidents at different analyst tiers"""
    
    def __init__(self):
        self.mitre_tactics_map = {
            "TA0001": "Initial Access",
            "TA0002": "Execution",
            "TA0003": "Persistence",
            "TA0004": "Privilege Escalation",
            "TA0005": "Defense Evasion",
            "TA0006": "Credential Access",
            "TA0007": "Discovery",
            "TA0008": "Lateral Movement",
            "TA0009": "Collection",
            "TA0010": "Exfiltration",
            "TA0011": "Command and Control",
            "TA0013": "Impact",
        }
        
        self.mitre_techniques_map = {
            "T1016": "System Network Configuration Discovery",
            "T1021": "Remote Services",
            "T1005": "Data from Local System",
            "T1041": "Exfiltration Over Command and Control Channel",
            "T1020": "Automated Exfiltration",
            "T1048": "Exfiltration Over Alternative Protocol",
        }
    
    def analyze_incident(self, incident: Dict[str, Any], tier: str = "L1") -> str:
        """
        Analyze an incident at the specified tier level.
        
        Args:
            incident: Incident data dictionary
            tier: Analysis tier (L1, L2, or L3)
            
        Returns:
            Analysis response string
        """
        tier_upper = tier.upper()
        if tier_upper == "L1":
            return self._analyze_l1(incident)
        elif tier_upper == "L2":
            return self._analyze_l2(incident)
        elif tier_upper == "L3":
            return self._analyze_l3(incident)
        else:
            return "Invalid tier. Please specify L1, L2, or L3."
    
    def _analyze_l1(self, incident: Dict[str, Any]) -> str:
        """
        L1 Analysis: Simple, high-level explanation.
        Focus: What happened, why it matters, and basic escalation.
        """
        incident_id = incident.get("id", "Unknown")
        title = incident.get("title", "Unknown Incident")
        priority = incident.get("priority", "Unknown")
        risk_score = incident.get("riskScore", 0)
        status = incident.get("status", "Unknown")
        assignee = incident.get("assignee", "Unassigned")
        alert_count = incident.get("alertCount", 0)
        categories = incident.get("categories", [])
        
        # Extract simple category descriptions
        category_desc = self._extract_simple_categories(categories)
        
        analysis = f"""**INCIDENT OVERVIEW - {incident_id}**

**What Happened:**
{title}

**Key Information:**
- Priority: {priority}
- Risk Level: {risk_score}/100 ({'High Risk' if risk_score >= 70 else 'Medium Risk' if risk_score >= 40 else 'Low Risk'})
- Status: {status}
- Alert Count: {alert_count}
- Category: {category_desc}

**Why This Matters:**
This incident has been flagged by the detection system with a {priority} priority. A risk score of {risk_score} indicates {'this requires immediate attention' if risk_score >= 70 else 'this needs investigation' if risk_score >= 40 else 'this should be reviewed'}.

**What You Should Do:**
1. Review the incident summary and assigned owner ({assignee})
2. Check if any immediate action is needed based on the status ({status})
3. If priority is {priority}, escalate to your SOC lead if this is urgent

**Who to Contact:**
- Assigned Analyst: {assignee}
- Need escalation? Contact your SOC Team Lead"""
        
        return analysis.strip()
    
    def _analyze_l2(self, incident: Dict[str, Any]) -> str:
        """
        L2 Analysis: Technical investigation and triage.
        Focus: Root causes, field analysis, validation steps.
        """
        incident_id = incident.get("id", "Unknown")
        title = incident.get("title", "Unknown Incident")
        priority = incident.get("priority", "Unknown")
        risk_score = incident.get("riskScore", 0)
        categories = incident.get("categories", [])
        tactics = incident.get("tactics", [])
        techniques = incident.get("techniques", [])
        alert_meta = incident.get("alertMeta", {})
        source_ips = alert_meta.get("SourceIp", [])
        dest_ips = alert_meta.get("DestinationIp", [])
        rule_id = incident.get("ruleId", "Unknown")
        created = incident.get("created", "Unknown")
        first_alert_time = incident.get("firstAlertTime", "Unknown")
        event_count = incident.get("eventCount", 0)
        sources = incident.get("sources", [])
        
        # Extract technical details
        category_info = self._extract_categories(categories)
        tactic_names = [self.mitre_tactics_map.get(t, t) for t in tactics] if tactics else []
        technique_names = [self.mitre_techniques_map.get(t, t) for t in techniques] if techniques else []
        
        analysis = f"""**TECHNICAL INCIDENT ANALYSIS - {incident_id}**

**Incident Metadata:**
- Title: {title}
- Incident ID: {incident_id}
- Rule ID: {rule_id}
- Priority: {priority} | Risk Score: {risk_score}/100
- First Alert: {first_alert_time}
- Total Events: {event_count}
- Detection Source: {', '.join(sources) if sources else 'N/A'}

**Network Indicators:**
- Source IP(s): {', '.join(source_ips) if source_ips else 'Not captured'}
- Destination IP(s): {', '.join(dest_ips) if dest_ips else 'Not captured'}

**Attack Classification:**
- Categories: {category_info if category_info else 'Unclassified'}
- MITRE Tactics: {', '.join(tactic_names) if tactic_names else 'Not mapped'}
- MITRE Techniques: {', '.join(technique_names) if technique_names else 'Not mapped'}

**Likely Root Causes:**
"""
        
        # Add root cause analysis based on categories and title
        if any('export' in cat.lower() or 'data' in cat.lower() for cat in category_info.lower().split(',')):
            analysis += "- Unauthorized data exfiltration or excessive data transfer detected\n"
        if any('misuse' in cat.lower() or 'mishandl' in cat.lower() for cat in category_info.lower().split(',')):
            analysis += "- Potential policy violation or improper data handling\n"
        if any('config' in title.lower() for _ in [title]):
            analysis += "- Unauthorized system or network configuration changes\n"
        if any('ftp' in title.lower() for _ in [title]):
            analysis += "- Use of legacy/unencrypted protocol for data transfer\n"
        if any('router' in title.lower() for _ in [title]):
            analysis += "- Attempts to modify network infrastructure settings\n"
        
        analysis += f"""

**Investigation Validation Steps:**

1. **Log Correlation:**
   - Search firewall/proxy logs for source IP: {source_ips[0] if source_ips else 'N/A'}
   - Check authentication logs (success/failed) from this source
   - Verify if source is internal (trusted network) or external

2. **Alert Verification:**
   - Review rule definition for {rule_id}
   - Check if this alert is a known false positive
   - Verify alert sensitivity settings are appropriate
   - Cross-reference with similar alerts in the last 24-48 hours

3. **Timeline Analysis:**
   - Map all {event_count} events chronologically from {first_alert_time}
   - Identify if events cluster or spread over time
   - Look for correlated alerts from other detection systems

4. **Basic Correlation:**
   - Search for other incidents from source IP: {source_ips[0] if source_ips else 'Unknown'}
   - Check asset/user history for previous suspicious activity
   - Review if destination IP has known reputation issues

**Evidence to Collect:**
- Full PCAP if available for the time window
- Endpoint logs (process execution, file transfers, connections)
- Authentication logs (source, destination, user, success/failure)
- Application logs if applicable

**Next Steps:**
- If confirmed malicious → Escalate to L3 threat hunting
- If unclear/suspicious → Gather more context and re-assess
- If false positive → Update rule and document finding"""
        
        return analysis.strip()
    
    def _analyze_l3(self, incident: Dict[str, Any]) -> str:
        """
        L3 Analysis: Senior analyst & threat hunter perspective.
        Focus: Detailed investigation, pivots, threat hunting, containment.
        """
        incident_id = incident.get("id", "Unknown")
        title = incident.get("title", "Unknown Incident")
        risk_score = incident.get("riskScore", 0)
        priority = incident.get("priority", "Unknown")
        alert_meta = incident.get("alertMeta", {})
        source_ips = alert_meta.get("SourceIp", [])
        dest_ips = alert_meta.get("DestinationIp", [])
        rule_id = incident.get("ruleId", "Unknown")
        first_alert_time = incident.get("firstAlertTime", "Unknown")
        event_count = incident.get("eventCount", 0)
        categories = incident.get("categories", [])
        tactics = incident.get("tactics", [])
        techniques = incident.get("techniques", [])
        assignee = incident.get("assignee", "Unassigned")
        
        category_info = self._extract_categories(categories)
        tactic_names = [self.mitre_tactics_map.get(t, t) for t in tactics] if tactics else []
        technique_names = [self.mitre_techniques_map.get(t, t) for t in techniques] if techniques else []
        
        src_ip = source_ips[0] if source_ips else "N/A"
        dst_ip = dest_ips[0] if dest_ips else "N/A"
        
        analysis = f"""**ADVANCED THREAT ANALYSIS & HUNTING BRIEF - {incident_id}**

**Executive Summary:**
Title: {title}
Risk Score: {risk_score}/100 | Priority: {priority} | Analyst: {assignee}
Detection Rule: {rule_id}
Event Count: {event_count} | First Alert: {first_alert_time}

---
**THREAT CLASSIFICATION & MITRE MAPPING:**

- Categories: {category_info if category_info else 'Unclassified'}
- MITRE Tactics: {', '.join(tactic_names) if tactic_names else 'Not mapped'}
- MITRE Techniques: {', '.join(technique_names) if technique_names else 'Not mapped'}

Attack Phase Assessment: {self._classify_attack_phase(categories, title)}

---
**PHASE 1: IMMEDIATE TRIAGE & VALIDATION**

1.1 Rule Assessment:
   - Retrieve and review rule {rule_id} logic and recent modifications
   - Analyze false positive rate for this rule over past 30 days
   - Compare current alert spike against historical baseline
   - Verify rule parameters match intended detection scope

1.2 Alert Artifact Verification:
   - Validate each of the {event_count} events for accuracy
   - Cross-check alert timestamps with system time synchronization
   - Identify any alert aggregation, deduplication, or filtering issues
   - Search for related alerts that may have been suppressed

1.3 Network Indicator Analysis:
   - Source IP: {src_ip} ({self._classify_ip_type(src_ip)})
   - Destination IP: {dst_ip} ({self._classify_ip_type(dst_ip)})
   - Determine if this communication pattern matches baseline

---
**PHASE 2: ADVANCED PIVOTING & CORRELATION**

2.1 Source IP Investigation ({src_ip}):
   
   Historical Context:
   - Query all incidents involving {src_ip} over past 90 days
   - Identify asset owner and last logged-in users
   - Check reputation across threat intelligence feeds
   - Verify geographic origin and ISP characteristics
   
   NetWitness Query Examples:
   ```
   query=ip.src="{src_ip}" | hosts, service, risk
   query=ip.src="{src_ip}" | flow_start_time, data_type, volume
   ```
   
   SIEM Query Examples:
   ```
   index=* source_ip={src_ip} earliest=-90d | stats count by user, dest_ip
   index=network src_ip={src_ip} | where action!=allowed
   ```

2.2 Destination IP Investigation ({dst_ip}):
   
   Threat Intelligence:
   - Check if {dst_ip} is known malicious (VirusTotal, AlienVault OTX, abuse.ch)
   - Identify hosting profile (datacenter, residential, shared hosting)
   - Determine FQDN(s) and domain resolution history
   - Check for DGA (Domain Generation Algorithm) indicators
   
   NetWitness Queries:
   ```
   query=ip.dst="{dst_ip}" | risk, hostname, event_count, service
   query=ip.dst="{dst_ip}" | session_type, host, service, data_type
   ```
   
   SIEM Queries:
   ```
   index=* dest_ip={dst_ip} | stats count by src_ip, user, protocol
   index=dns dest_ip={dst_ip} | stats values(query) as domain_names
   ```

2.3 User & Entity Behavioral Analytics:
   - Identify users/systems associated with source IP
   - Compare current behavior against 30-day baseline
   - Check for privilege escalation or unusual access patterns
   - Review failed logon attempts and MFA anomalies
   - Identify any account compromises or unusual service account activity

2.4 Timeline Reconstruction:
   - Build complete event timeline from {first_alert_time} onwards
   - Map precursor events (reconnaissance, scanning, probing)
   - Identify lateral movement patterns
   - Locate data exfiltration windows (if applicable)
   - Mark post-exploitation activity

---
**PHASE 3: THREAT HUNTING HYPOTHESES & PIVOTS**

3.1 Hypothesis 1: Insider Threat / Account Compromise
   
   Evidence Support:
   - Is {src_ip} an internal network address?
   - Categories indicate data export/mishandling?
   
   Investigation Actions:
   - Pull account logon history for assets on {src_ip}
   - Check for recent password changes or credential resets
   - Review API tokens and privileged access changes
   - Search for unusual outbound connections from user's other devices
   - Check for VPN/proxy usage anomalies
   
   Containment Options:
   - Force password reset and MFA challenge
   - Revoke active sessions and tokens
   - Isolate asset from network if confirmed malicious
   - Block suspicious destinations at firewall

3.2 Hypothesis 2: External C2 / Malware Communication
   
   Evidence Support:
   - Is {dst_ip} an external/untrusted address?
   - Any malware/exfiltration categories present?
   
   Investigation Actions:
   - Analyze PCAP for protocol anomalies and suspicious patterns
   - Check DNS resolution history to {dst_ip}
   - Extract and analyze any SSL/TLS certificates
   - Search for similar communication patterns (port, timing, protocol, volume)
   - Hunt for parent process spawning network connections
   
   Containment Options:
   - Block {dst_ip} at firewall/proxy immediately
   - Inspect endpoint for malware/implants
   - Isolate infected system from network
   - Conduct full forensic acquisition

3.3 Hypothesis 3: Data Exfiltration Activity
   
   Evidence Support:
   - Categories include 'Export data' or 'Data mishandling'?
   - High volume transfer detected?
   
   Investigation Actions:
   - Identify data touched and volume transferred
   - Check if encryption was bypassed
   - Search for file copy/transfer processes
   - Review data classification of affected files
   - Check backup integrity for affected data
   
   Containment Options:
   - Implement DLP policy to block further exfiltration
   - Review data access controls
   - Restore affected data from clean backups
   - Notify data owners and compliance team

---
**PHASE 4: DETECTION EVASION & PERSISTENCE**

4.1 Evasion Techniques:
   - Check for encrypted tunnels (SSH, VPN, proxies, Tor)
   - Identify low-and-slow transfers designed to evade volume detection
   - Search for user-agent spoofing or protocol obfuscation
   - Detect timestamp manipulation or log clearing attempts

4.2 Persistence Mechanisms:
   - Endpoint: Scheduled tasks, cron jobs, startup folders, registry run keys
   - Active Directory: Group Policy modifications, domain trusts
   - Network: Backdoor ports, shadow accounts, service modifications
   - Cloud: API credentials, access tokens, service principals

4.3 Lateral Movement Indicators:
   - Pass-the-hash / Pass-the-ticket artifacts
   - Service account abuse
   - Share enumeration and network mapping commands
   - DCSync-like replication activity

---
**PHASE 5: FORENSICS & CONTAINMENT ACTIONS**

5.1 Immediate Containment (if malicious confirmed):
   - Network: Null-route or firewall-block {dst_ip}
   - Endpoint: Isolate compromised asset immediately
   - Account: Revoke all sessions, reset credentials, force re-authentication
   - Data: Identify and protect affected data

5.2 Forensic Preservation:
   - Acquire full memory dump (WinPmem for Windows)
   - Export Security/System/Application event logs
   - Capture PCAP for affected timeframe
   - Hash and preserve executables and suspicious files
   - Export registry (SYSTEM, SAM, SECURITY hives)

5.3 Threat Intelligence:
   - Report {dst_ip} to threat intel team
   - Update detection rule if false positive confirmed
   - Document MITRE mapping for future correlation
   - Share findings with incident response team

---
**RECOMMENDED NETWITNESS/SIEM QUERIES FOR IMMEDIATE EXECUTION:**

```
1. User Behavior Baseline:
   NetWitness: query=ip.src="{src_ip}" | user, service, data_type, volume | sort by volume desc
   
2. Protocol/Port Anomalies:
   NetWitness: query=ip.dst="{dst_ip}" | service, port | where service='unknown'
   
3. File Transfer Detection:
   SIEM: (action=transfer OR command IN (ftp, sftp, scp)) src_ip={src_ip}
   
4. Lateral Movement Pivots:
   SIEM: src_ip=10.0.0.0/8 dest_ip=10.0.0.0/8 | search NOT service IN (kerberos, ldap, smtp)
   
5. Registry/Process Persistence:
   SIEM: process IN (schtasks, reg.exe, wmic) host={self._get_hostname_from_ip(src_ip)}
   
6. Data Access Patterns:
   SIEM: event_type=file_access src_ip={src_ip} | stats count by file_path, user
```

---
**ESCALATION & DECISION TREE:**

- **If Confirmed Malicious (high confidence):**
  → Immediately activate IR playbook
  → Notify CISO/Security leadership
  → Prepare stakeholder communications
  → Begin evidence preservation for legal/post-mortem

- **If Suspicious (medium confidence):**
  → Increase monitoring/alerting for related indicators
  → Schedule follow-up hunt in 48-72 hours
  → Request additional telemetry from endpoint tools
  → Loop back to Phase 2 with new data

- **If Likely False Positive (low confidence):**
  → Tune detection rule to reduce noise
  → Document root cause (benign process, whitelisted activity, etc.)
  → Notify detection engineering team
  → Close incident with detailed justification"""

        return analysis.strip()
    
    def _extract_categories(self, categories: List[Dict]) -> str:
        """Extract category information from incident data"""
        if not categories:
            return "Unclassified"
        
        category_names = []
        for cat in categories:
            parent = cat.get("parent", "")
            name = cat.get("name", "")
            if parent and name:
                category_names.append(f"{parent}/{name}")
            elif name:
                category_names.append(name)
        
        return ", ".join(category_names) if category_names else "Unclassified"
    
    def _extract_simple_categories(self, categories: List[Dict]) -> str:
        """Extract simple category names for L1 analysis"""
        if not categories:
            return "Unknown"
        
        names = [cat.get("name", "") for cat in categories]
        return ", ".join(filter(None, names)) if names else "Unknown"
    
    def _classify_attack_phase(self, categories: List[Dict], title: str) -> str:
        """Classify the attack phase based on categories"""
        category_str = self._extract_categories(categories).lower()
        title_lower = title.lower()
        
        if "export" in category_str or "exfiltration" in category_str or "upload" in title_lower:
            return "**Exfiltration/Data Theft Phase** - Data is being moved out of the organization"
        elif "config" in category_str or "discovery" in category_str or "router" in title_lower:
            return "**Reconnaissance/Discovery Phase** - Attacker scanning/probing network"
        elif "lateral" in category_str or "movement" in category_str:
            return "**Lateral Movement Phase** - Attacker moving through network"
        else:
            return "**Post-Compromise Activity** - Potential active compromise in progress"
    
    def _classify_ip_type(self, ip: str) -> str:
        """Classify IP as internal or external"""
        if not ip or ip == "":
            return "N/A"
        
        try:
            octets = ip.split(".")
            if len(octets) != 4:
                return "Invalid"
            
            first_octet = int(octets[0])
            second_octet = int(octets[1])
            
            # Check for private IP ranges
            if first_octet == 10:
                return "Internal (10.0.0.0/8)"
            elif first_octet == 172 and 16 <= second_octet <= 31:
                return "Internal (172.16.0.0/12)"
            elif first_octet == 192 and second_octet == 168:
                return "Internal (192.168.0.0/16)"
            elif first_octet == 127:
                return "Loopback"
            else:
                return "External/Public"
        except:
            return "Invalid"
    
    def _get_hostname_from_ip(self, ip: str) -> str:
        """Generate placeholder hostname from IP"""
        return f"host_{ip.replace('.', '_')}" if ip and ip != "N/A" else "unknown_host"

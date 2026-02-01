#!/usr/bin/env python3
"""
API Integration Test - Verify /api/chat endpoint with incident data

This script tests the FastAPI endpoint to ensure incident queries work correctly.
Run this after starting the FastAPI server: python UI2/server.py
"""

import json
import requests
import time

# Server URL
BASE_URL = "http://localhost:8000"

# Test incident data
test_incident = {
    "id": "INC-126",
    "title": "Suspicious PowerShell Activity Detected",
    "status": "ACTIVE",
    "priority": "HIGH",
    "riskScore": 8.7,
    "source": "EDR/Endpoint Detection",
    "categories": ["Malware", "Persistence"],
    "alertMeta": {
        "user": "CORP\\jsmith",
        "hostname": "DESKTOP-ABC123",
        "process": "powershell.exe"
    }
}

def print_test_header(test_num, title):
    """Print test header"""
    print(f"\n{'='*70}")
    print(f"TEST {test_num}: {title}")
    print(f"{'='*70}\n")

def test_api_endpoint(test_num, title, question, level, incident=None, expect_escalation=False):
    """Test API endpoint"""
    print_test_header(test_num, title)
    
    # Prepare request
    payload = {
        "question": question,
        "level": level
    }
    if incident:
        payload["incident"] = incident
    
    print(f"Request:")
    print(f"  User Level: {level}")
    print(f"  Question: {question}")
    print(f"  Incident Data: {'Yes' if incident else 'No'}\n")
    
    try:
        # Send request
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload,
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("success"):
                response_text = data.get("response", "")
                response_length = len(response_text)
                is_escalation = "Authorization Required" in response_text or "Privilege" in response_text
                
                print(f"Success: {data['success']}")
                print(f"Response Length: {response_length} chars")
                print(f"Is Escalation Message: {is_escalation}")
                
                # Check if result matches expectation
                if expect_escalation and is_escalation:
                    print(f"\n✅ PASSED - Correctly escalated")
                    return True
                elif not expect_escalation and not is_escalation:
                    print(f"\n✅ PASSED - Analysis provided")
                    return True
                else:
                    print(f"\n❌ FAILED - Unexpected result")
                    return False
            else:
                print(f"Success: {data['success']}")
                print(f"Error: {data.get('error', 'Unknown error')}")
                print(f"\n❌ FAILED - Request failed")
                return False
        else:
            print(f"Error: {response.text}")
            print(f"\n❌ FAILED - HTTP error")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server")
        print(f"   Make sure FastAPI is running: python UI2/server.py")
        return None
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║            API INTEGRATION TEST - L1 INCIDENT ACCESS CONTROL                 ║
║                                                                              ║
║  This tests the /api/chat endpoint with incident data to verify:            ║
║  1. L1 users can query L1 incident questions                                ║
║  2. L1 users are escalated from L2/L3 incident questions                     ║
║  3. L2/L3 users can access their authorized tiers                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check if server is running
    print("Checking server connection...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print("✅ Server is running\n")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        print("Please start the FastAPI server first:")
        print("  python UI2/server.py")
        return False
    
    results = []
    
    # Test 1: L1 user asking L1 incident question (should succeed)
    results.append(test_api_endpoint(
        1,
        "L1 User - L1 Incident Question (ALLOWED)",
        question="What do these incidents mean? Should I escalate them?",
        level="L1",
        incident=test_incident,
        expect_escalation=False
    ))
    
    # Test 2: L1 user asking L1 incident question variant
    results.append(test_api_endpoint(
        2,
        "L1 User - L1 Incident Question Variant (ALLOWED)",
        question="What is the meaning of this alert?",
        level="L1",
        incident=test_incident,
        expect_escalation=False
    ))
    
    # Test 3: L1 user asking L2 incident question (should escalate)
    results.append(test_api_endpoint(
        3,
        "L1 User - L2 Incident Question (ESCALATION REQUIRED)",
        question="How would I investigate this incident? What evidence should I look for?",
        level="L1",
        incident=test_incident,
        expect_escalation=True
    ))
    
    # Test 4: L1 user asking L3 incident question (should escalate)
    results.append(test_api_endpoint(
        4,
        "L1 User - L3 Incident Question (ESCALATION REQUIRED)",
        question="Show me a threat hunting strategy for this incident",
        level="L1",
        incident=test_incident,
        expect_escalation=True
    ))
    
    # Test 5: L2 user asking L2 incident question (should succeed)
    results.append(test_api_endpoint(
        5,
        "L2 User - L2 Incident Question (ALLOWED)",
        question="How do I investigate this incident and what artifacts should I collect?",
        level="L2",
        incident=test_incident,
        expect_escalation=False
    ))
    
    # Test 6: L3 user asking L3 incident question (should succeed)
    results.append(test_api_endpoint(
        6,
        "L3 User - L3 Incident Question (ALLOWED)",
        question="What threat hunting methodology would you recommend?",
        level="L3",
        incident=test_incident,
        expect_escalation=False
    ))
    
    # Test 7: Regular question (no incident) - L1
    results.append(test_api_endpoint(
        7,
        "L1 User - Regular Question (NO INCIDENT DATA)",
        question="What is MITRE ATT&CK?",
        level="L1",
        incident=None,
        expect_escalation=False
    ))
    
    # Test 8: Regular L2 question - L1 user (should escalate)
    results.append(test_api_endpoint(
        8,
        "L1 User - L2 Regular Question (ESCALATION REQUIRED)",
        question="How do I investigate credential dumping?",
        level="L1",
        incident=None,
        expect_escalation=True
    ))
    
    # Print summary
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print(f"{'='*70}\n")
    
    passed = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is False)
    errors = sum(1 for r in results if r is None)
    
    print(f"Passed: {passed}/8")
    print(f"Failed: {failed}/8")
    print(f"Errors: {errors}/8")
    
    if passed == 8:
        print("\n✅ ALL TESTS PASSED - L1 Incident Access Control is working!")
        return True
    else:
        print("\n❌ SOME TESTS FAILED - Check implementation")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

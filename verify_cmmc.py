#!/usr/bin/env python3
"""
CMMC Level 2 Verification Script
Verifies that we have all 110 controls and 320 assessment objectives
"""

import requests
import json

def verify_cmmc_controls():
    """Verify CMMC Level 2 controls and objectives count"""
    
    # Expected counts for CMMC Level 2
    EXPECTED_CONTROLS = 110
    EXPECTED_OBJECTIVES = 320
    
    # Expected controls per domain based on CMMC 2.0
    EXPECTED_DOMAIN_COUNTS = {
        'AC': 22,  # Access Control
        'AT': 4,   # Awareness and Training  
        'AU': 12,  # Audit and Accountability
        'CA': 9,   # Assessment, Authorization, and Monitoring
        'CM': 12,  # Configuration Management
        'CP': 3,   # Contingency Planning
        'IA': 12,  # Identification and Authentication
        'IR': 6,   # Incident Response
        'MA': 6,   # Maintenance
        'MP': 8,   # Media Protection
        'PE': 6,   # Physical Protection
        'PS': 2,   # Personnel Security
        'RA': 3,   # Risk Assessment
        'SA': 4,   # System and Services Acquisition
        'SC': 23,  # System and Communications Protection
        'SI': 7    # System and Information Integrity
    }
    
    try:
        # Fetch controls from the application
        response = requests.get('http://localhost:8080/api/controls')
        if response.status_code != 200:
            print(f"❌ Failed to fetch controls: HTTP {response.status_code}")
            return False
            
        controls = response.json()
        
        # Count controls and objectives
        total_controls = len(controls)
        total_objectives = sum(len(control.get('objectives', [])) for control in controls)
        
        print("=== CMMC Level 2 Verification Report ===")
        print(f"📊 Total Controls: {total_controls}/{EXPECTED_CONTROLS}")
        print(f"📋 Total Objectives: {total_objectives}/{EXPECTED_OBJECTIVES}")
        print()
        
        # Count by domain
        domain_counts = {}
        domain_objectives = {}
        
        for control in controls:
            domain = control.get('domain', 'Unknown')
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
            domain_objectives[domain] = domain_objectives.get(domain, 0) + len(control.get('objectives', []))
        
        print("=== Controls by Domain ===")
        missing_controls = 0
        missing_objectives = 0
        
        for domain, expected_count in EXPECTED_DOMAIN_COUNTS.items():
            actual_count = domain_counts.get(domain, 0)
            objectives_count = domain_objectives.get(domain, 0)
            status = "✅" if actual_count >= expected_count else "❌"
            
            print(f"{status} {domain}: {actual_count}/{expected_count} controls, {objectives_count} objectives")
            
            if actual_count < expected_count:
                missing_controls += (expected_count - actual_count)
        
        print()
        print("=== Summary ===")
        
        if total_controls >= EXPECTED_CONTROLS:
            print("✅ All 110 controls are present")
        else:
            print(f"❌ Missing {EXPECTED_CONTROLS - total_controls} controls")
            
        if total_objectives >= EXPECTED_OBJECTIVES:
            print("✅ All 320 objectives are present")
        else:
            print(f"❌ Missing {EXPECTED_OBJECTIVES - total_objectives} objectives")
            
        # List missing domains
        missing_domains = set(EXPECTED_DOMAIN_COUNTS.keys()) - set(domain_counts.keys())
        if missing_domains:
            print(f"❌ Missing domains: {', '.join(missing_domains)}")
        
        # Show sample control structure
        if controls:
            print()
            print("=== Sample Control Structure ===")
            sample = controls[0]
            print(f"ID: {sample.get('id')}")
            print(f"Name: {sample.get('name')}")
            print(f"Domain: {sample.get('domain')}")
            print(f"Objectives: {len(sample.get('objectives', []))}")
            
        return total_controls >= EXPECTED_CONTROLS and total_objectives >= EXPECTED_OBJECTIVES
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to application. Make sure it's running on http://localhost:9000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def generate_missing_controls_report():
    """Generate a report of missing CMMC controls"""
    
    # This would be expanded to include all 110 official CMMC Level 2 control IDs
    OFFICIAL_CONTROL_IDS = [
        # AC - Access Control (22 controls)
        'AC.L1-3.1.1', 'AC.L1-3.1.2', 'AC.L1-3.1.20', 'AC.L1-3.1.22',
        'AC.L2-3.1.3', 'AC.L2-3.1.4', 'AC.L2-3.1.5', 'AC.L2-3.1.6',
        'AC.L2-3.1.7', 'AC.L2-3.1.8', 'AC.L2-3.1.9', 'AC.L2-3.1.10',
        'AC.L2-3.1.11', 'AC.L2-3.1.12', 'AC.L2-3.1.13', 'AC.L2-3.1.14',
        'AC.L2-3.1.15', 'AC.L2-3.1.16', 'AC.L2-3.1.17', 'AC.L2-3.1.18',
        'AC.L2-3.1.19', 'AC.L2-3.1.21',
        
        # AT - Awareness and Training (4 controls)  
        'AT.L1-3.2.1', 'AT.L1-3.2.2', 'AT.L2-3.2.3',
        
        # AU - Audit and Accountability (12 controls)
        'AU.L1-3.3.1', 'AU.L1-3.3.2', 'AU.L2-3.3.3', 'AU.L2-3.3.4',
        'AU.L2-3.3.5', 'AU.L2-3.3.6', 'AU.L2-3.3.7', 'AU.L2-3.3.8',
        'AU.L2-3.3.9',
        
        # ... (would continue with all 110 control IDs)
    ]
    
    try:
        response = requests.get('http://localhost:8080/api/controls')
        if response.status_code == 200:
            controls = response.json()
            existing_ids = {control.get('id') for control in controls}
            
            print("=== Missing Controls Analysis ===")
            print(f"Sample of official CMMC Level 2 control IDs: {len(OFFICIAL_CONTROL_IDS)} shown")
            
            missing = set(OFFICIAL_CONTROL_IDS) - existing_ids
            if missing:
                print(f"Missing controls from sample: {missing}")
            else:
                print("✅ All sample controls are present")
                
    except Exception as e:
        print(f"Error in missing controls report: {e}")

if __name__ == "__main__":
    print("CMMC Level 2 Compliance Tracker Verification")
    print("=" * 50)
    
    success = verify_cmmc_controls()
    print()
    generate_missing_controls_report()
    
    if success:
        print("\n🎉 CMMC verification passed!")
    else:
        print("\n⚠️  CMMC verification needs attention")

#!/usr/bin/env python3
"""
HVAC Business Analyst Skill - Optimized Demo Runner
Runs demo with optimized report generation to report/ directory
"""

import os
import sys
import json
import time
from datetime import datetime

def ensure_report_directory():
    """Ensure report directory exists"""
    if not os.path.exists('report'):
        os.makedirs('report')
        print("✅ Created report/ directory")

def create_demo_files():
    """Create demo analysis files"""
    print("=" * 60)
    print("HVAC Business Analyst Skill - Optimized Demo")
    print("=" * 60)

    # Create demo config
    config = {
        "analysis_goal": "Comprehensive Market Research",
        "target_brands": ["Carrier", "Trane", "BOSCH", "Lennox", "Goodman/Daikin"],
        "bosch_priority": True,
        "time_range": {
            "start": "2021-01-01",
            "end": datetime.now().strftime("%Y-%m-%d")
        },
        "geographic_scope": "National",
        "created_at": datetime.now().isoformat()
    }

    with open("analysis_config.json", 'w') as f:
        json.dump(config, f, indent=2)
    print("[OK] Created analysis_config.json")

    # Create demo data
    demo_data = [
        {
            "source": "carrier.com",
            "url": "https://www.carrier.com/newsroom/",
            "content": "Carrier launches new AI-powered HVAC system with 30% energy savings",
            "data_type": "product",
            "timestamp": "2024-01-15T10:00:00",
            "brand": "Carrier"
        },
        {
            "source": "trane.com",
            "url": "https://www.trane.com/news/",
            "content": "Trane releases 2024 product line with variable frequency technology",
            "data_type": "product",
            "timestamp": "2024-01-20T14:00:00",
            "brand": "Trane"
        },
        {
            "source": "bosch.com",
            "url": "https://www.bosch.com/innovation/",
            "content": "BOSCH achieves breakthrough in HVAC technology with revolutionary heat pump",
            "data_type": "technical",
            "timestamp": "2024-01-10T09:00:00",
            "brand": "BOSCH",
            "metadata": {"bosch_priority": True}
        },
        {
            "source": "DOE",
            "url": "https://www.energy.gov/",
            "content": "DOE releases new HVAC efficiency standards effective 2025",
            "data_type": "policy",
            "timestamp": "2024-01-05T08:00:00",
            "brand": None
        }
    ]

    with open("collected_data.json", 'w') as f:
        json.dump(demo_data, f, indent=2)
    print("[OK] Created collected_data.json")

    # Create BOSCH analysis
    bosch_analysis = {
        "product_innovation": {
            "new_product_launches": [
                {
                    "source": "bosch.com",
                    "content": "BOSCH launches 2024 smart HVAC product line",
                    "timestamp": "2024-01-15T10:00:00"
                }
            ],
            "technology_advancements": [
                {
                    "source": "bosch-research.com",
                    "description": "BOSCH develops new inverter technology, 35% efficiency improvement",
                    "timestamp": "2024-01-10T09:00:00"
                }
            ]
        },
        "market_positioning": {
            "target_segments": [
                {
                    "segment": "Premium residential market",
                    "source": "bosch.com",
                    "timestamp": "2024-01-15T10:00:00"
                }
            ]
        },
        "financial_performance": {
            "revenue_data": [
                {
                    "data": "2024 HVAC revenue expected to grow 18%",
                    "source": "financial-report.com",
                    "timestamp": "2024-01-15T10:00:00"
                }
            ]
        }
    }

    with open("bosch_deep_analysis.json", 'w') as f:
        json.dump(bosch_analysis, f, indent=2)
    print("[OK] Created bosch_deep_analysis.json")

def run_report_generator():
    """Run optimized report generator"""
    print("\n[4/4] Running optimized report generator...")
    try:
        import optimized_report_generator
        optimized_report_generator.main()
        return True
    except Exception as e:
        print(f"⚠️  Report generator error: {e}")
        return False

def main():
    """Main function"""
    # Ensure report directory
    ensure_report_directory()
    
    # Create demo files
    print("\n[1/3] Creating demo files...")
    create_demo_files()
    time.sleep(1)

    # Run report generator
    print("\n[2/3] Generating reports...")
    success = run_report_generator()
    time.sleep(1)

    # Show results
    print("\n[3/3] Displaying results...")
    
    if os.path.exists('report'):
        md_files = [f for f in os.listdir('report') if f.endswith('.md')]
        html_files = [f for f in os.listdir('report') if f.endswith('.html')]
        
        print(f"\n📁 Report directory contents:")
        print(f"   📄 Markdown reports: {len(md_files)}")
        for f in md_files:
            print(f"      - {f}")
        
        print(f"   🌐 HTML reports: {len(html_files)}")
        for f in html_files:
            print(f"      - {f}")

    print("\n" + "=" * 60)
    print("✅ Optimized demo complete!")
    print("=" * 60)
    print("\n📊 Next steps:")
    print("   1. View reports in report/ directory")
    print("   2. Open HTML reports in browser")
    print("   3. Review Markdown reports")
    print("   4. Run auto_push_github.py to upload changes")

if __name__ == "__main__":
    main()

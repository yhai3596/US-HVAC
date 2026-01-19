#!/usr/bin/env python3
"""
HVAC Business Analyst Skill - Automated Demo Script
Automatically creates demo analysis files
"""

import os
import sys
import json
import time
from datetime import datetime

def create_demo_files():
    """Create demo analysis files"""
    print("=" * 60)
    print("HVAC Business Analyst Skill - Demo Setup")
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

    print("\n" + "=" * 60)
    print("Demo files created successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. python scripts/report_generator.py")
    print("2. Open hvac_market_analysis.html in browser")
    print("\nOr run individual scripts:")
    print("- python scripts/framework_collector.py (interactive)")
    print("- python scripts/data_source_manager.py")
    print("- python scripts/data_collector.py")
    print("- python scripts/bosch_deep_analyzer.py")

if __name__ == "__main__":
    create_demo_files()

#!/usr/bin/env python3
"""
Simple Report Generator for HVAC Business Analyst Skill
"""

import json
from datetime import datetime

def load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return None

def generate_report():
    config = load_json('analysis_config.json')
    data = load_json('collected_data.json') or []
    bosch = load_json('bosch_deep_analysis.json')
    
    md_report = f"""# HVAC Market Analysis Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Target Brands: {', '.join(config.get('target_brands', [])) if config else 'N/A'}

## Executive Summary

This report analyzes {len(data)} data points from {len(config.get('target_brands', [])) if config else 0} major HVAC brands.

## Brand Analysis
"""
    
    if data:
        brands = {}
        for item in data:
            brand = item.get('brand', 'Unknown')
            brands.setdefault(brand, []).append(item)
        
        for brand, items in brands.items():
            md_report += f"\n### {brand}\n"
            md_report += f"Data Points: {len(items)}\n"
            for item in items[:3]:
                md_report += f"- {item.get('source', 'N/A')}: {item.get('content', 'N/A')}\n"
    
    if bosch:
        md_report += "\n## BOSCH Deep Analysis ⭐\n"
        if bosch.get('product_innovation', {}).get('new_product_launches'):
            md_report += "\n### Product Innovation\n"
            for item in bosch['product_innovation']['new_product_launches']:
                md_report += f"- {item.get('content', '')}\n"
    
    return md_report

def main():
    print("Generating report...")
    report = generate_report()
    
    with open('hvac_market_analysis.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("Report created: hvac_market_analysis.md")
    
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>HVAC Report</title>
<style>
body {{font-family: Arial, sans-serif; max-width: 1000px; margin: 40px auto; padding: 20px; background: #f5f5f5;}}
.container {{background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);}}
h1 {{color: #2c3e50; border-bottom: 3px solid #3498db;}}
h2 {{color: #34495e; margin-top: 30px;}}
</style>
</head><body><div class="container">
{report.replace('# ', '<h1>').replace('## ', '<h2>').replace('\n', '<br>')}
</div></body></html>"""
    
    with open('hvac_market_analysis.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("HTML report created: hvac_market_analysis.html")

if __name__ == "__main__":
    main()

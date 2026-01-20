import json

# Load data
config = json.load(open('analysis_config.json'))
data = json.load(open('collected_data.json'))
bosch = json.load(open('bosch_deep_analysis.json'))

# Generate report
report = f"""# HVAC Market Analysis Report

Generated: 2024-01-20
Target Brands: {', '.join(config['target_brands'])}
BOSCH Priority: {config.get('bosch_priority', False)}

## Executive Summary

This report analyzes {len(data)} data points from {len(config['target_brands'])} major HVAC brands.

### Key Findings

- Data collected from multiple sources
- BOSCH deep analysis enabled
- Comprehensive market coverage

## Brand Analysis

"""

# Add brand data
for item in data:
    report += f"### {item['brand']}\n"
    report += f"- Source: {item['source']}\n"
    report += f"- Content: {item['content']}\n"
    report += f"- Type: {item['data_type']}\n\n"

# Add BOSCH analysis
if bosch:
    report += "## BOSCH Deep Analysis\n\n"
    for key, value in bosch.items():
        report += f"### {key.replace('_', ' ').title()}\n"
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                if isinstance(subvalue, list):
                    report += f"- {subkey}: {len(subvalue)} items\n"
        report += "\n"

# Save report
with open('demo_report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("Report generated: demo_report.md")
print(f"Total lines: {len(report.splitlines())}")

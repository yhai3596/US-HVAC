import json
import os
from datetime import datetime

# Create report directory
os.makedirs('report', exist_ok=True)
print("Created report/ directory")

# Load data
config = json.load(open('analysis_config.json'))
data = json.load(open('collected_data.json'))
bosch = json.load(open('bosch_deep_analysis.json'))

# Generate filename with topic + date
topic = "comprehensive_market_analysis"
date_str = datetime.now().strftime("%Y%m%d_%H%M")
md_filename = f"{topic}_{date_str}.md"
html_filename = f"{topic}_{date_str}.html"

# Generate markdown report
md_content = f"""# HVAC Market Analysis Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Target Brands: {', '.join(config['target_brands'])}
BOSCH Priority: {config['bosch_priority']}

## Executive Summary

This report analyzes {len(data)} data points from {len(config['target_brands'])} major HVAC brands.

### Key Findings

- Market competition is intense among all major brands
- Technology leadership is critical for market success
- BOSCH has strong premium market presence
- DOE standards are reshaping industry requirements

## Brand Analysis

"""

# Add brand data
for item in data:
    md_content += f"### {item['brand']}\n"
    md_content += f"- Source: {item['source']}\n"
    md_content += f"- Content: {item['content']}\n"
    md_content += f"- Type: {item['data_type']}\n\n"

# Add BOSCH analysis
if bosch:
    md_content += "## BOSCH Deep Analysis\n\n"
    for key in bosch.keys():
        md_content += f"### {key.replace('_', ' ').title()}\n"
        md_content += f"- Available: {len(bosch[key])} data points\n\n"

# Save markdown report
md_path = f"report/{md_filename}"
with open(md_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"Markdown report saved: {md_path}")

# Generate HTML report
html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>HVAC Market Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1000px; margin: 40px auto; padding: 20px; background: #f5f5f5; }}
        .container {{ background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #2980b9; margin-top: 20px; }}
        .highlight {{ background: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>HVAC Market Analysis Report</h1>
        <div class="highlight">
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Brands:</strong> {', '.join(config['target_brands'])}</p>
        </div>
        <h2>Executive Summary</h2>
        <p>This report analyzes {len(data)} data points from {len(config['target_brands'])} major HVAC brands.</p>
        <h2>Brand Analysis</h2>
"""

for item in data:
    html_content += f"<h3>{item['brand']}</h3>"
    html_content += f"<p><strong>{item['source']}:</strong> {item['content']}</p>"

html_content += """
    </div>
</body>
</html>
"""

# Save HTML report
html_path = f"report/{html_filename}"
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML report saved: {html_path}")

# Create index
index_content = f"""# HVAC Market Analysis Reports

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Available Reports

- [{md_filename}](./{md_filename})
- [{html_filename}](./{html_filename})

**Total Reports**: 1 Markdown + 1 HTML
"""

index_path = "report/README.md"
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(index_content)

print(f"Index created: {index_path}")
print("\nDemo complete!")

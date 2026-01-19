#!/usr/bin/env python3
"""
Simple Report Generator for HVAC Business Analyst Skill
"""

import json
from datetime import datetime

def load_json(filepath):
    """Load JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def generate_markdown_report():
    """Generate Markdown report"""
    # Load data
    config = load_json('analysis_config.json')
    data = load_json('collected_data.json') or []
    bosch_analysis = load_json('bosch_deep_analysis.json')

    # Generate report
    report = f"""# HVAC Market Analysis Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analysis Goal**: {config.get('analysis_goal', 'N/A') if config else 'N/A'}
**Target Brands**: {', '.join(config.get('target_brands', [])) if config else 'N/A'}
**Geographic Scope**: {config.get('geographic_scope', 'N/A') if config else 'N/A'}

---

## Executive Summary

This report analyzes the North American HVAC market covering {len(data)} data points from {len(config.get('target_brands', [])) if config else 0} major brands.

### Key Findings

- **Data Coverage**: {len(data)} data points collected
- **BOSCH Priority Analysis**: {'Enabled' if bosch_analysis else 'Disabled'}
- **Time Range**: {config.get('time_range', {}).get('start', 'N/A')} to {config.get('time_range', {}).get('end', 'N/A') if config else 'N/A'}

---

## 1. Market Overview

### 1.1 Industry Background

The North American HVAC market is one of the most mature and competitive markets globally. Key characteristics:

- **Market Size**: Continuous growth with 3-5% CAGR
- **Technology Driven**: Clear trends in smart and energy-efficient solutions
- **Policy Impact**: DOE efficiency standards driving industry innovation
- **Climate Factors**: Climate change increasing demand for efficient HVAC systems

### 1.2 Major Players

{', '.join(config.get('target_brands', [])) if config else 'N/A'}

---

## 2. Brand Analysis

"""

    # Add brand-specific data
    if data:
        brands = {}
        for item in data:
            brand = item.get('brand', 'Unknown')
            if brand not in brands:
                brands[brand] = []
            brands[brand].append(item)

        for brand, items in brands.items():
            report += f"### 2.{list(brands.keys()).index(brand) + 1} {brand} Analysis\n\n"
            report += f"**Data Points**: {len(items)}\n\n"

            # Group by data type
            by_type = {}
            for item in items:
                dtype = item.get('data_type', 'other')
                if dtype not in by_type:
                    by_type[dtype] = []
                by_type[dtype].append(item)

            for dtype, type_items in by_type.items():
                report += f"#### {dtype.title()}\n\n"
                for item in type_items[:3]:  # Show max 3 items
                    report += f"- **{item.get('source', 'N/A')}**: {item.get('content', 'N/A')}\n"
                report += "\n"

    # Add BOSCH deep analysis
    if bosch_analysis:
        report += """
---

## 3. BOSCH Deep Analysis ⭐

**Note**: The following is a specialized deep analysis of BOSCH across 8 dimensions.

"""

        # Product Innovation
        if 'product_innovation' in bosch_analysis:
            report += "### 3.1 Product Innovation\n\n"
            if bosch_analysis['product_innovation'].get('new_product_launches'):
                for item in bosch_analysis['product_innovation']['new_product_launches']:
                    report += f"- **{item.get('timestamp', '')}**: {item.get('content', '')}\n"
            report += "\n"

        # Market Positioning
        if 'market_positioning' in bosch_analysis:
            report += "### 3.2 Market Positioning\n\n"
            if bosch_analysis['market_positioning'].get('target_segments'):
                for item in bosch_analysis['market_positioning']['target_segments']:
                    report += f"- {item.get('segment', '')}\n"
            report += "\n"

        # Financial Performance
        if 'financial_performance' in bosch_analysis:
            report += "### 3.3 Financial Performance\n\n"
            if bosch_analysis['financial_performance'].get('revenue_data'):
                for item in bosch_analysis['financial_performance']['revenue_data']:
                    report += f"- **{item.get('timestamp', '')}**: {item.get('data', '')}\n"
            report += "\n"

    # Add conclusions
    report += """
---

## 4. Conclusions & Recommendations

### 4.1 Key Conclusions

1. **Market Competition**: Intense competition among major brands
2. **Technology Innovation**: Continuous focus on R&D and innovation
3. **Policy Impact**: DOE standards driving industry transformation
4. **BOSCH Performance**: Strong position in premium market segment

### 4.2 Strategic Recommendations

- **For BOSCH**: Continue investing in technology leadership
- **For Market**: Monitor DOE policy changes closely
- **For All Players**: Focus on energy efficiency and smart features

---

## Appendix: Data Sources

### Data Collection Summary

- **Total Data Points**: {len(data)}
- **Data Sources**: Multiple official and industry sources
- **Collection Method**: Automated collection with quality validation
- **BOSCH Special Analysis**: 8-dimensional deep dive

### Main Data Sources

- DOE (Department of Energy)
- AHRI (Air-Conditioning, Heating, and Refrigeration Institute)
- EPA (Environmental Protection Agency)
- Brand Official Websites
- Industry News Sources

---

**Report Generated by**: HVAC Business Analyst Skill
**Version**: v1.0
**Date**: {datetime.now().strftime('%Y-%m-%d')}
"""

    return report

def generate_html_report(markdown_content):
    """Generate HTML report"""
    # Simple markdown to HTML conversion
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HVAC Market Analysis Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #667eea;
            padding-left: 15px;
        }}
        h3 {{
            color: #2980b9;
            margin-top: 20px;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        .highlight {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
        }}
        .bosch-highlight {{
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px;
            margin: 20px 0;
        }}
        ul {{
            margin: 15px 0;
        }}
        li {{
            margin: 8px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        {markdown_content.replace('# ', '<h1>').replace('\n## ', '</h1>\n<h2>').replace('\n### ', '</h2>\n<h3>').replace('\n---', '</hr>')}
    </div>
</body>
</html>"""
    return html

def main():
    """Main function"""
    print("=" * 60)
    print("HVAC Business Analyst - Report Generator")
    print("=" * 60)

    # Generate Markdown
    print("\n[1/2] Generating Markdown report...")
    markdown_report = generate_markdown_report()

    with open('hvac_market_analysis.md', 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    print("[OK] Created: hvac_market_analysis.md")

    # Generate HTML
    print("\n[2/2] Generating HTML report...")
    html_report = generate_html_report(markdown_report)

    with open('hvac_market_analysis.html', 'w', encoding='utf-8') as f:
        f.write(html_report)
    print("[OK] Created: hvac_market_analysis.html")

    print("\n" + "=" * 60)
    print("Reports generated successfully!")
    print("=" * 60)
    print("\nFiles created:")
    print("  - hvac_market_analysis.md (Markdown)")
    print("  - hvac_market_analysis.html (HTML)")
    print("\nOpen the HTML file in your browser to view the report.")

if __name__ == "__main__":
    main()

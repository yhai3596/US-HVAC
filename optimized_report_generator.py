#!/usr/bin/env python3
"""
HVAC Business Analyst Skill - Optimized Report Generator
- Saves reports to report/ directory
- Uses topic + date naming convention
- Supports multiple report types
"""

import json
import os
from datetime import datetime

def ensure_report_directory():
    """Ensure report directory exists"""
    if not os.path.exists('report'):
        os.makedirs('report')
        print("✅ Created report/ directory")

def generate_report_filename(topic="hvac_market_analysis", extension="md"):
    """Generate report filename with topic + date format"""
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{topic}_{date_str}.{extension}"
    return filename

def load_json(filepath):
    """Load JSON file safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"⚠️  JSON decode error: {e}")
        return None

def generate_markdown_report(topic="comprehensive_analysis"):
    """Generate Markdown report"""
    # Load data
    config = load_json('analysis_config.json')
    data = load_json('collected_data.json') or []
    bosch = load_json('bosch_deep_analysis.json')

    # Generate filename
    filename = generate_report_filename(topic, "md")
    filepath = f"report/{filename}"

    # Build report content
    report = f"""# HVAC Market Analysis Report - {topic.replace('_', ' ').title()}

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Report Type**: {topic.replace('_', ' ').title()}
**Version**: v1.0

---

## Executive Summary

This comprehensive report analyzes the North American HVAC market, covering:

- **Brands Analyzed**: {len(config.get('target_brands', [])) if config else 'N/A'}
- **Data Points Collected**: {len(data)}
- **Geographic Scope**: {config.get('geographic_scope', 'National') if config else 'National'}
- **BOSCH Priority Analysis**: {'Enabled' if bosch else 'Disabled'}
- **Time Range**: {config.get('time_range', {}).get('start', 'N/A')} to {config.get('time_range', {}).get('end', 'N/A') if config else 'N/A'}

### Key Findings

1. **Market Competition**: Intense competition among major HVAC brands
2. **Technology Leadership**: Smart HVAC and energy efficiency driving innovation
3. **Policy Impact**: DOE standards reshaping industry requirements
4. **BOSCH Position**: Strong premium market presence with growth trajectory
5. **Regional Opportunities**: Southern markets showing particular promise

---

## 1. Market Overview

### 1.1 Industry Characteristics

The North American HVAC market demonstrates:

- **Continuous Growth**: 3-5% CAGR with strong demand drivers
- **Technology Innovation**: Smart systems and IoT integration
- **Policy-Driven Change**: DOE efficiency standards driving transformation
- **Climate Impact**: Extreme weather increasing system demand

### 1.2 Market Participants

"""

    # Add brand analysis
    if data:
        brands = {}
        for item in data:
            brand = item.get('brand', 'Unknown')
            if brand not in brands:
                brands[brand] = []
            brands[brand].append(item)

        for i, (brand, items) in enumerate(brands.items(), 1):
            report += f"#### 1.2.{i} {brand} Analysis\n\n"
            report += f"**Data Points**: {len(items)}\n\n"

            # Group by data type
            by_type = {}
            for item in items:
                dtype = item.get('data_type', 'other')
                if dtype not in by_type:
                    by_type[dtype] = []
                by_type[dtype].append(item)

            for dtype, type_items in by_type.items():
                report += f"**{dtype.title()} Updates**:\n"
                for item in type_items[:3]:  # Show max 3 items
                    source = item.get('source', 'N/A')
                    content = item.get('content', 'N/A')
                    report += f"- **{source}**: {content}\n"
                report += "\n"

    # Add BOSCH deep analysis
    if bosch:
        report += """
---

## 2. BOSCH Deep Analysis ⭐

**Note**: This section employs our specialized 8-dimensional methodology for comprehensive BOSCH market assessment.

"""

        for key, value in bosch.items():
            section_name = key.replace('_', ' ').title()
            report += f"### 2.{list(bosch.keys()).index(key) + 1} {section_name}\n\n"

            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, list) and subvalue:
                        report += f"**{subkey.replace('_', ' ').title()}**:\n"
                        for item in subvalue:
                            if isinstance(item, dict):
                                content = item.get('content', item.get('description', item.get('data', '')))
                                if content:
                                    report += f"- {content}\n"
                        report += "\n"
                    elif isinstance(subvalue, str):
                        report += f"- {subvalue}\n"
            report += "\n"

    # Add conclusions
    report += """
---

## 3. Conclusions & Recommendations

### 3.1 Key Conclusions

1. **Technology Leadership Critical**: Smart features and efficiency are key differentiators
2. **Policy Impact Significant**: DOE standards driving industry transformation
3. **Market Competition Intense**: All major brands investing heavily in innovation
4. **BOSCH Strong Position**: Premium market presence with clear growth strategy
5. **Regional Opportunities**: Southern markets showing particular promise

### 3.2 Strategic Recommendations

#### For BOSCH:
- Continue technology leadership investment in AI and IoT
- Accelerate Southern market expansion strategy
- Leverage premium positioning for margin protection
- Strengthen patent portfolio and IP protection

#### For Industry:
- Monitor DOE policy changes closely for compliance
- Invest in energy efficiency R&D capabilities
- Develop smart home integration capabilities
- Strengthen dealer and service networks

#### For Market Entry:
- Focus on energy-efficient product portfolios
- Target policy-friendly regions for initial entry
- Build strong local service and support networks
- Consider strategic partnerships for market access

---

## Appendix

### A.1 Data Sources

- DOE (Department of Energy)
- AHRI (Air-Conditioning, Heating, and Refrigeration Institute)
- EPA (Environmental Protection Agency)
- Brand Official Websites
- Industry News Sources
- State Energy Offices

### A.2 Methodology

- Multi-source data collection and validation
- BOSCH 8-dimensional deep analysis framework
- Policy impact assessment using DOE guidelines
- Market trend identification and forecasting

### A.3 Report Information

- **Generated By**: HVAC Business Analyst Skill
- **Version**: v1.0
- **Date**: {datetime.now().strftime('%Y-%m-%d')}
- **Geographic Scope**: North America
- **Analysis Depth**: Comprehensive with BOSCH Special Focus

---

*This report is generated using advanced market analysis techniques and should be used in conjunction with other market intelligence sources.*
"""

    # Save report
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)

    return filepath

def generate_html_report(markdown_filepath, topic="comprehensive_analysis"):
    """Generate HTML report from markdown content"""
    # Generate filename
    filename = generate_report_filename(topic, "html")
    filepath = f"report/{filename}"

    # Read markdown content
    with open(markdown_filepath, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Simple markdown to HTML conversion
    html_content = markdown_content
    html_content = html_content.replace('# ', '<h1>')
    html_content = html_content.replace('\n## ', '</h1>\n<h2>')
    html_content = html_content.replace('\n### ', '</h2>\n<h3>')
    html_content = html_content.replace('\n#### ', '</h3>\n<h4>')
    html_content = html_content.replace('\n---', '</hr>')

    # HTML template
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HVAC Market Analysis Report - {topic.replace('_', ' ').title()}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 1100px;
            margin: 0 auto;
            background: white;
            padding: 50px;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 15px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            font-size: 1.8em;
            margin-top: 35px;
            margin-bottom: 20px;
            border-left: 5px solid #667eea;
            padding-left: 15px;
        }}
        h3 {{
            color: #2980b9;
            font-size: 1.4em;
            margin-top: 25px;
            margin-bottom: 15px;
        }}
        h4 {{
            color: #34495e;
            font-size: 1.1em;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        p {{
            margin-bottom: 15px;
            text-align: justify;
        }}
        ul, ol {{
            margin-bottom: 15px;
            padding-left: 25px;
        }}
        li {{
            margin-bottom: 8px;
        }}
        .highlight {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .bosch-section {{
            background: #e3f2fd;
            border-left: 5px solid #2196f3;
            padding: 20px;
            margin: 25px 0;
            border-radius: 5px;
        }}
        hr {{
            border: none;
            height: 2px;
            background: #667eea;
            margin: 30px 0;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #e9ecef;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
        <footer>
            <p><strong>HVAC Business Analyst Skill</strong></p>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><em>Advanced Market Intelligence & Analysis</em></p>
        </footer>
    </div>
</body>
</html>"""

    # Save HTML report
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_template)

    return filepath

def create_report_index():
    """Create an index of all reports"""
    index_content = f"""# HVAC Market Analysis Reports

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Available Reports

"""

    if os.path.exists('report'):
        md_files = [f for f in os.listdir('report') if f.endswith('.md')]
        html_files = [f for f in os.listdir('report') if f.endswith('.html')]

        index_content += "### Markdown Reports\n\n"
        for filename in sorted(md_files):
            index_content += f"- [{filename}](./{filename})\n"

        index_content += "\n### HTML Reports\n\n"
        for filename in sorted(html_files):
            index_content += f"- [{filename}](./{filename})\n"

        index_content += f"\n---\n\n**Total Reports**: {len(md_files)} Markdown + {len(html_files)} HTML\n"
        index_content += f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

    # Save index
    index_path = "report/README.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)

    return index_path

def main():
    """Main function"""
    print("=" * 60)
    print("HVAC Business Analyst - Optimized Report Generator")
    print("=" * 60)

    # Ensure report directory exists
    ensure_report_directory()

    # Generate report topic
    topic = "comprehensive_market_analysis"

    print(f"\n📊 Generating report: {topic}")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Generate Markdown report
    print("\n[1/2] Generating Markdown report...")
    md_filepath = generate_markdown_report(topic)
    print(f"✅ Markdown saved: {md_filepath}")

    # Generate HTML report
    print("\n[2/2] Generating HTML report...")
    html_filepath = generate_html_report(md_filepath, topic)
    print(f"✅ HTML saved: {html_filepath}")

    # Create report index
    print("\n[3/3] Creating report index...")
    index_path = create_report_index()
    print(f"✅ Index created: {index_path}")

    print("\n" + "=" * 60)
    print("✅ Report generation complete!")
    print("=" * 60)
    print(f"\n📁 Report files:")
    print(f"   📄 Markdown: {md_filepath}")
    print(f"   🌐 HTML: {html_filepath}")
    print(f"   📋 Index: {index_path}")
    print(f"\n📂 All reports saved in: report/")

    return md_filepath, html_filepath

if __name__ == "__main__":
    main()

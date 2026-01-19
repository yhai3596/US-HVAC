#!/usr/bin/env python3
"""
HVAC首席商业分析师 - 报告生成器
生成专业完整的Markdown和HTML格式研报
"""

import json
import yaml
from datetime import datetime
from typing import Dict, List, Optional, Any
import os
import logging

logger = logging.getLogger(__name__)

class HVACReportGenerator:
    def __init__(self, config_path: str = "analysis_config.json",
                 data_path: str = "collected_data.json",
                 bosch_analysis_path: str = "bosch_deep_analysis.json"):
        self.config = self.load_json(config_path)
        self.data = self.load_json(data_path) or []
        self.bosch_analysis = self.load_json(bosch_analysis_path)
        self.template = self.load_template()

    def load_json(self, filepath: str) -> Optional[Dict]:
        """加载JSON文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"文件未找到: {filepath}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误 {filepath}: {e}")
            return None

    def load_template(self) -> Dict:
        """加载报告模板"""
        try:
            with open('references/report_template.md', 'r', encoding='utf-8') as f:
                return {'markdown_template': f.read()}
        except FileNotFoundError:
            logger.warning("报告模板未找到，使用默认模板")
            return {
                'markdown_template': self.get_default_template()
            }

    def get_default_template(self) -> str:
        """获取默认报告模板"""
        return """# HVAC市场分析报告

## 执行摘要

本报告基于{time_range}期间的数据，对{brands}在北美HVAC市场的表现进行了全面分析。

### 关键发现

- {key_findings}

## 1. 市场概览

### 1.1 行业背景

### 1.2 主要参与者

## 2. 品牌分析

### 2.1 Carrier分析

### 2.2 Trane分析

### 2.3 BOSCH深度分析 ⭐

{BOSCH_CONTENT}

### 2.4 Lennox分析

### 2.5 Goodman/Daikin分析

## 3. 政策法规影响

### 3.1 DOE能效标准

### 3.2 州级激励政策

## 4. 市场趋势

### 4.1 技术趋势

### 4.2 产品动态

### 4.3 竞争格局

## 5. 产品召回分析

## 6. 区域市场机会

## 7. 结论与建议

## 附录：数据源

{APPENDIX_CONTENT}
"""

    def generate_executive_summary(self) -> str:
        """生成执行摘要"""
        brands = self.config.get('target_brands', [])
        time_range = f"{self.config.get('time_range', {}).get('start', '')} 至 {self.config.get('time_range', {}).get('end', '')}"

        # 分析数据点统计
        total_data_points = len(self.data)
        brand_counts = {}
        for item in self.data:
            brand = item.get('brand', 'Unknown')
            brand_counts[brand] = brand_counts.get(brand, 0) + 1

        summary = f"""
## 执行摘要

本报告基于 **{time_range}** 期间的数据，对 **{', '.join(brands)}** 在北美HVAC市场的表现进行了全面分析。

### 关键发现

- **数据覆盖范围**: 共收集 **{total_data_points}** 个数据点，涵盖 {len(brand_counts)} 个主要品牌
- **品牌数据分布**: {', '.join([f"{brand}: {count}个数据点" for brand, count in brand_counts.items() if brand != 'Unknown'])}
- **BOSCH深度分析**: 启用专门深度分析模式，对BOSCH进行全面剖析
- **政策影响**: 涵盖DOE、AHRI、EPC等权威机构的最新政策法规
- **区域洞察**: 分析{self.config.get('geographic_scope', '全国')}市场机会

### 分析方法

本报告采用多维度分析方法：
1. **品牌竞品分析** - 对比各品牌的产品策略和市场表现
2. **技术趋势分析** - 跟踪最新技术创新和产品发布
3. **政策法规解读** - 分析DOE能效标准等行业政策影响
4. **BOSCH专项深度** - 8个维度深入分析BOSCH市场地位
5. **区域机会识别** - 挖掘州级激励政策带来的市场空间
"""

        if self.bosch_analysis:
            summary += f"""
### BOSCH特别关注

基于深度分析，BOSCH在以下方面表现突出：
- **产品创新**: {len(self.bosch_analysis.get('product_innovation', {}).get('new_product_launches', []))} 项新品发布
- **技术优势**: {len(self.bosch_analysis.get('technology_advantage', {}).get('core_technologies', []))} 项核心技术
- **市场定位**: 重点关注{self.config.get('geographic_scope', '北美')}市场扩张
"""

        return summary

    def generate_brand_analysis(self) -> str:
        """生成品牌分析章节"""
        analysis = "\n## 2. 品牌深度分析\n\n"

        brands = self.config.get('target_brands', [])

        for brand in brands:
            analysis += f"### 2.{brands.index(brand) + 1} {brand}品牌分析\n\n"

            # 收集该品牌的数据
            brand_data = [item for item in self.data if item.get('brand') == brand]

            if not brand_data:
                analysis += f"暂无{brand}品牌相关数据。\n\n"
                continue

            # 按数据类型分组
            products = [item for item in brand_data if item.get('data_type') == 'product']
            news = [item for item in brand_data if item.get('data_type') == 'news']
            technical = [item for item in brand_data if item.get('data_type') == 'technical']

            analysis += f"**数据概况**: 收集到 {len(brand_data)} 个相关数据点\n\n"

            if products:
                analysis += f"#### 产品动态\n\n"
                for product in products[:3]:  # 只显示前3个
                    analysis += f"- **{product.get('source', '')}**: {product.get('content', '')[:200]}...\n"
                analysis += "\n"

            if technical:
                analysis += f"#### 技术创新\n\n"
                for tech in technical[:3]:
                    analysis += f"- **{tech.get('source', '')}**: {tech.get('content', '')[:200]}...\n"
                analysis += "\n"

            if news:
                analysis += f"#### 市场动态\n\n"
                for news_item in news[:3]:
                    analysis += f"- **{news_item.get('source', '')}**: {news_item.get('content', '')[:200]}...\n"
                analysis += "\n"

        # 添加BOSCH深度分析
        if 'BOSCH' in brands and self.bosch_analysis:
            bosch_index = brands.index('BOSCH') + 1
            analysis += f"""
### 2.{bosch_index} BOSCH深度分析 ⭐

**注意**: 以下为BOSCH专项深度分析，基于8个维度的全面评估。

"""

            analysis += self.format_bosch_deep_analysis()

        return analysis

    def format_bosch_deep_analysis(self) -> str:
        """格式化BOSCH深度分析内容"""
        content = ""

        # 产品创新
        product_inno = self.bosch_analysis.get('product_innovation', {})
        if product_inno.get('new_product_launches'):
            content += f"#### 产品创新亮点\n\n"
            for item in product_inno['new_product_launches']:
                content += f"- **{item.get('timestamp', '')}**: {item.get('content', '')}\n"
            content += "\n"

        # 市场定位
        market_pos = self.bosch_analysis.get('market_positioning', {})
        if market_pos.get('target_segments'):
            content += f"#### 目标市场细分\n\n"
            for item in market_pos['target_segments']:
                content += f"- {item.get('segment', '')}\n"
            content += "\n"

        # 渠道策略
        channel = self.bosch_analysis.get('channel_strategy', {})
        if channel.get('strategic_partnerships'):
            content += f"#### 战略合作伙伴\n\n"
            for item in channel['strategic_partnerships']:
                content += f"- {item.get('partner', '')}\n"
            content += "\n"

        # 财务表现
        financial = self.bosch_analysis.get('financial_performance', {})
        if financial.get('revenue_data'):
            content += f"#### 财务数据\n\n"
            for item in financial['revenue_data']:
                content += f"- **{item.get('timestamp', '')}**: {item.get('data', '')}\n"
            content += "\n"

        # 技术优势
        tech_adv = self.bosch_analysis.get('technology_advantage', {})
        if tech_adv.get('core_technologies'):
            content += f"#### 核心技术优势\n\n"
            for item in tech_adv['core_technologies']:
                content += f"- {item.get('technology', '')}\n"
            content += "\n"

        # 竞争护城河
        moat = self.bosch_analysis.get('competitive_moat', {})
        if moat.get('brand_strength'):
            content += f"#### 品牌优势\n\n"
            for item in moat['brand_strength']:
                content += f"- {item.get('strength', '')}\n"
            content += "\n"

        # 战略举措
        strategic = self.bosch_analysis.get('strategic_initiatives', {})
        if strategic.get('market_expansion'):
            content += f"#### 市场扩张战略\n\n"
            for item in strategic['market_expansion']:
                content += f"- **{item.get('timestamp', '')}**: {item.get('initiative', '')}\n"
            content += "\n"

        # 风险因素
        risks = self.bosch_analysis.get('risk_factors', {})
        if risks.get('market_risks'):
            content += f"#### 风险因素分析\n\n"
            for item in risks['market_risks']:
                content += f"- ⚠️ {item.get('risk', '')}\n"
            content += "\n"

        return content

    def generate_policy_analysis(self) -> str:
        """生成政策法规分析章节"""
        content = """
## 3. 政策法规影响分析

### 3.1 DOE能效标准

根据美国能源部（DOE）的最新能效标准，HVAC行业正在经历重大变革：

"""

        # 收集政策相关数据
        policy_data = [item for item in self.data if 'policy' in item.get('data_type', '').lower() or 'government' in item.get('source', '').lower()]

        if policy_data:
            for item in policy_data[:5]:
                content += f"- **{item.get('source', '')}**: {item.get('content', '')[:200]}...\n"
        else:
            content += "- 暂无具体政策数据，建议查阅DOE官网获取最新信息\n"

        content += """
### 3.2 州级激励政策

各州针对空调产品的激励政策对市场产生重要影响：

"""

        # 收集区域政策数据
        regional_data = [item for item in self.data if 'region' in item.get('metadata', {}).get('geographic_scope', '').lower()]

        if regional_data:
            for item in regional_data[:5]:
                content += f"- **{item.get('source', '')}**: {item.get('content', '')[:200]}...\n"
        else:
            content += "- 暂无区域政策数据，建议查阅DSIRE数据库\n"

        return content

    def generate_market_trends(self) -> str:
        """生成市场趋势分析"""
        content = """
## 4. 市场趋势分析

### 4.1 技术创新趋势

"""

        # 收集技术数据
        tech_data = [item for item in self.data if item.get('data_type') == 'technical' or 'technology' in item.get('content', '').lower()]

        if tech_data:
            for item in tech_data[:5]:
                content += f"- **{item.get('source', '')}**: {item.get('content', '')[:200]}...\n"
        else:
            content += "- 暂无技术趋势数据\n"

        content += """
### 4.2 产品发布动态

"""

        # 收集产品数据
        product_data = [item for item in self.data if item.get('data_type') == 'product' or 'product' in item.get('data_type', '').lower()]

        if product_data:
            for item in product_data[:5]:
                content += f"- **{item.get('brand', '')}** - {item.get('content', '')[:200]}...\n"
        else:
            content += "- 暂无产品发布数据\n"

        return content

    def generate_recall_analysis(self) -> str:
        """生成召回分析"""
        content = """
## 5. 产品召回分析

产品召回对品牌形象和市场信心有重要影响。以下是收集到的召回信息：

"""

        # 收集召回数据
        recall_data = [item for item in self.data if 'recall' in item.get('content', '').lower() or '召回' in item.get('content', '')]

        if recall_data:
            for item in recall_data:
                brand = item.get('brand', 'Unknown')
                content += f"""
### 5.{recall_data.index(item) + 1} {brand}产品召回

- **信息来源**: {item.get('source', '')}
- **召回详情**: {item.get('content', '')}
- **影响范围**: {item.get('metadata', {}).get('impact', '未知')}
"""
        else:
            content += """
✅ **好消息**: 在分析期间内，未发现重大HVAC产品召回事件。

这表明行业整体质量控制水平较高，各品牌对产品质量把控严格。
"""

        return content

    def generate_regional_opportunities(self) -> str:
        """生成区域市场机会分析"""
        geo_scope = self.config.get('geographic_scope', 'national')

        content = f"""
## 6. 区域市场机会分析

### 6.1 {geo_scope}市场概况

"""

        # 根据地理范围生成内容
        if 'east' in geo_scope.lower():
            content += """
东部各州（特别是纽约、马萨诸塞等）一直是能效政策的先行者，这些州通常有更严格的要求和更大的激励力度。
"""
        elif 'south' in geo_scope.lower():
            content += """
南部各州（德州、佛州等）是HVAC产品的重要市场，气候条件使得空调需求旺盛。
"""
        elif 'west' in geo_scope.lower():
            content += """
西部各州（加州、华盛顿等）在环保和能效方面要求严格，是高端产品的重点市场。
"""
        else:
            content += """
全国范围内，各州政策差异较大，需要针对性分析。
"""

        content += """
### 6.2 政策激励带来的机会

- **直接激励**: 直接补贴和税收减免
- **间接激励**: 建筑能效标准提升
- **长期机会**: 可再生能源整合

### 6.3 投资建议

- 重点关注政策友好的州/区域
- 优先投资符合高能效标准的产品线
- 建立本地化的渠道和售后网络
"""

        return content

    def generate_conclusions(self) -> str:
        """生成结论与建议"""
        content = """
## 7. 结论与建议

### 7.1 核心结论

1. **市场竞争激烈**: 各大品牌在技术创新和市场扩张方面投入巨大
2. **政策驱动明显**: DOE等机构的政策对行业发展方向产生重要影响
3. **BOSCH表现突出**: 在技术创新和市场扩张方面具有明显优势
4. **区域机会差异**: 不同州/区域的政策环境差异较大

### 7.2 战略建议

#### 对于BOSCH:
- 继续加大在{geo_scope}的投入
- 强化技术领先优势，特别是智能化方向
- 深化渠道合作，扩大市场覆盖面

#### 对于市场参与者:
- 密切关注DOE能效标准变化
- 提前布局政策友好的州/区域
- 重视产品召回风险管理

### 7.3 风险提示

- 政策变化风险
- 市场竞争加剧风险
- 技术替代风险
- 供应链中断风险
""".format(geo_scope=self.config.get('geographic_scope', '重点区域'))

        return content

    def generate_appendix(self) -> str:
        """生成附录 - 数据源"""
        content = """
## 附录：数据源与信息来源

### 数据收集概况

- **数据点总数**: {total_points}
- **数据源数量**: {source_count}
- **时间跨度**: {time_range}
- **收集方法**: Firecrawl + 网络搜索

### 主要数据源

#### 政府和行业机构
""".format(
            total_points=len(self.data),
            source_count=len(set(item.get('source', '') for item in self.data)),
            time_range=f"{self.config.get('time_range', {}).get('start', '')} 至 {self.config.get('time_range', {}).get('end', '')}"
        )

        # 按来源分组显示数据源
        sources = {}
        for item in self.data:
            source = item.get('source', 'Unknown')
            if source not in sources:
                sources[source] = []
            sources[source].append({
                'url': item.get('url', ''),
                'type': item.get('data_type', ''),
                'timestamp': item.get('timestamp', '')
            })

        for source, items in list(sources.items())[:10]:  # 只显示前10个
            content += f"- **{source}**: {len(items)} 个数据点\n"

        content += """
### 敏感信息声明

本报告中标记为"restricted"或"confidential"的信息来源于行业内部知情人士，
仅供内部参考，不对外传播。

### 数据时效性

- 数据截至: {current_date}
- 建议定期更新以保持分析的时效性

### 免责声明

本报告基于公开信息和行业分析，仅供参考。
投资决策请结合多方面信息，谨慎评估风险。
""".format(current_date=datetime.now().strftime('%Y-%m-%d'))

        return content

    def generate_markdown_report(self, output_path: str = "hvac_market_analysis.md") -> str:
        """生成Markdown格式报告"""
        logger.info("生成Markdown格式报告...")

        # 构建报告内容
        report_content = self.template['markdown_template'].format(
            time_range=f"{self.config.get('time_range', {}).get('start', '')} 至 {self.config.get('time_range', {}).get('end', '')}",
            brands=', '.join(self.config.get('target_brands', [])),
            key_findings='详见各章节分析',
            BOSCH_CONTENT=self.format_bosch_deep_analysis() if self.bosch_analysis else '未启用BOSCH深度分析',
            APPENDIX_CONTENT=self.generate_appendix()
        )

        # 替换各章节内容
        sections = {
            '执行摘要': self.generate_executive_summary(),
            '品牌深度分析': self.generate_brand_analysis(),
            '政策法规影响': self.generate_policy_analysis(),
            '市场趋势': self.generate_market_trends(),
            '产品召回': self.generate_recall_analysis(),
            '区域市场': self.generate_regional_opportunities(),
            '结论与建议': self.generate_conclusions(),
            '附录': self.generate_appendix()
        }

        # 动态替换章节
        for section_title, section_content in sections.items():
            placeholder = f"## {section_title}"
            if placeholder in report_content:
                report_content = report_content.replace(placeholder, f"{placeholder}\n{section_content}")

        # 保存Markdown文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        logger.info(f"Markdown报告已保存到: {output_path}")
        return output_path

    def generate_html_report(self, markdown_path: str = "hvac_market_analysis.md",
                           output_path: str = "hvac_market_analysis.html") -> str:
        """生成HTML格式报告"""
        logger.info("生成HTML格式报告...")

        # 读取Markdown内容
        try:
            with open(markdown_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
        except FileNotFoundError:
            logger.error(f"Markdown文件未找到: {markdown_path}")
            return ""

        # 简单的Markdown到HTML转换（实际使用中可以调用markdown库）
        html_content = self.convert_markdown_to_html(markdown_content)

        # 添加HTML头部和样式
        full_html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HVAC市场分析报告</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #2980b9;
            margin-top: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .highlight {{
            background-color: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 20px 0;
        }}
        .toc {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .toc ul {{
            list-style-type: none;
        }}
        .toc a {{
            text-decoration: none;
            color: #2980b9;
        }}
        .toc a:hover {{
            text-decoration: underline;
        }}
        .metadata {{
            font-size: 0.9em;
            color: #7f8c8d;
            margin: 20px 0;
        }}
        @media print {{
            body {{
                background-color: white;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>
"""

        # 保存HTML文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_html)

        logger.info(f"HTML报告已保存到: {output_path}")
        return output_path

    def convert_markdown_to_html(self, markdown: str) -> str:
        """简单的Markdown到HTML转换"""
        import re

        # 转换标题
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', markdown, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

        # 转换粗体
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)

        # 转换列表
        html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)

        # 转换段落
        html = re.sub(r'\n\n', '</p><p>', html)
        html = '<p>' + html + '</p>'

        # 清理空标签
        html = re.sub(r'<p>\s*</p>', '', html)
        html = re.sub(r'<p>\s*<h', r'<h', html)
        html = re.sub(r'</h>\s*</p>', r'</h>', html)

        return html

    def generate_complete_report(self) -> Dict[str, str]:
        """生成完整报告（Markdown + HTML）"""
        logger.info("开始生成完整报告...")

        # 生成Markdown报告
        md_path = self.generate_markdown_report()

        # 生成HTML报告
        html_path = self.generate_html_report(md_path)

        return {
            'markdown': md_path,
            'html': html_path,
            'summary': {
                'total_data_points': len(self.data),
                'bosch_analysis_enabled': self.bosch_analysis is not None,
                'report_formats': ['markdown', 'html'],
                'output_directory': os.getcwd()
            }
        }

def main():
    """主函数 - 报告生成测试"""
    print("HVAC报告生成器")
    print("=" * 60)

    generator = HVACReportGenerator()

    if not generator.config:
        print("❌ 未找到分析配置文件")
        return

    # 生成完整报告
    result = generator.generate_complete_report()

    print(f"\n📊 报告生成摘要:")
    print(f"   数据点总数: {result['summary']['total_data_points']}")
    print(f"   BOSCH深度分析: {'启用' if result['summary']['bosch_analysis_enabled'] else '未启用'}")
    print(f"   报告格式: {', '.join(result['summary']['report_formats'])}")

    print(f"\n📁 输出文件:")
    print(f"   Markdown: {result['markdown']}")
    print(f"   HTML: {result['html']}")

    print(f"\n✅ 报告生成完成")

if __name__ == "__main__":
    main()

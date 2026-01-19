#!/usr/bin/env python3
"""
HVAC首席商业分析师技能 - 打包脚本
验证技能结构并创建可分发的zip包
"""

import os
import zipfile
import yaml
import json
from datetime import datetime
import shutil

def validate_skill_structure(skill_dir):
    """验证技能目录结构"""
    print("=" * 60)
    print("验证HVAC首席商业分析师技能结构")
    print("=" * 60)

    required_files = [
        'SKILL.md',
        'scripts/framework_collector.py',
        'scripts/data_source_manager.py',
        'scripts/data_collector.py',
        'scripts/bosch_deep_analyzer.py',
        'scripts/report_generator.py',
        'references/hvac_analysis_framework.md',
        'references/data_source_config.yaml',
        'references/report_template.md',
        'references/bosch_methodology.md',
        'assets/styles/report_style.css',
        'assets/charts/market_share_chart.svg',
        'assets/charts/growth_trend_chart.svg',
        'assets/charts/technology_radar_chart.svg'
    ]

    optional_files = [
        'assets/charts/README.md',
        'assets/styles/README.md',
        'scripts/README.md'
    ]

    validation_passed = True

    # 检查必需文件
    print("\n📋 检查必需文件:")
    for file_path in required_files:
        full_path = os.path.join(skill_dir, file_path)
        if os.path.exists(full_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ 缺失: {file_path}")
            validation_passed = False

    # 检查可选文件
    print("\n📋 检查可选文件:")
    for file_path in optional_files:
        full_path = os.path.join(skill_dir, file_path)
        if os.path.exists(full_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ⚠️  未找到: {file_path} (可选)")

    # 验证SKILL.md
    print("\n📋 验证SKILL.md:")
    skill_md_path = os.path.join(skill_dir, 'SKILL.md')
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '---' in content:
                # 检查YAML frontmatter
                parts = content.split('---')
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    frontmatter = yaml.safe_load(yaml_content)
                    if 'name' in frontmatter and 'description' in frontmatter:
                        print(f"  ✅ 名称: {frontmatter['name']}")
                        print(f"  ✅ 描述: {frontmatter['description'][:60]}...")
                    else:
                        print("  ❌ YAML frontmatter缺少必需字段")
                        validation_passed = False
                else:
                    print("  ❌ 缺少YAML frontmatter分隔符")
                    validation_passed = False
            else:
                print("  ❌ 缺少YAML frontmatter")
                validation_passed = False
    except Exception as e:
        print(f"  ❌ 读取SKILL.md失败: {e}")
        validation_passed = False

    # 验证数据源配置
    print("\n📋 验证数据源配置:")
    config_path = os.path.join(skill_dir, 'references/data_source_config.yaml')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            if 'data_sources' in config:
                print(f"  ✅ 数据源数量: {len(config['data_sources'])}")
                brand_sources = [s for s in config['data_sources'] if s.get('category') == 'brand']
                print(f"  ✅ 品牌数据源: {len(brand_sources)}")
                bosch_sources = [s for s in config['data_sources'] if s.get('special_analysis')]
                print(f"  ✅ BOSCH专用数据源: {len(bosch_sources)}")
            else:
                print("  ❌ 配置文件中缺少data_sources字段")
                validation_passed = False
    except Exception as e:
        print(f"  ❌ 读取数据源配置失败: {e}")
        validation_passed = False

    # 统计文件数量
    print("\n📊 文件统计:")
    file_count = 0
    for root, dirs, files in os.walk(skill_dir):
        file_count += len(files)

    python_files = sum(1 for root, dirs, files in os.walk(skill_dir) for f in files if f.endswith('.py'))
    md_files = sum(1 for root, dirs, files in os.walk(skill_dir) for f in files if f.endswith('.md'))
    svg_files = sum(1 for root, dirs, files in os.walk(skill_dir) for f in files if f.endswith('.svg'))

    print(f"  📁 总文件数: {file_count}")
    print(f"  🐍 Python脚本: {python_files}")
    print(f"  📄 Markdown文档: {md_files}")
    print(f"  🎨 SVG图表: {svg_files}")

    print("\n" + "=" * 60)
    if validation_passed:
        print("✅ 验证通过！技能结构完整")
    else:
        print("❌ 验证失败！请检查缺失的文件")
    print("=" * 60)

    return validation_passed

def create_package(skill_dir, output_dir=None):
    """创建技能包"""
    if output_dir is None:
        output_dir = os.getcwd()

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 生成包名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"hvac-business-analyst-skill-{timestamp}.zip"
    package_path = os.path.join(output_dir, package_name)

    print(f"\n📦 创建技能包: {package_name}")

    # 创建zip文件
    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, skill_dir)
                zipf.write(file_path, arcname)
                print(f"  ➕ 添加: {arcname}")

    # 获取文件大小
    size_mb = os.path.getsize(package_path) / (1024 * 1024)

    print(f"\n✅ 技能包创建成功!")
    print(f"📁 路径: {package_path}")
    print(f"💾 大小: {size_mb:.2f} MB")

    return package_path

def create_readme(skill_dir):
    """创建README文件"""
    readme_content = """# HVAC首席商业分析师技能

## 概述

这是一个专门用于生成北美HVAC空调领域专业竞品分析或行业调研报告的技能。技能覆盖Carrier、Trane、BOSCH、Lennox、Goodman/Daikin等主流厂家的产品动态、技术趋势、政策法规和销售数据。

## 核心特性

- ✅ **5大品牌深度分析** - 覆盖主要HVAC品牌
- ✅ **BOSCH特别深度分析** - 8个维度全面剖析
- ✅ **多源数据收集** - 集成Firecrawl和网络搜索
- ✅ **政策法规追踪** - DOE、AHRI等权威机构
- ✅ **区域政策分析** - 州级激励政策
- ✅ **双格式输出** - Markdown + HTML
- ✅ **专业可视化** - SVG图表
- ✅ **可配置数据源** - 动态增减数据源

## 文件结构

```
hvac-business-analyst/
├── SKILL.md                          # 技能说明文档
├── scripts/                           # 核心脚本
│   ├── framework_collector.py         # 框架收集器
│   ├── data_source_manager.py         # 数据源管理器
│   ├── data_collector.py              # 数据收集引擎
│   ├── bosch_deep_analyzer.py        # BOSCH深度分析
│   └── report_generator.py            # 报告生成器
├── references/                        # 参考资料
│   ├── hvac_analysis_framework.md    # 分析框架
│   ├── bosch_methodology.md          # BOSCH方法论
│   ├── data_source_config.yaml       # 数据源配置
│   └── report_template.md            # 报告模板
└── assets/                           # 资源文件
    ├── styles/                       # 样式表
    └── charts/                       # SVG图表
```

## 使用方法

### 1. 框架收集
```bash
python scripts/framework_collector.py
```

### 2. 数据源管理
```bash
python scripts/data_source_manager.py
```

### 3. 数据收集
```bash
python scripts/data_collector.py
```

### 4. BOSCH深度分析
```bash
python scripts/bosch_deep_analyzer.py
```

### 5. 报告生成
```bash
python scripts/report_generator.py
```

## 配置说明

### 数据源配置
编辑 `references/data_source_config.yaml` 可以：
- 添加/删除数据源
- 调整优先级
- 启用/禁用特定源

### 报告模板
编辑 `references/report_template.md` 可以：
- 自定义报告结构
- 修改样式
- 调整内容格式

## 注意事项

1. **BOSCH深度分析**: 该技能特别注重BOSCH品牌的深度分析，不遗漏任何重要细节
2. **数据完整性**: 收集最近3年历史数据 + 当前实时数据
3. **敏感信息处理**: 自动识别和标记敏感信息
4. **多格式输出**: 同时提供Markdown和HTML格式

## 技术要求

- Python 3.7+
- 网络连接（用于数据收集）
- Firecrawl API（可选）

## 支持的品牌

- Carrier
- Trane
- BOSCH ⭐（特别深度分析）
- Lennox
- Goodman/Daikin

## 数据源

### 政府机构
- DOE (美国能源部)
- AHRI (空调制冷协会)
- EPA (环保署)
- ACCA (承包商协会)

### 品牌官网
- 各品牌官方产品发布
- 技术文档
- 财务报告

### 政策数据
- DSIRE (州级激励政策)
- 各州能源办公室

## 许可证

© 2024 保留所有权利

## 联系方式

如有问题或建议，请通过GitHub Issues联系。

---

**制作**: HVAC首席商业分析师技能
**技术支持**: Claude Code
"""

    readme_path = os.path.join(skill_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"✅ README.md 已创建")

def main():
    """主函数"""
    skill_dir = os.path.abspath(os.path.dirname(__file__))

    # 验证技能结构
    if not validate_skill_structure(skill_dir):
        print("\n❌ 验证失败，无法创建技能包")
        return

    # 创建README
    create_readme(skill_dir)

    # 创建技能包
    package_path = create_package(skill_dir)

    print("\n" + "=" * 60)
    print("🎉 HVAC首席商业分析师技能打包完成!")
    print("=" * 60)
    print(f"\n📦 技能包: {package_path}")
    print(f"\n📖 使用说明:")
    print(f"   1. 解压技能包到Claude Skills目录")
    print(f"   2. 阅读README.md了解详细使用方法")
    print(f"   3. 根据需要修改配置文件")
    print(f"   4. 运行脚本进行分析")

if __name__ == "__main__":
    main()

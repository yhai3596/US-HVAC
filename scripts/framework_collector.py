#!/usr/bin/env python3
"""
HVAC首席商业分析师 - 框架收集器
交互式收集用户分析需求，生成分析配置
"""

import json
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class HVACFrameworkCollector:
    def __init__(self):
        self.config = {
            "analysis_goal": None,
            "target_brands": [],
            "bosch_priority": False,
            "time_range": {
                "start": None,
                "end": datetime.now().strftime("%Y-%m-%d")
            },
            "geographic_scope": "national",
            "analysis_depth": "standard",
            "data_sources": [],
            "output_formats": ["markdown", "html"],
            "created_at": datetime.now().isoformat()
        }

    def collect_analysis_goal(self) -> str:
        """收集分析目标"""
        print("=" * 60)
        print("HVAC首席商业分析师 - 分析框架确认")
        print("=" * 60)

        goals = {
            "1": "竞品对比分析 - 比较不同品牌的产品、市场表现和策略",
            "2": "市场趋势分析 - 分析行业发展趋势和技术动态",
            "3": "政策法规影响 - 评估DOE/AHRI等政策对市场的影响",
            "4": "区域市场机会 - 分析州级刺激政策对销售的影响",
            "5": "产品召回影响 - 追踪召回事件对品牌和市场的影响",
            "6": "综合市场研究 - 包含多个维度的全面分析"
        }

        print("\n请选择分析目标（输入数字1-6）：")
        for key, value in goals.items():
            print(f"{key}. {value}")

        while True:
            choice = input("\n请输入选择: ").strip()
            if choice in goals:
                self.config["analysis_goal"] = goals[choice]
                return goals[choice]
            print("无效选择，请重新输入1-6")

    def collect_target_brands(self) -> List[str]:
        """收集目标品牌"""
        print("\n" + "=" * 60)
        print("品牌选择")
        print("=" * 60)

        all_brands = {
            "1": "Carrier",
            "2": "Trane",
            "3": "BOSCH",
            "4": "Lennox",
            "5": "Goodman/Daikin"
        }

        print("\n可选择的品牌（输入数字编号，多选用逗号分隔，如1,2,3）：")
        for key, value in all_brands.items():
            print(f"{key}. {value}")

        print("\n注意：BOSCH会自动进行深度分析，无需额外标记")

        while True:
            choices = input("\n请选择品牌: ").strip()
            try:
                selected = []
                for choice in choices.split(","):
                    choice = choice.strip()
                    if choice in all_brands:
                        selected.append(all_brands[choice])

                if not selected:
                    print("请至少选择一个品牌")
                    continue

                self.config["target_brands"] = selected
                if "BOSCH" in selected:
                    self.config["bosch_priority"] = True
                return selected
            except Exception:
                print("输入格式错误，请使用逗号分隔，如1,2,3")

    def collect_time_range(self) -> Dict[str, str]:
        """收集时间范围"""
        print("\n" + "=" * 60)
        print("时间范围选择")
        print("=" * 60)

        options = {
            "1": "最近一年",
            "2": "最近两年",
            "3": "最近三年",
            "4": "自定义时间范围"
        }

        print("\n请选择时间范围：")
        for key, value in options.items():
            print(f"{key}. {value}")

        while True:
            choice = input("\n请输入选择: ").strip()
            if choice == "1":
                start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            elif choice == "2":
                start_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
            elif choice == "3":
                start_date = (datetime.now() - timedelta(days=1095)).strftime("%Y-%m-%d")
            elif choice == "4":
                print("\n请输入自定义开始时间 (YYYY-MM-DD):")
                start_date = input("开始时间: ").strip()
                try:
                    datetime.strptime(start_date, "%Y-%m-%d")
                except ValueError:
                    print("日期格式错误，请使用YYYY-MM-DD格式")
                    continue
            else:
                print("无效选择，请重新输入")
                continue

            self.config["time_range"]["start"] = start_date
            return self.config["time_range"]

    def collect_geographic_scope(self) -> str:
        """收集地理范围"""
        print("\n" + "=" * 60)
        print("地理范围选择")
        print("=" * 60)

        options = {
            "1": "全国范围",
            "2": "东部各州",
            "3": "南部各州",
            "4": "西部各州",
            "5": "自定义州/区域"
        }

        print("\n请选择地理范围：")
        for key, value in options.items():
            print(f"{key}. {value}")

        while True:
            choice = input("\n请输入选择: ").strip()
            if choice in options:
                scope = options[choice]
                if choice == "5":
                    print("\n请输入具体州/区域（用逗号分隔）:")
                    custom_scope = input("州/区域: ").strip()
                    scope += f" ({custom_scope})"
                self.config["geographic_scope"] = scope
                return scope
            print("无效选择，请重新输入")

    def collect_data_sources(self) -> List[str]:
        """收集数据源偏好"""
        print("\n" + "=" * 60)
        print("数据源配置")
        print("=" * 60)

        sources = {
            "1": "DOE (美国能源部)",
            "2": "AHRI (空调制冷协会)",
            "3": "EPC (环保署)",
            "4": "ACCA (承包商协会)",
            "5": "CEE (能效联盟)",
            "6": "品牌官网和产品发布",
            "7": "行业新闻和媒体报道",
            "8": "州级激励政策网站"
        }

        print("\n可选数据源（全部默认启用，输入数字可选择排除，如2,4,5）：")
        for key, value in sources.items():
            print(f"{key}. {value}")

        print("\n直接回车表示使用全部数据源，或输入要排除的数据源编号：")
        exclusion = input("排除的数据源编号（可选）: ").strip()

        if not exclusion:
            selected_sources = list(sources.values())
        else:
            exclude_list = [s.strip() for s in exclusion.split(",")]
            selected_sources = [v for k, v in sources.items() if k not in exclude_list]

        self.config["data_sources"] = selected_sources
        return selected_sources

    def save_config(self, filepath: str = "analysis_config.json"):
        """保存配置到文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        print(f"\n✅ 配置已保存到: {filepath}")

    def generate_summary(self):
        """生成配置摘要"""
        print("\n" + "=" * 60)
        print("分析配置摘要")
        print("=" * 60)

        print(f"\n📊 分析目标: {self.config['analysis_goal']}")
        print(f"🏢 目标品牌: {', '.join(self.config['target_brands'])}")

        if self.config['bosch_priority']:
            print("⭐ BOSCH深度分析: 已启用")

        print(f"📅 时间范围: {self.config['time_range']['start']} 至 {self.config['time_range']['end']}")
        print(f"🌍 地理范围: {self.config['geographic_scope']}")
        print(f"📚 数据源数量: {len(self.config['data_sources'])} 个")

        print("\n" + "=" * 60)

    def run_collection(self):
        """运行完整收集流程"""
        self.collect_analysis_goal()
        self.collect_target_brands()
        self.collect_time_range()
        self.collect_geographic_scope()
        self.collect_data_sources()

        self.generate_summary()

        confirm = input("\n配置是否正确？输入 'yes' 确认，其他键重新开始: ").strip().lower()
        if confirm != 'yes':
            print("\n重新开始配置...")
            return self.run_collection()

        return self.config

def main():
    """主函数"""
    collector = HVACFrameworkCollector()
    config = collector.run_collection()

    # 保存配置
    collector.save_config("analysis_config.json")

    print("\n🎉 配置收集完成！可以开始数据收集和分析。")
    return config

if __name__ == "__main__":
    main()

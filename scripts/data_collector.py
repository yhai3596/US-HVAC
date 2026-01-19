#!/usr/bin/env python3
"""
HVAC首席商业分析师 - 数据收集引擎
支持Firecrawl和网络搜索双模式数据收集
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging
import re

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DataPoint:
    """数据点类"""
    source: str
    url: str
    content: str
    data_type: str  # product, news, policy, recall, technical
    timestamp: str
    brand: Optional[str] = None
    sensitivity: str = "public"  # public, restricted, confidential
    confidence: float = 1.0
    metadata: Optional[Dict] = None

class HVACDataCollector:
    def __init__(self, config_path: str = "analysis_config.json"):
        self.config = self.load_analysis_config(config_path)
        self.data_source_manager = None
        self.collected_data: List[DataPoint] = []

    def load_analysis_config(self, config_path: str) -> Dict:
        """加载分析配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                logger.info(f"已加载分析配置: {config_path}")
                return config
        except FileNotFoundError:
            logger.error(f"配置文件不存在: {config_path}")
            return {}

    def init_data_source_manager(self):
        """初始化数据源管理器"""
        try:
            from data_source_manager import DataSourceManager
            self.data_source_manager = DataSourceManager()
            logger.info("数据源管理器初始化成功")
        except ImportError:
            logger.error("无法导入数据源管理器")

    async def collect_from_firecrawl(self, urls: List[str],
                                   keywords: List[str] = None) -> List[DataPoint]:
        """使用Firecrawl方式收集数据"""
        logger.info(f"使用Firecrawl模式收集 {len(urls)} 个URL的数据")

        # 这里模拟Firecrawl的实际调用
        # 在实际使用中，会调用真实的Firecrawl API
        data_points = []

        for url in urls:
            try:
                # 模拟数据收集过程
                mock_data = {
                    'source': url,
                    'content': f"从 {url} 收集的内容...",
                    'timestamp': datetime.now().isoformat()
                }

                # 检查是否包含关键词
                if keywords and any(keyword.lower() in url.lower() for keyword in keywords):
                    data_points.append(DataPoint(
                        source=url,
                        url=url,
                        content=mock_data['content'],
                        data_type='news',
                        timestamp=mock_data['timestamp'],
                        brand=self.extract_brand_from_url(url),
                        metadata={'collection_method': 'firecrawl'}
                    ))

            except Exception as e:
                logger.error(f"收集 {url} 时出错: {str(e)}")

        return data_points

    async def collect_from_web_search(self, queries: List[str]) -> List[DataPoint]:
        """使用网络搜索方式收集数据"""
        logger.info(f"使用网络搜索模式收集 {len(queries)} 个查询的数据")

        data_points = []

        for query in queries:
            try:
                # 模拟搜索过程
                # 在实际使用中，会调用真实的搜索引擎API
                mock_results = [
                    {
                        'title': f"搜索结果 for {query}",
                        'url': f"https://example.com/result1",
                        'snippet': f"关于 {query} 的信息..."
                    }
                ]

                for result in mock_results:
                    data_points.append(DataPoint(
                        source="web_search",
                        url=result['url'],
                        content=f"{result['title']}: {result['snippet']}",
                        data_type='news',
                        timestamp=datetime.now().isoformat(),
                        brand=self.extract_brand_from_query(query),
                        metadata={
                            'collection_method': 'web_search',
                            'query': query,
                            'title': result['title']
                        }
                    ))

            except Exception as e:
                logger.error(f"搜索 {query} 时出错: {str(e)}")

        return data_points

    def extract_brand_from_url(self, url: str) -> Optional[str]:
        """从URL提取品牌信息"""
        brand_patterns = {
            'carrier': 'Carrier',
            'trane': 'Trane',
            'bosch': 'BOSCH',
            'lennox': 'Lennox',
            'goodman': 'Goodman',
            'daikin': 'Daikin'
        }

        url_lower = url.lower()
        for pattern, brand in brand_patterns.items():
            if pattern in url_lower:
                return brand
        return None

    def extract_brand_from_query(self, query: str) -> Optional[str]:
        """从查询提取品牌信息"""
        brand_keywords = {
            'Carrier': ['carrier', 'carrier hvac', 'carrier heating'],
            'Trane': ['trane', 'trane hvac', 'trane heating'],
            'BOSCH': ['bosch', 'bosch hvac', 'bosch heating'],
            'Lennox': ['lennox', 'lennox hvac', 'lennox heating'],
            'Goodman': ['goodman', 'goodman hvac', 'goodman heating'],
            'Daikin': ['daikin', 'daikin hvac', 'daikin heating']
        }

        query_lower = query.lower()
        for brand, keywords in brand_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return brand
        return None

    async def collect_brand_data(self, brand: str) -> List[DataPoint]:
        """收集特定品牌的数据"""
        logger.info(f"开始收集品牌数据: {brand}")

        if not self.data_source_manager:
            self.init_data_source_manager()

        brand_sources = self.data_source_manager.get_brand_sources(brand)
        urls = [source['url'] for source in brand_sources]

        # 构建搜索查询
        queries = [
            f"{brand} HVAC 新品发布 2024",
            f"{brand} 产品召回 2024",
            f"{brand} 技术创新 HVAC",
            f"{brand} 市场策略 北美"
        ]

        # 并行收集数据
        firecrawl_task = self.collect_from_firecrawl(urls)
        search_task = self.collect_from_web_search(queries)

        firecrawl_data, search_data = await asyncio.gather(firecrawl_task, search_task)

        all_data = firecrawl_data + search_data

        # 标记BOSCH特殊分析
        if brand == "BOSCH":
            for data_point in all_data:
                data_point.metadata = data_point.metadata or {}
                data_point.metadata['bosch_priority'] = True
                data_point.metadata['deep_analysis'] = True

        return all_data

    async def collect_policy_data(self) -> List[DataPoint]:
        """收集政策法规数据"""
        logger.info("开始收集政策法规数据")

        policy_queries = [
            "DOE HVAC 能效标准 2024",
            "AHRI HVAC 认证 标准",
            "州级 空调 激励政策 退税",
            "EPA 环保政策 HVAC",
            "建筑能效标准 HVAC"
        ]

        return await self.collect_from_web_search(policy_queries)

    async def collect_recall_data(self) -> List[DataPoint]:
        """收集产品召回数据"""
        logger.info("开始收集产品召回数据")

        recall_queries = [
            "HVAC 产品召回 2024",
            "空调 召回 安全 通告",
            "Carrier 召回 2024",
            "Trane 召回 2024",
            "BOSCH 召回 2024",
            "Lennox 召回 2024",
            "Goodman 召回 2024",
            "Daikin 召回 2024"
        ]

        return await self.collect_from_web_search(recall_queries)

    async def collect_regional_data(self, region: str) -> List[DataPoint]:
        """收集区域市场数据"""
        logger.info(f"开始收集区域数据: {region}")

        region_queries = [
            f"{region} 空调 激励政策",
            f"{region} HVAC 市场 销售数据",
            f"{region} 建筑能效 标准"
        ]

        return await self.collect_from_web_search(region_queries)

    async def run_collection(self) -> List[DataPoint]:
        """运行完整的数据收集流程"""
        logger.info("开始HVAC市场数据收集流程")

        all_data = []

        # 收集品牌数据
        for brand in self.config.get('target_brands', []):
            brand_data = await self.collect_brand_data(brand)
            all_data.extend(brand_data)

        # 收集政策法规数据
        policy_data = await self.collect_policy_data()
        all_data.extend(policy_data)

        # 收集召回数据
        recall_data = await self.collect_recall_data()
        all_data.extend(recall_data)

        # 收集区域数据
        geo_scope = self.config.get('geographic_scope', 'national')
        if geo_scope != 'national':
            regional_data = await self.collect_regional_data(geo_scope)
            all_data.extend(regional_data)

        # 数据去重和验证
        all_data = self.deduplicate_data(all_data)
        all_data = self.validate_data(all_data)

        self.collected_data = all_data
        logger.info(f"数据收集完成，共收集 {len(all_data)} 个数据点")

        return all_data

    def deduplicate_data(self, data: List[DataPoint]) -> List[DataPoint]:
        """数据去重"""
        seen = set()
        unique_data = []

        for item in data:
            # 使用URL和内容前100字符作为去重键
            key = (item.url, item.content[:100])
            if key not in seen:
                seen.add(key)
                unique_data.append(item)

        logger.info(f"去重完成，原始数据 {len(data)} -> 去重后 {len(unique_data)}")
        return unique_data

    def validate_data(self, data: List[DataPoint]) -> List[DataPoint]:
        """数据验证"""
        valid_data = []

        for item in data:
            # 基本验证
            if not item.url or not item.content:
                logger.warning(f"跳过无效数据: 缺少URL或内容")
                continue

            # 敏感信息检测
            sensitive_keywords = ['unreleased', 'confidential', 'internal', '未发布', '机密']
            if any(keyword in item.content.lower() for keyword in sensitive_keywords):
                item.sensitivity = 'restricted'
                logger.info(f"检测到敏感信息: {item.source}")

            valid_data.append(item)

        logger.info(f"数据验证完成，有效数据 {len(valid_data)}")
        return valid_data

    def save_collected_data(self, filepath: str = "collected_data.json"):
        """保存收集的数据"""
        data_dict = [asdict(item) for item in self.collected_data]

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)

        logger.info(f"数据已保存到: {filepath}")

    def get_data_summary(self) -> Dict:
        """获取数据收集摘要"""
        if not self.collected_data:
            return {}

        summary = {
            'total_data_points': len(self.collected_data),
            'by_brand': {},
            'by_data_type': {},
            'by_sensitivity': {},
            'bosch_data_points': 0,
            'time_range': {
                'earliest': None,
                'latest': None
            }
        }

        for item in self.collected_data:
            # 按品牌统计
            if item.brand:
                summary['by_brand'][item.brand] = summary['by_brand'].get(item.brand, 0) + 1

            # 按数据类型统计
            summary['by_data_type'][item.data_type] = summary['by_data_type'].get(item.data_type, 0) + 1

            # 按敏感度统计
            summary['by_sensitivity'][item.sensitivity] = summary['by_sensitivity'].get(item.sensitivity, 0) + 1

            # BOSCH数据点统计
            if item.brand == 'BOSCH' or (item.metadata and item.metadata.get('bosch_priority')):
                summary['bosch_data_points'] += 1

            # 时间范围
            if not summary['time_range']['earliest'] or item.timestamp < summary['time_range']['earliest']:
                summary['time_range']['earliest'] = item.timestamp
            if not summary['time_range']['latest'] or item.timestamp > summary['time_range']['latest']:
                summary['time_range']['latest'] = item.timestamp

        return summary

async def main():
    """主函数 - 数据收集测试"""
    print("HVAC数据收集引擎")
    print("=" * 60)

    collector = HVACDataCollector()

    if not collector.config:
        print("❌ 未找到分析配置文件")
        return

    # 运行数据收集
    data = await collector.run_collection()

    # 显示摘要
    summary = collector.get_data_summary()
    print(f"\n📊 数据收集摘要:")
    print(f"   总数据点: {summary['total_data_points']}")
    print(f"   按品牌: {summary['by_brand']}")
    print(f"   按类型: {summary['by_data_type']}")
    print(f"   BOSCH数据点: {summary['bosch_data_points']}")

    # 保存数据
    collector.save_collected_data()

    print(f"\n✅ 数据收集完成，已保存到 collected_data.json")

if __name__ == "__main__":
    asyncio.run(main())

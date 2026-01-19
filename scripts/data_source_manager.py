#!/usr/bin/env python3
"""
HVAC首席商业分析师 - 数据源管理器
管理数据源配置、验证和动态增减
"""

import yaml
import json
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataSourceManager:
    def __init__(self, config_path: str = "references/data_source_config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()
        self.brand_urls = self._init_brand_urls()

    def load_config(self) -> Dict:
        """加载数据源配置"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                logger.info(f"已加载数据源配置: {self.config_path}")
                return config
        except FileNotFoundError:
            logger.warning(f"配置文件不存在，创建默认配置: {self.config_path}")
            return self.create_default_config()

    def create_default_config(self) -> Dict:
        """创建默认数据源配置"""
        default_config = {
            'data_sources': [
                {
                    'name': 'DOE',
                    'url': 'https://www.energy.gov/',
                    'priority': 1,
                    'enabled': True,
                    'description': '美国能源部 - 能效标准和政策',
                    'category': 'government',
                    'update_frequency': 'weekly',
                    'last_checked': datetime.now().isoformat()
                },
                {
                    'name': 'AHRI',
                    'url': 'https://www.ahrinet.org/',
                    'priority': 1,
                    'enabled': True,
                    'description': '空调制冷协会 - 行业数据和认证',
                    'category': 'industry',
                    'update_frequency': 'monthly',
                    'last_checked': datetime.now().isoformat()
                },
                {
                    'name': 'EPC',
                    'url': 'https://www.epa.gov/',
                    'priority': 2,
                    'enabled': True,
                    'description': '环保署 - 环保政策和标准',
                    'category': 'government',
                    'update_frequency': 'monthly',
                    'last_checked': datetime.now().isoformat()
                },
                {
                    'name': 'ACCA',
                    'url': 'https://www.acca.org/',
                    'priority': 2,
                    'enabled': True,
                    'description': '空调承包商协会 - 行业标准和培训',
                    'category': 'industry',
                    'update_frequency': 'monthly',
                    'last_checked': datetime.now().isoformat()
                },
                {
                    'name': 'CEE',
                    'url': 'https://www.energyefficiencyalliance.org/',
                    'priority': 2,
                    'enabled': True,
                    'description': '能效联盟 - 能效标准和认证',
                    'category': 'industry',
                    'update_frequency': 'monthly',
                    'last_checked': datetime.now().isoformat()
                },
                {
                    'name': 'Carrier',
                    'url': 'https://www.carrier.com/',
                    'priority': 1,
                    'enabled': True,
                    'description': 'Carrier官网 - 产品发布和技术文档',
                    'category': 'brand',
                    'brand': 'Carrier',
                    'update_frequency': 'weekly',
                    'last_checked': datetime.now().isoformat()
                },
                {
                    'name': 'Trane',
                    'url': 'https://www.trane.com/',
                    'priority': 1,
                    'enabled': True,
                    'description': 'Trane官网 - 产品发布和技术文档',
                    'category': 'brand',
                    'brand': 'Trane',
                    'update_frequency': 'weekly',
                    'last_checked': datetime.now().isoformat()
                },
                {
                    'name': 'BOSCH',
                    'url': 'https://www.bosch.com/',
                    'priority': 1,
                    'enabled': True,
                    'description': 'BOSCH官网 - 产品发布和技术文档',
                    'category': 'brand',
                    'brand': 'BOSCH',
                    'update_frequency': 'weekly',
                    'last_checked': datetime.now().isoformat(),
                    'special_analysis': True
                },
                {
                    'name': 'Lennox',
                    'url': 'https://www.lennox.com/',
                    'priority': 1,
                    'enabled': True,
                    'description': 'Lennox官网 - 产品发布和技术文档',
                    'category': 'brand',
                    'brand': 'Lennox',
                    'update_frequency': 'weekly',
                    'last_checked': datetime.now().isoformat()
                },
                {
                    'name': 'Goodman',
                    'url': 'https://www.goodmanmfg.com/',
                    'priority': 1,
                    'enabled': True,
                    'description': 'Goodman官网 - 产品发布和技术文档',
                    'category': 'brand',
                    'brand': 'Goodman',
                    'update_frequency': 'weekly',
                    'last_checked': datetime.now().isoformat()
                },
                {
                    'name': 'Daikin',
                    'url': 'https://www.daikin.com/',
                    'priority': 1,
                    'enabled': True,
                    'description': 'Daikin官网 - 产品发布和技术文档',
                    'category': 'brand',
                    'brand': 'Daikin',
                    'update_frequency': 'weekly',
                    'last_checked': datetime.now().isoformat()
                },
                {
                    'name': 'State_Incentives',
                    'url': 'https://www.dsireusa.org/',
                    'priority': 2,
                    'enabled': True,
                    'description': 'DSIRE - 州级激励政策和退税信息',
                    'category': 'policy',
                    'update_frequency': 'monthly',
                    'last_checked': datetime.now().isoformat()
                },
                {
                    'name': 'HVAC_News',
                    'url': 'https://www.achrnews.com/',
                    'priority': 3,
                    'enabled': True,
                    'description': 'ACHR News - HVAC行业新闻',
                    'category': 'news',
                    'update_frequency': 'daily',
                    'last_checked': datetime.now().isoformat()
                }
            ],
            'regional_sources': {
                'east_coast': [
                    {
                        'name': 'NY_Energy',
                        'url': 'https://www.nyserda.ny.gov/',
                        'description': '纽约州能源研究与发展署'
                    },
                    {
                        'name': 'MA_Energy',
                        'url': 'https://www.mass.gov/orgs/department-of-public-utilities',
                        'description': '马萨诸塞州公用事业部'
                    }
                ],
                'south_coast': [
                    {
                        'name': 'TX_Energy',
                        'url': 'https://www.texasgulf.org/energy/',
                        'description': '德克萨斯州能源'
                    },
                    {
                        'name': 'FL_Energy',
                        'url': 'https://www.floridajobs.org/energy/',
                        'description': '佛罗里达州能源办公室'
                    }
                ]
            }
        }

        # 保存默认配置
        self.save_config(default_config)
        return default_config

    def _init_brand_urls(self) -> Dict[str, List[str]]:
        """初始化品牌相关URL"""
        return {
            'Carrier': [
                'https://www.carrier.com/commercial/',
                'https://www.carrier.com/residential/',
                'https://www.carrier.com/newsroom/',
                'https://www.carrier.com/investors/'
            ],
            'Trane': [
                'https://www.trane.com/commercial/',
                'https://www.trane.com/residential/',
                'https://www.trane.com/news/',
                'https://investor.trane.com/'
            ],
            'BOSCH': [
                'https://www.bosch.com/innovation-day/',
                'https://www.bosch.com/stories/',
                'https://www.bosch.com/media/',
                'https://www.bosch.com/research/',
                'https://www.bosch-presse.de/'
            ],
            'Lennox': [
                'https://www.lennox.com/commercial/',
                'https://www.lennox.com/residential/',
                'https://www.lennox.com/about/newsroom/',
                'https://investor.lennox.com/'
            ],
            'Goodman': [
                'https://www.goodmanmfg.com/',
                'https://www.goodmanmfg.com/about/news/',
                'https://www.goodmanmfg.com/support/'
            ],
            'Daikin': [
                'https://www.daikin.com/about/innovation',
                'https://www.daikin.com/about/news',
                'https://investor.daikin.com/'
            ]
        }

    def save_config(self, config: Optional[Dict] = None):
        """保存配置到文件"""
        if config is None:
            config = self.config

        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, indent=2)
        logger.info(f"配置已保存到: {self.config_path}")

    def add_data_source(self, name: str, url: str, description: str,
                       priority: int = 3, category: str = 'custom',
                       brand: Optional[str] = None):
        """添加新的数据源"""
        new_source = {
            'name': name,
            'url': url,
            'priority': priority,
            'enabled': True,
            'description': description,
            'category': category,
            'brand': brand,
            'update_frequency': 'weekly',
            'last_checked': datetime.now().isoformat()
        }

        # 检查是否已存在
        for source in self.config['data_sources']:
            if source['name'] == name:
                logger.warning(f"数据源 {name} 已存在，跳过添加")
                return False

        self.config['data_sources'].append(new_source)
        self.save_config()
        logger.info(f"已添加新数据源: {name}")
        return True

    def remove_data_source(self, name: str):
        """删除数据源"""
        original_length = len(self.config['data_sources'])
        self.config['data_sources'] = [
            source for source in self.config['data_sources']
            if source['name'] != name
        ]

        if len(self.config['data_sources']) < original_length:
            self.save_config()
            logger.info(f"已删除数据源: {name}")
            return True
        else:
            logger.warning(f"未找到数据源: {name}")
            return False

    def toggle_data_source(self, name: str, enabled: bool):
        """启用/禁用数据源"""
        for source in self.config['data_sources']:
            if source['name'] == name:
                source['enabled'] = enabled
                self.save_config()
                status = "启用" if enabled else "禁用"
                logger.info(f"已{status}数据源: {name}")
                return True

        logger.warning(f"未找到数据源: {name}")
        return False

    def get_enabled_sources(self) -> List[Dict]:
        """获取启用的数据源列表"""
        enabled_sources = [source for source in self.config['data_sources'] if source['enabled']]
        # 按优先级排序
        enabled_sources.sort(key=lambda x: x.get('priority', 3))
        return enabled_sources

    def get_brand_sources(self, brand: str) -> List[Dict]:
        """获取特定品牌的数据源"""
        brand_sources = []
        for source in self.config['data_sources']:
            if source.get('brand') == brand or source['category'] == 'brand':
                brand_sources.append(source)
        return brand_sources

    def get_bosch_sources(self) -> List[Dict]:
        """获取BOSCH专用数据源（优先级最高）"""
        bosch_sources = []
        for source in self.config['data_sources']:
            if source.get('brand') == 'BOSCH' or source.get('special_analysis'):
                bosch_sources.append(source)
        return bosch_sources

    def validate_source(self, url: str) -> Tuple[bool, str]:
        """验证数据源可访问性"""
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                return True, "可访问"
            else:
                return False, f"HTTP {response.status_code}"
        except requests.RequestException as e:
            return False, f"连接错误: {str(e)}"

    def update_last_checked(self, name: str):
        """更新数据源最后检查时间"""
        for source in self.config['data_sources']:
            if source['name'] == name:
                source['last_checked'] = datetime.now().isoformat()
                self.save_config()
                return True
        return False

    def get_config_summary(self) -> Dict:
        """获取配置摘要"""
        total_sources = len(self.config['data_sources'])
        enabled_sources = len(self.get_enabled_sources())
        brand_sources = len([s for s in self.config['data_sources'] if s['category'] == 'brand'])
        bosch_sources = len(self.get_bosch_sources())

        return {
            'total_sources': total_sources,
            'enabled_sources': enabled_sources,
            'brand_sources': brand_sources,
            'bosch_priority_sources': bosch_sources,
            'government_sources': len([s for s in self.config['data_sources'] if s['category'] == 'government']),
            'industry_sources': len([s for s in self.config['data_sources'] if s['category'] == 'industry']),
            'policy_sources': len([s for s in self.config['data_sources'] if s['category'] == 'policy'])
        }

def main():
    """主函数 - 数据源管理测试"""
    manager = DataSourceManager()

    print("HVAC数据源管理器")
    print("=" * 60)

    # 显示配置摘要
    summary = manager.get_config_summary()
    print(f"\n📊 配置摘要:")
    print(f"   总数据源: {summary['total_sources']}")
    print(f"   启用数据源: {summary['enabled_sources']}")
    print(f"   品牌数据源: {summary['brand_sources']}")
    print(f"   BOSCH专用: {summary['bosch_priority_sources']}")

    # 显示BOSCH数据源
    print(f"\n⭐ BOSCH专用数据源:")
    bosch_sources = manager.get_bosch_sources()
    for source in bosch_sources:
        print(f"   - {source['name']}: {source['url']}")

    # 显示启用的数据源
    print(f"\n✅ 启用的数据源:")
    enabled = manager.get_enabled_sources()
    for source in enabled[:5]:  # 只显示前5个
        print(f"   - {source['name']} (优先级: {source['priority']})")

    if len(enabled) > 5:
        print(f"   ... 还有 {len(enabled) - 5} 个数据源")

if __name__ == "__main__":
    main()

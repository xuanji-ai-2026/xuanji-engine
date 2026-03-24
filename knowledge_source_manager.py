#!/usr/bin/env python3
"""
知识获取数据源管理器
版本: v1.0
创建时间: 2026-03-23 09:20
功能: 管理18个免费知识源的配置和账号池
"""

import asyncio
import json
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class SourceType(Enum):
    """数据源类型"""
    NATIONAL_LIBRARY = "national_library"
    LOCAL_LIBRARY = "local_library"
    EDUCATION = "education"
    INDUSTRY_STANDARD = "industry_standard"
    INDUSTRY_MATERIAL = "industry_material"
    ACADEMIC_DATABASE = "academic_database"

class Priority(Enum):
    """优先级"""
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"

@dataclass
class DataSourceConfig:
    """数据源配置"""
    source_id: str
    name: str
    url: str
    source_type: SourceType
    priority: Priority
    data_types: List[str]
    account_required: bool
    cost: str
    difficulty: str
    rate_limit: str
    coverage: str
    base_url: str
    search_url: str
    download_url: str
    registration_url: Optional[str]
    required_fields: List[str]
    captcha_type: str
    ip_check: str
    notes: str
    status: str = "待配置"

@dataclass
class Account:
    """账号"""
    account_id: str
    username: str
    password: str
    phone: Optional[str] = None
    email: Optional[str] = None
    real_name: Optional[str] = None
    id_card: Optional[str] = None
    teacher_card: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    status: str = "正常"
    source_id: str = ""

class AccountPool:
    """账号池"""
    
    def __init__(self):
        self.accounts: Dict[str, List[Account]] = {}
        self.current_index: Dict[str, int] = {}
    
    def add_account(self, source_id: str, account: Account):
        """添加账号"""
        if source_id not in self.accounts:
            self.accounts[source_id] = []
            self.current_index[source_id] = 0
        
        self.accounts[source_id].append(account)
    
    def get_account(self, source_id: str) -> Optional[Account]:
        """获取账号（轮换使用）"""
        if source_id not in self.accounts or not self.accounts[source_id]:
            return None
        
        accounts = self.accounts[source_id]
        current = self.current_index[source_id]
        
        # 轮换
        account = accounts[current]
        current = (current + 1) % len(accounts)
        self.current_index[source_id] = current
        
        account.last_used = datetime.now()
        return account
    
    def get_available_account(self, source_id: str) -> Optional[Account]:
        """获取可用账号"""
        if source_id not in self.accounts or not self.accounts[source_id]:
            return None
        
        # 返回最近使用的账号
        account = self.accounts[source_id][-1]
        account.last_used = datetime.now()
        return account

class IPPool:
    """IP池"""
    
    def __init__(self):
        self.ips: List[str] = []
        self.current_index = 0
        self.blacklist: set = set()
    
    def add_ip(self, ip: str):
        """添加IP"""
        if ip not in self.ips:
            self.ips.append(ip)
    
    def get_ip(self) -> Optional[str]:
        """获取IP（轮换使用）"""
        if not self.ips:
            return None
        
        # 轮换
        ip = self.ips[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.ips)
        
        # 避免黑名单IP
        if ip in self.blacklist:
            return self.get_ip()
        
        return ip
    
    def blacklist_ip(self, ip: str):
        """加入黑名单"""
        self.blacklist.add(ip)

class KnowledgeSourceManager:
    """知识源管理器"""
    
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.sources: Dict[str, DataSourceConfig] = {}
        self.account_pool = AccountPool()
        self.ip_pool = IPPool()
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        # 这里应该从配置文件加载，暂时使用示例配置
        # 实际实现应该读取 knowledge_getting_data_source_config.md
        pass
    
    def register_source(self, config: DataSourceConfig):
        """注册数据源"""
        self.sources[config.source_id] = config
        print(f"✅ 注册数据源: {config.name} ({config.source_id})")
    
    def get_source(self, source_id: str) -> Optional[DataSourceConfig]:
        """获取数据源配置"""
        return self.sources.get(source_id)
    
    def get_sources_by_priority(self, priority: Priority) -> List[DataSourceConfig]:
        """按优先级获取数据源"""
        return [s for s in self.sources.values() if s.priority == priority]
    
    def get_sources_by_type(self, source_type: SourceType) -> List[DataSourceConfig]:
        """按类型获取数据源"""
        return [s for s in self.sources.values() if s.source_type == source_type]
    
    def add_account(self, source_id: str, account: Account):
        """添加账号"""
        self.account_pool.add_account(source_id, account)
    
    def get_account(self, source_id: str) -> Optional[Account]:
        """获取账号"""
        return self.account_pool.get_account(source_id)
    
    def add_ip(self, ip: str):
        """添加IP"""
        self.ip_pool.add_ip(ip)
    
    def get_ip(self) -> Optional[str]:
        """获取IP"""
        return self.ip_pool.get_ip()
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "total_sources": len(self.sources),
            "sources_by_type": {
                st.value: len(self.get_sources_by_type(st))
                for st in SourceType
            },
            "sources_by_priority": {
                p.value: len(self.get_sources_by_priority(p))
                for p in Priority
            },
            "total_accounts": sum(len(accounts) for accounts in self.account_pool.accounts.values()),
            "total_ips": len(self.ip_pool.ips),
            "blacklisted_ips": len(self.ip_pool.blacklist)
        }

# 示例配置（应该从配置文件加载）
EXAMPLE_SOURCES = [
    DataSourceConfig(
        source_id="nlc_001",
        name="中国国家图书馆",
        url="https://www.nlc.cn/",
        source_type=SourceType.NATIONAL_LIBRARY,
        priority=Priority.P0,
        data_types=["学术论文", "期刊杂志", "古籍文献", "方志族谱", "数字资源"],
        account_required=True,
        cost="免费",
        difficulty="中等",
        rate_limit="无明确限制",
        coverage="95%+",
        base_url="https://www.nlc.cn/",
        search_url="https://opac.nlc.cn/F",
        download_url="https://opac.nlc.cn/F/?func=file-base",
        registration_url="https://opac.nlc.cn/F/?func=file-dir&file_name=LOGIN",
        required_fields=["用户名", "密码", "手机号", "验证码", "真实姓名", "身份证"],
        captcha_type="图片验证码",
        ip_check="宽松",
        notes="需要实名认证，审核周期1-3天",
        status="待配置"
    ),
    DataSourceConfig(
        source_id="gb_standard_001",
        name="国家标准全文公开系统",
        url="https://openstd.samr.gov.cn/",
        source_type=SourceType.INDUSTRY_STANDARD,
        priority=Priority.P2,
        data_types=["国家标准（GB）", "行业标准", "技术规范", "指导性文件"],
        account_required=False,
        cost="免费",
        difficulty="简单",
        rate_limit="无明确限制",
        coverage="国家标准100%",
        base_url="https://openstd.samr.gov.cn/",
        search_url="https://openstd.samr.gov.cn/",
        download_url="https://openstd.samr.gov.cn/",
        registration_url=None,
        required_fields=[],
        captcha_type="无",
        ip_check="无",
        notes="完全公开，无需注册，可直接下载PDF",
        status="可立即使用"
    )
]

__all__ = [
    "SourceType", "Priority", "DataSourceConfig", "Account", 
    "AccountPool", "IPPool", "KnowledgeSourceManager", "EXAMPLE_SOURCES"
]

"""
右弼星 - 防火墙模块
网络安全防护
"""

import time
import ipaddress
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class RuleType(str, Enum):
    """规则类型"""
    ALLOW = "allow"
    DENY = "deny"
    RATE_LIMIT = "rate_limit"


class IPRule(BaseModel):
    """IP规则"""
    ip: str
    rule_type: RuleType
    description: str = ""
    expires_at: Optional[float] = None


class RateLimitRule(BaseModel):
    """限速规则"""
    endpoint: str
    max_requests: int = Field(default=100, ge=1)
    window_seconds: int = Field(default=60, ge=1)


class Firewall:
    """防火墙"""
    
    def __init__(self):
        self.ip_rules: List[IPRule] = []
        self.rate_limit_rules: List[RateLimitRule] = []
        self.blocked_ips: Dict[str, float] = {}  # IP -> 封禁截止时间
        self.request_counts: Dict[str, List[float]] = {}  # IP -> 请求时间列表
    
    def add_rule(self, rule: IPRule):
        """添加IP规则"""
        # 检查是否已存在
        for existing in self.ip_rules:
            if existing.ip == rule.ip:
                existing.rule_type = rule.rule_type
                return
        self.ip_rules.append(rule)
    
    def remove_rule(self, ip: str) -> bool:
        """移除IP规则"""
        for i, rule in enumerate(self.ip_rules):
            if rule.ip == ip:
                del self.ip_rules[i]
                return True
        return False
    
    def block_ip(self, ip: str, duration_seconds: int = 3600):
        """封禁IP"""
        self.blocked_ips[ip] = time.time() + duration_seconds
    
    def unblock_ip(self, ip: str):
        """解封IP"""
        if ip in self.blocked_ips:
            del self.blocked_ips[ip]
    
    def is_blocked(self, ip: str) -> bool:
        """检查IP是否被封禁"""
        if ip not in self.blocked_ips:
            return False
        
        # 检查封禁是否过期
        if time.time() > self.blocked_ips[ip]:
            del self.blocked_ips[ip]
            return False
        
        return True
    
    def check_ip(self, ip: str) -> tuple[bool, Optional[str]]:
        """检查IP"""
        # 检查是否被封禁
        if self.is_blocked(ip):
            return False, "IP blocked"
        
        # 检查规则
        for rule in self.ip_rules:
            if rule.ip == ip:
                if rule.rule_type == RuleType.ALLOW:
                    return True, None
                elif rule.rule_type == RuleType.DENY:
                    return False, "IP denied by rule"
        
        # 默认拒绝
        return False, "Default deny"
    
    def add_rate_limit(self, rule: RateLimitRule):
        """添加限速规则"""
        # 检查是否已存在
        for existing in self.rate_limit_rules:
            if existing.endpoint == rule.endpoint:
                existing.max_requests = rule.max_requests
                existing.window_seconds = rule.window_seconds
                return
        self.rate_limit_rules.append(rule)
    
    def check_rate_limit(self, ip: str, endpoint: str) -> tuple[bool, Optional[str]]:
        """检查限速"""
        # 查找规则
        rule = None
        for r in self.rate_limit_rules:
            if r.endpoint == endpoint:
                rule = r
                break
        
        if not rule:
            return True, None
        
        # 记录请求
        now = time.time()
        if ip not in self.request_counts:
            self.request_counts[ip] = []
        
        # 清理过期请求
        self.request_counts[ip] = [
            t for t in self.request_counts[ip]
            if now - t < rule.window_seconds
        ]
        
        # 检查是否超过限制
        if len(self.request_counts[ip]) >= rule.max_requests:
            return False, f"Rate limit exceeded: {rule.max_requests} requests per {rule.window_seconds}s"
        
        # 记录新请求
        self.request_counts[ip].append(now)
        return True, None
    
    def check(self, ip: str, endpoint: str = "/") -> tuple[bool, Optional[str]]:
        """综合检查"""
        # IP检查
        allowed, reason = self.check_ip(ip)
        if not allowed:
            return False, reason
        
        # 限速检查
        allowed, reason = self.check_rate_limit(ip, endpoint)
        if not allowed:
            return False, reason
        
        return True, None
    
    def get_status(self) -> Dict:
        """获取状态"""
        return {
            "ip_rules_count": len(self.ip_rules),
            "rate_limit_rules_count": len(self.rate_limit_rules),
            "blocked_ips_count": len(self.blocked_ips),
            "active_ips_count": len(self.request_counts)
        }


# 测试代码
if __name__ == "__main__":
    fw = Firewall()
    
    # 添加规则
    fw.add_rule(IPRule(ip="192.168.1.100", rule_type=RuleType.ALLOW, description="允许内部"))
    fw.add_rule(IPRule(ip="10.0.0.0/8", rule_type=RuleType.ALLOW, description="允许内网"))
    
    # 添加限速
    fw.add_rate_limit(RateLimitRule(endpoint="/api/chat", max_requests=10, window_seconds=60))
    
    # 测试
    print("状态:", fw.get_status())
    print("检查 192.168.1.100:", fw.check_ip("192.168.1.100"))
    print("检查 8.8.8.8:", fw.check_ip("8.8.8.8"))

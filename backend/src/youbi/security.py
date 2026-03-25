"""
右弼星 - 安全审计模块
三层防护、安全审计、风险检测
"""

import time
import hashlib
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class RiskLevel(str, Enum):
    """风险等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AuditEvent(BaseModel):
    """审计事件"""
    event_id: str
    timestamp: float = Field(default_factory=time.time)
    user_id: str
    action: str
    resource: str
    risk_level: RiskLevel = RiskLevel.LOW
    details: Dict = Field(default_factory=dict)


class SecurityPolicy(BaseModel):
    """安全策略"""
    name: str
    description: str
    enabled: bool = True
    rules: List[Dict] = Field(default_factory=list)


class SecurityAuditor:
    """安全审计器"""
    
    def __init__(self):
        self.audit_log: List[AuditEvent] = []
        self.policies: Dict[str, SecurityPolicy] = {}
        self.risk_events: List[AuditEvent] = []
        self._init_default_policies()
    
    def _init_default_policies(self):
        """初始化默认策略"""
        self.policies["command_block"] = SecurityPolicy(
            name="command_block",
            description="阻止危险命令执行",
            enabled=True,
            rules=[
                {"type": "command", "pattern": "rm -rf /"},
                {"type": "command", "pattern": "drop table"},
                {"type": "command", "pattern": "delete from"}
            ]
        )
        
        self.policies["data_access"] = SecurityPolicy(
            name="data_access",
            description="敏感数据访问控制",
            enabled=True,
            rules=[
                {"type": "resource", "pattern": "*.pem"},
                {"type": "resource", "pattern": "*.key"},
                {"type": "resource", "pattern": "password*"}
            ]
        )
    
    def log_event(
        self,
        user_id: str,
        action: str,
        resource: str,
        risk_level: RiskLevel = RiskLevel.LOW,
        details: Dict = None
    ) -> AuditEvent:
        """记录审计事件"""
        event = AuditEvent(
            event_id=hashlib.md5(
                f"{user_id}{action}{resource}{time.time()}".encode()
            ).hexdigest()[:16],
            user_id=user_id,
            action=action,
            resource=resource,
            risk_level=risk_level,
            details=details or {}
        )
        
        self.audit_log.append(event)
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            self.risk_events.append(event)
        
        return event
    
    def check_policy(self, action: str, resource: str) -> tuple[bool, Optional[str]]:
        """检查策略"""
        for policy in self.policies.values():
            if not policy.enabled:
                continue
            
            for rule in policy.rules:
                if rule["type"] == "command" and rule["pattern"] in action:
                    return False, f"Blocked by policy: {policy.name}"
                if rule["type"] == "resource" and rule["pattern"] in resource:
                    return False, f"Blocked by policy: {policy.name}"
        
        return True, None
    
    def get_audit_log(
        self,
        user_id: str = None,
        start_time: float = None,
        limit: int = 100
    ) -> List[AuditEvent]:
        """获取审计日志"""
        logs = self.audit_log
        
        if user_id:
            logs = [e for e in logs if e.user_id == user_id]
        
        if start_time:
            logs = [e for e in logs if e.timestamp >= start_time]
        
        return logs[-limit:]
    
    def get_risk_events(self, level: RiskLevel = None) -> List[AuditEvent]:
        """获取风险事件"""
        if level:
            return [e for e in self.risk_events if e.risk_level == level]
        return self.risk_events
    
    def generate_report(self) -> Dict:
        """生成安全报告"""
        total = len(self.audit_log)
        critical = len([e for e in self.audit_log if e.risk_level == RiskLevel.CRITICAL])
        high = len([e for e in self.audit_log if e.risk_level == RiskLevel.HIGH])
        medium = len([e for e in self.audit_log if e.risk_level == RiskLevel.MEDIUM])
        
        return {
            "summary": {
                "total_events": total,
                "critical": critical,
                "high": high,
                "medium": medium,
            },
            "policies": {
                name: {"enabled": p.enabled, "rules_count": len(p.rules)}
                for name, p in self.policies.items()
            },
            "top_users": self._get_top_users(5)
        }
    
    def _get_top_users(self, limit: int) -> List[Dict]:
        """获取活跃用户"""
        user_counts = {}
        for event in self.audit_log:
            user_counts[event.user_id] = user_counts.get(event.user_id, 0) + 1
        
        sorted_users = sorted(
            user_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return [{"user_id": u, "events": c} for u, c in sorted_users]


# 测试代码
if __name__ == "__main__":
    auditor = SecurityAuditor()
    
    # 记录事件
    auditor.log_event(
        user_id="user001",
        action="login",
        resource="/api/auth",
        risk_level=RiskLevel.LOW
    )
    
    auditor.log_event(
        user_id="user001",
        action="execute_code",
        resource="sandbox",
        risk_level=RiskLevel.MEDIUM
    )
    
    # 检查策略
    allowed, reason = auditor.check_policy("rm -rf /", "any")
    print(f"Allowed: {allowed}, Reason: {reason}")
    
    # 生成报告
    report = auditor.generate_report()
    print(report)

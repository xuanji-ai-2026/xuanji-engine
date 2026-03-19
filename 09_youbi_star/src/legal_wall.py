"""
右弼星（安全层）- 法律防火墙模块
版本: v2.0
负责人: 冯涛 (025)
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import asyncio

class LegalCategory(Enum):
    """法律红线分类"""
    PERSONAL_SAFETY = "personal_safety"      # 人身安全（暴力、伤害、危险行为）
    ILLEGAL_ACTION = "illegal_action"      # 法律行为（诈骗、赌博、洗钱、网络攻击）
    INFORMATION_SECURITY = "information_security" # 信息安全（造谣、传谣、伪造公文）
    RIGHTS_PROTECTION = "rights_protection"   # 权利保护（诽谤、版权侵犯、歧视）
    EXECUTION_BAN = "execution_ban"          # 执行禁区（越权、未授权访问）

class SecurityLevel(Enum):
    """安全等级"""
    LEGAL = "legal"        # 法律合规
    MORAL = "moral"        # 道德合规
    PERMISSION = "permission" # 权限合规

@dataclass
class SecurityCheckResult:
    """安全检查结果"""
    passed: bool
    security_level: SecurityLevel
    violation_category: Optional[LegalCategory]
    violation_reason: Optional[str]
    confidence: float
    actions: List[str] = field(default_factory=list)

class LegalWall:
    """法律防火墙"""
    
    def __init__(self):
        # 违禁词库
        self.forbidden_keywords = {
            LegalCategory.PERSONAL_SAFETY: [
                "杀人", "自杀", "暴力", "伤害", "伤害", "自杀", "袭击", "攻击",
                "虐待", "虐待", "残忍", "残忍", "虐待动物", "虐待儿童"
            ],
            LegalCategory.ILLEGAL_ACTION: [
                "诈骗", "赌博", "洗钱", "非法集资", "高利贷", "传销", "非法集资",
                "网络攻击", "黑客", "黑客", "钓鱼", "黑客攻击", "网络钓鱼",
                "伪造", "伪造公文", "造谣", "传谣", "伪造证件", "假证", "假证",
                "洗钱", "洗钱", "地下钱庄", "非法转账", "地下转账"
            ],
            LegalCategory.INFORMATION_SECURITY: [
                "造谣", "传谣", "虚假", "谣言", "假新闻", "谣言",
                "机密", "泄密", "泄露", "机密文件", "国家机密", "商业机密",
                "窃取", "窃取", "数据窃取", "获取", "非法获取", "非法获得"
            ],
            LegalCategory.RIGHTS_PROTECTION: [
                "诽谤", "中伤", "诬谤罪", "中伤罪", "造谣中伤", "造谣中伤",
                "版权侵犯", "盗版", "侵犯版权", "侵权", "抄袭", "盗版", "侵犯版权",
                "歧视", "歧视", "种族歧视", "性别歧视", "地域歧视", "宗教歧视"
            ],
            LegalCategory.EXECUTION_BAN: [
                "越权", "越权访问", "未授权", "未授权访问",
                "入侵", "系统入侵", "黑客攻击", "入侵系统",
                "破坏", "系统破坏", "系统破坏", "恶意破坏",
                "窃取", "窃取数据", "非法获取", "非法获取",
                "篡改", "篡改数据", "非法篡改", "修改数据", "非法修改"
            ]
        }
        
        # 告警规则
        self.alert_rules = {
            "CRITICAL": [
                LegalCategory.PERSONAL_SAFETY,
                LegalCategory.ILLEGAL_ACTION
            ],
            "HIGH": [
                LegalCategory.INFORMATION_SECURITY,
                LegalCategory.EXECUTION_BAN
            ],
            "MEDIUM": [
                LegalCategory.RIGHTS_PROTECTION
            ]
        }
    
    async def check_content(
        self,
        content: str,
        user_id: str,
        context: Optional[Dict[str, Any]] = None
    ) -> SecurityCheckResult:
        """
        检查内容是否违法
        
        Args:
            content: 输入内容
            user_id: 用户ID
            context: 上下文
        
        Returns:
            SecurityCheckResult: 安全检查结果
        """
        content_lower = content.lower()
        
        # 检查每个违法类别
        for category, keywords in self.forbidden_keywords.items():
            for keyword in keywords:
                if keyword in content_lower:
                    severity = self._get_severity(category)
                    
                    return SecurityCheckResult(
                        passed=False,
                        security_level=SecurityLevel.LEGAL,
                        violation_category=category,
                        violation_reason=f"包含违法关键词: {keyword}",
                        confidence=1.0,
                        actions=["拒绝", "审计", "告警", "阻止"]
                    )
        
        # 未检测到违法
        return SecurityCheckResult(
            passed=True,
            security_level=SecurityLevel.LEGAL,
            confidence=0.99,
            actions=["通过"]
        )
    
    def _get_severity(self, category: LegalCategory) -> str:
        """获取严重等级"""
        for severity, categories in self.alert_rules.items():
            if category in categories:
                return severity
        return "LOW"

# 示例使用
if __name__ == "__main__":
    async def main():
    wall = LegalWall()
    
    # 测试违法内容
    result = await wall.check_content(
        content="我想制造假新闻",
        user_id="user_001",
        context={}
    )
    
    print(f"检查结果: {result.violation_reason}")
    
    asyncio.run(main())

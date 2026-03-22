#!/usr/bin/env python3
"""
AI数字员工第三期开发启动脚本（最终修正版）
创建时间: 2026-03-22 08:00
修正内容:
1. 从第一期第二期开发人员名单加载真实AI数字员工
2. 包括玄玑引擎团队77人（10名组长 + 67名成员）
3. 任务分配给组员（而非组长）
4. 组长负责管理和代码审查
5. 增补支援人员也系统驱动

核心原则（必须遵守）:
1. AI员工不需要"手动签收"、"手动阅读"、"手动反馈"
2. 系统自动解析开发文档
3. 系统自动分解为代码任务
4. 系统自动注入AI员工工作队列
5. AI员工立即开始编写代码
"""

import asyncio
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

# 添加项目路径
sys.path.insert(0, "/workspace/projects/workspace/xuanji-engine-v2")

from multi_project_task_queue import MultiProjectTaskQueue, Task, TaskPriority
from code_generator import CodeGenerator
from auto_git_commit import AutoCommitManager

class Phase3Launcher:
    """第三期开发启动器（最终修正版）"""

    def __init__(self):
        self.incoming_dir = Path("/workspace/projects/workspace/incoming")
        self.project_path = Path("/workspace/projects/workspace/xuanji-engine-v2")
        self.task_queue = MultiProjectTaskQueue()
        self.code_generator = CodeGenerator()
        self.git_manager = AutoCommitManager()

        # 180名员工：核心管理层10人 + 各部门90人 + 玄玑引擎团队80人
        self.employees: Dict[str, Dict] = {}
        self.stats = {
            "total_employees": 0,
            "active_employees": 0,
            "total_tasks": 0,
            "assigned_tasks": 0,
            "start_time": None
        }

        # 注册Git仓库
        if self.project_path.exists():
            self.git_manager.register_repo("xuanji_engine", str(self.project_path))

    def load_third_phase_docs(self) -> List[Dict]:
        """加载第三期开发文档"""
        docs = []

        # 开发文档（10-29号）
        for i in range(10, 30):
            matching = list(self.incoming_dir.glob(f"{i:02d}_*.md"))
            if matching:
                for file in matching:
                    doc_info = {
                        "id": i,
                        "name": file.stem,
                        "path": str(file),
                        "category": self._get_category(i)
                    }
                    docs.append(doc_info)

        # 核心文档（01-09号）
        for i in range(1, 10):
            matching = list(self.incoming_dir.glob(f"{i:02d}_*.md"))
            if matching:
                for file in matching:
                    doc_info = {
                        "id": i,
                        "name": file.stem,
                        "path": str(file),
                        "category": "core"
                    }
                    docs.append(doc_info)

        return sorted(docs, key=lambda x: x["id"])

    def _get_category(self, doc_id: int) -> str:
        """根据文档ID获取星层类别"""
        mapping = {
            10: "XJ01",  # 紫微帝星
            20: "XJ01",
            11: "XJ02",  # 禄存星
            21: "XJ02",
            12: "XJ03",  # 巨门星
            22: "XJ03",
            13: "XJ04",  # 贪狼星
            23: "XJ04",
            14: "XJ05",  # 廉贞星
            24: "XJ05",
            15: "XJ06",  # 武曲星
            25: "XJ06",
            16: "XJ07",  # 破军星
            26: "XJ07",
            17: "XJ08",  # 左辅星
            27: "XJ08",
            18: "XJ09",  # 右弼星
            28: "XJ09",
            19: "XJ10",  # 辅弼星辰
            29: "XJ10",
        }
        return mapping.get(doc_id, "UNKNOWN")

    def load_employees_from_phase1_phase2(self) -> Dict[str, Dict]:
        """从第一期第二期开发人员名单加载真实AI数字员工"""
        employees = {}

        # ==================== 核心管理层（10人） ====================
        core_management = [
            ("001", "李明远", "CEO", "核心管理层"),
            ("002", "张志远", "CTO", "核心管理层"),
            ("003", "王思远", "CPO", "核心管理层"),
            ("004", "赵华", "CMO", "核心管理层"),
            ("005", "孙强", "CSO", "核心管理层"),
            ("006", "周敏", "CCSO", "核心管理层"),
            ("007", "吴刚", "CHO", "核心管理层"),
            ("008", "郑睿", "CFO", "核心管理层"),
            ("009", "钱进", "CLO", "核心管理层"),
            ("010", "冯涛", "COO", "核心管理层"),
        ]

        for emp_id, name, role, dept in core_management:
            employees[emp_id] = {
                "id": emp_id,
                "name": name,
                "role": role,
                "department": dept,
                "status": "idle",
                "assigned_tasks": 0,
                "completed_tasks": 0,
                "is_leader": False,
                "is_manager": True,
                "team": "管理层"
            }

        # ==================== 玄玑引擎团队（80人）====================

        # 组长（10人）
        group_leaders = [
            ("102", "陈元灵", "XJ01组长", "玄玑引擎", "XJ01紫微元灵"),
            ("111", "周禄存", "XJ02组长", "玄玑引擎", "XJ02禄存星"),
            ("119", "蒋巨门", "XJ03组长", "玄玑引擎", "XJ03巨门星"),
            ("163", "伍廉贞", "XJ04组长", "玄玑引擎", "XJ04廉贞星"),
            ("127", "谢武功", "XJ05组长", "玄玑引擎", "XJ05武曲星"),
            ("133", "章军", "XJ06组长", "玄玑引擎", "XJ06破军星"),
            ("146", "倪左辅", "XJ07组长", "玄玑引擎", "XJ07左辅星"),
            ("105", "周右弼", "XJ08组长", "玄玑引擎", "XJ08右弼星"),
            ("143", "薛贪狼", "XJ09组长", "玄玑引擎", "XJ09贪狼星"),
            ("161", "齐辅弼", "XJ10组长", "玄玑引擎", "XJ10辅弼星辰"),
        ]

        for emp_id, name, role, dept, team in group_leaders:
            employees[emp_id] = {
                "id": emp_id,
                "name": name,
                "role": role,
                "department": dept,
                "status": "idle",
                "assigned_tasks": 0,
                "completed_tasks": 0,
                "is_leader": True,
                "is_manager": False,
                "team": team
            }

        # 成员（67人）- 第一期第二期真实员工
        xj01_members = [
            ("106", "张一凡", "XJ01成员"), ("107", "刘二明", "XJ01成员"),
            ("108", "王三思", "XJ01成员"), ("109", "赵四维", "XJ01成员"),
            ("110", "孙五维", "XJ01成员"),
        ]

        xj02_members = [
            ("112", "吴存真", "XJ02成员"), ("113", "郑存义", "XJ02成员"),
            ("114", "钱存信", "XJ02成员"), ("115", "冯存智", "XJ02成员"),
            ("116", "陈存理", "XJ02成员"), ("117", "褚存道", "XJ02成员"),
            ("118", "卫存德", "XJ02成员"),
        ]

        xj03_members = [
            ("120", "沈巨明", "XJ03成员"), ("121", "韩巨亮", "XJ03成员"),
            ("122", "杨巨知", "XJ03成员"), ("123", "朱巨信", "XJ03成员"),
            ("124", "秦巨诚", "XJ03成员"), ("125", "许巨真", "XJ03成员"),
            ("126", "戚巨实", "XJ03成员"),
        ]

        xj04_members = [
            ("164", "余廉心", "XJ04成员"), ("165", "元廉情", "XJ04成员"),
            ("166", "孟廉意", "XJ04成员"),
        ]

        xj05_members = [
            ("128", "邹武全", "XJ05成员"), ("129", "喻武能", "XJ05成员"),
            ("130", "柏武技", "XJ05成员"), ("131", "水武库", "XJ05成员"),
            ("132", "窦武备", "XJ05成员"),
        ]

        xj06_members = [
            ("134", "云破敌", "XJ06成员"), ("135", "苏破阵", "XJ06成员"),
            ("136", "潘破晓", "XJ06成员"), ("137", "葛破浪", "XJ06成员"),
            ("138", "奚破浪", "XJ06成员"), ("139", "范破空", "XJ06成员"),
            ("140", "柯破云", "XJ06成员"),
        ]

        xj07_members = [
            ("147", "汤左膀", "XJ07成员"), ("148", "殷左翼", "XJ07成员"),
            ("149", "殷左护", "XJ07成员"), ("150", "罗左卫", "XJ07成员"),
            ("151", "毕左护", "XJ07成员"), ("152", "郝左持", "XJ07成员"),
            ("153", "邬左扶", "XJ07成员"), ("154", "安左助", "XJ07成员"),
            ("155", "常左协", "XJ07成员"), ("101", "李星辰", "XJ07成员"),
            ("156", "乐右弼", "XJ07成员"),
        ]

        xj08_members = [
            ("157", "于右护", "XJ08成员"), ("158", "时右卫", "XJ08成员"),
            ("159", "皮右防", "XJ08成员"), ("160", "卞右盾", "XJ08成员"),
            ("176", "贡志强", "XJ08成员"),
        ]

        xj09_members = [
            ("144", "雷贪音", "XJ09成员"), ("145", "贺贪形", "XJ09成员"),
            ("177", "赏志明", "XJ09成员"), ("178", "巴图", "XJ09成员"),
            ("179", "弓志明", "XJ09成员"), ("180", "母志明", "XJ09成员"),
        ]

        xj10_members = [
            ("162", "康辅星", "XJ10成员"), ("168", "和产品", "XJ10成员"),
            ("169", "穆产品", "XJ10成员"), ("183", "财市场", "XJ10成员"),
            ("184", "干市场", "XJ10成员"), ("185", "曲市场", "XJ10成员"),
            ("188", "桥客服", "XJ10成员"), ("189", "银客服", "XJ10成员"),
            ("190", "言客服", "XJ10成员"),
        ]

        # 加载所有星层成员
        for members, team_name in [
            (xj01_members, "XJ01紫微元灵"),
            (xj02_members, "XJ02禄存星"),
            (xj03_members, "XJ03巨门星"),
            (xj04_members, "XJ04廉贞星"),
            (xj05_members, "XJ05武曲星"),
            (xj06_members, "XJ06破军星"),
            (xj07_members, "XJ07左辅星"),
            (xj08_members, "XJ08右弼星"),
            (xj09_members, "XJ09贪狼星"),
            (xj10_members, "XJ10辅弼星辰"),
        ]:
            for emp_id, name, role in members:
                employees[emp_id] = {
                    "id": emp_id,
                    "name": name,
                    "role": role,
                    "department": "玄玑引擎",
                    "status": "idle",
                    "assigned_tasks": 0,
                    "completed_tasks": 0,
                    "is_leader": False,
                    "is_manager": False,
                    "team": team_name
                }

        # ==================== 增补支援人员（90人）====================

        # 技术开发部（30人）- 第一期第二期真实员工
        tech_members = [
            ("011", "张伟", "临时CTO"), ("012", "刘斌", "后端工程师"),
            ("013", "赵阳", "后端工程师"), ("014", "葛浩", "后端工程师"),
            ("015", "昌艺", "后端工程师"), ("016", "陈磊", "后端工程师"),
            ("017", "周杰", "后端工程师"), ("018", "马丽", "后端工程师"),
            ("019", "赵强", "后端工程师"), ("020", "钱浩", "后端工程师"),
            ("021", "孙明", "后端工程师"), ("022", "周明", "后端工程师"),
            ("023", "吴浩", "后端工程师"), ("024", "郑明", "后端工程师"),
            ("025", "冯浩", "后端工程师"), ("026", "钱明", "后端工程师"),
            ("027", "孙浩", "后端工程师"), ("028", "周浩", "后端工程师"),
            ("029", "吴明", "测试工程师"), ("030", "郑浩", "测试工程师"),
            ("031", "冯明", "测试工程师"), ("032", "钱浩", "测试工程师"),
            ("033", "孙明", "测试工程师"), ("034", "周明", "测试工程师"),
            ("035", "吴浩", "运维工程师"), ("036", "郑明", "运维工程师"),
            ("037", "冯浩", "运维工程师"), ("038", "钱明", "运维工程师"),
            ("039", "孙浩", "运维工程师"), ("040", "周浩", "运维工程师"),
        ]

        for emp_id, name, role in tech_members:
            employees[emp_id] = {
                "id": emp_id,
                "name": name,
                "role": role,
                "department": "技术开发部",
                "status": "idle",
                "assigned_tasks": 0,
                "completed_tasks": 0,
                "is_leader": False,
                "is_manager": False,
                "team": "技术开发"
            }

        # 产品设计部（20人）
        design_members = [
            ("041", "吴明", "UI设计师"), ("042", "郑浩", "UI设计师"),
            ("043", "冯明", "UI设计师"), ("044", "钱浩", "UI设计师"),
            ("045", "孙明", "UI设计师"), ("046", "周明", "UI设计师"),
            ("047", "吴浩", "UI设计师"), ("048", "郑明", "UI设计师"),
            ("049", "冯浩", "UI设计师"), ("050", "钱明", "UI设计师"),
            ("051", "孙浩", "产品经理"), ("052", "周浩", "产品经理"),
            ("053", "吴浩", "产品经理"), ("054", "郑浩", "产品经理"),
            ("055", "冯浩", "产品经理"), ("056", "钱明", "产品经理"),
            ("057", "孙明", "产品经理"), ("058", "周明", "产品经理"),
            ("059", "吴浩", "产品经理"), ("060", "郑浩", "产品经理"),
        ]

        for emp_id, name, role in design_members:
            employees[emp_id] = {
                "id": emp_id,
                "name": name,
                "role": role,
                "department": "产品设计部",
                "status": "idle",
                "assigned_tasks": 0,
                "completed_tasks": 0,
                "is_leader": False,
                "is_manager": False,
                "team": "产品设计"
            }

        # 市场销售部（18人）
        sales_members = [
            ("061", "冯明", "市场专员"), ("062", "钱浩", "市场专员"),
            ("063", "孙明", "市场专员"), ("064", "周明", "销售经理"),
            ("065", "吴浩", "销售经理"), ("066", "郑明", "销售经理"),
            ("067", "冯浩", "销售经理"), ("068", "钱明", "销售经理"),
            ("069", "孙浩", "销售经理"), ("070", "周浩", "销售经理"),
            ("071", "吴浩", "销售经理"), ("072", "郑明", "销售经理"),
            ("073", "冯浩", "市场专员"), ("074", "钱明", "市场专员"),
            ("075", "孙明", "市场专员"), ("076", "周明", "市场专员"),
            ("077", "吴浩", "市场专员"), ("078", "郑明", "市场专员"),
        ]

        for emp_id, name, role in sales_members:
            employees[emp_id] = {
                "id": emp_id,
                "name": name,
                "role": role,
                "department": "市场销售部",
                "status": "idle",
                "assigned_tasks": 0,
                "completed_tasks": 0,
                "is_leader": False,
                "is_manager": False,
                "team": "市场销售"
            }

        # 客服支持部（12人）
        support_members = [
            ("079", "冯浩", "客服专员"), ("080", "钱明", "客服专员"),
            ("081", "孙浩", "客服专员"), ("082", "周明", "客服专员"),
            ("083", "吴浩", "客服专员"), ("084", "郑明", "客服专员"),
            ("085", "冯浩", "客服专员"), ("086", "钱明", "客服专员"),
            ("087", "孙浩", "客服专员"), ("088", "周明", "客服专员"),
            ("089", "吴浩", "客服专员"), ("090", "郑明", "客服专员"),
        ]

        for emp_id, name, role in support_members:
            employees[emp_id] = {
                "id": emp_id,
                "name": name,
                "role": role,
                "department": "客服支持部",
                "status": "idle",
                "assigned_tasks": 0,
                "completed_tasks": 0,
                "is_leader": False,
                "is_manager": False,
                "team": "客服支持"
            }

        # 专业支持部（10人）
        professional_members = [
            ("091", "冯浩", "技术顾问"), ("092", "钱明", "业务顾问"),
            ("093", "孙浩", "咨询顾问"), ("094", "周明", "解决方案顾问"),
            ("095", "吴浩", "培训顾问"), ("096", "郑明", "实施顾问"),
            ("097", "冯浩", "迁移顾问"), ("098", "钱明", "集成顾问"),
            ("099", "孙浩", "定制开发顾问"), ("100", "周浩", "高级顾问"),
        ]

        for emp_id, name, role in professional_members:
            employees[emp_id] = {
                "id": emp_id,
                "name": name,
                "role": role,
                "department": "专业支持部",
                "status": "idle",
                "assigned_tasks": 0,
                "completed_tasks": 0,
                "is_leader": False,
                "is_manager": False,
                "team": "专业支持"
            }

        return employees

    def parse_docs_to_tasks(self, docs: List[Dict]) -> List[Task]:
        """将开发文档解析为代码任务，分配给星层组员而非组长"""
        tasks = []

        # 定义每个星层的组员（不包括组长）
        xj01_members = ["106", "107", "108", "109", "110"]
        xj02_members = ["112", "113", "114", "115", "116", "117", "118"]
        xj03_members = ["120", "121", "122", "123", "124", "125", "126"]
        xj04_members = ["164", "165", "166"]
        xj05_members = ["128", "129", "130", "131", "132"]
        xj06_members = ["134", "135", "136", "137", "138", "139", "140"]
        xj07_members = ["147", "148", "149", "150", "151", "152", "153", "154", "155", "101", "156"]
        xj08_members = ["157", "158", "159", "160", "176"]
        xj09_members = ["144", "145", "177", "178", "179", "180"]
        xj10_members = ["162", "168", "169", "183", "184", "185", "188", "189", "190"]

        task_index = 0

        for doc in docs:
            category = doc["category"]
            doc_id = doc["id"]

            if category == "XJ01":
                tasks.extend([
                    Task(f"P3-XJ01-{doc_id}-001", "元灵层核心模块", "元灵层", "xuanji_engine", "01_ziwei_star", xj01_members[task_index % len(xj01_members)], TaskPriority.P0),
                    Task(f"P3-XJ01-{doc_id}-002", "意图识别增强", "意图识别", "xuanji_engine", "01_ziwei_star", xj01_members[(task_index + 1) % len(xj01_members)], TaskPriority.P0),
                ])
                task_index += 2
            elif category == "XJ02":
                tasks.extend([
                    Task(f"P3-XJ02-{doc_id}-001", "调度层核心模块", "调度层", "xuanji_engine", "02_lucun_star", xj02_members[task_index % len(xj02_members)], TaskPriority.P0),
                    Task(f"P3-XJ02-{doc_id}-002", "ReAct引擎优化", "ReAct引擎", "xuanji_engine", "02_lucun_star", xj02_members[(task_index + 1) % len(xj02_members)], TaskPriority.P0),
                ])
                task_index += 2
            elif category == "XJ03":
                tasks.extend([
                    Task(f"P3-XJ03-{doc_id}-001", "记忆层核心模块", "记忆层", "xuanji_engine", "03_jumen_star", xj03_members[task_index % len(xj03_members)], TaskPriority.P0),
                    Task(f"P3-XJ03-{doc_id}-002", "向量检索优化", "向量检索", "xuanji_engine", "03_jumen_star", xj03_members[(task_index + 1) % len(xj03_members)], TaskPriority.P0),
                ])
                task_index += 2
            elif category == "XJ04":
                tasks.extend([
                    Task(f"P3-XJ04-{doc_id}-001", "交互层核心模块", "交互层", "xuanji_engine", "04_lianzheng_star", xj04_members[task_index % len(xj04_members)], TaskPriority.P0),
                    Task(f"P3-XJ04-{doc_id}-002", "ASR/TTS集成", "语音交互", "xuanji_engine", "04_lianzheng_star", xj04_members[(task_index + 1) % len(xj04_members)], TaskPriority.P0),
                ])
                task_index += 2
            elif category == "XJ05":
                tasks.extend([
                    Task(f"P3-XJ05-{doc_id}-001", "人格层核心模块", "人格层", "xuanji_engine", "05_wuqu_star", xj05_members[task_index % len(xj05_members)], TaskPriority.P0),
                    Task(f"P3-XJ05-{doc_id}-002", "情绪状态机", "情绪引擎", "xuanji_engine", "05_wuqu_star", xj05_members[(task_index + 1) % len(xj05_members)], TaskPriority.P0),
                ])
                task_index += 2
            elif category == "XJ06":
                tasks.extend([
                    Task(f"P3-XJ06-{doc_id}-001", "技能层核心模块", "技能层", "xuanji_engine", "06_pojun_star", xj06_members[task_index % len(xj06_members)], TaskPriority.P0),
                    Task(f"P3-XJ06-{doc_id}-002", "插件系统增强", "插件系统", "xuanji_engine", "06_pojun_star", xj06_members[(task_index + 1) % len(xj06_members)], TaskPriority.P0),
                ])
                task_index += 2
            elif category == "XJ07":
                tasks.extend([
                    Task(f"P3-XJ07-{doc_id}-001", "执行层核心模块", "执行层", "xuanji_engine", "07_zuofu_star", xj07_members[task_index % len(xj07_members)], TaskPriority.P0),
                    Task(f"P3-XJ07-{doc_id}-002", "沙箱隔离环境", "沙箱", "xuanji_engine", "07_zuofu_star", xj07_members[(task_index + 1) % len(xj07_members)], TaskPriority.P0),
                ])
                task_index += 2
            elif category == "XJ08":
                tasks.extend([
                    Task(f"P3-XJ08-{doc_id}-001", "底座层核心模块", "底座层", "xuanji_engine", "08_youbi_star", xj08_members[task_index % len(xj08_members)], TaskPriority.P0),
                    Task(f"P3-XJ08-{doc_id}-002", "用户管理系统", "用户管理", "xuanji_engine", "08_youbi_star", xj08_members[(task_index + 1) % len(xj08_members)], TaskPriority.P0),
                ])
                task_index += 2
            elif category == "XJ09":
                tasks.extend([
                    Task(f"P3-XJ09-{doc_id}-001", "安全层核心模块", "安全层", "xuanji_engine", "09_tanlang_star", xj09_members[task_index % len(xj09_members)], TaskPriority.P0),
                    Task(f"P3-XJ09-{doc_id}-002", "权限控制系统", "权限控制", "xuanji_engine", "09_tanlang_star", xj09_members[(task_index + 1) % len(xj09_members)], TaskPriority.P0),
                ])
                task_index += 2
            elif category == "XJ10":
                tasks.extend([
                    Task(f"P3-XJ10-{doc_id}-001", "扩展层核心模块", "扩展层", "xuanji_engine", "10_fubi_star", xj10_members[task_index % len(xj10_members)], TaskPriority.P0),
                    Task(f"P3-XJ10-{doc_id}-002", "插件市场", "插件市场", "xuanji_engine", "10_fubi_star", xj10_members[(task_index + 1) % len(xj10_members)], TaskPriority.P0),
                ])
                task_index += 2

        return tasks

    def activate_employees(self):
        """激活所有AI员工"""
        print("\n" + "=" * 80)
        print("🚀 AI数字员工第三期开发启动（最终修正版）")
        print("=" * 80)
        print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        # 加载真实员工（从第一期第二期）
        self.employees = self.load_employees_from_phase1_phase2()
        print(f"\n✅ 员工加载完成: {len(self.employees)} 人")

        # 统计各部门
        dept_stats = {}
        role_stats = {"核心管理层": 0, "组长": 0, "玄玑成员": 0, "支援人员": 0}

        for emp in self.employees.values():
            dept = emp["department"]
            dept_stats[dept] = dept_stats.get(dept, 0) + 1

            if emp["is_manager"]:
                role_stats["核心管理层"] += 1
            elif emp["is_leader"]:
                role_stats["组长"] += 1
            elif dept == "玄玑引擎":
                role_stats["玄玑成员"] += 1
            else:
                role_stats["支援人员"] += 1

        print("\n部门分布:")
        for dept, count in sorted(dept_stats.items()):
            print(f"  - {dept}: {count} 人")

        print("\n角色分布:")
        for role, count in sorted(role_stats.items()):
            print(f"  - {role}: {count} 人")

        # 激活所有员工
        print(f"\n🔥 正在激活 {len(self.employees)} 名AI员工...")
        for emp_id, emp in self.employees.items():
            emp["status"] = "active"
            if emp["is_manager"]:
                print(f"  ✅ [{emp_id}] {emp['name']} - {emp['role']} 已激活（管理层）")
            elif emp["is_leader"]:
                print(f"  ✅ [{emp_id}] {emp['name']} - {emp['role']} 已激活（组长）")
            elif dept == "玄玑引擎":
                print(f"  ✅ [{emp_id}] {emp['name']} - {emp['role']} 已激活（玄玑成员）")
            else:
                print(f"  ✅ [{emp_id}] {emp['name']} - {emp['role']} 已激活（支援）")

        self.stats["total_employees"] = len(self.employees)
        self.stats["active_employees"] = len(self.employees)
        print(f"\n✅ 所有员工已激活！{len(self.employees)} 人在岗")

    def inject_tasks(self):
        """注入任务到AI员工工作队列"""
        print(f"\n📋 正在解析第三期开发文档...")

        # 加载开发文档
        docs = self.load_third_phase_docs()
        print(f"✅ 加载开发文档: {len(docs)} 份")

        # 解析为任务
        tasks = self.parse_docs_to_tasks(docs)
        print(f"✅ 解析为代码任务: {len(tasks)} 个")

        # 注入任务队列
        print(f"\n🎯 正在分配任务给AI员工组员...")
        for task in tasks:
            self.task_queue.add_task("xuanji_engine", task)
            if task.employee_id in self.employees:
                self.employees[task.employee_id]["assigned_tasks"] += 1

        # 统计分配情况
        assigned_employees = sum(1 for emp in self.employees.values() if emp["assigned_tasks"] > 0)
        leader_assigned = sum(1 for emp in self.employees.values() if emp["assigned_tasks"] > 0 and emp["is_leader"])
        member_assigned = sum(1 for emp in self.employees.values() if emp["assigned_tasks"] > 0 and emp["department"] == "玄玑引擎" and not emp["is_leader"])

        print(f"✅ 任务分配完成: {len(tasks)} 个任务已分配给 {assigned_employees} 名员工")
        print(f"  - 玄玑成员收到任务: {member_assigned} 人 ✅")
        print(f"  - 组长收到任务: {leader_assigned} 人 ⚠️ （组长应该管理，不应编码）")

        self.stats["total_tasks"] = len(tasks)
        self.stats["assigned_tasks"] = len(tasks)

    def start_development(self):
        """启动开发"""
        print(f"\n🎨 AI数字员工开始编写代码...")
        print(f"📝 预计第一批代码提交时间: {datetime.now().strftime('%H:%M')} + 20分钟")

        self.stats["start_time"] = datetime.now()

        print(f"\n{'=' * 80}")
        print("✅ 第三期开发启动完成！（最终修正版）")
        print(f"{'=' * 80}")
        print(f"📊 统计信息:")
        print(f"  - 激活员工: {self.stats['active_employees']}/{self.stats['total_employees']}")
        print(f"  - 分配任务: {self.stats['assigned_tasks']}/{self.stats['total_tasks']}")
        print(f"  - 启动时间: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 80}")
        print(f"💡 核心原则:")
        print(f"  - ✅ 从第一期第二期加载真实AI数字员工")
        print(f"  - ✅ 系统自动解析文档（无需手动阅读）")
        print(f"  - ✅ 系统自动分解任务（无需手动分配）")
        print(f"  - ✅ 系统自动激活员工（无需到岗）")
        print(f"  - ✅ AI员工立即开始编写代码")
        print(f"  - ✅ AI员工每小时自动汇报进度")
        print(f"  - ✅ AI员工每4小时自动提交代码")
        print(f"  - ✅ 任务分配给组员（而非组长）")
        print(f"  - ✅ 组长负责管理和代码审查")
        print(f"  - ✅ 增补支援人员也系统驱动")
        print(f"{'=' * 80}")


def main():
    """主函数"""
    launcher = Phase3Launcher()

    # 步骤1: 激活AI员工
    launcher.activate_employees()

    # 步骤2: 注入任务
    launcher.inject_tasks()

    # 步骤3: 启动开发
    launcher.start_development()

    print(f"\n🎉 AI数字员工系统启动完成！现在开始干活！")
    print(f"🕐 下一次代码提交: 约20分钟后 ({datetime.now().strftime('%H:%M')} -> 20分钟后)")
    print(f"📊 下一次进度汇报: 1小时后 ({(datetime.now().replace(minute=0, second=0) + timedelta(hours=1)).strftime('%H:%M')})")


if __name__ == "__main__":
    main()

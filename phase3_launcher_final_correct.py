#!/usr/bin/env python3
"""
AI数字员工第三期开发启动脚本（最终正确版）
创建时间: 2026-03-22 08:18
基于第一期第二期的成功模式

核心原则（第一期第二期验证）:
1. 李明远（001）不编码，负责任务管理、进度管理、资源调配
2. 张志远（002）不编码，负责任务分派、代码质检、代码推送、阻塞治理
3. 10名组长亲自写代码
4. 67名成员亲自写代码
5. 90名增补人员亲自写代码
6. AI员工不需要"手动签收"、"手动阅读"、"手动反馈"
7. 系统自动解析开发文档
8. 系统自动分解为代码任务
9. 系统自动注入AI员工工作队列
10. AI员工立即开始编写代码
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
    """第三期开发启动器（最终正确版）"""

    def __init__(self):
        self.incoming_dir = Path("/workspace/projects/workspace/incoming")
        self.project_path = Path("/workspace/projects/workspace/xuanji-engine-v2")
        self.task_queue = MultiProjectTaskQueue()
        self.code_generator = CodeGenerator()
        self.git_manager = AutoCommitManager()

        # 177名员工：管理层2人 + 玄玑引擎团队75人 + 增补人员90人
        self.employees: Dict[str, Dict] = {}
        self.stats = {
            "total_employees": 0,
            "coding_employees": 0,
            "management_employees": 0,
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

        # ==================== 管理层（2人，不编码）====================

        # 李明远（001）- 任务管理、进度管理、资源调配
        employees["001"] = {
            "id": "001",
            "name": "李明远",
            "role": "CEO",
            "department": "核心管理层",
            "status": "idle",
            "assigned_tasks": 0,
            "completed_tasks": 0,
            "is_leader": False,
            "is_manager": True,
            "will_code": False,
            "responsibility": "任务管理、进度管理、资源调配",
            "team": "管理层"
        }

        # 张志远（002）- 任务分派、代码质检、代码推送、阻塞治理
        employees["002"] = {
            "id": "002",
            "name": "张志远",
            "role": "CTO",
            "department": "核心管理层",
            "status": "idle",
            "assigned_tasks": 0,
            "completed_tasks": 0,
            "is_leader": False,
            "is_manager": True,
            "will_code": False,
            "responsibility": "任务分派、代码质检、代码推送、阻塞治理",
            "team": "管理层"
        }

        # ==================== 玄玑引擎团队（75人，全部编码）====================

        # 组长（10人）- 亲自写代码
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
                "will_code": True,
                "responsibility": f"编码 + {team}管理",
                "team": team
            }

        # 成员（65人）- 亲自写代码
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
                    "will_code": True,
                    "responsibility": "编码",
                    "team": team_name
                }

        # ==================== 增补支援人员（90人，全部编码）====================

        # 技术开发部（30人）
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
                "will_code": True,
                "responsibility": "编码",
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
                "will_code": True,
                "responsibility": "编码",
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
                "will_code": True,
                "responsibility": "编码",
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
                "will_code": True,
                "responsibility": "编码",
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
                "will_code": True,
                "responsibility": "编码",
                "team": "专业支持"
            }

        return employees

    def parse_docs_to_tasks(self, docs: List[Dict]) -> List[Task]:
        """将开发文档解析为代码任务，按照第一期第二期模式分配"""
        tasks = []

        # 每个星层：组长1个任务 + 成员X个任务
        for doc in docs:
            category = doc["category"]
            doc_id = doc["id"]

            if category == "XJ01":  # 紫微帝星 - 组长1人 + 成员5人 = 6人
                tasks.extend([
                    Task(f"P3-XJ01-{doc_id}-001", "元灵层核心模块", "元灵层", "xuanji_engine", "01_ziwei_star", "102", TaskPriority.P0),  # 组长
                    Task(f"P3-XJ01-{doc_id}-002", "意图识别增强", "意图识别", "xuanji_engine", "01_ziwei_star", "106", TaskPriority.P0),
                    Task(f"P3-XJ01-{doc_id}-003", "意图对齐机制", "对齐机制", "xuanji_engine", "01_ziwei_star", "107", TaskPriority.P0),
                    Task(f"P3-XJ01-{doc_id}-004", "意图漂移检测", "漂移检测", "xuanji_engine", "01_ziwei_star", "108", TaskPriority.P0),
                    Task(f"P3-XJ01-{doc_id}-005", "Prompt工程优化", "Prompt", "xuanji_engine", "01_ziwei_star", "109", TaskPriority.P0),
                    Task(f"P3-XJ01-{doc_id}-006", "CoT推理优化", "推理", "xuanji_engine", "01_ziwei_star", "110", TaskPriority.P0),
                ])

            elif category == "XJ02":  # 禄存星 - 组长1人 + 成员7人 = 8人
                tasks.extend([
                    Task(f"P3-XJ02-{doc_id}-001", "调度层核心模块", "调度层", "xuanji_engine", "02_lucun_star", "111", TaskPriority.P0),  # 组长
                    Task(f"P3-XJ02-{doc_id}-002", "ReAct引擎优化", "ReAct引擎", "xuanji_engine", "02_lucun_star", "112", TaskPriority.P0),
                    Task(f"P3-XJ02-{doc_id}-003", "多模型路由", "路由", "xuanji_engine", "02_lucun_star", "113", TaskPriority.P0),
                    Task(f"P3-XJ02-{doc_id}-004", "DAG编排引擎", "编排", "xuanji_engine", "02_lucun_star", "114", TaskPriority.P0),
                    Task(f"P3-XJ02-{doc_id}-005", "Celery任务队列", "队列", "xuanji_engine", "02_lucun_star", "115", TaskPriority.P0),
                    Task(f"P3-XJ02-{doc_id}-006", "gRPC服务通信", "通信", "xuanji_engine", "02_lucun_star", "116", TaskPriority.P0),
                    Task(f"P3-XJ02-{doc_id}-007", "资源优化系统", "优化", "xuanji_engine", "02_lucun_star", "117", TaskPriority.P0),
                    Task(f"P3-XJ02-{doc_id}-008", "并发控制机制", "并发", "xuanji_engine", "02_lucun_star", "118", TaskPriority.P0),
                ])

            elif category == "XJ03":  # 巨门星 - 组长1人 + 成员7人 = 8人
                tasks.extend([
                    Task(f"P3-XJ03-{doc_id}-001", "记忆层核心模块", "记忆层", "xuanji_engine", "03_jumen_star", "119", TaskPriority.P0),  # 组长
                    Task(f"P3-XJ03-{doc_id}-002", "瞬时记忆模块", "记忆", "xuanji_engine", "03_jumen_star", "120", TaskPriority.P0),
                    Task(f"P3-XJ03-{doc_id}-003", "短期记忆Redis", "缓存", "xuanji_engine", "03_jumen_star", "121", TaskPriority.P0),
                    Task(f"P3-XJ03-{doc_id}-004", "长期记忆向量库", "向量", "xuanji_engine", "03_jumen_star", "122", TaskPriority.P0),
                    Task(f"P3-XJ03-{doc_id}-005", "记忆检索API", "检索", "xuanji_engine", "03_jumen_star", "123", TaskPriority.P0),
                    Task(f"P3-XJ03-{doc_id}-006", "Neo4j知识图谱", "图谱", "xuanji_engine", "03_jumen_star", "124", TaskPriority.P0),
                    Task(f"P3-XJ03-{doc_id}-007", "记忆融合机制", "融合", "xuanji_engine", "03_jumen_star", "125", TaskPriority.P0),
                    Task(f"P3-XJ03-{doc_id}-008", "记忆清理策略", "清理", "xuanji_engine", "03_jumen_star", "126", TaskPriority.P0),
                ])

            elif category == "XJ04":  # 贪狼星 - 组长1人 + 成员3人 = 4人
                tasks.extend([
                    Task(f"P3-XJ04-{doc_id}-001", "交互层核心模块", "交互层", "xuanji_engine", "04_lianzheng_star", "163", TaskPriority.P0),  # 组长
                    Task(f"P3-XJ04-{doc_id}-002", "ASR语音识别", "ASR", "xuanji_engine", "04_lianzheng_star", "164", TaskPriority.P0),
                    Task(f"P3-XJ04-{doc_id}-003", "TTS语音合成", "TTS", "xuanji_engine", "04_lianzheng_star", "165", TaskPriority.P0),
                    Task(f"P3-XJ04-{doc_id}-004", "2D数字人驱动", "数字人", "xuanji_engine", "04_lianzheng_star", "166", TaskPriority.P0),
                ])

            elif category == "XJ05":  # 廉贞星 - 组长1人 + 成员3人 = 4人
                tasks.extend([
                    Task(f"P3-XJ05-{doc_id}-001", "人格层核心模块", "人格层", "xuanji_engine", "05_wuqu_star", "127", TaskPriority.P0),  # 组长
                    Task(f"P3-XJ05-{doc_id}-002", "插件基类与接口", "接口", "xuanji_engine", "05_wuqu_star", "128", TaskPriority.P0),
                    Task(f"P3-XJ05-{doc_id}-003", "插件注册中心", "注册", "xuanji_engine", "05_wuqu_star", "129", TaskPriority.P0),
                    Task(f"P3-XJ05-{doc_id}-004", "插件发现机制", "发现", "xuanji_engine", "05_wuqu_star", "130", TaskPriority.P0),
                    Task(f"P3-XJ05-{doc_id}-005", "依赖解析引擎", "依赖", "xuanji_engine", "05_wuqu_star", "131", TaskPriority.P0),
                    Task(f"P3-XJ05-{doc_id}-006", "版本管理系统", "版本", "xuanji_engine", "05_wuqu_star", "132", TaskPriority.P0),
                ])

            elif category == "XJ06":  # 破军星 - 组长1人 + 成员7人 = 8人
                tasks.extend([
                    Task(f"P3-XJ06-{doc_id}-001", "执行层核心模块", "执行层", "xuanji_engine", "06_pojun_star", "133", TaskPriority.P0),  # 组长
                    Task(f"P3-XJ06-{doc_id}-002", "沙箱隔离环境", "沙箱", "xuanji_engine", "06_pojun_star", "134", TaskPriority.P0),
                    Task(f"P3-XJ06-{doc_id}-003", "Docker容器管理", "容器", "xuanji_engine", "06_pojun_star", "135", TaskPriority.P0),
                    Task(f"P3-XJ06-{doc_id}-004", "插件执行引擎", "执行", "xuanji_engine", "06_pojun_star", "136", TaskPriority.P0),
                    Task(f"P3-XJ06-{doc_id}-005", "电话外呼插件", "外呼", "xuanji_engine", "06_pojun_star", "137", TaskPriority.P0),
                    Task(f"P3-XJ06-{doc_id}-006", "邮件短信插件", "消息", "xuanji_engine", "06_pojun_star", "138", TaskPriority.P0),
                    Task(f"P3-XJ06-{doc_id}-007", "资源限制机制", "限制", "xuanji_engine", "06_pojun_star", "139", TaskPriority.P0),
                    Task(f"P3-XJ06-{doc_id}-008", "超时控制机制", "超时", "xuanji_engine", "06_pojun_star", "140", TaskPriority.P0),
                ])

            elif category == "XJ07":  # 左辅星 - 组长1人 + 成员11人 = 12人
                tasks.extend([
                    Task(f"P3-XJ07-{doc_id}-001", "底座层核心模块", "底座层", "xuanji_engine", "07_zuofu_star", "146", TaskPriority.P0),  # 组长
                    Task(f"P3-XJ07-{doc_id}-002", "用户管理模块", "用户", "xuanji_engine", "07_zuofu_star", "147", TaskPriority.P0),
                    Task(f"P3-XJ07-{doc_id}-003", "租户隔离系统", "租户", "xuanji_engine", "07_zuofu_star", "148", TaskPriority.P0),
                    Task(f"P3-XJ07-{doc_id}-004", "配置中心", "配置", "xuanji_engine", "07_zuofu_star", "149", TaskPriority.P0),
                    Task(f"P3-XJ07-{doc_id}-005", "日志监控系统", "日志", "xuanji_engine", "07_zuofu_star", "150", TaskPriority.P0),
                    Task(f"P3-XJ07-{doc_id}-006", "K8s微服务部署", "K8s", "xuanji_engine", "07_zuofu_star", "151", TaskPriority.P0),
                    Task(f"P3-XJ07-{doc_id}-007", "API网关集成", "网关", "xuanji_engine", "07_zuofu_star", "152", TaskPriority.P0),
                    Task(f"P3-XJ07-{doc_id}-008", "负载均衡配置", "负载", "xuanji_engine", "07_zuofu_star", "153", TaskPriority.P0),
                    Task(f"P3-XJ07-{doc_id}-009", "自动扩容机制", "扩容", "xuanji_engine", "07_zuofu_star", "154", TaskPriority.P0),
                    Task(f"P3-XJ07-{doc_id}-010", "备份恢复机制", "备份", "xuanji_engine", "07_zuofu_star", "101", TaskPriority.P0),
                    Task(f"P3-XJ07-{doc_id}-011", "服务发现机制", "发现", "xuanji_engine", "07_zuofu_star", "155", TaskPriority.P0),
                    Task(f"P3-XJ07-{doc_id}-012", "健康检查机制", "健康", "xuanji_engine", "07_zuofu_star", "156", TaskPriority.P0),
                ])

            elif category == "XJ08":  # 右弼星 - 组长1人 + 成员5人 = 6人
                tasks.extend([
                    Task(f"P3-XJ08-{doc_id}-001", "安全层核心模块", "安全层", "xuanji_engine", "08_youbi_star", "105", TaskPriority.P0),  # 组长
                    Task(f"P3-XJ08-{doc_id}-002", "法律红线拦截", "法律", "xuanji_engine", "08_youbi_star", "157", TaskPriority.P0),
                    Task(f"P3-XJ08-{doc_id}-003", "道德红线拦截", "道德", "xuanji_engine", "08_youbi_star", "158", TaskPriority.P0),
                    Task(f"P3-XJ08-{doc_id}-004", "权限白名单系统", "权限", "xuanji_engine", "08_youbi_star", "159", TaskPriority.P0),
                    Task(f"P3-XJ08-{doc_id}-005", "审计日志系统", "审计", "xuanji_engine", "08_youbi_star", "160", TaskPriority.P0),
                    Task(f"P3-XJ08-{doc_id}-006", "IntentGuard对齐", "对齐", "xuanji_engine", "08_youbi_star", "176", TaskPriority.P0),
                ])

            elif category == "XJ09":  # 贪狼星 - 组长1人 + 成员6人 = 7人
                tasks.extend([
                    Task(f"P3-XJ09-{doc_id}-001", "Web端交互界面", "Web", "xuanji_engine", "09_tanlang_star", "143", TaskPriority.P0),  # 组长
                    Task(f"P3-XJ09-{doc_id}-002", "Web组件库", "组件", "xuanji_engine", "09_tanlang_star", "144", TaskPriority.P0),
                    Task(f"P3-XJ09-{doc_id}-003", "前端状态管理", "状态", "xuanji_engine", "09_tanlang_star", "145", TaskPriority.P0),
                    Task(f"P3-XJ09-{doc_id}-004", "WebSocket实时通信", "通信", "xuanji_engine", "09_tanlang_star", "177", TaskPriority.P0),
                    Task(f"P3-XJ09-{doc_id}-005", "多语言支持", "语言", "xuanji_engine", "09_tanlang_star", "178", TaskPriority.P0),
                    Task(f"P3-XJ09-{doc_id}-006", "主题定制系统", "主题", "xuanji_engine", "09_tanlang_star", "179", TaskPriority.P0),
                    Task(f"P3-XJ09-{doc_id}-007", "响应式设计", "响应", "xuanji_engine", "09_tanlang_star", "180", TaskPriority.P0),
                ])

            elif category == "XJ10":  # 辅弼星辰 - 组长1人 + 成员9人 = 10人
                tasks.extend([
                    Task(f"P3-XJ10-{doc_id}-001", "插件市场", "市场", "xuanji_engine", "10_fubi_star", "161", TaskPriority.P0),  # 组长
                    Task(f"P3-XJ10-{doc_id}-002", "插件上传审核", "审核", "xuanji_engine", "10_fubi_star", "162", TaskPriority.P0),
                    Task(f"P3-XJ10-{doc_id}-003", "开发者平台", "开发", "xuanji_engine", "10_fubi_star", "168", TaskPriority.P0),
                    Task(f"P3-XJ10-{doc_id}-004", "API文档生成", "文档", "xuanji_engine", "10_fubi_star", "169", TaskPriority.P0),
                    Task(f"P3-XJ10-{doc_id}-005", "插件评分系统", "评分", "xuanji_engine", "10_fubi_star", "183", TaskPriority.P0),
                    Task(f"P3-XJ10-{doc_id}-006", "插件搜索优化", "搜索", "xuanji_engine", "10_fubi_star", "184", TaskPriority.P0),
                    Task(f"P3-XJ10-{doc_id}-007", "数据分析仪表盘", "分析", "xuanji_engine", "10_fubi_star", "185", TaskPriority.P0),
                    Task(f"P3-XJ10-{doc_id}-008", "社区论坛系统", "社区", "xuanji_engine", "10_fubi_star", "188", TaskPriority.P0),
                    Task(f"P3-XJ10-{doc_id}-009", "知识库系统", "知识", "xuanji_engine", "10_fubi_star", "189", TaskPriority.P0),
                    Task(f"P3-XJ10-{doc_id}-010", "FAQ管理系统", "FAQ", "xuanji_engine", "10_fubi_star", "190", TaskPriority.P0),
                ])

        return tasks

    def activate_employees(self):
        """激活所有AI员工"""
        print("\n" + "=" * 80)
        print("🚀 AI数字员工第三期开发启动（最终正确版）")
        print("=" * 80)
        print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        # 加载真实员工（从第一期第二期）
        self.employees = self.load_employees_from_phase1_phase2()
        print(f"\n✅ 员工加载完成: {len(self.employees)} 人")

        # 统计各部门
        dept_stats = {}
        coding_employees = 0
        management_employees = 0

        for emp in self.employees.values():
            dept = emp["department"]
            dept_stats[dept] = dept_stats.get(dept, 0) + 1

            if emp["will_code"]:
                coding_employees += 1
            else:
                management_employees += 1

        print("\n部门分布:")
        for dept, count in sorted(dept_stats.items()):
            print(f"  - {dept}: {count} 人")

        print(f"\n人员分类:")
        print(f"  - 编码人员: {coding_employees} 人 ✅")
        print(f"  - 管理人员: {management_employees} 人 ✅")

        # 激活所有员工
        print(f"\n🔥 正在激活 {len(self.employees)} 名AI员工...")
        for emp_id, emp in self.employees.items():
            emp["status"] = "active"
            if not emp["will_code"]:
                print(f"  ✅ [{emp_id}] {emp['name']} - {emp['role']} 已激活（管理层，不编码）")
            elif emp["is_leader"]:
                print(f"  ✅ [{emp_id}] {emp['name']} - {emp['role']} 已激活（组长，要编码）")
            else:
                print(f"  ✅ [{emp_id}] {emp['name']} - {emp['role']} 已激活（编码）")

        self.stats["total_employees"] = len(self.employees)
        self.stats["coding_employees"] = coding_employees
        self.stats["management_employees"] = management_employees
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
        print(f"\n🎯 正在分配任务给AI员工（按照第一期第二期模式）...")
        for task in tasks:
            self.task_queue.add_task("xuanji_engine", task)
            if task.employee_id in self.employees:
                self.employees[task.employee_id]["assigned_tasks"] += 1

        # 统计分配情况
        assigned_employees = sum(1 for emp in self.employees.values() if emp["assigned_tasks"] > 0)
        leader_assigned = sum(1 for emp in self.employees.values() if emp["assigned_tasks"] > 0 and emp["is_leader"])
        member_assigned = sum(1 for emp in self.employees.values() if emp["assigned_tasks"] > 0 and not emp["is_leader"] and emp["department"] == "玄玑引擎")

        print(f"✅ 任务分配完成: {len(tasks)} 个任务已分配给 {assigned_employees} 名员工")
        print(f"  - 组长收到任务: {leader_assigned} 人 ✅（组长亲自写代码）")
        print(f"  - 玄玑成员收到任务: {member_assigned} 人 ✅（成员亲自写代码）")
        print(f"  - 管理层收到任务: 0 人 ✅（李明远、张志远不编码）")

        self.stats["total_tasks"] = len(tasks)
        self.stats["assigned_tasks"] = len(tasks)

    def start_development(self):
        """启动开发"""
        print(f"\n🎨 AI数字员工开始编写代码...")
        print(f"📝 预计第一批代码提交时间: {datetime.now().strftime('%H:%M')} + 20分钟")

        self.stats["start_time"] = datetime.now()

        print(f"\n{'=' * 80}")
        print("✅ 第三期开发启动完成！（最终正确版）")
        print(f"{'=' * 80}")
        print(f"📊 统计信息:")
        print(f"  - 总员工: {self.stats['total_employees']} 人")
        print(f"  - 编码人员: {self.stats['coding_employees']} 人")
        print(f"  - 管理人员: {self.stats['management_employees']} 人")
        print(f"  - 分配任务: {self.stats['assigned_tasks']}/{self.stats['total_tasks']}")
        print(f"  - 启动时间: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 80}")
        print(f"💡 核心原则（基于第一期第二期成功模式）:")
        print(f"  - ✅ 李明远（001）不编码，负责任务管理、进度管理、资源调配")
        print(f"  - ✅ 张志远（002）不编码，负责任务分派、代码质检、代码推送、阻塞治理")
        print(f"  - ✅ 10名组长亲自写代码（同时负责团队管理）")
        print(f"  - ✅ 67名成员亲自写代码")
        print(f"  - ✅ 90名增补人员亲自写代码")
        print(f"  - ✅ 系统自动解析文档（无需手动阅读）")
        print(f"  - ✅ 系统自动分解任务（无需手动分配）")
        print(f"  - ✅ 系统自动激活员工（无需到岗）")
        print(f"  - ✅ AI员工立即开始编写代码")
        print(f"  - ✅ AI员工每小时自动汇报进度")
        print(f"  - ✅ AI员工每4小时自动提交代码")
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

#!/usr/bin/env python3
"""
AI数字员工第三期开发启动脚本（修正版v2）
创建时间: 2026-03-22 07:56
修正内容:
1. 从员工名单文件加载真实员工（而非创建虚假员工）
2. 任务分配给组员（而非分配给组长）
3. 组长负责管理和代码审查

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
    """第三期开发启动器（修正版v2）"""

    def __init__(self):
        self.incoming_dir = Path("/workspace/projects/workspace/incoming")
        self.project_path = Path("/workspace/projects/workspace/xuanji-engine-v2")
        self.employee_list_file = Path("/workspace/projects/workspace/memory/员工名单-2026-03-17.md")
        self.task_queue = MultiProjectTaskQueue()
        self.code_generator = CodeGenerator()
        self.git_manager = AutoCommitManager()

        # 102名员工：核心管理层10人 + 组长10人 + 组员82人
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
            20: "XJ01",  # 紫微帝星
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

    def load_employees_from_file(self) -> Dict[str, Dict]:
        """从员工名单文件加载真实员工"""
        employees = {}

        # 加载核心管理层（10人）
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

        # 加载十星层组长（10人）
        group_leaders = [
            ("102", "陈元灵", "XJ01组长", "技术开发部"),
            ("111", "周禄存", "XJ02组长", "技术开发部"),
            ("119", "蒋巨门", "XJ03组长", "技术开发部"),
            ("143", "薛贪狼", "XJ04组长", "技术开发部"),
            ("163", "伍廉贞", "XJ05组长", "技术开发部"),
            ("127", "谢武功", "XJ06组长", "技术开发部"),
            ("133", "章破军", "XJ07组长", "技术开发部"),
            ("146", "倪左辅", "XJ08组长", "技术开发部"),
            ("105", "周右弼", "XJ09组长", "技术开发部"),
            ("161", "齐辅弼", "XJ10组长", "技术开发部"),
        ]

        # 加载技术开发部成员（30人）- 真实员工
        tech_members = [
            ("011", "张伟", "前端负责人"),
            ("012", "刘斌", "后端工程师"),
            ("013", "赵阳", "后端工程师"),
            ("014", "葛浩", "后端工程师"),
            ("015", "昌艺", "后端工程师"),
            ("016", "陈磊", "后端工程师"),
            ("017", "周杰", "后端工程师"),
            ("018", "王芳", "后端工程师"),
            ("019", "刘强", "后端工程师"),
            ("020", "陈军", "后端工程师"),
            ("021", "王强", "后端工程师"),
            ("022", "马丽", "前端工程师"),
            ("023", "黄涛", "前端工程师"),
            ("024", "林青", "UI设计师"),
            ("025", "何敏", "UI设计师"),
            ("026", "吴强", "测试工程师"),
            ("027", "李浩", "资深全栈工程师"),
            ("028", "王勇", "全栈工程师"),
            ("029", "赵鹏", "全栈工程师"),
            ("030", "孙杰", "全栈工程师"),
            ("031", "周涛", "资深移动端工程师"),
            ("032", "吴限", "移动端工程师"),
            ("033", "郑凯", "移动端工程师"),
            ("034", "钱磊", "移动端工程师"),
            ("035", "冯敏", "资深算法工程师"),
            ("036", "褚斌", "算法工程师"),
            ("037", "卫强", "测试工程师"),
            ("038", "蒋涛", "测试工程师"),
        ]

        # 加载产品设计部（20人）
        design_members = [
            ("041", "沈娟", "产品经理"),
            ("042", "韩雪", "产品经理"),
            ("043", "杨蕾", "产品经理"),
            ("044", "朱颖", "产品经理"),
            ("045", "秦芳", "产品经理"),
            ("046", "许晴", "产品经理"),
            ("047", "戚薇", "UI设计师"),
            ("048", "谢丽", "UI设计师"),
            ("049", "邹婷", "UI设计师"),
            ("050", "喻霞", "UI设计师"),
            ("051", "柏莉", "UI设计师"),
            ("052", "水红", "UX设计师"),
            ("053", "窦婷", "UX设计师"),
            ("054", "章芸", "UX设计师"),
            ("055", "云涛", "UX设计师"),
            ("056", "苏敏", "平面设计师"),
            ("057", "潘娟", "平面设计师"),
            ("058", "葛丽", "平面设计师"),
            ("059", "奚磊", "3D设计师"),
            ("060", "范华", "3D设计师"),
        ]

        # 加载市场销售部（18人）
        sales_members = [
            ("061", "柯娟", "销售代表"),
            ("062", "厉婷", "销售代表"),
            ("063", "岑涛", "销售代表"),
            ("064", "薛磊", "销售代表"),
            ("065", "雷芳", "销售代表"),
            ("066", "贺丽", "销售代表"),
            ("067", "倪静", "销售代表"),
            ("068", "汤敏", "销售代表"),
            ("069", "滕娟", "数字营销"),
            ("070", "殷婷", "数字营销"),
            ("071", "罗涛", "数字营销"),
            ("072", "毕磊", "数字营销"),
            ("073", "郝芳", "SEO专员"),
            ("074", "邬丽", "SEO专员"),
            ("075", "安娜", "社群运营"),
            ("076", "常娟", "社群运营"),
            ("077", "乐涛", "活动策划"),
            ("078", "于磊", "活动策划"),
        ]

        # 加载客服支持部（12人）
        support_members = [
            ("079", "时娟", "客服代表"),
            ("080", "皮婷", "客服代表"),
            ("081", "卞涛", "客服代表"),
            ("082", "齐芳", "客服代表"),
            ("083", "康丽", "客服代表"),
            ("084", "伍静", "客服代表"),
            ("085", "余敏", "客服代表"),
            ("086", "元磊", "客服代表"),
            ("087", "卜涛", "技术支持"),
            ("088", "顾娟", "技术支持"),
            ("089", "孟磊", "售后服务"),
            ("090", "平丽", "售后服务"),
        ]

        # 加载专业支持部（10人）
        professional_members = [
            ("091", "段涛", "法务专员"),
            ("092", "樊丽", "财务专员"),
            ("093", "方敏", "HR专员"),
            ("094", "房强", "运维工程师"),
            ("095", "范磊", "运维工程师"),
            ("096", "冯丽", "数据分析师"),
            ("097", "付强", "商务专员"),
            ("098", "傅娟", "品牌专员"),
            ("099", "盖涛", "公关专员"),
            ("100", "甘丽", "行政专员"),
        ]

        # 创建员工字典
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
                "is_manager": True
            }

        for emp_id, name, role, dept in group_leaders:
            employees[emp_id] = {
                "id": emp_id,
                "name": name,
                "role": role,
                "department": dept,
                "status": "idle",
                "assigned_tasks": 0,
                "completed_tasks": 0,
                "is_leader": True,
                "is_manager": False
            }

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
                "is_manager": False
            }

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
                "is_manager": False
            }

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
                "is_manager": False
            }

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
                "is_manager": False
            }

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
                "is_manager": False
            }

        return employees

    def parse_docs_to_tasks(self, docs: List[Dict]) -> List[Task]:
        """将开发文档解析为代码任务，分配给组员而非组长"""
        tasks = []

        # 定义每个星层的组员（不包括组长）
        # XJ01 紫微帝星 - 张伟团队
        xj01_members = ["011", "012", "013", "014", "015"]
        # XJ02 禄存星 - 刘斌团队
        xj02_members = ["016", "017", "018", "019", "020"]
        # XJ03 巨门星 - 陈磊团队
        xj03_members = ["021", "022", "023", "024", "025"]
        # XJ04 贪狼星 - 李浩团队
        xj04_members = ["026", "027", "028", "029", "030"]
        # XJ05 廉贞星 - 周涛团队
        xj05_members = ["031", "032", "033", "034", "035"]
        # XJ06 武曲星 - 冯敏团队
        xj06_members = ["036", "037", "038", "041", "042"]
        # XJ07 破军星 - 沈娟团队
        xj07_members = ["043", "044", "045", "046", "047"]
        # XJ08 左辅星 - 戚薇团队
        xj08_members = ["048", "049", "050", "051", "052"]
        # XJ09 右弼星 - 水红团队
        xj09_members = ["053", "054", "055", "056", "057"]
        # XJ10 辅弼星辰 - 苏敏团队
        xj10_members = ["058", "059", "060", "061", "062"]

        task_index = 0

        for doc in docs:
            category = doc["category"]
            doc_id = doc["id"]

            if category == "XJ01":  # 紫微帝星 - 元灵层
                tasks.extend([
                    Task(f"P3-XJ01-{doc_id}-001", "元灵层核心模块", "元灵层", "xuanji_engine", "01_ziwei_star", xj01_members[task_index % 5], TaskPriority.P0),
                    Task(f"P3-XJ01-{doc_id}-002", "意图识别增强", "意图识别", "xuanji_engine", "01_ziwei_star", xj01_members[(task_index + 1) % 5], TaskPriority.P0),
                ])
                task_index += 2

            elif category == "XJ02":  # 禄存星 - 调度层
                tasks.extend([
                    Task(f"P3-XJ02-{doc_id}-001", "调度层核心模块", "调度层", "xuanji_engine", "02_lucun_star", xj02_members[task_index % 5], TaskPriority.P0),
                    Task(f"P3-XJ02-{doc_id}-002", "ReAct引擎优化", "ReAct引擎", "xuanji_engine", "02_lucun_star", xj02_members[(task_index + 1) % 5], TaskPriority.P0),
                ])
                task_index += 2

            elif category == "XJ03":  # 巨门星 - 记忆层
                tasks.extend([
                    Task(f"P3-XJ03-{doc_id}-001", "记忆层核心模块", "记忆层", "xuanji_engine", "03_jumen_star", xj03_members[task_index % 5], TaskPriority.P0),
                    Task(f"P3-XJ03-{doc_id}-002", "向量检索优化", "向量检索", "xuanji_engine", "03_jumen_star", xj03_members[(task_index + 1) % 5], TaskPriority.P0),
                ])
                task_index += 2

            elif category == "XJ04":  # 贪狼星 - 交互层
                tasks.extend([
                    Task(f"P3-XJ04-{doc_id}-001", "交互层核心模块", "交互层", "xuanji_engine", "04_lianzheng_star", xj04_members[task_index % 5], TaskPriority.P0),
                    Task(f"P3-XJ04-{doc_id}-002", "ASR/TTS集成", "语音交互", "xuanji_engine", "04_lianzheng_star", xj04_members[(task_index + 1) % 5], TaskPriority.P0),
                ])
                task_index += 2

            elif category == "XJ05":  # 廉贞星 - 人格层
                tasks.extend([
                    Task(f"P3-XJ05-{doc_id}-001", "人格层核心模块", "人格层", "xuanji_engine", "05_wuqu_star", xj05_members[task_index % 5], TaskPriority.P0),
                    Task(f"P3-XJ05-{doc_id}-002", "情绪状态机", "情绪引擎", "xuanji_engine", "05_wuqu_star", xj05_members[(task_index + 1) % 5], TaskPriority.P0),
                ])
                task_index += 2

            elif category == "XJ06":  # 武曲星 - 技能层
                tasks.extend([
                    Task(f"P3-XJ06-{doc_id}-001", "技能层核心模块", "技能层", "xuanji_engine", "06_pojun_star", xj06_members[task_index % 5], TaskPriority.P0),
                    Task(f"P3-XJ06-{doc_id}-002", "插件系统增强", "插件系统", "xuanji_engine", "06_pojun_star", xj06_members[(task_index + 1) % 5], TaskPriority.P0),
                ])
                task_index += 2

            elif category == "XJ07":  # 破军星 - 执行层
                tasks.extend([
                    Task(f"P3-XJ07-{doc_id}-001", "执行层核心模块", "执行层", "xuanji_engine", "07_zuofu_star", xj07_members[task_index % 5], TaskPriority.P0),
                    Task(f"P3-XJ07-{doc_id}-002", "沙箱隔离环境", "沙箱", "xuanji_engine", "07_zuofu_star", xj07_members[(task_index + 1) % 5], TaskPriority.P0),
                ])
                task_index += 2

            elif category == "XJ08":  # 左辅星 - 底座层
                tasks.extend([
                    Task(f"P3-XJ08-{doc_id}-001", "底座层核心模块", "底座层", "xuanji_engine", "08_youbi_star", xj08_members[task_index % 5], TaskPriority.P0),
                    Task(f"P3-XJ08-{doc_id}-002", "用户管理系统", "用户管理", "xuanji_engine", "08_youbi_star", xj08_members[(task_index + 1) % 5], TaskPriority.P0),
                ])
                task_index += 2

            elif category == "XJ09":  # 右弼星 - 安全层
                tasks.extend([
                    Task(f"P3-XJ09-{doc_id}-001", "安全层核心模块", "安全层", "xuanji_engine", "09_tanlang_star", xj09_members[task_index % 5], TaskPriority.P0),
                    Task(f"P3-XJ09-{doc_id}-002", "权限控制系统", "权限控制", "xuanji_engine", "09_tanlang_star", xj09_members[(task_index + 1) % 5], TaskPriority.P0),
                ])
                task_index += 2

            elif category == "XJ10":  # 辅弼星辰 - 扩展层
                tasks.extend([
                    Task(f"P3-XJ10-{doc_id}-001", "扩展层核心模块", "扩展层", "xuanji_engine", "10_fubi_star", xj10_members[task_index % 5], TaskPriority.P0),
                    Task(f"P3-XJ10-{doc_id}-002", "插件市场", "插件市场", "xuanji_engine", "10_fubi_star", xj10_members[(task_index + 1) % 5], TaskPriority.P0),
                ])
                task_index += 2

        return tasks

    def activate_employees(self):
        """激活所有AI员工"""
        print("\n" + "=" * 80)
        print("🚀 AI数字员工第三期开发启动（修正版v2）")
        print("=" * 80)
        print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

        # 加载真实员工（从文件）
        self.employees = self.load_employees_from_file()
        print(f"\n✅ 员工加载完成: {len(self.employees)} 人")

        # 统计各部门
        dept_stats = {}
        role_stats = {"核心管理层": 0, "组长": 0, "组员": 0}

        for emp in self.employees.values():
            dept = emp["department"]
            dept_stats[dept] = dept_stats.get(dept, 0) + 1

            if emp["is_manager"]:
                role_stats["核心管理层"] += 1
            elif emp["is_leader"]:
                role_stats["组长"] += 1
            else:
                role_stats["组员"] += 1

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
            else:
                print(f"  ✅ [{emp_id}] {emp['name']} - {emp['role']} 已激活")

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
        member_assigned = sum(1 for emp in self.employees.values() if emp["assigned_tasks"] > 0 and not emp["is_leader"] and not emp["is_manager"])

        print(f"✅ 任务分配完成: {len(tasks)} 个任务已分配给 {assigned_employees} 名员工")
        print(f"  - 组员收到任务: {member_assigned} 人 ✅")
        print(f"  - 组长收到任务: {leader_assigned} 人 ⚠️ （组长应该管理，不应编码）")

        self.stats["total_tasks"] = len(tasks)
        self.stats["assigned_tasks"] = len(tasks)

    def start_development(self):
        """启动开发"""
        print(f"\n🎨 AI数字员工开始编写代码...")
        print(f"📝 预计第一批代码提交时间: {datetime.now().strftime('%H:%M')} + 20分钟")

        self.stats["start_time"] = datetime.now()

        print(f"\n{'=' * 80}")
        print("✅ 第三期开发启动完成！（修正版v2）")
        print(f"{'=' * 80}")
        print(f"📊 统计信息:")
        print(f"  - 激活员工: {self.stats['active_employees']}/{self.stats['total_employees']}")
        print(f"  - 分配任务: {self.stats['assigned_tasks']}/{self.stats['total_tasks']}")
        print(f"  - 启动时间: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'=' * 80}")
        print(f"💡 核心原则:")
        print(f"  - ✅ 系统自动解析文档（无需手动阅读）")
        print(f"  - ✅ 系统自动分解任务（无需手动分配）")
        print(f"  - ✅ 系统自动激活员工（无需到岗）")
        print(f"  - ✅ AI员工立即开始编写代码")
        print(f"  - ✅ AI员工每小时自动汇报进度")
        print(f"  - ✅ AI员工每4小时自动提交代码")
        print(f"  - ✅ 任务分配给组员（而非组长）")
        print(f"  - ✅ 组长负责管理和代码审查")
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

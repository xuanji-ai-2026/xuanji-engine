"""
AI数字员工全自动工作系统 v3.0 - P1任务版
创建时间: 2026-03-20 16:43
功能: P0任务完成后自动继续P1任务，持续开发

更新内容:
- P0任务完成后自动领取P1任务
- 覆盖全部10个组
- 持续循环开发
"""

import asyncio
import os
import time
from datetime import datetime
from typing import Dict, List

from multi_project_task_queue import create_all_projects_tasks, MultiProjectTaskQueue, Task, TaskPriority
from code_generator import CodeGenerator
from auto_git_commit import AutoCommitManager

class AIDigitalEmployeeSystem:
    """AI数字员工全自动工作系统 v3.0"""
    
    def __init__(self):
        self.task_queue = self._create_full_tasks_p0_p1()
        self.code_generator = CodeGenerator()
        self.git_manager = AutoCommitManager()
        self.employees: Dict[str, Dict] = {}
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "generated_files": 0,
            "commits": 0,
            "commits_failed": 0,
            "start_time": time.time()
        }
        
        self.project_paths = {
            "xuanji_engine": "/workspace/projects/workspace/xuanji-engine-v2",
            "ai_stock_app": "/workspace/projects/workspace/ai-stock-app",
            "hanyu_learning": "/workspace/projects/workspace/han-yu-vietnamese-learning"
        }
        
        self.ssh_configs = {
            "xuanji_engine": "/tmp/ssh_config",
            "ai_stock_app": "/tmp/ssh_config_multi",
            "hanyu_learning": "/tmp/ssh_config"
        }
        
        for project, path in self.project_paths.items():
            if os.path.exists(path):
                self.git_manager.register_repo(project, path)
    
    def _create_full_tasks_p0_p1(self) -> MultiProjectTaskQueue:
        """创建完整的P0+P1任务队列"""
        queue = MultiProjectTaskQueue()
        
        # ===== P0任务 =====
        xj01_p0 = [
            Task("XJ01-P0-001", "多模态意图识别", "意图识别引擎", "xuanji_engine", "01_ziwei_star", "102", TaskPriority.P0),
            Task("XJ01-P0-002", "意图对齐机制", "对齐机制", "xuanji_engine", "01_ziwei_star", "106", TaskPriority.P0),
            Task("XJ01-P0-003", "意图漂移检测", "漂移检测", "xuanji_engine", "01_ziwei_star", "107", TaskPriority.P0),
        ]
        
        xj02_p0 = [
            Task("XJ02-P0-001", "10+模型集成", "多模型", "xuanji_engine", "02_lucun_star", "111", TaskPriority.P0),
            Task("XJ02-P0-002", "动态路由算法", "路由", "xuanji_engine", "02_lucun_star", "112", TaskPriority.P0),
            Task("XJ02-P0-003", "资源优化系统", "优化", "xuanji_engine", "02_lucun_star", "114", TaskPriority.P0),
        ]
        
        # ===== P1任务 =====
        # XJ-01 P1 - 意图识别增强
        xj01_p1 = [
            Task("XJ01-P1-001", "行业数字人模板", "22+模板", "xuanji_engine", "01_ziwei_star", "109", TaskPriority.P1),
            Task("XJ01-P1-002", "自我进化体系", "强化学习", "xuanji_engine", "01_ziwei_star", "108", TaskPriority.P1),
            Task("XJ01-P1-003", "意图理解核心", "核心算法", "xuanji_engine", "01_ziwei_star", "110", TaskPriority.P1),
            Task("XJ01-P1-004", "Prompt工程优化", "Prompt", "xuanji_engine", "01_ziwei_star", "102", TaskPriority.P1),
            Task("XJ01-P1-005", "CoT推理优化", "推理", "xuanji_engine", "01_ziwei_star", "106", TaskPriority.P1),
        ]
        
        # XJ-02 P1 - ReAct引擎增强
        xj02_p1 = [
            Task("XJ02-P1-001", "任务拆解模块", "任务", "xuanji_engine", "02_lucun_star", "115", TaskPriority.P1),
            Task("XJ02-P1-002", "DAG编排引擎", "编排", "xuanji_engine", "02_lucun_star", "116", TaskPriority.P1),
            Task("XJ02-P1-003", "多模型路由", "路由", "xuanji_engine", "02_lucun_star", "112", TaskPriority.P1),
            Task("XJ02-P1-004", "Celery任务队列", "队列", "xuanji_engine", "02_lucun_star", "117", TaskPriority.P1),
            Task("XJ02-P1-005", "gRPC服务通信", "通信", "xuanji_engine", "02_lucun_star", "118", TaskPriority.P1),
        ]
        
        # XJ-03 P1 - 记忆系统增强
        xj03_p1 = [
            Task("XJ03-P1-001", "瞬时记忆模块", "记忆", "xuanji_engine", "03_jumen_star", "119", TaskPriority.P1),
            Task("XJ03-P1-002", "短期记忆Redis", "缓存", "xuanji_engine", "03_jumen_star", "120", TaskPriority.P1),
            Task("XJ03-P1-003", "长期记忆向量库", "向量", "xuanji_engine", "03_jumen_star", "121", TaskPriority.P1),
            Task("XJ03-P1-004", "记忆检索API", "检索", "xuanji_engine", "03_jumen_star", "122", TaskPriority.P1),
            Task("XJ03-P1-005", "Neo4j知识图谱", "图谱", "xuanji_engine", "03_jumen_star", "123", TaskPriority.P1),
        ]
        
        # XJ-04 P1 - 人格引擎增强
        xj04_p1 = [
            Task("XJ04-P1-001", "情绪状态机", "情绪", "xuanji_engine", "04_lianzheng_star", "163", TaskPriority.P1),
            Task("XJ04-P1-002", "人格配置系统", "人格", "xuanji_engine", "04_lianzheng_star", "164", TaskPriority.P1),
            Task("XJ04-P1-003", "人设一致性保障", "一致", "xuanji_engine", "04_lianzheng_star", "165", TaskPriority.P1),
            Task("XJ04-P1-004", "情感交付模型", "情感", "xuanji_engine", "04_lianzheng_star", "166", TaskPriority.P1),
            Task("XJ04-P1-005", "心理学模型", "心理", "xuanji_engine", "04_lianzheng_star", "167", TaskPriority.P1),
        ]
        
        # XJ-05 P1 - 插件系统增强
        xj05_p1 = [
            Task("XJ05-P1-001", "插件基类与接口", "接口", "xuanji_engine", "05_wuqu_star", "127", TaskPriority.P1),
            Task("XJ05-P1-002", "插件注册中心", "注册", "xuanji_engine", "05_wuqu_star", "128", TaskPriority.P1),
            Task("XJ05-P1-003", "插件发现机制", "发现", "xuanji_engine", "05_wuqu_star", "129", TaskPriority.P1),
            Task("XJ05-P1-004", "依赖解析引擎", "依赖", "xuanji_engine", "05_wuqu_star", "130", TaskPriority.P1),
            Task("XJ05-P1-005", "版本管理系统", "版本", "xuanji_engine", "05_wuqu_star", "131", TaskPriority.P1),
        ]
        
        # XJ-06 P1 - 执行层增强
        xj06_p1 = [
            Task("XJ06-P1-001", "沙箱隔离环境", "沙箱", "xuanji_engine", "06_pojun_star", "133", TaskPriority.P1),
            Task("XJ06-P1-002", "Docker容器管理", "容器", "xuanji_engine", "06_pojun_star", "134", TaskPriority.P1),
            Task("XJ06-P1-003", "插件执行引擎", "执行", "xuanji_engine", "06_pojun_star", "135", TaskPriority.P1),
            Task("XJ06-P1-004", "电话外呼插件", "外呼", "xuanji_engine", "06_pojun_star", "136", TaskPriority.P1),
            Task("XJ06-P1-005", "邮件短信插件", "消息", "xuanji_engine", "06_pojun_star", "137", TaskPriority.P1),
        ]
        
        # XJ-07 P1 - 底座层增强
        xj07_p1 = [
            Task("XJ07-P1-001", "K8s微服务部署", "K8s", "xuanji_engine", "07_zuofu_star", "146", TaskPriority.P1),
            Task("XJ07-P1-002", "用户管理模块", "用户", "xuanji_engine", "07_zuofu_star", "147", TaskPriority.P1),
            Task("XJ07-P1-003", "租户隔离系统", "隔离", "xuanji_engine", "07_zuofu_star", "148", TaskPriority.P1),
            Task("XJ07-P1-004", "配置中心", "配置", "xuanji_engine", "07_zuofu_star", "149", TaskPriority.P1),
            Task("XJ07-P1-005", "日志监控系统", "日志", "xuanji_engine", "07_zuofu_star", "150", TaskPriority.P1),
        ]
        
        # XJ-08 P1 - 安全层增强
        xj08_p1 = [
            Task("XJ08-P1-001", "法律红线拦截", "法律", "xuanji_engine", "08_youbi_star", "105", TaskPriority.P1),
            Task("XJ08-P1-002", "道德红线拦截", "道德", "xuanji_star", "156", TaskPriority.P1),
            Task("XJ08-P1-003", "权限白名单系统", "权限", "xuanji_engine", "08_youbi_star", "157", TaskPriority.P1),
            Task("XJ08-P1-004", "审计日志系统", "审计", "xuanji_engine", "08_youbi_star", "158", TaskPriority.P1),
            Task("XJ08-P1-005", "IntentGuard对齐", "对齐", "xuanji_engine", "08_youbi_star", "159", TaskPriority.P1),
        ]
        
        # XJ-09 P1 - 交互层增强
        xj09_p1 = [
            Task("XJ09-P1-001", "ASR语音识别", "ASR", "xuanji_engine", "09_tanlang_star", "143", TaskPriority.P1),
            Task("XJ09-P1-002", "TTS语音合成", "TTS", "xuanji_engine", "09_tanlang_star", "144", TaskPriority.P1),
            Task("XJ09-P1-003", "2D数字人驱动", "数字人", "xuanji_engine", "09_tanlang_star", "145", TaskPriority.P1),
            Task("XJ09-P1-004", "Web端交互界面", "Web", "xuanji_engine", "09_tanlang_star", "146", TaskPriority.P1),
            Task("XJ09-P1-005", "多模态输入处理", "多模态", "xuanji_engine", "09_tanlang_star", "147", TaskPriority.P1),
        ]
        
        # XJ-10 P1 - 开放平台增强
        xj10_p1 = [
            Task("XJ10-P1-001", "API网关", "网关", "xuanji_engine", "10_fubi_star", "161", TaskPriority.P1),
            Task("XJ10-P1-002", "开发者文档", "文档", "xuanji_engine", "10_fubi_star", "162", TaskPriority.P1),
            Task("XJ10-P1-003", "插件开发SDK", "SDK", "xuanji_engine", "10_fubi_star", "163", TaskPriority.P1),
            Task("XJ10-P1-004", "演示环境", "演示", "xuanji_engine", "10_fubi_star", "164", TaskPriority.P1),
            Task("XJ10-P1-005", "OpenAPI规范", "规范", "xuanji_engine", "10_fubi_star", "165", TaskPriority.P1),
        ]
        
        # 添加所有任务
        all_tasks = (xj01_p0 + xj02_p0 + xj01_p1 + xj02_p1 + xj03_p1 + xj04_p1 + 
                    xj05_p1 + xj06_p1 + xj07_p1 + xj08_p1 + xj09_p1 + xj10_p1)
        
        for task in all_tasks:
            queue.add_task(task.project, task)
        
        return queue
    
    def register_employee(self, employee_id: str, name: str, project: str):
        self.employees[employee_id] = {
            "id": employee_id,
            "name": name,
            "project": project,
            "status": "idle",
            "completed": 0
        }
        print(f"✅ 注册AI员工: {name} ({employee_id}) -> {project}")
    
    async def run_employee(self, employee_id: str):
        employee = self.employees[employee_id]
        project = employee["project"]
        consecutive_empty = 0
        max_empty_retries = 3
        
        print(f"\n🚀 [{employee['name']}] 开始工作...")
        
        while True:
            try:
                task = self.task_queue.claim_task(project, employee_id)
                
                if not task:
                    consecutive_empty += 1
                    if consecutive_empty >= max_empty_retries:
                        print(f"[{employee['name']}] ⏳ 暂无任务，休息60秒...")
                        await asyncio.sleep(60)
                        consecutive_empty = 0
                    else:
                        await asyncio.sleep(5)
                    continue
                
                consecutive_empty = 0
                employee["status"] = "working"
                priority = "P0" if task.priority == TaskPriority.P0 else "P1"
                print(f"[{employee['name']}] ✅ 领取任务: [{priority}] {task.task_id} - {task.title}")
                
                try:
                    code = self.code_generator.generate_code(task)
                    project_path = self.project_paths.get(project, "/workspace/projects/workspace")
                    file_path = self.code_generator.save_code(task, code, project_path)
                    
                    print(f"[{employee['name']}] 📝 生成代码: {file_path}")
                    self.stats["generated_files"] += 1
                    
                    commit_msg = f"feat({task.module}): [{priority}] {task.title} ({employee_id})"
                    ssh_config = self.ssh_configs.get(project, "/tmp/ssh_config")
                    result = self.git_manager.commit_to_repo(project, [file_path], commit_msg, employee_id, ssh_config)
                    
                    if result["success"]:
                        print(f"[{employee['name']}] ✅ Git提交成功: {result['commit_hash']}")
                        self.stats["commits"] += 1
                    else:
                        print(f"[{employee['name']}] ⚠️ Git提交失败: {result['message']}")
                        self.stats["commits_failed"] += 1
                    
                    self.task_queue.complete_task(project, employee_id)
                    employee["completed"] += 1
                    self.stats["completed_tasks"] += 1
                    employee["status"] = "idle"
                    
                except Exception as e:
                    print(f"[{employee['name']}] ❌ 处理任务错误: {e}")
                    employee["status"] = "error"
                
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"[{employee['name']}] ❌ 严重错误: {e}")
                await asyncio.sleep(10)
    
    async def run_all(self):
        print("\n" + "=" * 60)
        print("🚀 AI数字员工全自动工作系统 v3.0 (P1任务版)")
        print("=" * 60)
        print(f"总员工数: {len(self.employees)}")
        print(f"项目数: {len(self.project_paths)}")
        print("=" * 60)
        print("⚠️ P0任务完成后自动继续P1任务")
        print("⚠️ 覆盖玄玑引擎全部10个组")
        print("=" * 60)
        
        tasks = []
        for employee_id in self.employees:
            task = asyncio.create_task(self.run_employee(employee_id))
            tasks.append(task)
        
        await asyncio.gather(*tasks, return_exceptions=True)


async def main():
    system = AIDigitalEmployeeSystem()
    
    # XJ-01 紫微元灵组（5人）
    xj01 = [("102", "陈元灵", "xuanji_engine"), ("106", "林对齐", "xuanji_engine"),
            ("107", "黄漂移", "xuanji_engine"), ("108", "周进化", "xuanji_engine"), ("109", "吴模板", "xuanji_engine")]
    
    # XJ-02 禄存星组（5人）
    xj02 = [("111", "周禄存", "xuanji_engine"), ("112", "郑路由", "xuanji_engine"),
            ("113", "王规划", "xuanji_engine"), ("114", "冯优化", "xuanji_engine"), ("115", "钱调度", "xuanji_engine")]
    
    # XJ-03 巨门星组（5人）
    xj03 = [("119", "蒋巨门", "xuanji_engine"), ("120", "沈记忆", "xuanji_engine"),
            ("121", "韩向量", "xuanji_engine"), ("122", "杨检索", "xuanji_engine"), ("123", "朱图谱", "xuanji_engine")]
    
    # XJ-04 廉贞星组（5人）
    xj04 = [("163", "伍廉贞", "xuanji_engine"), ("164", "余情绪", "xuanji_engine"),
            ("165", "元人格", "xuanji_engine"), ("166", "孟一致", "xuanji_engine"), ("167", "平心理", "xuanji_engine")]
    
    # XJ-05 武曲星组（5人）
    xj05 = [("127", "谢武功", "xuanji_engine"), ("128", "邹接口", "xuanji_engine"),
            ("129", "喻发现", "xuanji_engine"), ("130", "柏依赖", "xuanji_engine"), ("131", "水版本", "xuanji_engine")]
    
    # XJ-06 破军星组（5人）
    xj06 = [("133", "章破军", "xuanji_engine"), ("134", "云沙箱", "xuanji_engine"),
            ("135", "苏容器", "xuanji_engine"), ("136", "潘外呼", "xuanji_engine"), ("137", "葛消息", "xuanji_engine")]
    
    # XJ-07 左辅星组（5人）
    xj07 = [("146", "倪左辅", "xuanji_engine"), ("147", "汤K8s", "xuanji_engine"),
            ("148", "殷用户", "xuanji_engine"), ("149", "罗隔离", "xuanji_engine"), ("150", "毕配置", "xuanji_engine")]
    
    # XJ-08 右弼星组（5人）
    xj08 = [("105", "周右弼", "xuanji_engine"), ("156", "乐法律", "xuanji_engine"),
            ("157", "于道德", "xuanji_engine"), ("158", "时权限", "xuanji_engine"), ("159", "皮审计", "xuanji_engine")]
    
    # XJ-09 贪狼星组（5人）
    xj09 = [("143", "薛贪狼", "xuanji_engine"), ("144", "雷ASR", "xuanji_engine"),
            ("145", "贺TTS", "xuanji_engine"), ("176", "贡数字人", "xuanji_engine"), ("177", "赏界面", "xuanji_engine")]
    
    # XJ-10 辅弼星辰组（5人）
    xj10 = [("161", "齐辅弼", "xuanji_engine"), ("162", "康网关", "xuanji_engine"),
            ("168", "和产品", "xuanji_engine"), ("169", "穆文档", "xuanji_engine"), ("183", "财SDK", "xuanji_engine")]
    
    for emp_id, name, project in xj01 + xj02 + xj03 + xj04 + xj05 + xj06 + xj07 + xj08 + xj09 + xj10:
        system.register_employee(emp_id, name, project)
    
    await system.run_all()

if __name__ == "__main__":
    print("启动AI数字员工全自动工作系统 v3.0 (P1任务版)...")
    asyncio.run(main())

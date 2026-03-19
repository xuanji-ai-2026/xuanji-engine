"""
AI数字员工全自动工作系统 v1.0
创建时间: 2026-03-19 23:59
功能: 自动领取 + 代码生成 + 自动提交
"""

import asyncio
import os
from datetime import datetime
from typing import Dict, List

# 导入各模块
from multi_project_task_queue import create_all_projects_tasks, MultiProjectTaskQueue
from code_generator import CodeGenerator
from auto_git_commit import AutoCommitManager

class AIDigitalEmployeeSystem:
    """
    AI数字员工全自动工作系统
    
    三大核心机制:
    1. 自动领取机制 - AI员工自动从队列领取任务
    2. 代码自动生成 - 根据任务描述生成高质量代码
    3. 自动提交机制 - 自动Git提交到GitHub
    """
    
    def __init__(self):
        self.task_queue = create_all_projects_tasks()
        self.code_generator = CodeGenerator()
        self.git_manager = AutoCommitManager()
        self.employees: Dict[str, Dict] = {}
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "generated_files": 0,
            "commits": 0
        }
        
        # 注册项目路径
        self.project_paths = {
            "xuanji_engine": "/workspace/projects/workspace/xuanji-engine-v2",
            "kuncanyun_saas": "/workspace/projects/workspace/kuncanyun-saas",
            "ai_stock_app": "/workspace/projects/workspace/ai-stock-app",
            "hanyu_learning": "/workspace/projects/workspace/han-yu-vietnamese-learning"
        }
        
        # SSH配置映射（不同项目使用不同密钥）
        self.ssh_configs = {
            "xuanji_engine": "/tmp/ssh_config",
            "kuncanyun_saas": "/tmp/ssh_config",
            "ai_stock_app": "/tmp/ssh_config_multi",
            "hanyu_learning": "/tmp/ssh_config"
        }
        
        # 注册Git仓库
        for project, path in self.project_paths.items():
            if os.path.exists(path):
                self.git_manager.register_repo(project, path)
    
    def register_employee(self, employee_id: str, name: str, project: str):
        """注册AI员工"""
        self.employees[employee_id] = {
            "id": employee_id,
            "name": name,
            "project": project,
            "status": "idle",
            "completed": 0
        }
        print(f"✅ 注册AI员工: {name} ({employee_id}) -> {project}")
    
    async def run_employee(self, employee_id: str):
        """运行单个AI员工"""
        employee = self.employees[employee_id]
        project = employee["project"]
        
        print(f"\n🚀 [{employee['name']}] 开始工作...")
        
        while True:
            # 1. 自动领取任务
            task = self.task_queue.claim_task(project, employee_id)
            
            if not task:
                print(f"[{employee['name']}] ⏳ 无任务，等待中...")
                break  # 没有任务了，退出
            
            employee["status"] = "working"
            print(f"[{employee['name']}] ✅ 领取任务: {task.task_id} - {task.title}")
            
            try:
                # 2. 代码自动生成
                code = self.code_generator.generate_code(task)
                
                # 3. 保存代码文件
                project_path = self.project_paths.get(project, "/workspace/projects/workspace")
                file_path = self.code_generator.save_code(task, code, project_path)
                
                print(f"[{employee['name']}] 📝 生成代码: {file_path}")
                self.stats["generated_files"] += 1
                
                # 4. 自动Git提交（使用项目对应的SSH配置）
                commit_msg = f"feat({task.module}): {task.title} ({employee_id})"
                ssh_config = self.ssh_configs.get(project, "/tmp/ssh_config")
                result = self.git_manager.commit_to_repo(
                    project, 
                    [file_path], 
                    commit_msg, 
                    employee_id,
                    ssh_config
                )
                
                if result["success"]:
                    print(f"[{employee['name']}] ✅ Git提交成功: {result['commit_hash']}")
                    self.stats["commits"] += 1
                else:
                    print(f"[{employee['name']}] ⚠️ Git提交失败: {result['message']}")
                
                # 5. 完成任务
                self.task_queue.complete_task(project, employee_id)
                employee["completed"] += 1
                self.stats["completed_tasks"] += 1
                employee["status"] = "idle"
                
            except Exception as e:
                print(f"[{employee['name']}] ❌ 错误: {e}")
                employee["status"] = "error"
            
            # 短暂休息后继续
            await asyncio.sleep(0.5)
    
    async def run_all(self):
        """运行所有AI员工"""
        print("\n" + "=" * 60)
        print("🚀 AI数字员工全自动工作系统 v1.0")
        print("=" * 60)
        print(f"总员工数: {len(self.employees)}")
        print(f"项目数: {len(self.project_paths)}")
        print("=" * 60)
        
        # 创建所有员工任务
        tasks = []
        for employee_id in self.employees:
            task = asyncio.create_task(self.run_employee(employee_id))
            tasks.append(task)
        
        # 等待所有员工完成
        await asyncio.gather(*tasks, return_exceptions=True)
        
        # 输出统计
        self._print_stats()
    
    def _print_stats(self):
        """打印统计信息"""
        print("\n" + "=" * 60)
        print("📊 工作统计")
        print("=" * 60)
        print(f"完成任务: {self.stats['completed_tasks']}")
        print(f"生成文件: {self.stats['generated_files']}")
        print(f"Git提交: {self.stats['commits']}")
        print("\n员工完成情况:")
        for emp_id, emp in self.employees.items():
            print(f"  {emp['name']}: {emp['completed']} 个任务")
        print("=" * 60)

# ==================== 启动174个AI员工 ====================

async def main():
    """主程序"""
    system = AIDigitalEmployeeSystem()
    
    # 注册玄玑引擎v2.0员工 (77人 - 示例注册14人)
    xuanji_employees = [
        ("102", "陈元灵", "xuanji_engine"),
        ("106", "林对齐", "xuanji_engine"),
        ("107", "黄漂移", "xuanji_engine"),
        ("108", "周进化", "xuanji_engine"),
        ("109", "吴模板", "xuanji_engine"),
        ("110", "孙五维", "xuanji_engine"),
        ("111", "周禄存", "xuanji_engine"),
        ("112", "郑路由", "xuanji_engine"),
        ("113", "王规划", "xuanji_engine"),
        ("114", "冯优化", "xuanji_engine"),
        ("115", "钱存信", "xuanji_engine"),
        ("116", "陈存理", "xuanji_engine"),
        ("117", "褚存道", "xuanji_engine"),
        ("118", "卫存器", "xuanji_engine"),
    ]
    
    for emp_id, name, project in xuanji_employees:
        system.register_employee(emp_id, name, project)
    
    # 注册坤灿云SAAS员工 (32人 - 示例注册7人)
    kuncanyun_employees = [
        ("KC001", "插件工程师1", "kuncanyun_saas"),
        ("KC002", "插件工程师2", "kuncanyun_saas"),
        ("KC003", "OA开发", "kuncanyun_saas"),
        ("KC004", "CRM开发", "kuncanyun_saas"),
        ("KC005", "ERP开发", "kuncanyun_saas"),
        ("KC006", "AI工程师", "kuncanyun_saas"),
        ("KC007", "自动化工程师", "kuncanyun_saas"),
    ]
    
    for emp_id, name, project in kuncanyun_employees:
        system.register_employee(emp_id, name, project)
    
    # 注册AI选股App员工 (35人 - 示例注册6人)
    stock_employees = [
        ("ST001", "后端开发1", "ai_stock_app"),
        ("ST002", "后端开发2", "ai_stock_app"),
        ("ST003", "策略工程师1", "ai_stock_app"),
        ("ST004", "策略工程师2", "ai_stock_app"),
        ("ST005", "前端开发1", "ai_stock_app"),
        ("ST006", "AI工程师", "ai_stock_app"),
    ]
    
    for emp_id, name, project in stock_employees:
        system.register_employee(emp_id, name, project)
    
    # 注册汉越语学习工具员工 (30人 - 示例注册8人)
    hanyu_employees = [
        ("HY001", "词汇工程师1", "hanyu_learning"),
        ("HY002", "词汇工程师2", "hanyu_learning"),
        ("HY003", "词根工程师", "hanyu_learning"),
        ("HY004", "卡片工程师", "hanyu_learning"),
        ("HY005", "语音工程师1", "hanyu_learning"),
        ("HY006", "语音工程师2", "hanyu_learning"),
        ("HY007", "测试工程师", "hanyu_learning"),
        ("HY008", "移动端工程师", "hanyu_learning"),
    ]
    
    for emp_id, name, project in hanyu_employees:
        system.register_employee(emp_id, name, project)
    
    # 启动所有员工
    await system.run_all()

if __name__ == "__main__":
    asyncio.run(main())

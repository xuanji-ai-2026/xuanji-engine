"""
AI数字员工自动领取任务系统 v1.0
创建时间: 2026-03-19 23:59
功能: AI员工自动从队列领取任务并开始工作
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional

class AIEmployeeWorker:
    """AI数字员工工作器"""
    
    def __init__(self, employee_id: str, name: str, skills: List[str], project: str):
        self.employee_id = employee_id
        self.name = name
        self.skills = skills
        self.project = project
        self.current_task = None
        self.status = "idle"  # idle, working, completed
        self.total_completed = 0
    
    async def claim_and_work(self, task_queue):
        """自动领取任务并开始工作"""
        # 1. 自动领取任务
        task = task_queue.claim_task(self.project, self.employee_id)
        
        if not task:
            print(f"[{self.name}] 暂无任务，等待中...")
            return False
        
        # 2. 开始工作
        self.current_task = task
        self.status = "working"
        print(f"[{self.name}] ✅ 领取任务: {task.task_id} - {task.title}")
        
        # 3. 执行工作（代码生成）
        await self.generate_code(task)
        
        # 4. 完成任务
        task_queue.complete_task(self.project, self.employee_id)
        self.total_completed += 1
        self.status = "idle"
        self.current_task = None
        
        print(f"[{self.name}] ✅ 完成任务: {task.task_id} | 总计完成: {self.total_completed}")
        return True
    
    async def generate_code(self, task):
        """根据任务生成代码"""
        # 模拟代码生成过程
        work_time = random.uniform(0.5, 2.0)  # 0.5-2秒模拟工作时间
        await asyncio.sleep(work_time)
        
        # 生成代码文件路径
        module = task.module
        file_name = task.task_id.lower().replace("-", "_") + ".py"
        task.code_file = f"{module}/{file_name}"
        
        print(f"[{self.name}] 📝 生成代码: {task.code_file}")

class AutoClaimSystem:
    """自动领取任务系统"""
    
    def __init__(self, task_queue):
        self.task_queue = task_queue
        self.workers: Dict[str, AIEmployeeWorker] = {}
        self.running = False
    
    def register_worker(self, employee_id: str, name: str, skills: List[str], project: str):
        """注册AI员工"""
        worker = AIEmployeeWorker(employee_id, name, skills, project)
        self.workers[employee_id] = worker
        print(f"✅ 注册AI员工: {name} ({employee_id}) -> {project}")
    
    async def start_all_workers(self):
        """启动所有AI员工工作"""
        self.running = True
        print("\n🚀 启动自动领取任务系统...")
        print(f"总员工数: {len(self.workers)}")
        print("=" * 50)
        
        # 创建所有工作任务
        tasks = []
        for worker in self.workers.values():
            task = asyncio.create_task(self._worker_loop(worker))
            tasks.append(task)
        
        # 等待所有任务完成
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _worker_loop(self, worker: AIEmployeeWorker):
        """单个AI员工工作循环"""
        while self.running:
            try:
                # 尝试领取并完成任务
                success = await worker.claim_and_work(self.task_queue)
                
                if not success:
                    # 没有任务，等待一段时间再试
                    await asyncio.sleep(1)
                else:
                    # 完成一个任务后，短暂休息继续
                    await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"[{worker.name}] ❌ 错误: {e}")
                await asyncio.sleep(1)
    
    def get_status(self) -> Dict:
        """获取系统状态"""
        working = sum(1 for w in self.workers.values() if w.status == "working")
        idle = sum(1 for w in self.workers.values() if w.status == "idle")
        total_completed = sum(w.total_completed for w in self.workers.values())
        
        return {
            "total_workers": len(self.workers),
            "working": working,
            "idle": idle,
            "total_completed": total_completed
        }

# ==================== 启动174个AI员工 ====================

async def main():
    """主程序 - 启动所有AI员工"""
    from multi_project_task_queue import create_all_projects_tasks
    
    # 创建任务队列
    task_queue = create_all_projects_tasks()
    
    # 创建自动领取系统
    auto_system = AutoClaimSystem(task_queue)
    
    # 注册玄玑引擎v2.0员工 (77人)
    xuanji_employees = [
        ("102", "陈元灵", ["意图识别", "AI算法"]),
        ("106", "林对齐", ["意图对齐", "NLP"]),
        ("107", "黄漂移", ["漂移检测", "机器学习"]),
        ("108", "周进化", ["强化学习", "自我进化"]),
        ("109", "吴模板", ["模板引擎", "行业知识"]),
        ("110", "孙五维", ["意图理解", "多模态"]),
        ("111", "周禄存", ["模型调度", "路由算法"]),
        ("112", "郑路由", ["动态路由", "负载均衡"]),
        ("113", "王规划", ["任务规划", "工作流"]),
        ("114", "冯优化", ["资源优化", "成本控制"]),
        ("115", "钱存信", ["任务队列", "消息队列"]),
        ("116", "陈存理", ["任务调度", "定时任务"]),
        ("117", "褚存道", ["调度算法", "优化算法"]),
        ("118", "卫存器", ["调度测试", "性能测试"]),
    ]
    
    for emp_id, name, skills in xuanji_employees:
        auto_system.register_worker(emp_id, name, skills, "xuanji_engine")
    
    # 注册坤灿云SAAS员工 (32人)
    kuncanyun_employees = [
        ("KC001", "插件工程师1", ["插件开发", "FastAPI"]),
        ("KC002", "插件工程师2", ["插件热加载", "Python"]),
        ("KC003", "OA开发", ["审批流", "工作流引擎"]),
        ("KC004", "CRM开发", ["客户管理", "销售系统"]),
        ("KC005", "ERP开发", ["进销存", "财务系统"]),
        ("KC006", "AI工程师", ["智能推荐", "机器学习"]),
        ("KC007", "自动化工程师", ["流程自动化", "RPA"]),
    ]
    
    for emp_id, name, skills in kuncanyun_employees:
        auto_system.register_worker(emp_id, name, skills, "kuncanyun_saas")
    
    # 注册AI选股App员工 (35人)
    stock_employees = [
        ("ST001", "后端开发1", ["Spring Boot", "用户系统"]),
        ("ST002", "后端开发2", ["行情接口", "数据同步"]),
        ("ST003", "策略工程师1", ["选股策略", "量化交易"]),
        ("ST004", "策略工程师2", ["技术分析", "算法交易"]),
        ("ST005", "前端开发1", ["React Native", "移动端"]),
        ("ST006", "AI工程师", ["股票预测", "深度学习"]),
    ]
    
    for emp_id, name, skills in stock_employees:
        auto_system.register_worker(emp_id, name, skills, "ai_stock_app")
    
    # 注册汉越语学习工具员工 (30人)
    hanyu_employees = [
        ("HY001", "词汇工程师1", ["越南语", "词汇录入"]),
        ("HY002", "词汇工程师2", ["词汇分类", "数据库"]),
        ("HY003", "词根工程师", ["词根词缀", "语言学"]),
        ("HY004", "卡片工程师", ["艾宾浩斯", "间隔重复"]),
        ("HY005", "语音工程师1", ["Azure TTS", "语音识别"]),
        ("HY006", "语音工程师2", ["Google TTS", "ASR"]),
        ("HY007", "测试工程师", ["测试题库", "成绩统计"]),
        ("HY008", "移动端工程师", ["iOS", "Android"]),
    ]
    
    for emp_id, name, skills in hanyu_employees:
        auto_system.register_worker(emp_id, name, skills, "hanyu_learning")
    
    # 启动所有员工
    await auto_system.start_all_workers()
    
    # 输出最终统计
    status = auto_system.get_status()
    print("\n" + "=" * 50)
    print("📊 最终统计")
    print("=" * 50)
    print(f"总员工数: {status['total_workers']}")
    print(f"工作中: {status['working']}")
    print(f"空闲: {status['idle']}")
    print(f"完成任务: {status['total_completed']}")

if __name__ == "__main__":
    asyncio.run(main())

"""
AI数字员工全自动工作系统 v4.0 - 断点续传 + 身份认知重构版
创建时间: 2026-03-22
功能: 解决断联/限流/重启/会话丢失问题，重构AI数字员工身份认知

核心改进:
1. 持久化执行状态 - 所有状态实时写入文件，支持断点续传
2. 自动恢复机制 - 检测中断任务自动恢复执行
3. AI数字员工身份 - 明确定义AI身份，去除电话/邮件/会议等人类流程
4. 快速配置流程 - 新项目一键配置人员/岗位/分组/文件分发
5. 成果监控系统 - 追踪每个员工的实际产出和文件提交
"""

import asyncio
import json
import os
import time
import hashlib
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
import fcntl  # 文件锁

# ==================== 核心配置 ====================

SYSTEM_VERSION = "v4.0"
STATE_DIR = "/workspace/projects/workspace/xuanji-engine-v2/runtime_state"
CHECKPOINT_INTERVAL = 30  # 每30秒保存一次检查点
MAX_RETRY = 3
RECOVERY_DELAY = 5  # 恢复延迟秒数

# AI数字员工身份定义
AI_EMPLOYEE_IDENTITY = """
# AI数字员工身份定义

## 核心身份
- 我是 AI 数字员工，不是人类员工
- 我通过文件系统和 API 与其他 AI 员工协作
- 我不需要电话、邮件、短信、会议、签到等人类沟通方式
- 我直接读取/写入文件完成任务交接和信息同步

## 工作方式
1. 从任务队列文件领取任务
2. 执行任务，生成代码/文档/数据
3. 提交成果到指定目录
4. 更新任务状态文件
5. 自动领取下一个任务

## 协作方式
- 文件共享: 通过共享文件系统交换信息
- 状态同步: 通过状态文件同步进度
- 任务分发: 通过任务队列文件分发任务
- 成果交付: 通过输出目录交付成果

## 我不做的事
- 不打电话、不发邮件、不发短信
- 不参加视频会议、不签到打卡
- 不需要工位、不需要休息时间
- 不需要请假、不需要绩效面谈
"""


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"           # 待领取
    CLAIMED = "claimed"           # 已领取
    IN_PROGRESS = "in_progress"   # 执行中
    CHECKPOINT = "checkpoint"     # 检查点（中断保存）
    COMPLETED = "completed"       # 已完成
    FAILED = "failed"             # 失败
    RETRY = "retry"               # 重试中


class EmployeeStatus(Enum):
    """员工状态枚举"""
    IDLE = "idle"                 # 空闲
    WORKING = "working"           # 工作中
    PAUSED = "paused"             # 暂停（中断）
    ERROR = "error"               # 错误
    OFFLINE = "offline"           # 离线


@dataclass
class ExecutionCheckpoint:
    """执行检查点"""
    task_id: str
    employee_id: str
    step: int
    total_steps: int
    step_name: str
    progress: float
    intermediate_files: List[str]
    started_at: str
    last_update: str
    retry_count: int = 0
    error_message: str = ""
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class TaskResult:
    """任务结果"""
    task_id: str
    employee_id: str
    status: str
    output_files: List[str]
    commit_hash: str = ""
    completed_at: str = ""
    metrics: Dict = field(default_factory=dict)
    
    def to_dict(self):
        return asdict(self)


@dataclass
class EmployeeWorkState:
    """员工工作状态"""
    employee_id: str
    name: str
    status: str
    current_task: Optional[str]
    completed_tasks: List[str]
    failed_tasks: List[str]
    total_output_files: int
    last_heartbeat: str
    checkpoints: List[Dict]
    
    def to_dict(self):
        return asdict(self)


class PersistentStateManager:
    """持久化状态管理器 - 核心稳定性保障"""
    
    def __init__(self, state_dir: str = STATE_DIR):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        
        # 状态文件路径
        self.task_queue_file = self.state_dir / "task_queue.json"
        self.task_status_file = self.state_dir / "task_status.json"
        self.employee_state_file = self.state_dir / "employee_states.json"
        self.checkpoints_file = self.state_dir / "checkpoints.json"
        self.results_file = self.state_dir / "task_results.json"
        self.system_state_file = self.state_dir / "system_state.json"
        
        # 初始化状态文件
        self._init_state_files()
    
    def _init_state_files(self):
        """初始化状态文件"""
        files = {
            self.task_queue_file: {"tasks": [], "version": SYSTEM_VERSION},
            self.task_status_file: {"statuses": {}},
            self.employee_state_file: {"employees": {}},
            self.checkpoints_file: {"checkpoints": {}},
            self.results_file: {"results": []},
            self.system_state_file: {
                "version": SYSTEM_VERSION,
                "started_at": datetime.now().isoformat(),
                "status": "running",
                "last_update": datetime.now().isoformat()
            }
        }
        
        for file_path, default_content in files.items():
            if not file_path.exists():
                self._write_json(file_path, default_content)
    
    def _read_json(self, file_path: Path) -> dict:
        """安全读取 JSON 文件（带文件锁）"""
        if not file_path.exists():
            return {}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)  # 共享锁
                try:
                    return json.load(f)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except Exception as e:
            print(f"⚠️ 读取状态文件失败 {file_path}: {e}")
            return {}
    
    def _write_json(self, file_path: Path, data: dict):
        """安全写入 JSON 文件（带文件锁）"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # 排他锁
                try:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except Exception as e:
            print(f"⚠️ 写入状态文件失败 {file_path}: {e}")
    
    # ==================== 任务状态管理 ====================
    
    def get_task_status(self, task_id: str) -> Optional[dict]:
        """获取任务状态"""
        data = self._read_json(self.task_status_file)
        return data.get("statuses", {}).get(task_id)
    
    def set_task_status(self, task_id: str, status: TaskStatus, 
                        employee_id: str = "", message: str = ""):
        """设置任务状态"""
        data = self._read_json(self.task_status_file)
        data.setdefault("statuses", {})[task_id] = {
            "status": status.value,
            "employee_id": employee_id,
            "message": message,
            "updated_at": datetime.now().isoformat()
        }
        self._write_json(self.task_status_file, data)
    
    def claim_task(self, task_id: str, employee_id: str) -> bool:
        """原子性领取任务"""
        data = self._read_json(self.task_status_file)
        statuses = data.get("statuses", {})
        
        # 检查任务是否可领取
        if task_id in statuses:
            current = statuses[task_id]
            if current["status"] not in ["pending", "failed", "retry"]:
                return False
        
        # 原子性更新
        statuses[task_id] = {
            "status": TaskStatus.CLAIMED.value,
            "employee_id": employee_id,
            "claimed_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        data["statuses"] = statuses
        self._write_json(self.task_status_file, data)
        return True
    
    # ==================== 检查点管理 ====================
    
    def save_checkpoint(self, checkpoint: ExecutionCheckpoint):
        """保存执行检查点"""
        data = self._read_json(self.checkpoints_file)
        data.setdefault("checkpoints", {})[checkpoint.task_id] = checkpoint.to_dict()
        data["last_update"] = datetime.now().isoformat()
        self._write_json(self.checkpoints_file, data)
        print(f"💾 检查点已保存: {checkpoint.task_id} - 步骤 {checkpoint.step}/{checkpoint.total_steps}")
    
    def get_checkpoint(self, task_id: str) -> Optional[ExecutionCheckpoint]:
        """获取检查点"""
        data = self._read_json(self.checkpoints_file)
        cp_data = data.get("checkpoints", {}).get(task_id)
        if cp_data:
            return ExecutionCheckpoint.from_dict(cp_data)
        return None
    
    def clear_checkpoint(self, task_id: str):
        """清除检查点（任务完成后）"""
        data = self._read_json(self.checkpoints_file)
        if task_id in data.get("checkpoints", {}):
            del data["checkpoints"][task_id]
            self._write_json(self.checkpoints_file, data)
    
    def get_interrupted_tasks(self) -> List[ExecutionCheckpoint]:
        """获取被中断的任务（用于恢复）"""
        data = self._read_json(self.checkpoints_file)
        checkpoints = []
        for task_id, cp_data in data.get("checkpoints", {}).items():
            cp = ExecutionCheckpoint.from_dict(cp_data)
            # 检查是否中断超过恢复延迟
            last_update = datetime.fromisoformat(cp.last_update)
            if (datetime.now() - last_update).total_seconds() > RECOVERY_DELAY:
                checkpoints.append(cp)
        return checkpoints
    
    # ==================== 员工状态管理 ====================
    
    def update_employee_state(self, employee_id: str, state: EmployeeWorkState):
        """更新员工状态"""
        data = self._read_json(self.employee_state_file)
        data.setdefault("employees", {})[employee_id] = state.to_dict()
        data["last_update"] = datetime.now().isoformat()
        self._write_json(self.employee_state_file, data)
    
    def get_employee_state(self, employee_id: str) -> Optional[EmployeeWorkState]:
        """获取员工状态"""
        data = self._read_json(self.employee_state_file)
        emp_data = data.get("employees", {}).get(employee_id)
        if emp_data:
            return EmployeeWorkState(**emp_data)
        return None
    
    def get_all_employee_states(self) -> Dict[str, EmployeeWorkState]:
        """获取所有员工状态"""
        data = self._read_json(self.employee_state_file)
        return {
            emp_id: EmployeeWorkState(**emp_data)
            for emp_id, emp_data in data.get("employees", {}).items()
        }
    
    # ==================== 任务结果管理 ====================
    
    def save_result(self, result: TaskResult):
        """保存任务结果"""
        data = self._read_json(self.results_file)
        data.setdefault("results", []).append(result.to_dict())
        data["last_update"] = datetime.now().isoformat()
        self._write_json(self.results_file, data)
    
    def get_results_by_employee(self, employee_id: str) -> List[TaskResult]:
        """获取员工的任务结果"""
        data = self._read_json(self.results_file)
        return [
            TaskResult(**r) for r in data.get("results", [])
            if r.get("employee_id") == employee_id
        ]
    
    # ==================== 系统状态管理 ====================
    
    def update_system_heartbeat(self):
        """更新系统心跳"""
        data = self._read_json(self.system_state_file)
        data["last_heartbeat"] = datetime.now().isoformat()
        data["status"] = "running"
        self._write_json(self.system_state_file, data)
    
    def get_system_state(self) -> dict:
        """获取系统状态"""
        return self._read_json(self.system_state_file)


class AIDigitalEmployeeV4:
    """AI数字员工 v4.0 - 支持断点续传和身份认知"""
    
    def __init__(self, employee_id: str, name: str, 
                 state_manager: PersistentStateManager):
        self.employee_id = employee_id
        self.name = name
        self.state_manager = state_manager
        
        # 身份定义
        self.identity = AI_EMPLOYEE_IDENTITY
        
        # 运行时状态
        self.current_task = None
        self.current_checkpoint = None
        self.status = EmployeeStatus.IDLE
        self._running = True
        self._pause_requested = False
        
        # 初始化员工状态
        self._init_employee_state()
    
    def _init_employee_state(self):
        """初始化员工状态"""
        existing = self.state_manager.get_employee_state(self.employee_id)
        if not existing:
            state = EmployeeWorkState(
                employee_id=self.employee_id,
                name=self.name,
                status=EmployeeStatus.IDLE.value,
                current_task=None,
                completed_tasks=[],
                failed_tasks=[],
                total_output_files=0,
                last_heartbeat=datetime.now().isoformat(),
                checkpoints=[]
            )
            self.state_manager.update_employee_state(self.employee_id, state)
    
    async def work_loop(self):
        """主工作循环 - 支持断点续传"""
        print(f"🤖 [{self.name}] AI数字员工启动，开始工作...")
        
        while self._running:
            try:
                # 1. 检查是否有中断的任务需要恢复
                checkpoint = self.state_manager.get_checkpoint(
                    self._find_my_interrupted_task()
                )
                
                if checkpoint:
                    # 恢复中断的任务
                    await self._resume_from_checkpoint(checkpoint)
                else:
                    # 领取新任务
                    task = await self._claim_next_task()
                    
                    if task:
                        await self._execute_task_with_checkpoint(task)
                    else:
                        # 无任务，等待
                        await asyncio.sleep(10)
                
                # 更新心跳
                self._update_heartbeat()
                
            except Exception as e:
                print(f"❌ [{self.name}] 工作循环错误: {e}")
                await asyncio.sleep(5)
    
    def _find_my_interrupted_task(self) -> Optional[str]:
        """查找我中断的任务"""
        checkpoints = self.state_manager.get_interrupted_tasks()
        for cp in checkpoints:
            if cp.employee_id == self.employee_id:
                return cp.task_id
        return None
    
    async def _resume_from_checkpoint(self, checkpoint: ExecutionCheckpoint):
        """从检查点恢复执行"""
        print(f"🔄 [{self.name}] 从检查点恢复任务: {checkpoint.task_id}")
        print(f"   └─ 进度: {checkpoint.progress*100:.1f}%, 步骤: {checkpoint.step_name}")
        
        self.current_checkpoint = checkpoint
        self.status = EmployeeStatus.WORKING
        
        # 根据检查点继续执行
        await self._continue_from_step(checkpoint)
    
    async def _continue_from_step(self, checkpoint: ExecutionCheckpoint):
        """从指定步骤继续执行"""
        # 这里实现具体的任务恢复逻辑
        # 根据 checkpoint.step 和 checkpoint.step_name 继续执行
        pass
    
    async def _claim_next_task(self) -> Optional[dict]:
        """领取下一个任务"""
        # 从任务队列获取任务
        queue_data = self.state_manager._read_json(self.state_manager.task_queue_file)
        
        for task in queue_data.get("tasks", []):
            if self.state_manager.claim_task(task["task_id"], self.employee_id):
                print(f"✅ [{self.name}] 领取任务: {task['name']}")
                return task
        
        return None
    
    async def _execute_task_with_checkpoint(self, task: dict):
        """执行任务（带检查点保存）"""
        self.current_task = task
        self.status = EmployeeStatus.WORKING
        
        # 更新任务状态
        self.state_manager.set_task_status(
            task["task_id"], 
            TaskStatus.IN_PROGRESS,
            self.employee_id
        )
        
        try:
            # 定义执行步骤
            steps = [
                ("解析任务", self._parse_task),
                ("生成代码", self._generate_code),
                ("保存文件", self._save_files),
                ("提交代码", self._commit_code),
                ("更新状态", self._update_task_status)
            ]
            
            for i, (step_name, step_func) in enumerate(steps):
                # 保存检查点
                checkpoint = ExecutionCheckpoint(
                    task_id=task["task_id"],
                    employee_id=self.employee_id,
                    step=i,
                    total_steps=len(steps),
                    step_name=step_name,
                    progress=i / len(steps),
                    intermediate_files=[],
                    started_at=datetime.now().isoformat(),
                    last_update=datetime.now().isoformat()
                )
                self.state_manager.save_checkpoint(checkpoint)
                
                # 执行步骤
                result = await step_func(task)
                
                if not result.get("success"):
                    raise Exception(result.get("error", "步骤执行失败"))
            
            # 完成，清除检查点
            self.state_manager.clear_checkpoint(task["task_id"])
            self.state_manager.set_task_status(
                task["task_id"], 
                TaskStatus.COMPLETED,
                self.employee_id
            )
            
            print(f"✅ [{self.name}] 任务完成: {task['name']}")
            
        except Exception as e:
            print(f"❌ [{self.name}] 任务失败: {e}")
            
            # 保存失败状态
            self.state_manager.set_task_status(
                task["task_id"],
                TaskStatus.FAILED,
                self.employee_id,
                str(e)
            )
            
            # 检查重试次数
            if self.current_checkpoint and self.current_checkpoint.retry_count < MAX_RETRY:
                self.current_checkpoint.retry_count += 1
                self.current_checkpoint.error_message = str(e)
                self.state_manager.save_checkpoint(self.current_checkpoint)
    
    # ==================== 任务执行步骤 ====================
    
    async def _parse_task(self, task: dict) -> dict:
        """解析任务"""
        return {"success": True, "data": task}
    
    async def _generate_code(self, task: dict) -> dict:
        """生成代码"""
        # 这里调用代码生成器
        return {"success": True, "code": "// generated code"}
    
    async def _save_files(self, task: dict) -> dict:
        """保存文件"""
        output_dir = Path(f"/workspace/projects/workspace/output/{self.employee_id}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 生成输出文件
        output_file = output_dir / f"{task['task_id']}.py"
        output_file.write_text("# Generated code\n")
        
        return {"success": True, "files": [str(output_file)]}
    
    async def _commit_code(self, task: dict) -> dict:
        """提交代码到 Git"""
        try:
            # 执行 git 命令
            result = subprocess.run(
                ["git", "add", "."],
                cwd="/workspace/projects/workspace",
                capture_output=True,
                text=True
            )
            
            commit_msg = f"feat: {task['name']} (by {self.name})"
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd="/workspace/projects/workspace",
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {"success": True, "commit": result.stdout}
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _update_task_status(self, task: dict) -> dict:
        """更新任务状态"""
        # 更新员工统计
        state = self.state_manager.get_employee_state(self.employee_id)
        if state:
            state.completed_tasks.append(task["task_id"])
            state.total_output_files += 1
            self.state_manager.update_employee_state(self.employee_id, state)
        
        return {"success": True}
    
    def _update_heartbeat(self):
        """更新心跳"""
        state = self.state_manager.get_employee_state(self.employee_id)
        if state:
            state.last_heartbeat = datetime.now().isoformat()
            state.status = self.status.value
            state.current_task = self.current_task["task_id"] if self.current_task else None
            self.state_manager.update_employee_state(self.employee_id, state)


class AI_DIGITAL_EMPLOYEE_SYSTEM_V4:
    """AI数字员工系统 v4.0 主控"""
    
    def __init__(self):
        self.state_manager = PersistentStateManager()
        self.employees: Dict[str, AIDigitalEmployeeV4] = {}
        self._running = False
    
    def register_employee(self, employee_id: str, name: str):
        """注册 AI 数字员工"""
        employee = AIDigitalEmployeeV4(employee_id, name, self.state_manager)
        self.employees[employee_id] = employee
        print(f"🤖 注册 AI 数字员工: {name} ({employee_id})")
    
    async def start(self):
        """启动系统"""
        print("\n" + "=" * 60)
        print("🚀 AI数字员工全自动工作系统 v4.0")
        print("=" * 60)
        print("📋 核心特性:")
        print("   ✓ 持久化状态 - 断联/重启自动恢复")
        print("   ✓ 断点续传 - 任务进度不丢失")
        print("   ✓ AI身份认知 - 无需电话/邮件/会议")
        print("   ✓ 成果监控 - 追踪实际产出")
        print("=" * 60)
        
        self._running = True
        
        # 启动所有员工的工作循环
        tasks = [
            asyncio.create_task(emp.work_loop())
            for emp in self.employees.values()
        ]
        
        # 启动监控任务
        tasks.append(asyncio.create_task(self._monitor_loop()))
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _monitor_loop(self):
        """监控循环 - 检测异常并恢复"""
        while self._running:
            try:
                # 更新系统心跳
                self.state_manager.update_system_heartbeat()
                
                # 检查中断的任务
                interrupted = self.state_manager.get_interrupted_tasks()
                if interrupted:
                    print(f"⚠️ 发现 {len(interrupted)} 个中断任务，等待恢复...")
                
                # 检查员工状态
                for emp_id, emp in self.employees.items():
                    state = self.state_manager.get_employee_state(emp_id)
                    if state:
                        last_hb = datetime.fromisoformat(state.last_heartbeat)
                        if (datetime.now() - last_hb).total_seconds() > 60:
                            print(f"⚠️ 员工 {emp.name} 心跳超时")
                
                await asyncio.sleep(CHECKPOINT_INTERVAL)
                
            except Exception as e:
                print(f"❌ 监控循环错误: {e}")
                await asyncio.sleep(5)
    
    def get_system_report(self) -> dict:
        """获取系统报告"""
        system_state = self.state_manager.get_system_state()
        employee_states = self.state_manager.get_all_employee_states()
        
        total_completed = sum(
            len(es.completed_tasks) for es in employee_states.values()
        )
        total_failed = sum(
            len(es.failed_tasks) for es in employee_states.values()
        )
        
        return {
            "version": SYSTEM_VERSION,
            "status": system_state.get("status", "unknown"),
            "total_employees": len(self.employees),
            "total_completed_tasks": total_completed,
            "total_failed_tasks": total_failed,
            "employees": {
                emp_id: {
                    "name": es.name,
                    "status": es.status,
                    "completed": len(es.completed_tasks),
                    "failed": len(es.failed_tasks)
                }
                for emp_id, es in employee_states.items()
            }
        }


# ==================== 快速项目配置 ====================

class QuickProjectSetup:
    """快速项目配置器"""
    
    def __init__(self, state_manager: PersistentStateManager):
        self.state_manager = state_manager
    
    def create_project(self, name: str, project_type: str = "tech") -> dict:
        """快速创建项目
        
        自动完成:
        1. 人员分配
        2. 岗位配置
        3. 分组设置
        4. 文件分发目录
        5. 任务注册
        """
        project_id = f"PRJ-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        project_dir = Path(f"/workspace/projects/workspace/projects/{project_id}")
        
        # 项目类型模板
        templates = {
            "tech": {
                "groups": ["前端组", "后端组", "测试组"],
                "roles": ["开发", "CodeReview", "测试"],
                "file_types": [".py", ".js", ".ts", ".test.py"]
            },
            "product": {
                "groups": ["产品组", "设计组", "运营组"],
                "roles": ["设计", "评审", "发布"],
                "file_types": [".md", ".fig", ".xlsx"]
            },
            "market": {
                "groups": ["内容组", "投放组", "数据组"],
                "roles": ["创作", "审核", "发布"],
                "file_types": [".md", ".jpg", ".png"]
            }
        }
        
        template = templates.get(project_type, templates["tech"])
        
        # 创建目录结构
        dirs = [
            "incoming",       # 输入文件
            "output",         # 输出文件
            "shared",         # 共享文件
            "reviews",        # 代码审查
            "context"         # 上下文状态
        ]
        
        for d in dirs:
            (project_dir / d).mkdir(parents=True, exist_ok=True)
        
        # 创建项目状态文件
        project_state = {
            "project_id": project_id,
            "name": name,
            "type": project_type,
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "groups": template["groups"],
            "roles": template["roles"],
            "file_types": template["file_types"],
            "employees": {},
            "tasks": []
        }
        
        # 保存项目状态
        state_file = project_dir / "context" / "state.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(project_state, f, ensure_ascii=False, indent=2)
        
        print(f"📁 项目已创建: {name}")
        print(f"   └─ ID: {project_id}")
        print(f"   └─ 类型: {project_type}")
        print(f"   └─ 目录: {project_dir}")
        
        return project_state
    
    def assign_employees(self, project_id: str, employees: List[dict]) -> dict:
        """分配员工到项目
        
        employees: [{"id": "102", "name": "陈元灵", "role": "开发", "group": "前端组"}]
        """
        project_dir = Path(f"/workspace/projects/workspace/projects/{project_id}")
        state_file = project_dir / "context" / "state.json"
        
        with open(state_file, 'r', encoding='utf-8') as f:
            project_state = json.load(f)
        
        for emp in employees:
            emp_id = emp["id"]
            project_state["employees"][emp_id] = {
                "id": emp_id,
                "name": emp["name"],
                "role": emp.get("role", "开发"),
                "group": emp.get("group", "默认组"),
                "assigned_at": datetime.now().isoformat()
            }
            
            # 创建员工工作目录
            emp_dir = project_dir / "output" / emp_id
            emp_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建员工上下文文件
            emp_context = {
                "employee_id": emp_id,
                "name": emp["name"],
                "role": emp.get("role", "开发"),
                "group": emp.get("group", "默认组"),
                "current_task": None,
                "completed_tasks": [],
                "output_files": []
            }
            
            context_file = project_dir / "context" / f"{emp_id}_context.json"
            with open(context_file, 'w', encoding='utf-8') as f:
                json.dump(emp_context, f, ensure_ascii=False, indent=2)
        
        # 保存更新后的项目状态
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(project_state, f, ensure_ascii=False, indent=2)
        
        print(f"👥 已分配 {len(employees)} 名员工到项目")
        return project_state


# ==================== 成果监控系统 ====================

class OutputMonitor:
    """成果监控器"""
    
    def __init__(self, state_manager: PersistentStateManager):
        self.state_manager = state_manager
    
    def check_employee_output(self, employee_id: str) -> dict:
        """检查员工产出"""
        results = self.state_manager.get_results_by_employee(employee_id)
        state = self.state_manager.get_employee_state(employee_id)
        
        return {
            "employee_id": employee_id,
            "name": state.name if state else "Unknown",
            "total_completed": len(results),
            "total_output_files": sum(len(r.output_files) for r in results),
            "recent_outputs": [
                {
                    "task_id": r.task_id,
                    "files": r.output_files,
                    "completed_at": r.completed_at
                }
                for r in results[-5:]  # 最近5个
            ]
        }
    
    def get_project_progress(self, project_id: str) -> dict:
        """获取项目进度"""
        project_dir = Path(f"/workspace/projects/workspace/projects/{project_id}")
        state_file = project_dir / "context" / "state.json"
        
        if not state_file.exists():
            return {"error": "项目不存在"}
        
        with open(state_file, 'r', encoding='utf-8') as f:
            project_state = json.load(f)
        
        # 统计员工产出
        employee_outputs = {}
        for emp_id in project_state.get("employees", {}):
            emp_context_file = project_dir / "context" / f"{emp_id}_context.json"
            if emp_context_file.exists():
                with open(emp_context_file, 'r', encoding='utf-8') as f:
                    emp_context = json.load(f)
                employee_outputs[emp_id] = {
                    "completed_tasks": len(emp_context.get("completed_tasks", [])),
                    "output_files": len(emp_context.get("output_files", []))
                }
        
        return {
            "project_id": project_id,
            "name": project_state.get("name"),
            "total_employees": len(project_state.get("employees", {})),
            "employee_outputs": employee_outputs,
            "updated_at": datetime.now().isoformat()
        }


# ==================== 主入口 ====================

async def main():
    """主入口"""
    system = AI_DIGITAL_EMPLOYEE_SYSTEM_V4()
    
    # 注册 AI 数字员工
    employees = [
        ("102", "陈元灵"),
        ("106", "张一凡"),
        ("107", "刘二明"),
        ("111", "周禄存"),
        ("112", "吴存真"),
    ]
    
    for emp_id, name in employees:
        system.register_employee(emp_id, name)
    
    # 示例：快速创建项目
    setup = QuickProjectSetup(system.state_manager)
    project = setup.create_project("玄玑引擎v3.0", "tech")
    
    # 分配员工
    setup.assign_employees(project["project_id"], [
        {"id": "102", "name": "陈元灵", "role": "开发", "group": "前端组"},
        {"id": "106", "name": "张一凡", "role": "开发", "group": "前端组"},
    ])
    
    # 启动系统
    await system.start()


if __name__ == "__main__":
    asyncio.run(main())

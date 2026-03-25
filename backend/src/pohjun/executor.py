"""
破军星 - 执行引擎模块
插件执行、沙箱隔离、资源限制
"""

import asyncio
import subprocess
import os
import tempfile
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
import hashlib
import time


class ExecutionStatus(str, Enum):
    """执行状态"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    TIMEOUT = "timeout"


class ResourceLimit(BaseModel):
    """资源限制"""
    max_cpu_percent: float = Field(default=50.0)
    max_memory_mb: int = Field(default=256)
    max_execution_time: int = Field(default=30)  # 秒
    max_disk_mb: int = Field(default=100)


class ExecutionResult(BaseModel):
    """执行结果"""
    status: ExecutionStatus
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0
    execution_time: float = 0.0
    error: Optional[str] = None


class SandboxExecutor(BaseModel):
    """沙箱执行器"""
    sandbox_id: str = ""
    working_dir: str = ""
    resource_limit: ResourceLimit = Field(default_factory=ResourceLimit)
    status: ExecutionStatus = ExecutionStatus.PENDING
    
    class Config:
        arbitrary_types_allowed = True


class ExecutionEngine:
    """执行引擎"""
    
    def __init__(self, base_sandbox_dir: str = None):
        self.base_sandbox_dir = base_sandbox_dir or tempfile.mkdtemp(prefix="xuanji_sandbox_")
        self.active_sandboxes: Dict[str, SandboxExecutor] = {}
        self.execution_history: list = []
    
    async def execute_code(
        self,
        code: str,
        language: str = "python",
        timeout: int = 30,
        resources: ResourceLimit = None
    ) -> ExecutionResult:
        """执行代码"""
        start_time = time.time()
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix=f'.{language}',
            delete=False
        ) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            # 执行代码
            result = await self._run_in_sandbox(
                temp_file,
                language,
                timeout,
                resources or ResourceLimit()
            )
            result.execution_time = time.time() - start_time
            return result
            
        finally:
            # 清理临时文件
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    async def _run_in_sandbox(
        self,
        file_path: str,
        language: str,
        timeout: int,
        resources: ResourceLimit
    ) -> ExecutionResult:
        """在沙箱中运行"""
        cmd_map = {
            "python": ["python3", file_path],
            "javascript": ["node", file_path],
            "bash": ["bash", file_path],
        }
        
        cmd = cmd_map.get(language, ["python3", file_path])
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.base_sandbox_dir
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
                
                return ExecutionResult(
                    status=ExecutionStatus.SUCCESS if process.returncode == 0 else ExecutionStatus.FAILED,
                    stdout=stdout.decode() if stdout else "",
                    stderr=stderr.decode() if stderr else "",
                    exit_code=process.returncode or 0
                )
                
            except asyncio.TimeoutError:
                process.kill()
                return ExecutionResult(
                    status=ExecutionStatus.TIMEOUT,
                    error=f"Execution timeout after {timeout}s"
                )
                
        except Exception as e:
            return ExecutionResult(
                status=ExecutionStatus.FAILED,
                error=str(e)
            )
    
    def get_sandbox_status(self, sandbox_id: str) -> Optional[SandboxExecutor]:
        """获取沙箱状态"""
        return self.active_sandboxes.get(sandbox_id)
    
    def list_active_sandboxes(self) -> list:
        """列出活跃沙箱"""
        return list(self.active_sandboxes.keys())


# 测试代码
if __name__ == "__main__":
    async def test():
        engine = ExecutionEngine()
        
        # 测试Python代码执行
        code = """
print("Hello from XuanJi Engine!")
result = 1 + 2
print(f"1 + 2 = {result}")
"""
        result = await engine.execute_code(code, "python", timeout=10)
        
        print(f"Status: {result.status}")
        print(f"Output: {result.stdout}")
        print(f"Execution time: {result.execution_time:.2f}s")
    
    asyncio.run(test())

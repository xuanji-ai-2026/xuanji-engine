"""
自动Git提交系统 v1.0
创建时间: 2026-03-19 23:59
功能: 自动提交代码到GitHub
"""

import subprocess
import os
from datetime import datetime
from typing import List, Dict

class AutoGitCommit:
    """自动Git提交系统"""
    
    def __init__(self, repo_path: str, ssh_config: str = "/tmp/ssh_config"):
        self.repo_path = repo_path
        self.ssh_config = ssh_config
        self.git_ssh_command = f"ssh -F {ssh_config} -o StrictHostKeyChecking=no"
    
    def commit_code(self, file_paths: List[str], message: str, employee_id: str = "") -> Dict:
        """
        自动提交代码
        
        Args:
            file_paths: 要提交的文件路径列表
            message: 提交信息
            employee_id: 员工ID（可选）
            
        Returns:
            提交结果字典
        """
        result = {
            "success": False,
            "message": "",
            "commit_hash": "",
            "files_committed": 0
        }
        
        try:
            # 1. 切换到仓库目录
            os.chdir(self.repo_path)
            
            # 2. 配置Git用户信息（如果提供了员工ID）
            if employee_id:
                subprocess.run(
                    ["git", "config", "user.name", f"AI-Employee-{employee_id}"],
                    check=True, capture_output=True
                )
                subprocess.run(
                    ["git", "config", "user.email", f"{employee_id}@xuanji.ai"],
                    check=True, capture_output=True
                )
            
            # 3. 添加文件到暂存区
            for file_path in file_paths:
                subprocess.run(
                    ["git", "add", file_path],
                    check=True, capture_output=True
                )
            
            # 4. 提交
            commit_result = subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True,
                text=True
            )
            
            if commit_result.returncode != 0:
                result["message"] = f"提交失败: {commit_result.stderr}"
                return result
            
            # 5. 获取提交哈希
            hash_result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True
            )
            commit_hash = hash_result.stdout.strip()
            
            # 6. 推送到远程
            push_result = subprocess.run(
                ["git", "push", "origin", "main"],
                capture_output=True,
                text=True,
                env={**os.environ, "GIT_SSH_COMMAND": self.git_ssh_command}
            )
            
            if push_result.returncode != 0:
                result["message"] = f"推送失败: {push_result.stderr}"
                return result
            
            # 成功
            result["success"] = True
            result["message"] = "提交并推送成功"
            result["commit_hash"] = commit_hash
            result["files_committed"] = len(file_paths)
            
        except Exception as e:
            result["message"] = f"错误: {str(e)}"
        
        return result
    
    def batch_commit(self, commits: List[Dict]) -> List[Dict]:
        """
        批量提交
        
        Args:
            commits: 提交列表，每个元素是{files, message, employee_id}
            
        Returns:
            提交结果列表
        """
        results = []
        
        for commit in commits:
            result = self.commit_code(
                file_paths=commit["files"],
                message=commit["message"],
                employee_id=commit.get("employee_id", "")
            )
            results.append(result)
        
        return results
    
    def create_branch(self, branch_name: str) -> bool:
        """创建分支"""
        try:
            os.chdir(self.repo_path)
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                check=True, capture_output=True
            )
            return True
        except:
            return False
    
    def merge_branch(self, branch_name: str) -> bool:
        """合并分支"""
        try:
            os.chdir(self.repo_path)
            # 切换到main
            subprocess.run(
                ["git", "checkout", "main"],
                check=True, capture_output=True
            )
            # 合并
            subprocess.run(
                ["git", "merge", branch_name],
                check=True, capture_output=True
            )
            return True
        except:
            return False
    
    def get_commit_count(self) -> int:
        """获取提交次数"""
        try:
            os.chdir(self.repo_path)
            result = subprocess.run(
                ["git", "rev-list", "--count", "HEAD"],
                capture_output=True,
                text=True
            )
            return int(result.stdout.strip())
        except:
            return 0
    
    def get_status(self) -> Dict:
        """获取Git状态"""
        try:
            os.chdir(self.repo_path)
            
            # 获取当前分支
            branch_result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True
            )
            branch = branch_result.stdout.strip()
            
            # 获取未提交文件数
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True
            )
            uncommitted = len(status_result.stdout.strip().split("\n")) if status_result.stdout.strip() else 0
            
            # 获取提交数
            commit_count = self.get_commit_count()
            
            return {
                "branch": branch,
                "uncommitted_files": uncommitted,
                "total_commits": commit_count
            }
        except Exception as e:
            return {"error": str(e)}

# ==================== 自动化提交管理器 ====================

class AutoCommitManager:
    """自动提交管理器"""
    
    def __init__(self):
        self.repos = {}
    
    def register_repo(self, name: str, path: str, ssh_config: str = "/tmp/ssh_config"):
        """注册仓库"""
        self.repos[name] = AutoGitCommit(path, ssh_config)
        print(f"✅ 注册仓库: {name} -> {path}")
    
    def commit_to_repo(self, repo_name: str, files: List[str], message: str, employee_id: str = "") -> Dict:
        """提交到指定仓库"""
        if repo_name not in self.repos:
            return {"success": False, "message": f"仓库 {repo_name} 未注册"}
        
        return self.repos[repo_name].commit_code(files, message, employee_id)
    
    def get_all_status(self) -> Dict:
        """获取所有仓库状态"""
        status = {}
        for name, repo in self.repos.items():
            status[name] = repo.get_status()
        return status

# ==================== 主程序 ====================

if __name__ == "__main__":
    # 示例用法
    manager = AutoCommitManager()
    
    # 注册仓库
    manager.register_repo(
        "xuanji-engine",
        "/workspace/projects/workspace/xuanji-engine-v2"
    )
    
    print("\n自动Git提交系统已就绪")
    print("支持功能: 自动提交、批量提交、分支管理、状态查询")

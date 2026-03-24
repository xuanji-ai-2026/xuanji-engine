#!/usr/bin/env python3
"""
玄玑引擎项目深度问题排查系统
创建时间: 2026-03-23 02:50
功能: 深度排查员工无提交、任务发布、系统注册等问题
"""

import subprocess
import re
import json
from collections import defaultdict

class DeepInvestigator:
    def __init__(self):
        self.project_path = "/workspace/projects/workspace/xuanji-engine-v2"
        self.automate_file = "ai_employee_full_automation_v3.py"
        self.task_queue_file = "ultimate_task_queue.json"
        self.git_log = []

    def load_ultimate_tasks(self):
        """加载终极版任务"""
        try:
            with open(f"{self.project_path}/{self.task_queue_file}", 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"❌ 加载终极版任务失败: {e}")
            return {}

    def parse_automation_employees(self):
        """解析自动化系统中的员工注册"""
        employees = defaultdict(dict)
        
        with open(f"{self.project_path}/{self.automate_file}", 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取所有星组的员工
        star_patterns = {
            'xj01': r'xj01\s*=\s*\[(.*?)\]',
            'xj02': r'xj02\s*=\s*\[(.*?)\]',
            'xj03': r'xj03\s*=\s*\[(.*?)\]',
            'xj04': r'xj04\s*=\s*\[(.*?)\]',
            'xj05': r'xj05\s*=\s*\[(.*?)\]',
            'xj06': r'xj06\s*=\s*\[(.*?)\]',
            'xj07': r'xj07\s*=\s*\[(.*?)\]',
            'xj08': r'xj08\s*=\s*\[(.*?)\]',
            'x09': r'xj09\s*=\s*\[(.*?)\]',
            'xj10': r'xj10\s*=\s*\[(.*?)\]',
        }

        for star, pattern in star_patterns.items():
            match = re.search(pattern, content)
            if match:
                members_str = match.group(1)
                members = []
                for m in re.finditer(r'\("(\d+)", "([^"]+)", "([^"]+)"', members_str):
                    emp_id = m.group(1)
                    emp_name = m.group(2)
                    employees[emp_id] = {
                        'star': star,
                        'emp_id': emp_id,
                        'name': emp_name
                    }

        return employees

    def extract_git_commits(self):
        """提取所有Git提交"""
        try:
            result = subprocess.check_output(
                ['git', 'log', '--all', '--pretty=format:%an|%ae|%s|%H'],
                stderr=subprocess.DEVNULL,
                cwd=self.project_path
            ).decode('utf-8')

            commits = []
            for line in result.split('\n'):
                if not line.strip():
                    continue
                parts = line.split('|')
                if len(parts) >= 3:
                    author = parts[0].strip()
                    email = parts[1].strip()
                    msg = parts[2].strip()
                    commits.append({
                        'author': author,
                        'email': email,
                        'message': msg
                    })
            return commits
        except Exception as e:
            print(f"❌ 提取Git提交失败: {e}")
            return []

    def check_employee_101(self, git_commits):
        """深度排查工号101李星辰"""
        print("=" * 120)
        print("🔍 深度排查：工号101 李星辰（技术VP/总负责）")
        print("=" * 120)

        # 1. 检查Git提交
        commits_by_101 = [c for c in git_commits if '101' in c['author'] or '101@xuanji.ai' in c['email']]
        
        print(f"📊 Git提交记录:")
        if commits_by_101:
            for commit in commits_by_101:
                print(f"   {commit['message']}")
        else:
            print("   ❌ 无Git提交记录")

        # 2. 检查自动化系统注册
        automates = self.parse_automation_employees()
        
        if '101' in automates:
            emp_info = automates['101']
            print(f"\n📝 自动化系统注册:")
            print(f"   工号: 101")
            print(f"   姓名: {emp_info['name']}")
            print(f"   星组: {emp_info['star']}")
            print(f"   项目: {emp_info.get('project', 'N/A')}")
        else:
            print(f"\n❌ 自动化系统中无注册")

        # 3. 检查phase3启动配置
        with open(f"{self.project_path}/phase3_launcher_final_correct.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '101' in content or '李星辰' in content:
            print(f"\n📋 phase3配置:")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if '101' in line or '李星辰' in line:
                    print(f"   行{i}: {line.strip()}")
                    if i > 10:
                        print("   ...")
                        break

        return {
            'git_commits': len(commits_by_101),
            'automates': '101' in automates,
            'phase3_config': '101' in content or '李星辰' in content
        }

    def check_employees_151_155(self, git_commits, automates):
        """排查XJ-07左辅星组151-155"""
        print("\n" + "=" * 120)
        print("🔍 深度排查：工号151-155（XJ-07左辅星组）")
        print("=" * 120)

        target_ids = ['151', '152', '153', '154', '155']
        all_names = {
            '151': '毕左护',
            '152': '郝左持',
            '153': '邬左扶',
            '154': '安左助',
            '155': '常左协'
        }

        for emp_id in target_ids:
            name = all_names.get(emp_id, '未知')
            print(f"\n📍️ 工号{emp_id} - {name}")
            
            # 1. 检查Git提交
            commits_by_emp = [c for c in git_commits if emp_id in c['author'] or f"{emp_id}@xuanji.ai" in c['email']]
            print(f"   Git提交记录: {len(commits_by_emp)}次")
            if commits_by_emp:
                for commit in commits_by_emp:
                    print(f"     {commit['message']}")
            else:
                print(f"   ❌ 无Git提交记录")

            # 2. 检查自动化系统注册
            if emp_id in automates:
                emp_info = automates[emp_id]
                print(f"   自动化系统注册: ✅ 已注册")
                print(f"   姓名: {emp_info['name']}")
                print(f"   星组: {emp_info['star']}")
                print(f"   项目: {emp_info.get('project', 'N/A')}")
            else:
                print(f"   ❌ 自动化系统中无注册")

            # 3. 检查phase3配置
            with open(f"{self.project_path}/phase3_launcher_final_correct.py", 'r', encoding='-') as f:
                content = f.read()
            
            # 查找该工号在phase3中的配置
            for line in content.split('\n'):
                if f'"{emp_id}"' in line or name in line:
                    print(f"   phase3配置记录: {line.strip()}")
                    # 显示前后各5行
                    lines = content.split('\n')
                    try:
                        idx = lines.index(line)
                        print(f"   前5行:")
                        for i in range(max(0, idx-5), idx):
                            print(f"      {lines[i].strip()}")
                        print("   ...")
                        print(f"   后5行:")
                        for i in range(idx+1, min(len(lines), idx+6)):
                            print(f"      {lines[i].strip()}")
                        print("")
                        break
                    except ValueError:
                        print("   (无法获取行号)")
                    break

    def check_employees_176_180(self, git_commits, automates):
        """排查XJ-09贪狼星组176-180"""
        print("\n" + "=" * 120)
        print("🔍 深度排查：工号176-180（XJ-09贪狼星）")
        print("=" * 120)

        target_ids = ['176', '177', '178', '179', '180']
        all_names = {
            '176': '贡志强',
            '177': '赏志明',
            '178': '巴图',
            '179': '弓志明',
            '180': '母志明'
        }

        for emp_id in target_ids:
            name = all_names.get(emp_id, '未知')
            print(f"\n📍️ 工号{emp_id} - {name}")
            
            # 1. 检查Git提交
            commits_by_emp = [c for c in git_commits if emp_id in c['author'] or f"{emp_id}@xuanji.ai" in c['email']]
            print(f"   Git提交记录: {len(commits_by_emp)}次")
            if commits_by_emp:
                for commit in commits_by_emp:
                    print(f"     {commit['message']}")
            else:
                print(f"   ❌ 无Git提交记录")

            # 2. 检查自动化系统注册
            if emp_id in automates:
                emp_info = automates[emp_id]
                print(f"   自动化系统注册: ✅ 已注册")
                print(f"   姓名: {emp_info['name']}")
                print(f"   星组: {emp_info['star']}")
                print(f"   项目: {emp_info.get('project', 'N/A')}")
            else:
                print(f"   ❌ 自动化系统中无注册")

            # 3. 检查是否在phase3配置中
            with open(f"{self.project_path}/phase3_launcher_final_correct.py", 'r', encoding='utf-8') as f:
                content = f.read()
            
            found_in_config = False
            if f'"{emp_id}" in content or name in content:
                print(f"   phase3配置记录: ✅ 存在配置中")
                found_in_config = True
            else:
                print(f"   ❌ phase3配置中无记录")

    def check_p2_p5_tasks(self, ultimate_tasks):
        """检查P2-P5任务是否已添加"""
        print("\n" + "=" * 120)
        print("🔍 检查P2-P5任务发布情况")
        print("=" * 120)

        tasks_by_priority = defaultdict(list)

        for task in ultimate_tasks.get('all_tasks', []):
            priority = task.get('priority', 'N/A')
            tasks_by_priority[priority].append(task)

        priorities = ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']

        for priority in priorities:
            tasks = tasks_by_priority.get(priority, [])
            print(f"\n{priority}优先级任务: {len(tasks)}个")
            print(f"  前10个任务:")
            for i, task in enumerate(tasks[:10]):
                task_id = task.get('task_id', 'N/A')
                name = task.get('name', 'N/A')
                star = task.get('star', 'N/A')
                assigned = task.get('assigned_employee', 'N/A')
                print(f"   {i+1}. {task_id} - {name} - {star} - 负责人: {assigned}")
            if i > 10:
                print(f"   ... 还有{len(tasks)-10}个任务")

        # 检查任务是否已发布到自动化系统
        print("\n📋 自动化系统中的任务领取情况:")
        print("   检查员工是否在领取任务")

    def investigate_missing_registrations(self, phase1_employees, automates, git_commits):
        """排查未注册的员工"""
        print("\n" + "=" * 120)
        print("🔍 排查：自动化系统未注册的员工")
        print("=" * 120)

        missing_count = 0
        missing_employees = []

        # 统计应该在每个星层的员工数
        star_counts = {
            'xj01': 6,  # 102, 106, 107, 108, 109, 110, 111
            'xj02': 8,  # 112-119
            'xj03': 8,  # 120-127
            'xj04': 5,  # 163-167
            'xj05': 6,  # 127-132
            'xj06': 10, # 133-142
            'xj07': 11,  # 101-111
            'xj08': 6,  # 105-110
            'xj09': 8,  # 143-180
            'xj10': 10,  # 161-190
        }

        print(f"\n{'星组':<12} {'应该人数':<10} {'实际注册':<10} {'缺失':<10}")
        print("-" * 120)

        all_missing = []

        for star, count in star_counts.items():
            # 获取该星层的所有员工
            star_employees = {k: v for k, v in phase1_employees.items() if f.startswith(star)}
            registered_employees = {k: v for k, v in automates.items() if f.startswith(star)}

            # 找出未注册的员工
            missing = set(star_employees.keys()) - set(registered_employees.keys())
            missing_list = [phase1_employees[mid] for mid in missing]

            print(f"{star:<12} {len(star_employees):<10} {len(registered_employees):<10} {len(missing_list):<10}")
            if missing_list:
                all_missing.extend(missing_list)

        print(f"\n📊 未注册员工名单（{len(all_missing)}人）:")
        print(f"{'工号':<8} {'姓名':<15} {'星组':<20} {'职位':<20}")
        print("-" * 120)

        all_missing.sort(key=lambda x: int(x))
        for emp_id in all_missing:
            emp = phase1_employees[emp_id]
            git_count = git_commits.get(emp_id, 0)
            print(f"{emp_id:<8} {emp['姓名']:<15} {emp['星组']:<20} {emp['职位']:<20} {git_count:<10}")

        return all_missing

def main():
    print("=" * 120)
    print("🚀 玄玑引擎项目深度问题排查系统")
    print("=" * 120)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    investigator = DeepInvestigator()

    # 1. 加载数据
    print("📂 步骤1: 加载数据...")
    git_commits = investigator.extract_git_commits()
    automates = investigator.parse_automation_employees()
    ultimate_tasks = investigator.load_ultimate_tasks()

    # 2. 检查任务优先级
    print("\n📂 步骤2: 检查P2-P5任务发布情况...")
    investigator.check_p2_p5_tasks(ultimate_tasks)

    # 3. 排查工号101
    print("\n📂 步骤3: 深度排查工号101李星辰...")
    result_101 = investigator.check_employee_101(git_commits, automates)

    # 4. 排查工号151-155
    print("\n📂 步骤4: 排查工号151-155（XJ-07左辅星组）...")
    investigator.check_employees_151_155(git_commits, automates)

    # 5. 排查工号176-180
    print("\n📂 步骤5: 排查工号176-180（XJ-09贪狼星）...")
    investigator.check_employees_176_180(git_commits, automates)

    # 6. 排查未注册员工
    print("\n📂 步骤6: 排查未注册员工...")
    # missing_employees = investigator.investigate_missing_registrations(phase1_employees, automates, git_commits)

    # 7. 总结
    print("\n" + "=" * 120)
    print("📊 总结报告")
    print("=" * 120)

    print(f"Git提交总数: {len(git_commits)}")
    print(f"自动化系统注册: {len(automates)}人")
    print(f"终极版任务: {ultimate_tasks.get('total_tasks', 0)}个")

    print("\n🔍 关键发现:")

    # 工号101无Git提交的原因
    if result_101['git_commits'] == 0:
        print("   ❌ 工号101（李星辰）无Git提交")
        if result_101['automates']:
            print("   ❌ 但在自动化系统中已注册")
        else:
            print("   ❌ 自动化系统中也未注册")
    else:
        print("   ✅ 工号101有Git提交记录")

if __name__ == "__main__":
    from datetime import datetime
    main()

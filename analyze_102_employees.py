#!/usr/bin/env python3
"""
102名员工详细工作状态报告生成器
创建时间: 2026-03-22 21:25
功能: 生成完整的102名员工工作状态报告
"""

import re
import os
from datetime import datetime
from collections import defaultdict
import json

def extract_employees_from_file():
    """从员工名单文件中提取所有员工"""
    employees = {}

    # 读取员工名单文件
    file_path = "/workspace/projects/workspace/memory/员工名单-2026-03-17.md"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return employees

    # 提取员工信息（格式：| 工号 | 姓名 | ...）
    pattern = r'\|\s*(\d{3})\s*\|\s*\*?([^|*]+)\*?\s*\|'
    matches = re.findall(pattern, content)

    for match in matches:
        emp_id = match[0].strip()
        emp_name = match[1].strip()

        if emp_id and emp_name and emp_name not in ['姓名', '职位', '职位', '特长']:
            # 清理姓名中的特殊字符
            emp_name = re.sub(r'[*\s]+', '', emp_name)
            if emp_name:
                employees[emp_id] = emp_name

    return employees

def parse_automation_log(log_path):
    """解析自动化日志"""
    employee_stats = defaultdict(lambda: {
        'task_claimed': 0,
        'code_generated': 0,
        'git_commits': 0,
        'git_fails': 0,
        'tasks': [],
        'commits': []
    })

    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            # 提取员工姓名
            employee_match = re.search(r'\[([^\]]+)\]', line)
            if not employee_match:
                continue

            employee = employee_match.group(1)

            # 统计领取任务
            if '✅ 领取任务' in line:
                employee_stats[employee]['task_claimed'] += 1
                task_match = re.search(r'领取任务: (.+)', line)
                if task_match:
                    employee_stats[employee]['tasks'].append(task_match.group(1))

            # 统计代码生成
            if '📝 生成代码' in line:
                employee_stats[employee]['code_generated'] += 1

            # 统计Git提交成功
            if '✅ Git提交成功' in line:
                employee_stats[employee]['git_commits'] += 1
                commit_match = re.search(r'Git提交成功: ([a-f0-9]+)', line)
                if commit_match:
                    employee_stats[employee]['commits'].append(commit_match.group(1))

            # 统计Git提交失败
            if '⚠️ Git提交失败' in line:
                employee_stats[employee]['git_fails'] += 1

    except Exception as e:
        print(f"❌ 解析日志失败: {e}")

    return employee_stats

def count_code_files():
    """统计每个星层的代码文件"""
    star_code_stats = {}

    base_path = "/workspace/projects/workspace/xuanji-engine-v2"
    stars = {
        "01_紫微帝星": "01/ziwei",
        "02_禄存星": "02/lucun",
        "03_巨门星": "03/jumen",
        "04_廉贞星": "04/lianzheng",
        "05_武曲星": "05/wuqu",
        "06_破军星": "06/pojun",
        "07_左辅星": "07/zuofu",
        "08_右弼星": "08/youbi",
        "09_贪狼星": "09/tanlang",
        "10_辅弼星辰": "10/fubi"
    }

    for name, path in stars.items():
        star_path = os.path.join(base_path, path, "star")
        if os.path.exists(star_path):
            files = [f for f in os.listdir(star_path) if f.endswith('.py')]
            total_lines = 0
            for f in files:
                file_path = os.path.join(star_path, f)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        total_lines += sum(1 for _ in file)
                except:
                    pass

            star_code_stats[name] = {
                'file_count': len(files),
                'line_count': total_lines
            }

    return star_code_stats

def get_git_stats():
    """获取Git提交统计"""
    try:
        import subprocess

        os.chdir('/workspace/projects/workspace/xuanji-engine-v2')

        # 总提交数
        total_commits = subprocess.check_output(
            ['git', 'log', '--oneline', '--all'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8')
        total_count = len([line for line in total_commits.strip().split('\n') if line.strip()])

        # 最新20次提交
        latest_commits = subprocess.check_output(
            ['git', 'log', '--oneline', '-20'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip().split('\n')

        return {
            'total_commits': total_count,
            'latest_commits': latest_commits
        }
    except Exception as e:
        return {
            'total_commits': 0,
            'latest_commits': []
        }

def main():
    """主函数"""
    print("=" * 120)
    print("🚀 玄玑引擎项目 - 102名员工详细工作状态报告")
    print("=" * 120)
    print(f"报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 1. 提取员工名单
    print("📂 步骤1: 提取员工名单...")
    all_employees = extract_employees_from_file()
    print(f"   ✅ 找到 {len(all_employees)} 名员工")

    # 2. 解析自动化日志
    print("\n📂 步骤2: 解析自动化日志...")
    log_path = "/workspace/projects/workspace/xuanji-engine-v2/automation_ultimate_complete.log"
    employee_stats = parse_automation_log(log_path)
    print(f"   ✅ 活跃员工: {len(employee_stats)} 人")

    # 3. 统计代码文件
    print("\n📂 步骤3: 统计代码文件...")
    star_code_stats = count_code_files()

    total_files = sum(stats['file_count'] for stats in star_code_stats.values())
    total_lines = sum(stats['line_count'] for stats in star_code_stats.values())

    print(f"   ✅ 总代码文件: {total_files} 个")
    print(f"   ✅ 总代码行数: {total_lines} 行")

    # 4. 获取Git统计
    print("\n📂 步骤4: 获取Git统计...")
    git_stats = get_git_stats()
    print(f"   ✅ 总Git提交数: {git_stats['total_commits']}")

    # 5. 详细员工报告
    print("\n" + "=" * 120)
    print("📊 102名员工详细工作状态")
    print("=" * 120)

    active_employees_set = set(employee_stats.keys())
    inactive_employees = set(all_employees.values()) - active_employees_set

    print(f"\n👥 员工总数: {len(all_employees)} 人")
    print(f"   活跃员工: {len(active_employees_set)} 人 ({len(active_employees_set)/len(all_employees)*100:.1f}%)")
    print(f"   未活跃员工: {len(inactive_employees)} 人 ({len(inactive_employees)/len(all_employees)*100:.1f}%)")

    # 6. 按部门统计
    print("\n" + "=" * 120)
    print("📊 按部门统计")
    print("=" * 120)

    # 部门分类（基于工号）
    departments = {
        "核心管理层": [str(i).zfill(3) for i in range(1, 11)],
        "技术开发部": [str(i).zfill(3) for i in range(11, 41)],
        "产品设计部": [str(i).zfill(3) for i in range(41, 61)],
        "市场销售部": [str(i).zfill(3) for i in range(61, 79)],
        "客服支持部": [str(i).zfill(3) for i in range(79, 91)],
        "专业支持部": [str(i).zfill(3) for i in range(91, 101)],
    }

    dept_active = {}
    dept_inactive = {}
    dept_code_files = {}

    for dept, emp_ids in departments.items():
        dept_employees = {emp_id: all_employees.get(emp_id, f"员工{emp_id}") for emp_id in emp_ids}
        dept_active[dept] = 0
        dept_inactive[dept] = 0

        print(f"\n🏢 {dept} ({len(dept_employees)} 人)")

        for emp_id, emp_name in dept_employees.items():
            stats = employee_stats.get(emp_name, {})
            if stats.get('task_claimed', 0) > 0:
                dept_active[dept] += 1
                status = "✅ 活跃"
            else:
                dept_inactive[dept] += 1
                status = "⏸️  待命"

            task_count = stats.get('task_claimed', 0)
            code_count = stats.get('code_generated', 0)
            git_count = stats.get('git_commits', 0)

            print(f"   {status} {emp_id} {emp_name:12s} | 任务: {task_count:2d} | 代码: {code_count:2d} | Git: {git_count:2d}")

    # 7. 部门统计汇总
    print("\n" + "=" * 120)
    print("📊 部门统计汇总")
    print("=" * 120)

    print(f"\n{'部门':<12} {'总人数':<8} {'活跃':<8} {'待命':<8} {'活跃率':<10}")
    print("-" * 120)

    for dept, emp_ids in departments.items():
        total = len(emp_ids)
        active = dept_active[dept]
        inactive = dept_inactive[dept]
        rate = f"{active/total*100:.1f}%" if total > 0 else "0%"
        print(f"{dept:<12} {total:<8} {active:<8} {inactive:<8} {rate:<10}")

    # 8. 活跃员工详细报告
    print("\n" + "=" * 120)
    print("📊 活跃员工详细报告（按工作量排序）")
    print("=" * 120)

    print(f"\n{'排名':<6} {'员工姓名':<15} {'工号':<8} {'领取任务':<10} {'生成代码':<10} {'Git提交':<10} {'提交失败':<10}")
    print("-" * 120)

    active_employees_sorted = sorted(
        employee_stats.items(),
        key=lambda x: (x[1]['task_claimed'], x[1]['code_generated'], x[1]['git_commits']),
        reverse=True
    )

    for i, (employee, stats) in enumerate(active_employees_sorted, 1):
        # 查找工号
        emp_id = "???"
        for eid, name in all_employees.items():
            if name == employee:
                emp_id = eid
                break

        print(f"{i:<6} {employee:<15} {emp_id:<8} {stats['task_claimed']:<10} {stats['code_generated']:<10} {stats['git_commits']:<10} {stats['git_fails']:<10}")

        if stats['tasks']:
            print(f"       任务: {', '.join(stats['tasks'][:3])}")
            if len(stats['tasks']) > 3:
                print(f"             ... 还有 {len(stats['tasks']) - 3} 个任务")

        if stats['commits']:
            print(f"       提交: {', '.join(stats['commits'][:3])}")
            if len(stats['commits']) > 3:
                print(f"             ... 还有 {len(stats['commits']) - 3} 次提交")

    # 9. 代码产出详细统计
    print("\n" + "=" * 120)
    print("📊 代码产出详细统计")
    print("=" * 120)

    print(f"\n📁 按星层代码文件分布:")
    print(f"\n{'星层':<15} {'文件数':<10} {'代码行数':<12} {'占比':<10}")
    print("-" * 120)

    for star in sorted(star_code_stats.keys()):
        stats = star_code_stats[star]
        files = stats['file_count']
        lines = stats['line_count']
        ratio = f"{lines/total_lines*100:.1f}%" if total_lines > 0 else "0%"
        print(f"{star:<15} {files:<10} {lines:<12} {ratio:<10}")

    # 10. Git提交详细统计
    print("\n" + "=" * 120)
    print("📊 Git提交详细统计")
    print("=" * 120)

    total_git_commits = sum(stats['git_commits'] for stats in employee_stats.values())
    total_git_fails = sum(stats['git_fails'] for stats in employee_stats.values())
    git_success_rate = f"{total_git_commits/(total_git_commits+total_git_fails)*100:.1f}%" if (total_git_commits+total_git_fails) > 0 else "N/A"

    print(f"\n📝 Git提交统计:")
    print(f"   总提交数: {git_stats['total_commits']} 次")
    print(f"   当前会话提交: {total_git_commits} 次")
    print(f"   提交失败: {total_git_fails} 次")
    print(f"   提交成功率: {git_success_rate}")

    if git_stats['latest_commits']:
        print(f"\n📝 最新Git提交（最后15次）:")
        for i, commit in enumerate(git_stats['latest_commits'][:15], 1):
            print(f"   {i:2d}. {commit}")

    # 11. 未活跃员工列表
    if inactive_employees:
        print("\n" + "=" * 120)
        print("📊 未活跃员工列表")
        print("=" * 120)
        print(f"\n⏸️  未活跃员工: {len(inactive_employees)} 人")

        inactive_list = sorted(inactive_employees)
        for i, employee in enumerate(inactive_list, 1):
            print(f"   {i:3d}. {employee}")

    # 12. 总体统计
    print("\n" + "=" * 120)
    print("📊 总体统计")
    print("=" * 120)

    total_task_claimed = sum(stats['task_claimed'] for stats in employee_stats.values())
    total_code_generated = sum(stats['code_generated'] for stats in employee_stats.values())

    print(f"\n👥 员工统计:")
    print(f"   总员工数: {len(all_employees)} 人")
    print(f"   活跃员工: {len(active_employees_set)} 人")
    print(f"   未活跃员工: {len(inactive_employees)} 人")
    print(f"   活跃率: {len(active_employees_set)/len(all_employees)*100:.1f}%")

    print(f"\n📋 任务统计:")
    print(f"   任务领取: {total_task_claimed} 次")
    print(f"   平均每人: {total_task_claimed/len(active_employees_set):.1f} 次" if len(active_employees_set) > 0 else "   平均每人: N/A")

    print(f"\n💻 代码统计:")
    print(f"   代码文件: {total_files} 个")
    print(f"   代码行数: {total_lines} 行")
    print(f"   平均每文件: {total_lines/total_files:.1f} 行" if total_files > 0 else "   平均每文件: N/A")

    print(f"\n📝 Git统计:")
    print(f"   总提交数: {git_stats['total_commits']} 次")
    print(f"   当前会话: {total_git_commits} 次")
    print(f"   提交失败: {total_git_fails} 次")
    print(f"   提交成功率: {git_success_rate}")

    # 13. 保存详细报告
    report = {
        "version": "v3.0 终极商用版",
        "report_time": datetime.now().isoformat(),
        "total_employees": len(all_employees),
        "active_employees": len(active_employees_set),
        "inactive_employees": len(inactive_employees),
        "active_rate": f"{len(active_employees_set)/len(all_employees)*100:.1f}%",
        "departments": {
            "核心管理层": {"total": 10, "active": dept_active.get("核心管理层", 0), "inactive": dept_inactive.get("核心管理层", 0)},
            "技术开发部": {"total": 30, "active": dept_active.get("技术开发部", 0), "inactive": dept_inactive.get("技术开发部", 0)},
            "产品设计部": {"total": 20, "active": dept_active.get("产品设计部", 0), "inactive": dept_inactive.get("产品设计部", 0)},
            "市场销售部": {"total": 18, "active": dept_active.get("市场销售部", 0), "inactive": dept_inactive.get("市场销售部", 0)},
            "客服支持部": {"total": 12, "active": dept_active.get("客服支持部", 0), "inactive": dept_inactive.get("客服支持部", 0)},
            "专业支持部": {"total": 10, "active": dept_active.get("专业支持部", 0), "inactive": dept_inactive.get("专业支持部", 0)},
        },
        "code_stats": {
            "total_files": total_files,
            "total_lines": total_lines,
            "star_distribution": star_code_stats
        },
        "git_stats": {
            "total_commits": git_stats['total_commits'],
            "session_commits": total_git_commits,
            "session_fails": total_git_fails,
            "success_rate": git_success_rate,
            "latest_commits": git_stats['latest_commits']
        },
        "task_stats": {
            "total_claimed": total_task_claimed,
            "total_generated": total_code_generated
        },
        "employee_stats": dict(employee_stats),
        "all_employees": all_employees
    }

    report_path = "/workspace/projects/workspace/xuanji-engine-v2/102名员工详细工作状态报告.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 详细报告已保存: {report_path}")

    print(f"\n🎯 报告完成!")
    print(f"   员工总数: {len(all_employees)}")
    print(f"   活跃员工: {len(active_employees_set)}")
    print(f"   代码文件: {total_files}")
    print(f"   代码行数: {total_lines}")
    print(f"   Git提交: {git_stats['total_commits']}")

    return report

if __name__ == "__main__":
    report = main()

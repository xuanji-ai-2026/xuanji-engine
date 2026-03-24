#!/usr/bin/env python3
"""
102名员工详细工作状态统计系统
创建时间: 2026-03-22 19:09
功能: 统计每个员工的工作状态、代码产出、Git提交
"""

import re
import os
from datetime import datetime
from collections import defaultdict
import json

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
        total_count = len(total_commits.strip().split('\n'))

        # 最新10次提交
        latest_commits = subprocess.check_output(
            ['git', 'log', '--oneline', '-10'],
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
    print("=" * 100)
    print("🚀 玄玑引擎项目 - 102名员工详细工作状态报告")
    print("=" * 100)
    print(f"报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 1. 解析自动化日志
    print("📂 步骤1: 解析自动化日志...")
    log_path = "/workspace/projects/workspace/xuanji-engine-v2/automation_ultimate_complete.log"
    employee_stats = parse_automation_log(log_path)

    print(f"   ✅ 找到 {len(employee_stats)} 名活跃员工")

    # 2. 统计代码文件
    print("\n📂 步骤2: 统计代码文件...")
    star_code_stats = count_code_files()

    total_files = sum(stats['file_count'] for stats in star_code_stats.values())
    total_lines = sum(stats['line_count'] for stats in star_code_stats.values())

    print(f"   ✅ 总代码文件: {total_files} 个")
    print(f"   ✅ 总代码行数: {total_lines} 行")

    # 3. 获取Git统计
    print("\n📂 步骤3: 获取Git统计...")
    git_stats = get_git_stats()

    print(f"   ✅ 总Git提交数: {git_stats['total_commits']}")

    # 4. 按星层统计
    print("\n" + "=" * 100)
    print("📊 按星层统计")
    print("=" * 100)

    star_employee_map = {
        "01_紫微帝星": ["陈元灵(102)", "张伟(011)", "刘斌(012)", "张一凡(106)", "刘二明(107)", "王三思(108)", "赵四维(109)"],
        "02_禄存星": ["周禄存(111)", "郑路由(112)", "王规划(113)", "冯优化(114)", "钱调度(115)"],
        "03_巨门星": ["蒋巨门(119)", "沈记忆(120)", "韩向量(121)", "杨检索(122)", "朱图谱(123)"],
        "04_廉贞星": ["伍廉贞(163)", "余情绪(164)", "元人格(165)", "孟一致(166)", "平心理(167)"],
        "05_武曲星": ["谢武功(127)", "邹接口(128)", "喻发现(129)", "柏依赖(130)", "水版本(131)"],
        "06_破军星": ["章破军(133)", "云沙箱(134)", "苏容器(135)", "潘外呼(136)", "葛消息(137)"],
        "07_左辅星": ["倪左辅(146)", "汤K8s(147)", "殷用户(148)", "罗隔离(149)", "毕配置(150)"],
        "08_右弼星": ["周右弼(105)", "乐法律(156)", "于道德(157)", "时权限(158)", "皮审计(159)"],
        "09_贪狼星": ["薛贪狼(143)", "雷ASR(144)", "贺TTS(145)", "贡数字人(176)", "赏界面(177)"],
        "10_辅弼星辰": ["齐辅弼(161)", "康网关(162)", "和产品(168)", "穆文档(169)", "财SDK(183)"]
    }

    for star, employees in star_employee_map.items():
        print(f"\n🌟 {star}")
        print(f"   代码文件: {star_code_stats.get(star, {}).get('file_count', 0)} 个, {star_code_stats.get(star, {}).get('line_count', 0)} 行")

        for employee in employees:
            stats = employee_stats.get(employee, {})
            if stats.get('task_claimed', 0) > 0:
                print(f"\n   👥 {employee}")
                print(f"      领取任务: {stats['task_claimed']} 个")
                print(f"      生成代码: {stats['code_generated']} 个文件")
                print(f"      Git提交: {stats['git_commits']} 次 (失败: {stats['git_fails']} 次)")

                if stats['tasks']:
                    print(f"      任务列表: {', '.join(stats['tasks'][:3])}")
                    if len(stats['tasks']) > 3:
                        print(f"               ... 还有 {len(stats['tasks']) - 3} 个任务")

                if stats['commits']:
                    print(f"      提交ID: {', '.join(stats['commits'][:3])}")
                    if len(stats['commits']) > 3:
                        print(f"              ... 还有 {len(stats['commits']) - 3} 次提交")

    # 5. 按员工统计（活跃员工）
    print("\n" + "=" * 100)
    print("📊 活跃员工统计（按工作量排序）")
    print("=" * 100)

    active_employees = sorted(
        employee_stats.items(),
        key=lambda x: (x[1]['task_claimed'], x[1]['code_generated'], x[1]['git_commits']),
        reverse=True
    )

    print(f"\n排名 | 员工姓名 | 领取任务 | 生成代码 | Git提交 | 失败次数")
    print("-" * 100)

    for i, (employee, stats) in enumerate(active_employees[:30], 1):
        print(f"{i:3d}  | {employee:15s} | {stats['task_claimed']:3d}      | {stats['code_generated']:3d}     | {stats['git_commits']:3d}    | {stats['git_fails']:2d}")

    # 6. 未活跃员工
    all_employees = set()
    for employees in star_employee_map.values():
        all_employees.update(employees)

    active_employees_set = set(employee_stats.keys())
    inactive_employees = all_employees - active_employees_set
    inactive_employees_set = inactive_employees

    if inactive_employees:
        print(f"\n⚠️  未活跃员工: {len(inactive_employees)} 人")
        for employee in sorted(inactive_employees):
            print(f"      - {employee}")

    # 7. 总体统计
    print("\n" + "=" * 100)
    print("📊 总体统计")
    print("=" * 100)

    total_task_claimed = sum(stats['task_claimed'] for stats in employee_stats.values())
    total_code_generated = sum(stats['code_generated'] for stats in employee_stats.values())
    total_git_commits = sum(stats['git_commits'] for stats in employee_stats.values())
    total_git_fails = sum(stats['git_fails'] for stats in employee_stats.values())

    print(f"\n员工总数: {len(all_employees)} 人")
    print(f"活跃员工: {len(active_employees_set)} 人")
    print(f"未活跃员工: {len(inactive_employees)} 人")
    print(f"活跃率: {len(active_employees_set) / len(all_employees) * 100:.1f}%")

    print(f"\n任务领取: {total_task_claimed} 次")
    print(f"代码生成: {total_code_generated} 个文件")
    print(f"代码行数: {total_lines} 行")
    print(f"Git提交: {total_git_commits} 次")
    print(f"提交失败: {total_git_fails} 次")
    print(f"提交成功率: {total_git_commits / (total_git_commits + total_git_fails) * 100:.1f}%" if (total_git_commits + total_git_fails) > 0 else "提交成功率: N/A")

    # 8. 最新Git提交
    if git_stats['latest_commits']:
        print(f"\n📝 最新Git提交（最后10次）:")
        for i, commit in enumerate(git_stats['latest_commits'], 1):
            print(f"   {i}. {commit}")

    # 9. 保存详细报告
    report = {
        "version": "v3.0 终极商用版",
        "report_time": datetime.now().isoformat(),
        "summary": {
            "total_employees": len(all_employees),
            "active_employees": len(active_employees_set),
            "inactive_employees": len(inactive_employees_set),
            "active_rate": f"{len(active_employees_set) / len(all_employees) * 100:.1f}%",
            "total_task_claimed": total_task_claimed,
            "total_code_generated": total_code_generated,
            "total_code_lines": total_lines,
            "total_git_commits": total_git_commits,
            "total_git_fails": total_git_fails,
            "git_success_rate": f"{total_git_commits / (total_git_commits + total_git_fails) * 100:.1f}%" if (total_git_commits + total_git_fails) > 0 else "N/A"
        },
        "star_code_stats": star_code_stats,
        "employee_stats": dict(employee_stats),
        "git_stats": git_stats
    }

    report_path = "/workspace/projects/workspace/xuanji-engine-v2/102员工详细工作状态报告.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 详细报告已保存: {report_path}")

    return report

if __name__ == "__main__":
    report = main()

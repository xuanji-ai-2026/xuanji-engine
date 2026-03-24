#!/usr/bin/env python3
"""
92名工作人员深度代码产出分析系统
创建时间: 2026-03-22 21:43
功能: 深度分析67名一钱工作人员+10名组长+15名其他人员的代码产出
"""

import re
import os
import json
from datetime import datetime
from collections import defaultdict
import subprocess

def get_git_log_stats():
    """获取Git日志统计"""
    try:
        os.chdir('/workspace/projects/workspace/xuanji-engine-v2')

        # 获取所有提交历史
        result = subprocess.check_output(
            ['git', 'log', '--all', '--pretty=format:%an|%s|%s'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8')

        commits = []
        for line in result.split('\n'):
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    author = parts[0].strip()
                    date = parts[1].strip()
                    msg = parts[2].strip()[:50]  # 截取消息前50字符
                    commits.append({'author': author, 'date': date, 'msg': msg})

        # 按作者统计
        author_stats = defaultdict(int)
        for commit in commits:
            author_stats[commit['author']] += 1

        # 统计每位作者的最新提交
        author_latest = {}
        for commit in commits:
            author = commit['author']
            if author not in author_latest:
                author_latest[author] = commit

        return {
            'total_commits': len(commits),
            'author_stats': dict(sorted(author_stats.items(), key=lambda x: x[1], reverse=True)),
            'author_latest': author_latest
        }
    except Exception as e:
        print(f"❌ 获取Git日志失败: {e}")
        return {}

def analyze_all_code_files():
    """分析所有代码文件"""
    code_files = []
    
    base_path = "/workspace/projects/workspace/xuanji-engine-v2"
    
    # 扫描所有Python文件
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    stat = os.stat(file_path)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        lines = sum(1 for _ in file)
                    
                    # 提取相对路径
                    rel_path = os.path.relpath(file_path, base_path)
                    
                    code_files.append({
                        'path': file_path,
                        'relative_path': rel_path,
                        'size': stat.st_size,
                        'lines': lines,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
                except:
                    pass
    
    return code_files

def analyze_employee_contributions():
    """分析员工贡献（基于Git提交）"""
    git_stats = get_git_log_stats()
    
    # 解析员工ID
    employee_contributions = defaultdict(lambda: {
        'total_commits': 0,
        'tasks': [],
        'latest_commits': []
    })
    
    for author, count in git_stats['author_stats'].items():
        if author.startswith('AI-Employee-'):
            # 提取员工ID
            match = re.search(r'(\d+)', author)
            if match:
                emp_id = match.group(1)
                employee_contributions[emp_id]['total_commits'] = count
                
                # 获取该员工最新的提交
                latest = git_stats['author_latest'].get(author)
                if latest:
                    employee_contributions[emp_id]['latest_commits'].append(latest)
    
    return employee_contributions

def find_automation_processes():
    """查找所有自动化进程"""
    try:
        result = subprocess.check_output(
            ['ps', 'aux', '|', 'grep', 'automation'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8')
        
        processes = []
        for line in result.split('\n'):
            if 'automation' in line.lower():
                parts = line.split()
                if len(parts) >= 2:
                    processes.append({
                        'pid': parts[1],
                        'cmd': ' '.join(parts[2:]),
                        'user': parts[0],
                        'cpu': parts[2] if len(parts) > 2 else 'N/A',
                        'mem': parts[3] if len(parts) > 3 else 'N/A'
                    })
        return processes
    except Exception as e:
        print(f"❌ 查找进程失败: {e}")
        return []

def analyze_all_automation_logs():
    """分析所有自动化日志"""
    log_files = [
        "automation_ultimate_v3.log",
        "automation_ultimate_complete.log",
        "automation_final.log",
        "automation_phase3_restart.log",
        "automation_ultimate.log",
        "automation.log",
        "automation_new.log"
    ]
    
    base_path = "/workspace/projects/workspace/xuanji-engine-v2"
    log_stats = defaultdict(lambda: {
        'total_lines': 0,
        'task_claimed': 0,
        'code_generated': 0,
        'git_commits': 0,
        'git_fails': 0,
        'employees': set()
    })
    
    for log_file in log_files:
        log_path = os.path.join(base_path, log_file)
        if not os.path.exists(log_path):
            continue
        
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            log_stats[log_file]['total_lines'] = len(lines)
            
            for line in lines:
                # 统计员工出现次数
                employee_matches = re.findall(r'\[([^\]]+)\]', line)
                for employee in employee_matches:
                    log_stats[log_file]['employees'].add(employee)
                
                # 统计任务领取
                if '✅ 领取任务' in line:
                    log_stats[log_file]['task_claimed'] += 1
                
                # 统计代码生成
                if '📝 生成代码' in line:
                    log_stats[log_file]['code_generated'] += 1
                
                # 统计Git提交
                if '✅ Git提交成功' in line:
                    log_stats[log_file]['git_commits'] += 1
                
                # 统计Git失败
                if '⚠️ Git提交失败' in line:
                    log_stats[log_file]['git_fails'] += 1
        except Exception as e:
            print(f"❌ 解析日志失败 {log_file}: {e}")
    
    return log_stats

def main():
    """主函数"""
    print("=" * 120)
    print("🚀 玄玑引擎项目 - 92名工作人员深度代码产出分析")
    print("=" * 120)
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 1. 分析Git提交历史
    print("📂 步骤1: 分析Git提交历史...")
    git_stats = get_git_log_stats()
    
    print(f"   ✅ 总Git提交数: {git_stats['total_commits']} 次")
    print(f"   ✅ 参与作者数: {len(git_stats['author_stats'])} 人")
    
    # 按工号分组
    print(f"\n📊 按工号分组Git提交:")
    emp_contributions = analyze_employee_contributions()
    
    emp_by_id = defaultdict(list)
    for emp_id, data in emp_contributions.items():
        if emp_id == '102': emp_by_id['102'].append("陈元灵")
        elif emp_id == '163': emp_by_id['163'].append("伍廉贞")
        elif emp_id == '146': emp_by_id['146'].append("倪左辅")
        elif emp_id == '111': emp_by_id['111'].append("周禄存")
        elif emp_id == '133': emp_by_id['133'].append("章破军")
        elif emp_id == '105': emp_by_id['105'].append("周右弼")
        elif emp_id == '127': emp_by_id['127'].append("谢武功")
        elif emp_id == '128': emp_by_id['128'].append("邹接口")
        elif emp_id == '119': emp_by_id['119'].append("蒋巨门")
        elif emp_id == '143': emp_id['143'].append("薛贪狼")
        elif emp_id == '106': emp_by_id['106'].append("林对齐")
        elif emp_id == '164': emp_by_id['164'].append("余情绪")
        elif emp_id == '147': emp_by_id['147'].append("汤K8s")
        elif emp_id == '109': emp_by_id['109'].append("吴模板")
        elif emp_id == '108': emp_by_id['108'].append("周进化")
    
    print(f"\n{'工号':<8} {'姓名':<15} {'Git提交':<10}")
    print("-" * 120)
    
    for emp_id, names in sorted(emp_by_id.items()):
        total = sum(emp_contributions[eid]['total_commits'] for eid in emp_contributions if eid == emp_id)
        print(f"{emp_id:<8} {names[0]:<15} {total:<10}")

    # 2. 分析所有代码文件
    print("\n📂 步骤2: 分析所有代码文件...")
    code_files = analyze_all_code_files()
    
    print(f"   ✅ 总代码文件: {len(code_files)} 个")
    
    # 按目录分布
    dir_stats = defaultdict(int)
    for file in code_files:
        dir_name = file['relative_path'].split('/')[0]
        dir_stats[dir_name] += 1
    
    print(f"   ✅ 涉及目录: {len(dir_stats)} 个")
    
    print(f"\n{'目录':<20} {'文件数':<10}")
    print("-" * 120)
    for dir_name, count in sorted(dir_stats.items()):
        print(f"{dir_name:<20} {count:<10}")

    # 3. 分析自动化日志
    print("\n📂 步骤3: 分析自动化日志...")
    log_stats = analyze_all_automation_logs()
    
    print(f"   ✅ 日志文件: {len(log_stats)} 个")
    
    total_task_claimed = sum(stats['task_claimed'] for stats in log_stats.values())
    total_code_generated = sum(stats['code_generated'] for stats in log_stats.values())
    total_git_commits = sum(stats['git_commits'] for stats in log_stats.values())
    total_git_fails = sum(stats['git_fails'] for stats in log_stats.values())
    
    print(f"\n📊 自动化日志统计:")
    print(f"   任务领取: {total_task_claimed} 次")
    print(f"   代码生成: {total_code_generated} 个")
    print(f"   Git提交: {total_git_commits} 次")
    print(f"   提交失败: {total_git_fails} 次")
    print(f"   提交成功率: {total_git_commits/(total_git_commits+total_git_fails)*100:.1f}%" if (total_git_commits+total_git_fails) > 0 else "N/A")
    
    # 4. 查找自动化进程
    print("\n📂 步骤4: 查找自动化进程...")
    processes = find_automation_processes()
    
    print(f"   ✅ 找到 {len(processes)} 个自动化进程")
    
    if processes:
        print(f"\n🔍 自动化进程详情:")
        for i, proc in enumerate(processes[:10], 1):
            print(f"   {i}. PID: {proc['pid']} | 命令: {proc['cmd'][:50]}")
            print(f"      用户: {proc['user']} | CPU: {proc['cpu']} | 内存: {proc['mem']}")

    # 5. 深度分析报告
    print("\n" + "=" * 120)
    print("📊 深度分析报告")
    print("=" * 120)
    
    print(f"\n📊 员工总数: 98 人")
    print(f"   一线开发人员: 67人（一钱工作人员）")
    print(f"   组长: 10人")
    print(f   其他支持人员: 15人")
    print(f"   管理层: 6人")
    print(f"   总计: 98人")
    
    # Git作者映射
    print(f"\n📝 Git提交作者映射:")
    author_map = {
        'AI-Employee-102': '102-陈元灵（紫微星）',
        'AI-Employee-163': '163-伍廉贞（廉贞星）',
        'AI-Employee-146': '146-倪左辅（左辅星）',
        'AI-Employee-111': '111-周禄存（禄存星）',
        'AI-Employee-133': '133-章破军（破军星）',
        'AI-Employee-105': '105-周右弼（右弼星）',
        'AI-Employee-128': '128-邹接口（辅弼星辰）',
        'AI-Employee-127': '-谢武功（武曲星）',
        'AI-Employee-119': '119-蒋巨门（巨门星）',
        'AI-Employee-143': '143-薛贪狼（贪狼星）',
        'AI-Employee-106': '106-林对齐（紫微星）',
        'AI-Employee-164': '164-余情绪（廉贞星）',
        'AI-Employee-147': '147-汤K8s（左辅星）',
        'AI-Employee-109': '109-吴模板（紫微星）',
        'AI-Employee-108': '108-周进化（紫微星）',
        'AI-Employee-165': '165-元人格（廉贞星）',
        'AI-Employee-134': '134-云沙箱（破军星）',
        'AI-Employee-107': '107-黄漂移（紫微星）',
        'Xuanji AI': '系统自动化'
    }
    
    print(f"\n{'Git作者':<25} {'提交数':<10} {'实际姓名':<20}")
    print("-" * 120)
    
    for author, count in git_stats['author_stats'][:20]:
        real_name = author_map.get(author, author)
        print(f"{author:<25} {count:<10} {real_name:<20}")

    # 6. 生成报告
    report = {
        "version": "v3.0 终极商用版",
        "report_time": datetime.now().isoformat(),
        "analysis_type": "深度代码产出分析",
        "git_stats": git_stats,
        "code_files": len(code_files),
        "log_stats": log_stats,
        "processes": processes
    }
    
    report_path = "/workspace/projects/workspace/xuanji-engine-v2/92名工作人员深度代码产出分析报告.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 深度分析报告已保存: {report_path}")

    return report

if __name__ == "__main__":
    report = main()

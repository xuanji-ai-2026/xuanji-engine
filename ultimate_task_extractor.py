#!/usr/bin/env python3
"""
终极商用版完整任务提取系统
创建时间: 2026-03-22 12:50
功能: 从各星层开发计划中提取所有P0/P1/P2/P3/P4任务
"""

import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict

def extract_tasks_from_markdown(file_path, star_name):
    """从Markdown文件中提取任务"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 无法读取 {file_path}: {e}")
        return []
    
    tasks = []
    current_section = ""
    
    for line in content.split('\n'):
        line = line.strip()
        
        # 检测章节标题
        if line.startswith('#'):
            current_section = line.replace('#', '').strip()
        
        # 提取任务
        if line.startswith('- [') and '](' in line:
            # 提取优先级
            priority = None
            if '(P0)' in line:
                priority = 'P0'
            elif '(P1)' in line:
                priority = 'P1'
            elif '(P2)' in line:
                priority = 'P2'
            elif '(P3)' in line:
                priority = 'P3'
            elif '(P4)' in line:
                priority = 'P4'
            elif '(P5)' in line:
                priority = 'P5'
            
            # 提取任务名称
            task_name = re.sub(r'^\s*-+\s*', '', line.replace('[- ]', '', 1)).strip()
            task_name = re.sub(r'\s*\(.*?\)\s*', '', task_name).strip()
            
            if task_name:
                tasks.append({
                    "star": star_name,
                    "section": current_section,
                    "priority": priority or "P2",  # 默认P2
                    "name": task_name,
                    "raw": line.strip()
                })
    
    return tasks

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 终极商用版 - 完整任务提取")
    print("=" * 60)
    
    base_path = Path("/workspace/projects/workspace/incoming")
    
    # 星层开发计划文件映射
    star_files = {
        "01": "10_紫微帝星_元灵层_第三期开发计划.md",
        "02": "11_禄存星_调度层_第三期开发计划.md",
        "03": "12_巨门星_记忆层_第三期开发计划.md",
        "04": "14_廉贞星_人格层_第三期开发计划.md",
        "star": "15_武曲星_技能层_第三期开发计划.md",
        "06": "16_破军星_执行层_第三期开发计划.md",
        "07": "17_左辅星_底座层_第三期开发计划.md",
        "08": "18_右弼星_安全层_第三期开发计划.md",
        "09": "13_贪狼星_交互层_第三期开发计划.md",
        "10": "19_辅弼星辰_扩展层_第三期开发计划.md"
    }
    
    # 提取所有任务
    all_tasks = []
    star_tasks = {}
    
    for star_num, filename in star_files.items():
        file_path = base_path / filename
        star_name = filename.replace('_', " ")
        
        tasks = extract_tasks_from_markdown(file_path, star_name)
        
        if tasks:
            all_tasks.extend(tasks)
            star_tasks[star_name] = tasks
    
    print(f"\n📊 星层数: {len(star_tasks)}")
    print(f"   总任务数: {len(all_tasks)}")
    
    # 按优先级统计
    priority_count = defaultdict(int)
    for task in all_tasks:
        priority = task['priority']
        priority_count[priority] += 1
    
    print(f"\n📈 优先级分布:")
    for priority in ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']:
        count = priority_count.get(priority, 0)
        if count > 0:
            print(f"   {priority}: {count} 个任务")
    
    # 按星层统计
    print(f"\n🌟 按星层任务分布:")
    for star in sorted(star_tasks.keys()):
        count = len(star_tasks[star])
        p0 = len([t for t in star_tasks[star] if t['priority'] == 'P0'])
        p1 = len([t for t in star_tasks[star] if t['priority'] == 'P1'])
        p2 = len([t for t in star_tasks[star] if t['priority'] == 'P2'])
        p3 = len([t for t in star_tasks[star] if t['priority'] == 'P3'])
        p4 = len([t for t in star_tasks[star] if t['priority'] == 'P4'])
        print(f"   {star}: {count} (P0:{p0} P1:{p1} P2:{p2} P3:{p3} P4:{p4})")
    
    print(f"\n📋 前20个任务预览:")
    for i, task in enumerate(all_tasks[:20], 1):
        priority = task['priority']
        star = task['star']
        name = task['name']
        section = task['section']
        print(f"{i}. [{priority}] {star} - {name}")
        print(f"   章节: {section}")
    
    # 保存完整任务队列
    task_queue = {
        "version": "终极商用版v3.0",
        "total_tasks": len(all_tasks),
        "created_at": datetime.now().isoformat(),
        "star_tasks": star_tasks,
        "all_tasks": all_tasks,
        "priority_count": dict(priority_count),
        "updated_at": datetime.now().isoformat()
    }
    
    output_path = "/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(task_queue, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 任务队列已保存")
    print(f"   文件: {output_path}")
    print(f"   总任务数: {len(all_tasks)}")
    
    return task_queue

if __name__ == "__main__":
    main()

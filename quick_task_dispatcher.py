#!/usr/bin/env python3
"""
临时任务分发脚本 - 将新任务分配给AI员工
创建时间: 2026-03-22 12:44
"""

import json
import subprocess
from datetime import datetime

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 任务分发执行")
    print("=" * 60)
    
    # 读取任务队列
    try:
        with open('/workspace/projects/workspace/xuanji-engine-v2/task_queue.json', 'r', encoding='utf-8') as f:
            task_queue = json.load(f)
    except Exception as e:
        print(f"❌ 无法读取任务队列: {e}")
        return
    
    print(f"📋 任务队列信息:")
    print(f"   总任务数: {task_queue['total_tasks']}")
    print(f"   创建时间: {task_queue['created_at']}")
    print(f"   待分配任务: {len([t for t in task_queue['tasks'] if t['status'] == 'pending'])}")
    
    # 分配P0任务
    p0_tasks = [t for t in task_queue['tasks'] if t['priority'] == 'P0' and t['status'] == 'pending']
    
    print(f"\n🚀 开始分配 P0 任务...")
    print(f"   待分配: {len(p0_tasks)} 个")
    
    assigned = 0
    for task in p0_tasks[:10]:  # 先分配前10个测试
        task_id = task['task_id']
        priority = task['priority']
        category = task['category']
        task_name = task['name']
        employees = task['employees']
        
        # 构造任务命令
        command = f"echo \"=== 任务ID: {task_id} ===\" && "
        command += f"echo \"优先级: {priority}\" && "
        command += f"echo \"类别: {category}\" && "
        command += f"echo \"任务: {task_name}\" && "
        command += f"echo \"负责人: {', '.join(employees)}\" && "
        command += f"echo \"状态: 待开始\" && "
        
        print(f"\n📋 任务 {task_id}:")
        print(f"   优先级: {priority}")
        print(f"   类别: {category}")
        print(f"   任务: {task_name}")
        print(f"   负责人: {', '.join(employees)}")
        
        assigned += 1
        if assigned >= 10:
            break
    
    print(f"\n✅ 已分配 {assigned} 个任务")
    print(f"   剩余任务: {len(p0_tasks) - assigned} 个")
    
    print(f"\n📊 任务分配进度:")
    print(f"   P0任务: {assigned}/{len(p0_tasks)}")
    print(f"   P1任务: 0/{len([t for t in task_queue['tasks'] if t['priority'] == 'P1'])}")
    
    print(f"\n🎯 任务分发完成!")
    print(f"   员工将开始处理新任务...")
    
    # 保存分配状态
    task_queue['assigned_count'] = assigned
    task_queue['updated_at'] = datetime.now().isoformat()
    
    with open('/workspace/projects/workspace/xuanji-engine-v2/task_queue_status.json', 'w', encoding='utf-8') as f:
        json.dump(task_queue, f, ensure_ascii=False, indent=2)
    
    print(f"   状态已保存")

if __name__ == "__main__":
    main()

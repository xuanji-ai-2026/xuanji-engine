#!/usr/bin/env python3
"""
终极商用版任务分发启动系统
创建时间: 2026-03-22 18:48
功能: 将终极版任务队列注入自动化系统，启动AI员工
"""

import json
import os
import time
from datetime import datetime

def load_task_queue():
    """加载任务队列"""
    queue_path = "/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue.json"
    try:
        with open(queue_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 无法加载任务队列: {e}")
        return None

def update_automation_system(task_queue):
    """更新自动化系统配置"""
    print("=" * 80)
    print("🚀 启动终极商用版任务分发系统")
    print("=" * 80)
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 获取任务列表
    all_tasks = task_queue['all_tasks']
    assignments = task_queue.get('assignments', [])

    print(f"📋 任务队列信息:")
    print(f"   总任务数: {len(all_tasks)}")
    print(f"   P0任务: {task_queue['priority_summary']['P0']} 个")
    print(f"   P1任务: {task_queue['priority_summary']['P1']} 个")
    print(f"   P2任务: {task_queue['priority_summary']['P2']} 个")
    print(f"   P3任务: {task_queue['priority_summary']['P3']} 个")
    print(f"   P4任务: {task_queue['priority_summary']['P4']} 个")
    print(f"   P5任务: {task_queue['priority_summary']['P5']} 个")

    # 按优先级排序任务
    sorted_tasks = sorted(all_tasks, key=lambda x: {
        'P0': 0,
        'P1': 1,
        'P2': 2,
        'P3': 3,
        'P4': 4,
        'P5': 5
    }.get(x['priority'], 6))

    # 生成任务分发文件
    task_distribution = {
        "version": "v3.0 终极商用版",
        "created_at": datetime.now().isoformat(),
        "total_tasks": len(sorted_tasks),
        "tasks": sorted_tasks,
        "assignments": assignments,
        "distribution_strategy": "priority_first",
        "created_by": "李明远(001)",
        "status": "ready"
    }

    # 保存任务分发文件
    distribution_path = "/workspace/projects/workspace/xuanji-engine-v2/task_distribution_ultimate.json"
    with open(distribution_path, 'w', encoding='utf-8') as f:
        json.dump(task_distribution, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 任务分发文件已保存")
    print(f"   文件: {distribution_path}")

    # 生成P0任务列表（优先执行）
    p0_tasks = [t for t in sorted_tasks if t['priority'] == 'P0']
    p0_distribution_path = "/workspace/projects/workspace/xuanji-engine-v2/p0_tasks_only.json"
    with open(p0_distribution_path, 'w', encoding='utf-8') as f:
        json.dump(p0_tasks, f, ensure_ascii=False, indent=2)

    print(f"✅ P0任务列表已保存")
    print(f"   文件: {p0_distribution_path}")
    print(f"   P0任务数: {len(p0_tasks)}")

    return task_distribution

def restart_automation_system():
    """重启自动化系统"""
    print("\n" + "=" * 80)
    print("🔄 重启自动化系统")
    print("=" * 80)

    # 停止旧进程
    print("🛑 停止旧进程...")
    os.system("pkill -f 'ai_employee_full_automation_v3.py'")
    time.sleep(2)

    # 启动新进程
    print("🚀 启动新进程...")
    os.system("nohup python3 /workspace/projects/workspace/xuanji-engine-v2/ai_employee_full_automation_v3.py > /workspace/projects/workspace/xuanji-engine-v2/automation_ultimate.log 2>&1 &")

    time.sleep(3)

    # 检查进程状态
    result = os.popen("ps aux | grep 'ai_employee_full_automation_v3.py' | grep -v grep").read()
    if result:
        print("✅ 自动化系统启动成功")
        print(f"   进程信息:\n{result}")
    else:
        print("⚠️  自动化系统启动可能失败，请手动检查")

def monitor_ai_employees():
    """监控AI员工状态"""
    print("\n" + "=" * 80)
    print("👥 监控AI员工状态")
    print("=" * 80)

    time.sleep(5)  # 等待系统启动

    # 读取日志
    log_path = "/workspace/projects/workspace/xuanji-engine-v2/automation_ultimate.log"
    if os.path.exists(log_path):
        print("\n📋 最新日志（最后20行）:")
        result = os.popen(f"tail -20 {log_path}").read()
        print(result)

        # 统计活跃员工
        active_count = result.count("✅ 领取任务") + result.count("开始工作")
        print(f"\n📊 活跃员工统计:")
        print(f"   活跃员工: {active_count} 人")
    else:
        print(f"⚠️  日志文件不存在: {log_path}")

def main():
    """主函数"""
    # 1. 加载任务队列
    print("步骤1: 加载任务队列")
    task_queue = load_task_queue()
    if not task_queue:
        print("❌ 任务队列加载失败，退出")
        return

    # 2. 更新自动化系统
    print("\n步骤2: 更新自动化系统配置")
    task_distribution = update_automation_system(task_queue)

    # 3. 重启自动化系统
    print("\n步骤3: 重启自动化系统")
    restart_automation_system()

    # 4. 监控AI员工状态
    print("\n步骤4: 监控AI员工状态")
    monitor_ai_employees()

    # 5. 总结
    print("\n" + "=" * 80)
    print("🎯 任务分发启动完成")
    print("=" * 80)
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总任务数: {task_queue['total_tasks']}")
    print(f"P0任务: {task_queue['priority_summary']['P0']} 个")
    print(f"涉及员工: 30人")
    print(f"自动化系统: 已重启")
    print("\n✅ 终极商用版任务分发系统启动成功！")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
对比Git提交历史和任务列表
找出已完成和未完成的任务
"""

import json

# 读取已完成任务
with open('/workspace/projects/workspace/xuanji-engine-v2/completed_tasks.txt', 'r', encoding='utf-8') as f:
    completed = set(line.strip() for line in f if line.strip())

# 读取任务列表
with open('/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue_with_p5.json', 'r', encoding='utf-8') as f:
    task_queue = json.load(f)

# 分析任务完成情况
all_tasks = task_queue["all_tasks"]
total_tasks = len(all_tasks)

print("=" * 100)
print("📊 任务完成情况深度分析")
print("=" * 100)

print(f"\n总任务数: {total_tasks}个")
print(f"Git提交记录: {len(completed)}个")

# 按优先级分类
by_priority = {}
completed_by_priority = {}

for task in all_tasks:
    priority = task["priority"]
    task_name = task["name"]

    if priority not in by_priority:
        by_priority[priority] = []
    by_priority[priority].append(task_name)

    # 检查是否完成
    is_completed = False
    for completed_task in completed:
        if completed_task.lower() in task_name.lower() or task_name.lower() in completed_task.lower():
            is_completed = True
            break

    if priority not in completed_by_priority:
        completed_by_priority[priority] = {"total": 0, "completed": 0}

    completed_by_priority[priority]["total"] += 1
    if is_completed:
        completed_by_priority[priority]["completed"] += 1

# 按星组分类
by_star = {}
completed_by_star = {}

for task in all_tasks:
    star = task["star"]
    task_name = task["name"]

    if star not in by_star:
        by_star[star] = []
    by_star[star].append(task_name)

    # 检查是否完成
    is_completed = False
    for completed_task in completed:
        if completed_task.lower() in task_name.lower() or task_name.lower() in completed_task.lower():
            is_completed = True
            break

    if star not in completed_by_star:
        completed_by_star[star] = {"total": 0, "completed": 0}

    completed_by_star[star]["total"] += 1
    if is_completed:
        completed_by_star[star]["completed"] += 1

# 找出未完成的任务
uncompleted_tasks = []
for task in all_tasks:
    task_name = task["name"]
    is_completed = False

    for completed_task in completed:
        if completed_task.lower() in task_name.lower() or task_name.lower() in completed_task.lower():
            is_completed = True
            break

    if not is_completed:
        uncompleted_tasks.append(task)

# 输出按优先级统计
print("\n" + "=" * 100)
print("📋 按优先级统计")
print("=" * 100)

for priority in sorted(by_priority.keys()):
    total = completed_by_priority[priority]["total"]
    done = completed_by_priority[priority]["completed"]
    percentage = (done / total * 100) if total > 0 else 0
    status = "✅" if percentage >= 90 else "⚠️" if percentage >= 50 else "❌"
    print(f"{priority}: {done}/{total} ({percentage:.1f}%) {status}")

# 输出按星组统计
print("\n" + "=" * 100)
print("📋 按星组统计")
print("=" * 100)

for star in sorted(by_star.keys()):
    total = completed_by_star[star]["total"]
    done = completed_by_star[star]["completed"]
    percentage = (done / total * 100) if total > 0 else 0
    status = "✅" if percentage >= 90 else "⚠️" if percentage >= 50 else "❌"
    print(f"{star}: {done}/{total} ({percentage:.1f}%) {status}")

# 总体完成情况
total_completed = sum(v["completed"] for v in completed_by_priority.values())
overall_percentage = (total_completed / total_tasks * 100) if total_tasks > 0 else 0

print("\n" + "=" * 100)
print("📈 总体完成情况")
print("=" * 100)

print(f"\n总任务数: {total_tasks}个")
print(f"已完成: {total_completed}个")
print(f"未完成: {total_tasks - total_completed}个")
print(f"完成率: {overall_percentage:.1f}%")

if uncompleted_tasks:
    print(f"\n⚠️ 未完成任务清单 ({len(uncompleted_tasks)}个):")

    # 按星组分组
    uncompleted_by_star = {}
    for task in uncompleted_tasks:
        star = task["star"]
        if star not in uncompleted_by_star:
            uncompleted_by_star[star] = []
        uncompleted_by_star[star].append(task)

    for star in sorted(uncompleted_by_star.keys()):
        print(f"\n【{star}】- {len(uncompleted_by_star[star])}个:")
        for task in uncompleted_by_star[star]:
            print(f"  - {task['task_id']}: {task['name']} [{task['priority']}]")

    # 保存未完成任务列表
    output_file = "/workspace/projects/workspace/xuanji-engine-v2/uncompleted_tasks.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(uncompleted_tasks, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 未完成任务列表已保存到: {output_file}")
else:
    print("\n✅ 所有任务已完成！")

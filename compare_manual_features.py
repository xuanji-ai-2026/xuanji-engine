#!/usr/bin/env python3
"""
对比手动整理的60个核心功能与当前145个任务
找出缺失的任务
"""

import json

# 读取手动整理的功能
with open('/workspace/projects/workspace/xuanji-engine-v2/phase3_manual_features.json', 'r', encoding='utf-8') as f:
    manual_data = json.load(f)

# 读取当前任务队列
with open('/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue_with_p5.json', 'r', encoding='utf-8') as f:
    task_data = json.load(f)

# 提取所有功能需求
manual_features = {}
for star, features in manual_data["features_by_star"].items():
    manual_features[star] = set(features)

# 提取所有当前任务
current_tasks = {}
for task in task_data["all_tasks"]:
    star = task["star"]
    task_name = task["name"]
    if star not in current_tasks:
        current_tasks[star] = set()
    current_tasks[star].add(task_name)

# 对比分析
print("=" * 100)
print("📊 手动整理的60个核心功能与当前145个任务对比")
print("=" * 100)

print(f"\n功能需求总数: {manual_data['total_features']}个")
print(f"当前任务总数: {task_data['total_tasks']}个")

# 按星组对比
missing_tasks = []

for star in manual_features:
    features_count = len(manual_features[star])
    tasks_count = len(current_tasks.get(star, set()))

    print(f"\n【{star}】")
    print(f"  功能需求: {features_count}个")
    print(f"  当前任务: {tasks_count}个")

    # 检查缺失的功能
    missing_features = []
    for feature in manual_features[star]:
        found = False
        for task_name in current_tasks.get(star, set()):
            if feature.lower() in task_name.lower() or task_name.lower() in feature.lower():
                found = True
                break
        if not found:
            missing_features.append(feature)

    if missing_features:
        print(f"  缺失功能: {len(missing_features)}个 ⚠️")
        for feature in missing_features:
            print(f"    - {feature}")
            missing_tasks.append({
                "star": star,
                "feature": feature,
                "task_name": feature,
                "priority": "P0"  # 核心功能全部P0
            })
    else:
        print(f"  状态: ✅ 已全部覆盖")

# 输出汇总
print("\n" + "=" * 100)
print("🆕 需要添加的新任务汇总")
print("=" * 100)

if missing_tasks:
    print(f"\n总共需要添加 {len(missing_tasks)} 个新任务\n")

    # 按星组分组
    missing_by_star = {}
    for task in missing_tasks:
        star = task["star"]
        if star not in missing_by_star:
            missing_by_star[star] = []
        missing_by_star[star].append(task)

    for star in sorted(missing_by_star.keys()):
        print(f"\n【{star}】- {len(missing_by_star[star])}个新任务:")
        for task in missing_by_star[star]:
            print(f"  - {task['task_name']} [{task['priority']}]")

    # 保存新任务列表
    new_tasks_file = "/workspace/projects/workspace/xuanji-engine-v2/missing_core_tasks.json"
    with open(new_tasks_file, 'w', encoding='utf-8') as f:
        json.dump({
            "missing_count": len(missing_tasks),
            "tasks": missing_tasks
        }, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 新任务列表已保存到: {new_tasks_file}")
else:
    print("\n✅ 所有60个核心功能已覆盖，无需添加新任务")

# 输出统计
print("\n" + "=" * 100)
print("📈 完整统计")
print("=" * 100)

print(f"\n功能需求: {manual_data['total_features']}个")
print(f"当前任务: {task_data['total_tasks']}个")
print(f"缺失任务: {len(missing_tasks)}个")

if missing_tasks:
    print(f"\n任务补充后预计总数: {task_data['total_tasks'] + len(missing_tasks)}个")
else:
    print(f"\n✅ 任务覆盖完整，当前任务数: {task_data['total_tasks']}个")

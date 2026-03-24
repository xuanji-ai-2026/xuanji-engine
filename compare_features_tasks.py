#!/usr/bin/env python3
"""
对比29个文档的192个功能需求与当前145个任务
找出未实现的功能
"""

import json

# 读取功能需求
with open('/workspace/projects/workspace/xuanji-engine-v2/phase3_complete_features.json', 'r', encoding='utf-8') as f:
    feature_data = json.load(f)

# 读取当前任务队列
with open('/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue_with_p5.json', 'r', encoding='utf-8') as f:
    task_data = json.load(f)

# 统计功能需求
features_by_star = {}
for item in feature_data["complete_list"]:
    star = item["star"]
    feature = item["feature"]
    if star not in features_by_star:
        features_by_star[star] = set()
    features_by_star[star].add(feature)

# 统计当前任务
tasks_by_star = {}
for task in task_data["all_tasks"]:
    star = task["star"]
    task_name = task["name"]
    if star not in tasks_by_star:
        tasks_by_star[star] = set()
    tasks_by_star[star].add(task_name)

# 对比分析
print("=" * 100)
print("📊 功能需求与任务对比分析")
print("=" * 100)

print(f"\n功能需求总数: {feature_data['total_features']}个")
print(f"当前任务总数: {task_data['total_tasks']}个")
print(f"功能缺口: {feature_data['total_features'] - task_data['total_tasks']}个")

# 按星组对比
print("\n" + "=" * 100)
print("📋 按星组对比")
print("=" * 100)

all_missing_tasks = []

for star in features_by_star:
    features_count = len(features_by_star[star])
    tasks_count = len(tasks_by_star.get(star, set()))
    gap = features_count - tasks_count

    print(f"\n【{star}】")
    print(f"  功能需求: {features_count}个")
    print(f"  当前任务: {tasks_count}个")
    print(f"  功能缺口: {gap}个 {'✅' if gap == 0 else '⚠️'}")

    # 列出缺失的任务（功能需求转换为任务名称）
    if gap > 0:
        print(f"  缺失功能:")
        for feature in list(features_by_star[star])[:10]:  # 只显示前10个
            if feature not in tasks_by_star.get(star, set()):
                task_name = f"实现: {feature}"
                all_missing_tasks.append({
                    "star": star,
                    "task_name": task_name,
                    "feature": feature,
                    "priority": "P1" if gap <= 5 else "P2"
                })
                print(f"    - {task_name}")

# 生成新任务列表
print("\n" + "=" * 100)
print("🆕 需要添加的新任务")
print("=" * 100)

if all_missing_tasks:
    print(f"\n总共需要添加 {len(all_missing_tasks)} 个新任务\n")

    # 按星组分组
    missing_by_star = {}
    for task in all_missing_tasks:
        star = task["star"]
        if star not in missing_by_star:
            missing_by_star[star] = []
        missing_by_star[star].append(task)

    for star in sorted(missing_by_star.keys()):
        print(f"\n【{star}】- {len(missing_by_star[star])}个新任务")
        for task in missing_by_star[star]:
            print(f"  - {task['task_name']} [{task['priority']}]")

    # 保存新任务列表
    new_tasks_file = "/workspace/projects/workspace/xuanji-engine-v2/missing_tasks.json"
    with open(new_tasks_file, 'w', encoding='utf-8') as f:
        json.dump({
            "missing_count": len(all_missing_tasks),
            "tasks": all_missing_tasks
        }, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 新任务列表已保存到: {new_tasks_file}")
else:
    print("\n✅ 所有功能需求已覆盖，无需添加新任务")

# 输出统计
print("\n" + "=" * 100)
print("📈 完整统计")
print("=" * 100)

print(f"\n功能需求: {feature_data['total_features']}个")
print(f"当前任务: {task_data['total_tasks']}个")
print(f"缺失任务: {len(all_missing_tasks)}个")
print(f"需要补充: {len(all_missing_tasks)}个 ({len(all_missing_tasks)/task_data['total_tasks']*100:.1f}%)")

if all_missing_tasks:
    print(f"\n任务补充后预计总数: {task_data['total_tasks'] + len(all_missing_tasks)}个")

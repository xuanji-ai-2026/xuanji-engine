#!/usr/bin/env python3
"""
修复自动化系统任务加载问题
1. 添加P4和P5优先级
2. 修改queue_path指向完整任务文件
3. 确保P4和P5能正确执行
"""

# 第1步：修复multi_project_task_queue.py
original_path = "/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue.json"
new_path = "/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue_with_p5.json"

# 第2步：读取并修复multi_project_task_queue.py
with open("/workspace/projects/workspace/xuanji-engine-v2/multi_project_task_queue.py", 'r', encoding='utf-8') as f:
    content = f.read()

# 修复1: 添加P4和P5优先级
old_priority_class = """class TaskPriority:
    P0 = 0  # 紧急
    P1 = 1  # 高
    P2 = 2  # 普通
    P3 = 3  # 低"""

new_priority_class = """class TaskPriority:
    P0 = 0  # 紧急
    P1 = 1  # 高
    P2 = 2  # 普通
    P3 = 3  # 低
    P4 = 4  # 更低
    P5 = 5  # 最低"""

content = content.replace(old_priority_class, new_priority_class)

# 修复2: 修改priority_map
old_priority_map = """            priority_map = {
                'P0': TaskPriority.P0,
                'P1': TaskPriority.P1,
                'P2': TaskPriority.P2,
                'P3': TaskPriority.P3,
                'P4': TaskPriority.P3,  # 映射到P3
                'P5': TaskPriority.P3   # 映射到P3
            }"""

new_priority_map = """            priority_map = {
                'P0': TaskPriority.P0,
                'P1': TaskPriority.P1,
                'P2': TaskPriority.P2,
                'P3': TaskPriority.P3,
                'P4': TaskPriority.P4,  # 新增P4
                'P5': TaskPriority.P5    # 新增P5
            }"""

content = content.replace(old_priority_map, new_priority_map)

# 修复3: 修改queue_path
content = content.replace(original_path, new_path)

# 写回文件
with open("/workspace/projects/workspace/xuanji-engine-v2/multi_project_task_queue.py", 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ multi_project_task_queue.py 修复完成")
print(f"  - 添加P4和P5优先级")
print(f"  - 修改queue_path: {new_path}")
print(f"  - P4和P5现在有正确的优先级")

# 第3步：验证修复
from multi_project_task_queue import TaskPriority, load_ultimate_tasks

print("\n🔍 验证修复结果:")
print(f"  TaskPriority.P0 = {TaskPriority.P0}")
print(f"  TaskPriority.P1 = {TaskPriority.P1}")
print(f"  TaskPriority.P2 = {TaskPriority.P2}")
print(f"  TaskPriority.P3 = {TaskPriority.P3}")
print(f"  TaskPriority.P4 = {TaskPriority.P4}")
print(f"  TaskPriority.P5 = {TaskPriority.P5}")

# 加载任务并统计
queue = load_ultimate_tasks()
status = queue.get_status('xuanji_engine')
print(f"\n📊 任务加载结果:")
print(f"  待执行任务: {status['pending']}个")
print(f"  进行中: {status['in_progress']}个")
print(f"  已完成: {status['completed']}个")

print("\n🎉 自动化系统已修复，可以执行P0-P5全部任务！")

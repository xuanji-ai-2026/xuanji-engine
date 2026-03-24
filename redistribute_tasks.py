#!/usr/bin/env python3
"""
重新分配任务给所有50名员工
创建时间: 2026-03-22 19:02
功能: 将115个任务分配给所有50名AI员工
"""

import json
from datetime import datetime

def redistribute_tasks():
    """重新分配任务给所有员工"""

    print("=" * 80)
    print("🔄 任务重新分配系统")
    print("=" * 80)
    print(f"分配时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 加载任务队列
    with open('/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue.json', 'r', encoding='utf-8') as f:
        task_queue = json.load(f)

    all_tasks = task_queue['all_tasks']

    # 所有50名员工（按星层分组）
    star_employee_map = {
        "01_紫微帝星": [
            {"id": "102", "name": "陈元灵"},
            {"id": "106", "name": "张一凡"},
            {"id": "107", "name": "刘二明"},
            {"id": "108", "name": "王三思"},
            {"id": "109", "name": "赵四维"}
        ],
        "02_禄存星": [
            {"id": "111", "name": "周禄存"},
            {"id": "112", "name": "郑路由"},
            {"id": "113", "name": "王规划"},
            {"id": "114", "name": "冯优化"},
            {"id": "115", "name": "钱调度"}
        ],
        "03_巨门星": [
            {"id": "119", "name": "蒋巨门"},
            {"id": "120", "name": "沈记忆"},
            {"id": "121", "name": "韩向量"},
            {"id": "122", "name": "杨检索"},
            {"id": "123", "name": "朱图谱"}
        ],
        "04_廉贞星": [
            {"id": "163", "name": "伍廉贞"},
            {"id": "164", "name": "余情绪"},
            {"id": "165", "name": "元人格"},
            {"id": "166", "name": "孟一致"},
            {"id": "167", "name": "平心理"}
        ],
        "05_武曲星": [
            {"id": "127", "name": "谢武功"},
            {"id": "128", "name": "邹接口"},
            {"id": "129", "name": "喻发现"},
            {"id": "130", "name": "柏依赖"},
            {"id": "131", "name": "水版本"}
        ],
        "06_破军星": [
            {"id": "133", "name": "章破军"},
            {"id": "134", "name": "云沙箱"},
            {"id": "135", "name": "苏容器"},
            {"id": "136", "name": "潘外呼"},
            {"id": "137", "name": "葛消息"}
        ],
        "07_左辅星": [
            {"id": "146", "name": "倪左辅"},
            {"id": "147", "name": "汤K8s"},
            {"id": "148", "name": "殷用户"},
            {"id": "149", "name": "罗隔离"},
            {"id": "150", "name": "毕配置"}
        ],
        "08_右弼星": [
            {"id": "105", "name": "周右弼"},
            {"id": "156", "name": "乐法律"},
            {"id": "157", "name": "于道德"},
            {"id": "158", "name": "时权限"},
            {"id": "159", "name": "皮审计"}
        ],
        "09_贪狼星": [
            {"id": "143", "name": "薛贪狼"},
            {"id": "144", "name": "雷ASR"},
            {"id": "145", "name": "贺TTS"},
            {"id": "176", "name": "贡数字人"},
            {"id": "177", "name": "赏界面"}
        ],
        "10_辅弼星辰": [
            {"id": "161", "name": "齐辅弼"},
            {"id": "162", "name": "康网关"},
            {"id": "168", "name": "和产品"},
            {"id": "169", "name": "穆文档"},
            {"id": "183", "name": "财SDK"}
        ]
    }

    print(f"👥 员工统计:")
    total_employees = sum(len(emps) for emps in star_employee_map.values())
    print(f"   总员工数: {total_employees} 人")
    for star, emps in star_employee_map.items():
        print(f"   {star}: {len(emps)} 人")

    # 重新分配任务
    print(f"\n📋 任务重新分配:")

    assignments = []
    task_index = 0

    # 按星层分配任务
    for star, employees in star_employee_map.items():
        # 获取该星层的所有任务
        star_tasks = [t for t in all_tasks if t['star'] == star]

        if not star_tasks:
            print(f"   ⚠️  {star} 没有任务，跳过")
            continue

        # 按优先级排序
        star_tasks.sort(key=lambda t: {
            'P0': 0,
            'P1': 1,
            'P2': 2,
            'P3': 3,
            'P4': 4,
            'P5': 5
        }.get(t['priority'], 6))

        # 均匀分配给该星层的所有员工
        for i, task in enumerate(star_tasks):
            employee = employees[i % len(employees)]
            emp_str = f"{employee['name']}({employee['id']})"

            task['assigned_employee'] = emp_str
            task['assigned_employee_id'] = employee['id']

            assignments.append({
                "task_id": task['task_id'],
                "task_name": task['name'],
                "priority": task['priority'],
                "star": star,
                "employee": emp_str,
                "employee_id": employee['id']
            })

        print(f"   ✅ {star}: {len(star_tasks)} 任务 → {len(employees)} 员工")

    # 统计每个员工的任务数
    employee_task_count = {}
    for assignment in assignments:
        emp_id = assignment['employee_id']
        employee_task_count[emp_id] = employee_task_count.get(emp_id, 0) + 1

    print(f"\n📊 每位员工任务数:")
    for star, employees in star_employee_map.items():
        print(f"\n   {star}:")
        for emp in employees:
            count = employee_task_count.get(emp['id'], 0)
            status = "✅" if count > 0 else "⚠️"
            print(f"      {status} {emp['name']}({emp['id']}): {count} 个任务")

    # 保存重新分配的任务队列
    task_queue['assignments'] = assignments
    task_queue['assignments_count'] = len(assignments)
    task_queue['employee_task_count'] = employee_task_count
    task_queue['star_employee_map'] = star_employee_map
    task_queue['total_employees'] = total_employees
    task_queue['redistributed_at'] = datetime.now().isoformat()

    output_path = "/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(task_queue, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 任务重新分配完成")
    print(f"   文件: {output_path}")
    print(f"   总任务数: {len(all_tasks)}")
    print(f"   总员工数: {total_employees}")
    print(f"   有任务员工: {len(employee_task_count)} 人")

    # 检查是否有员工没有任务
    no_task_employees = [emp_id for emp_id, count in employee_task_count.items() if count == 0]
    if no_task_employees:
        print(f"\n⚠️  没有任务的员工: {no_task_employees}")
    else:
        print(f"\n✅ 所有员工都有任务")

    return task_queue

if __name__ == "__main__":
    task_queue = redistribute_tasks()

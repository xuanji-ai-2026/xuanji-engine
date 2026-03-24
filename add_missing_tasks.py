#!/usr/bin/env python3
"""
添加12个缺失的核心任务到任务队列
并分配给200名员工
"""

import json

# 读取缺失任务
with open('/workspace/projects/workspace/xuanji-engine-v2/missing_core_tasks.json', 'r', encoding='utf-8') as f:
    missing_data = json.load(f)

# 读取当前任务队列
with open('/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue_with_p5.json', 'r', encoding='utf-8') as f:
    task_queue = json.load(f)

# 读取员工名单
with open('/workspace/projects/workspace/memory/员工名单-融合版-v5.0.md', 'r', encoding='utf-8') as f:
    employee_data = f.read()

# 提取员工名单（简单解析）
employees_by_star = {
    "01_紫微帝星": ["陈元灵(102)", "张伟(011)", "刘斌(012)", "赵阳(013)"],
    "02_禄存星": ["周禄存(111)", "吴存真(112)", "郑存义(113)", "钱存信(114)", "冯存智(115)", "陈存理(116)", "褚存道(117)", "卫存德(118)"],
    "03_巨门星": ["蒋巨门(119)", "沈巨明(120)", "韩巨亮(121)", "杨巨知(122)", "朱巨信(123)", "秦巨诚(124)", "许巨真(125)", "戚巨实(126)"],
    "04_廉贞星": ["伍廉贞(163)", "余廉心(164)", "元廉情(165)", "孟廉意(166)", "李廉智(167)"],
    "05_武曲星": ["谢武功(127)", "邹武全(128)", "喻武能(129)", "柏武技(130)", "水武库(131)", "窦武备(132)", "章破军(133)", "云破敌(134)", "苏破阵(135)", "潘破晓(136)", "葛破浪(137)", "奚破浪(138)", "范破空(139)", "柯破云(140)", "厉破风(141)", "岑破雷(142)"],
    "06_破军星": ["薛贪狼(143)", "雷贪音(144)", "贺贪形(145)", "贡志强(176)", "赏志明(177)", "巴图(178)", "弓志明(179)", "母志明(180)"],
    "07_左辅星": ["倪左辅(146)", "汤左膀(147)", "殷左翼(148)", "殷左护(149)", "罗左卫(150)", "毕左护(151)", "郝左持(152)", "邬左扶(153)", "安左助(154)", "常左协(155)", "李星辰(101)", "周右弼(105)"],
    "08_右弼星": ["乐右弼(156)", "于右护(157)", "时右卫(158)", "皮右防(159)", "卞右盾(160)", "齐辅弼(161)", "康辅星(162)"],
    "09_贪狼星": ["和产品(168)", "穆产品(169)", "财市场(183)", "干市场(184)", "曲市场(185)", "桥客服(188)", "银客服(189)", "言客服(190)"],
    "10_辅弼星辰": ["产品经理1", "产品经理2", "产品经理3", "产品经理4", "产品经理5", "产品经理6"]
}

# 获取下一个任务ID
max_task_id = 0
for task in task_queue["all_tasks"]:
    if task["task_id"].startswith("Task-"):
        try:
            num = int(task["task_id"].replace("Task-", ""))
            if num > max_task_id:
                max_task_id = num
        except:
            pass

# 添加新任务
new_tasks = []
task_counter = max_task_id + 1

for missing in missing_data["tasks"]:
    star = missing["star"]
    feature = missing["feature"]
    priority = missing["priority"]

    # 获取该星组的员工
    employees = employees_by_star.get(star, ["未知"])

    # 选择第一个员工作为负责人
    assigned_employee = employees[0] if employees else "未知"

    # 提取工号
    import re
    match = re.search(r'\((\d+)\)', assigned_employee)
    employee_id = match.group(1) if match else "000"

    # 创建新任务
    new_task = {
        "task_id": f"Task-{task_counter}",
        "name": feature,
        "responsible": assigned_employee,
        "workload": "2周",
        "priority": priority,
        "star": star,
        "module": star.replace("_", "-"),
        "source": "第三期开发文档分析",
        "assigned_employees": employees,
        "assigned_employee": assigned_employee,
        "assigned_employee_id": employee_id
    }

    new_tasks.append(new_task)
    task_counter += 1

# 添加新任务到队列
task_queue["all_tasks"].extend(new_tasks)
task_queue["total_tasks"] = len(task_queue["all_tasks"])

# 保存更新后的任务队列
output_file = "/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue_v5.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(task_queue, f, ensure_ascii=False, indent=2)

print("=" * 100)
print("✅ 任务队列更新完成")
print("=" * 100)

print(f"\n原有任务数: {task_queue['total_tasks'] - len(new_tasks)}个")
print(f"新增任务数: {len(new_tasks)}个")
print(f"更新后任务数: {task_queue['total_tasks']}个")

print(f"\n📋 新增任务清单:")
for task in new_tasks:
    print(f"  [{task['task_id']}] {task['name']} - {task['assigned_employee']} [{task['priority']}]")

# 按星组统计
print(f"\n📊 按星组统计:")
by_star = {}
for task in task_queue["all_tasks"]:
    star = task["star"]
    if star not in by_star:
        by_star[star] = 0
    by_star[star] += 1

for star in sorted(by_star.keys()):
    print(f"  {star}: {by_star[star]}个任务")

print(f"\n✅ 更新后的任务队列已保存到: {output_file}")

#!/usr/bin/env3
"""
添加网站建设和文档编写任务到自动任务管理系统
"""

import json

# 读取现有任务
with open('/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue_with_p5.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 新增任务列表
new_tasks = [
    # ===== 网站建设任务 =====
    {
        "task_id": "WEB-001",
        "name": "官网首页设计开发",
        "category": "前端",
        "priority": "P0",
        "star": "09_贪狼星",
        "module": "tanlang_star",
        "source": "/workspace/projects/workspace/incoming/02_玄玑AI数字人引擎第三期开发计划.md",
        "assigned_employees": ["葛浩(014)", "昌艺(015)"],
        "assigned_employee": "葛浩(014)",
        "assigned_employee_id": "014",
        "workload": "2周",
        "description": "官网首页开发 - 产品介绍、核心功能展示、Hero section、特性卡片、CTA按钮"
    },
    {
        "task_id": "WEB-002",
        "name": "官网产品页面开发",
        "category": "前端",
        "priority": "P0",
        "star": "09_贪狼星",
        "module": "tanlang_star",
        "source": "/workspace/projects/workspace/incoming/02_玄玑AI数字人引擎第三期开发计划.md",
        "assigned_employees": ["葛浩(014)", "昌艺(015)"],
        "assigned_employee": "葛浩(014)",
        "assigned_employee_id": "014",
        "workload": "2周",
        "description": "官网产品页面开发 - 功能详情、技术架构、应用场景、成功案例"
    },
    {
        "task_id": "WEB-003",
        "name": "官网定价页面开发",
        "category": "前端",
        "priority": "P0",
        "star": "09_贪狼星",
        "module": "tanlang_star",
        "source": "/workspace/projects/workspace/incoming/02_玄玑AI数字人引擎第三期开发计划.md",
        "assigned_employees": ["葛浩(014)", "昌艺(015)"],
        "assigned_employee": "葛浩(014)",
        "assigned_employee_id": "014",
        "workload": "2周",
        "description": "官网定价页面开发 - 价格方案、套餐对比、付费流程、FAQ"
    },
    {
        "task_id": "WEB-004",
        "name": "用户社区功能开发",
        "category": "前端",
        "priority": "P0",
        "star": "09_贪狼星",
        "module": "tanlang_star",
        "source": "/workspace/projects/workspace/incoming/02_玄玑AI数字人引擎第三期开发计划.md",
        "assigned_employees": ["陈磊(016)", "周杰(017)"],
        "assigned_employee": "陈磊(016)",
        "assigned_employee_id": "016",
        "workload": "2周",
        "description": "用户社区功能 - 用户讨论区、案例分享、问答系统、点赞评论"
    },
    {
        "task_id": "WEB-005",
        "name": "用户社区社交功能",
        "category": "前端",
        "priority": "P0",
        "star": "09_贪狼星",
        "module": "tanlang_star",
        "source": "/workspace/projects/workspace/incoming/02_玄玑AI数字人引擎第三期开发计划.md",
        "assigned_employees": ["陈磊(016)", "周杰(017)"],
        "assigned_employee": "陈磊(016)",
        "assigned_employee_id": "016",
        "workload": "2周",
        "description": "用户社区社交功能 - 关注机制、私信系统、个人主页、动态发布"
    },
    # ===== 文档编写任务 =====
    {
        "task_id": "DOC-001",
        "name": "产品手册编写",
        "category": "文档",
        "priority": "P0",
        "star": "10_辅弼星辰",
        "module": "fubi_star",
        "source": "/workspace/projects/workspace/incoming/02_玄玑AI数字人引擎第三期开发计划.md",
        "assigned_employees": ["马丽(018)", "郑睿(008)"],
        "assigned_employee": "马丽(018)",
        "assigned_employee_id": "018",
        "workload": "3周",
        "description": "产品手册编写 - 产品介绍、功能特性、技术架构、应用场景、成功案例"
    },
    {
        "task_id": "DOC-002",
        "name": "用户手册编写",
        "category": "文档",
        "priority": "P0",
        "star": "10_辅弼星辰",
        "module": "fubi_star",
        "source": "/workspace/projects/workspace/incoming/02_玄玑AI数字人引擎第三期开发计划.md",
        "assigned_employees": ["马丽(018)", "郑睿(008)"],
        "assigned_employee": "马丽(018)",
        "assigned_employee_id": "018",
        "workload": "2周",
        "description": "用户手册编写 - 快速开始、使用指南、常见问题、故障排查、最佳实践"
    },
    {
        "task_id": "DOC-003",
        "name": "开发者手册编写",
        "category": "文档",
        "priority": "P0",
        "star": "10_辅弼星辰",
        "module": "fubi_star",
        "source": "/workspace/projects/workspace/incoming/02_玄玑AI数字人引擎第三期开发计划.md",
        "assigned_employees": ["马丽(018)", "郑睿(008)"],
        "assigned_employee": "马丽(018)",
        "assigned_employee_id": "018",
        "workload": "3周",
        "description": "开发者手册编写 - API参考、SDK使用、插件开发、集成指南、调试技巧"
    },
    {
        "task_id": "DOC-004",
        "name": "文档系统结构搭建",
        "category": "文档",
        "priority": "P0",
        "star": "10_辅弼星辰",
        "module": "fubi_star",
        "source": "/workspace/projects/workspace/incoming/02_玄玑AI数字人引擎第三期开发计划.md",
        "assigned_employees": ["马丽(018)", "郑睿(008)"],
        "assigned_employee": "马丽(018)",
        "assigned_employee_id": "018",
        "workload": "1周",
        "description": "文档系统结构搭建 - Docusaurus配置、侧边栏导航、版本控制、搜索功能"
    },
    {
        "task_id": "DOC-005",
        "name": "API参考文档编写",
        "category": "文档",
        "priority": "P0",
        "star": "10_辅弼星辰",
        "module": "fubi_star",
        "source": "/workspace/projects/workspace/incoming/02_玄玑AI数字人引擎第三期开发计划.md",
        "assigned_employees": ["马丽(018)", "郑睿(008)"],
        "assigned_employee": "马丽(018)",
        "assigned_employee_id": "018",
        "workload": "2周",
        "description": "API参考文档编写 - 接口定义、请求参数、响应格式、错误代码、示例代码"
    }
]

# 添加新任务到现有任务列表
data['all_tasks'].extend(new_tasks)
data['total_tasks'] = len(data['all_tasks'])

# 保存更新后的任务文件
with open('/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue_with_p5.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 新任务添加成功!")
print(f"  网站建设任务: 5个")
print(f"  文档编写任务: 5个")
print(f"  总任务数: {data['total_tasks']}个")

# 统计各优先级任务数
priority_count = {}
for task in data['all_tasks']:
    priority = task.get('priority', 'P2')
    priority_count[priority] = priority_count.get(priority, 0) + 1

print(f"\n📊 按优先级统计:")
for p in sorted(priority_count.keys()):
    print(f"  {p}: {priority_count[p]}个")

print(f"\n📋 新增任务列表:")
for task in new_tasks:
    print(f"  - {task['task_id']}: {task['name']} [{task['priority']}] - {task['assigned_employee']}")

print("\n🎉 自动化系统将自动开始执行这些任务!")

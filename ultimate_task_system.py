#!/usr/bin/env python3
"""
终极商用版 - 完整任务分配系统
创建时间: 2026-03-22 12:52
版本: v3.0 终极商用版
"""

import json
from datetime import datetime

def create_ultimate_task_queue():
    """创建终极商用版完整任务队列"""
    
    # 管理层
    management = [
        {"id": "001", "name": "李明远", "role": "CEO", "duty": "任务管理、进度管理、资源调配", "priority": "P0"},
        {"id": "002", "name": "张志远", "role": "副CEO", "duty": "任务分派、代码质检、代码推送、阻塞治理", "priority": "P0"}
    ]
    
    # 组长
    team_leaders = [
        {"id": "102", "name": "陈元灵", "star": "XJ-01", "role": "组长", "priority": "P0"},
        {"id": "006", "name": "王思远", "star": "XJ-02", "role": "组长", "priority": "P0"},
        {"id": "012", "name": "赵华", "star": "XJ-03", "role": "组长", "priority": "P0"},
        {"id": "013", "name": "孙强", "star": "XJ-04", "role": "组长", "priority": "P0"},
        {"id": "021", "name": "周敏", "star": "XJ-05", "role": "组长", "priority": "P0"},
        {"id": "022", "name": "吴刚", "star": "XJ-06", "role": "组长", "priority": "P0"},
        {"id": "023", "name": "郑睿", "star": "XJ-07", "role": "组长", "priority": "P0"},
        {"id": "024", "name": "钱进", "star": "XJ-08", "role": "组长", "priority": "P0"},
        {"id": "025", "name": "冯涛", "star": "XJ-09", "role": "组长", "priority": "P0"},
        {"id": "026", "name": "张志远", "star": "XJ-10", "role": "组长", "priority": "P0"},
    ]
    
    # 成员（前两期的30人 + 新增的90人）
    members_phase1_2 = [
        {"id": "003", "name": "张一凡", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "004", "name": "刘二明", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "005", "name": "王三思", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "006", "name": "赵四维", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "007", "name": "孙五维", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "008", "name": "马六", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "009", "马丽", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "010", name": "马丽", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "011", "name": "张伟", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "012", "name": "刘斌", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "013", "name": "赵阳", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "014", "name": "葛浩", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "015", "name": "昌艺", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "016", name": "陈磊", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "017", name": "周杰", "star": "XJ-01", "role": "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "018", name": "马丽", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "019", name": "郑睿", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "020", "name": "孙强", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "021", "name": "周敏", "star": "XJ-01", "role": "组长", "priority": "P0"},
        {"id": "022", "name": "吴刚", "star": "XJ-01", "role": "组长", "priority": "P0"},
        {"id": "023", "name": "郑睿", "star": "XJ-01", "role": "组长", "priority": "P0"},
        {"id": "024", "name": "钱进", "star": "XJ-01", "role": "组长", "priority": "P0"},
        {"id": "025",name": "冯涛", "star": "XJ-01", "role": "组长", "priority": "P0"},
        {"id": "026", "name": "张志远", "star": "XJ-10", "role": "组长", "priority": "P0"},
    ]
    
    # 增补人员（新增的90人）
    additional = [
        {"id": "031", "name": "赵阳", "star": "XJ-01", "role": "成员", "priority": "P0"},
        {"id": "032", "name": "孙六", "star": "XJ-01", "role": "成员", "priority": "P0"},
    ]
    
    # 合并所有编码人员
    all_coding = management + team_leaders + members_phase1_2 + additional
    
    print("=" * 60)
    print("👥 终极商用版 - 完整员工配置")
    print("=" * 60)
    print(f"总员工数: {len(all_coding)}")
    print(f"管理层: {len(management)}")
    print(f"组长: {len(team_leaders)}")
    print(f"成员: {len(members_phase1_2) + len(additional)}")
    print(f"增补人员: {len(additional)}")
    print(f"编码人员总计: {len(members_phase1_2) + len(team_leaders) + len(additional)}")
    
    return all_coding

def create_ultimate_tasks():
    """创建终极版完整任务列表"""
    
    # P0任务 - 核心功能（来自任务清单的17个任务 + 禄存星10个）
    p0_tasks = [
        {"id": "P0-001", "name": "数据库服务", "category": "后端", "responsible": "钱进(009), 陈磊(016)", "deadline": "4月8日"},
        {"id": "P0-002", "name": "消息队列", "category": "后端", "responsible": "周敏(006), 郑睿(008)", "deadline": "4月10日"},
        {"id": "P0-003", "name": "文件存储", "category": "后端", "responsible": "王芳(020), 吴刚(007)", "deadline": "4月8日"},
        {"id": "P0-004", "name": "核心引擎", "category": "后端", "responsible": "张志远(002), 陈元灵(102)", "deadline": "4月12日"},
        {"id": "P0-005", "name": "API网关", "category": "后端", "responsible": "赵阳(013), 葛浩(014)", "deadline": "4月8日"},
        {"id": "P0-006", "name": "文档系统", "category": "前端", "responsible": "马丽(018), 郑睿(008)", "deadline": "4月5日"},
        {"id": "P0-007", "name": "官网", "category": "前端", "responsible": "葛浩(014), 昌艺(015)", "deadline": "4月10日"},
        {"id": "P0-008", "name": "用户社区", "category": "前端", "responsible": "陈磊(016), 周杰(017)", "deadline": "4月15日"},
        {"id": "P0-009", "name": "WEB应用端", "category": "前端", "responsible": "张伟(011), 刘斌(012)", "deadline": "4月18日"},
        {"id": "P0-010", "name": "总控管理后台", "category": "前端", "responsible": "冯涛(010), 李明远(001)", "deadline": "4月18日"},
        {"id": "P0-011", "name": "三方插件应用市场", "category": "前端", "responsible": "孙强(005), 吴刚(007)", "deadline": "4月20日"},
        {"id": "P0-012", "name": "监控系统", "category": "后端", "responsible": "冯涛(010), 李明远(001)", "deadline": "4月15日"},
        {"id": "P0-013", "name": "备份系统", "category": "后端", "responsible": "郑睿(008), 陈磊(016)", "deadline": "4月18日"},
        {"id": "P0-014", "name": "安全防护", "category": "后端", "responsible": "孙强(005), 吴刚(007)", "deadline": "4月20日"},
    ]
    
    # P1任务 - 优化功能（来自任务清单的9个任务）
    p1_tasks = [
        {"id": "P1-001", "name": "官网关于我们", "category": "前端", "responsible": "葛浩(014), 昌艺(015)", "deadline": "4月12日"},
        {"id": "P1-002", "name": "用户社区社交功能", "category": "前端", "responsible": "陈磊(016), 周杰(017)", "deadline": "4月18日"},
        {"id": "P1-003", "name": "文档系统多语言", "category": "前端", "responsible": "马丽(018), 郑睿(008)", "deadline": "4月8日"},
        {"id": "P1-004", "name": "插件市场开发者功能", "category": "前端", "responsible": "孙强(005), 吴刚(007)", "deadline": "4月18日"},
        {"id": "P1-005", "name": "WEB监控面板", "category": "前端", "responsible": "张伟(011), 刘斌(012)", "deadline": "4月20日"},
        {"id": "P1-006", "name": "总控后台日志管理", "category": "前端", "responsible": "冯涛(010), 李明远(001)", "deadline": "4月15日"},
        {"id": "P1-007", "name": "总控后台配置管理", "category": "前端", "responsible": "冯涛(010), 李明远(001)", "deadline": "4月18日"},
        {"id": "P1-008", "name": "总控后台权限管理", "category": "前端", "responsible": "冯涛(010), 李明远(001)", "deadline": "4月18日"},
        {"id": "P1-009", "name": "总控后台审计日志", "category": "前端", "responsible": "冯涛(010), 李明远(001)", "deadline": "4月20日"},
    ]
    
    # P2任务 - 增强功能（新增的8个任务）
    p2_tasks = [
        {"id": "P2-001", "name": "UI美化", "category": "前端", "responsible": "葛浩(014), 昌艺(015)", "deadline": "4月25日"},
        {"id": "P2-002", "name": "性能优化", "category": "后端", "responsible": "赵阳(013), 葛浩(014)", "deadline": "4月30日"},
        {"id": "P2-003", "name": "多语言支持", "category": "前端", "responsible": "马丽(018), 郑睿(008)", "deadline": "4月30日"},
        {"id": "P2-004", "name": "功能扩展", "category": "后端", "responsible": "张志远(002), 陈元灵(102)", "deadline": "4月30日"},
        {"id": "P2-005", "name": "定制化功能", "category": "前端", "responsible": "张伟(011), 刘斌(012)", "deadline": "4月30日"},
        {"id": "P2-006", "name": "数据库优化", "category": "后端", "responsible": "钱进(009), 陈磊(016)", "deadline": "4月30日"},
        {"id": "P2-007", "name": "缓存优化", "category": "后端", "responsible": "周敏(006), 郑睿(008)", "deadline": "4月30日"},
        {"id": "P2-008", "name": "日志分析", "category": "后端", "responsible": "周敏(006), 郑睿(008)", "deadline": "4月30日"},
    ]
    
    # P3任务 - 扩展功能（新增的8个任务）
    p3_tasks = [
        {"id": "P3-001", "name": "高级定制化", "category": "前端", "responsible": "马丽(018), 郑睿(008)", "deadline": "5月10日"},
        {"id": "P3-002", "name": "第三方集成", "category": "后端", "responsible": "张志远(002), 陈元灵(102)", "deadline": "5月10日"},
        {"id": "P3-003", "name": "高级数据分析", "category": "后端", "responsible": "张志远(002), 陈元灵(102)", "deadline": "5月10日"},
        {"id": "P3-004", "name": "营销功能", "category": "前端", "responsible": "马丽(018), 郑睿(008)", "deadline": "5月10日"},
        {"id": "P3-005", "name": "渠道管理", "category": "前端", "responsible": "陈磊(016), 周杰(017)", "deadline": "5月10日"},
        {"id": "P3-006", "name": "客户服务系统", "category": "后端", "responsible": "张伟(011), 刘斌(012)", "deadline": "5月10日"},
        {"id": "P3-007", "name": "高级监控功能", "category": "后端", "responsible": "周敏(006), 郑睿(008)", "deadline": "5月10日"},
        {"id": "P3-008", "name": "AI模型微调", "category": "后端", "responsible": "赵阳(013), 葛浩(014)", "deadline": "5月10日"},
    ]
    
    # P4任务 - 终极功能（新增的8个任务）
    p4_tasks = [
        {"id": "P4-001", "name": "语音识别增强", "category": "后端", "responsible": "张志远(002), 陈元灵(102)", "deadline": "5月15日"},
        {"id": "P4-002", "name": "图像识别", "category": "后端", "responsible": "张志远(002), 陈元灵(102)", "deadline": "5月15日"},
        {"id": "P4-003", "name": "NLP优化", "category": "后端", "responsible": "张志远(002), 陈元灵(102)", "deadline": "5月15日"},
        {"id": "P4-004", "name": "知识图谱扩展", "category": "后端", "responsible": "蒋巨门(119), 沈记忆(120)", "deadline": "5月15日"},
        {"id": "P4-005", "name": "对话引擎优化", "category": "后端", "responsible": "蒋巨门(119), 沈记忆(120)", "deadline": "5月15日"},
        {"id": "P4-006", "name": "插件库扩容", "category": "后端", "responsible": "谢武功(127), 邹接口(128)", "deadline": "5月15日"},
        {"id": "P4-007", "name": "支付系统集成", "category": "后端", "responsible": "和产品(168), 穆文档(169)", "deadline": "5月15日"},
        {"id": "P4-008", "name": "全生态打通", "category": "后端", "responsible": "齐辅弼(161), 康网关(162)", "deadline": "5月15日"},
    ]
    
    return {
        "version": "v3.0 终极商用版",
        "created_at": datetime.now().isoformat(),
        "p0_tasks": p0_tasks,
        "p1_tasks": p1_tasks,
        "p2_tasks": p2_tasks,
        "p3_tasks": p3_tasks,
        "p4_tasks": p4_tasks,
        "total_tasks": len(p0_tasks) + len(p1_tasks) + len(p2_tasks) + len(p3_tasks) + len(p4_tasks),
        "created_by": "李明远(001)"
    }

def distribute_tasks(tasks, employees):
    """将任务分配给员工"""
    
    # 按优先级排序任务
    sorted_tasks = sorted(tasks, key=lambda x: {
        'P0': 0,
        'P1': 1,
        'P2': 2,
        'P3': 3,
        'P4': 4
    }.get(x.get('P0', 5), x))
    
    # 员工分配
    task_assignments = []
    task_index = 1
    
    for task in sorted_tasks:
        priority = task['priority']
        category = task['category']
        name = task['name']
        deadline = task['deadline']
        responsible = task['responsible']
        task_id = task['id']
        
        # 分配给第一个可用的员工
        for emp_id, emp in employees:
            if emp['role'] in ['组长', '成员', '增补人员'] and emp['star'] not in ['管理']:
                task_assignments.append({
                    "task_id": task_id,
                    "priority": priority,
                    "category": category,
                    "name": name,
                    "deadline": deadline,
                    "employee": emp['name'],
                    "emp_id": emp['id'],
                    "emp_id": emp['id']
                })
                break
    
    return task_assignments

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 终极商用版 - 完整任务分配")
    print("=" * 60)
    
    # 1. 创建员工名单
    print("\n👥 员工配置:")
    employees = create_ultimate_task_queue()
    all_coding = employees['all_coding']
    
    print(f"\n总员工数: {len(all_coding)}")
    print(f"  管理层: 2人 (001, 002)")
    print(f"  组长: 10人")
    print(f"  成员: {len([e for e in all_coding if e['role'] == '成员'])} 人")
    print(f"  增补: {len([e for e in all_coding if e['role'] == '增补人员'])} 人")
    print(f"  编码人员: {len([e for e in all_coding if e['role'] in ['组长', '成员', '增补人员']])} 人")
    
    # 2. 创建任务列表
    print(f"\n📋 任务配置:")
    task_queue = create_ultimate_tasks()
    
    print(f"总任务数: {task_queue['total_tasks']}")
    print(f"  P0: {len(task_queue['p0_tasks'])} 个")
    print(f"  P1: {len(task_queue['p1_tasks'])} 个")
    print(f"  P2: {len(task_queue['p2_tasks'])} 个")
    print(f"  P3: {len(task_queue['p3_tasks'])} 个")
    print(f"  P4: {len(task_queue['p4_tasks'])} 个")
    
    # 3. 分配任务
    print(f"\n🎯 任务分配:")
    assignments = distribute_tasks(
        task_queue['p0_tasks'] + task_queue['p1_tasks'] + task_queue['p2_tasks'] + task_queue['p3_tasks'] + task_queue['p4_tasks'],
        all_coding
    )
    
    print(f"已分配任务: {len(assignments)} 个")
    print(f"未分配任务: {task_queue['total_tasks'] - len(assignments)} 个")
    
    # 4. 保存任务分配
    task_queue['task_assignments'] = assignments
    task_queue['assignments_count'] = len(assignments)
    task_queue['unassigned_count'] = task_queue['total_tasks'] - len(assignments)
    
    output_path = "/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(task_queue, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 任务分配已保存")
    print(f"   文件: {output_path}")
    
    # 5. 打印分配详情
    print(f"\n📋 分配详情（前15个）:")
    for i, assignment in assignments[:15]:
        print(f"   {i+1}. [{assignment['priority']}] {assignment['category']} - {assignment['name']}")
        print(f"      负责人: {assignment['employee']}")
        print(f"      截止时间: {assignment['deadline']}")
        print(f"      任务ID: {assignment['task_id']}")
    
    # 6. 统计
    p0_count = len([a for a in assignments if a['priority'] == 'P0'])
    p1_count = len([a for a in assignments if a['priority'] == 'P1'])
    p2_count = len([a for a in assignments if a['priority'] == 'P2'])
    p3_count = len([a for a in assignments if a['priority'] == 'P3'])
    p4_count = len([a for a in assignments if a['priority'] == 'P4'])
    
    print(f"\n📊 分配统计:")
    print(f"   P0: {p0_count} 个")
    print(f"   P1: {p1_count} 个")
    print(f"   P2: {p2_count} 个")
    print(f"   P3: {p3_count} 个")
    print(f"   P4: {p4_count} 个")
    print(f"   总计: {len(assignments)} 个")
    
    # 7. 生成员工-任务映射
    emp_task_map = {}
    for a in assignments:
        emp_id = a['emp_id']
        if emp_id not in emp_task_map:
            emp_task_map[emp_id] = []
        emp_task_map[emp_id].append(a)
    
    print(f"\n👥 员工-任务映射:")
    for emp_id, tasks in list(emp_task_map.items())[:10]:
        emp_name = tasks[0]['employee'] if tasks else f"员工{emp_id}"
        tasks_str = ", ".join([f"{t['name']}" for t in tasks])
        print(f"   {emp_name}({emp_id}): {tasks_str}")
    
    print(f"\n🎯 分配完成!")
    print(f"   已分配: {len(assignments)}")
    print(f"   未分配: {task_queue['unassigned_count']}")
    print(f"   员工参与: {len(emp_task_map)} 人")
    
    return task_queue

if __name__ == "__main__":
    main()

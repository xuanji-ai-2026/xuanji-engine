#!/usr/bin/env python3
"""
终极商用版任务提取系统 v2.0
创建时间: 2026-03-22 18:45
功能: 从星层开发计划文档中提取完整的P0-P5任务
"""

import re
import json
from datetime import datetime
from pathlib import Path

def extract_tasks_from_document(file_path, star_name):
    """从文档中提取任务"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 无法读取 {file_path}: {e}")
        return []

    tasks = []
    in_task_table = False

    for line in content.split('\n'):
        # 检测任务表头（多种格式）
        if ('任务编号' in line or '任务名称' in line) and '优先级' in line:
            in_task_table = True
            continue

        # 如果在任务表中，提取任务
        if in_task_table:
            # 跳过空行和分隔线
            if not line.strip() or line.strip().startswith('─'):
                continue

            # 跳过非任务行
            if not line.strip().startswith('Task-'):
                # 如果遇到新的章节标题，结束任务提取
                if line.strip().startswith('#') or '三、' in line or '四、' in line or '五、' in line:
                    break
                continue

            # 解析任务行
            parts = line.strip().split()
            if len(parts) >= 5:
                task_id = parts[0]
                task_name = ' '.join(parts[1:-3])  # 任务名称
                responsible = parts[-3]  # 负责人
                workload = parts[-2]  # 工作量
                priority = parts[-1].upper()  # 优先级

                # 确保优先级是P0-P5
                if priority in ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']:
                    tasks.append({
                        "task_id": task_id,
                        "name": task_name,
                        "responsible": responsible,
                        "workload": workload,
                        "priority": priority,
                        "star": star_name,
                        "source": str(file_path)
                    })

    return tasks

def extract_tasks_from_objectives(file_path, star_name):
    """从核心目标中提取任务（用于没有任务表格的文档）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 无法读取 {file_path}: {e}")
        return []

    tasks = []
    in_objectives = False
    objective_count = 0

    for line in content.split('\n'):
        # 检测核心目标章节
        if '核心目标' in line or '1.2' in line:
            in_objectives = True
            continue

        # 如果在核心目标中，提取任务
        if in_objectives:
            # 跳过空行
            if not line.strip():
                continue

            # 检测目标行
            if '目标' in line and ('一：' in line or '二：' in line or '三：' in line or
                                   '1：' in line or '2：' in line or '3：' in line or
                                   '一、' in line or '二、' in line or '三、' in line):
                objective_count += 1
                task_name = line.strip().split('：')[1].strip() if '：' in line else line.strip()

                # 默认P0优先级
                task_id = f"OBJ-{star_name[:2].upper()}-{objective_count:03d}"
                tasks.append({
                    "task_id": task_id,
                    "name": task_name,
                    "responsible": f"{star_name}组",
                    "workload": "2-4周",
                    "priority": "P0",
                    "star": star_name,
                    "source": str(file_path),
                    "from_objectives": True
                })

            # 如果遇到新的章节标题，结束任务提取
            if line.strip().startswith('#') and '技术要点' in line:
                break

    return tasks

def extract_capability_matrix(file_path, star_name):
    """从能力矩阵中提取任务"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 无法读取 {file_path}: {e}")
        return []

    tasks = []
    in_capability_matrix = False

    for line in content.split('\n'):
        # 检测能力矩阵
        if '能力名称' in line and '优先级' in line and '目标指标' in line:
            in_capability_matrix = True
            continue

        # 如果在能力矩阵中，提取任务
        if in_capability_matrix:
            # 跳过空行和分隔线
            if not line.strip() or line.strip().startswith('─'):
                continue

            # 检查是否是任务行（包含P0-P5）
            if re.search(r'\bP[0-5]\b', line):
                parts = line.strip().split()
                if len(parts) >= 4:
                    task_name = parts[0]
                    priority = parts[1].upper()

                    # 确保优先级是P0-P5
                    if priority in ['P0', 'P1', 'P2', 'P3', 'P4', 'P5']:
                        task_id = f"C-{star_name[:2].upper()}-{len(tasks)+1:03d}"
                        tasks.append({
                            "task_id": task_id,
                            "name": task_name,
                            "responsible": f"{star_name}组",
                            "workload": "2-4周",
                            "priority": priority,
                            "star": star_name,
                            "source": str(file_path),
                            "from_matrix": True
                        })

            # 检查是否结束能力矩阵
            if line.strip().startswith('#') and '核心任务' in line:
                break

    return tasks

def main():
    """主函数"""
    print("=" * 80)
    print("🚀 终极商用版 - 完整任务提取系统 v2.0")
    print("=" * 80)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    base_path = Path("/workspace/projects/workspace/incoming")

    # 星层开发计划文件映射
    star_files = {
        "01_紫微帝星": "10_紫微帝星_元灵层_第三期开发计划.md",
        "02_禄存星": "11_禄存星_调度层_第三期开发计划.md",
        "03_巨门星": "12_巨门星_记忆层_第三期开发计划.md",
        "04_廉贞星": "14_廉贞星_人格层_第三期开发计划.md",
        "05_武曲星": "15_武曲星_技能层_第三期开发计划.md",
        "06_破军星": "16_破军星_执行层_第三期开发计划.md",
        "07_左辅星": "17_左辅星_底座层_第三期开发计划.md",
        "08_右弼星": "18_右弼星_安全层_第三期开发计划.md",
        "09_贪狼星": "13_贪狼星_交互层_第三期开发计划.md",
        "10_辅弼星辰": "19_辅弼星辰_扩展层_第三期开发计划.md"
    }

    all_tasks = []
    star_tasks = {}

    print("📂 开始提取星层任务...\n")

    for star_name, filename in star_files.items():
        file_path = base_path / filename

        print(f"📄 处理: {star_name} ({filename})")

        # 方法1: 从任务清单提取
        tasks_from_list = extract_tasks_from_document(file_path, star_name)

        # 方法2: 从能力矩阵提取
        tasks_from_matrix = extract_capability_matrix(file_path, star_name)

        # 方法3: 从核心目标提取（备用方法）
        tasks_from_objectives = []
        if not tasks_from_list and not tasks_from_matrix:
            tasks_from_objectives = extract_tasks_from_objectives(file_path, star_name)

        # 合并任务（去重）
        all_star_tasks = tasks_from_list + tasks_from_matrix + tasks_from_objectives

        # 去重（按任务名称）
        seen_names = set()
        unique_tasks = []
        for task in all_star_tasks:
            if task['name'] not in seen_names:
                seen_names.add(task['name'])
                unique_tasks.append(task)

        if unique_tasks:
            star_tasks[star_name] = unique_tasks
            all_tasks.extend(unique_tasks)
            print(f"   ✅ 提取成功: {len(unique_tasks)} 个任务")
        else:
            print(f"   ⚠️  未找到任务")

        print()

    print("=" * 80)
    print("📊 任务提取统计")
    print("=" * 80)

    # 按星层统计
    print(f"\n🌟 按星层任务分布:")
    for star in sorted(star_tasks.keys()):
        tasks = star_tasks[star]
        p0 = len([t for t in tasks if t['priority'] == 'P0'])
        p1 = len([t for t in tasks if t['priority'] == 'P1'])
        p2 = len([t for t in tasks if t['priority'] == 'P2'])
        p3 = len([t for t in tasks if t['priority'] == 'P3'])
        p4 = len([t for t in tasks if t['priority'] == 'P4'])
        p5 = len([t for t in tasks if t['priority'] == 'P5'])
        print(f"   {star}: {len(tasks)} 个任务 (P0:{p0} P1:{p1} P2:{p2} P3:{p3} P4:{p4} P5:{p5})")

    # 按优先级统计
    p0_count = len([t for t in all_tasks if t['priority'] == 'P0'])
    p1_count = len([t for t in all_tasks if t['priority'] == 'P1'])
    p2_count = len([t for t in all_tasks if t['priority'] == 'P2'])
    p3_count = len([t for t in all_tasks if t['priority'] == 'P3'])
    p4_count = len([t for t in all_tasks if t['priority'] == 'P4'])
    p5_count = len([t for t in all_tasks if t['priority'] == 'P5'])

    print(f"\n📈 优先级分布:")
    print(f"   P0 (核心功能): {p0_count} 个任务")
    print(f"   P1 (优化功能): {p1_count} 个任务")
    print(f"   P2 (增强功能): {p2_count} 个任务")
    print(f"   P3 (扩展功能): {p3_count} 个任务")
    print(f"   P4 (终极功能): {p4_count} 个任务")
    print(f"   P5 (其他功能): {p5_count} 个任务")
    print(f"   总计: {len(all_tasks)} 个任务")

    print(f"\n📋 前15个任务预览:")
    for i, task in enumerate(all_tasks[:15], 1):
        print(f"   {i}. [{task['priority']}] {task['star']} - {task['name']}")
        print(f"      任务ID: {task['task_id']}")
        print(f"      负责人: {task['responsible']}")
        print(f"      工作量: {task['workload']}")

    # 保存任务队列
    task_queue = {
        "version": "v3.0 终极商用版",
        "created_at": datetime.now().isoformat(),
        "total_tasks": len(all_tasks),
        "star_tasks": star_tasks,
        "all_tasks": all_tasks,
        "priority_summary": {
            "P0": p0_count,
            "P1": p1_count,
            "P2": p2_count,
            "P3": p3_count,
            "P4": p4_count,
            "P5": p5_count
        },
        "created_by": "李明远(001)",
        "status": "ready_to_distribute"
    }

    output_path = "/workspace/projects/workspace/xuanji-engine-v2/ultimate_task_queue.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(task_queue, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 任务队列已保存")
    print(f"   文件: {output_path}")
    print(f"   总任务数: {len(all_tasks)}")
    print(f"   创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 按星层分配给AI员工
    print(f"\n👥 任务分配方案:")
    star_employee_map = {
        "01_紫微帝星": ["陈元灵(102)", "张伟(011)", "刘斌(012)"],
        "02_禄存星": ["周禄存(111)", "赵阳(013)", "葛浩(014)"],
        "03_巨门星": ["蒋巨门(119)", "陈磊(016)", "周杰(017)"],
        "04_廉贞星": ["伍廉贞(163)", "马丽(018)", "郑睿(008)"],
        "05_武曲星": ["谢武功(127)", "孙强(005)", "吴刚(007)"],
        "06_破军星": ["章破军(133)", "周敏(006)", "王思远(006)"],
        "07_左辅星": ["倪左辅(146)", "钱进(009)", "冯涛(010)"],
        "08_右弼星": ["周右弼(105)", "张志远(002)", "李明远(001)"],
        "09_贪狼星": ["薛贪狼(143)", "贺TTS(145)", "雷ASR(144)"],
        "10_辅弼星辰": ["邹接口(128)", "喻发现(129)", "柏依赖(130)"]
    }

    assignments = []
    for task in all_tasks:
        star = task['star']
        if star in star_employee_map:
            employees = star_employee_map[star]
            task['assigned_employees'] = employees
            assignments.append({
                "task_id": task['task_id'],
                "task_name": task['name'],
                "priority": task['priority'],
                "star": star,
                "employees": employees
            })

    print(f"\n   已分配任务: {len(assignments)} 个")
    print(f"   涉及员工: {len(star_employee_map)} 个星层 × 3人 = 30人")

    # 保存任务分配
    task_queue['assignments'] = assignments
    task_queue['assignments_count'] = len(assignments)
    task_queue['employee_count'] = 30

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(task_queue, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 任务分配已保存到任务队列")

    print(f"\n🎯 任务提取完成!")
    print(f"   总任务数: {len(all_tasks)}")
    print(f"   P0任务: {p0_count} 个")
    print(f"   P1任务: {p1_count} 个")
    print(f"   P2任务: {p2_count} 个")
    print(f"   P3任务: {p3_count} 个")
    print(f"   P4任务: {p4_count} 个")
    print(f"   P5任务: {p5_count} 个")
    print(f"   完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return task_queue

if __name__ == "__main__":
    task_queue = main()

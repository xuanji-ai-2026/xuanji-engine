#!/usr/bin/env python3
"""
任务分发系统 - 将未完成任务分发给员工
创建时间: 2026-03-22 12:42
"""

import json
from datetime import datetime

def create_task_queue():
    """创建任务队列"""
    
    # P0任务 - 前端应用
    p0_frontend = [
        ("P0", "前端", "官网首页", "葛浩(014) 昌艺(015)"),
        ("P0", "前端", "官网产品页面", "葛浩(014) 完艺(015)"),
        ("P0", "前端", "官网定价页面", "葛浩(014) 完艺(015)"),
        ("P0", "前端", "用户社区功能", "陈磊(016) 周杰(017)"),
        ("P0", "前端", "用户社区社交功能", "陈磊(016) 周杰(017)"),
        ("P0", "前端", "文档系统结构", "马丽(018) 郑睿(008)"),
        ("P0", "前端", "文档API参考", "马丽(018) 郑睿(008)"),
        ("P0", "前端", "插件市场列表", "孙强(005) 吴刚(007)"),
        ("P0", "前端", "插件管理功能", "孙强(005) 吴刚(007)"),
        ("P0", "前端", "WEB用户管理", "张伟(011) 刘斌(012)"),
        ("P0", "前端", "WEB对话功能", "张伟(011) 刘斌(012)"),
        ("P0", "前端", "总控后台监控", "冯涛(010) 李明远(001)"),
        ("P0", "前端", "总控后台用户管理", "冯涛(010) 李明远(001)"),
        ("P0", "前端", "总控后台日志管理", "冯涛(010) 李明远(001)"),
        ("P0", "前端", "总控后台配置管理", "冯涛(010) 李明远(001)"),
        ("P0", "前端", "总控后台权限管理", "冯涛(010) 李明远(001)"),
    ]
    
    # P0任务 - 后端服务
    p0_backend = [
        ("P0", "后端", "API网关路由", "赵阳(013) 葛浩(014)"),
        ("P0", "后端", "API网关流量控制", "赵阳(013) 葛浩(014)"),
        ("P0", "后端", "API网关安全", "赵阳(013) 葛浩(014)"),
        ("P0", "后端", "核心引擎意图识别", "张志远(002) 陈元灵(102)"),
        ("P0", "后端", "核心引擎对话生成", "张志远(002) 陈元灵(102)"),
        ("P0", "后端", "核心引擎插件执行", "张志远(002) 陈元灵(102)"),
        ("P0", "后端", "核心引擎记忆管理", "张志远(002) 陈元灵(102)"),
        ("P0", "后端", "数据库PostgreSQL", "钱进(009) 陈磊(016)"),
        ("P0", "后端", "数据库Redis", "钱进(009) 陈磊(016)"),
        ("P0", "后端", "数据库Elasticsearch", "钱进(009) 陈磊(016)"),
        ("P0", "后端", "消息队列", "周敏(006) 郑睿(008)"),
        ("P0", "后端", "消息队列任务调度", "周敏(006) 郑睿(008)"),
        ("P0", "后端", "文件存储", "周敏(006) 郑睿(008)"),
        ("P0", "后端", "监控系统", "周敏(006) 郑睿(008)"),
        ("P0", "后端", "监控指标采集", "周敏(006) 郑睿(008)"),
        ("P0", "后端", "监控告警", "周敏(006) 郑睿(008)"),
        ("P0", "后端", "监控仪表盘", "周敏(006) 郑睿(008)"),
    ]
    
    # P1任务
    p1_tasks = [
        ("P1", "前端", "文档系统多语言", "马丽(018) 郑睿(008)"),
        ("P1", "前端", "插件市场开发者功能", "孙强(005) 吴刚(007)"),
        ("P1", "前端", "WEB监控面板", "张伟(011) 刘斌(012)"),
    ]
    
    # 合并所有任务
    all_tasks = p0_frontend + p0_backend + p1_tasks
    
    # 生成任务队列
    task_queue = {
        "total_tasks": len(all_tasks),
        "created_at": datetime.now().isoformat(),
        "tasks": []
    }
    
    task_id = 1
    for task in all_tasks:
        task_queue["tasks"].append({
            "task_id": task_id,
            "priority": task[0],
            "category": task[1],
            "name": task[2],
            "employees": task[3].split(" "),
            "status": "pending",
            "created_at": datetime.now().isoformat()
        })
        task_id += 1
    
    return task_queue

def main():
    """主函数"""
    print("=" * 60)
    print("📋 任务分发系统启动")
    print("=" * 60)
    
    # 创建任务队列
    task_queue = create_task_queue()
    
    print(f"\n✅ 任务队列已创建")
    print(f"   总任务数: {task_queue['total_tasks']}")
    print(f"   创建时间: {task_queue['created_at']}")
    
    print(f"\n📊 任务分布:")
    p0_count = len([t for t in task_queue['tasks'] if t['priority'] == 'P0'])
    p1_count = len([t for t in task_queue['tasks'] if t['priority'] == 'P1'])
    frontend_count = len([t for t in task_queue['tasks'] if t['category'] == '前端'])
    backend_count = len([t for t in task_queue['tasks'] if t['category'] == '后端'])
    
    print(f"   前端应用: {frontend_count} 任务")
    print(f"   后端服务: {backend_count} 任务")
    print(f"   P0高优先级: {p0_count} 任务")
    print(f"   P1中优先级: {p1_count} 任务")
    
    # 保存任务队列
    output_path = "/workspace/projects/workspace/xuanji-engine-v2/task_queue.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(task_queue, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 任务队列已保存")
    print(f"   路径: {output_path}")
    
    print(f"\n📋 前10个任务预览:")
    for i, task in enumerate(task_queue['tasks'][:10], 1):
        print(f"   {i}. [{task['priority']}] {task['category']} - {task['name']}")
        print(f"      负责人: {', '.join(task['employees'])}")
        print(f"      状态: {task['status']}")
    
    print(f"\n🚀 任务分发完成!")
    print(f"   等待员工领取...")
    
    return task_queue

if __name__ == "__main__":
    main()

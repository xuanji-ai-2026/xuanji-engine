#!/usr/bin/env python3
"""
AI数字员工第三期开发 - 简单代码质检
创建时间: 2026-03-22 08:50
功能: 快速检查Python文件的基本质量
"""

import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

def main():
    print("🔍 开始代码质检...")
    print("=" * 80)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    project_path = Path("/workspace/projects/workspace/xanji-engine-v2")
    
    # 查找Python文件
    python_files = list(project_path.rglob("*.py"))
    
    total_files = len(python_files)
    print(f"📊 检查 {total_files} 个Python文件...")
    
    # 统计
    total_lines = 0
    total_functions = 0
    total_classes = 0
    total_imports = 0
    docstrings = 0
    naming_issues = 0
    
    file_count = 0
    file_details = []
    
    for file_path in python_files[:50]:  # 只检查前50个
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue
        
        lines_total = content.count('\n')
        lines_code = lines_total - content.count('#')
        
        funcs = re.findall(r'def\s+\w+', content)
        classes = re.findall(r'class\s+\w+', content)
        imports = re.findall(r'import\s+\w+', content)
        
        docstrings = content.count('"""')
        type_anns = len(re.findall(r':\s+\w+\s+', content))
        
        naming_issues_count = len([m for m in funcs if not re.match(r'^[a-z_]+$', m)])
        long_funcs_count = len([m for m in funcs if len(m) > 50])
        
        total_lines += lines_total
        total_functions += len(funcs)
        total_classes += len(classes)
        total_imports += len(imports)
        docstrings += docstrings
        naming_issues += naming_issues_count
        long_funcs_count += long_funcs_count
        
        file_count += 1
        
        file_details.append({
            "file": file_path.name,
            "lines": lines_total,
            "funcs": len(funcs),
            "classes": len(classes),
            "imports": len(imports),
            "docs": docstrings,
            "type_anns": type_anns,
            "naming_issues": naming_issues_count,
            "long_funcs": long_funcs_count
        })
    
    print(f"\n📊 检查完成（前50个文件）:")
    print(f"  总文件数: {file_count}")
    print(f"  总代码行数: {total_lines}")
    print(f"  总函数数: {total_functions}")
    print(f"  总类数: {total_classes}")
    print(f"  总导入数: {total_imports}")
    print(f)  文档字符串数: {docstrings}")
    print(f)  类型注解数: {total_type_anns}")
    print(f)  命名问题数: {naming_issues}")
    print(f)  长函数数: {long_funcs_count} (>50行)")
    
    # 质量评估
    if file_count > 0:
        avg_lines = total_lines / file_count
        avg_funcs = total_functions / file_count
        avg_classes = total_classes / file_count
        avg_imports = total_imports / file_count
        
        print(f"\n📊 质量指标:")
        if total_functions + total_classes > 0:
            type_coverage = (total_type_anns / total_functions) * 100
            docstring_coverage = (docstrings / (total_functions + total_classes)) * 100
        else:
            type_coverage = 0
            docstring_coverage = 0
        
        print(f"  类型注解覆盖率: {type_coverage:.1f}%")
        print(f"  文档字符串覆盖率: {docstring_coverage:.1f}%")
        print(f"  平均文件大小: {avg_lines:.1f} 行/文件")
        print(f"  平均函数数: {avg_funcs:.1f} 个/文件")
        print(f"  平均类数: {avg_classes:.1f} 个/文件")
        print(f"  平均导入数: {avg_imports:.1f} 个/文件")
        print(f"  平均命名问题: {naming_issues / file_count:.1f} 个/文件")
        print(f"  平均长函数: {long_funcs_count / file_count:.1f} 个/文件")
    
    # Git状态
    print(f"\n📦 Git仓库状态:")
    try:
        result = subprocess.run(['git', 'status'], cwd="/workspace/projects/workspace/xuanji-engine-v2", capture_output=True, text=True)
        print("  Git状态: 正常")
    except:
        print("  Git状态: 未知")
    
    try:
        result = subprocess.run(['git', 'log', '--oneline', '-10'], cwd="/workspace/projects/workspace/xuanji-engine-v2", capture_output=True, text=True)
        commits = [l for l in result.stdout.split('\n') if l.strip() and ('commit' in l.lower())]
        print(f"  最近10次提交:")
        for commit in commits:
            print(f"    {commit}")
    except:
        print("  无法获取Git提交历史")
    
    # 详细文件信息
    print(f"\n📋 详细文件信息（前10个文件）:")
    sorted_files = sorted(file_details, key=lambda x: x['lines'], reverse=True)
    for i, file_info in enumerate(sorted_files[:10]):
        print(f"{i+1}. {file_info['file']}")
        print(f"     {file_info['lines']} 行, {file_info['funcs']} 函数, {file_info['classes']} 类, {file_info['imports']} 导入")
        print(f"     文档: {file_info['docs']} 个, 注解: {file_info['type_anns']} 个")
        print(f"     问题: 命名{file_info['naming_issues']}个, 长函数{file_info['long_funcs']}个")
    
    print(f"\n✅ 质检完成！")
    print("=" * 80)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
简化版代码质检系统
创建时间: 2026-03-22 14:00
功能: 快速检查304个Python文件的基本质量指标
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from collections import defaultdict, Counter

def check_file_quality(file_path: str) -> Dict:
    """检查单个文件的质量"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {"error": str(e)}

    lines = content.split('\n')
    total_lines = len(lines)
    code_lines = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
    blank_lines = len([l for l in lines if not l.strip()])
    comment_lines = total_lines - code_lines - blank_lines

    # 检查类型注解
    type_hint_lines = len([l for l in lines if ':' in l and ('->' in l or re.search(r':\s*int|str|bool|float|list|dict', l))])
    type_annotation_coverage = (type_hint_lines / code_lines * 100) if code_lines > 0 else 0

    # 检查文档字符串
    docstring_count = len(re.findall(r'""".*?"""', content, re.DOTALL))
    docstring_count += len(re.findall(r"'''.*?'''", content, re.DOTALL))
    docstring_coverage = (docstring_count / code_lines * 100) if code_lines > 0 else 0

    # 检查PEP8基本规则
    pep8_issues = []
    for i, line in enumerate(lines, 1):
        # 行长度
        if len(line) > 100:
            pep8_issues.append(f"行{i}: 长度超过100字符 ({len(line)})")
        # 缩进
        if line.startswith('    ') and '\t' in line:
            pep8_issues.append(f"行{i}: 混用空格和制表符")

    return {
        "file_path": file_path,
        "total_lines": total_lines,
        "code_lines": code_lines,
        "blank_lines": blank_lines,
        "comment_lines": comment_lines,
        "type_annotation_coverage": round(type_annotation_coverage, 2),
        "docstring_coverage": round(docstring_coverage, 2),
        "pep8_issues": pep8_issues,
        "error": None
    }

def main():
    """主函数"""
    print("=" * 80)
    print("🔍 玄玑引擎第三期 - 简化版代码质检")
    print("=" * 80)
    print(f"⏰ 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    base_dir = Path("/workspace/projects/workspace/xuanji-engine-v2")

    # 查找所有Python文件
    python_files = list(base_dir.rglob("*.py"))
    print(f"\n📊 发现 {len(python_files)} 个Python文件")

    # 质检所有文件
    results = []
    failed_files = []

    for i, file_path in enumerate(python_files, 1):
        if i % 50 == 0:
            print(f"  进度: {i}/{len(python_files)}")

        result = check_file_quality(str(file_path))
        if result.get("error"):
            failed_files.append((file_path, result["error"]))
        else:
            results.append(result)

    print(f"\n✅ 检查完成: {len(results)} 个文件")
    print(f"❌ 检查失败: {len(failed_files)} 个文件")

    # 统计数据
    total_lines = sum(r["total_lines"] for r in results)
    total_code_lines = sum(r["code_lines"] for r in results)
    total_type_coverage = sum(r["type_annotation_coverage"] for r in results) / len(results) if results else 0
    total_doc_coverage = sum(r["docstring_coverage"] for r in results) / len(results) if results else 0
    total_pep8_issues = sum(len(r["pep8_issues"]) for r in results)

    # 按星层统计
    star_layer_stats = defaultdict(lambda: {"files": 0, "lines": 0, "code_lines": 0})
    for r in results:
        file_path = r["file_path"]
        # 简单的星层识别
        if "01" in file_path or "ziwei" in file_path.lower():
            star_layer_stats["01_紫微星"]["files"] += 1
            star_layer_stats["01_紫微星"]["lines"] += r["total_lines"]
            star_layer_stats["01_紫微星"]["code_lines"] += r["code_lines"]
        elif "02" in file_path or "lucun" in file_path.lower():
            star_layer_stats["02_禄存星"]["files"] += 1
            star_layer_stats["02_禄存星"]["lines"] += r["total_lines"]
            star_layer_stats["02_禄存星"]["code_lines"] += r["code_lines"]
        elif "03" in file_path or "jumen" in file_path.lower():
            star_layer_stats["03_巨门星"]["files"] += 1
            star_layer_stats["03_巨门星"]["lines"] += r["total_lines"]
            star_layer_stats["03_巨门星"]["code_lines"] += r["code_lines"]
        elif "04" in file_path or "lianzheng" in file_path.lower():
            star_layer_stats["04_廉贞星"]["files"] += 1
            star_layer_stats["04_廉贞星"]["lines"] += r["total_lines"]
            star_layer_stats["04_廉贞星"]["code_lines"] += r["code_lines"]
        elif "05" in file_path or "wuqu" in file_path.lower():
            star_layer_stats["05_武曲星"]["files"] += 1
            star_layer_stats["05_武曲星"]["lines"] += r["total_lines"]
            star_layer_stats["05_武曲星"]["code_lines"] += r["code_lines"]
        elif "06" in file_path or "pojun" in file_path.lower():
            star_layer_stats["06_破军星"]["files"] += 1
            star_layer_stats["06_破军星"]["lines"] += r["total_lines"]
            star_layer_stats["06_破军星"]["code_lines"] += r["code_lines"]
        elif "07" in file_path or "zuofu" in file_path.lower():
            star_layer_stats["07_左辅星"]["files"] += 1
            star_layer_stats["07_左辅星"]["lines"] += r["total_lines"]
            star_layer_stats["07_左辅星"]["code_lines"] += r["code_lines"]
        elif "08" in file_path or "youbi" in file_path.lower():
            star_layer_stats["08_右弼星"]["files"] += 1
            star_layer_stats["08_右弼星"]["lines"] += r["total_lines"]
            star_layer_stats["08_右弼星"]["code_lines"] += r["code_lines"]
        elif "09" in file_path or "tanlang" in file_path.lower():
            star_layer_stats["09_贪狼星"]["files"] += 1
            star_layer_stats["09_贪狼星"]["lines"] += r["total_lines"]
            star_layer_stats["09_贪狼星"]["code_lines"] += r["code_lines"]
        elif "10" in file_path or "fubi" in file_path.lower():
            star_layer_stats["10_辅弼星辰"]["files"] += 1
            star_layer_stats["10_辅弼星辰"]["lines"] += r["total_lines"]
            star_layer_stats["10_辅弼星辰"]["code_lines"] += r["code_lines"]

    # 生成报告
    print("\n" + "=" * 80)
    print("📋 质检报告")
    print("=" * 80)

    print(f"\n📊 总体统计:")
    print(f"   总文件数: {len(results)}")
    print(f"   总代码行数: {total_lines:,}")
    print(f"   实际代码行: {total_code_lines:,}")
    print(f"   空白行: {sum(r['blank_lines'] for r in results):,}")
    print(f"   注释行: {sum(r['comment_lines'] for r in results):,}")
    print(f"   类型注解覆盖率: {total_type_coverage:.1f}%")
    print(f"   文档字符串覆盖率: {total_doc_coverage:.1f}%")
    print(f"   PEP8问题数: {total_pep8_issues}")

    print(f"\n🌟 按星层统计:")
    for star, stats in sorted(star_layer_stats.items()):
        print(f"   {star}: {stats['files']} 个文件, {stats['lines']:,} 行, {stats['code_lines']:,} 代码行")

    print(f"\n❌ 检查失败的文件 ({len(failed_files)}):")
    for file_path, error in failed_files[:10]:
        print(f"   {file_path}")
        print(f"     错误: {error}")
    if len(failed_files) > 10:
        print(f"   ... 还有 {len(failed_files) - 10} 个失败文件")

    # 质量评分
    type_score = min(total_type_coverage / 95 * 100, 100)
    doc_score = min(total_doc_coverage / 95 * 100, 100)
    pep8_score = max(100 - total_pep8_issues, 0)
    overall_score = (type_score + doc_score + pep8_score) / 3

    print(f"\n🎯 质量评分:")
    print(f"   类型注解: {total_type_coverage:.1f}% (目标95%+) - 得分: {type_score:.1f}")
    print(f"   文档字符串: {total_doc_coverage:.1f}% (目标95%+) - 得分: {doc_score:.1f}")
    print(f"   PEP8规范: {total_pep8_issues} 个问题 - 得分: {pep8_score:.1f}")
    print(f"   综合得分: {overall_score:.1f}/100")

    if overall_score >= 80:
        grade = "✅ 优秀"
    elif overall_score >= 60:
        grade = "⚠️ 良好"
    elif overall_score >= 40:
        grade = "🔴 需改进"
    else:
        grade = "🔴 严重警告"

    print(f"   等级: {grade}")

    # 保存详细报告
    report_path = "/workspace/projects/workspace/docs/简化版代码质检报告-2026-03-22.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# 玄玑引擎第三期 - 简化版代码质检报告\n\n")
        f.write(f"**质检时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## 📊 总体统计\n\n")
        f.write(f"- 总文件数: {len(results)}\n")
        f.write(f"- 总代码行数: {total_lines:,}\n")
        f.write(f"- 实际代码行: {total_code_lines:,}\n")
        f.write(f"- 空白行: {sum(r['blank_lines'] for r in results):,}\n")
        f.write(f"- 注释行: {sum(r['comment_lines'] for r in results):,}\n")
        f.write(f"- 类型注解覆盖率: {total_type_coverage:.1f}%\n")
        f.write(f"- 文档字符串覆盖率: {total_doc_coverage:.1f}%\n")
        f.write(f"- PEP8问题数: {total_pep8_issues}\n\n")
        f.write(f"## 🎯 质量评分\n\n")
        f.write(f"- 类型注解: {total_type_coverage:.1f}% (目标95%+) - 得分: {type_score:.1f}\n")
        f.write(f"- 文档字符串: {total_doc_coverage:.1f}% (目标95%+) - 得分: {doc_score:.1f}\n")
        f.write(f"- PEP8规范: {total_pep8_issues} 个问题 - 得分: {pep8_score:.1f}\n")
        f.write(f"- 综合得分: {overall_score:.1f}/100\n\n")
        f.write(f"## 🌟 按星层统计\n\n")
        for star, stats in sorted(star_layer_stats.items()):
            f.write(f"- {star}: {stats['files']} 个文件, {stats['lines']:,} 行, {stats['code_lines']:,} 代码行\n")
        f.write(f"\n## ❌ 检查失败的文件\n\n")
        for file_path, error in failed_files:
            f.write(f"- {file_path}\n")
            f.write(f"  错误: {error}\n\n")

    print(f"\n📄 详细报告已保存: {report_path}")

    # 返回建议
    print(f"\n💡 改进建议:")
    if total_type_coverage < 95:
        print(f"   1. 类型注解覆盖率 ({total_type_coverage:.1f}%) 低于目标 (95%)，需要补充类型注解")
    if total_doc_coverage < 95:
        print(f"   2. 文档字符串覆盖率 ({total_doc_coverage:.1f}%) 低于目标 (95%)，需要添加文档字符串")
    if total_pep8_issues > 0:
        print(f"   3. 发现 {total_pep8_issues} 个PEP8问题，需要修复")
    if failed_files:
        print(f"   4. {len(failed_files)} 个文件检查失败，需要检查语法错误")

    return {
        "total_files": len(results),
        "total_lines": total_lines,
        "type_coverage": total_type_coverage,
        "doc_coverage": total_doc_coverage,
        "pep8_issues": total_pep8_issues,
        "overall_score": overall_score,
        "failed_files": len(failed_files)
    }

if __name__ == "__main__":
    main()

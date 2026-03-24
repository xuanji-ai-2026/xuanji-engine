#!/usr/bin/env python3
"""
提取29个第三期开发文档的所有功能需求
"""

import os
import re
import json
from pathlib import Path

# 文档目录
doc_dir = "/workspace/projects/workspace/incoming"

# 29个文档文件
doc_files = sorted([
    "01_玄玑AI数字人引擎第三期开发总览.md",
    "02_玄玑AI数字人引擎第三期开发计划.md",
    "03_玄玑AI数字人引擎第三期开发计划完整索引.md",
    "04_紫微星元灵_自动化知识闭环系统v1.0.md",
    "05_实名认证与多租户管理系统v1.0.md",
    "06_总控管理后台_免费知识闭环集成方案v3.0.md",
    "07_武曲星插件库_学历学识类插件扩展方案.md",
    "08_武曲星插件库_第9大类_真实世界交互类插件.md",
    "09_生态社区插件市场融合方案.md",
    "10_紫微帝星_元灵层_第三期开发计划.md",
    "11_禄存星_调度层_第三期开发计划.md",
    "12_巨门星_记忆层_第三期开发计划.md",
    "13_贪狼星_交互层_第三期开发计划.md",
    "14_廉贞星_人格层_第三期开发计划.md",
    "15_武曲星_技能层_第三期开发计划.md",
    "16_破军星_执行层_第三期开发计划.md",
    "17_左辅星_底座层_第三期开发计划.md",
    "18_右弼星_安全层_第三期开发计划.md",
    "19_辅弼星辰_扩展层_第三期开发计划.md",
    "20_紫微帝星_元灵层_开发文档.md",
    "21_禄存星_调度层_开发文档.md",
    "22_巨门星_记忆层_开发文档.md",
    "23_贪狼星_交互层_开发文档.md",
    "24_廉贞星_人格层_开发文档.md",
    "25_武曲星_技能层_开发文档.md",
    "26_破军星_执行层_开发文档.md",
    "27_左辅星_底座层_开发文档.md",
    "28_右弼星_安全层_开发文档.md",
    "29_辅弼星辰_扩展层_开发文档.md",
])

# 功能需求提取
all_features = {
    "doc_index": [],
    "features_by_star": {}
}

print("📖 开始分析29个第三期开发文档...\n")

for idx, doc_file in enumerate(doc_files, 1):
    doc_path = os.path.join(doc_dir, doc_file)
    print(f"[{idx:02d}/{len(doc_files)}] 读取: {doc_file}")

    if not os.path.exists(doc_path):
        print(f"  ⚠️ 文件不存在")
        continue

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取星组信息
    star_match = re.search(r'(紫微帝星|禄存星|巨门星|廉贞星|武曲星|破军星|左辅星|右弼星|贪狼星|辅弼星辰)', doc_file)
    star_name = star_match.group(1) if star_match else "未知"

    # 提取核心功能
    features = []

    # 模式1: 功能标题（## 或 ###）
    feature_matches = re.findall(r'#+\s*(功能|模块|特性|系统)\s*[:：]?\s*(.+)', content, re.IGNORECASE)
    for match in feature_matches:
        features.append(f"{match[0]}: {match[1].strip()}")

    # 模式2: 列表项（- 或 * 开头）
    list_matches = re.findall(r'^[-*]\s*\[?([^\]]+)\]?\s+(.+)$', content, re.MULTILINE)
    for match in list_matches:
        if len(match[1]) > 5 and len(match[1]) < 100:
            features.append(match[1].strip())

    # 模式3: 任务标题（任务编号）
    task_matches = re.findall(r'(任务\d+|Task-\d+|OBJ-\d+-\d+|P[0-5]-\d+-\d+)', content)
    features.extend(task_matches)

    # 去重
    features = list(set(features))

    if star_name not in all_features["features_by_star"]:
        all_features["features_by_star"][star_name] = []

    all_features["features_by_star"][star_name].extend(features)
    all_features["doc_index"].append({
        "index": idx,
        "file": doc_file,
        "star": star_name,
        "feature_count": len(features)
    })

    print(f"  ✅ {star_name}: {len(features)}个功能\n")

# 统计汇总
print("=" * 80)
print("📊 功能需求统计汇总")
print("=" * 80)

for star_name, features in all_features["features_by_star"].items():
    unique_features = list(set(features))
    print(f"{star_name}: {len(unique_features)}个功能")

print("\n" + "=" * 80)
print("📋 各文档功能详细清单")
print("=" * 80)

for doc in all_features["doc_index"]:
    print(f"\n[{doc['index']:02d}] {doc['file']}")
    print(f"    星组: {doc['star']}")
    print(f"    功能数: {doc['feature_count']}个")

# 保存结果
output_file = "/workspace/projects/workspace/xuanji-engine-v2/phase3_features_analysis.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        "doc_count": len(doc_files),
        "total_features": sum(len(set(f)) for f in all_features["features_by_star"].values()),
        "features_by_star": {k: list(set(v)) for k, v in all_features["features_by_star"].items()},
        "doc_index": all_features["doc_index"]
    }, f, ensure_ascii=False, indent=2)

print(f"\n✅ 分析结果已保存到: {output_file}")

#!/usr/bin/env python3
"""
全面分析29个第三期开发文档，提取所有功能需求
对比当前任务队列，找出未实现的功能
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

print("📖 开始全面分析29个第三期开发文档...\n")

# 功能需求提取
all_features = {
    "by_star": {},
    "by_module": {},
    "by_priority": {},
    "complete_list": []
}

# 星组映射
star_mapping = {
    "紫微星": "01_紫微帝星",
    "紫微帝星": "01_紫微帝星",
    "禄存星": "02_禄存星",
    "巨门星": "03_巨门星",
    "廉贞星": "04_廉贞星",
    "武曲星": "05_武曲星",
    "破军星": "06_破军星",
    "左辅星": "07_左辅星",
    "右弼星": "08_右弼星",
    "贪狼星": "09_贪狼星",
    "辅弼星辰": "10_辅弼星辰",
}

# 提取所有文档的功能需求
for idx, doc_file in enumerate(doc_files, 1):
    doc_path = os.path.join(doc_dir, doc_file)
    print(f"[{idx:02d}/{len(doc_files)}] 分析: {doc_file}")

    if not os.path.exists(doc_path):
        print(f"  ⚠️ 文件不存在")
        continue

    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 确定星组
    star_name = "未知"
    for key, value in star_mapping.items():
        if key in doc_file:
            star_name = value
            break

    # 提取核心需求（多种模式）
    features = []

    # 模式1: 核心需求（核心能力、功能模块、主要特性）
    pattern1 = r'(?:核心能力|核心功能|主要特性|主要功能)\s*[:：]\s*([^\n]+)'
    matches = re.findall(pattern1, content)
    features.extend(matches)

    # 模式2: 功能列表（- 或 * 开头的功能）
    pattern2 = r'^[-*]\s*(?:\[(?:✅|❌|⏳)\])?\s*([^\n]{5,100})$'
    matches = re.findall(pattern2, content, re.MULTILINE)
    for m in matches:
        if not m.startswith("阶段") and not m.startswith("版本"):
            features.append(m)

    # 模式3: 技术实现（技术实现、技术方案）
    pattern3 = r'(?:技术实现|技术方案|交付物)\s*[:：]\s*([^\n]+)'
    matches = re.findall(pattern3, content)
    features.extend(matches)

    # 模式4: 任务编号（Task、OBJ、P任务）
    pattern4 = r'(Task-\d+|OBJ-\d+-\d+|P[0-5]-\d+-\d+|任务\d+)'
    matches = re.findall(pattern4, content)
    features.extend(matches)

    # 模式5: 标题（##或###开头的功能标题）
    pattern5 = r'#+\s*(?:功能|模块|特性|系统)\s*[：:]?\s*(.+)'
    matches = re.findall(pattern5, content)
    for m in matches:
        if len(m) < 100:
            features.append(m.strip())

    # 清理和去重
    clean_features = []
    for f in features:
        f = f.strip()
        if len(f) > 5 and len(f) < 150 and "完成" not in f and "实现" not in f:
            # 移除特殊符号
            f = re.sub(r'^[\s\*\-\•]+', '', f)
            if f not in clean_features:
                clean_features.append(f)

    # 存储功能
    if star_name not in all_features["by_star"]:
        all_features["by_star"][star_name] = []

    all_features["by_star"][star_name].extend(clean_features)
    all_features["complete_list"].extend([
        {
            "star": star_name,
            "feature": f,
            "source": doc_file
        }
        for f in clean_features
    ])

    print(f"  ✅ {star_name}: {len(clean_features)}个功能\n")

# 统计汇总
print("=" * 80)
print("📊 功能需求统计汇总")
print("=" * 80)

total_features = 0
for star_name, features in all_features["by_star"].items():
    unique_features = list(set(features))
    print(f"{star_name}: {len(unique_features)}个功能")
    total_features += len(unique_features)

print(f"\n总功能数: {total_features}个")

# 保存结果
output_file = "/workspace/projects/workspace/xuanji-engine-v2/phase3_complete_features.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        "doc_count": len(doc_files),
        "total_features": total_features,
        "features_by_star": {k: list(set(v)) for k, v in all_features["by_star"].items()},
        "complete_list": all_features["complete_list"]
    }, f, ensure_ascii=False, indent=2)

print(f"\n✅ 完整分析结果已保存到: {output_file}")

#!/usr/bin/env python3
"""
AI数字员工第三期开发 - 简化代码质检系统
创建时间: 2026-03-22 08:42
功能: 快速检查Python文件的代码质量
"""

import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

def check_code_quality(file_path):
    """检查单个文件的代码质量"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return None
    
    if not content:
        return None
    
    # 基本信息
    lines_total = content.count('\n')
    lines_blank = sum(1 for line in content.split('\n') if not line.strip())
    lines_code = lines_total - lines_blank
    lines_comment = content.count('#')
    file_size = len(content)
    
    # 统计函数定义
    functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*\s*\(', content)
    classes = re.findall(r'class\s+([A-Z][a-zA-Z0-9]*)\s*\(', content)
    imports = re.findall(r'import\s+([a-zA-Z][a-zA-Z0-9._]+)', content)
    
    # 类型注解
    type_annotations = len(re.findall(r':\s*[A-Za-z]+\s+', content))
    # 文档字符串
    docstrings = len(re.findall(r'""".*?""|\'\'\'\)?""\'\'|"""', content))
    
    # 命名问题
    naming_issues = []
    
    # 函数命名
    func_names = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*\s*\(', content)
    for name in func_names:
        if not re.match(r'^[a-z_][a-zA-Z0-9_]*$', name):
            naming_issues.append(f"函数名不符合PEP8: {name}")
        elif name.isupper():
            naming_issues.append(f"函数名不应全大写: {name}")
    
    # 类命名
    class_names = re.findall(r'class\s+([A-Z][a-zA-Z0-9]*)\s*\(', content)
    for name in class_names:
        if not re.match(r'^[A-Z][a-zA-Z0-9]+$', name):
            naming_issues.append(f"类名不符合PascalCase: {name}")
    
    # 复杂度检查（简化版）
    complexity_score = len(re.findall(r'\b\s+(if|elif|for|while|with|try|except)', content))
    
    # 长函数检查
    long_functions = re.findall(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*:\s*\)', content)
    long_function_lines = [len(m.group(1)) for m in long_functions if len(m.group(1)) > 50]
    very_long_function_lines = [len(m.group(1)) for m in long_function_lines if len(m.group(1)) > 100]
    
    # 导入检查
    imports_list = re.findall(r'import\s+([a-zA-Z][a-zA-Z0-9._]+)', content)
    duplicate_imports = [imp for imp, count in Counter(imports_list).items() if count > 1]
    
    return {
        "file_path": str(file_path),
        "file_name": file_path.name,
        "file_size": file_size,
        "lines_total": lines_total,
        "lines_code": lines_code,
        "lines_blank": lines_blank,
        "lines_comment": lines_comment,
        "functions": len(functions),
        "classes": len(classes),
        "imports": len(imports),
        "type_annotations": len(type_annotations),
        "docstrings": len(docstrings),
        "naming_issues": len(naming_issues),
        "complexity_score": complexity_score,
        "long_functions": len(long_function_lines),
        "very_long_functions": len(very_long_function_lines),
        "duplicate_imports": len(duplicate_imports)
    }

def analyze_by_starlayer(project_path):
    """按星层分析代码质量"""
    star_layers = {
        "XJ01": "紫微元灵",
        "XJ02": "禄存星",
        "XJ03": "star"
    }
    
    for key, star_layer in star_layers.items():
        layer_dir = None
        
        # 尝试不同的路径模式
        possible_dirs = [
            Path(project_path) / key.lower().replace(' ', '_'),
            Path(project_path) / key[:2],
            Path(project_path) / key.lower().replace('-', '_'),
            Path(project_path) / key.replace(' ', '_'),
        ]
        
        for test_dir in possible_dirs:
            if test_dir.exists() and test_dir.is_dir():
                layer_dir = test_dir
                break
        
        if layer_dir:
            files = list(layer_dir.glob("**/*.py"))
            print(f"\n{star_layer} ({len(files)} 个文件):")
            print(f"目录: {layer_dir}")
            print(f"文件列表:")
            
            for file in files[:20]:  # 只显示前20个
                result = check_code_quality(file)
                if result:
                    print(f"  {file.name}: {result['lines_total']}行, {result['functions']} 函数, {result['classes']} 类")
                    
                    # 质量评分
                    score = 0
                    score += 10 if result['type_annotations'] >= 3 else 0
                    score += 10 if result['docstrings'] >= 2 else 0
                    score += 10 if result['complexity_score'] <= 10 else 0
                    score += 10 if result['naming_issues'] == 0 else 0
                    score += 10 if result['duplicate_imports'] == 0 else 0
                    score += 10 if result['long_functions'] == 0 else 0
                    score += 10 if result['very_long_functions'] == 0 else 0
                    
                    quality = "优秀" if score >= 50 else "需优化" if score >= 40 else "需重构"
                    print(f"      质量评分: {score}/70 - {quality}")
                    
                    if result['naming_issues'] > 0:
                        print(f"      ⚠️ 命名问题: {result['naming_issues']}个")
                        if result['naming_issues'] <= 3:
                            for issue in result['naming_issues'][:3]:
                                print(f"        • {issue}")
                    if result['duplicate_imports'] > 0:
                        print(f"      ⚠️ 重复导入: {result['duplicate_imports']}个")
                    if result['long_functions'] > 0:
                        print(f"      ⚠️  长函数: {result['long_functions']}个 (>50行)")
                    if result['very_long_functions'] > 0:
                        print(f"      ⚠️  超长函数: {result['very_long_functions']}个 (>100行)")
            else:
                print(f"  未找到{star_layer}目录")
        else:
            print(f"  ⚠️  未找到{star_layer}目录")
    
    print(f"\n总计检查完成")

def main():
    """主函数"""
    project_path = "/workspace/projects/workspace/xuanji-engine-v2"
    print("=" * 80)
    print("📋 AI数字员工第三期开发 - 快速代码质检")
    print("=" * 80)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    try:
        # 检查主要目录
        dirs_to_check = [
            ("XJ01", "01_ziwei_star"),
            ("XJ02", "02_lucun_star"),
            ("XJ03", "03_jumen_star"),
            ("XJ04", "04_lianzheng_star"),
            ("XJ05", "05_wuqu_star"),
            ("XJ06", "06_pojun_star"),
            ("XJ07", "07_zuofu_star"),
            ("XJ08", "08_youbi_star"),
            ("XJ09", "09_tanlang_star"),
            ("XJ10", "10_fubi_star")
        ]
        
        total_files = 0
        total_lines = 0
        total_functions = 0
        total_classes = 0
        total_imports = 0
        type_annotations = 0
        docstrings = 0
        naming_issues = 0
        long_functions = 0
        duplicate_imports = 0
        duplicate_imports_details = []
        
        for layer_name, dir_name in dirs_to_check:
            dir_path = Path(project_path) / dir_name
            if dir_path.exists() and dir_path.is_dir():
                files = list(dir_path.glob("**/*.py"))
                print(f"\n{layer_name} ({len(files)} 个文件):")
                for file in files[:30]:  # 只显示前30个
                    result = check_code_quality(file)
                    if result:
                        total_files += 1
                        total_lines += result['lines_total']
                        total_functions += result['functions']
                        total_classes += result['classes']
                        total_imports += result['imports']
                        type_annotations += result['type_annotations']
                        docstrings += result['docstrings']
                        naming_issues += result['naming_issues']
                        long_functions += result['long_functions']
                        duplicate_imports += result['duplicate_imports']
                        
                        duplicate_imports_details.extend([imp for imp, count in Counter(imports_list).items() if count > 1 for imports_list in [result['imports']]])
                        
                        # 显示质量评分
                        score = 0
                        score += 10 if result['type_annotations'] >= 3 else 0
                        score += 10 if result['docstrings'] >= 2 else 0
                        score += 10 if result['complexity_score'] <= 10 else 0
                        score += 10 if result['naming_issues'] == 0 else 0
                        score += 10 if result['duplicate_imports'] == 0 else 0
                        score += 10 if result['long_functions'] == 0 else 0
                        score += 10 if result['very_long_functions'] == 0 else 0
                        
                        quality = "优秀" if score >= 50 else "需优化" if score >= 40 else "需重构"
                        print(f"  ✅ {file.name}: {result['lines_total']}行, {result['functions']} 函数, {result['classes']} 类")
                        print(f"      质量评分: {score}/70 - {quality}")
                        
                        if result['naming_issues'] > 0:
                            print(f"      ⚠️  命名问题: {result['naming_issues']}个")
                        if result['duplicate_imports'] > 0:
                            print(f"      ⚠️ 重复导入: {result['duplicate_imports']}个")
                            if result['duplicate_imports'] <= 5:
                                for imp in result['imports']:
                                    count = [imp for imp, c in result['imports']].count(imp)
                                    if count > 1:
                                        dup_list = [imp for imp in result['imports'] if result['imports'].count(imp) > 1]
                                        print(f"        • {dup_list[0]} ({count}次)")
                        if result['long_functions'] > 0:
                            print(f"      ⚠️  长函数: {result['long_functions']}个 (>50行)")
                        if result['very_long_functions'] > 0:
                            print(f"      ⚠️  超长函数: {result['very_long_functions']}个 (>100行)")
                        if result['complexity_score'] > 20:
                            print(f"      ⚠️  复杂度: {result['complexity_score']}/30")
                else:
                    print(f"  ⚠️  未找到{layer_name}目录")
        
        print(f"\n📊 整体统计:")
        print(f"  总文件数: {total_files}")
        print(f"  总代码行数: {total_lines}")
        print(f"  总函数数: {total_functions}")
        print(f"  总类数: {total_classes}")
        print(f"  总导入数: {total_imports}")
        print(f"  类型注解数: {type_annotations}")
        print(f"  文档字符串数: {total_docstrings}")
        print(f"  命名问题: {naming_issues}")
        print(f"  长函数数: {long_functions} (>50行)")
        print(f")
        
        if total_functions > 0:
            print(f"📊 质量指标:")
            print(f"  类型注解覆盖率: {(type_annotations / (total_functions + total_classes)) * 100:.1f}%")
            print(f"  文档字符串覆盖率: {(total_docstrings / (total_functions + total_classes)) * 100:.1f}%")
            
            avg_complexity = sum([self._calculate_complexity(file) for file in Path(project_path).rglob("*.py")]) / len([f for f in Path(project_path).rglob("*.py")])
            print(f"  平均复杂度: {avg_complexity:.1f}")
            
            avg_maintainability = sum([100 - self._calculate_maintainability(file) for file in Path(project_path).rglob("*.py")]) / len([f for f in Path(project_path).rglob("*.py")])
            print(f"  平均可维护性: {avg_maintainability:.1f}%")
            
            duplicate_imp_count = len([item for item in duplicate_imports_details for item in duplicate_imports_details])
            print(f"  重复导入问题: {duplicate_imp_count} 个")
            if duplicate_imp_count > 0:
                print(f"    常见重复导入: {Counter([imp for imp in duplicate_imports_details]).most_common(1)}")
        
        else:
            print("⚠️  无法计算质量指标（无法解析函数和类）")
    
    except Exception as e:
        print(f"❌ 检查失败: {e}")

def _calculate_complexity(file_path):
    """计算文件复杂度"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return 0
    
    complexity = len(re.findall(r'\b(?:if|elif|for|while|with|try|except|async\s+with)\b+', content))
    return complexity

def _calculate_maintainability(file_path):
    """计算可维护性指数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return 0
    
    lines_of_code = content.count('\n') - content.count('\n#') - content.count('"""') * 3
    functions = len(re.findall(r'def\s+', content))
    avg_func_length = lines_of_code / functions if functions > 0 else 0
    
    if avg_func_length > 0:
        maintainability = max(0, 100 - avg_func_length)
    else:
        maintainability = 0
    
    return maintainability

if __name__ == "__main__":
    main()

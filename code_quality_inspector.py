#!/usr/bin/env python3
"""
AI数字员工第三期开发 - 代码质检系统
创建时间: 2026-03-22 08:42
功能: 全面检查93个Python文件的代码质量
"""

import os
import re
import ast
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass
from collections import defaultdict, Counter

@dataclass
class CodeQualityMetrics:
    """代码质量指标"""
    file_name: str
    file_path: str
    employee_id: str
    employee_name: str
    star_layer: str
    task_id: str
    lines_total: int
    lines_code: int
    lines_blank: int
    lines_comment: int
    lines_docstring: int
    type_annotation_coverage: float  # 类型注解覆盖率
    docstring_coverage: float       # 文档字符串覆盖率
    pep8_compliance: float      # PEP8规范符合度
    cyclomatic_complexity: float   # 圈复杂度
    maintainability_index: float # 可维护性指数
    num_functions: int
    num_classes: int
    num_imports: int
    unused_imports: List[str]
    function_lengths: List[int]
    class_lengths: List[int]
    naming_issues: List[str]    # 命名规范问题
    quality_issues: List[str]   # 质量问题
    security_issues: List[str] # 安全问题
    files: int                # 引用的其他文件数
    complexity_high: bool         # 复杂度过高
    maintainability_low: bool       # 可维护性低
    pep8_compliant: bool        # PEP8符合

class CodeQualityInspector:
    """代码质检器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.metrics = []
        
    def inspect_all_files(self) -> List[CodeQualityMetrics]:
        """检查所有Python文件"""
        python_files = list(self.project_path.rglob("*.py"))
        
        print(f"🔍 开始质检 {len(python_files)} 个Python文件...")
        
        for file in python_files:
            metrics = self._inspect_file(file)
            if metrics:
                self.metrics.append(metrics)
        
        print(f"✅ 质检完成！")
        return self.metrics
    
    def _inspect_file(self, file_path: Path) -> CodeQualityMetrics:
        """检查单个Python文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析AST
            try:
                tree = ast.parse(content)
            except SyntaxError as e:
                return None
            
            # 基本信息
            lines_total = content.count('\n')
            lines_blank = sum(1 for line in content.split('\n') if not line.strip())
            lines_code = lines_total - lines_blank
            lines_comment = content.count('#')
            lines_docstring = 0
            
            # 计算指标
            num_functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
            num_classes = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            num_imports = len([node for node in ast.walk(tree) if isinstance(node, ast.Import)])
            
            # 类型注解覆盖率和文档字符串覆盖率
            type_annotation_coverage, docstring_coverage = self._calculate_coverage(tree)
            
            # 复杂度和可维护性
            cyclomatic_complexity = self._calculate_cyclomatic_complexity(tree)
            maintainability_index = self._calculate_maintainability(tree, num_functions, num_classes, lines_code)
            
            # 命名问题
            naming_issues = self._check_naming_conventions(tree)
            
            # 质量问题
            quality_issues = self._check_quality_issues(tree)
            
            # 安全问题
            security_issues = self._check_security_issues(tree)
            
            # 文件依赖
            files = self._count_imported_files(tree)
            
            # 复杂度和可维护性判断
            complexity_high = cyclomatic_complexity > 15
            maintainability_low = maintainability_index < 50
            
            # PEP8符合度
            pep8_compliant = self._check_pep8_compliance(tree)
            
            return CodeQualityMetrics(
                file_name=file_path.name,
                file_path=str(file_path),
                employee_id=self._extract_employee_id(file_path),
                employee_name=self._extract_employee_name(file_path),
                star_layer=self._extract_star_layer(file_path),
                task_id=self._extract_task_id(file_path),
                lines_total=lines_total,
                lines_code=lines_code,
                lines_blank=lines_blank,
                lines_comment=lines_comment,
                lines_docstring=lines_docstring,
                type_annotation_coverage=type_annotation_coverage,
                docstring_coverage=docstring_coverage,
                pep8_compliance=pep8_compliant,
                cyclomatic_complexity=cyclomatic_complexity,
                maintainability_index=maintainability_index,
                num_functions=num_functions,
                num_classes=num_classes,
                num_imports=num_imports,
                unused_imports=self._find_unused_imports(tree),
                function_lengths=self._get_function_lengths(tree),
                class_lengths=self._get_class_lengths(tree),
                naming_issues=naming_issues,
                quality_issues=quality_issues,
                security_issues=security_issues,
                files=files,
                complexity_high=complexity_high,
                maintainability_low=maintability_low,
                pep8_compliant=pep8_compliant
            )
            
        except Exception as e:
            print(f"❌ 文件检查失败 {file_path}: {e}")
            return None
    
    def _extract_employee_id(self, file_path: str) -> str:
        """从文件路径提取员工ID"""
        # 从文件名中提取（如 xj01_p0_001.py -> 001）
        match = re.search(r'(\d{3})', file_path.stem)
        return match.group(1) if match else "000"
    
    def _extract_employee_name(self, file_path: str) -> str:
        """从文件名或文件内容提取员工姓名"""
        # 尝试从文件名提取
        match = re.search(r'(?:陈元灵|周禄存|蒋巨门|薛贪狼|伍廉贞|谢武功|章破军|倪左辅|周右弼|齐辅弼)', file_path.stem)
        return match.group(1) if match else "未知"
    
    def _extract_star_layer(self, file_path: str) -> str:
        """从文件路径提取星层"""
        star_layers = {
            '01': 'XJ01紫微元灵',
            '02': 'XJ02禄存星',
            '03': 'XJ03巨门星',
            '04': 'XJ04廉贞星',
            '05': 'XJ05武曲星',
            '06': 'XJ06破军星',
            '07': 'XJ07左辅星',
            '08': 'XJ08右弼星',
            '09': 'XJ09贪狼星',
            '10': 'XJ10辅弼星辰',
        }
        
        for key, value in star_layers.items():
            if key in file_path:
                return value
        
        return "未知星层"
    
    def _extract_task_id(self, file_path: str) -> str:
        """从文件名提取任务ID"""
        match = re.search(r'(?:xj\d{2}-p[0-9]-\d{3})', file_path.stem, re.IGNORECASE)
        return match.group(1) if match else "未知任务"
    
    def _calculate_coverage(self, tree: ast.AST) -> Tuple[float, float]:
        """计算类型注解覆盖率和文档字符串覆盖率"""
        type_annotations = 0
        docstrings = 0
        
        for node in ast.walk(tree):
            # 类型注解
            for child_node in ast.iter_child_nodes(node):
                if isinstance(child_node, ast.AST):
                    type_annotations += 1
                elif isinstance(child_node, ast.AnnAssign):
                    type_annotations += 1
                elif isinstance(child_node, ast.AnnSubscript):
                    type_annotations += 2
                elif isinstance(child_node, ast.Subscript):
                    type_annotations += 2
            
            # 文档字符串
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    docstrings += 1
                for child in ast.iter_child_nodes(node):
                    if isinstance(child_node, ast.Expr):
                        docstrings += 1
            
            # 类文档字符串
            elif isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    docstrings += 1
                for child in ast.iter_child_nodes(node):
                    if isinstance(child_node, ast.Expr):
                        docstrings += 1
            
        # 计算覆盖率
        if type_annotations > 0:
            type_annotation_coverage = (type_annotations / self._count_functions_and_classes(tree)) * 100
        if docstrings > 0:
            docstring_coverage = (docstrings / (self._count_functions_and_classes(tree))) * 100
        
        return type_annotation_coverage, docstring_coverage
    
    def _count_functions_and_classes(self, tree: ast.AST) -> int:
        """计算函数和类的总数"""
        functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef)])
        classes = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
        return functions + classes
    
    def _calculate_cyclomatic_complexity(self, tree: ast.AST) -> float:
        """计算圈复杂度"""
        complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                complexity += self._function_complexity(node)
            elif isinstance(node, ast.ClassDef):
                complexity += self._class_complexity(node)
        return complexity
    
    def _function_complexity(self, node) -> int:
        """计算函数复杂度"""
        complexity = 1
        # if-elif嵌套+1
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.If) or isinstance(child, ast.While):
                complexity += 1
                complexity += self._function_complexity(child)
            elif isinstance(child, ast.For):
                complexity += 1
                complexity += self._function_complexity(child)
            elif isinstance(child, ast.With):
                complexity += 1
                complexity += self._function_complexity(child)
            elif isinstance(child, ast.Try):
                complexity += 2  # try-except
                complexity += self._function_complexity(child)
                complexity += self._function_complexity(child)
                complexity += self._function_complexity(child)
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
                complexity += self._function_complexity(child)
            elif isinstance(child, ast.Except):
                complexity += 1
                complexity += self._function_complexity(child)
            elif isinstance(child, ast.Finally):
                complexity += 1
                complexity += self._function_complexity(child)
                complexity += self._function_complexity(child)
                complexity += self._function_complexity(child)
            elif isinstance(child, ast.Raise):
                complexity += 1
                complexity += self._function_complexity(child)
            elif isinstance(child, ast.Return) or isinstance(child, ast.Yield):
                complexity += 1
                complexity += self._function_complexity(child)
            elif isinstance(child, ast.AsyncWith) or isinstance(child, AsyncWith):
                complexity += 1
                complexity += self._function_complexity(child)
                complexity += self._function_complexity(child)
                complexity += self._function_complexity(child)
        
        return complexity
    
    def _class_complexity(self, node) -> int:
        """计算类复杂度"""
        complexity = 1
        for child in ast.iter_child_nodes(node):
            complexity += self._node_complexity(child)
        return complexity
    
    def _node_complexity(self, node) -> int:
        """计算节点复杂度"""
        complexity = 1
        for child in ast.iter_child_nodes(node):
            complexity += self._node_complexity(child)
        return complexity
    
    def _check_naming_conventions(self, tree: ast.AST) -> List[str]:
        """检查命名规范"""
        issues = []
        
        # 检查函数命名
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z_][a-zA-Z0-9_]*$', node.name, re.IGNORECASE):
                    issues.append(f"函数名不符合PEP8: {node.name}")
                if node.name.isupper():
                    issues.append(f"函数名不应全大写: {node.name}")
            
            # 检查变量命名
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    if not re.match(r'^[a-z_][a-zA-Z0-9_]*$', node.id, re.IGNORECASE):
                        issues.append(f"变量名不符合PEP8: {node.id}")
                    if node.id.isupper():
                        issues.append(f"变量名不应全大写: {node.id}")
                for child in ast.iter_child_nodes(node):
                    for grandchild in ast.iter_child_nodes(child):
                        if isinstance(grandchild, ast.Name):
                            if not re.match(r'^[a-z_][a-zA-Z0-9_]*$', grandchild.id, re.IGNORECASE):
                                issues.append(f"变量名不符合PEP8: {grandchild.id}")
        
        # 检查类命名
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not re.match(r'^[A-Z][a-zA-Z0-9]+', node.name, re.IGNORECASE):
                    issues.append(f"类名不符合PascalCase: {node.name}")
        
        return issues
    
    def _check_quality_issues(self, tree: ast.AST) -> List[str]:
        """检查质量问题"""
        issues = []
        
        # 检查未使用的导入
        unused_imports = self._find_unused_imports(tree)
        if unused_imports:
            unused_str = ", ".join([f"·{imp}" for imp in unused_imports[:5]])
            if len(unused_imports) > 5:
                issues.append(f"存在大量未使用的导入: {len(unused_imports)}个: {unused_str}...")
        
        # 检查过长的函数
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._function_complexity(node)
                if complexity > 20:
                    issues.append(f"函数 '{node.name}' 复杂度过高: {complexity}")
            elif isinstance(node, ast.ClassDef):
                complexity = self._class_complexity(node)
                if complexity > 30:
                    issues.append(f"类 '{node.name}' 复杂度过高: {complexity}")
        
        return issues
    
    def _check_security_issues(self, tree: ast.AST) -> List[str]:
        """检查安全问题"""
        issues = []
        
        # 检查危险的函数调用
        dangerous_calls = [
            'eval',
            'exec',
            'open',
            'subprocess',
            'os.system',
            'os.popen',
            'compile'
        ]
        
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name) and child.func.id in dangerous_calls:
                        issues.append(f"检测到危险函数调用: {child.func.id}")
                    elif isinstance(child, ast.Attribute):
                        if child.attr in dangerous_calls:
                        issues.append(f"检测到危险属性: {child.attr}")
        
        return issues
    
    def _find_unused_imports(self, tree: ast.AST) -> List[str]:
        """查找未使用的导入"""
        imports = set()
        used_imports = set()
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.ImportFrom)):
                for alias in node.names:
                    imports.add(alias)
                for name in node.names:
                    if name:  # 不仅仅是别名
                        used_imports.add(name)
            elif isinstance(node, (ast.ImportFrom, ast.Import)):
                for alias in node.module:
                    imports.add(alias)
                for name in node.names:
                    if name:
                        used_imports.add(name)
        
        unused = sorted(list(imports - used_imports))
        return unused
    
    def _get_function_lengths(self, tree: ast.AST) -> List[int]:
        """获取所有函数的长度"""
        lengths = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                lengths.append(len(node.body))
        return lengths
    
    def _get_class_lengths(self, tree: ast.AST) -> List[int]:
        """获取所有类的长度"""
        lengths = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                lengths.append(len(node.body))
        return lengths
    
    def check_pep8_compliance(self, tree: ast.AST) -> bool:
        """检查PEP8规范符合度"""
        # 检查缩进
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                if not re.match(r'^[ \t]*for [ \t]+.*:', node.body[0], re.UNICODE):
                    return False
            elif isinstance(node, ast.While) or isinstance(node, node.orelse):
                if not re.match(r'^[ \t]*while [ \t]+.*:', node.body[0], re.UNICODE):
                    return False
        
        # 检查导入顺序
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.ImportFrom)):
                imports = [node.names[0] if node.names else 'default']
                for name in node.names:
                    if name and name not in imports:
                        return False
        
        return True

def main():
    """主函数"""
    inspector = CodeQualityInspector("/workspace/projects/workspace/xuanji-engine-v2")
    metrics = inspector.inspect_all_files()
    
    if not metrics:
        print("❌ 没有找到Python文件")
        return
    
    print("\n" + "=" * 80)
    print("📋 AI数字员工第三期开发 - 代码质检报告")
    print("=" * 80)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 按星层统计
    star_layers = defaultdict(lambda: {
        "XJ01": "紫微元灵",
        "XJ02": "禄存星",
        "XJ03": "巨门星",
        "XJ04": "廉贞星",
        "XJ05": "武曲星",
        "XJ06": "破军星",
        "XJ07": "左辅星",
        "XJ08": "右弼星",
        "XJ09": "贪狼星",
        "XJ10": "辅弼星辰"
    })
    
    # 分类统计
    quality_good = 0  # 优秀
    quality_warnings = 0  # 警告
    quality_errors = 0    # 错误
    critical_issues = []  # 严重问题
    
    print("\n📊 整体质量统计:")
    print(f"  总文件数: {len(metrics)}")
    print(f" 总代码行数: {sum(m.lines_code for m in metrics)}")
    print(f" 类型注解覆盖率: {sum(m.type_annotation_coverage for m in metrics) / len(metrics):.1f}%")
    print(f" 文档字符串覆盖率: {sum(m.docstring_coverage for m in metrics) / len(metrics):.1f}%")
    print(f" PEP8符合: {sum(1 for m in metrics if m.pep8_compliant)}/{len(metrics)} ({sum(1 for m in metrics if m.pep8_compliant) / len(metrics) * 100:.1f}%)")
    
    print("\n🔴 按星层质量统计:")
    for layer, layer_name in star_layers.items():
        layer_files = [m for m in metrics if layer in m.star_layer]
        if layer_files:
            avg_coverage = sum(m.type_annotation_coverage for m in layer_files) / len(layer_files)
            avg_docstring = sum(m.docstring_coverage for m in layer_files) / len(layer_files)
            avg_pep8 = sum(1 for m in layer_files if m.pep8_compliant) / len(layer_files)
            avg_complexity = sum(m.cyclomatic_complexity for m in layer_files) / len(layer_files)
            avg_maintainability = sum(m.maintainability_index for m in layer_files) / len(layer_files)
            
            print(f"\n{layer_name}:")
            print(f"  文件数: {len(layer_files)}")
            print(f" 代码行数: {sum(m.lines_code for m in layer_files)}")
            print(f"  平均类型注解覆盖率: {avg_coverage:.1f}%")
            print(f" 平均文档字符串覆盖率: {avg_docstring:.1f}%")
            print(f" 平均复杂度: {avg_complexity:.1f}")
            print(f" 平均可维护性: {avg_maintainability:.1f}%")
            print(f" PEP8符合: {avg_pep8:.1f}%")
            
            # 显示该星层的质量问题
            quality_issues_in_layer = [issue for m in layer_files for issue in m.quality_issues for issue in m.quality_issues]
            naming_issues_in_layer = [issue for m in layer_files for issue in m.naming_issues for issue in m.naming_issues]
            security_issues_in_layer = [issue for m in layer_files for issue in m.security_issues for issue in m.security_issues]
            
            if quality_issues_in_layer:
                print(f"\n  ⚠️  质量问题 ({len(quality_issues_in_layer)}个):")
                for issue in quality_issues_in_layer[:5]:
                    print(f"    • {issue}")
            if naming_issues_in_layer:
                print(f"\n  🔧 命名问题 ({len(naming_issues_in_layer)}个):")
                for issue in naming_issues_in_layer[:5]:
                    print(f"    • {issue}")
            if security_issues_in_layer:
                print(f"\n  🔒 安全问题 ({len(security_issues_in_layer)}个):")
                for issue in security_issues_in_layer[:5]:
                    print(f"    • {issue}")
            
            # 显示严重问题
            critical_in_layer = [m for m in layer_files if m.complexity_high or m.maintainability_low]
            if critical_in_layer:
                print(f"\n  🔴 严重问题 ({len(critical_in_layer)}个):")
                for m in critical_in_layer[:5]:
                    print(f"    ⚠️  {m.employee_name} - {m.task_id} - 复杂度{m.cyclomatic_complexity} 可维护性{m.maintainability}")
                if m.complexity_high and m.maintainability_low:
                    print(f"    ⚠️  {m.employee_name} - {m.task_id} - 复杂度过高且可维护性低")
    
    print("\n📊 质量分级统计:")
    quality_good = sum(1 for m in metrics if m.type_annotation_coverage >= 95 and m.docstring_coverage >= 95 and m.pep8_compliant)
    quality_warnings = sum(1 for m in metrics if (0.7 <= m.type_annotation_coverage < 95 or 0.7 <= m.docstring_coverage < 95 or not m.pep8_compliant))
    quality_errors = len(metrics) - quality_good - quality_warnings
    critical_issues = len([m for m in metrics if m.complexity_high and m.maintainability_low])
    
    print(f"\n  ✅ 优秀: {quality_good} 个 (类型注解≥95% AND 文档≥95% AND PEP8符合)")
    print(f"  ⚠️  警告: {quality_warnings} 个 (覆盖率或PEP8不符合)")
    print(f"  ❌ 错误: {quality_errors} 个 (复杂度或可维护性问题)")
    print(f"  🔴 严重问题: {critical_issues} 个 (复杂度>15 且可维护性<50)")
    
    # 详细问题清单
    all_issues = defaultdict(list)
    for m in metrics:
        for issue in m.quality_issues:
            all_issues[f"{m.employee_name}({m.task_id})"]: issue]
        for issue in m.naming_issues:
            all_issues[f"{m.employee_name}({m.task_id})"]: issue]
        for issue in m.security_issues:
            all_issues[f"{m.employee_name}({m.task_id})"]: issue]
    
    if all_issues:
        print(f"\n📝 详细问题清单 (前20个):")
        issue_count = 0
        for employee, issues in sorted(all_issues.items()):
            print(f"\n  {employee}:")
            for issue in issues[:2]:
                print(f"    • {issue}")
                issue_count += 1
            if issue_count >= 20:
                print(f"    ... 还有 {len(issues) - 2} 个问题")
                break
            break
    
    # 统计数据
    total_employees = len({m.employee_id for m in metrics})
    good_employees = len([m for m in metrics if m.type_annotation_coverage >= 95 and m.docstring_coverage >= 95 and m.pep8_compliant])
    warning_employees = len([m for m in metrics if (0.7 <= m.type_annotation_coverage < 95 or 0.7 <= m.docstring_coverage < 95 or not m.pep8_compliant)])
    error_employees = len(metrics) - good_employees - warning_employees
    
    print(f"\n👘 员工质量统计:")
    print(f"  ✅ 优秀: {good_employees} 人")
    print(f"  ⚠️  警告: {warning_employees} 人")
    print(f"  ❌ 错误: {error_employees} 人")
    print(f"  🔴 严重问题: {critical_issues} 人")
    
    # GitHub仓库检查
    print(f"\n📦 Git仓库状态:")
    try:
        result = subprocess.run(
            ['git', 'log', '--oneline', '--all', '--oneline', '--oneline-graph', '--all', '--decorate'],
            cwd="/workspace/projects/workspace/xuanji-engine-v2",
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            commits = [l for l in lines if l.strip().startswith('*') or l.strip().startswith('(') or 'commit ' in l.lower()[:1]]
            print(f"✅ Git提交历史: {len(commits)} 次")
            
            # 统计最近10次提交的作者
            authors = defaultdict(int)
            for commit in commits:
                match = re.search(r'^\s*([A-Z][a-z]+)', commit)
                if match:
                    authors[match.group(1)] += 1
            
            print(f"活跃开发者: {len(authors)} 人:")
            for author, count in sorted(authors.items(), reverse=True)[:10]:
                print(f"  - {author}: {count} 次提交")
            
            # 获取最新一次提交
            result = subprocess.run(
                ['git', 'log', '-1', '--pretty=format:%h'],
                cwd="/workspace/projects/workspace/xuanji-engine-v2",
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                latest_commit = result.stdout.strip().split('\n')[0]
                print(f"  最新提交: {latest_commit}")
        
    except Exception as e:
        print(f"⚠️  Git检查失败: {e}")

if __name__ == "__main__":
    main()

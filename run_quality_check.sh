#!/bin/bash
# 张志远(002) 代码质检任务
# 执行时间: 2026-03-22

cd /workspace/projects/workspace/xuanji-engine-v2

echo "=== 张志远(002) 代码质检任务 ==="
echo "时间: $(date)"
echo ""

# 统计各星层代码
echo "📊 代码统计:"
total_files=0
total_lines=0
for dir in 01 02 03 04 05 06 07 08 09 10; do
  count=$(ls $dir/*/star/*.py 2>/dev/null | wc -l)
  lines=$(cat $dir/*/star/*.py 2>/dev/null | wc -l)
  total_files=$((total_files + count))
  total_lines=$((total_lines + lines))
  echo "  XJ-$dir: $count 文件, $lines 行"
done
echo "  总计: $total_files 文件, $total_lines 行"
echo ""

# 质量检查
echo "📈 质量指标:"
has_docs=0
has_type=0
for dir in 01 02 03 04 05 06 07 08 09 10; do
  for file in $dir/*/star/*.py; do
    if [ -f "$file" ]; then
      if grep -q '"""' "$file"; then
        has_docs=$((has_docs + 1))
      fi
      if grep -q ": str\|: int\|: float\|: bool\|: List\|: Dict" "$file"; then
        has_type=$((has_type + 1))
      fi
    fi
  done
done
echo "  文档覆盖率: $(awk "BEGIN {printf \"%.1f\", ($has_docs/$total_files)*100}")%"
echo "  类型注解覆盖率: $(awk "BEGIN {printf \"%.1f\", ($has_type/$total_files)*100}")%"
echo ""

# 问题文件列表
echo "⚠️ 需要改进的文件:"
problem_count=0
for dir in 01 02 03 04 05 06 07 08 09 10; do
  for file in $dir/*/star/*.py; do
    if [ -f "$file" ]; then
      has_type=$(grep -c ": str\|: int\|: float\|: bool" "$file")
      if [ "$has_type" -eq 0 ]; then
        echo "  - $file (缺少类型注解)"
        problem_count=$((problem_count + 1))
      fi
    fi
  done
done

echo ""
echo "=== 质检完成 ==="
echo "发现问题文件: $problem_count 个"

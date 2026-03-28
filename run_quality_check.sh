#!/bin/bash
# 玄玑引擎项目质检任务
# 更新时间: 2026-03-27
# 轮询间隔: 1小时

cd /workspace/projects/workspace

# 时间戳
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
REPORT_FILE="memory/玄玑引擎项目质检报告-$(date "+%Y-%m-%d-%H-%M").md"

echo "# 玄玑引擎项目质检报告" > "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**质检时间**: $TIMESTAMP" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 读取任务状态
TASKS_FILE="skills/digital-employee-manager/state/task_status.json"
PROJECT_FILE="skills/digital-employee-manager/state/project_status.json"

# 初始化变量
TOTAL_TASKS=0
COMPLETED_TASKS=0
IN_PROGRESS_TASKS=0
PENDING_TASKS=0
PROJECT_PROGRESS=0
PROJECT_PHASE="未知"

if [ -f "$PROJECT_FILE" ]; then
  PROJECT_PROGRESS=$(python3 -c "import json; print(json.load(open('$PROJECT_FILE')).get('xuanji_engine_v4', {}).get('progress', 0))")
  PROJECT_PHASE=$(python3 -c "import json; print(json.load(open('$PROJECT_FILE')).get('xuanji_engine_v4', {}).get('phase', '未知'))")
fi

if [ -f "$TASKS_FILE" ]; then
  TOTAL_TASKS=$(python3 -c "import json; print(len(json.load(open('$TASKS_FILE'))))")
  COMPLETED_TASKS=$(python3 -c "import json; tasks = json.load(open('$TASKS_FILE')); print(len([k for k,v in tasks.items() if v.get('status') == 'completed']))")
  IN_PROGRESS_TASKS=$(python3 -c "import json; tasks = json.load(open('$TASKS_FILE')); print(len([k for k,v in tasks.items() if v.get('status') == 'in_progress']))")
  PENDING_TASKS=$(python3 -c "import json; tasks = json.load(open('$TASKS_FILE')); print(len([k for k,v in tasks.items() if v.get('status') == 'pending']))")
fi

# 计算任务完成率
if [ "$TOTAL_TASKS" -gt 0 ]; then
  TASK_COMPLETION=$(python3 -c "import json; tasks = json.load(open('$TASKS_FILE')); completed = len([k for k,v in tasks.items() if v.get('status') == 'completed']); total = len(tasks); print(int(completed/total*100))")
else
  TASK_COMPLETION=0
fi

# 基于项目阶段确定完成度
PHASE_COMPLEPONENT=0
if [ "$PROJECT_PHASE" = "第四期（功能迭代）" ]; then
  PHASE_COMPLEPONENT=$PROJECT_PROGRESS
elif [ "$PROJECT_PHASE" = "第三期（四端开发）" ]; then
  PHASE_COMPLEPONENT=100
elif [ "$PROJECT_PHASE" = "第二期（核心开发）" ]; then
  PHASE_COMPLEPONENT=100
elif [ "$PROJECT_PHASE" = "第一期（架构设计）" ]; then
  PHASE_COMPLEPONENT=100
fi

# Git提交统计（最近6小时）
cd xuanji-engine-v2
RECENT_COMMITS=$(git log --since="6 hours ago" --no-merges 2>/dev/null | grep -c "^commit" || echo 0)
RECENT_COMMITS_24H=$(git log --since="24 hours ago" --no-merges 2>/dev/null | grep -c "^commit" || echo 0)

# 代码统计
BACKEND_PY=$(find backend -type f -name "*.py" 2>/dev/null | wc -l)
FRONTEND_TS=$(find frontend -path "*/node_modules" -prune -o -type f \( -name "*.ts" -o -name "*.tsx" \) -print 2>/dev/null | wc -l)
FRONTEND_JS=$(find frontend -path "*/node_modules" -prune -o -type f \( -name "*.js" -o -name "*.jsx" \) -print 2>/dev/null | wc -l)

# 服务器状态检查（可选）
SERVER_STATUS="未检查"
if [ -f "DEPLOYMENT_COMPLETE_REPORT.md" ]; then
  SERVER_STATUS="已部署"
fi

# 回到上层目录
cd ..

# 生成报告
echo "## 📊 核心指标" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "| 维度 | 状态 | 数值 | 说明 |" >> "$REPORT_FILE"
echo "|------|------|------|------|" >> "$REPORT_FILE"
echo "| 项目阶段 | $PROJECT_PHASE | - | 当前执行阶段 |" >> "$REPORT_FILE"
echo "| 项目进度 | $PHASE_COMPLEPONENT% | $PROJECT_PROGRESS% | 基于阶段计算 |" >> "$REPORT_FILE"
echo "| 任务完成度 | $TASK_COMPLETION% | $COMPLETED_TASKS/$TOTAL_TASKS | 已完成/总任务 |" >> "$REPORT_FILE"
echo "| 后端代码 | $BACKEND_PY个文件 | | Python文件数 |" >> "$REPORT_FILE"
echo "| 前端代码 | $((FRONTEND_TS + FRONTEND_JS))个文件 | | TS/JS文件数 |" >> "$REPORT_FILE"
echo "| Git提交(6h) | $RECENT_COMMITS次 | | 最近6小时提交 |" >> "$REPORT_FILE"
echo "| Git提交(24h) | $RECENT_COMMITS_24H次 | | 最近24小时提交 |" >> "$REPORT_FILE"
echo "| 服务器状态 | $SERVER_STATUS | | 部署状态 |" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "## 📋 任务分布" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "| 状态 | 数量 | 占比 |" >> "$REPORT_FILE"
echo "|------|------|------|" >> "$REPORT_FILE"

if [ "$TOTAL_TASKS" -gt 0 ]; then
  COMPLETED_PCT=$(python3 -c "import json; tasks = json.load(open('$TASKS_FILE')); completed = len([k for k,v in tasks.items() if v.get('status') == 'completed']); total = len(tasks); print(f'{int(completed/total*100)}%')")
  IN_PROGRESS_PCT=$(python3 -c "import json; tasks = json.load(open('$TASKS_FILE')); in_progress = len([k for k,v in tasks.items() if v.get('status') == 'in_progress']); total = len(tasks); print(f'{int(in_progress/total*100)}%')")
  PENDING_PCT=$(python3 -c "import json; tasks = json.load(open('$TASKS_FILE')); pending = len([k for k,v in tasks.items() if v.get('status') == 'pending']); total = len(tasks); print(f'{int(pending/total*100)}%')")
else
  COMPLETED_PCT="0%"
  IN_PROGRESS_PCT="0%"
  PENDING_PCT="0%"
fi

echo "| ✅ 已完成 | $COMPLETED_TASKS | ${COMPLETED_PCT} |" >> "$REPORT_FILE"
echo "| 🔄 进行中 | $IN_PROGRESS_TASKS | ${IN_PROGRESS_PCT} |" >> "$REPORT_FILE"
echo "| ⏳ 待执行 | $PENDING_TASKS | ${PENDING_PCT} |" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 添加任务详情
echo "## 📝 任务详情" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 已完成任务
echo "### ✅ 已完成任务 ($COMPLETED_TASKS个)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
if [ "$COMPLETED_TASKS" -gt 0 ]; then
  python3 << PYTHON_SCRIPT >> "$REPORT_FILE"
import json
tasks = json.load(open('$TASKS_FILE'))
completed = {k: v for k, v in tasks.items() if v.get('status') == 'completed'}
for task_id, task in sorted(completed.items()):
    phase = task.get('phase', '-')
    name = task.get('name', 'Unknown')
    progress = task.get('progress', 0)
    print(f"- **{task_id}** [{phase}期] {name} (进度: {progress}%)")
PYTHON_SCRIPT
else
  echo "* 无" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 进行中任务
echo "### 🔄 进行中任务 ($IN_PROGRESS_TASKS个)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
if [ "$IN_PROGRESS_TASKS" -gt 0 ]; then
  python3 << PYTHON_SCRIPT >> "$REPORT_FILE"
import json
tasks = json.load(open('$TASKS_FILE'))
in_progress = {k: v for k, v in tasks.items() if v.get('status') == 'in_progress'}
for task_id, task in sorted(in_progress.items()):
    phase = task.get('phase', '-')
    name = task.get('name', 'Unknown')
    progress = task.get('progress', 0)
    print(f"- **{task_id}** [{phase}期] {name} (进度: {progress}%)")
PYTHON_SCRIPT
else
  echo "* 无" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 待执行任务
echo "### ⏳ 待执行任务 ($PENDING_TASKS个)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
if [ "$PENDING_TASKS" -gt 0 ]; then
  python3 << PYTHON_SCRIPT >> "$REPORT_FILE"
import json
tasks = json.load(open('$TASKS_FILE'))
pending = {k: v for k, v in tasks.items() if v.get('status') == 'pending'}
for task_id, task in sorted(pending.items()):
    phase = task.get('phase', '-')
    name = task.get('name', 'Unknown')
    priority = task.get('priority', 'P1')
    print(f"- **{task_id}** [{priority}] [{phase}期] {name}")
PYTHON_SCRIPT
else
  echo "* 无" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 核心发现
echo "## 🔍 核心发现" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

ISSUES=0
WARNINGS=0

if [ "$RECENT_COMMITS" -lt 5 ]; then
  echo "- 🔴 **代码提交活跃度低** - 6小时内仅${RECENT_COMMITS}次提交，建议关注开发进度" >> "$REPORT_FILE"
  ISSUES=$((ISSUES + 1))
fi

if [ "$IN_PROGRESS_TASKS" -gt 5 ]; then
  echo "- 🟡 **多任务并行** - ${IN_PROGRESS_TASKS}个任务同时进行中，需关注资源分配" >> "$REPORT_FILE"
  WARNINGS=$((WARNINGS + 1))
fi

if [ "$PENDING_TASKS" -gt 10 ]; then
  echo "- 🟡 **待处理任务较多** - ${PENDING_TASKS}个任务待执行，建议评估优先级" >> "$REPORT_FILE"
  WARNINGS=$((WARNINGS + 1))
fi

if [ "$ISSUES" -eq 0 ] && [ "$WARNINGS" -eq 0 ]; then
  echo "- ✅ **项目运行正常** - 所有关键指标健康" >> "$REPORT_FILE"
fi

echo "" >> "$REPORT_FILE"

# 下次质检时间
NEXT_HOUR=$(date -d "+1 hour" "+%H:%M")
echo "## ⏰ 下次质检" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "**时间**: $NEXT_HOUR (1小时后)" >> "$REPORT_FILE"
echo "**文件**: $REPORT_FILE" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

echo "---" >> "$REPORT_FILE"
echo "*质检完成时间: $TIMESTAMP*" >> "$REPORT_FILE"

# 输出到控制台
echo "=== 玄玑引擎项目质检报告 ==="
echo "时间: $TIMESTAMP"
echo ""
echo "项目阶段: $PROJECT_PHASE"
echo "项目进度: $PROJECT_PROGRESS%"
echo "任务: $COMPLETED_TASKS/$TOTAL_TASKS 完成 ($TASK_COMPLETION%)"
echo "Git提交(6h): $RECENT_COMMITS次"
echo ""
echo "报告已保存至: $REPORT_FILE"
echo "下次质检: $NEXT_HOUR (1小时后)"

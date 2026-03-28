/**
 * 小元 - 代码审查服务
 * 提供代码质量检查、安全漏洞提示、性能优化建议等功能
 */

import {
  CodeReviewRequest,
  CodeReviewResult,
  ReviewIssue,
  ReviewSuggestion,
  ReviewRule,
  CodeMetrics,
  SecurityVulnerability,
} from '../types';

export class CodeReviewService {
  private config: any;
  private logger: any;
  private rules: Map<string, ReviewRule> = new Map();

  constructor(config: any, logger: any) {
    this.config = config;
    this.logger = logger;
    this.initializeRules();
  }

  /**
   * 初始化代码审查规则
   */
  private initializeRules(): void {
    // 安全规则
    this.registerRule({
      id: 'no-hardcoded-secrets',
      name: '不允许硬编码密钥',
      category: 'security',
      severity: 'critical',
      enabled: true,
      config: {
        patterns: [
          /password\s*=\s*['"][\w]+['"]/gi,
          /api[_-]?key\s*=\s*['"][\w]+['"]/gi,
          /secret\s*=\s*['"][\w]+['"]/gi,
          /token\s*=\s*['"][\w]+['"]/gi,
        ],
      },
    });

    this.registerRule({
      id: 'sql-injection',
      name: 'SQL 注入风险',
      category: 'security',
      severity: 'high',
      enabled: true,
      config: {
        patterns: [
          /execute\s*\(\s*['"]\s*\+.*['"]/gi,
          /query\s*\(\s*['"]\s*\+.*['"]/gi,
          /\$?\w+\s*=\s*['"][\w\s]*['"]\s*\+.*\s*;\s*\$?\w+\s*=.*query/i,
        ],
      },
    });

    this.registerRule({
      id: 'xss-vulnerability',
      name: 'XSS 跨站脚本风险',
      category: 'security',
      severity: 'high',
      enabled: true,
      config: {
        patterns: [
          /innerHTML\s*=.*userInput/i,
          /document\.write\s*\(.*userInput/i,
          /eval\s*\(\s*user/i,
        ],
      },
    });

    this.registerRule({
      id: 'insecure-random',
      name: '不安全的随机数生成',
      category: 'security',
      severity: 'medium',
      enabled: true,
      config: {
        patterns: [] as RegExp[],
      },
    });

    // 性能规则
    this.registerRule({
      id: 'no-nested-loops',
      name: '避免深层嵌套循环',
      category: 'performance',
      severity: 'medium',
      enabled: true,
      config: {
        maxDepth: 3,
      },
    });

    this.registerRule({
      id: 'avoid-multiple-api-calls',
      name: '避免多个同步 API 调用',
      category: 'performance',
      severity: 'medium',
      enabled: true,
      config: {
        maxSequentialCalls: 3,
      },
    });

    this.registerRule({
      id: 'use-memoization',
      name: '使用缓存/记忆化优化性能',
      category: 'performance',
      severity: 'low',
      enabled: true,
      config: {
        detectRepeatedCalculations: true,
      },
    });

    // 代码质量规则
    this.registerRule({
      id: 'no-console-log',
      name: '生产代码不应包含 console.log',
      category: 'quality',
      severity: 'low',
      enabled: true,
      config: {
        allowedInDevelopment: true,
      },
    });

    this.registerRule({
      id: 'consistent-naming',
      name: '命名一致性',
      category: 'quality',
      severity: 'medium',
      enabled: true,
      config: {
        enforceCamelCase: true,
        enforcePascalCaseForClasses: true,
      },
    });

    this.registerRule({
      id: 'proper-error-handling',
      name: '适当的错误处理',
      category: 'quality',
      severity: 'high',
      enabled: true,
      config: {
        requireTryCatch: true,
      },
    });

    this.registerRule({
      id: 'function-length',
      name: '函数长度限制',
      category: 'quality',
      severity: 'medium',
      enabled: true,
      config: {
        maxLines: 50,
      },
    });

    // 代码风格规则
    this.registerRule({
      id: 'max-line-length',
      name: '代码行长度限制',
      category: 'style',
      severity: 'low',
      enabled: true,
      config: { maxLength: 120 },
    });

    this.registerRule({
      id: 'no-trailing-whitespace',
      name: '无尾随空白',
      category: 'style',
      severity: 'low',
      enabled: true,
    });
  }

  /**
   * 注册审查规则
   */
  private registerRule(rule: ReviewRule): void {
    this.rules.set(rule.id, rule);
    this.logger.debug(`Registered code review rule: ${rule.id}`);
  }

  /**
   * 执行代码审查
   */
  async reviewCode(request: CodeReviewRequest): Promise<CodeReviewResult> {
    this.logger.debug(`Starting code review for ${request.language} code`);

    const lines = request.code.split('\n');
    const issues: ReviewIssue[] = [];
    const suggestions: ReviewSuggestion[] = [];

    // 执行所有启用的规则
    for (const rule of this.rules.values()) {
      if (!rule.enabled) continue {
      }

      if (request.rules) {
        const customRule = request.rules.find(r => r.id === rule.id);
        if (customRule && !customRule.enabled) continue;
      }

      const ruleIssues = await this.checkRule(rule, request.code, lines);
      issues.push(...ruleIssues);
    }

    // 生成代码指标
    const metrics = this.calculateMetrics(request.code, lines, issues);

    // 生成优化建议
    const codeSuggestions = this.generateSuggestions(request.code, metrics, request.language);
    suggestions.push(...codeSuggestions);

    // 计算总体评分
    const overallScore = this.calculateScore(issues, metrics);

    const result: CodeReviewResult = {
      overallScore,
      summary: this.generateSummary(overallScore, issues, metrics),
      issues: issues.sort((a, b) => {
        const severityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
        return severityOrder[a.severity] - severityOrder[b.severity];
      }),
      suggestions,
      metrics,
      timestamp: Date.now(),
    };

    this.logger.info(`Code review completed. Score: ${overallScore}/100, Issues: ${issues.length}`);

    return result;
  }

  /**
   * 检查单个规则
   */
  private async checkRule(rule: ReviewRule, code: string, lines: string[]): Promise<ReviewIssue[]> {
    const issues: ReviewIssue[] = [];

    switch (rule.id) {
      case 'no-hardcoded-secrets':
        issues.push(...this.checkHardcodedSecrets(rule, code, lines));
        break;
      case 'sql-injection':
        issues.push(...this.checkSqlInjection(rule, code, lines));
        break;
      case 'xss-vulnerability':
        issues.push(...this.checkXssVulnerability(rule, code, lines));
        break;
      case 'no-console-log':
        issues.push(...this.checkConsoleLog(rule, code, lines));
        break;
      case 'function-length':
        issues.push(...this.checkFunctionLength(rule, code, lines));
        break;
      case 'max-line-length':
        issues.push(...this.checkLineLength(rule, code, lines));
        break;
      case 'proper-error-handling':
        issues.push(...this.checkErrorHandling(rule, code, lines));
        break;
      default:
        // 对于其他规则，使用模式匹配
        if (rule.config?.patterns) {
          issues.push(...this.checkByPatterns(rule, code, lines));
        }
    }

    return issues;
  }

  /**
   * 检查硬编码密钥
   */
  private checkHardcodedSecrets(rule: ReviewRule, code: string, lines: string[]): ReviewIssue[] {
    const issues: ReviewIssue[] = [];
    const patterns = rule.config?.patterns || [];

    lines.forEach((line, index) => {
      patterns.forEach((pattern: RegExp) => {
        const matches = line.match(pattern);
        if (matches) {
          issues.push({
            id: `${rule.id}-${index}`,
            category: rule.category,
            severity: rule.severity,
            title: rule.name,
            description: '检测到潜在的硬编码敏感信息',
            line: index + 1,
            column: line.indexOf(matches[0]) + 1,
            rule: rule.id,
            codeSnippet: line.trim(),
            suggestedFix: '使用环境变量或配置文件存储敏感信息',
          });
        }
      });
    });

    return issues;
  }

  /**
   * 检查 SQL 注入
   */
  private checkSqlInjection(rule: ReviewRule, code: string, lines: string[]): ReviewIssue[] {
    const issues: ReviewIssue[] = [];

    lines.forEach((line, index) => {
      if (/execute\s*\(\s*['"]\s*\+/i.test(line) || /query\s*\(\s*['"]\s*\+/i.test(line)) {
        issues.push({
          id: `${rule.id}-${index}`,
          category: rule.category,
          severity: rule.severity,
          title: rule.name,
          description: '直接拼接 SQL 语句可能导致注入攻击',
          line: index + 1,
          rule: rule.id,
          codeSnippet: line.trim(),
          suggestedFix: '使用参数化查询或 ORM',
        });
      }
    });

    return issues;
  }

  /**
   * 检查 XSS 漏洞
   */
  private checkXssVulnerability(rule: ReviewRule, code: string, lines: string[]): ReviewIssue[] {
    const issues: ReviewIssue[] = [];

    lines.forEach((line, index) => {
      if (/innerHTML\s*=/i.test(line) || /document\.write\s*\(/i.test.test(line)) {
        issues.push({
          id: `${rule.id}-${index}`,
          category: rule.category,
          severity: rule.severity,
          title: rule.name,
          description: '直接设置 innerHTML 或使用 document.write 可能导致 XSS 攻击',
          line: index + 1,
          rule: rule.id,
          codeSnippet: line.trim(),
          suggestedFix: '使用 textContent 或安全的 HTML 消毒库',
        });
      }
    });

    return issues;
  }

  /**
   * 检查 console.log
   */
  private checkConsoleLog(rule: ReviewRule, code: string, lines: string[]): ReviewIssue[] {
    const issues: ReviewIssue[] = [];

    lines.forEach((line, index) => {
      if (/console\.(log|debug|info|warn|error|trace)/.test(line) && !line.includes('eslint-disable')) {
        issues.push({
          id: `${rule.id}-${index}`,
          category: rule.category,
          severity: rule.severity,
          title: rule.name,
          description: '生产代码中不应保留调试日志',
          line: index + 1,
          rule: rule.id,
          codeSnippet: line.trim(),
          suggestedFix: '移除或替换为适当的日志系统',
            // 添加 eslint-disable 注释
        });
      }
    });

    return issues;
  }

  /**
   * 检查函数长度
   */
  private checkFunctionLength(rule: ReviewRule, code: string, lines: string[]): ReviewIssue[] {
    const issues: ReviewIssue[] = [];
    const maxLength = rule.config?.maxLines || 50;

    let currentFunction: { name: string; start: number; } | null = null;
    let braceCount = 0;

    lines.forEach((line, index) => {
      const functionMatch = line.match(/function\s+(\w+)\s*\(|const\s+(\w+)\s*=\s*(?:async\s+)?\(?/);
      if (functionMatch) {
        if (currentFunction && braceCount === 0) {
          const length = index - currentFunction.start;
          if (length > maxLength) {
            issues.push({
              id: `${rule.id}-${currentFunction.start}`,
              category: rule.category,
              severity: rule.severity,
              title: rule.name,
              description: `函数 ${currentFunction.name} 过长 (${length} 行)`,
              line: currentFunction.start + 1,
              rule: rule.id,
              codeSnippet: `function ${currentFunction.name}() { ... } (${length} lines)`,
              suggestedFix: '考虑将函数拆分为更小的函数',
            });
          }
        }
        currentFunction = {
          name: functionMatch[1] || functionMatch[2] || 'anonymous',
          start: index,
        };
        braceCount = 0;
      }

      braceCount += (line.match(/\{/g) || []).length;
      braceCount -= (line.match(/\}/g) || []).length;
    });

    return issues;
  }

  /**
   * 检查行长度
   */
  private checkLineLength(rule: ReviewRule, code: string, lines: string[]): ReviewIssue[] {
    const issues: ReviewIssue[] = [];
    const maxLength = rule.config?.maxLength || 120;

    lines.forEach((line, index) => {
      if (line.length > maxLength) {
        issues.push({
          id: `${rule.id}-${index}`,
          category: rule.category,
          severity: rule.severity,
          title: rule.name,
          description: `代码行过长 (${line.length} 字符)`,
          line: index + 1,
          column: maxLength + 1,
          rule: rule.id,
          codeSnippet: line.trim(),
          suggestedFix: '将长行拆分为多行',
        });
      }
    });

    return issues;
  }

  /**
   * 检查错误处理
   */
  private checkErrorHandling(rule: ReviewRule, code: string, lines: string[]): ReviewIssue[] {
    const issues: ReviewIssue[] = [];

    // 检测异步调用但没有 try-catch
    const asyncCallPattern = /await\s+\w+\.\w+\(/g;
    const hasTryCatch = /try\s*\{[\s\S]*?\}\s*catch/i.test(code);

    lines.forEach((line, index) => {
      if (asyncCallPattern.test(line) && !hasTryCatch) {
        issues.push({
          id: `${rule.id}-${index}`,
          category: rule.category,
          severity: rule.severity,
          title: rule.name,
          description: '异步操作缺少错误处理',
          line: index + 1,
          rule: rule.id,
          codeSnippet: line.trim(),
          suggestedFix: '添加 try-catch 块处理可能的错误',
        });
      }
    });

    return issues;
  }

  /**
   * 使用模式匹配检查
   */
  private checkByPatterns(rule: ReviewRule, code: string, lines: string[]): ReviewIssue[] {
    const issues: ReviewIssue[] = [];
    const patterns = rule.config?.patterns || [];

    lines.forEach((line, index) => {
      patterns.forEach((pattern: RegExp) => {
        const match = line.match(pattern);
        if (match) {
          issues.push({
            id: `${rule.id}-${index}`,
            category: rule.category,
            severity: rule.severity,
            title: rule.name,
            description: `检测到规则: ${rule.name}`,
            line: index + 1,
            column: line.indexOf(match[0]) + 1,
            rule: rule.id,
            codeSnippet: line.trim(),
            suggestedFix: '请参考最佳实践进行改进',
          });
        }
      });
    });

    return issues;
  }

  /**
   * 计算代码指标
   */
  private calculateMetrics(code: string, lines: string[], issues: ReviewIssue[]): CodeMetrics {
    const linesOfCode = lines.filter(line => line.trim().length > 0).length;

    // 计算复杂度（简化版）
    const complexity = this.calculateComplexity(code);

    // 可维护性指数（简化计算）
    const maintainabilityIndex = this.calculateMaintainabilityIndex(linesOfCode, complexity, issues);

    // 技术债务（基于问题数量和严重程度）
    const technicalDebt = this.calculateTechnicalDebt(issues);

    return {
      linesOfCode,
      complexity,
      maintainabilityIndex,
      technicalDebt,
    };
  }

  /**
   * 计算复杂度
   */
  private calculateComplexity(code: string): number {
    let complexity = 1; // 基础复杂度

    // 控制流语句增加复杂度
    const controlFlow = ['if', 'else', 'for', 'while', 'case', 'catch', '&&', '||'];
    controlFlow.forEach(keyword => {
      const regex = new RegExp(`\\b${keyword}\\b`, 'g');
      const matches = code.match(regex);
      if (matches) {
        complexity += matches.length;
      }
    });

    return complexity;
  }

  /**
   * 计算可维护性指数
   */
  private calculateMaintainabilityIndex(loc: number, complexity: number, issues: ReviewIssue[]): number {
    // 简化的可维护性指数计算
    const volume = loc;
    const difficulty = complexity / 2;
    const effort = volume * difficulty;

    // 根据问题数量降低分数
    const criticalIssues = issues.filter(i => i.severity === 'critical').length;
    const highIssues = issues.filter(i => i.severity === 'high').length;
    const penalty = criticalIssues * 20 + highIssues * 10;

    const rawIndex = 171 - 5.2 * Math.log(effort) - 0.23 * complexity - 16.2 * Math.log(loc);
    const adjustedIndex = Math.max(0, rawIndex - penalty);

    return Math.min(100, Math.round(adjustedIndex));
  }

  /**
   * 计算技术债务
   */
  private calculateTechnicalDebt(issues: ReviewIssue[]): number {
    const weights = {
      critical: 100,
      high: 50,
      medium: 20,
      low: 5,
    };

    return issues.reduce((total, issue) => total + weights[issue.severity], 0);
  }

  /**
   * 计算总体评分
   */
  private calculateScore(issues: ReviewIssue[], metrics: CodeMetrics): number {
    let score = 100;

    // 根据问题严重程度扣分
    issues.forEach(issue => {
      const penalty = {
        critical: 25,
        high: 15,
        medium: 8,
        low: 3,
      };
      score -= penalty[issue.severity];
    });

    // 根据可维护性指数调整
    score = score * (metrics.maintainabilityIndex / 100);

    // 根据复杂度调整
    if (metrics.complexity > 50) {
      score -= 10;
    } else if (metrics.complexity > 30) {
      score -= 5;
    }

    return Math.max(0, Math.min(100, Math.round(score)));
  }

  /**
   * 生成审查摘要
   */
  private generateSummary(score: number, issues: ReviewIssue[], metrics: CodeMetrics): string {
    const criticalCount = issues.filter(i => i.severity === 'critical').length;
    const highCount = issues.filter(i => i.severity === 'high').length;
    const mediumCount = issues.filter(i => i.severity === 'medium').length;
    const lowCount = issues.filter(i => i.severity === 'low').length;

    let summary = `代码审查完成。总体评分: ${score}/100。\n`;
    summary += `发现 ${issues.length} 个问题：`;
    summary += criticalCount > 0 ? ` ${criticalCount} 个严重问题，` : '';
    summary += highCount > 0 ? ` ${highCount} 个高优先级问题，` : '';
    summary += mediumCount > 0 ? ` ${mediumCount} 个中优先级问题，` : '';
    summary += lowCount > 0 ? ` ${lowCount} 个低优先级问题。` : '。';
    summary += `\n代码复杂度: ${metrics.complexity}，可维护性指数: ${metrics.maintainabilityIndex}。`;

    if (score >= 80) {
      summary += '\n代码质量良好！';
    } else if (score >= 60) {
      summary += '\n代码质量一般，建议改进。';
    } else {
      summary += '\n代码质量需要改进，请优先处理高严重性问题。';
    }

    return summary;
  }

  /**
   * 生成优化建议
   */
  private generateSuggestions(code: string, metrics: CodeMetrics, language: string): ReviewSuggestion[] {
    const suggestions: ReviewSuggestion[] = [];

    // 复杂度建议
    if (metrics.complexity > 30) {
      suggestions.push({
        type: 'refactor',
        title: '降低代码复杂度',
        description: '代码复杂度较高，建议拆分函数或提取方法',
        impact: 'high',
      });
    }

    // 现代化建议（语言特定）
    if (language === 'javascript' || language === 'typescript') {
      if (code.includes('var ')) {
        suggestions.push({
          type: 'modernize',
          title: '使用现代变量声明',
          description: '将 var 替换为 let 或 const',
          impact: 'low',
          codeSnippet: 'var x = 10;',
          suggestedCode: 'const x = 10;',
        });
      }

      if (code.includes('function ') && code.includes('=>') === false) {
        suggestions.push({
          type: 'modernize',
          title: '使用箭头函数',
          description: '适当使用箭头函数简化代码',
          impact: 'medium',
        });
      }
    }

    // 性能优化建议
    if (code.includes('for (') && code.includes('.forEach(')) {
      suggestions.push({
        type: 'optimization',
        title: '统一循环风格',
        description: '代码中混用了 for 循环和 forEach，建议统一风格',
        impact: 'low',
      });
    }

    return suggestions;
  }

  /**
   * 扫描安全漏洞
   */
  async scanSecurityVulnerabilities(code: string, language: string, filePath?: string): Promise<SecurityVulnerability[]> {
    const vulnerabilities: SecurityVulnerability[] = [];
    const lines = code.split('\n');

    lines.forEach((line, index) => {
      // 检查常见安全漏洞
      const checks = [
        {
          pattern: /password\s*=\s*['"][\w]+['"]/gi,
          cwe: 'CWE-798',
          title: '硬编码凭据',
          description: '代码中包含硬编码的密码或密钥',
          recommendation: '使用环境变量或密钥管理服务存储凭据',
        },
        {
          pattern: /eval\s*\(/gi,
          cwe: 'CWE-95',
          title: '动态代码执行',
          description: '使用 eval() 函数可能导致代码注入',
          recommendation: '避免使用 eval()，使用替代方案如 JSON.parse()',
        },
        {
          pattern: /innerHTML\s*=/gi,
          cwe: 'CWE-79',
          title: 'XSS 漏洞',
          description: '直接设置 innerHTML 可能导致跨站脚本攻击',
          recommendation: '使用 textContent 或安全的 HTML 消毒库',
        },
      ];

      checks.forEach(check => {
        const match = line.match(check.pattern);
        if (match) {
          vulnerabilities.push({
            id: `vuln-${Date.now()}-${index}`,
            severity: 'high',
            cwe: check.cwe,
            title: check.title,
            description: check.description,
            location: {
              file: filePath || 'unknown',
              line: index + 1,
              column: line.indexOf(match[0]) + 1,
            },
            codeSnippet: line.trim(),
            recommendation: check.recommendation,
            references: [
              'https://cwe.mitre.org/data/definitions/' + check.cwe.split('-')[1],
            ],
          });
        }
      });
    });

    return vulnerabilities;
  }

  /**
   * 获取所有规则
   */
  async getAllRules(): Promise<ReviewRule[]> {
    return Array.from(this.rules.values());
  }

  /**
   * 更新规则配置
   */
  async updateRuleConfig(ruleId: string, config: Partial<ReviewRule>): Promise<void> {
    const rule = this.rules.get(rule(ruleId));
    if (rule) {
      Object.assign(rule, config);
      this.logger.debug(`Updated rule config: ${ruleId}`);
    }
  }
}

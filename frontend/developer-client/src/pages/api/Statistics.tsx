import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../components/Card';
import { Button } from '../../components/Button';
import { useApiStore } from '../../stores/apiStore';
import { formatNumber } from '../../utils';

export const Statistics: React.FC = () => {
  const { statistics, trends, loading, fetchStatistics, fetchTrends } = useApiStore();
  const [period, setPeriod] = useState('week');

  useEffect(() => {
    fetchStatistics(period);
    fetchTrends(period);
  }, [period, fetchStatistics, fetchTrends]);

  const periods = [
    { value: 'today', label: '今日' },
    { value: 'week', label: '本周' },
    { value: 'month', label: '本月' },
    { value: 'year', label: '本年' },
  ];

  if (!statistics) return null;

  const successRate = statistics.totalCalls > 0
    ? ((statistics.successCalls / statistics.totalCalls) * 100).toFixed(2)
    : '0';

  const errorRate = statistics.totalCalls > 0
    ? ((statistics.errorCalls / statistics.totalCalls) * 100).toFixed(2)
    : '0';

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">调用统计</h2>
          <p className="text-muted-foreground">查看API调用数据和趋势</p>
        </div>
        <div className="flex gap-2">
          {periods.map((p) => (
            <Button
              key={p.value}
              variant={period === p.value ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setPeriod(p.value)}
            >
              {p.label}
            </Button>
          ))}
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="pb-3">
            <CardDescription>总调用次数</CardDescription>
            <CardTitle className="text-3xl">{formatNumber(statistics.totalCalls)}</CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardDescription>成功调用</CardDescription>
            <CardTitle className="text-3xl text-green-600">{formatNumber(statistics.successCalls)}</CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardDescription>失败调用</CardDescription>
            <CardTitle className="text-3xl text-red-600">{formatNumber(statistics.errorCalls)}</CardTitle>
          </CardHeader>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardDescription>总成本</CardDescription>
            <CardTitle className="text-3xl">¥{statistics.cost.toFixed(2)}</CardTitle>
          </CardHeader>
        </Card>
      </div>

      {/* Rates */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>成功率</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-green-600">{successRate}%</div>
            <p className="mt-2 text-sm text-muted-foreground">
              成功: {statistics.successCalls} / 总计: {statistics.totalCalls}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>错误率</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold text-red-600">{errorRate}%</div>
            <p className="mt-2 text-sm text-muted-foreground">
              失败: {statistics.errorCalls} / 总计: {statistics.totalCalls}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <Card>
        <CardHeader>
          <CardTitle>调用趋势</CardTitle>
          <CardDescription>API调用次数和成本变化</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="calls" stroke="#0ea5e9" name="调用次数" />
              <Line yAxisId="right" type="monotone" dataKey="cost" stroke="#a21caf" name="成本(元)" />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>错误率趋势</CardTitle>
          <CardDescription>API错误率变化</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="errorRate" fill="#ef4444" name="错误率(%)" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
};

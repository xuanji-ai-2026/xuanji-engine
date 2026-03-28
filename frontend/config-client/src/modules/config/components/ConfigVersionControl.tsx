import React, { useEffect, useState } from 'react'
import { Button } from '@/components/Button'
import { Card } from '@/components/Card'
import { Badge } from '@/components/Badge'
import { cn } from '@/utils'
import { GitBranch, Eye, RotateCcw, CheckCircle } from 'lucide-react'
import type { ConfigVersion, ConfigDiff } from '@/types'

export const ConfigVersionControl: React.FC = () => {
  const [configId, setConfigId] = useState('')
  const [versions, setVersions] = useState<ConfigVersion[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedVersion1, setSelectedVersion1] = useState<ConfigVersion | null>(null)
  const [selectedVersion2, setSelectedVersion2] = useState<ConfigVersion | null>(null)
  const [showDiff, setShowDiff] = useState(false)
  const [diffs, setDiffs] = useState<ConfigDiff[]>([])

  useEffect(() => {
    if (configId) {
      fetchVersions()
    }
  }, [configId])

  const fetchVersions = async () => {
    if (!configId) return
    setLoading(true)
    try {
      const response = await fetch(`/api/config-requests/${configId}/versions`)
      const data: ConfigVersion[] = await response.json()
      setVersions(data)
      if (data.length > 0) {
        setSelectedVersion1(data[0])
        setSelectedVersion2(data.length > 1 ? data[1] : data[0])
      }
    } catch (error) {
      console.error('Failed to fetch versions:', error)
    } finally {
      setLoading(false)
    }
  }

  const compareVersions = () => {
    if (!selectedVersion1 || !selectedVersion2) return

    const diffs: ConfigDiff[] = []
    const data1 = selectedVersion1.configData
    const data2 = selectedVersion2.configData

    const allKeys = new Set([...Object.keys(data1), ...Object.keys(data2)])

    allKeys.forEach((key) => {
      const val1 = data1[key]
      const val2 = data2[key]

      if (!(key in data1)) {
        diffs.push({ field: key, oldValue: undefined, newValue: val2, changeType: 'added' })
      } else if (!(key in data2)) {
        diffs.push({ field: key, oldValue: val1, newValue: undefined, changeType: 'removed' })
      } else if (JSON.stringify(val1) !== JSON.stringify(val2)) {
        diffs.push({ field: key, oldValue: val1, newValue: val2, changeType: 'modified' })
      }
    })

    setDiffs(diffs)
    setShowDiff(true)
  }

  const handleRollback = async (version: ConfigVersion) => {
    if (!confirm(`确定要回滚到版本 ${version.version} 吗？`)) return
    try {
      const response = await fetch(`/api/config-requests/${configId}/rollback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ versionId: version.id }),
      })
      if (response.ok) {
        alert('回滚成功')
        fetchVersions()
      }
    } catch (error) {
      console.error('Failed to rollback:', error)
      alert('回滚失败')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">配置版本控制</h1>
        <p className="mt-1 text-sm text-gray-600">
          查看和比较配置的不同版本
        </p>
      </div>

      <Card className="p-6">
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            配置ID
          </label>
          <input
            type="text"
            value={configId}
            onChange={(e) => setConfigId(e.target.value)}
            placeholder="输入配置请求ID"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-xuanji-500"
          />
        </div>

        {loading ? (
          <div className="py-12 text-center text-gray-500">加载中...</div>
        ) : versions.length === 0 ? (
          <div className="py-12 text-center text-gray-500">
            {configId ? '该配置没有版本记录' : '请输入配置ID'}
          </div>
        ) : (
          <div className="space-y-4">
            {/* Version List */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                版本历史
              </h3>
              <div className="space-y-2">
                {versions.map((version, index) => (
                  <div
                    key={version.id}
                    className={cn(
                      'flex items-center justify-between p-4 border rounded-lg',
                      selectedVersion1?.id === version.id || selectedVersion2?.id === version.id
                        ? 'border-xuanji-500 bg-xuanji-50'
                        : 'border-gray-200 hover:border-gray-300'
                    )}
                  >
                    <div className="flex items-center gap-3">
                      <div className="p-2 bg-gray-100 rounded-lg">
                        <GitBranch className="w-5 h-5 text-gray-600" />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-medium text-gray-900">
                            版本 {version.version}
                          </span>
                          {index === 0 && (
                            <Badge variant="success" size="sm">
                              当前
                            </Badge>
                          )}
                        </div>
                        <div className="text-sm text-gray-600">
                          {version.changeLog}
                        </div>
                        <div className="text-xs text-gray-500 mt-1">
                          {new Date(version.createdAt).toLocaleString('zh-CN')} | 创建者: {version.createdBy}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant={selectedVersion1?.id === version.id ? 'primary' : 'ghost'}
                        size="sm"
                        onClick={() => setSelectedVersion1(version)}
                      >
                        {selectedVersion1?.id === version.id ? '版本 A' : '选为 A'}
                      </Button>
                      <Button
                        variant={selectedVersion2?.id === version.id ? 'primary' : 'ghost'}
                        size="sm"
                        onClick={() => setSelectedVersion2(version)}
                      >
                        {selectedVersion2?.id === version.id ? '版本 B' : '选为 B'}
                      </Button>
                      {index > 0 && (
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleRollback(version)}
                          icon={<RotateCcw className="w-4 h-4" />}
                        >
                          回滚
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Compare Button */}
            {selectedVersion1 && selectedVersion2 && (
              <div className="flex justify-center">
                <Button
                  variant="primary"
                  onClick={compareVersions}
                  disabled={selectedVersion1.id === selectedVersion2.id}
                  icon={<Eye className="w-4 h-4" />}
                >
                  对比版本
                </Button>
              </div>
            )}

            {/* Diff View */}
            {showDiff && diffs.length > 0 && (
              <div className="mt-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  差异对比 ({selectedVersion1?.version} → {selectedVersion2?.version})
                </h3>
                <div className="border border-gray-200 rounded-lg overflow-hidden">
                  <table className="w-full">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                          字段
                        </th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                          类型
                        </th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                          旧值
                        </th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                          新值
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {diffs.map((diff, index) => (
                        <tr key={index} className="hover:bg-gray-50">
                          <td className="px-4 py-3 text-sm font-medium text-gray-900">
                            {diff.field}
                          </td>
                          <td className="px-4 py-3">
                            <Badge
                              variant={
                                diff.changeType === 'added'
                                  ? 'success'
                                  : diff.changeType === 'removed'
                                    ? 'danger'
                                    : 'warning'
                              }
                              size="sm"
                            >
                              {diff.changeType}
                            </Badge>
                          </td>
                          <td className="px-4 py-3">
                            <code className="text-sm text-gray-700 bg-gray-100 px-2 py-1 rounded">
                              {diff.oldValue !== undefined
                                ? JSON.stringify(diff.oldValue)
                                : '-'}
                            </code>
                          </td>
                          <td className="px-4 py-3">
                            <code className="text-sm text-gray-700 bg-gray-100 px-2 py-1 rounded">
                              {diff.newValue !== undefined
                                ? JSON.stringify(diff.newValue)
                                : '-'}
                            </code>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {showDiff && diffs.length === 0 && (
              <div className="mt-6 text-center py-8 bg-green-50 rounded-lg">
                <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-3" />
                <p className="text-sm font-medium text-green-700">
                  两个版本完全相同，没有差异
                </p>
              </div>
            )}
          </div>
        )}
      </Card>
    </div>
  )
}

export default ConfigVersionControl

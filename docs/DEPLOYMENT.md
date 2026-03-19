# 玄玑AI数字员工引擎部署文档

**版本**: v2.0
**更新时间**: 2026-03-18

---

## 📋 目录

- [环境要求](#环境要求)
- [快速部署](#快速部署)
- [Kubernetes部署](#kubernetes部署)
- [配置说明](#配置说明)
- [监控配置](#监控配置)
- [故障排查](#故障排查)

---

## 环境要求

### 硬件要求

| 组件 | CPU | 内存 | 存储 |
|------|-----|------|------|
| 最小配置 | 2核 | 4GB | 20GB |
| 推荐配置 | 4核 | 8GB | 50GB |
| 生产配置 | 8核+ | 16GB+ | 100GB+ |

### 软件要求

| 软件 | 版本 |
|------|------|
| Kubernetes | 1.25+ |
| Docker | 20.10+ |
| PostgreSQL | 14+ |
| Redis | 7+ |
| Python | 3.9+ |

---

## 快速部署

### 1. 克隆代码

```bash
git clone https://github.com/xuanji-ai-2026/xuanji-engine.git
cd xuanji-engine
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑.env文件，填入实际配置
```

### 3. 构建Docker镜像

```bash
docker build -t xuanji-ai-2026/xuanji-engine:latest .
```

### 4. 启动服务

```bash
docker-compose up -d
```

### 5. 验证服务

```bash
curl http://localhost:8080/health
```

---

## Kubernetes部署

### 前置条件

1. Kubernetes集群已就绪
2. kubectl已配置
3. Docker Hub已配置

### 部署步骤

#### 1. 创建命名空间

```bash
kubectl create namespace xuanji-engine
```

#### 2. 部署PostgreSQL

```bash
kubectl apply -f k8s/postgres/
```

#### 3. 部署Redis

```bash
kubectl apply -f k8s/redis/
```

#### 4. 部署ConfigMap

```bash
kubectl apply -f k8s/configmap.yaml
```

#### 5. 部署应用

```bash
kubectl apply -f k8s/deployment.yaml
```

#### 6. 部署Service

```bash
kubectl apply -f k8s/service.yaml
```

#### 7. 部署Ingress

```bash
kubectl apply -f k8s/ingress.yaml
```

#### 8. 部署HPA

```bash
kubectl apply -f k8s/hpa.yaml
```

### 验证部署

#### 检查Pod状态

```bash
kubectl get pods -n xuanji-engine
```

#### 检查Service

```bash
kubectl get svc -n xuanji-engine
```

#### 检查HPA

```bash
kubectl get hpa -n xuanji-engine
```

#### 测试访问

```bash
curl https://xuanji-engine.xuanji-ai.com/health
```

---

## 配置说明

### 环境变量

#### 应用配置

```bash
APP_NAME=玄玑AI数字员工引擎
APP_VERSION=2.0
APP_ENVIRONMENT=production
DEBUG=false
```

#### API配置

```bash
API_HOST=0.0.0.0
API_PORT=8080
API_WORKERS=4
```

#### DeepSeek配置

```bash
DEEPSEEK_API_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_API_KEY=your_api_key_here
```

#### 数据库配置

```bash
DB_HOST=postgres
DB_PORT=5432
DB_NAME=xuanji_engine
DB_USER=xuanji
DB_PASSWORD=your_password_here
```

#### Redis配置

```bash
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your_password_here
```

### Kubernetes配置

#### 副本数

```yaml
replicas: 3  # 最小副本数
```

#### 资源限制

```yaml
resources:
  requests:
    memory: "512Mi"
    cpu: "500m"
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

#### HPA配置

```yaml
minReplicas: 3
maxReplicas: 10
metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## 监控配置

### Prometheus配置

#### 访问Prometheus

```bash
kubectl port-forward -n monitoring svc/prometheus 9090:9090
```

#### 查询指标

```promql
# CPU使用率
rate(process_cpu_seconds_total[5m])

# 内存使用率
process_resident_memory_bytes

# 请求速率
rate(http_requests_total[5m])
```

### Grafana配置

#### 访问Grafana

```bash
kubectl port-forward -n monitoring svc/grafana 3000:3000
```

#### 默认账号

```
用户名: admin
密码: 见环境变量GRAFANA_ADMIN_PASSWORD
```

### 日志配置

#### 访问Loki

```bash
kubectl port-forward -n logging svc/loki 3100:3100
```

#### 查询日志

```logql
{app="xuanji-engine", level="error"} |= "错误"
```

---

## 故障排查

### Pod无法启动

#### 检查Pod状态

```bash
kubectl describe pod <pod-name> -n xuanji-engine
```

#### 查看Pod日志

```bash
kubectl logs <pod-name> -n xuanji-engine
```

#### 常见问题

1. **镜像拉取失败**
   - 检查Docker Hub配置
   - 检查镜像名称和标签

2. **配置错误**
   - 检查ConfigMap配置
   - 检查环境变量

3. **资源不足**
   - 检查节点资源
   - 调整资源限制

### 服务无法访问

#### 检查Service

```bash
kubectl get svc -n xuanji-engine
kubectl describe svc <service-name> -n xuanji-engine
```

#### 检查Ingress

```bash
kubectl get ingress -n xuanji-engine
kubectl describe ingress <ingress-name> -n xuanji-engine
```

#### 检查DNS解析

```bash
nslookup xuanji-engine.xuanji-ai.com
```

### 性能问题

#### 检查资源使用

```bash
kubectl top pods -n xuanji-engine
kubectl top nodes
```

#### 检查HPA

```bash
kubectl get hpa -n xuanji-engine
kubectl describe hpa <hpa-name> -n xuanji-engine
```

#### 检查慢查询

```bash
# PostgreSQL慢查询
kubectl exec -it <postgres-pod> -n xuanji-engine -- psql -U xuanji -d xuanji_engine
```

### 数据库连接问题

#### 检查数据库连接

```bash
kubectl exec -it <app-pod> -n xuanji-engine -- psql -h postgres -U xuanji -d xuanji_engine
```

#### 检查连接池

```bash
kubectl exec -it <app-pod> -n xuanji-engine -- env | grep DB_POOL
```

---

## 升级指南

### 滚动更新

```bash
# 更新镜像
kubectl set image deployment/xuanji-engine xuanji-engine=xuanji-ai-2026/xuanji-engine:v2.0.1 -n xuanji-engine

# 查看更新状态
kubectl rollout status deployment/xuanji-engine -n xuanji-engine

# 回滚
kubectl rollout undo deployment/xuanji-engine -n xuanji-engine
```

### 蓝绿部署

1. 部署新版本
2. 切换流量
3. 监控新版本
4. 清理旧版本

---

## 备份恢复

### 备份

```bash
# 备份PostgreSQL
kubectl exec -it <postgres-pod> -n xuanji-engine -- pg_dump -U xuanji xuanji_engine > backup.sql

# 备份ConfigMap
kubectl get configmap xuanji-engine-config -n xuanji-engine -o yaml > configmap-backup.yaml
```

### 恢复

```bash
# 恢复PostgreSQL
kubectl exec -i <postgres-pod> -n xuanji-engine -- psql -U xuanji xuanji_engine < backup.sql

# 恢复ConfigMap
kubectl apply -f configmap-backup.yaml
```

---

## 安全建议

1. **启用TLS**
   - 配置Ingress TLS证书
   - 强制HTTPS

2. **网络隔离**
   - 使用NetworkPolicy
   - 限制Pod间通信

3. **密钥管理**
   - 使用K8s Secret
   - 定期轮换密钥

4. **访问控制**
   - 配置RBAC
   - 最小权限原则

---

**文档版本**: v2.0
**更新时间**: 2026-03-18

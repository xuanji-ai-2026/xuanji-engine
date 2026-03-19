# 玄玑AI数字员工引擎 - 常见问题 (FAQ)

**版本**: v2.0
**更新时间**: 2026-03-18

---

## 📋 目录

- [安装问题](#安装问题)
- [配置问题](#配置问题)
- [使用问题](#使用问题)
- [性能问题](#性能问题)
- [故障排查](#故障排查)

---

## 安装问题

### Q1: 安装依赖时出错？

**问题**: `pip install -r requirements.txt` 失败

**解决方案**:
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者升级pip
pip install --upgrade pip
```

### Q2: 启动服务时端口被占用？

**问题**: `OSError: [Errno 98] Address already in use`

**解决方案**:
```bash
# 查找占用端口的进程
lsof -i :8080

# 杀掉进程
kill -9 <PID>

# 或者修改端口
export API_PORT=8000
```

### Q3: 数据库连接失败？

**问题**: `psycopg2.OperationalError: could not connect to server`

**解决方案**:
1. 检查数据库服务是否启动
2. 检查连接字符串是否正确
3. 检查防火墙设置
4. 检查用户权限

---

## 配置问题

### Q4: 如何配置DeepSeek API？

**问题**: 不清楚如何配置DeepSeek API

**解决方案**:
在`.env`文件中配置：
```bash
DEEPSEEK_API_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_API_KEY=your_api_key_here
```

### Q5: 如何配置飞书机器人？

**问题**: 不清楚如何配置飞书机器人

**解决方案**:
1. 在飞书开放平台创建应用
2. 获取App ID和App Secret
3. 在`.env`文件中配置：
```bash
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
```

### Q6: 如何配置监控和日志？

**问题**: 不清楚如何配置监控和日志

**解决方案**:
1. 部署Prometheus和Grafana
2. 配置Loki日志收集
3. 在`.env`文件中配置：
```bash
METRICS_ENABLED=true
LOG_LEVEL=INFO
```

---

## 使用问题

### Q7: 如何调用API？

**问题**: 不清楚如何调用API

**解决方案**:
```bash
# 健康检查
curl http://localhost:8080/health

# 对话API
curl -X POST http://localhost:8080/api/v2/dialogue/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"message":"你好","user_id":"user123","session_id":"session456"}'
```

### Q8: 如何获取认证Token？

**问题**: 不清楚如何获取Token

**解决方案**:
```bash
curl -X POST http://localhost:8080/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'
```

### Q9: 如何处理并发请求？

**问题**: 并发请求时出现错误

**解决方案**:
- 使用连接池
- 配置合理的超时时间
- 使用异步API
- 配置HPA自动扩展

### Q10: 如何调试对话流程？

**问题**: 不清楚如何调试对话

**解决方案**:
1. 启用调试模式：`DEBUG=true`
2. 查看日志文件
3. 使用对话历史跟踪
4. 使用测试工具验证

---

## 性能问题

### Q11: 响应时间过长？

**问题**: API响应时间>1秒

**解决方案**:
- 检查数据库查询性能
- 使用缓存减少重复计算
- 优化算法复杂度
- 增加资源（CPU、内存）

### Q12: 内存使用过高？

**问题**: 内存占用>1GB

**解决方案**:
- 检查内存泄漏
- 优化数据结构
- 限制缓存大小
- 使用对象池

### Q13. CPU使用过高？

**问题**: CPU占用>80%

**解决方案**:
- 优化算法
- 使用异步操作
- 实现负载均衡
- 增加实例数量

### Q14. 数据库连接池耗尽？

**问题**: `PoolExhaustedError`

**解决方案**:
```python
# 增加连接池大小
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=40

# 或者使用连接池监控
```

---

## 故障排查

### Q15: 服务无法启动？

**问题**: 服务启动失败

**排查步骤**:
1. 检查端口是否被占用
2. 检查依赖是否安装
3. 检查配置文件是否正确
4. 查看错误日志

### Q16: 数据库查询失败？

**问题**: 数据库查询失败

**排查步骤**:
1. 检查数据库连接
2. 检查SQL语句
3. 检查数据表结构
4. 检查用户权限

### Q17: 缓存失效？

**问题**: 缓存无法正常工作

**排查步骤**:
1. 检查Redis服务状态
2. 检查Redis连接配置
3. 检查缓存键是否正确
4. 检查缓存过期时间

### Q18: 消息丢失？

**问题**: 消息队列消息丢失

**排查步骤**:
1. 检查消息队列服务
2. 检查消息持久化
3. 检查消费端状态
4. 检查网络连接

### Q19: 健康检查失败？

**问题**: `/health` 返回错误

**排查步骤**:
1. 检查服务状态
2. 检查依赖服务
3. 检查资源使用
4. 查看日志文件

### Q20: 日志无法输出？

**问题**: 日志无法输出

**排查步骤**:
1. 检查日志配置
2. 检查日志目录权限
3. 检查日志级别
4. 检查磁盘空间

---

## 技术支持

如果以上解决方案无法解决您的问题，请联系技术支持：

- **GitHub Issues**: https://github.com/xuanji-ai-2026/xuanji-engine/issues
- **Email**: support@xuanji-ai.com
- **在线文档**: https://docs.xuanji-ai.com

---

**文档版本**: v2.0
**更新时间**: 2026-03-18

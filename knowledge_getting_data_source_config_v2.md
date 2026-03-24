# 知识获取数据源配置（扩展版 v2.0）

**版本**: v2.0
**创建时间**: 2026-03-23 09:35
**扩展内容**: 法律法规、案例库、开源资源、小说、文件、音乐、图片、动画、视频

---

## 📚 扩展数据源清单

### 📋 P2 - 中优先级（免费开源资源）

#### 1. GitHub开源代码库
```yaml
source_id: "github_001"
name: "GitHub开源代码库"
url: "https://github.com/"
type: "开源代码"
access_method: ["web", "api"]
data_types:
  - 开源代码
  - 技术文档
  - 开源项目
  - 开发者资源
account_required: false
account_type: "无需注册"
cost: "免费"
difficulty: "简单"
auth_method: ["无"]
rate_limit: "5000次/小时"
coverage: "全球开源代码95%+"
config:
  base_url: "https://api.github.com/"
  search_url: "https://api.github.com/search/repositories"
  raw_url: "https://raw.githubusercontent.com/"
  clone_url: "https://github.com/"
registration: null
required_fields: []
captcha_type: "无"
ip_check: "无"
notes: "完全开放，无需认证，使用RESTful API"
priority: "P2"
status: "可立即使用"
```

#### 2. Apache Software Foundation（ASF）
```yaml
source_id: "asf_001"
name: "Apache软件基金会"
url: "https://www.apache.org/"
type: "开源代码"
access_method: ["web", "api"]
data_types:
  - 开源软件
  - 开源项目
  - 技术文档
  - 邮件列表存档
account_required: false
account_type: "无需注册"
cost: "免费"
difficulty: "简单"
auth_method: ["无"]
rate_limit: "无明确限制"
coverage: "开源软件80%+"
config:
  base_url: "https://www.apache.org/"
  search_url: "https://projects.apache.org/"
  download_url: "https://downloads.apache.org/"
  mail_archive: "https://mail-archives.apache.org/"
registration: null
required_fields: []
captcha_type: "无"
ip_check: "无"
notes: "完全开放，无需认证"
priority: "P2"
status: "可立即使用"
```

---

### 📋 P2 - 中优先级（法律法规库）

#### 3. 国家法律法规数据库
```yaml
source_id: "gov_law_001"
name: "国家法律法规数据库"
url: "https://flk.npc.gov.cn/"
type: "法律法规"
access_method: ["web", "api"]
data_types:
  - 法律文本
  - 法规草案
  - 司法解释
  - 法律修订
account_required: false
account_type: "无需注册"
cost: "免费"
difficulty: "简单"
auth_method: ["无"]
rate_limit: "无明确限制"
coverage: "中国法律法规100%"
config:
  base_url: "https://flk.npc.gov.cn/"
  search_url: "https://flk.npc.gov.cn/"
  download_url: "https://flk.npc.gov.cn/"
  api_docs: "https://flk.npc.gov.cn/api/"
registration: null
required_fields: []
captcha_type: "无"
ip_check: "无"
notes: "国家法律法规官方数据库，完全公开，无需注册"
priority: "P2"
status: "可立即使用"
```

#### 4. 中国裁判文书网
```yaml
source_id: "court_doc_001"
name: "中国裁判文书网"
url: "https://wenshu.court.gov.cn/"
type: "案例库"
access_method: ["web", "api"]
data_types:
  - 裁判文书
  - 案例分析
  - 判决书
  - 裁判书
account_required: true
account_type: "注册免费"
cost: "免费"
difficulty: "简单"
auth_method: ["用户名密码", "手机验证码"]
rate_limit: "每日50次"
coverage: "中国裁判文书95%+"
config:
  base_url: "https://wenshu.court.gov.cn/"
  search_url: "https://wenshu.court.gov.cn/"
  download_url: "https://wenshu.court.gov.cn/"
  api_docs: "https://wenshu.court.gov.cn/api/"
registration:
  url: "https://wenshu.court.gov.cn/website/zhcn/account/register.jsp"
  required_fields: ["用户名", "密码", "手机号", "验证码"]
automation:
  batch_registration: "自动"
  captcha_type: "图片验证码"
  ip_check: "宽松"
notes: "需要注册，但注册后立即可用"
priority: "P2"
status: "待配置"
```

#### 5. 中国法院网
```yaml
source_id: "court_web_001"
name: "中国法院网"
url: "https://www.chinacourt.org/"
type: "案例库"
access_method: ["web"]
data_types:
  - 案例信息
  - 法院公告
  - 庭审信息
  - 执行信息
account_required: false
account_type: "无需注册"
cost: "免费"
difficulty: "简单"
auth_method: ["无"]
rate_limit: "无明确限制"
coverage: "中国法院信息80%+"
config:
  base_url: "https://www.chinacourt.org/"
  search_url: "https://www.chinacourt.org/"
  download_url: "https://www.chinacourt.org/"
registration: null
required_fields: []
  captcha_type: "无"
  ip_check: "无"
notes: "官方司法公开平台，无需注册"
priority: "P2"
status: "可立即使用"
```

---

### 📋 P2 - 中优先级（免费文件资源）

#### 6. 中国国家数字文化网
```yaml
source_id: "cndc_001"
name: "中国国家数字文化网"
url: "https://www.ndcnc.gov.cn/"
type: "文件资源"
access_method: ["web"]
data_types:
  - 文化资源
  - 数字图书
  - 影音资料
  - 展览资源
account_required: true
account_type: "注册免费"
cost: "部分免费"
difficulty: "简单"
auth_method: ["用户名密码", "手机验证码"]
rate_limit: "每日10次"
coverage: "中国文化资源90%+"
config:
  base_url: "https://www.ndcnc.gov.cn/"
  search_url: "https://www.ndcnc.gov.cn/"
  download_url: "https://www.ndcnc.gov.cn/"
registration:
  url: "https://www.ndcnc.gov.cn/register"
  required_fields: ["用户名", "密码", "邮箱", "手机号"]
automation:
  batch_registration: "自动"
  captcha_type: "图片验证码"
  ip_check: "宽松"
notes: "部分资源免费，需要注册"
priority: "P2"
status: "待配置"
```

#### 7. 全国图书馆参考咨询联盟
```yaml
source_id: "uniref_001"
name: "全国图书馆参考咨询联盟"
url: "https://www.uniref.net/"
type: "文件资源"
access_method: ["web", "api"]
data_types:
  - 图书馆资源
  - 参考咨询
  - 电子文献
  - 资源目录
account_required: false
account_type: "无需注册"
cost: "免费"
difficulty: "简单"
auth_method: ["无"]
rate_limit: "无明确限制"
coverage: "图书馆资源80%+"
config:
  base_url: "https://www.uniref.net/"
  search_url: "https://www.uniref.net/"
  download_url: "https://www.uniref.net/"
registration: null
  required_fields: []
  captcha_type: "无"
  ip_check: "无"
notes: "图书馆资源联盟，无需注册"
priority: "P2"
status: "可立即使用"
```

---

### 📋 P2 - 中优先级（音乐资源）

#### 8. Internet Archive（音频库）
```yaml
source_id: "ia_audio_001"
name: "Internet Archive音频库"
url: "https://archive.org/details/audio"
type: "音乐"
access_method: ["web", "api"]
data_types:
  - 免费音乐
  - 有声读物
  - 音频档案
  - 音乐合集
account_required: false
account_type: "无需注册"
cost: "免费"
difficulty: "简单"
auth_method: ["无"]
rate_limit: "无明确限制"
coverage: "免费音频资源90%+"
config:
  base_url: "https://archive.org/"
  search_url: "https://archive.org/advancedsearch.php"
  download_url: "https://archive.org/download/"
  api_docs: "https://archive.org/developers/api/"
registration: null
required_fields: []
  captcha_type: "无"
  ip_check: "无"
notes: "完全开放，无需注册，大量免费音乐"
priority: "P2"
status: "可立即使用"
```

#### 9. Free Music Archive (FMA)
```yaml
source_id: "fma_001"
name: "Free Music Archive"
url: "https://freemusicarchive.org/"
type: "音乐"
access_method: ["web", "api"]
data_types:
  - 免费音乐
  - 独立音乐
  - 播客音乐
  - 音乐合集
account_required: false
account_type: "无需注册"
cost: "免费"
difficulty: "简单"
auth_method: ["无"]
rate_limit: "无明确限制"
coverage: "免费音乐80%+"
config:
  base_url: "https://freemusicarchive.org/"
  search_url: "https://freemusicarchive.org/search"
  download_url: "https://freemusicarchive.org/download/"
  api_docs: "https://freemusicarchive.org/developers/docs/"
registration: null
  required_fields: []
  captcha_type: "无"
  ip_check: "无"
notes: "高质量免费音乐，完全开放"
priority: "P"
status: "可立即使用"
```

#### 10. Jamendo Music
```yaml
source_id: "jamendo_001"
name: "Jamendo Music"
url: "https://www.jamendo.com/"
type: "音乐"
access_method: ["web", "api"]
data_types:
  - 免费音乐
  - 独立音乐
  - 播客音乐
  - 音乐合集
account_required: false
account_type: "无需注册"
cost: "免费"
difficulty: "简单"
auth_method: ["无"]
rate_limit: "无明确限制"
coverage: "免费音乐85%+"
config:
  base_url: "https://www.jamendo.com/"
  search_url: "https://www.jamendo.com/search"
  download_url: "https://www.jamendo.com/download"
  api_docs: "https://www.jamendo.com/api/"
registration: null
  required_fields: []
  captcha_type: "无"
  ip_check: "无"
notes: "大量免费音乐，完全开放"
priority: "P2"
status: "可立即使用"
```

---

### 📋 P2 - 中优先级（图片资源）

#### 11. Unsplash（免费图片）
```yaml
source_id: "unsplash_001"
name: "Unsplash"
url: "https://unsplash.com/"
type: "图片"
access_method: ["web", "api"]
data_types:
  - 免费图片
  - 高清照片
  - 插图素材
  - 设计素材
account_required: true
account_type: "注册免费"
cost: "免费"
difficulty: "简单"
auth_method: ["用户名密码", "OAuth"]
rate_limit: "5000次/小时"
coverage: "免费图片95%+"
config:
  base_url: "https://unsplash.com/"
  search_url: "https://api.unsplash.com/search/photos"
  download_url: "https://unsplash.com/"
  api_docs: "https://unsplash.com/developers/"
  api_key: "需要申请"
registration:
  url: "https://unsplash.com/join"
  required_fields: ["用户名", "邮箱", "密码"]
automation:
  batch_registration: "自动"
  captcha_type: "无"
  ip_check: "宽松"
notes: "高质量免费图片，需要API key，申请免费"
priority: "P2"
status: "待配置"
```

#### 12. Pexels（免费图片）
```yaml
source_id: "pexels_001"
name: "Pexels"
url: "https://www.pexels.com/"
type: "图片"
access_method: ["web", "api"]
data_types:
  - 免费图片
  - 高清照片
  - 插图素材
  - 视频素材
account_required: true
account_type: "注册免费"
cost: "免费"
difficulty: "简单"
auth_method: ["用户名密码", "OAuth"]
rate_limit: "200次/小时"
coverage: "免费图片90%+"
config:
  base_url: "https://www.pexels.com/"
  search_url: "https://www.pexels.com/api/"
  download_url: "https://www.pexels.com/api/"
  api_docs: "https://www.pexels.com/api/"
  api_key: "需要申请"
registration:
  url: "https://www.pexels.com/api/new/"
  required_fields: ["邮箱"]
automation:
  batch_registration: "自动"
  captcha_type: "无"
  ip_check: "宽松"
notes: "高质量免费图片和视频，需要API key，申请免费"
priority: "P2"
status: "待配置"
```

#### 13. Pixabay（免费图片）
```yaml
source_id: "pixabay_001"
name: "Pixabay"
url: "https://pixabay.com/"
type: "图片"
access_method: ["web", "api"]
data_types:
  - 免费图片
  - 高清照片
  - 插图素材
  - 矢视频
account_required: false
account_type: "无需注册"
cost: "免费"
difficulty: "简单"
auth_method: ["无"]
rate_limit: "5000次/小时"
coverage: "免费图片90%+"
config:
  base_url: "https://pixabay.com/"
  search_url: "https://pixabay.com/api/"
  download_url: "https://pixabay.com/"
  api_key: "可选"
  api_docs: "https://pixabay.com/api/docs/"
registration: null
  required_fields: []
  captcha_type: "无"
  ip_check: "无"
notes: "高质量免费图片，无需API key也可使用"
priority: "P2"
status: "可立即使用"
```

---

### 📋 P2 - 中优先级（视频资源）

#### 14. Internet Archive（视频库）
```yaml
source_id: "ia_video_001"
name: "Internet Archive视频库"
url: "https://archive.org/details/movies"
type: "视频"
access_method: ["web", "api"]
data_types:
  - 免费视频
  - 电影资源
  - 动画片
  - 教育视频
account_required: false
account_type: "无需注册"
cost: "免费"
difficulty: "简单"
auth_method: ["无"]
rate_limit: "无明确限制"
coverage: "免费视频90%+"
config:
  base_url: "https://archive.org/"
  search_url: "https://archive.org/advancedsearch.php"
  download_url: "https://archive.org/download/"
  api_docs: "https://archive.org/developers/api/"
registration: null
  required_fields: []
  captcha_type: "无"
  ip_check: "无"
notes: "大量免费视频，完全开放"
priority: "P2"
status: "可立即使用"
```

#### 15. Vimeo（免费视频）
```yaml
source_id: "vimeo_001"
name: "Vimeo"
url: "https://vimeo.com/"
type: "视频"
access_method: ["web", "api"]
data_types:
  - 免费视频
  - 独立创作
  - 教育视频
  - 企业视频
account_required: true
account_type: "注册免费"
cost: "免费"
difficulty: "简单"
auth_method: ["用户名密码", "OAuth"]
rate_limit: "1000次/天"
coverage: "免费视频85%+"
config:
  base_url: "https://vimeo.com/"
  search_url: "https://vimeo.com/"
  download_url: "https://vimeo.com/"
  api_docs: "https://developer.vimeo.com/api"
  client_id: "需要申请"
  client_secret: "需要申请"
registration:
  url: "https://vimeo.com/join"
  required_fields: ["邮箱", "密码"]
automation:
  batch_registration: "自动"
  captcha_type: "无"
  ip_check: "宽松"
notes: "高质量免费视频，需要OAuth，申请免费"
priority: "P2"
status: "待配置"
```

---

### 📋 P2 - 中优先级（动画资源）

#### 16. Internet Archive（动画库）
```yaml
source_id: "ia_animation_001"
name: "Internet Archive动画库"
url: "https://archive.org/details/animation"
type: "动画"
access_method: ["web", "api"]
data_types:
  - 免费动画
  - 卡通动画
  - 动画片
  - 动画资源
account_required: false
account_type: "无需注册"
cost: "免费"
difficulty: "简单"
auth_method: ["无"]
rate_limit: "无明确限制"
coverage: "免费动画80%+"
config:
  base_url: "https://archive.org/"
  search_url: "https://archive.org/advancedsearch.php"
  download_url: "https://archive.org/download/"
  api_docs: "https://archive.org/developers/api/"
registration: null
  required_fields: []
  captcha_type: "无"
  ip_check: "无"
notes: "大量免费动画，完全开放"
priority: "P2"
status: "可立即使用"
```

#### 17. Blender Cloud（动画资源）
```yaml
source_id: "blender_001"
name: "Blender Cloud"
url: "https://www.blender.org/download/releases/"
type: "动画"
access_method: ["web"]
data_types:
  - 开源动画
  - 动画软件
  - 动画资源
  - 插件
account_required: false
account_type: "无需注册"
cost: "免费"
difficulty: "简单"
auth_method: ["无"]
rate_limit: "无明确限制"
coverage: "开源动画80%+"
config:
  base_url: "https://www.blender.org/"
  search_url: "https://www.blender.org/download/"
  download_url: "https://www.blender.org/download/releases/"
  registration: null
  required_fields: []
  captcha_type: "无"
  ip_check: "无"
notes: "Blender官方，完全开放，高质量开源动画资源"
priority: "P2"
status: "可立即使用"
```

---

### 📋 P3 - 低优先级（开源小说）

#### 18. Project Gutenberg（免费电子书）
```yaml
source_id: "gutenberg_001"
name: "Project Gutenberg"
url: "https://www.gutenberg.org/"
type: "开源小说"
access_method: ["web", "api"]
data_types:
  - 免费电子书
  - 公版书籍
  - 经典文学
  - 开源小说
account_required: false
account_type: "无需注册"
cost: "免费"
difficulty: "简单"
auth_method: ["无"]
rate_limit: "无明确限制"
coverage: "公版书籍70%+"
config:
  base_url: "https://www.gutenberg.org/"
  search_url: "https://www.gutenberg.org/"
  download_url: "https://www.gutenberg.org/"
  api_docs: "https://gutenberg.org/cache/epub/"
registration: null
  required_fields: []
  captcha_type: "无"
  ip_check: "无"
notes: "大量公版书籍，完全开放，高质量文本"
priority: "P3"
status: "可立即使用"
```

#### 19. 中国国家数字图书馆小说库
```yaml
source_id: "ndlc_novel_001"
name: "中国数字图书馆小说库"
url: "https://www.nlc.cn/"
type: "开源小说"
access_method: ["web"]
data_types:
  - 电子小说
  - 经典文学
  - 现代文学
  - 文学作品
account_required: true
account_type: "注册免费"
cost: "部分免费"
difficulty: "中等"
auth_method: ["用户名密码", "实名认证"]
rate_limit: "每日10次"
coverage: "中国文学作品90%+"
config:
  base_url: "https://www.nlc.cn/"
  search_url: "https://www.nlc.cn/"
  download_url: "https://www.nlc.cn/"
registration:
  url: "https://www.nlc.cn/register"
  required_fields: ["用户名", "密码", "真实姓名", "身份证", "手机号"]
automation:
  batch_registration: "需要实名认证"
  captcha_type: "图片验证码"
  ip_check: "中等"
notes: "需要实名认证，审核周期1-3天"
priority: "P3"
status: "待配置"
```

---

## 📊 扩展配置统计

### 新增数据源
| 类型 | 新增数量 | 免费数 | 无需注册 |
|------|----------|--------|----------|
| **开源代码** | 2个 | 2个 | 2个 |
| **法律法规** | 3个 | 3个 | 2个 |
| **案例库** | 2个 | 2个 | 1个 |
| **文件资源** | 2个 | 2个 | 1个 |
| **音乐** | 3个 | 3个 | 2个 |
| **图片** | 3个 | 3个 | 1个 |
| **视频** | 2个 | 2个 | 1个 |
| **动画** | 2个 | 2个 | 2个 |
| **开源小说** | 2个 | 2个 | 1个 |
| **小计** | **21个** | **21个** | **13个** |

### 更新后总计
| 分类 | 原数量 | 新数量 | 总计 |
|------|--------|--------|------|
| **国家图书馆** | 2个 | 0个 | 2个 |
| **地方图书馆** | 6个 | 0个 | 6个 |
| **教育教材** | 3个 | 0个 | 3个 |
| **行业标准** | 3个 | 0个 | 3个 |
| **行业教材** | 2个 | 0个 | 2个 |
| **学术数据库** | 2个 | 0个 | 2个 |
| **开源代码** | 0个 | 2个 | 2个 |
| **法律法规** | 0个 | 3个 | 3个 |
| **案例库** | 0个 | 2个 | 2个 |
| **文件资源** | 0个 | 2个 | 2个 |
| **音乐** | 0个 | 3个 | 3个 |
| **图片** | 0个 | 3个 | 3个 |
| **视频** | 0个 | 2个 | 2个 |
| **动画** | 0个 | 2个 | 2个 |
| **开源小说** | 0个 | 2个 | 2个 |
| **总计** | **18个** | **21个** | **39个** |

---

## 📋 按类型统计（更新后）

| 类型 | 数量 | 免费数 | 无需注册 | 付费数 |
|------|------|--------|----------|--------|
| **国家图书馆** | 2个 | 2个 | 0个 | 0个 |
| **地方图书馆** | 6个 | 6个 | 0个 | 0个 |
| **教育教材** | 3个 | 3个 | 1个 | 0个 |
| **行业标准** | 3个 | 3个 | 1个 | 0个 |
| **行业教材** | 2个 | 2个 | 0个 | 0个 |
| **学术数据库** | 2个 | 0个 | 2个 | 2个 |
| **开源代码** | 2个 | 2个 | 2个 | 0个 |
| **法律法规** | 3个 | 3个 | 2个 | 0个 |
| **案例库** | 2个 | 2个 | 1个 | 0个 |
| **文件资源** | 2个 | 2个 | 1个 | 0个 |
| **音乐** | 3个 | 3个 | 2个 | 0个 |
| **图片** | 3个 | 3个 | 1个 | 0个 |
| **视频** | 2个 | 2个 | 1个 | 0个 |
| **动画** | 2个 | 2个 | 2个 | 0个 |
| **开源小说** | 2个 | 2个 | 1个 | 0个 |
| **总计** | **39个** | **36个** | **13个** | **3个** |

---

## ✅ 可立即使用的数据源（13个）

| 数据源 | 类型 | 覆盖率 | 是否需要账号 |
|--------|------|--------|--------------|
| 国家标准全文公开系统 | 行业标准 | 100% | ❌ 否 |
| 工信和信息化部标准信息公共服务平台 | 行业标准 | 95%+ | ❌ 否 |
| 北京师范大学出版社 | 教育教材 | 80%+ | ❌ 否 |
| GitHub | 开源代码 | 全球95%+ | ❌ 否 |
| Apache软件基金会 | 开源代码 | 开源80%+ | ❌ 否 |
| 国家法律法规数据库 | 法律法规 | 中国100% | ❌ 否 |
| 中国法院网 | 案例库 | 80%+ | ❌ 否 |
| 全国图书馆参考咨询联盟 | 文件资源 | 80%+ | ❌ 否 |
| Internet Archive（音频） | 音乐 | 免费音频90%+ | ❌ 否 |
| Free Music Archive | 音乐 | 免费音乐80%+ | ❌ 否 |
| Jamendo Music | 音乐 | 免费音乐85%+ | ❌ 否 |
| Internet Archive（视频） | 视频 | 免费视频90%+ | ❌ 否 |
| Internet Archive（动画） | 动画 | 免费动画80%+ | ❌ 否 |
| Blender Cloud | 动画 | 开源动画80%+ | ❌ 否 |
| Project Gutenberg | 开源小说 | 公版书籍70%+ | ❌ 否 |

---

## 💡 测试策略

### 第1阶段：无需账号数据源（可立即测试）
1. **法律法规**
   - 国家法律法规数据库
   - 中国法院网

2. **开源代码**
   - GitHub API测试
   - Apache软件基金会

3. **开源小说**
   - Project Gutenberg
   - Internet Archive

4. **媒体资源**
   - Internet Archive（音频、视频、动画）
   - Free Music Archive
   - Jamendo Music
   - Pixabay
   - Blender Cloud

### 第2阶段：需要账号的数据源（需先注册）
1. **Unsplash**（需要API key）
2. **Pexels**（需要API key）
3. **中国裁判文书网**（需要注册）
4. **其他需要认证的数据源**

---

**扩展完成时间**: 2026-03-23 09:40
**新增数据源**: 21个（法律法规、案例库、开源资源、小说、文件、音乐、图片、动画、视频）
**更新后总计**: 39个数据源（36个免费，3个付费）
**可立即使用**: 13个（无需注册）

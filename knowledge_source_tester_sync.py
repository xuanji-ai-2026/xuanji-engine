#!/usr/bin/env python3
"""
知识获取同步测试工具（简化版）
"""

import requests
from datetime import datetime

def test_sync():
    """同步测试数据源"""
    print("=" * 80)
    print("🧪 知识获取能力测试（同步版）")
    print("=" * 80)
    
    test_sources = [
        {
            "name": "国家法律法规数据库",
            "url": "https://flk.npc.gov.cn/",
            "type": "法律法规"
        },
        {
            "name": "中国法院网",
            "url": "https://www.chinacourt.org/",
            "type": "案例库"
        },
        {
            "name": "GitHub API",
            "url": "https://api.github.com/",
            "type": "开源代码"
        },
        {
            "name": "Project Gutenberg",
            "url": "https://www.gutenberg.org/",
            "type": "开源小说"
        },
        {
            "name": "Internet Archive - 动画",
            "url": "https://archive.org/details/animation",
            "type": "动画"
        },
        {
            "name": "Pixabay",
            "url": "https://pixabay.com/",
            "type": "图片"
        }
    ]
    
    results = []
    
    for source in test_sources:
        print(f"\n🔍 测试: {source['name']} ({source['type']})")
        print(f"   URL: {source['url']}")
        
        try:
            start = datetime.now()
            response = response = requests.get(source['url'], timeout=10)
            elapsed = (datetime.now() - start).total_seconds()
            
            status_code = response.status_code
            content_length = len(response.text)
            
            if status_code == 200:
                print(f"   ✅ 成功: {status_code} ({content_length}字节, {elapsed:.2f}秒)")
                print(f"   📝 预览: {response.text[:150]}")
                
                results.append({
                    "name": source['name'],
                    "type": source['type'],
                    "url": source['url'],
                    "status_code": status_code,
                    "content_length": content_length,
                    "elapsed": elapsed,
                    "success": True
                })
            else:
                print(f"   ❌ 失败: {status_code}")
                results.append({
                    "name": source['name'],
                    "type": source['type'],
                    "url": source['url'],
                    "status_code": status_code,
                    "content_length": 0,
                    "elapsed": elapsed,
                    "success": False,
                    "error": f"HTTP {status_code}"
                })
        
        except requests.exceptions.Timeout:
            print(f"   ❌ 超时")
            results.append({
                "name": source['name'],
                "type": source['type'],
                "url": source['url'],
                "status_code": None,
                "content_length": 0,
                "elapsed": 10.0,
                "success": False,
                "error": "超时"
            })
        
        except Exception as e:
            print(f"   ❌ 异常: {e}")
            results.append({
                "name": source['name'],
                "type": source['type'],
                "url": source['url'],
                "status_code": None,
                "content_length": 0,
                "elapsed": 0.0,
                "success": False,
                "error": str(e)
            })
    
    # 测试下载功能
    print("\n📋 测试下载功能")
    print("-" * 80)
    
    # 下载一张图片
    print("\n🔍 下载测试1: Pixabay图片")
    try:
        start = datetime.now()
        response = response = requests.get(
            "https://cdn.pixabay.com/photo/2022/01/20/tree-branch-snow-1964308_1280.jpg",
            timeout=30
        )
        elapsed = (datetime.now() - start).total_seconds()
        
        if response.status_code == 200:
            file_size = len(response.content)
            with open('/tmp/test_pixabay.jpg', 'wb') as f:
                f.write(response.content)
            print(f"   ✅ 下载成功: {file_size}字节 -> /tmp/test_pixabay.jpg")
            print(f"   耗时: {elapsed:.2f}秒")
            results.append({
                "name": "Pixabay图片下载",
                "type": "下载",
                "success": True,
                "file_size": file_size,
                "elapsed": elapsed
            })
        else:
            print(f"   ❌ 下载失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    # 搜索测试
    print("\n🔍 测试搜索功能: GitHub API")
    try:
        start = datetime.now()
        response = requests.get(
            "https://api.github.com/search/repositories?q=language:python&sort=stars",
            timeout=10
        )
        elapsed = (datetime.now() - start).total_seconds()
        
        if response.status_code == 200:
            data = response.json()
            repo_count = data.get("total_count", 0)
            print(f"   ✅ 搜索成功: 找到 {repo_count}个Python项目")
            print(f"   耗时: {elapsed:.2f}秒")
            if repo_count > 0:
                print(f"   📝 示例: {data.get('items', [{}])[:1][0]['name']}")
            results.append({
                "name": "GitHub搜索",
                "type": "搜索",
                "success": True,
                "repo_count": repo_count,
                "elapsed": elapsed
            })
        else:
            print(f"   ❌ 搜索失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    # 测试法律法规下载
    print("\n🔍 测试下载功能: 法律法规")
    try:
        start = datetime.now()
        response = response = requests.get(
            "https://flk.npc.gov.cn/detail2?MzAxNzAwODUyMzAwMDAwNjAwMDAwNw==&zZmYyNzAwN2RkYTZjNjAwMDAwOA==&zZmYxODAwNzAwMDAwNjAwMDAwNw==&zZmYxNjAwNzAwMDAwNjAwMDAwNQ==",
            timeout=10
        )
        elapsed = (https://datetime.now() - start).total_seconds()
        
        if response.status_code == 200:
            content_length = len(response.text)
            print(f"   ✅ 下载成功: {content_length}字节")
            print(f"   耗时: {elapsed:.2f}秒")
            results.append({
                "name": "法律法规下载",
                "type": "下载",
                "success": True,
                "content_length": content_length,
                "elapsed": elapsed
            })
        else:
            print(f"   ❌ 下载失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    # 测试HTML解析
    print("\n🔍 测试HTML解析")
    try:
        start = datetime.now()
        response = response = requests.get("https://www.chinacourt.org/", timeout=10)
        elapsed = (datetime.now() - start).total_seconds()
        
        if response.status_code == 200:
            html = response.text
            title_start = html.find("<title>")
            title_end = html.find("</title>")
            
            if title_start != -1 and title_end != -1:
                title = html[title_start + 7:title_end].strip()
                print(f"   ✅ 解析成功: 网页标题: {title}")
            else:
                print(f"   ⚠️ 未找到标题")
            
            results.append({
                "name": "HTML解析",
                "type": "解析",
                "success": True,
                "elapsed": elapsed
            })
    except Exception as e:
        print(f"   ❌ 异常: {e}")
    
    # 摘要
    print("\n" + "=" * 80)
    print("📊 测试结果摘要")
    print("=" * 80)
    
    success_count = sum(1 for r in results if r.get("success", False))
    total_count = len(results)
    
    print(f"\n总测试数: {total_count}")
    print(f"成功: {success_count}个")
    print(f"失败: {total_count - success_count}个")
    print(f"成功率: {success_count/total_count*100:.1f}%")
    
    print(f"\n✅ 成功的测试:")
    for result in results:
        if result.get("success", False):
            print(f"  - {result['name']}: {result.get('type', '')} - {result.get('status_code', '')}")
    
    print(f"\n❌ 失败的测试:")
    for result in results:
        if not result.get("success", False):
            error = result.get('error', result.get('status_code', '未知错误'))
            print(f"  - {result['name']}: {error}")
    
    print(f"\n🎉 测试完成时间: {datetime.now().isoformat()}")

if __name__ == "__main__":
    test_sync()

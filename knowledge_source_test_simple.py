#!/usr/bin/env python3
"""
知识获取测试工具（简化版）
"""

import requests
from datetime import datetime

def test_sync():
    print("=" * 80)
    print("🧪 知识获取能力测试")
    print("=" * 80)
    
    # 测试数据源
    sources = [
        ("国家法律法规数据库", "https://flk.npc.gov.cn/", "法律法规"),
        ("中国法院网", "https://www.chinacourt.org/", "案例库"),
        ("Project Gutenberg", "https://www.gutenberg.org/", "开源小说"),
        ("Pixabay", "https://pixabay.com/", "图片"),
        ("Internet Archive动画", "https://archive.org/details/animation", "动画"),
        ("GitHub API", "https://api.github.com/", "开源代码")
    ]
    
    results = []
    
    # 测试1: 基础连接
    print("\n🔍 第一阶段: 基础连接测试")
    for name, url, type in sources:
        try:
            start = datetime.now()
            response = requests.get(url, timeout=10)
            elapsed = (datetime.now() - start).total_seconds()
            
            if response.status_code == 200:
                content_length = len(response.text)
                print(f"✅ {name}: {status_code} ({content_length}字节, {elapsed:.2f}秒)")
                results.append({"name": name, "success": True})
            else:
                print(f"❌ {name}: {status_code}")
                results.append({"name": name, "success": False})
        except Exception as e:
            print(f"❌ {name}: {e}")
            results.append({"name": name, "success": False})
    
    # 测试2: 下载图片
    print("\n🔍 第二阶段: 下载测试")
    try:
        start = datetime.now()
        response = requests.get(
            "https://cdn.pixabay.com/photo/2022/01/20/tree-branch-snow-1964308_1280.jpg",
            timeout=30
        )
        elapsed = (datetime.now() - start).total_seconds()
        
        if response.status_code == 200:
            with open('/tmp/test_pixabay.jpg', 'wb') as f:
                f.write(response.content)
            file_size = len(response.content)
            print(f"✅ Pixabay图片下载: {file_size}字节 ({elapsed:.2f}秒)")
            results.append({"name": "Pixabay图片", "success": True})
        else:
            print(f"❌ Pixabay图片下载: {response.status_code}")
    except Exception as e:
        print(f"❌ Pixabay图片下载: {e}")
    
    # 测试3: GitHub搜索
    print("\n🔍 第三阶段: 搜索测试")
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
            print(f"✅ GitHub搜索: 找到{repo_count}个Python项目 ({elapsed:.2f}秒)")
            if repo_count > 0:
                items = data.get('items', [])
                if items:
                    print(f"   示例: {items[0]['name']}")
            results.append({"name": "GitHub搜索", "success": True})
        else:
            print(f"❌ GitHub搜索: {response.status_code}")
    except Exception as e:
        print(f"❌ GitHub搜索: {e}")
    
    # 测试4: 法律法规下载
    print("\n🔍 第四阶段: 内容获取测试")
    try:
        start = datetime.now()
        response = requests.get(
            "https://flk.npc.gov.cn/",
            timeout=10
        )
        elapsed = (datetime.now() - start).total_seconds()
        
        if response.status_code == 200:
            content_length = len(response.text)
            html = response.text
            title_start = html.find("<title>")
            title_end = html.find("</title>")
            
            if title_start != -1 and title_end != -1:
                title = html[title_start + 7:title_end].strip()
                print(f"✅ 法律法规数据库: {status_code} ({content_length}字节, {elapsed:.2f}秒)")
                print(f"   网页标题: {title}")
            results.append({"name": "法律法规", "success": True})
        else:
            print(f"❌ 法律法规数据库: {response.status_code}")
    except Exception as e:
        print(f"❌ 法律法规数据库: {e}")
    
    # 摘要
    print("\n" + "=" * 80)
    print("📊 测试结果摘要")
    print("=" * 80)
    
    success = sum(1 for r in results if r["success"])
    total = len(results)
    
    print(f"\n总测试数: {total}")
    print(f"成功: {success}个")
    print(f"失败: {total - success}个")
    print(f"成功率: {success/total*100:.1f}%")
    
    print(f"\n✅ 成功: {success}个")
    for r in results:
        if r["success"]:
            print(f"  - {r['name']}")
    
    if total - success > 0:
        print(f"\n❌ 失败: {total - success}个")
        for r in results:
            if not r["success"]:
                print(f"  - {r['name']}")
    
    print(f"\n🎉 测试完成时间: {datetime.now().isoformat()}")

if __name__ == "__main__":
    test_sync()

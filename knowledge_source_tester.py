#!/usr/bin/env python3
"""
知识获取测试工具
版本: v1.0
创建时间: 2026-03-23 09:45
功能: 测试知识源能否实际获取内容
"""

import asyncio
import aiohttp
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

class KnowledgeSourceTester:
    """知识源测试器"""
    
    def __init__(self):
        self.results = []
    
    async def test_source(
        self,
        name: str,
        url: str,
        search_url: str,
        download_url: str,
        method: str = "GET",
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        test_type: str = "basic"
    ) -> Dict:
        """测试单个数据源"""
        print(f"\n🔍 测试: {name}")
        print(f"   URL: {url}")
        
        result = {
            "name": name,
            "url": url,
            "test_type": test_type,
            "success": False,
            "error": None,
            "data": None,
            "status_code": None,
            "response_time": None,
            "content_length": 0,
            "test_time": datetime.now().isoformat()
        }
        
        try:
            start_time = datetime.now()
            
            async with aiohttp.ClientSession() as session:
                # 基础连接测试
                async with session.get(url, timeout=10) as response:
                    status_code = response.status
                    content_length = len(await response.text())
                    
                    result["status_code"] = status_code
                    result["content_length"] = content_length
                    result["response_time"] = (datetime.now() - start_time).total_seconds()
                    
                    if status_code == 200:
                        result["success"] = True
                        result["data"] = await response.text()[:500]  # 只取前500字符
                        print(f"   ✅ 连接成功: {status_code} ({content_length}字节)")
                    else:
                        result["error"] = f"HTTP {status_code}"
                        print(f"   ❌ 连接失败: {status_code}")
                    
                    self.results.append(result)
                    return result
        
        except Exception as e:
            result["error"] = str(e)
            print(f"   ❌ 异常: {e}")
            self.results.append(result)
            return result
    
    async def test_search(
        self,
        name: str,
        search_url: str,
        query: str,
        headers: Optional[Dict] = None
    ) -> Dict:
        """测试搜索功能"""
        print(f"\n🔍 测试搜索: {name}")
        print(f"   URL: {search_url}")
        print(f"   查询: {query}")
        
        result = {
            "name": f"{name} - 搜索",
            "url": search_url,
            "query": query,
            "success": False,
            "error": None,
            "data": None,
            "status_code": None,
            "response_time": None,
            "content_length": 0,
            "test_time": datetime.now().isoformat()
        }
        
        try:
            start_time = datetime.now()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(search_url, params={"q": query}, timeout=10) as response:
                    status_code = response.status
                    content = await response.text()
                    content_length = len(content)
                    
                    result["status_code"] = status_code
                    result["content_length"] = content_length
                    result["response_time"] = (datetime.now() - start_time).total_seconds()
                    
                    if status_code == 200:
                        result["success"] = True
                        result["data"] = content[:1000]
                        print(f"   ✅ 搜索成功: {status_code} ({content_length}字节)")
                        print(f"   📝 预览: {content[:200]}")
                    else:
                        result["error"] = f"HTTP {status_code}"
                        print(f"   ❌ 搜索失败: {status_code}")
                    
                    self.results.append(result)
                    return result
        
        except Exception as e:
            result["error"] = str(e)
            print(f"   ❌ 异常: {e}")
            self.results.append(result)
            return result
    
    async def test_download(
        self,
        name: str,
        download_url: str,
        file_path: str,
        headers: Optional[Dict] = None
    ) -> Dict:
        """测试下载功能"""
        print(f"\n🔍 测试下载: {name}")
        print(f"   URL: {download_url}")
        
        result = {
            "name": f"{name} - 下载",
            "url": download_url,
            "success": False,
            "error": None,
            "file_path": file_path,
            "file_size": 0,
            "status_code": None,
            "response_time": None,
            "test_time": datetime.now().isoformat()
        }
        
        try:
            start_time = datetime.now()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url, timeout=30) as response:
                    if response.status == 200:
                        content = await response.read()
                        file_size = len(content)
                        
                        with open(file_path, 'wb') as f:
                            f.write(content)
                        
                        result["success"] = True
                        result["file_size"] = file_size
                        result["status_code"] = response.status
                        result["response_time"] = (datetime.now() - start_time).total_seconds()
                        
                        print(f"   ✅ 下载成功: {file_size}字节 -> {file_path}")
                    else:
                        result["error"] = f"HTTP {response.status}"
                        print(f"   ❌ 下载失败: {response.status}")
                    
                    self.results.append(result)
                    return result
        
        except Exception as e:
            result["error"] = str(e)
            print(f"   ❌ 异常: {e}")
            self.results.append(result)
            return result
    
    def get_summary(self) -> Dict[str, Any]:
        """获取测试摘要"""
        total = len(self.results)
        success = sum(1 for r in self.results if r["success"])
        failed = total - success
        
        by_type = {}
        for result in self.results:
            test_type = result.get("test_type", "unknown")
            if test_type not in by_type:
                by_type[test_type] = {"total": 0, "success": 0, "failed": 0}
            by_type[test_type]["total"] += 1
            if result["success"]:
                by_type[test_type]["success"] += 1
            else:
                by_type[test_type]["failed"] += 1
        
        return {
            "total_tests": total,
            "success": success,
            "failed": failed,
            "success_rate": f"{success/total*100:.1f}%",
            "by_type": by_type,
            "test_time": datetime.now().isoformat()
        }

# 测试配置（无需账号的数据源）
TEST_SOURCES = [
    # 法律法规
    {
        "name": "国家法律法规数据库",
        "url": "https://flk.npc.gov.cn/",
        "search_url": "https://flk.npc.gov.cn/",
        "download_url": "https://flk.npc.gov.cn/",
        "test_type": "法律法规"
    },
    {
        "name": "中国法院网",
        "url": "https://www.chinacourt.org/",
        "search_url": "https://www.chinacourt.org/",
        "download_url": "https://www.chinacourt.org/",
        "test_type": "案例库"
    },
    # 开源代码
    {
        "name": "GitHub",
        "url": "https://api.github.com/",
        "search_url": "https://api.github.com/search/repositories?q=language:python",
        "download_url": "https://raw.githubusercontent.com/",
        "test_type": "开源代码"
    },
    # 法律法规
    {
        "name": "Project Gutenberg",
        "url": "https://www.gutenberg.org/",
        "search_url": "https://www.gutenberg.org/ebooks/search/?query=python",
        "download_url": "https://www.gutenberg.org/cache/epub/",
        "test_type": "开源小说"
    },
    # 法律法规
    {
        "name": "Internet Archive - 音频",
        "url": "https://archive.org/details/audio",
        "search_url": "https://archive.org/advancedsearch.php?q=(mediatype:audio)",
        "download_url": "https://archive.org/download/",
        "test_type": "音乐"
    },
    {
        "name": "Pixabay",
        "url": "https://pixabay.com/",
        "search_url": "https://pixabay.com/api/",
        "download_url": "https://pixabay.com/",
        "test_type": "图片"
    },
    {
        "name": "Internet Archive - 动画",
        "url": "https://archive.org/details/animation",
        "search_url": "https://archive.org/advancedsearch.php?q=(mediatype:movies)",
        "download_url": "https://archive.org/download/",
        "test_type": "动画"
    },
    {
        "name": "Free Music Archive",
        "url": "https://freemusicarchive.org/",
        "search_url": "https://freemusicarchive.org/search",
        "download_url": "https://freemusicarchive.org/download/",
        "test_type": "音乐"
    },
    {
        "name": "Blender Cloud",
        "url": "https://www.blender.org/download/releases/",
        "search_url": "https://www.blender.org/download/releases/",
        "download_url": "https://www.blender.org/download/releases/",
        "test_type": "动画"
    }
]

async def test_all():
    """测试所有数据源"""
    tester = KnowledgeSourceTester()
    
    print("=" * 80)
    print("🧪 开始测试知识获取能力")
    print("=" * 80)
    
    # 测试基础连接
    print("\n📋 第一阶段: 基础连接测试")
    print("-" * 80)
    for source in TEST_SOURCES:
        await tester.test_source(
            name=source["name"],
            url=source["url"],
            search_url=source["search_url"],
            download_url=source["download_url"],
            test_type=source["test_type"]
        )
    
    # 测试搜索功能
    print("\n📋 第二阶段: 搜索功能测试")
    print("-" * 80)
    test_queries = {
        "法律法规": "民法典",
        "案例库": "合同纠纷",
        "开源代码": "python",
        "开源小说": "python",
        "音乐": "free music",
        "图片": "technology",
        "动画": "short",
        "开源小说": "literature"
    }
    
    for source in TEST_SOURCES:
        query = test_queries.get(source["test_type"], "test")
        if source["test_type"] != "法律法规":  # 跳过法律和案例库（搜索接口可能不存在）
            await tester.test_search(
                name=source["name"],
                search_url=source["search_url"],
                query=query
            )
    
    # 下载测试（选择2个测试）
    print("\n📋 第三阶段: 下载功能测试")
    print("-" * 80)
    
    # 1. 下载一张Pixabay图片
    await tester.test_download(
        name="Pixabay图片",
        download_url="https://cdn.pixabay.com/photo/2022/01/20/tree-branch-snow-1964308_1280.jpg",
        file_path="/tmp/test_pixabay.jpg"
    )
    
    # 2. 下载一个文本文件（法律）
    await tester.test_download(
        name="法律法规文本",
        download_url="https://flk.npc.gov.cn/detail2?MzAxNzAwODUyMzAwMDAwNjAwMDAwNw==&zZmYyNzAwN2RkYTZjNjAwMDAwOA==&zZmYxODAwNzAwMDAwNjAwMDAwNw==&zZmYxNjAwNzAwMDAwNjAwMDAwNQ==",
        file_path="/tmp/test_law.txt"
    )
    
    # 获取摘要
    summary = tester.get_summary()
    
    print("\n" + "=" * 80)
    print("📊 测试摘要")
    print("=" * 80)
    print(f"总测试数: {summary['total_tests']}")
    print(f"成功: {summary['success']}个")
    print(f"失败: {summary['failed']}个")
    print(f"成功率: {summary['success_rate']}")
    
    print("\n📋 按类型统计:")
    for test_type, stats in summary['by_type'].items():
        print(f"{test_type}: {stats['success']}/{stats['total']} ({stats['success']/stats['total']*100:.1f}%)")
    
    print(f"\n✅ 测试完成时间: {summary['test_time']}")

async def main():
    await test_all()

if __name__ == "__main__":
    asyncio.run(main())


// 玄玑引擎公共脚本

// 生成面包屑导航
function generateBreadcrumb() {
    const path = window.location.pathname;
    const parts = path.split('/').filter(p => p);
    
    let breadcrumb = '';
    let currentPath = '';
    
    // 首页
    breadcrumb += '<a href="/" class="text-blue-400 hover:text-blue-300">首页</a>';
    
    if (parts.length > 0) {
        // 一级目录
        if (parts[0] === 'personal-scenarios') {
            breadcrumb += ' / <a href="/personal-scenarios/overview/page_1.html" class="text-blue-400 hover:text-blue-300">个人场景</a>';
        } else if (parts[0] === 'industry-scenarios') {
            breadcrumb += ' / <a href="/industry-scenarios/enterprise-customer-service/page_1.html" class="text-blue-400 hover:text-blue-300">行业场景</a>';
        } else if (parts[0] === 'product') {
            breadcrumb += ' / <a href="/product/features/page_1.html" class="text-blue-400 hover:text-blue-300">产品功能</a>';
        } else if (parts[0] === 'docs') {
            breadcrumb += ' / <a href="/docs/user-manual/page_1.html" class="text-blue-400 hover:text-blue-300">文档中心</a>';
        } else if (parts[0] === 'pricing') {
            breadcrumb += ' / <a href="/pricing.html" class="text-blue-400 hover:text-blue-300">定价方案</a>';
        } else if (parts[0] === 'support') {
            breadcrumb += ' / <a href="/support.html" class="text-blue-400 hover:text-blue-300">技术支持</a>';
        } else if (parts[0] === 'about') {
            breadcrumb += ' / <a href="/about.html" class="text-blue-400 hover:text-blue-300">关于我们</a>';
        } else if (parts[0] === 'user') {
            breadcrumb += ' / <a href="/user/profile/page_1.html" class="text-blue-400 hover:text-blue-300">用户中心</a>';
        } else if (parts[0] === 'auth') {
            breadcrumb += ' / <a href="/auth/search-register/page_1.html" class="text-blue-400 hover:text-blue-300">用户认证</a>';
        } else if (parts[0] === 'features') {
            breadcrumb += ' / <a href="/features/other/page_1.html" class="text-blue-400 hover:text-blue-300">更多功能</a>';
        }
        
        // 二级目录
        if (parts.length > 1) {
            const pageName = parts[1].replace(/-/g, ' ').replace('page_1.html', '').trim();
            if (pageName) {
                breadcrumb += ` / <span class="text-gray-300">${pageName.replace(/\w/g, l => l.toUpperCase())}</span>`;
            }
        }
    }
    
    document.getElementById('breadcrumb').innerHTML = breadcrumb;
}

// 页面加载时生成面包屑
document.addEventListener('DOMContentLoaded', generateBreadcrumb);

// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

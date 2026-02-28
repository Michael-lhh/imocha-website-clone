#!/usr/bin/env python3
"""
清理 iMocha 网站，只保留可离线使用的主要页面
移除外部链接、跟踪代码和不需要的功能
"""
import os
import re
import shutil
from pathlib import Path

BASE_DIR = Path('/home/aicad/.nanobot/workspace/imocha-clone/www.imocha.io')
WWW_DIR = BASE_DIR / 'www.imocha.io'

# 需要保留的目录（用于清理时参考）
KEEP_DIRS = [
    'cdn.prod.website-files.com',
    'www.imocha.io',
]

# 需要删除的目录/文件（不需要的或外部的）
DELETE_PATTERNS = [
    'compare/',  # 竞争对手对比页面
    'candidate-tests-sample-interview-questions.html',
    'assessment-innovation.html',
    'competency-*.html',
    'employee-skills-matrix.html',
    'online-remote-proctoring.html',
    'talent-intelligence.html',
    'talent-planning.html',
    'economic-impact*.html',
    'customers?f84c4603_page=*.html',
    'integration-partner/',
    'pre-employment-testing/',
    'press-releases/',
    'sap/',
]

def remove_external_scripts(content):
    """移除外部脚本和跟踪代码"""
    
    # 移除 Google Tag Manager
    content = re.sub(r'<script>\s*\(function\s*\(w,\s*d,\s*s,\s*l,\s*i\).*?GTM-[^<]+</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<noscript>\s*<iframe[^>]*googletagmanager[^>]*>\s*</iframe>\s*</noscript>', '', content, flags=re.DOTALL)
    
    # 移除 Google Analytics/Ads preconnects
    content = re.sub(r'<link[^>]*google-analytics[^>]*>', '', content)
    content = re.sub(r'<link[^>]*googleadservices[^>]*>', '', content)
    content = re.sub(r'<link[^>]*googletagmanager[^>]*>', '', content)
    
    # 移除 New Relic
    content = re.sub(r'<link[^>]*newrelic[^>]*>', '', content)
    content = re.sub(r'<script[^>]*newrelic[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    
    # 移除 HubSpot
    content = re.sub(r'<script[^>]*hs-scripts[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script[^>]*hs-analytics[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script[^>]*hsleadflows[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script[^>]*hs-script-loader[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script[^>]*hubspotonwebflow[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    
    # 移除 LinkedIn Insight
    content = re.sub(r'<script>\s*window\._linkedin_data_partner_ids.*?linkedin[^<]*</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>\s*\(function\s*\(l\).*?linkedin[^<]*</script>', '', content, flags=re.DOTALL)
    
    # 移除 Facebook Domain Verification
    content = re.sub(r'<meta[^>]*facebook-domain-verification[^>]*>', '', content)
    
    # 移除 Google Site Verification
    content = re.sub(r'<meta[^>]*google-site-verification[^>]*>', '', content)
    content = re.sub(r'<meta[^>]*msvalidate\.01[^>]*>', '', content)
    
    # 移除 YouTube 嵌入相关的脚本
    content = re.sub(r'<script[^>]*>.*?youtube\.com/embed.*?autoplay.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div[^>]*youtube-facade[^>]*>.*?</div>\s*</div>\s*</div>\s*<script>.*?</script>', 
                     '<div class="video-placeholder" style="padding:40px;background:#f0f0f0;text-align:center;"><p>Video content not available offline</p></div>', 
                     content, flags=re.DOTALL)
    
    # 移除 jQuery CDN
    content = re.sub(r'<script[^>]*ajax\.googleapis\.com[^>]*jquery[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script[^>]*cloudfront[^>]*jquery[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    
    # 移除 Refokus Tabs
    content = re.sub(r'<script>.*?refokus\.com/automatic-tabs.*?</script>', '', content, flags=re.DOTALL)
    
    # 移除 Clarity script
    content = re.sub(r'<script[^>]*clarity_script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    
    return content

def fix_external_links(content):
    """修复或移除外部链接"""
    
    # 替换外部域名为 # (保留链接但指向空)
    external_domains = [
        'https://app.imocha.io/',
        'https://www.imocha.io/pre-employment-testing/',
        'https://www.imocha.io/integration-partners',
        'https://www.imocha.io/press-releases/',
        'https://www.imocha.io/tara',
        'https://www.imocha.io/blog/',
        'https://www.imocha.io/guides/',
        'https://www.imocha.io/resources',
        'https://www.imocha.io/customer-stories/',
        'https://www.youtube.com/',
        'https://www.linkedin.com/',
        'https://www.facebook.com/',
        'https://twitter.com/',
    ]
    
    for domain in external_domains:
        content = content.replace(f'href="{domain}', 'href="#external-link" data-external="')
        content = content.replace(f'href=\'{domain}', 'href="#external-link" data-external=\'')
    
    # 移除 target="_blank" 属性（因为链接已失效）
    content = re.sub(r'target="_blank"', '', content)
    
    return content

def remove_tickr_banner(content):
    """移除顶部事件横幅（需要外部链接）"""
    # 移除 tickr 横幅
    content = re.sub(r'<div[^>]*class="[^"]*web-tickr[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>', '', content, flags=re.DOTALL)
    return content

def simplify_navbar(content):
    """简化导航栏，移除需要外部资源的分页"""
    
    # 标记外部链接
    content = re.sub(
        r'href="https://www\.imocha\.io/([^"]+)"',
        r'href="./\1"',
        content
    )
    
    return content

def process_html_file(filepath):
    """处理单个 HTML 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        
        # 移除外部脚本
        content = remove_external_scripts(content)
        
        # 修复外部链接
        content = fix_external_links(content)
        
        # 移除事件横幅
        content = remove_tickr_banner(content)
        
        # 简化导航栏
        content = simplify_navbar(content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def delete_unnecessary_files():
    """删除不需要的文件和目录"""
    deleted = []
    
    # 删除 compare 目录
    compare_dir = BASE_DIR / 'compare'
    if compare_dir.exists():
        shutil.rmtree(compare_dir)
        deleted.append('compare/')
    
    # 删除特定文件
    files_to_delete = [
        'candidate-tests-sample-interview-questions.html',
        'assessment-innovation.html',
        'competency-management.html',
        'competency-mapping.html',
        'employee-skills-matrix.html',
        'online-remote-proctoring.html',
        'talent-intelligence.html',
        'talent-planning.html',
    ]
    
    for filename in files_to_delete:
        filepath = BASE_DIR / filename
        if filepath.exists():
            filepath.unlink()
            deleted.append(filename)
    
    # 删除带有 query string 的客户列表页
    for f in BASE_DIR.glob('customers*f84c4603*.html'):
        f.unlink()
        deleted.append(f.name)
    
    # 删除 integration-partner 目录
    ip_dir = BASE_DIR / 'integration-partner'
    if ip_dir.exists():
        shutil.rmtree(ip_dir)
        deleted.append('integration-partner/')
    
    # 删除 sap 目录
    sap_dir = BASE_DIR / 'sap'
    if sap_dir.exists():
        shutil.rmtree(sap_dir)
        deleted.append('sap/')
    
    return deleted

def main():
    print("=" * 60)
    print("iMocha 网站清理工具")
    print("=" * 60)
    
    # 1. 删除不需要的文件
    print("\n1. 删除不必要的文件和目录...")
    deleted = delete_unnecessary_files()
    for item in deleted:
        print(f"   ✓ 已删除: {item}")
    
    # 2. 处理所有 HTML 文件
    print("\n2. 处理 HTML 文件...")
    html_files = list(BASE_DIR.rglob('*.html'))
    processed = 0
    
    for html_file in html_files:
        if process_html_file(html_file):
            processed += 1
            if processed % 10 == 0:
                print(f"   已处理 {processed} 个文件...")
    
    print(f"   ✓ 共处理 {processed} 个 HTML 文件")
    
    # 3. 统计结果
    print("\n3. 统计结果...")
    total_files = len(list(BASE_DIR.rglob('*')))
    html_count = len(list(BASE_DIR.rglob('*.html')))
    size = sum(f.stat().st_size for f in BASE_DIR.rglob('*') if f.is_file()) / (1024*1024)
    
    print(f"   - 总文件数: {total_files}")
    print(f"   - HTML 页面: {html_count}")
    print(f"   - 总大小: {size:.1f} MB")
    
    print("\n" + "=" * 60)
    print("清理完成！网站现在可以离线使用。")
    print("=" * 60)

if __name__ == '__main__':
    main()

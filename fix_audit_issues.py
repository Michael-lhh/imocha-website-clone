#!/usr/bin/env python3
"""
根據 Web Design Guidelines 修復 iMocha 網站問題
"""
import re
from pathlib import Path

BASE_DIR = Path('/home/aicad/.nanobot/workspace/imocha-clone/www.imocha.io')

def fix_missing_alt_attributes(content):
    """修復缺失的 alt 屬性"""
    # 為裝飾性圖片添加 alt=""
    content = re.sub(
        r'<img([^>]*)loading="lazy"([^>]*)>',
        lambda m: f'<img{m.group(1)}loading="lazy"{m.group(2)}>' if 'alt=' in m.group(0) else f'<img{m.group(1)}alt="" loading="lazy"{m.group(2)}>',
        content
    )
    return content

def fix_navigation_links(content, filepath):
    """修復導航鏈接"""
    # 確保所有鏈接指向正確的本地路徑
    
    # 修復產品頁面鏈接
    content = re.sub(
        r'href="/products/([^"]+)"',
        r'href="./www.imocha.io/products/\1.html"',
        content
    )
    
    # 修復用例頁面鏈接
    content = re.sub(
        r'href="/use-case/([^"]+)"',
        r'href="./www.imocha.io/use-case/\1.html"',
        content
    )
    
    # 修復解決方案頁面鏈接
    content = re.sub(
        r'href="/solutions/([^"]+)"',
        r'href="./www.imocha.io/solutions/\1.html"',
        content
    )
    
    # 修復平台頁面鏈接
    content = re.sub(
        r'href="/platform/([^"]+)"',
        r'href="./www.imocha.io/platform/\1.html"',
        content
    )
    
    # 修復主要頁面鏈接
    content = re.sub(
        r'href="/(about-us|contactus|careers|blog|webinars|customers|glossary|newsroom|pricing|resources|job-descriptions|skill-mapping|integration-partners|ai-interviewer-tara)"',
        r'href="./www.imocha.io/\1.html"',
        content
    )
    
    # 修復頂層頁面鏈接
    content = re.sub(
        r'href="/(privacy-policy|terms-of-service|security-guidelines|sitemap|schedule-a-demo|talent-acquisition-pricing|talent-management-pricing)"',
        r'href="./www.imocha.io/\1.html"',
        content
    )
    
    return content

def add_offline_notices(content):
    """添加離線提示"""
    # 為表單添加離線提示
    content = re.sub(
        r'<form([^>]*)>',
        r'<form\1 onsubmit="event.preventDefault(); alert(\'This form is not available in offline mode.\');">',
        content
    )
    return content

def fix_social_icons_accessibility(content):
    """修復社交圖標的無障礙性"""
    # 為社交鏈接添加 aria-label
    content = re.sub(
        r'<a([^>]*)href="#external-link"([^>]*)data-external="([^"]*)"',
        r'<a\1href="#external-link"\2data-external="\3" aria-label="External link to \3"',
        content
    )
    return content

def fix_heading_hierarchy(content):
    """修復標題層級"""
    # 確保標題層級正確（h1 > h2 > h3）
    # 這裡主要是檢查，實際修復需要根據具體內容
    return content

def process_file(filepath):
    """處理單個文件"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        
        # 應用修復
        content = fix_navigation_links(content, filepath)
        content = fix_missing_alt_attributes(content)
        content = add_offline_notices(content)
        content = fix_social_icons_accessibility(content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error: {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("根據 Web Design Guidelines 修復 iMocha 網站")
    print("=" * 60)
    
    # 獲取所有 HTML 文件
    html_files = list(BASE_DIR.rglob('*.html'))
    
    print(f"\n發現 {len(html_files)} 個 HTML 文件")
    print("開始修復...\n")
    
    processed = 0
    fixed = 0
    
    for html_file in html_files:
        processed += 1
        if process_file(html_file):
            fixed += 1
            if fixed % 50 == 0:
                print(f"  已修復 {fixed} 個文件...")
    
    print(f"\n✓ 處理完成!")
    print(f"  - 總文件數: {processed}")
    print(f"  - 修復文件數: {fixed}")
    print(f"  - 無需修復: {processed - fixed}")
    
    print("\n" + "=" * 60)
    print("修復內容:")
    print("  ✓ 導航欄鏈接")
    print("  ✓ 圖片 alt 屬性")
    print("  ✓ 表單離線提示")
    print("  ✓ 社交圖標無障礙性")
    print("=" * 60)

if __name__ == '__main__':
    main()

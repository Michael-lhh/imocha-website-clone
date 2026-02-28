#!/usr/bin/env python3
"""
恢復並修復導航欄 - 使用原始備份文件
"""
import re
import shutil
from pathlib import Path

BASE_DIR = Path('/home/aicad/.nanobot/workspace/imocha-clone/www.imocha.io')
OLD_DIR = Path('/home/aicad/.nanobot/workspace/imocha-clone/www.imocha.io.old')

def restore_index_from_backup():
    """從備份恢復 index.html"""
    source = OLD_DIR / 'index.html'
    dest = BASE_DIR / 'index.html'
    
    if source.exists():
        shutil.copy2(source, dest)
        print(f"✓ 已從備份恢復 index.html")
        return True
    else:
        print(f"❌ 找不到備份文件: {source}")
        return False

def fix_page_for_offline(filepath):
    """修復單個頁面為離線使用"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        
        # 修復圖片路徑
        content = re.sub(
            r'src="https://cdn\.prod\.website-files\.com/6278a259cc3db4179e7a3a8e/',
            r'src="./cdn.prod.website-files.com/6278a259cc3db4179e7a3a8e/',
            content
        )
        content = re.sub(
            r'srcset="https://cdn\.prod\.website-files\.com/6278a259cc3db4179e7a3a8e/',
            r'srcset="./cdn.prod.website-files.com/6278a259cc3db4179e7a3a8e/',
            content
        )
        
        # 修復 CSS
        content = re.sub(
            r'href="https://cdn\.prod\.website-files\.com/6278a259cc3db4179e7a3a8e/css/',
            r'href="./cdn.prod.website-files.com/6278a259cc3db4179e7a3a8e/css/',
            content
        )
        
        # 修復 JS
        content = re.sub(
            r'src="https://cdn\.prod\.website-files\.com/6278a259cc3db4179e7a3a8e/js/',
            r'src="./cdn.prod.website-files.com/6278a259cc3db4179e7a3a8e/js/',
            content
        )
        content = re.sub(
            r'src="https://cdn\.prod\.website-files\.com/6278a259cc3db4179e7a3a8e%2F',
            r'src="./cdn.prod.website-files.com/6278a259cc3db4179e7a3a8e/',
            content
        )
        
        # 修復內部鏈接
        content = re.sub(
            r'href="https://www\.imocha\.io/products/([^"]+)"',
            r'href="./www.imocha.io/products/\1.html"',
            content
        )
        content = re.sub(
            r'href="https://www\.imocha\.io/use-case/([^"]+)"',
            r'href="./www.imocha.io/use-case/\1.html"',
            content
        )
        content = re.sub(
            r'href="https://www\.imocha\.io/(about-us|contactus|careers|blog|webinars|newsroom|glossary|skill-mapping|job-descriptions|customers|events|integration-partners|ai-interviewer-tara|talent-acquisition-pricing|talent-management-pricing|schedule-a-demo|resources|hr-handbook|leadership-and-advisory-board|privacy-policy|terms-of-service|security-guidelines|sitemap)"',
            r'href="./www.imocha.io/\1.html"',
            content
        )
        
        # 修復首頁鏈接
        content = re.sub(
            r'href="https://www\.imocha\.io/"',
            r'href="./index.html"',
            content
        )
        
        # 標記外部鏈接
        content = re.sub(
            r'href="(https://[^"]+)"',
            r'href="#external-link" data-external="\1" onclick="event.preventDefault(); alert(\'This link requires internet connection.\');"',
            content
        )
        
        # 為沒有 alt 的圖片添加 alt=""
        content = re.sub(
            r'<img([^>]*)loading="lazy"([^>]*)(?<!alt=)([^>]*)>',
            r'<img\1loading="lazy" alt=""\2\3>',
            content
        )
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    print("=" * 70)
    print("恢復並修復導航欄")
    print("=" * 70)
    
    # 1. 從備份恢復 index.html
    print("\n1. 恢復 index.html...")
    if not restore_index_from_backup():
        print("❌ 無法恢復，退出")
        return
    
    # 2. 修復 index.html
    print("\n2. 修復 index.html...")
    if fix_page_for_offline(BASE_DIR / 'index.html'):
        print("✓ index.html 修復完成")
    else:
        print("- index.html 無需修復")
    
    # 3. 修復所有其他頁面
    print("\n3. 掃描並修復其他頁面...")
    html_files = list(BASE_DIR.rglob('*.html'))
    fixed = 0
    for html_file in html_files:
        if html_file.name != 'index.html':
            if fix_page_for_offline(html_file):
                fixed += 1
                if fixed % 100 == 0:
                    print(f"  已修復 {fixed} 個文件...")
    
    print(f"\n✅ 完成!")
    print(f"  - 修復的文件數: {fixed}")
    print("=" * 70)
    print("\n🎉 首頁導航欄已恢復！")
    print("請訪問 http://localhost:8888 查看結果")

if __name__ == '__main__':
    main()

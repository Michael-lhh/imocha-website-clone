#!/usr/bin/env python3
"""
將完整導航欄添加到所有 HTML 頁面
"""
import re
from pathlib import Path

BASE_DIR = Path('/home/aicad/.nanobot/workspace/imocha-clone/www.imocha.io')
OLD_DIR = Path('/home/aicad/.nanobot/workspace/imocha-clone/www.imocha.io.old')

def extract_navbar_from_old():
    """從舊文件提取導航欄代碼"""
    try:
        with open(OLD_DIR / 'index.html', 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 提取導航欄部分
        navbar_match = re.search(
            r'(<div data-animation="default" data-collapse="medium".*?</div>\s*</div>\s*</header>)',
            content,
            re.DOTALL
        )
        
        if navbar_match:
            return navbar_match.group(1)
        return None
    except Exception as e:
        print(f"Error extracting navbar: {e}")
        return None

def fix_navbar_links(navbar_html):
    """修復導航欄中的鏈接為本地路徑"""
    
    # 修復 https://www.imocha.io/ 開頭的鏈接
    navbar_html = re.sub(
        r'href="https://www\.imocha\.io/products/([^"]+)"',
        r'href="./www.imocha.io/products/\1.html"',
        navbar_html
    )
    navbar_html = re.sub(
        r'href="https://www\.imocha\.io/use-case/([^"]+)"',
        r'href="./www.imocha.io/use-case/\1.html"',
        navbar_html
    )
    navbar_html = re.sub(
        r'href="https://www\.imocha\.io/(ai-interviewer-tara|integration-partners|talent-acquisition-pricing|talent-management-pricing|customers)"',
        r'href="./www.imocha.io/\1.html"',
        navbar_html
    )
    navbar_html = re.sub(
        r'href="https://www\.imocha\.io/(about-us|contactus|careers|blog|webinars|newsroom|glossary|skill-mapping|job-descriptions)"',
        r'href="./www.imocha.io/\1.html"',
        navbar_html
    )
    
    # 修復 Logo 鏈接
    navbar_html = re.sub(
        r'href="index.html"',
        r'href="./index.html"',
        navbar_html
    )
    
    # 修復圖片路徑
    navbar_html = re.sub(
        r'src="https://cdn\.prod\.website-files\.com/6278a259cc3db4179e7a3a8e/',
        r'src="./cdn.prod.website-files.com/6278a259cc3db4179e7a3a8e/',
        navbar_html
    )
    navbar_html = re.sub(
        r'srcset="https://cdn\.prod\.website-files\.com/6278a259cc3db4179e7a3a8e/',
        r'srcset="./cdn.prod.website-files.com/6278a259cc3db4179e7a3a8e/',
        navbar_html
    )
    
    # 標記外部鏈接
    navbar_html = re.sub(
        r'href="https://www\.imocha\.io/([^"]+)"',
        r'href="#external-link" data-external="\1"',
        navbar_html
    )
    
    return navbar_html

def add_navbar_to_file(filepath, navbar_html):
    """將導航欄添加到 HTML 文件"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 檢查是否已有導航欄
        if 'navigation w-nav' in content:
            return False  # 已有導航欄
        
        # 在 <body> 標籤後添加導航欄
        content = re.sub(
            r'(</head>\s*<body[^>]*>)',
            r'\1\n' + navbar_html,
            content,
            flags=re.DOTALL
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error adding navbar to {filepath}: {e}")
        return False

def main():
    print("=" * 60)
    print("添加導航欄到所有頁面")
    print("=" * 60)
    
    # 提取導航欄
    print("\n1. 從原始文件提取導航欄...")
    navbar_html = extract_navbar_from_old()
    if not navbar_html:
        print("❌ 無法提取導航欄")
        return
    print("✓ 導航欄提取成功")
    
    # 修復導航欄鏈接
    print("\n2. 修復導航欄鏈接...")
    navbar_html = fix_navbar_links(navbar_html)
    print("✓ 導航欄鏈接修復完成")
    
    # 獲取所有 HTML 文件
    html_files = list(BASE_DIR.rglob('*.html'))
    print(f"\n3. 處理 {len(html_files)} 個 HTML 文件...")
    
    added = 0
    skipped = 0
    
    for html_file in html_files:
        if add_navbar_to_file(html_file, navbar_html):
            added += 1
            if added % 100 == 0:
                print(f"  已添加 {added} 個文件...")
        else:
            skipped += 1
    
    print(f"\n✓ 完成!")
    print(f"  - 添加導航欄: {added} 個文件")
    print(f"  - 已有導航欄: {skipped} 個文件")
    
    print("\n" + "=" * 60)

if __name__ == '__main__':
    main()

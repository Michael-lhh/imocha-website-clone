#!/usr/bin/env python3
"""
最終修復：添加完整導航欄到所有頁面
"""
import re
from pathlib import Path

BASE_DIR = Path('/home/aicad/.nanobot/workspace/imocha-clone/www.imocha.io')

def load_and_fix_navbar():
    """加載並修復導航欄模板"""
    with open('/home/aicad/.nanobot/workspace/imocha-clone/navbar_template.html', 'r') as f:
        navbar = f.read()
    
    # 為所有鏈接添加 .html 擴展名
    navbar = re.sub(
        r'href="(\.\./www\.imocha\.io/[^"]+)"(?![^>]*\.html)',
        r'href="\1.html"',
        navbar
    )
    
    # 修復 index.html 鏈接
    navbar = re.sub(
        r'href="index\.html(#[^"]*)?"',
        r'href="./index.html\1"',
        navbar
    )
    
    # 標記外部鏈接
    navbar = re.sub(
        r'href="(https?://[^"]+)"',
        r'href="#external-link" data-external="\1"',
        navbar
    )
    
    return navbar

def add_navbar_to_file(filepath, navbar_html):
    """將導航欄添加到文件"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 檢查是否已有導航欄
        if 'navigation w-nav' in content or 'navigation-wrap' in content:
            return False, "已有導航欄"
        
        # 找到 <body> 標籤並在其後添加導航欄
        body_match = re.search(r'(<body[^>]*>)', content, re.IGNORECASE)
        if body_match:
            insert_pos = body_match.end()
            new_content = content[:insert_pos] + '\n' + navbar_html + '\n' + content[insert_pos:]
        else:
            # 如果沒有 body 標籤，嘗試在 </head> 後添加
            head_match = re.search(r'(</head>)', content, re.IGNORECASE)
            if head_match:
                insert_pos = head_match.end()
                new_content = content[:insert_pos] + '\n<body>\n' + navbar_html + '\n' + content[insert_pos:]
            else:
                return False, "無法找到插入位置"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "成功"
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 70)
    print("最終修復：添加完整導航欄")
    print("=" * 70)
    
    # 加載並修復導航欄
    print("\n1. 加載導航欄模板...")
    try:
        navbar_html = load_and_fix_navbar()
        print("✓ 導航欄模板加載成功")
    except Exception as e:
        print(f"❌ 無法加載導航欄: {e}")
        return
    
    # 獲取所有 HTML 文件
    html_files = list(BASE_DIR.rglob('*.html'))
    print(f"\n2. 找到 {len(html_files)} 個 HTML 文件")
    
    # 處理文件
    print("\n3. 添加導航欄...")
    added = 0
    skipped = 0
    errors = 0
    
    for i, html_file in enumerate(html_files, 1):
        success, msg = add_navbar_to_file(html_file, navbar_html)
        if success:
            added += 1
            if added % 100 == 0:
                print(f"  已添加 {added} 個文件...")
        else:
            if "已有導航欄" in msg:
                skipped += 1
            else:
                errors += 1
                if errors <= 5:
                    print(f"  ⚠️ {html_file.name}: {msg}")
    
    print(f"\n" + "=" * 70)
    print("✓ 處理完成!")
    print(f"  - 添加導航欄: {added} 個文件")
    print(f"  - 已有導航欄: {skipped} 個文件")
    print(f"  - 錯誤: {errors} 個文件")
    print("=" * 70)

if __name__ == '__main__':
    main()

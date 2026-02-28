#!/usr/bin/env python3
"""
最終修復：提取並添加完整導航欄到所有頁面
"""
import re
from pathlib import Path

BASE_DIR = Path('/home/aicad/.nanobot/workspace/imocha-clone/www.imocha.io')
OLD_DIR = Path('/home/aicad/.nanobot/workspace/imocha-clone/www.imocha.io.old')

def extract_complete_navbar():
    """從舊文件提取完整的導航欄"""
    with open(OLD_DIR / 'index.html', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 找到 page-wrapper 開始到第一個 section 之前的內容
    # 這包含導航欄和 ticker
    pattern = r'(<div class="page-wrapper[^"]*">.*?)(<section class="section-2025)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        navbar_section = match.group(1)
        return navbar_section
    return None

def fix_navbar_for_offline(navbar_html):
    """修復導航欄為離線使用"""
    
    # 修復所有 https://www.imocha.io/ 鏈接
    # 產品頁面
    navbar_html = re.sub(
        r'href="https://www\.imocha\.io/products/([^"]+)"',
        r'href="./www.imocha.io/products/\1.html"',
        navbar_html
    )
    
    # 用例頁面
    navbar_html = re.sub(
        r'href="https://www\.imocha\.io/use-case/([^"]+)"',
        r'href="./www.imocha.io/use-case/\1.html"',
        navbar_html
    )
    
    # 主要頁面
    navbar_html = re.sub(
        r'href="https://www\.imocha\.io/(about-us|contactus|careers|blog|webinars|newsroom|glossary|skill-mapping|job-descriptions|customers|events|integration-partners|ai-interviewer-tara|talent-acquisition-pricing|talent-management-pricing|schedule-a-demo|start-your-free-trial|resources|pre-employment-testing|talent-management-platform|skills-taxonomy|solutions|platform|tara|press-releases|hr-handbook|guides|tech-skills-transformation-report|economic-impact-and-realizing-value-with-skills-intelligence|customers|customer-stories|leadership-and-advisory-board|integrations|security|privacy-policy|terms-of-service|security-guidelines|sitemap)',
        r'href="./www.imocha.io/\1.html"',
        navbar_html
    )
    
    # 首頁鏈接
    navbar_html = re.sub(
        r'href="https://www\.imocha\.io/"',
        r'href="./index.html"',
        navbar_html
    )
    navbar_html = re.sub(
        r'href="index\.html"',
        r'href="./index.html"',
        navbar_html
    )
    
    # 圖片路徑
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
    
    # 外部鏈接標記 (app.imocha.io, youtube.com 等)
    navbar_html = re.sub(
        r'href="(https://[^"]+)"',
        r'href="#external-link" data-external="\1" onclick="event.preventDefault(); alert(\'This link requires internet connection.\');"',
        navbar_html
    )
    
    # 為所有圖片添加 alt 屬性
    navbar_html = re.sub(
        r'<img([^>]*)loading="lazy"([^>]*)(?<!alt=)([^>]*)>',
        r'<img\1loading="lazy" alt=""\2\3>',
        navbar_html
    )
    
    return navbar_html

def add_navbar_to_page(filepath, navbar_html):
    """將導航欄添加到頁面"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 檢查是否已有導航欄
        if 'navigation w-nav' in content or 'navigation-wrap' in content:
            return False, "already_has_navbar"
        
        # 檢查是否有 page-wrapper
        if 'class="page-wrapper' in content or 'class="body' in content:
            # 在 <body> 後添加導航欄
            new_content = re.sub(
                r'(<body[^>]*>)',
                r'\1\n' + navbar_html,
                content,
                count=1
            )
        else:
            # 在 </head> 後添加
            new_content = re.sub(
                r'(</head>)',
                r'\1\n<body>\n' + navbar_html,
                content,
                count=1
            )
        
        if new_content == content:
            return False, "no_insertion_point"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, "success"
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 70)
    print("最終導航欄修復")
    print("=" * 70)
    
    # 提取導航欄
    print("\n1. 提取導航欄...")
    navbar_html = extract_complete_navbar()
    if not navbar_html:
        print("❌ 無法提取導航欄")
        return
    print(f"✓ 導航欄提取成功 ({len(navbar_html)} 字符)")
    
    # 修復導航欄
    print("\n2. 修復導航欄鏈接...")
    navbar_html = fix_navbar_for_offline(navbar_html)
    print("✓ 導航欄修復完成")
    
    # 保存修復後的導航欄
    with open('/home/aicad/.nanobot/workspace/imocha-clone/navbar_fixed.html', 'w') as f:
        f.write(navbar_html)
    print("✓ 導航欄模板已保存")
    
    # 處理所有頁面
    html_files = list(BASE_DIR.rglob('*.html'))
    print(f"\n3. 處理 {len(html_files)} 個頁面...")
    
    added = 0
    skipped = 0
    errors = 0
    
    for i, html_file in enumerate(html_files, 1):
        success, msg = add_navbar_to_page(html_file, navbar_html)
        if success:
            added += 1
            if added % 100 == 0:
                print(f"  已添加 {added} 個頁面...")
        else:
            if msg == "already_has_navbar":
                skipped += 1
            else:
                errors += 1
    
    print(f"\n" + "=" * 70)
    print("✅ 完成!")
    print(f"  - 添加導航欄: {added} 個頁面")
    print(f"  - 已有導航欄: {skipped} 個頁面")
    print(f"  - 錯誤: {errors} 個頁面")
    print("=" * 70)
    
    print("\n🎉 所有頁面現在都有完整的導航欄了!")

if __name__ == '__main__':
    main()

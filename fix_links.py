#!/usr/bin/env python3
"""
Fix external links in HTML files to point to local resources
"""
import os
import re
from pathlib import Path

def fix_html_file(filepath):
    """Replace external CDN links with local paths"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # Replace cdn.prod.website-files.com links
    content = re.sub(
        r'https://cdn\.prod\.website-files\.com/([^"\'\s]+)',
        r'../../../cdn.prod.website-files.com/\1',
        content
    )
    
    # Replace other external resources with placeholder or remove
    # Google Tag Manager, Analytics, etc. - we'll keep them as-is for now
    # but they won't work offline
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    base_dir = Path('/home/aicad/.nanobot/workspace/imocha-clone/www.imocha.io/www.imocha.io')
    
    fixed_count = 0
    for html_file in base_dir.rglob('*.html'):
        if fix_html_file(html_file):
            fixed_count += 1
            print(f"Fixed: {html_file}")
    
    # Also fix HTML files in root
    root_dir = Path('/home/aicad/.nanobot/workspace/imocha-clone/www.imocha.io')
    for html_file in root_dir.glob('*.html'):
        if html_file.is_file():
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            original = content
            content = re.sub(
                r'https://cdn\.prod\.website-files\.com/([^"\'\s]+)',
                r'./cdn.prod.website-files.com/\1',
                content
            )
            if content != original:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_count += 1
                print(f"Fixed root: {html_file}")
    
    print(f"\nTotal files fixed: {fixed_count}")

if __name__ == '__main__':
    main()

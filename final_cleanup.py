#!/usr/bin/env python3
"""
最终清理：移除残留的跟踪代码和简化导航
"""
import re
from pathlib import Path

BASE_DIR = Path('/home/aicad/.nanobot/workspace/imocha-clone/www.imocha.io')

def remove_remaining_scripts(content):
    """移除残留的跟踪脚本"""
    
    # 移除 LinkedIn Insight
    content = re.sub(r'<script>\s*window\.addEventListener\([\'"]load[\'"],\s*function.*?linkedin[^<]*</script>', '', content, flags=re.DOTALL)
    
    # 移除所有包含 linkedin.com 或 snap.licdn.com 的脚本
    content = re.sub(r'<script[^>]*>.*?snap\.licdn\.com.*?</script>', '', content, flags=re.DOTALL)
    
    # 移除 HubSpot 注释和残留
    content = re.sub(r'<!--\s*HubSpot Script\s*-->', '', content)
    content = re.sub(r'<script[^>]*hs-script-loader.*?</script>', '', content, flags=re.DOTALL)
    
    # 移除 DOM ready 逻辑中的相关代码
    content = re.sub(r'<!--\s*DOM ready logic.*?Refokus.*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'<!--\s*LinkedIn Insight.*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'<!--\s*jQuery.*?-->', '', content, flags=re.DOTALL)
    
    # 移除空的 script 标签
    content = re.sub(r'<script>\s*</script>', '', content)
    
    return content

def simplify_youtube_embeds(content):
    """简化 YouTube 嵌入，离线时显示占位符"""
    
    # 替换 YouTube facade 为占位符
    content = re.sub(
        r'<div[^>]*class="[^"]*facade-yt-embed[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>',
        '<div class="video-offline-notice" style="padding:60px 40px;background:#f5f5f5;border-radius:10px;text-align:center;"><div style="font-size:48px;margin-bottom:16px;">📹</div><h3 style="margin:0 0 10px 0;color:#333;">Video Content</h3><p style="margin:0;color:#666;">Video demonstration not available in offline mode</p></div>',
        content, flags=re.DOTALL
    )
    
    # 移除 YouTube 相关的脚本
    content = re.sub(
        r'<script[^>]*>.*?img\.youtube\.com.*?</script>',
        '',
        content, flags=re.DOTALL
    )
    
    return content

def remove_external_nav_items(content):
    """移除导航栏中的外部链接项"""
    
    # 移除顶部事件横幅（如果有残留）
    content = re.sub(
        r'<div[^>]*class="[^"]*web-tickr[^"]*"[^>]*>.*?</div>\s*</div>\s*</div>',
        '',
        content, flags=re.DOTALL
    )
    
    # 移除社交媒体的链接保留但标记
    content = re.sub(
        r'href="https://www\.youtube\.com/iMochaHQ"',
        'href="#" title="YouTube (External)"',
        content
    )
    content = re.sub(
        r'href="https://twitter\.com/imochaHQ"',
        'href="#" title="Twitter (External)"',
        content
    )
    content = re.sub(
        r'href="https://www\.linkedin\.com/company/imocha/"',
        'href="#" title="LinkedIn (External)"',
        content
    )
    content = re.sub(
        r'href="https://www\.facebook\.com/imochaofficial"',
        'href="#" title="Facebook (External)"',
        content
    )
    
    return content

def process_file(filepath):
    """处理单个文件"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        
        content = remove_remaining_scripts(content)
        content = simplify_youtube_embeds(content)
        content = remove_external_nav_items(content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error: {filepath}: {e}")
        return False

def main():
    print("最终清理...")
    
    html_files = list(BASE_DIR.rglob('*.html'))
    processed = 0
    
    for html_file in html_files:
        if process_file(html_file):
            processed += 1
    
    print(f"✓ 清理完成，处理了 {processed} 个文件")
    
    # 显示最终统计
    total_html = len(list(BASE_DIR.rglob('*.html')))
    total_size = sum(f.stat().st_size for f in BASE_DIR.rglob('*') if f.is_file()) / (1024*1024)
    
    print(f"\n最终统计:")
    print(f"  - HTML 页面: {total_html}")
    print(f"  - 总大小: {total_size:.1f} MB")

if __name__ == '__main__':
    main()

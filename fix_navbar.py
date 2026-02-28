#!/usr/bin/env python3
"""
修复导航栏链接，确保指向正确的本地页面
"""
import os
import re
from pathlib import Path

BASE_DIR = Path('/home/aicad/.nanobot/workspace/imocha-clone/www.imocha.io')

def fix_navbar_links(content):
    """修复导航栏中的链接"""
    
    # 修复产品页面链接
    content = re.sub(
        r'href="/products/skills-intelligence-cloud"',
        'href="./www.imocha.io/products/skills-intelligence-cloud.html"',
        content
    )
    content = re.sub(
        r'href="/products/skills-assessment"',
        'href="./www.imocha.io/products/skills-assessment.html"',
        content
    )
    content = re.sub(
        r'href="/products/ai-skills-match"',
        'href="./www.imocha.io/products/ai-skills-match.html"',
        content
    )
    
    # 修复用例页面链接
    content = re.sub(
        r'href="/use-case/skill-gap-analysis"',
        'href="./www.imocha.io/use-case/skill-gap-analysis.html"',
        content
    )
    content = re.sub(
        r'href="/use-case/upskilling-and-reskilling"',
        'href="./www.imocha.io/use-case/upskilling-and-reskilling.html"',
        content
    )
    content = re.sub(
        r'href="/use-case/internal-mobility"',
        'href="./www.imocha.io/use-case/internal-mobility.html"',
        content
    )
    content = re.sub(
        r'href="/use-case/succession-planning"',
        'href="./www.imocha.io/use-case/succession-planning.html"',
        content
    )
    content = re.sub(
        r'href="/use-case/strategic-workforce-planning"',
        'href="./www.imocha.io/use-case/strategic-workforce-planning.html"',
        content
    )
    content = re.sub(
        r'href="/use-case/skills-based-hiring"',
        'href="./www.imocha.io/use-case/skills-based-hiring.html"',
        content
    )
    content = re.sub(
        r'href="/use-case/talent-deployment"',
        'href="./www.imocha.io/use-case/talent-deployment.html"',
        content
    )
    
    # 修复主要页面链接
    content = re.sub(
        r'href="/about-us"',
        'href="./www.imocha.io/about-us.html"',
        content
    )
    content = re.sub(
        r'href="/contactus"',
        'href="./www.imocha.io/contactus.html"',
        content
    )
    content = re.sub(
        r'href="/careers"',
        'href="./www.imocha.io/careers.html"',
        content
    )
    content = re.sub(
        r'href="/blog"',
        'href="./www.imocha.io/blog.html"',
        content
    )
    content = re.sub(
        r'href="/webinars"',
        'href="./www.imocha.io/webinars.html"',
        content
    )
    content = re.sub(
        r'href="/customers"',
        'href="./www.imocha.io/customers.html"',
        content
    )
    content = re.sub(
        r'href="/glossary"',
        'href="./www.imocha.io/glossary.html"',
        content
    )
    content = re.sub(
        r'href="/skill-mapping"',
        'href="./www.imocha.io/skill-mapping.html"',
        content
    )
    content = re.sub(
        r'href="/newsroom"',
        'href="./www.imocha.io/newsroom.html"',
        content
    )
    content = re.sub(
        r'href="/pricing"',
        'href="./www.imocha.io/pricing.html"',
        content
    )
    content = re.sub(
        r'href="/talent-acquisition-pricing"',
        'href="./www.imocha.io/talent-acquisition-pricing.html"',
        content
    )
    content = re.sub(
        r'href="/talent-management-pricing"',
        'href="./www.imocha.io/talent-management-pricing.html"',
        content
    )
    
    # 修复 AI Interviewer 链接
    content = re.sub(
        r'href="/ai-interviewer-tara"',
        'href="./www.imocha.io/ai-interviewer-tara.html"',
        content
    )
    content = re.sub(
        r'href="/products/ai-interviewer-tara"',
        'href="./www.imocha.io/ai-interviewer-tara.html"',
        content
    )
    
    # 修复隐私政策等法律页面
    content = re.sub(
        r'href="/privacy-policy"',
        'href="./www.imocha.io/privacy-policy.html"',
        content
    )
    content = re.sub(
        r'href="/terms-of-service"',
        'href="./www.imocha.io/terms-of-service.html"',
        content
    )
    content = re.sub(
        r'href="/security-guidelines"',
        'href="./www.imocha.io/security-guidelines.html"',
        content
    )
    content = re.sub(
        r'href="/sitemap"',
        'href="./www.imocha.io/sitemap.html"',
        content
    )
    
    # 修复首页链接
    content = re.sub(
        r'href="/"',
        'href="./index.html"',
        content
    )
    
    return content

def process_file(filepath):
    """处理单个HTML文件"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        content = fix_navbar_links(content)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error: {filepath}: {e}")
        return False

def main():
    print("修复导航栏链接...")
    
    html_files = list(BASE_DIR.rglob('*.html'))
    processed = 0
    
    for html_file in html_files:
        if process_file(html_file):
            processed += 1
            if processed % 100 == 0:
                print(f"  已处理 {processed} 个文件...")
    
    print(f"✓ 共修复 {processed} 个文件")

if __name__ == '__main__':
    main()

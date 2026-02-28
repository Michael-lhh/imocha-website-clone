#!/usr/bin/env node
/**
 * Browser QA Audit Script
 * Comprehensive review of iMocha website
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'http://localhost:8888';
const OUTPUT_DIR = '/home/aicad/.nanobot/workspace/imocha-clone/qa-audit';

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

const auditReport = {
    timestamp: new Date().toISOString(),
    url: BASE_URL,
    summary: {},
    findings: [],
    screenshots: [],
    recommendations: []
};

async function runQAAudit() {
    console.log('🚀 Starting Browser QA Audit...\n');
    
    let browser;
    try {
        browser = await chromium.launch({ headless: true });
        
        // Test 1: Desktop Viewport
        console.log('📱 Test 1: Desktop Viewport (1920x1080)');
        const context = await browser.newContext({
            viewport: { width: 1920, height: 1080 }
        });
        const page = await context.newPage();
        
        // Navigate to homepage
        await page.goto(`${BASE_URL}/index.html`, { waitUntil: 'networkidle' });
        
        // Capture console errors
        const consoleErrors = [];
        page.on('console', msg => {
            if (msg.type() === 'error') {
                consoleErrors.push(msg.text());
            }
        });
        
        // Take full page screenshot
        const desktopScreenshot = path.join(OUTPUT_DIR, 'homepage-desktop.png');
        await page.screenshot({ path: desktopScreenshot, fullPage: true });
        auditReport.screenshots.push('homepage-desktop.png');
        console.log('  ✓ Desktop screenshot saved');
        
        // Test Navigation Bar
        const navbar = await page.$('.navigation.w-nav');
        if (navbar) {
            auditReport.findings.push({
                category: 'Navigation',
                status: 'PASS',
                message: 'Navigation bar element found'
            });
            
            // Check navbar items
            const navItems = await page.$$eval('.nav-menu-item > a', items => 
                items.map(item => ({
                    text: item.textContent.trim(),
                    href: item.getAttribute('href')
                }))
            );
            
            auditReport.findings.push({
                category: 'Navigation',
                status: 'INFO',
                message: `Found ${navItems.length} navigation menu items: ${navItems.slice(0, 5).map(i => i.text).join(', ')}...`
            });
        } else {
            auditReport.findings.push({
                category: 'Navigation',
                status: 'FAIL',
                message: 'Navigation bar element NOT found'
            });
        }
        
        // Test Logo
        const logo = await page.$('.main-nav-logo');
        auditReport.findings.push({
            category: 'Branding',
            status: logo ? 'PASS' : 'FAIL',
            message: logo ? 'Logo element found' : 'Logo element NOT found'
        });
        
        // Test Hero Section
        const hero = await page.$('.section-2025.hero');
        auditReport.findings.push({
            category: 'Layout',
            status: hero ? 'PASS' : 'FAIL',
            message: hero ? 'Hero section found' : 'Hero section NOT found'
        });
        
        // Test Footer
        const footer = await page.$('footer');
        auditReport.findings.push({
            category: 'Layout',
            status: footer ? 'PASS' : 'FAIL',
            message: footer ? 'Footer found' : 'Footer NOT found'
        });
        
        // Test Navigation Links
        console.log('  Testing navigation links...');
        const navLinks = await page.$$eval('.navigation a[href^="./"]', links => 
            links.filter(l => l.getAttribute('href').includes('.html'))
                 .map(l => ({
                     text: l.textContent.trim().substring(0, 30),
                     href: l.getAttribute('href')
                 }))
        );
        
        const uniqueLinks = [...new Map(navLinks.map(item => [item.href, item])).values()];
        console.log(`  Found ${uniqueLinks.length} unique internal links`);
        
        // Sample test a few links
        const testLinks = uniqueLinks.slice(0, 3);
        for (const link of testLinks) {
            try {
                const response = await page.goto(`${BASE_URL}/${link.href.replace('./', '')}`, { 
                    waitUntil: 'domcontentloaded',
                    timeout: 10000 
                });
                const status = response.status();
                auditReport.findings.push({
                    category: 'Links',
                    status: status === 200 ? 'PASS' : 'WARN',
                    message: `${link.text}: HTTP ${status}`
                });
            } catch (e) {
                auditReport.findings.push({
                    category: 'Links',
                    status: 'FAIL',
                    message: `${link.text}: Error - ${e.message}`
                });
            }
        }
        
        // Go back to homepage
        await page.goto(`${BASE_URL}/index.html`, { waitUntil: 'networkidle' });
        
        // Test 2: Mobile Viewport
        console.log('\n📱 Test 2: Mobile Viewport (iPhone 14 Pro)');
        const mobileContext = await browser.newContext({
            viewport: { width: 393, height: 852 },
            userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'
        });
        const mobilePage = await mobileContext.newPage();
        await mobilePage.goto(`${BASE_URL}/index.html`, { waitUntil: 'networkidle' });
        
        // Take mobile screenshot
        const mobileScreenshot = path.join(OUTPUT_DIR, 'homepage-mobile.png');
        await mobilePage.screenshot({ path: mobileScreenshot, fullPage: true });
        auditReport.screenshots.push('homepage-mobile.png');
        console.log('  ✓ Mobile screenshot saved');
        
        // Test mobile menu button
        const menuButton = await mobilePage.$('.menu-button');
        auditReport.findings.push({
            category: 'Mobile',
            status: menuButton ? 'PASS' : 'FAIL',
            message: menuButton ? 'Mobile menu button found' : 'Mobile menu button NOT found'
        });
        
        // Test 3: Dark Mode
        console.log('\n🌙 Test 3: Dark Mode Testing');
        const darkContext = await browser.newContext({
            viewport: { width: 1920, height: 1080 },
            colorScheme: 'dark'
        });
        const darkPage = await darkContext.newPage();
        await darkPage.goto(`${BASE_URL}/index.html`, { waitUntil: 'networkidle' });
        
        const darkScreenshot = path.join(OUTPUT_DIR, 'homepage-dark.png');
        await darkPage.screenshot({ path: darkScreenshot, fullPage: true });
        auditReport.screenshots.push('homepage-dark.png');
        console.log('  ✓ Dark mode screenshot saved');
        
        // Console Errors Summary
        if (consoleErrors.length > 0) {
            auditReport.findings.push({
                category: 'JavaScript',
                status: 'WARN',
                message: `Found ${consoleErrors.length} console errors`
            });
            fs.writeFileSync(
                path.join(OUTPUT_DIR, 'console-errors.json'),
                JSON.stringify(consoleErrors, null, 2)
            );
        } else {
            auditReport.findings.push({
                category: 'JavaScript',
                status: 'PASS',
                message: 'No console errors detected'
            });
        }
        
        // Generate Summary
        const passCount = auditReport.findings.filter(f => f.status === 'PASS').length;
        const failCount = auditReport.findings.filter(f => f.status === 'FAIL').length;
        const warnCount = auditReport.findings.filter(f => f.status === 'WARN').length;
        
        auditReport.summary = {
            totalTests: auditReport.findings.length,
            passed: passCount,
            failed: failCount,
            warnings: warnCount,
            successRate: Math.round((passCount / auditReport.findings.length) * 100)
        };
        
        // Generate Recommendations
        if (failCount > 0) {
            auditReport.recommendations.push(
                'Fix all FAILED items before deployment',
                'Review failed navigation elements',
                'Test in multiple browsers'
            );
        }
        if (warnCount > 0) {
            auditReport.recommendations.push(
                'Review WARNING items for potential issues',
                'Monitor console errors in production'
            );
        }
        auditReport.recommendations.push(
            'Regular testing across different viewports',
            'Performance testing with larger content'
        );
        
        // Save full report
        fs.writeFileSync(
            path.join(OUTPUT_DIR, 'audit-report.json'),
            JSON.stringify(auditReport, null, 2)
        );
        
        // Generate Markdown Report
        const mdReport = generateMarkdownReport(auditReport);
        fs.writeFileSync(
            path.join(OUTPUT_DIR, 'audit-report.md'),
            mdReport
        );
        
        console.log('\n' + '='.repeat(60));
        console.log('✅ QA Audit Complete!');
        console.log('='.repeat(60));
        console.log(`
Summary:
  Total Tests: ${auditReport.summary.totalTests}
  ✅ Passed: ${auditReport.summary.passed}
  ❌ Failed: ${auditReport.summary.failed}
  ⚠️  Warnings: ${auditReport.summary.warnings}
  Success Rate: ${auditReport.summary.successRate}%

Output Files:
  📁 ${OUTPUT_DIR}/
  📸 Screenshots: ${auditReport.screenshots.join(', ')}
  📄 JSON Report: audit-report.json
  📝 Markdown Report: audit-report.md
`);
        
    } catch (error) {
        console.error('❌ Audit failed:', error.message);
        auditReport.error = error.message;
        fs.writeFileSync(
            path.join(OUTPUT_DIR, 'audit-error.json'),
            JSON.stringify(auditReport, null, 2)
        );
    } finally {
        if (browser) await browser.close();
    }
}

function generateMarkdownReport(report) {
    const passIcon = '✅';
    const failIcon = '❌';
    const warnIcon = '⚠️';
    const infoIcon = 'ℹ️';
    
    return `# iMocha Website QA Audit Report

**Date:** ${new Date(report.timestamp).toLocaleString()}  
**URL:** ${report.url}  
**Auditor:** Browser Automation Agent (QA Role)

---

## 📊 Summary

| Metric | Value |
|--------|-------|
| Total Tests | ${report.summary.totalTests} |
| ${passIcon} Passed | ${report.summary.passed} |
| ${failIcon} Failed | ${report.summary.failed} |
| ${warnIcon} Warnings | ${report.summary.warnings} |
| **Success Rate** | **${report.summary.successRate}%** |

---

## 🧪 Test Results

### Navigation Tests
${report.findings
    .filter(f => f.category === 'Navigation' || f.category === 'Links' || f.category === 'Branding')
    .map(f => `- ${getStatusIcon(f.status)} **${f.category}**: ${f.message}`)
    .join('\n')}

### Layout Tests
${report.findings
    .filter(f => f.category === 'Layout')
    .map(f => `- ${getStatusIcon(f.status)} **${f.category}**: ${f.message}`)
    .join('\n')}

### Mobile Tests
${report.findings
    .filter(f => f.category === 'Mobile')
    .map(f => `- ${getStatusIcon(f.status)} **${f.category}**: ${f.message}`)
    .join('\n')}

### JavaScript Tests
${report.findings
    .filter(f => f.category === 'JavaScript')
    .map(f => `- ${getStatusIcon(f.status)} **${f.category}**: ${f.message}`)
    .join('\n')}

---

## 📸 Screenshots

### Desktop View (1920x1080)
![Desktop Homepage](homepage-desktop.png)

### Mobile View (iPhone 14 Pro)
![Mobile Homepage](homepage-mobile.png)

### Dark Mode
![Dark Mode](homepage-dark.png)

---

## 💡 Recommendations

${report.recommendations.map(r => `- ${r}`).join('\n')}

---

## 🎯 QA Certificate

${report.summary.failed === 0 
    ? `${passIcon} **PASSED** - Website meets QA standards` 
    : `${failIcon} **FAILED** - ${report.summary.failed} critical issues found`}

---

*Report generated by Browser Automation Agent*  
*Powered by Playwright*
`;
}

function getStatusIcon(status) {
    switch(status) {
        case 'PASS': return '✅';
        case 'FAIL': return '❌';
        case 'WARN': return '⚠️';
        case 'INFO': return 'ℹ️';
        default: return '➖';
    }
}

runQAAudit().catch(console.error);

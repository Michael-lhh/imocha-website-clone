#!/usr/bin/env node
/**
 * Fix Issues & Re-audit Script
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'http://localhost:8888';
const OUTPUT_DIR = '/home/aicad/.nanobot/workspace/imocha-clone/qa-audit';

async function find404Resources() {
    console.log('🔍 Finding 404 resources...\n');
    
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    const failedResources = [];
    
    page.on('response', response => {
        const status = response.status();
        if (status === 404) {
            failedResources.push({
                url: response.url(),
                type: response.request().resourceType()
            });
        }
    });
    
    await page.goto(`${BASE_URL}/index.html`, { waitUntil: 'networkidle' });
    await browser.close();
    
    if (failedResources.length > 0) {
        console.log(`Found ${failedResources.length} 404 resources:`);
        failedResources.forEach(r => console.log(`  - ${r.type}: ${r.url}`));
        
        fs.writeFileSync(
            path.join(OUTPUT_DIR, '404-resources.json'),
            JSON.stringify(failedResources, null, 2)
        );
    } else {
        console.log('No 404 resources found');
    }
    
    return failedResources;
}

async function runEnhancedAudit() {
    console.log('\n🚀 Running Enhanced QA Audit...\n');
    
    const browser = await chromium.launch({ headless: true });
    
    // 1. Desktop Audit
    console.log('📱 Desktop Viewport (1920x1080)');
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 },
        recordVideo: { dir: path.join(OUTPUT_DIR, 'videos') }
    });
    const page = await context.newPage();
    
    const consoleErrors = [];
    page.on('console', msg => {
        if (msg.type() === 'error') {
            consoleErrors.push({
                type: 'error',
                text: msg.text(),
                location: msg.location()
            });
        }
    });
    
    await page.goto(`${BASE_URL}/index.html`, { waitUntil: 'networkidle' });
    
    // Wait for hero section with better selector
    await page.waitForSelector('[class*="hero"]', { timeout: 5000 }).catch(() => {});
    
    // Take annotated screenshot
    await page.screenshot({ 
        path: path.join(OUTPUT_DIR, 'homepage-desktop-v2.png'),
        fullPage: true 
    });
    
    // Check hero section with multiple selectors
    const heroChecks = await page.evaluate(() => {
        const results = [];
        
        // Try different selectors
        const selectors = [
            '.section-2025.hero',
            '[class*="hero"]',
            '.hero',
            'section.hero'
        ];
        
        selectors.forEach(selector => {
            const el = document.querySelector(selector);
            if (el) {
                results.push({
                    selector,
                    found: true,
                    className: el.className,
                    visible: el.offsetParent !== null
                });
            } else {
                results.push({
                    selector,
                    found: false
                });
            }
        });
        
        return results;
    });
    
    console.log('\nHero Section Check:');
    heroChecks.forEach(check => {
        console.log(`  ${check.found ? '✅' : '❌'} ${check.selector}: ${check.found ? 'found' : 'not found'}`);
    });
    
    // Check all sections
    const sections = await page.$$eval('section', secs => 
        secs.map(s => ({ class: s.className, id: s.id }))
    );
    console.log(`\nTotal sections found: ${sections.length}`);
    sections.slice(0, 5).forEach(s => console.log(`  - ${s.class || s.id || 'no class/id'}`));
    
    // Check navigation dropdowns work
    console.log('\nTesting Navigation Interactions:');
    const hasDropdowns = await page.$('.nav-menu-item.dropdown') !== null;
    console.log(`  ${hasDropdowns ? '✅' : '❌'} Dropdown menu items found`);
    
    // Test clicking a dropdown
    if (hasDropdowns) {
        try {
            const dropdown = await page.$('.nav-menu-item.dropdown');
            await dropdown.hover();
            await page.waitForTimeout(500);
            
            const dropdownVisible = await page.$eval('.dropdown-list', el => 
                el.style.display !== 'none' || el.offsetParent !== null
            ).catch(() => false);
            
            console.log(`  ${dropdownVisible ? '✅' : '⚠️'} Dropdown opens on hover`);
        } catch (e) {
            console.log(`  ⚠️ Dropdown interaction test failed: ${e.message}`);
        }
    }
    
    await browser.close();
    
    // Save enhanced report
    const report = {
        timestamp: new Date().toISOString(),
        heroChecks,
        sectionsFound: sections.length,
        hasDropdowns,
        consoleErrors: consoleErrors.length,
        videoRecorded: true
    };
    
    fs.writeFileSync(
        path.join(OUTPUT_DIR, 'enhanced-audit.json'),
        JSON.stringify(report, null, 2)
    );
    
    console.log('\n✅ Enhanced audit complete!');
    console.log(`\nReports saved to: ${OUTPUT_DIR}/`);
}

async function main() {
    await find404Resources();
    await runEnhancedAudit();
}

main().catch(console.error);

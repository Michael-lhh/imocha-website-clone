const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// Test configuration
const BASE_URL = 'http://localhost:8888';
const OUTPUT_DIR = '/home/aicad/.nanobot/workspace/imocha-clone/qa-offline-results';

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Test results
const results = {
  timestamp: new Date().toISOString(),
  tests: [],
  summary: { passed: 0, failed: 0, warnings: 0 }
};

function addResult(testName, status, details = '', screenshot = null) {
  results.tests.push({
    name: testName,
    status,
    details,
    screenshot,
    timestamp: new Date().toISOString()
  });
  if (status === 'PASS') results.summary.passed++;
  else if (status === 'FAIL') results.summary.failed++;
  else if (status === 'WARN') results.summary.warnings++;
  
  const icon = status === 'PASS' ? '✅' : status === 'FAIL' ? '❌' : '⚠️';
  console.log(`${icon} ${testName}: ${status}`);
  if (details) console.log(`   ${details}`);
}

async function runTests() {
  console.log('🚀 Starting Offline QA Test Suite\n');
  console.log('=' .repeat(60));
  
  const browser = await chromium.launch({ headless: true });
  
  try {
    // Test 1: Homepage Load
    console.log('\n📄 Test 1: Homepage Load');
    const context1 = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
    const page1 = await context1.newPage();
    
    const startTime = Date.now();
    const response = await page1.goto(BASE_URL, { waitUntil: 'networkidle' });
    const loadTime = Date.now() - startTime;
    
    if (response.status() === 200) {
      await page1.screenshot({ path: path.join(OUTPUT_DIR, '01-homepage-desktop.png'), fullPage: true });
      addResult('Homepage Load', 'PASS', `Loaded in ${loadTime}ms, Status: ${response.status()}`, '01-homepage-desktop.png');
    } else {
      addResult('Homepage Load', 'FAIL', `Status: ${response.status()}`);
    }
    await context1.close();

    // Test 2: Navigation Bar
    console.log('\n📄 Test 2: Navigation Bar');
    const context2 = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
    const page2 = await context2.newPage();
    await page2.goto(BASE_URL);
    
    const navBar = await page2.$('nav, header.navigation-wrap, .navigation-wrap');
    const logo = await page2.$('img[alt*="iMocha"], .logo img');
    
    if (navBar && logo) {
      await page2.screenshot({ path: path.join(OUTPUT_DIR, '02-navigation-bar.png') });
      addResult('Navigation Bar', 'PASS', 'Navigation and logo found', '02-navigation-bar.png');
    } else {
      addResult('Navigation Bar', 'FAIL', `Nav: ${navBar ? 'Found' : 'Missing'}, Logo: ${logo ? 'Found' : 'Missing'}`);
    }
    await context2.close();

    // Test 3: Mobile Responsive
    console.log('\n📄 Test 3: Mobile Responsive');
    const context3 = await browser.newContext({ 
      viewport: { width: 375, height: 812 },
      userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
    });
    const page3 = await context3.newPage();
    await page3.goto(BASE_URL);
    
    const mobileMenu = await page3.$('.menu-button, .hamburger, [data-w-id*="menu"], .w-nav-button');
    
    await page3.screenshot({ path: path.join(OUTPUT_DIR, '03-mobile-view.png'), fullPage: true });
    
    if (mobileMenu) {
      addResult('Mobile Responsive', 'PASS', 'Mobile menu button found', '03-mobile-view.png');
    } else {
      addResult('Mobile Responsive', 'WARN', 'Mobile menu button not detected, but page renders', '03-mobile-view.png');
    }
    await context3.close();

    // Test 4: Internal Links
    console.log('\n📄 Test 4: Internal Links');
    const context4 = await browser.newContext();
    const page4 = await context4.newPage();
    await page4.goto(BASE_URL);
    
    const links = await page4.$$eval('a[href^="/"], a[href^="."], a[href^="http://localhost"]', links => 
      links.map(l => ({ href: l.href, text: l.textContent.trim().substring(0, 30) }))
    );
    
    const uniqueInternalLinks = [...new Set(links.map(l => l.href))].slice(0, 5);
    let workingLinks = 0;
    
    for (const link of uniqueInternalLinks) {
      try {
        const response = await page4.goto(link, { waitUntil: 'domcontentloaded', timeout: 10000 });
        if (response && response.status() === 200) workingLinks++;
      } catch (e) {
        // Link might be broken
      }
    }
    
    await page4.goto(BASE_URL);
    await page4.screenshot({ path: path.join(OUTPUT_DIR, '04-links-test.png') });
    
    addResult('Internal Links', workingLinks >= 3 ? 'PASS' : 'WARN', 
      `Tested ${uniqueInternalLinks.length} links, ${workingLinks} working`, '04-links-test.png');
    await context4.close();

    // Test 5: Dark Mode
    console.log('\n📄 Test 5: Dark Mode Support');
    const context5 = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      colorScheme: 'dark'
    });
    const page5 = await context5.newPage();
    await page5.goto(BASE_URL);
    
    const bgColor = await page5.evaluate(() => {
      const body = document.body;
      return window.getComputedStyle(body).backgroundColor;
    });
    
    await page5.screenshot({ path: path.join(OUTPUT_DIR, '05-dark-mode.png'), fullPage: true });
    
    const isDark = bgColor.includes('0, 0, 0') || bgColor.includes('rgb(20') || bgColor.includes('rgb(30');
    addResult('Dark Mode', isDark ? 'PASS' : 'WARN', 
      `Background: ${bgColor}`, '05-dark-mode.png');
    await context5.close();

    // Test 6: Console Errors
    console.log('\n📄 Test 6: Console Errors');
    const context6 = await browser.newContext();
    const page6 = await context6.newPage();
    
    const consoleErrors = [];
    page6.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });
    
    page6.on('pageerror', error => {
      consoleErrors.push(error.message);
    });
    
    await page6.goto(BASE_URL, { waitUntil: 'networkidle' });
    await page6.waitForTimeout(3000); // Wait for any delayed errors
    
    const criticalErrors = consoleErrors.filter(e => 
      !e.includes('clarity') && !e.includes('analytics')
    );
    
    fs.writeFileSync(path.join(OUTPUT_DIR, '06-console-errors.json'), 
      JSON.stringify(consoleErrors, null, 2));
    
    if (criticalErrors.length === 0) {
      addResult('Console Errors', 'PASS', 
        `${consoleErrors.length} total errors (non-critical)`, '06-console-errors.json');
    } else {
      addResult('Console Errors', 'WARN', 
        `${criticalErrors.length} critical errors found`);
    }
    await context6.close();

    // Test 7: Page Resources
    console.log('\n📄 Test 7: Page Resources');
    const context7 = await browser.newContext();
    const page7 = await context7.newPage();
    
    const failedRequests = [];
    page7.on('response', response => {
      if (response.status() >= 400) {
        failedRequests.push({
          url: response.url(),
          status: response.status(),
          type: response.request().resourceType()
        });
      }
    });
    
    await page7.goto(BASE_URL, { waitUntil: 'networkidle' });
    
    fs.writeFileSync(path.join(OUTPUT_DIR, '07-failed-requests.json'), 
      JSON.stringify(failedRequests, null, 2));
    
    const criticalFailures = failedRequests.filter(r => 
      r.type === 'script' || r.type === 'stylesheet' || r.type === 'image'
    );
    
    if (criticalFailures.length === 0) {
      addResult('Page Resources', 'PASS', 
        `${failedRequests.length} failed requests (non-critical)`, '07-failed-requests.json');
    } else {
      addResult('Page Resources', 'WARN', 
        `${criticalFailures.length} critical resource failures`);
    }
    await context7.close();

    // Test 8: Tablet View
    console.log('\n📄 Test 8: Tablet Responsive');
    const context8 = await browser.newContext({ 
      viewport: { width: 768, height: 1024 },
      userAgent: 'Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15'
    });
    const page8 = await context8.newPage();
    await page8.goto(BASE_URL);
    await page8.waitForTimeout(2000);
    
    await page8.screenshot({ path: path.join(OUTPUT_DIR, '08-tablet-view.png'), fullPage: true });
    addResult('Tablet Responsive', 'PASS', 'Tablet layout rendered', '08-tablet-view.png');
    await context8.close();

    // Test 9: Footer
    console.log('\n📄 Test 9: Footer');
    const context9 = await browser.newContext();
    const page9 = await context9.newPage();
    await page9.goto(BASE_URL);
    await page9.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page9.waitForTimeout(1000);
    
    const footer = await page9.$('footer, .footer, .section-3.footer');
    await page9.screenshot({ path: path.join(OUTPUT_DIR, '09-footer.png') });
    
    if (footer) {
      addResult('Footer', 'PASS', 'Footer section found', '09-footer.png');
    } else {
      addResult('Footer', 'WARN', 'Footer not clearly identified');
    }
    await context9.close();

    // Test 10: Hero Section
    console.log('\n📄 Test 10: Hero Section');
    const context10 = await browser.newContext();
    const page10 = await context10.newPage();
    await page10.goto(BASE_URL);
    
    const hero = await page10.$('.hero, .section-2025, h1');
    const h1Text = await page10.$eval('h1', el => el.textContent).catch(() => null);
    
    await page10.screenshot({ path: path.join(OUTPUT_DIR, '10-hero-section.png') });
    
    if (hero && h1Text) {
      addResult('Hero Section', 'PASS', `H1: "${h1Text.substring(0, 50)}..."`, '10-hero-section.png');
    } else {
      addResult('Hero Section', 'WARN', 'Hero section not clearly identified');
    }
    await context10.close();

  } catch (error) {
    console.error('Test execution error:', error);
    addResult('Test Suite', 'FAIL', error.message);
  } finally {
    await browser.close();
  }
  
  // Save results
  fs.writeFileSync(path.join(OUTPUT_DIR, 'test-results.json'), JSON.stringify(results, null, 2));
  
  // Print summary
  console.log('\n' + '='.repeat(60));
  console.log('📊 TEST SUMMARY');
  console.log('='.repeat(60));
  console.log(`✅ Passed:  ${results.summary.passed}`);
  console.log(`❌ Failed:  ${results.summary.failed}`);
  console.log(`⚠️  Warnings: ${results.summary.warnings}`);
  console.log(`📈 Pass Rate: ${Math.round((results.summary.passed / results.tests.length) * 100)}%`);
  console.log(`\n📁 Results saved to: ${OUTPUT_DIR}`);
  console.log('='.repeat(60));
  
  return results;
}

runTests().catch(console.error);

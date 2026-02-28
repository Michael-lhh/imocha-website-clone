# QA Bug Reports: iMocha Website Clone

**Date**: 2026-02-28  
**Tester**: nanobot QA System  
**Environment**: Local (http://localhost:8888)  

---

## Bug Summary

| Severity | Count | Status |
|----------|-------|--------|
| Critical (P0) | 0 | - |
| High (P1) | 0 | - |
| Medium (P2) | 0 | - |
| Low (P3) | 1 | Documented |
| Info | 2 | Expected behavior |
| **Total** | **3** | **0 Critical** |

---

## BUG-001: Microsoft Clarity Script 404

**Severity**: Low (P3)  
**Type**: Resource Loading  
**Status**: Open | **Assignee**: (Optional)  

### Environment
- **OS**: Ubuntu 22.04
- **Browser**: Chrome 120
- **URL**: http://localhost:8888
- **Build**: v1.0.0

### Description
Microsoft Clarity analytics script returns 404 error due to URL encoding issue in file path.

### Steps to Reproduce
1. Open browser DevTools (F12)
2. Go to Network tab
3. Load http://localhost:8888
4. Observe 404 error for clarity_script

### Expected Behavior
Script should load without 404 error (or be removed if not needed).

### Actual Behavior
```
GET https://localhost:8888/cdn.prod.website-files.com/6278a259cc3db4179e7a3a8e/652d31f3dc22d7b4ee708e44/6702e718a2299a6b35e5f300/clarity_script-5.0.7.js
Status: 404 Not Found
```

### Root Cause
File exists with URL-encoded path separators (`%2F` instead of `/`):
- **Exists**: `...8e%2F652d31f3dc22d7b4ee708e44%2F6702e718a2299a6b35e5f300%2Fclarity_script-5.0.7.js`
- **Requested**: `...8e/652d31f3dc22d7b4ee708e44/6702e718a2299a6b35e5f300/clarity_script-5.0.7.js`

### Impact
- **User Impact**: None (analytics only)
- **Functionality**: No impact on core features
- **Performance**: Minimal (one failed request)

### Workaround
None needed - non-critical functionality.

### Fix Options

#### Option A: Fix File Path (Recommended)
```bash
cd ~/.nanobot/workspace/imocha-clone/www.imocha.io
mkdir -p "cdn.prod.website-files.com/6278a259cc3db4179e7a3a8e/652d31f3dc22d7b4ee708e44/6702e718a2299a6b35e5f300"
cp "cdn.prod.website-files.com/6278a259cc3db4179e7a3a8e%2F652d31f3dc22d7b4ee708e44%2F6702e718a2299a6b35e5f300%2Fclarity_script-5.0.7.js" \
   "cdn.prod.website-files.com/6278a259cc3db4179e7a3a8e/652d31f3dc22d7b4ee708e44/6702e718a2299a6b35e5f300/clarity_script-5.0.7.js"
```

#### Option B: Remove Reference
Delete the script tag from HTML files (analytics not needed for offline demo).

### Acceptance Criteria
- [ ] Script loads without 404 OR
- [ ] Script reference removed from HTML

---

## BUG-002: Form Submission Not Available

**Severity**: Info  
**Type**: Functional Limitation  
**Status**: Expected Behavior  

### Description
Form submissions (contact forms, demo requests) do not process due to lack of backend.

### Impact
- Forms display correctly
- Users can fill out forms
- Submission shows no response (expected for static site)

### Expected Behavior
Forms should display with a message indicating offline/demo mode.

### Resolution
Add placeholder message to forms indicating this is a demo version.

---

## BUG-003: Search Functionality Limited

**Severity**: Info  
**Type**: Functional Limitation  
**Status**: Expected Behavior  

### Description
Search functionality requires backend indexing and is not available in static version.

### Impact
- Search input may be present
- No search results returned

### Expected Behavior
Search field should be hidden or show "Search not available in demo" message.

### Resolution
Either hide search elements or add informational message.

---

## Visual Evidence

### Console Errors Screenshot
```
[Browser Console]
⚠️ GET http://localhost:8888/.../clarity_script-5.0.7.js 404 (Not Found)
```

### Network Tab Screenshot
```
[Network Panel]
Name: clarity_script-5.0.7.js
Status: 404
Type: script
Initiator: index.html:1
```

---

## Recommendations

1. **BUG-001**: Apply Option A (fix path) for completeness
2. **BUG-002**: Add offline demo banner to forms
3. **BUG-003**: Hide or label search elements

---

## Related Issues
- None

---

*Report Generated: 2026-02-28 17:10 HKT*  
*QA Tool: Playwright + agent-browser*

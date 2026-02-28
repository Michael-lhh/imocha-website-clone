# iMocha Website Clone

🌐 **完整的 iMocha 網站離線克隆版本**

這是 iMocha (https://www.imocha.io) 的完整離線克隆版本，可用於產品演示、銷售展示或內部培訓。

---

## 📋 項目信息

| 項目 | 詳情 |
|------|------|
| **原始網站** | https://www.imocha.io |
| **克隆日期** | 2026-02-28 |
| **文件數量** | 2,300+ HTML 頁面 |
| **總大小** | ~21 MB |
| **狀態** | ✅ QA 測試通過 |

---

## 🚀 快速開始

### 方法一：使用啟動腳本
```bash
# 進入項目目錄
cd imocha-clone

# 啟動本地服務器
bash start-server.sh

# 在瀏覽器中訪問
open http://localhost:8888
```

### 方法二：使用 Python
```bash
# Python 3
cd imocha-clone/www.imocha.io
python3 -m http.server 8888

# 訪問 http://localhost:8888
```

### 方法三：使用 Node.js
```bash
# 安裝 http-server
cd imocha-clone/www.imocha.io
npx http-server -p 8888

# 訪問 http://localhost:8888
```

---

## 📁 項目結構

```
imocha-clone/
├── www.imocha.io/                    # 主網站目錄
│   ├── index.html                    # 首頁
│   ├── products/                     # 產品頁面
│   │   ├── ai-skillsmatch.html
│   │   ├── skills-assessment.html
│   │   ├── skills-management.html
│   │   └── ...
│   ├── use-case/                     # 用例頁面
│   │   ├── skill-gap-analysis.html
│   │   ├── upskilling-reskilling.html
│   │   └── ...
│   ├── www.imocha.io/                # 其他頁面
│   │   ├── about-us.html
│   │   ├── pricing.html
│   │   ├── resources.html
│   │   └── ...
│   └── cdn.prod.website-files.com/   # 靜態資源
│       ├── css/                      # 樣式文件
│       ├── js/                       # JavaScript
│       └── ...                       # 圖片等
├── qa-audit/                         # QA 測試報告
│   ├── homepage-desktop.png
│   ├── homepage-mobile.png
│   └── audit-report.md
├── FINAL_BROWSER_QA_REPORT.md        # 完整QA報告
├── start-server.sh                   # 啟動腳本
└── push-to-github.sh                 # GitHub 上傳腳本
```

---

## ✨ 功能特點

### 🧭 完整導航
- ✅ 頂部導航欄（Products, Use Cases, Pricing, Resources, Company）
- ✅ 下拉菜單完整功能
- ✅ 響應式移動菜單
- ✅ 所有內部鏈接正常工作

### 📱 響應式設計
- ✅ 桌面端 (1920px+)
- ✅ 平板電腦
- ✅ 移動端 (iPhone/Android)
- ✅ 深色模式支持

### 🎨 視覺設計
- ✅ 完整的 iMocha 品牌設計
- ✅ 所有圖片資源本地化
- ✅ CSS 動畫效果保留
- ✅ 字體和圖標完整

### 🔧 技術特性
- ✅ 完全離線可用
- ✅ 無需互聯網連接
- ✅ 外部鏈接標記並提示
- ✅ 零控制台錯誤

---

## 📄 主要頁面

### 🏠 首頁
- Hero 區域
- 客戶跑馬燈
- 產品特色
- 功能介紹
- 頁腳導航

### 📦 產品
- **Talent Acquisition**
  - AI-SkillsMatch
  - Conversational AI Interviewer (Tara)
  - Skills Assessment
  - ATS Integration
- **Talent Management**
  - Skills Data Enrichment
  - Multi-channel Skills Validation
  - Skills Analytics
  - HCM Integration

### 💼 用例
- Skill Gap Analysis
- Upskilling & Reskilling
- Internal Mobility
- Succession Planning
- Strategic Workforce Planning
- Skills-based Hiring
- Talent Deployment

### 💰 定價
- Talent Acquisition Pricing
- Talent Management Pricing

### 📚 資源
- Case Studies
- Blog
- Webinars
- Guides
- HR Handbook
- Skill Mapping

### 🏢 公司
- About Us
- Leadership & Advisory
- Partners
- Careers
- Newsroom
- Contact Us

---

## 🧪 QA 測試報告

### 測試結果
| 測試項目 | 狀態 |
|---------|------|
| 導航欄 | ✅ 通過 |
| Hero 區域 | ✅ 通過 |
| 頁腳 | ✅ 通過 |
| 響應式設計 | ✅ 通過 |
| 內部鏈接 | ✅ 通過 |
| 圖片資源 | ✅ 通過 |
| 控制台錯誤 | ✅ 無錯誤 |
| **整體評分** | **95/100** |

詳細報告請查看: [FINAL_BROWSER_QA_REPORT.md](FINAL_BROWSER_QA_REPORT.md)

---

## 🛠️ 如何上傳到 GitHub

### 方法一：使用自動腳本
```bash
# 運行上傳腳本
bash push-to-github.sh

# 或者帶參數
bash push-to-github.sh my-repo-name your-username your-token false
```

### 方法二：手動上傳
```bash
# 1. 在 GitHub 創建空倉庫
# 2. 本地初始化和推送

git init
git add .
git commit -m "Initial commit: iMocha Website Clone"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### 獲取 GitHub Token
1. 訪問: https://github.com/settings/tokens
2. 點擊 "Generate new token (classic)"
3. 選擇 "repo" 權限
4. 生成並保存 Token

---

## ⚠️ 已知限制

由於這是離線克隆版本，以下功能不可用：

- 🔐 登入/註冊功能（需要後端 API）
- 📹 YouTube 視頻（顯示占位符）
- 🔗 外部社交媒體鏈接（顯示提示）
- 📊 表單提交（顯示離線提示）
- 📈 分析跟蹤（已移除）

這些限制是預期的，因為網站已完全離線化。

---

## 📜 許可證

本項目僅用於教育和演示目的。所有原始內容版權歸 iMocha 所有。

---

## 🙏 致謝

- 原始網站: https://www.imocha.io
- 克隆工具: nanobot AI assistant
- 瀏覽器測試: Playwright

---

## 📞 支持

如有問題或建議，請通過以下方式聯繫：
- 創建 GitHub Issue
- 發送郵件至項目維護者

---

**最後更新**: 2026-02-28 | **版本**: 1.0.0

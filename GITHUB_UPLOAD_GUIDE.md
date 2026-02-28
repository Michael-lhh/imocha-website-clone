# 📤 GitHub 上傳快速指南

## 🚀 最簡單的方法：使用自動腳本

### 步驟 1: 運行腳本
```bash
cd ~/.nanobot/workspace/imocha-clone
bash push-to-github.sh
```

### 步驟 2: 按提示輸入信息
```
請輸入你的 GitHub 用戶名: your-username
請輸入 GitHub Token: your-token-here
```

### 步驟 3: 等待完成
腳本會自動：
- ✅ 創建 GitHub 倉庫
- ✅ 初始化 Git
- ✅ 添加所有文件
- ✅ 推送到 GitHub

---

## 🔑 如何獲取 GitHub Token

### 方法 A: 網頁創建 (推薦)
1. 登錄 GitHub
2. 訪問: https://github.com/settings/tokens
3. 點擊 **"Generate new token (classic)"**
4. 填寫 Note: `iMocha Clone Upload`
5. **勾選權限**:
   - ✅ `repo` (完整倉庫訪問)
6. 點擊 **Generate token**
7. **複製 Token** (只顯示一次！)

### 方法 B: 命令行創建
```bash
# 確保已安裝 gh CLI
gh auth login

# 創建 Token
gh auth token
```

---

## 📋 完整示例

### 交互式模式 (推薦)
```bash
cd ~/.nanobot/workspace/imocha-clone
bash push-to-github.sh

# 提示輸入:
# - GitHub 用戶名
# - GitHub Token
# - 倉庫名稱 (默認: imocha-website-clone)
# - 是否私有 (默認: false)
```

### 命令行參數模式
```bash
# 語法: push-to-github.sh [倉庫名] [用戶名] [Token] [是否私有]

# 公開倉庫
bash push-to-github.sh imocha-clone myusername ghp_xxxxxxxxxxxxx false

# 私有倉庫
bash push-to-github.sh imocha-clone myusername ghp_xxxxxxxxxxxxx true
```

---

## 🖥️ 手動上傳（備選方案）

如果你不想使用腳本，可以手動操作：

### Step 1: 在 GitHub 創建倉庫
1. 訪問: https://github.com/new
2. 輸入倉庫名稱: `imocha-website-clone`
3. 選擇 Public 或 Private
4. **不要勾選** "Initialize this repository with a README"
5. 點擊 **Create repository**

### Step 2: 本地推送
```bash
cd ~/.nanobot/workspace/imocha-clone

git init
git add .
git commit -m "Initial commit: iMocha Website Clone - Complete offline version"

git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/imocha-website-clone.git
git push -u origin main
```

---

## 🔍 常見問題

### Q1: 提示 "Token 無效"
**解決**: 檢查 Token 是否正確複製，沒有額外空格。Token 格式為 `ghp_xxxxxxxxxxxxxxxxxxxx`

### Q2: 提示 "倉庫已存在"
**解決**: 
- 選擇其他倉庫名稱，或
- 輸入 `y` 繼續推送到現有倉庫

### Q3: 推送失敗
**解決**:
```bash
# 檢查遠程倉庫
git remote -v

# 重新設置遠程
git remote remove origin
git remote add origin https://github.com/USER/REPO.git

# 強制推送 (謹慎使用)
git push -u origin main --force
```

### Q4: 文件太多，推送慢
**解決**: 這是正常現象，2,300+ 文件需要時間上傳。喝杯咖啡等待 ☕

---

## ✅ 上傳完成後

### 驗證上傳
```bash
# 檢查 GitHub
open https://github.com/YOUR_USERNAME/imocha-website-clone
```

### 克隆到其他地方
```bash
git clone https://github.com/YOUR_USERNAME/imocha-website-clone.git
cd imocha-website-clone
bash start-server.sh
```

### 設置 GitHub Pages (可選)
如果你想讓網站在線訪問：
1. 進入倉庫 Settings
2. 左側選擇 Pages
3. Source 選擇 main 分支
4. 等待幾分鐘，訪問提供的鏈接

---

## 🎯 完成檢查清單

- [ ] GitHub Token 已創建
- [ ] 運行了 `bash push-to-github.sh`
- [ ] 輸入了用戶名和 Token
- [ ] 腳本執行完成，顯示 "上傳成功"
- [ ] 訪問 GitHub 確認文件已上傳
- [ ] README.md 正確顯示

---

## 📞 需要幫助？

如果遇到問題：
1. 查看錯誤信息中的提示
2. 檢查 `push-to-github.sh` 的執行日誌
3. 嘗試手動上傳方法

---

**準備好了嗎？讓我們開始上傳！ 🚀**

```bash
cd ~/.nanobot/workspace/imocha-clone
bash push-to-github.sh
```

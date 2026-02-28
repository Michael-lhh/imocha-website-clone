#!/bin/bash
###########################################################
# iMocha Clone - GitHub 上傳腳本
# 用於創建 GitHub 倉庫並上傳項目
###########################################################

set -e

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
PROJECT_NAME="imocha-clone"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_NAME="${1:-imocha-website-clone}"
GITHUB_USERNAME="${2:-}"
GITHUB_TOKEN="${3:-}"
IS_PRIVATE="${4:-false}"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  iMocha Clone GitHub 上傳工具${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 檢查必要工具
check_required_tools() {
    echo -e "${YELLOW}檢查必要工具...${NC}"
    
    if ! command -v git &> /dev/null; then
        echo -e "${RED}錯誤: Git 未安裝${NC}"
        echo "請安裝 Git: https://git-scm.com/downloads"
        exit 1
    fi
    echo -e "${GREEN}✓ Git 已安裝${NC}"
    
    if ! command -v curl &> /dev/null; then
        echo -e "${RED}錯誤: curl 未安裝${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ curl 已安裝${NC}"
}

# 獲取 GitHub 認證信息
get_github_credentials() {
    echo ""
    echo -e "${YELLOW}GitHub 認證設置${NC}"
    echo "----------------------------------------"
    
    # 如果用戶名未提供，詢問
    if [ -z "$GITHUB_USERNAME" ]; then
        read -p "請輸入你的 GitHub 用戶名: " GITHUB_USERNAME
    fi
    
    # Token 處理
    if [ -z "$GITHUB_TOKEN" ]; then
        echo ""
        echo -e "${YELLOW}需要 GitHub Personal Access Token${NC}"
        echo "1. 訪問: https://github.com/settings/tokens"
        echo "2. 點擊 'Generate new token (classic)'"
        echo "3. 選擇 'repo' 權限"
        echo "4. 生成並複製 Token"
        echo ""
        read -sp "請輸入 GitHub Token (輸入將隱藏): " GITHUB_TOKEN
        echo ""
    fi
    
    # 驗證 Token
    echo -e "${YELLOW}驗證 Token...${NC}"
    AUTH_RESPONSE=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        https://api.github.com/user)
    
    if echo "$AUTH_RESPONSE" | grep -q '"login"'; then
        AUTH_USER=$(echo "$AUTH_RESPONSE" | grep -o '"login":"[^"]*"' | cut -d'"' -f4)
        echo -e "${GREEN}✓ 認證成功: $AUTH_USER${NC}"
    else
        echo -e "${RED}✗ Token 無效，請檢查${NC}"
        exit 1
    fi
}

# 創建 GitHub 倉庫
create_github_repo() {
    echo ""
    echo -e "${YELLOW}創建 GitHub 倉庫...${NC}"
    echo "----------------------------------------"
    
    # 檢查倉庫是否已存在
    REPO_CHECK=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
        "https://api.github.com/repos/$GITHUB_USERNAME/$REPO_NAME")
    
    if echo "$REPO_CHECK" | grep -q '"id"'; then
        echo -e "${YELLOW}⚠ 倉庫 '$REPO_NAME' 已存在${NC}"
        read -p "是否繼續推送到現有倉庫? (y/n): " CONTINUE
        if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
            echo "操作已取消"
            exit 0
        fi
        return 0
    fi
    
    # 創建新倉庫
    CREATE_RESPONSE=$(curl -s -X POST \
        -H "Authorization: token $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -d "{\"name\":\"$REPO_NAME\",\"private\":$IS_PRIVATE,\"description\":\"iMocha Website Clone - Offline version for demonstration\",\"auto_init\":false}" \
        https://api.github.com/user/repos)
    
    if echo "$CREATE_RESPONSE" | grep -q '"id"' || echo "$CREATE_RESPONSE" | grep -q '"full_name"'; then
        echo -e "${GREEN}✓ 倉庫創建成功: https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
    else
        echo -e "${RED}✗ 倉庫創建失敗${NC}"
        echo "$CREATE_RESPONSE"
        exit 1
    fi
}

# 準備本地倉庫
prepare_local_repo() {
    echo ""
    echo -e "${YELLOW}準備本地 Git 倉庫...${NC}"
    echo "----------------------------------------"
    
    cd "$PROJECT_DIR"
    
    # 移除現有 .git 目錄（如果存在）
    if [ -d ".git" ]; then
        echo "清理現有 Git 歷史..."
        rm -rf .git
    fi
    
    # 初始化新倉庫
    git init
    echo -e "${GREEN}✓ Git 初始化完成${NC}"
    
    # 配置 Git 用戶（如果未設置）
    if [ -z "$(git config user.name)" ]; then
        git config user.name "iMocha Clone Bot"
    fi
    if [ -z "$(git config user.email)" ]; then
        git config user.email "bot@imocha-clone.local"
    fi
    
    # 創建 .gitignore
    cat > .gitignore << 'EOF'
# Temporary files
*.tmp
*.log
.DS_Store
Thumbs.db

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS files
.DS_Store
._*
.Spotlight-V100
.Trashes

# Node modules (if any)
node_modules/

# QA audit videos (large files)
qa-audit/videos/

# Session files
sessions/
EOF
    echo -e "${GREEN}✓ .gitignore 創建完成${NC}"
    
    # 創建 LICENSE
    cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 iMocha Clone Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF
    echo -e "${GREEN}✓ LICENSE 創建完成${NC}"
}

# 添加文件並提交
commit_files() {
    echo ""
    echo -e "${YELLOW}添加文件到 Git...${NC}"
    echo "----------------------------------------"
    
    # 添加所有文件
    git add .
    
    # 檢查文件數量
    FILE_COUNT=$(git diff --cached --numstat | wc -l)
    echo -e "${GREEN}✓ 準備提交 $FILE_COUNT 個文件${NC}"
    
    # 創建提交
    git commit -m "Initial commit: iMocha Website Clone

- Complete offline website clone
- Fully functional navigation
- Responsive design
- All assets localized (~21MB)
- QA tested and approved

Features:
- Home page with hero section
- Products pages (Talent Acquisition, Management)
- Use Cases with dropdowns
- Pricing information
- Resources and Blog
- Company information
- Mobile responsive
- Dark mode support

Generated by nanobot AI assistant"
    
    echo -e "${GREEN}✓ 提交完成${NC}"
}

# 推送到 GitHub
push_to_github() {
    echo ""
    echo -e "${YELLOW}推送到 GitHub...${NC}"
    echo "----------------------------------------"
    
    # 添加遠程倉庫
    REMOTE_URL="https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    git remote add origin "$REMOTE_URL"
    
    # 重命名分支為 main
    git branch -M main
    
    # 推送
    git push -u origin main --force
    
    echo -e "${GREEN}✓ 推送完成${NC}"
}

# 顯示完成信息
show_completion() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  上傳成功！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "📁 倉庫名稱: ${BLUE}$REPO_NAME${NC}"
    echo -e "🔗 倉庫地址: ${BLUE}https://github.com/$GITHUB_USERNAME/$REPO_NAME${NC}"
    echo -e "🔒 私有倉庫: ${BLUE}$IS_PRIVATE${NC}"
    echo ""
    echo -e "${YELLOW}快速訪問:${NC}"
    echo "  git clone https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    echo ""
    echo -e "${YELLOW}啟動網站:${NC}"
    echo "  cd $REPO_NAME"
    echo "  bash start-server.sh"
    echo ""
}

# 主函數
main() {
    check_required_tools
    get_github_credentials
    create_github_repo
    prepare_local_repo
    commit_files
    push_to_github
    show_completion
}

# 顯示幫助信息
show_help() {
    echo "用法: $0 [倉庫名稱] [GitHub用戶名] [Token] [是否私有]"
    echo ""
    echo "參數:"
    echo "  倉庫名稱  - GitHub 倉庫名稱 (默認: imocha-website-clone)"
    echo "  GitHub用戶名 - 你的 GitHub 用戶名"
    echo "  Token      - GitHub Personal Access Token"
    echo "  是否私有    - true/false (默認: false)"
    echo ""
    echo "示例:"
    echo "  $0                           # 交互式模式"
    echo "  $0 my-repo user token123     # 全參數模式"
    echo "  $0 my-repo user token true   # 創建私有倉庫"
    echo ""
    echo "關於 GitHub Token:"
    echo "  1. 訪問: https://github.com/settings/tokens"
    echo "  2. 生成 Classic Token"
    echo "  3. 勾選 'repo' 權限"
}

# 處理命令行參數
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    show_help
    exit 0
fi

# 運行主程序
main

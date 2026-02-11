# 青銀共創 LINE OA Server - Railway 部署指南

## 部署步驟（約 5 分鐘）

### 1. 建立 Railway 專案
1. 前往 https://railway.app
2. 以 GitHub 帳號登入
3. New Project → Deploy from GitHub repo → 選 `my-first-business`
4. 選擇 `deploy/railway` 資料夾（或把此資料夾內容推到獨立 repo）

### 2. 設定環境變數（在 Railway Dashboard）
```
LINE_CHANNEL_SECRET = ce101f5d1f1a86a45fcb18890fdfc9f3
LINE_CHANNEL_TOKEN  = 8F4qdYGiJYU7s0Msru4RzoisfyeNMXX6BjRl862vwdP...（完整 token）
FORM_URL            = https://your-app.railway.app/form
PDF_URL             = （Google Drive PDF 連結）
WAITLIST_CSV        = /data/waitlist_signups.csv
```

### 3. 部署後取得 URL
- Railway 會給你一個 `https://your-app.railway.app` 網址
- 這個 URL 是永久的，不會因重啟而改變

### 4. 更新 LINE Webhook
部署完成後，AI 會自動：
1. 更新 LINE Webhook URL → `https://your-app.railway.app/webhook`
2. 更新 Rich Menu 的 Form 連結 → `https://your-app.railway.app/form`

### 費用
- Railway 免費方案：每月 $5 美元的 credit，夠用幾個月
- 正式上線後升級到 Starter ($5/月) 有 SLA 保障

## 告訴 AI 你的 Railway URL
部署完成後，把 `https://your-app.railway.app` 貼給小弟，
他會自動更新 LINE Webhook 和 Rich Menu。

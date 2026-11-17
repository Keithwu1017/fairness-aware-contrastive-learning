# 部署展示前端

## 本機

依 README 安裝 Python 3.11 與依賴後，執行 `python app.py`，開啟 http://127.0.0.1:7860。這是 CPU 展示程式，不需 PyTorch、CUDA 或原研究訓練環境。

若 7860 無法使用，可在 PowerShell 執行 `$env:PORT='17860'` 後啟動，改開啟 http://127.0.0.1:17860。macOS / Linux 可執行 `PORT=17860 python app.py`。

## Docker

```bash
docker build -t fairpath-showcase .
docker run --rm -p 127.0.0.1:7860:7860 fairpath-showcase
```

Docker 使用非 root 帳號並綁定容器內 0.0.0.0，以上指令只將主機本機連接埠公開。對外部署時由反向代理處理 HTTPS 與必要的存取控制。可用 `PORT` 指定服務埠、`GRADIO_SERVER_NAME` 指定綁定位址。

## Hugging Face Spaces（可選）

1. 在自己的帳號建立 Space，選擇 Gradio SDK 及 CPU 環境。
2. 上傳本展示檔案（勿包含 `.venv`、私人資料或模型權重）。
3. 在 Space 的 README 最前方加入下列 YAML；SDK 版本與本專案一致：

```yaml
---
title: FAIR-Path Showcase
emoji: 🔬
colorFrom: teal
colorTo: blue
sdk: gradio
sdk_version: 5.49.1
python_version: "3.11"
app_file: app.py
pinned: false
license: agpl-3.0
---
```

4. 設定環境變數 `GRADIO_SERVER_NAME=0.0.0.0`。
5. 等候建置完成，再確認三個頁籤、情境切換、CSV 匯入及還原功能。

本次交付不包含已建立的 Space 或公開服務網址。GitHub Pages 無法直接執行此 Python Gradio 應用。儲存庫可見性與執行服務的可見性分別管理。

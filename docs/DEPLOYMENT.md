# 部署展示前端

## GitHub Pages（公開展示）

公開網址：[FAIR-Path Showcase](https://keithwu1017.github.io/fairness-aware-contrastive-learning/)。

網站來源為 `site/`，不執行 Python、Gradio 或模型推論。圖表、情境切換、CSV 解析及指標計算全在瀏覽器中執行，不需伺服器或 GPU。訪客匯入的檔案只保留於當前分頁記憶體，重新整理即還原示範資料。

儲存庫的 **Settings → Pages → Source** 設為 **GitHub Actions**。`.github/workflows/pages.yml` 在 `main` 的網站內容更新時，執行 JavaScript 測試並發布 `site/`。也可以從 Actions 手動執行 `Deploy public showcase`。

修改公開頁面時編輯 `site/`，提交後等待該工作流程完成。網站使用相對資源路徑，支援 `/<repository>/` 子目錄及 `#results`、`#methods` 深層連結。

GitHub Free 的 Pages 需要公開儲存庫；GitHub Pro 等方案可支援私人來源。網站發布後可供任何人瀏覽。本專案僅公開展示內容、合成彙總資料與前端程式。

本機靜態預覽：`python -m http.server 8000 --directory site`，開啟 http://localhost:8000。

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

未建立 Hugging Face Space。GitHub Pages 使用獨立靜態版，Gradio 版則保留供本機或其他 Python 服務平台使用。

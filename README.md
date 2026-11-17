<div align="center">

# Fairness-aware Contrastive Learning
### 公平性數位病理 AI · 專案成果展示

以 Gradio 呈現研究背景、公開成果與群體效能比較。

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Gradio](https://img.shields.io/badge/Gradio-Showcase-F97316)
![Scope](https://img.shields.io/badge/Scope-Presentation%20Only-0D9488)

[研究來源](https://github.com/hms-dbmi/fairpath) · [方法與範圍](docs/OVERVIEW.md) · [部署說明](docs/DEPLOYMENT.md) · [資料格式](docs/DATA_FORMAT.md)

</div>

## 專案介紹

病理 AI 的平均效能可能掩蓋人口群體間的落差。本專案基於 FAIR-Path 研究，建立易於展示與操作的繁體中文前端，說明公平性感知對比學習的目的，並以群體比較圖表呈現效能與公平性的關係。

**這是獨立實作的成果展示層。** 儲存庫僅提供前端、圖表及彙總資料處理；不包含核心訓練、損失函數、模型權重或患者影像。本版未串接模型推論，啟動不需 GPU。

## 原研究公開成果

| 項目 | 原研究 README 摘要 |
| --- | --- |
| 泛癌種評估範圍 | 20 種癌症 |
| 觀察到的差異緩解 | 88.5% |
| 獨立外部驗證 | 15 個世代 |
| 外部差距縮減 | 91.1% |

來源：[hms-dbmi/fairpath / Overview](https://github.com/hms-dbmi/fairpath#overview)，查核日期 2026-11-17。這些是**原作者公開研究成果**，並非本專案重新驗證或自有模型實驗。百分比不是診斷準確率，其分母與統計定義請參閱原論文。本專案未取得個別任務的原始結果或預訓練權重。

## 展示功能

![Gradio 成果展示介面](assets/overview.webp)

![群體效能與公平性互動面板（合成示範數據）](assets/dashboard.webp)

- **專案概覽**：問題背景、研究成果卡片與來源。
- **互動比較**：切換兩種合成情境，比較 Baseline / Fairness-aware 的 AUROC、TPR、TNR。
- **公平性面板**：顯示 EOpp gap、EBAcc gap 與群體 AUROC 平均。
- **自有結果匯入**：依固定 CSV 格式載入群體彙總資料，顯示來源標籤。
- **方法說明**：保留高階概念與成果邊界，省略核心技術實作。

預設資料為**人工合成**，不是病理模型推論，也不對應真實癌種或患者。情境 A 示意群體差距縮小；情境 B 示意公平性改善時可能存在效能取捨。介面不會依影像或人口屬性產生虛構診斷。

## 快速啟動

使用 Python 3.11：

```bash
git clone https://github.com/Keithwu1017/fairness-aware-contrastive-learning.git
cd fairness-aware-contrastive-learning
python -m venv .venv
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS / Linux：

```bash
source .venv/bin/activate
```

安裝與啟動：

```bash
python -m pip install -r requirements.txt
python app.py
```

開啟 <http://127.0.0.1:7860>。預設僅綁定本機，`share=False`。私人儲存庫的 clone 需 GitHub 存取權限。

## 展示導覽（約 3 分鐘）

1. 「專案概覽」介紹公平性問題與原研究成果。
2. 「互動成果面板」切換 Recall，觀察兩模型的群體差距。
3. 切至情境 B，再看 AUROC，說明公平性與效能需要共同評估。
4. 展開指標定義；需要時匯入已授權的自有彙總結果。
5. 「方法與展示範圍」說明前端與核心研究系統的分工。

## 專案結構

```text
app.py                 Gradio 展示介面
metrics.py             CSV 驗證、展示指標與圖表
data/demo_metrics.csv  明確標示的合成示範資料
docs/                  方法、資料格式與部署說明
tests/                 彙總指標與輸入驗證測試
Dockerfile             CPU 展示容器
requirements.txt       固定展示依賴版本
```

本展示以各群體 AUROC 算術平均呈現摘要，**不能作為整體 pooled AUROC**。不執行顯著性檢定或信賴區間估計；gap 縮小不等同統計上已證明消除偏差。非臨床診斷工具。

## 驗證

```bash
python -m unittest discover -s tests -v
```

GitHub Actions 執行同樣的測試並檢查 Gradio UI 可建立。GitHub 儲存庫承載原始碼，執行中的 Gradio 應用需另行部署；請見 [Docker / Hugging Face Spaces 說明](docs/DEPLOYMENT.md)。

## 致謝與授權

研究概念與成果歸原作者所有：Lin, Shih-Yen; Tsai, Pei-Chen; Su, Fang-Yi; et al. (2025). *Contrastive learning enhances fairness in pathology artificial intelligence systems*. Cell Reports Medicine, 6(12)。完整作者資訊與引用格式見 [原始儲存庫](https://github.com/hms-dbmi/fairpath#citation)。本展示不表示獲原作者或機構背書。

展示程式採 [AGPL-3.0](LICENSE)。未複製原專案的訓練或推論程式；原研究程式另依其原有授權條件提供。

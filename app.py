"""Public Gradio showcase; intentionally independent of private model code."""
import os
from pathlib import Path

import gradio as gr
import pandas as pd

from metrics import DEMO_PATH, load_demo, render, validate

ROOT = Path(__file__).parent
CSS = """
.gradio-container {max-width: 1240px !important; font-family: 'Segoe UI', sans-serif;}
.hero {background:linear-gradient(120deg,#0f172a,#134e4a);border-radius:22px;padding:38px;color:#f8fafc;margin-bottom:18px;}
.hero h1 {color:white;font-size:36px;line-height:1.25;margin:10px 0;}
.hero p {color:#ccfbf1;font-size:16px;max-width:760px;}
.eyebrow {letter-spacing:3px;font-size:12px;color:#5eead4;}
.cards {display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0;}
.card {border:1px solid #cbd5e1;border-radius:16px;padding:20px;background:#f8fafc;color:#334155;}
.card strong {display:block;font-size:32px;color:#0f766e;}
.card small {display:block;margin-top:6px;color:#475569;}
@media(max-width:700px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}.card{padding:14px}.hero{padding:24px}.hero h1{font-size:27px}}
"""


def build_app():
    initial = load_demo()
    first = initial.scenario.iloc[0]
    first_view = render(initial, first, "AUROC", "合成示範數據")
    with gr.Blocks(title="FAIR-Path｜公平性病理 AI 成果展示", theme=gr.themes.Soft(primary_hue="teal"), css=CSS) as demo:
        frame_state = gr.State(initial)
        source_state = gr.State("合成示範數據")
        gr.HTML('''<section class="hero"><div class="eyebrow">FAIRNESS · PATHOLOGY · CONTRASTIVE LEARNING</div>
<h1>讓病理 AI，看見每一個群體。</h1><p>Fairness-aware Contrastive Learning<br>以公平性感知對比學習為出發點，展示模型效能與群體差距的關係。</p></section>''')
        gr.Markdown("**成果展示版** · 基於 [hms-dbmi/FAIR-Path](https://github.com/hms-dbmi/fairpath) 的研究介紹與獨立實作前端。未連接診斷模型，非臨床診斷工具。")
        with gr.Tabs():
            with gr.Tab("01 / 專案概覽"):
                gr.Markdown("## 公平性，也是模型品質的一部分\n模型平均表現良好，仍可能掩蓋不同種族、性別或年齡群體的效能落差。本展示聚焦於如何看見、比較與溝通這些差距。")
                gr.HTML('''<div class="cards"><div class="card"><strong>20</strong>癌症類型<small>原研究涵蓋範圍</small></div><div class="card"><strong>88.5%</strong>觀察到的差異緩解<small>原研究 README 摘要</small></div><div class="card"><strong>15</strong>獨立驗證世代<small>原研究外部驗證</small></div><div class="card"><strong>91.1%</strong>外部差距縮減<small>原研究 README 摘要</small></div></div>''')
                gr.Markdown("上述數字皆為**原研究公開成果**，不是本展示程式重新訓練或驗證所得，也不是診斷準確率。來源：[FAIR-Path README / Overview](https://github.com/hms-dbmi/fairpath#overview)。百分比的分母與統計定義須以原論文為準，不可解讀為每個群體均提升相同比例。")
                with gr.Row():
                    with gr.Column(min_width=300):
                        gr.Markdown("### 研究方法\n以對比學習建立表徵，再進行下游分類微調，目標是兼顧診斷相關訊號與人口群體公平性。")
                    with gr.Column(min_width=300):
                        gr.Markdown("### 本專案交付\n繁體中文成果頁、模型比較圖表、群體落差指標、彙總 CSV 匯入，以及可獨立啟動的輕量 Gradio 前端。")
            with gr.Tab("02 / 互動成果面板"):
                gr.Markdown("## 從平均表現，走向群體比較\n預設內容皆為**人工合成數據**，用於展示操作與指標解讀，與論文數值及實際患者無關。情境 B 刻意保留效能取捨。")
                with gr.Row():
                    scenario = gr.Dropdown(initial.scenario.unique().tolist(), value=first, label="展示情境")
                    metric = gr.Radio(["AUROC", "Recall / TPR", "Specificity / TNR"], value="AUROC", label="效能指標")
                with gr.Row():
                    performance = gr.Plot(first_view[0], label="群體效能")
                    fairness = gr.Plot(first_view[1], label="公平性落差")
                summary = gr.Dataframe(first_view[2], interactive=False, label="指標摘要")
                note = gr.Markdown(first_view[4])
                with gr.Accordion("檢視彙總資料與指標定義", open=False):
                    table = gr.Dataframe(first_view[3], interactive=False, label="目前情境資料")
                    gr.Markdown("**EOpp gap** = max(TPR) − min(TPR)。\n\n**EBAcc gap** = max((TPR + TNR)/2) − min((TPR + TNR)/2)。\n\n二者為此展示採用的群體範圍定義，0 表示觀察值相同；未估計信賴區間或執行 bootstrap。AUROC 衡量排序辨別力，不是準確率。")
                with gr.Accordion("匯入自己的彙總結果", open=False):
                    gr.Markdown("僅上傳已獲授權且無個資的群體彙總資料；請先閱讀 [CSV 格式說明](https://github.com/Keithwu1017/fairness-aware-contrastive-learning/blob/main/docs/DATA_FORMAT.md)。上傳只在本次應用程式工作階段顯示，不會寫入 GitHub。")
                    csv_file = gr.File(label="彙總 CSV（最多 1 MB / 1000 列）", file_types=[".csv"], type="filepath")
                    with gr.Row():
                        import_button = gr.Button("載入彙總結果", variant="primary")
                        reset_button = gr.Button("還原合成示範")
                    status = gr.Markdown()
                    gr.DownloadButton("下載 CSV 格式範例（合成數據）", value=str(DEMO_PATH))

                outputs = [performance, fairness, summary, table, note]

                def refresh(frame, selected, selected_metric, source):
                    return render(frame, selected, selected_metric, source)

                scenario.change(refresh, [frame_state, scenario, metric, source_state], outputs)
                metric.change(refresh, [frame_state, scenario, metric, source_state], outputs)

                def import_csv(path):
                    if not path:
                        raise gr.Error("請先選擇 CSV。")
                    if Path(path).stat().st_size > 1_000_000:
                        raise gr.Error("檔案不可超過 1 MB。")
                    try:
                        data = validate(pd.read_csv(path, encoding="utf-8-sig"))
                    except (ValueError, OSError, UnicodeError) as exc:
                        raise gr.Error(f"CSV 格式有誤：{exc}") from exc
                    choices = data.scenario.unique().tolist()
                    source = "使用者匯入彙總數據（未經本專案驗證）"
                    return (data, source, gr.update(choices=choices, value=choices[0]),
                            "已載入；這些數據的來源與真實性須由提供者確認。", *render(data, choices[0], "AUROC", source), "AUROC")

                def reset():
                    data = load_demo()
                    choices = data.scenario.unique().tolist()
                    return (data, "合成示範數據", gr.update(choices=choices, value=choices[0]),
                            "已還原合成示範。", *render(data, choices[0], "AUROC", "合成示範數據"), "AUROC")

                result_outputs = [frame_state, source_state, scenario, status, *outputs, metric]
                import_button.click(import_csv, [csv_file], result_outputs)
                reset_button.click(reset, [], result_outputs)
            with gr.Tab("03 / 方法與展示範圍"):
                gr.Markdown((ROOT / "docs" / "OVERVIEW.md").read_text(encoding="utf-8"))
        gr.Markdown("---\n**FAIR-Path Showcase** · 原研究：Lin et al., *Cell Reports Medicine* (2025) · [原始研究與程式](https://github.com/hms-dbmi/fairpath) · [本展示儲存庫](https://github.com/Keithwu1017/fairness-aware-contrastive-learning)")
    return demo


if __name__ == "__main__":
    build_app().launch(server_name=os.getenv("GRADIO_SERVER_NAME", "127.0.0.1"),
                       server_port=int(os.getenv("PORT", "7860")), share=False,
                       max_file_size="1mb")

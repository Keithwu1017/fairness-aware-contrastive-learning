"""Gradio application composition and display-only callbacks."""
from pathlib import Path

import gradio as gr
import pandas as pd

from metrics import DEMO_PATH, load_demo, render, validate
from presentation import DASHBOARD_HEADER, FOOTER, HEADER, HERO, METHODS, STATS, summary_cards

ROOT = Path(__file__).parent


def build_app():
    initial = load_demo()
    first = initial.scenario.iloc[0]
    first_view = render(initial, first, "AUROC", "合成示範數據")
    theme = gr.themes.Base(primary_hue="stone", secondary_hue="stone", neutral_hue="stone",
                           font=["Arial", "Microsoft JhengHei", "sans-serif"])
    theme.set(body_background_fill="#f5f4ef", body_background_fill_dark="#f5f4ef",
              body_text_color="#202a26", body_text_color_dark="#202a26",
              block_background_fill="#f9f9f5", block_background_fill_dark="#f9f9f5",
              block_border_color="#dedfd6", block_border_color_dark="#dedfd6",
              input_background_fill="#f9f9f5", input_background_fill_dark="#f9f9f5",
              button_primary_background_fill="#202a26", button_primary_text_color="#ffffff",
              button_primary_background_fill_dark="#202a26", button_primary_text_color_dark="#ffffff")
    with gr.Blocks(title="FAIR-Path — 公平性病理 AI", theme=theme,
                   js=(ROOT / "resize.js").read_text(encoding="utf-8"),
                   css=(ROOT / "ui.css").read_text(encoding="utf-8")) as demo:
        frame_state = gr.State(initial)
        source_state = gr.State("合成示範數據")
        gr.HTML(HEADER)
        with gr.Tabs(elem_id="main-tabs", selected="overview") as tabs:
            with gr.Tab("研究概覽", id="overview"):
                gr.HTML(HERO)
                with gr.Row(elem_id="hero-actions"):
                    explore = gr.Button("探索互動成果  ↗", variant="primary", min_width=150)
                    about = gr.Button("了解研究方法  →", variant="secondary", min_width=150)
                gr.HTML(STATS)
                gr.HTML(METHODS)
            with gr.Tab("互動成果", id="results"):
                gr.HTML(DASHBOARD_HEADER)
                with gr.Row(elem_classes="control-panel"):
                    scenario = gr.Dropdown(initial.scenario.unique().tolist(), value=first, label="評估情境", scale=1, min_width=230)
                    metric = gr.Radio(["AUROC", "Recall / TPR", "Specificity / TNR"], value="AUROC", label="比較指標", scale=1, min_width=280)
                kpis = gr.HTML(summary_cards(first_view[2]), elem_id="summary-kpis")
                with gr.Row(elem_classes="chart-row"):
                    performance = gr.Plot(first_view[0], show_label=False, elem_classes="chart-card", min_width=300)
                    fairness = gr.Plot(first_view[1], show_label=False, elem_classes="chart-card", min_width=300)
                note = gr.Markdown(first_view[4], elem_id="metric-note")
                with gr.Accordion("數據明細與指標定義", open=False, elem_classes="details-accordion"):
                    summary = gr.Dataframe(first_view[2], interactive=False, label="模型指標摘要")
                    table = gr.Dataframe(first_view[3], interactive=False, label="目前情境彙總資料")
                    gr.Markdown("**EOpp gap** = max(TPR) − min(TPR)。**EBAcc gap** = max((TPR + TNR)/2) − min((TPR + TNR)/2)。\n\n使用群體間最大與最小值之差，0 表示觀察值相同。未估計信賴區間；AUROC 衡量排序辨別力，不是準確率。")
                with gr.Accordion("匯入自己的彙總結果", open=False, elem_classes="details-accordion"):
                    gr.Markdown("使用已獲授權且無個資的群體彙總資料。[查看 CSV 格式](https://github.com/Keithwu1017/fairness-aware-contrastive-learning/blob/main/docs/DATA_FORMAT.md) · 上傳內容不會寫入 GitHub。")
                    csv_file = gr.File(label="彙總 CSV · 最多 1 MB / 1000 列", file_types=[".csv"], type="filepath")
                    with gr.Row():
                        import_button = gr.Button("載入彙總結果", variant="primary")
                        reset_button = gr.Button("還原合成示範")
                        gr.DownloadButton("下載 CSV 範例", value=str(DEMO_PATH))
                    status = gr.Markdown()

                def display(frame, selected, selected_metric, source):
                    view = render(frame, selected, selected_metric, source)
                    return (*view, summary_cards(view[2]))

                outputs = [performance, fairness, summary, table, note, kpis]
                scenario.change(display, [frame_state, scenario, metric, source_state], outputs)
                metric.change(display, [frame_state, scenario, metric, source_state], outputs)

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
                            "已載入；這些數據的來源與真實性須由提供者確認。", *display(data, choices[0], "AUROC", source), "AUROC")

                def reset():
                    data = load_demo()
                    choices = data.scenario.unique().tolist()
                    return (data, "合成示範數據", gr.update(choices=choices, value=choices[0]),
                            "已還原合成示範。", *display(data, choices[0], "AUROC", "合成示範數據"), "AUROC")

                result_outputs = [frame_state, source_state, scenario, status, *outputs, metric]
                import_button.click(import_csv, [csv_file], result_outputs)
                reset_button.click(reset, [], result_outputs)
            with gr.Tab("方法與範圍", id="methods"):
                gr.Markdown((ROOT / "docs" / "OVERVIEW.md").read_text(encoding="utf-8"), elem_id="scope-document")
        explore.click(lambda: gr.update(selected="results"), outputs=tabs)
        about.click(lambda: gr.update(selected="methods"), outputs=tabs)
        gr.HTML(FOOTER)
    return demo

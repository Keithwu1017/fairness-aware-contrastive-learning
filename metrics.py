"""Display-only metrics. No training, inference, or significance claims."""
import math
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

DEMO_PATH = Path(__file__).parent / "data" / "demo_metrics.csv"
COLUMNS = ["scenario", "model", "group", "auroc", "tpr", "tnr", "n"]
MODELS = ["Baseline", "Fairness-aware"]


def validate(frame):
    missing = set(COLUMNS) - set(frame.columns)
    if missing:
        raise ValueError("缺少欄位：" + ", ".join(sorted(missing)))
    frame = frame[COLUMNS].copy()
    if frame.empty or len(frame) > 1000:
        raise ValueError("請提供 1–1000 列彙總數據。")
    for col in ["scenario", "model", "group"]:
        if frame[col].isna().any():
            raise ValueError(f"{col} 不可為空。")
        frame[col] = frame[col].astype(str).str.strip()
        if (frame[col].str.len() == 0).any() or (frame[col].str.len() > 80).any():
            raise ValueError(f"{col} 須為 1–80 字元。")
    for col in ["auroc", "tpr", "tnr", "n"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
        if not frame[col].map(lambda x: pd.notna(x) and math.isfinite(x)).all():
            raise ValueError(f"{col} 須為有限數字。")
    if not frame[["auroc", "tpr", "tnr"]].apply(lambda x: x.between(0, 1)).all().all():
        raise ValueError("AUROC、TPR、TNR 必須介於 0 與 1。")
    if not ((frame.n > 0) & (frame.n % 1 == 0)).all():
        raise ValueError("n 須為正整數。")
    if frame.duplicated(["scenario", "model", "group"]).any():
        raise ValueError("同一情境、模型與群體不可重複。")
    for _, part in frame.groupby("scenario"):
        if set(part.model) != set(MODELS):
            raise ValueError("每個情境須同時含 Baseline 與 Fairness-aware。")
        a = part[part.model == MODELS[0]].set_index("group")
        b = part[part.model == MODELS[1]].set_index("group")
        if len(a) < 2 or len(a) > 12 or set(a.index) != set(b.index):
            raise ValueError("兩模型須有相同的 2–12 個群體。")
        if not a.n.sort_index().equals(b.n.sort_index()):
            raise ValueError("同群體的兩模型 n 必須相同，才能比較同一評估群體。")
    return frame


def load_demo():
    return validate(pd.read_csv(DEMO_PATH))


def summarize(part):
    rows = []
    for model in MODELS:
        data = part[part.model == model]
        bacc = (data.tpr + data.tnr) / 2
        rows.append([model, data.auroc.mean(), data.tpr.max() - data.tpr.min(),
                     bacc.max() - bacc.min()])
    return pd.DataFrame(rows, columns=["模型", "群體 AUROC 平均", "EOpp gap", "EBAcc gap"])


def render(frame, scenario, metric, source):
    part = frame[frame.scenario == scenario].copy()
    if part.empty:
        raise ValueError("找不到此情境，請重新選擇。")
    summary = summarize(part)
    field = {"AUROC": "auroc", "Recall / TPR": "tpr", "Specificity / TNR": "tnr"}[metric]
    fig = go.Figure()
    for model, color in zip(MODELS, ["#94a3b8", "#0d9488"]):
        data = part[part.model == model].sort_values("group")
        fig.add_bar(name=model, x=data.group, y=data[field], marker_color=color,
                    hovertemplate="%{x}<br>" + metric + ": %{y:.3f}<extra>%{fullData.name}</extra>")
    fig.update_layout(template="plotly_white", barmode="group", height=380,
                      title=f"{source}｜{metric}", yaxis=dict(range=[0, 1], title=metric),
                      legend=dict(orientation="h", y=1.12), margin=dict(l=40,r=20,t=85,b=40))
    gap = go.Figure()
    for row, color in zip(summary.values, ["#94a3b8", "#0d9488"]):
        gap.add_bar(name=row[0], x=["EOpp gap", "EBAcc gap"], y=[row[2], row[3]], marker_color=color)
    gap.update_layout(template="plotly_white", barmode="group", height=380,
                      title=f"{source}｜群體落差（越低越好）", yaxis=dict(range=[0, 1]),
                      legend=dict(orientation="h", y=1.12), margin=dict(l=40,r=20,t=85,b=40))
    delta = summary.iloc[0, 2] - summary.iloc[1, 2]
    note = (f"**數據來源：{source}** · EOpp gap 變化：{delta * 100:+.1f} 個百分點（正值表示縮小）。\n\n"
            "AUROC 欄位是各群體 AUROC 的算術平均，並非整體 pooled AUROC。"
            "此面板未執行統計顯著性檢定；差距縮小不等同已證明消除偏差。")
    return fig, gap, summary.round(4), part, note

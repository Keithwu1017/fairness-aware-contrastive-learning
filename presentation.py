"""Presentation markup, independent of the research model."""
import math


def representation_visual():
    dots = []
    # Deterministic geometric illustration, not observed embeddings.
    for cluster, (cx, cy) in enumerate([(137, 126), (311, 126)]):
        for i in range(44):
            angle = i * 2.39996
            radius = math.sqrt((i + 1) / 44) * 58
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius * .74
            color = "#c1d1a5" if i % 2 else "#dc9876"
            dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2.3 + (i % 3) * .55}" fill="{color}" opacity="{.55 + (i % 4) * .12}"/>')
    return '''<div class="visual"><div class="visual-top"><span>REPRESENTATION SPACE</span><span>01 — Concept illustration</span></div>
<svg viewBox="0 0 448 246" role="img" aria-label="對比學習表徵概念示意：依診斷訊號聚合特徵，兩種群體在群集內交錯；非實驗結果">
<defs><pattern id="dot-grid" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#96ac8a" opacity=".17"/></pattern></defs>
<rect width="448" height="246" fill="url(#dot-grid)"/>
<path d="M34 213H421M34 213V27" stroke="#95ab862d" fill="none"/>
<ellipse cx="137" cy="126" rx="78" ry="64" stroke="#c1d1a5" stroke-opacity=".3" stroke-dasharray="3 5" fill="#c1d1a5" fill-opacity=".035"/>
<ellipse cx="311" cy="126" rx="78" ry="64" stroke="#c1d1a5" stroke-opacity=".3" stroke-dasharray="3 5" fill="#c1d1a5" fill-opacity=".035"/>
<path d="M202 126h42m-5-4 5 4-5 4" stroke="#c7d4bc" stroke-opacity=".6" fill="none"/>
''' + ''.join(dots) + '''<text x="137" y="33" fill="#bfceb5" text-anchor="middle" font-size="9" letter-spacing="1.5">CLASS 01</text><text x="311" y="33" fill="#bfceb5" text-anchor="middle" font-size="9" letter-spacing="1.5">CLASS 02</text>
<text x="225" y="239" fill="#91a486" text-anchor="middle" font-size="9" letter-spacing="1">CLINICALLY RELEVANT FEATURES</text></svg>
<div class="visual-bottom"><div class="visual-legend"><span><i class="legend-dot" style="background:#c1d1a5"></i>群體 A</span><span><i class="legend-dot" style="background:#dc9876"></i>群體 B</span></div><span>概念示意 · 非實驗數據</span></div></div>'''


HEADER = '''<header class="brandbar"><div class="brand"><span class="brandmark" aria-hidden="true"><i></i><i></i><i></i><i></i></span>FAIR-Path<span class="brandtag">RESEARCH SHOWCASE</span></div><div class="brandlinks"><span class="projectstamp"><i class="statusdot"></i>公平性病理 AI</span><a href="https://github.com/hms-dbmi/fairpath" target="_blank" rel="noopener noreferrer">原始研究 ↗</a><a href="https://github.com/Keithwu1017/fairness-aware-contrastive-learning" target="_blank" rel="noopener noreferrer">GitHub ↗</a></div></header>'''
HERO = '''<section class="hero-layout"><div class="hero-copy"><div class="eyebrow">FAIRNESS-AWARE CONTRASTIVE LEARNING</div><h1>好的病理 AI，<br>應該<em>看見每個群體。</em></h1><p class="hero-deck">讓診斷訊號成為焦點，讓人口偏差退居背景。<br>探索對比學習如何回應病理 AI 的公平性挑戰，<br>看見平均效能背後，容易被忽略的群體差距。</p><div class="hero-caption">PATHOLOGY × REPRESENTATION LEARNING × EQUITY</div></div>''' + representation_visual() + '</section>'
STATS = '''<section class="research-stats" aria-label="原研究成果摘要"><div class="stat"><div class="stat-key">01 / PAN-CANCER</div><strong>20</strong><p>癌症類型，跨癌種評估</p></div><div class="stat"><div class="stat-key">02 / DISPARITY MITIGATION</div><strong>88.5<span>%</span></strong><p>觀察到的效能差異緩解</p></div><div class="stat"><div class="stat-key">03 / EXTERNAL VALIDATION</div><strong>15</strong><p>獨立外部驗證世代</p></div><div class="stat"><div class="stat-key">04 / GAP REDUCTION</div><strong>91.1<span>%</span></strong><p>外部驗證差距縮減</p></div></section><div class="source-line">原研究公開成果，非本展示重新驗證。百分比不是診斷準確率；統計定義與分母以原論文為準。<a href="https://github.com/hms-dbmi/fairpath#overview" target="_blank" rel="noopener noreferrer">資料來源 ↗</a></div>'''
METHODS = '''<section><div class="section-heading"><div><div class="kicker">THE IDEA BEHIND THE RESEARCH</div><h2>從辨識疾病，到兼顧公平。</h2></div><p>以兩階段學習建立表徵與分類能力，<br>再透過群體評估，看見模型表現的全貌。</p></div><div class="method-grid">
<article class="method-card"><span class="step">01 / REPRESENT</span><svg class="method-icon" viewBox="0 0 28 28" fill="none" stroke="currentColor"><rect x="3" y="3" width="8" height="8"/><rect x="16" y="3" width="8" height="8"/><rect x="3" y="16" width="8" height="8"/><rect x="16" y="16" width="8" height="8"/></svg><h3>學習病理表徵</h3><p>從病理影像圖塊中提取視覺特徵，<br>讓模型聚焦與診斷相關的訊號。</p></article>
<article class="method-card"><span class="step">02 / CONTRAST</span><svg class="method-icon" viewBox="0 0 28 28" fill="none" stroke="currentColor"><circle cx="8" cy="14" r="5"/><circle cx="21" cy="8" r="3"/><circle cx="21" cy="21" r="3"/><path d="m12 12 6-3m-6 8 6 3"/></svg><h3>減少群體偏差</h3><p>導入公平性感知對比學習，<br>兼顧疾病辨別與人口群體公平性。</p></article>
<article class="method-card"><span class="step">03 / EVALUATE</span><svg class="method-icon" viewBox="0 0 28 28" fill="none" stroke="currentColor"><path d="M3 24h23M7 20v-8m7 8V4m7 16V8" stroke-width="2"/></svg><h3>看見效能全貌</h3><p>同時比較預測效能與群體差距，<br>避免平均數掩蓋弱勢群體的表現。</p></article></div></section><div class="bottom-note">本專案是獨立的研究成果展示前端，未連接診斷模型。互動面板使用合成示範數據，也可匯入自己的群體彙總結果。非臨床診斷工具。</div>'''
DASHBOARD_HEADER = '''<div class="dashboard-heading"><div><div class="eyebrow">EXPLORE THE RESULTS</div><h1>平均之外，看見差距。</h1><p>比較兩種模型的群體效能，探索公平性與預測能力之間的關係。</p></div><div class="data-badge"><i></i>互動展示 · 預設為合成數據</div></div>'''
FOOTER = '''<footer class="site-footer"><div><strong>FAIR-Path</strong> &nbsp; / &nbsp; Fairness in every prediction.<br>Research showcase · Based on Lin et al., Cell Reports Medicine, 2025.</div><div class="footer-links"><span>非臨床診斷工具</span><a href="https://github.com/hms-dbmi/fairpath#citation" target="_blank" rel="noopener noreferrer">引用研究 ↗</a><a href="https://github.com/Keithwu1017/fairness-aware-contrastive-learning" target="_blank" rel="noopener noreferrer">Source code ↗</a></div></footer>'''


def summary_cards(summary):
    baseline, aware = summary.iloc[0], summary.iloc[1]
    gap_change = (baseline.iloc[2] - aware.iloc[2]) * 100
    return f'''<div class="summary-cards"><div class="summary-card"><div class="summary-label">群體 AUROC 平均</div><div class="summary-value">{aware.iloc[1]:.3f}<span>Fairness-aware</span></div><div class="summary-meta">Baseline {baseline.iloc[1]:.3f} · 非 pooled AUROC</div></div><div class="summary-card"><div class="summary-label">EOpp gap · 越低越好</div><div class="summary-value">{aware.iloc[2]:.3f}<span>← {baseline.iloc[2]:.3f}</span></div><div class="summary-meta">召回率的群體間落差</div></div><div class="summary-card"><div class="summary-label">EOpp gap 縮減</div><div class="summary-value">{gap_change:+.1f}<span>個百分點</span></div><div class="summary-meta">觀察值變化，未執行統計顯著性檢定</div></div></div>'''

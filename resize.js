() => {
  // Gradio 5 mounts hidden tab charts before their final size is known.
  // Notify Plotly's responsive handler when a chart becomes visible or resizes.
  const watched = new WeakSet();
  let resizeTimer;
  let scanQueued = false;
  const sizes = new ResizeObserver(entries => {
    if (!entries.some(entry => entry.contentRect.width > 0 && entry.contentRect.height > 0)) return;
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => window.dispatchEvent(new Event('resize')), 80);
  });
  const scan = () => {
    scanQueued = false;
    document.querySelectorAll('[data-testid="plotly"]').forEach(chart => {
      if (watched.has(chart)) return;
      watched.add(chart);
      sizes.observe(chart);
    });
  };
  new MutationObserver(() => {
    if (scanQueued) return;
    scanQueued = true;
    requestAnimationFrame(scan);
  }).observe(document.body, {childList: true, subtree: true});
  scan();
}

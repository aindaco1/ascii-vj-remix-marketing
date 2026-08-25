(() => {
  const layer = document.querySelector('canvas.ascii-art-background');
  const context = layer?.getContext('2d', { alpha: true });
  if (!layer || !context) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const ramp = ' .,:;irsXA253hMHGS#9B&@';
  const fields = {};
  let columns = 0;
  let rows = 0;
  let cellWidth = 8;
  let lineHeight = 15;
  let lastFrame = 0;
  let frameRequest = 0;
  let resizeRequest = 0;

  function trigField(name, size) {
    fields[`${name}Sin`] = new Float32Array(size);
    fields[`${name}Cos`] = new Float32Array(size);
  }

  function cachePhase(name, index, phase) {
    fields[`${name}Sin`][index] = Math.sin(phase);
    fields[`${name}Cos`][index] = Math.cos(phase);
  }

  function shiftedSine(name, index, phase) {
    return fields[`${name}Sin`][index] * phase.cos +
      fields[`${name}Cos`][index] * phase.sin;
  }

  function configure() {
    const style = window.getComputedStyle(layer);
    const fontSize = parseFloat(style.fontSize) || 14;
    const pixelRatio = Math.min(window.devicePixelRatio || 1, 1.5);
    const bounds = layer.getBoundingClientRect();

    layer.width = Math.ceil(bounds.width * pixelRatio);
    layer.height = Math.ceil(bounds.height * pixelRatio);
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    context.font = `${style.fontWeight} ${fontSize}px ${style.fontFamily}`;
    context.fillStyle = style.color;
    context.textBaseline = 'top';
    if ('letterSpacing' in context) context.letterSpacing = style.letterSpacing;

    cellWidth = Math.max(context.measureText('M').width + fontSize * .08, fontSize * .68);
    lineHeight = fontSize * 1.08;
    columns = Math.ceil(bounds.width / cellWidth);
    rows = Math.ceil(bounds.height / lineHeight);

    const size = columns * rows;
    fields.envelope = new Float32Array(size);
    ['tunnel', 'diagonal', 'scan', 'interference'].forEach((name) => trigField(name, size));

    for (let y = 0; y < rows; y += 1) {
      const normalizedY = y / Math.max(rows - 1, 1);
      for (let x = 0; x < columns; x += 1) {
        const normalizedX = x / Math.max(columns - 1, 1);
        const centerX = normalizedX - .5;
        const centerY = normalizedY - .5;
        const radius = Math.sqrt(centerX * centerX * 1.8 + centerY * centerY);
        const index = y * columns + x;

        fields.envelope[index] = Math.max(0, 1 - radius * 1.35);
        cachePhase('tunnel', index, radius * 38);
        cachePhase('diagonal', index, normalizedX * 11 + normalizedY * 17);
        cachePhase('scan', index, normalizedY * 46 + Math.PI / 2);
        cachePhase('interference', index, (normalizedX - normalizedY) * 22);
      }
    }
  }

  function glyph(value) {
    const clamped = Math.max(0, Math.min(1, value));
    return ramp[Math.floor(clamped * (ramp.length - 1))];
  }

  function render(time) {
    const wave = ((time % 12000) / 12000) * Math.PI * 2;
    const phase = (value) => ({ sin: Math.sin(value), cos: Math.cos(value) });
    const phases = {
      tunnel: phase(-wave * 3.4),
      diagonal: phase(wave * 2.2),
      scan: phase(-wave * 5),
      interference: phase(wave * 1.7)
    };

    context.clearRect(0, 0, layer.width, layer.height);
    for (let y = 0; y < rows; y += 1) {
      let line = '';
      for (let x = 0; x < columns; x += 1) {
        const index = y * columns + x;
        const value = (
          shiftedSine('tunnel', index, phases.tunnel) * .46 +
          shiftedSine('diagonal', index, phases.diagonal) * .28 +
          shiftedSine('scan', index, phases.scan) * .16 +
          shiftedSine('interference', index, phases.interference) * .22
        ) * fields.envelope[index] + .36;
        line += glyph(value);
      }
      context.fillText(line, 0, y * lineHeight);
    }
  }

  function tick(time) {
    if (!document.hidden && time - lastFrame > 80) {
      render(time);
      lastFrame = time;
    }
    frameRequest = window.requestAnimationFrame(tick);
  }

  function start() {
    window.cancelAnimationFrame(frameRequest);
    configure();
    render(0);
    if (!reduceMotion.matches) frameRequest = window.requestAnimationFrame(tick);
  }

  function scheduleResize() {
    window.cancelAnimationFrame(resizeRequest);
    resizeRequest = window.requestAnimationFrame(start);
  }

  start();
  document.fonts?.ready.then(scheduleResize);
  window.addEventListener('resize', scheduleResize, { passive: true });
  if (typeof reduceMotion.addEventListener === 'function') {
    reduceMotion.addEventListener('change', start);
  } else {
    reduceMotion.addListener(start);
  }
})();

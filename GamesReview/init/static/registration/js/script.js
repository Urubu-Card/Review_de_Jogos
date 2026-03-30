/* =====================================================
   PS2 INTRO — Colunas de luz animadas no canvas
   ===================================================== */

(function () {
  const canvas = document.getElementById('ps2-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  const BLUE = '#4fc3f7';
  const BLUE_DIM = 'rgba(79,195,247,0.18)';
  const COL_W = 2;        // largura de cada coluna
  const GAP   = 22;       // espaço entre colunas
  const STEP  = GAP + COL_W;
  const SPEED_MIN = 0.4;
  const SPEED_MAX = 2.2;
  const GLOW_CHANCE = 0.015; // chance por frame de uma coluna "acordar"

  let W, H, cols = [];

  function resize() {
    W = canvas.width  = window.innerWidth;
    H = canvas.height = window.innerHeight;
    buildCols();
  }

  function buildCols() {
    cols = [];
    const count = Math.floor(W / STEP) + 1;
    for (let i = 0; i < count; i++) {
      cols.push(makeCol(i * STEP, true));
    }
  }

  function makeCol(x, init) {
    const h = randomBetween(80, H * 0.85);
    return {
      x,
      y: init ? randomBetween(-H, H) : -h - randomBetween(0, 300),
      height: h,
      speed: randomBetween(SPEED_MIN, SPEED_MAX),
      bright: Math.random() < 0.12,   // algumas colunas são brilhantes
      opacity: randomBetween(0.08, 0.55),
      glowing: false,
      glowTimer: 0,
    };
  }

  function randomBetween(a, b) {
    return a + Math.random() * (b - a);
  }

  // ---- animação de "glow" ocasional (tipo PS2 piscando) ----
  function maybeTriggerGlow() {
    cols.forEach(c => {
      if (!c.glowing && Math.random() < GLOW_CHANCE) {
        c.glowing  = true;
        c.glowTimer = 0;
      }
    });
  }

  function drawCol(c) {
    const glowProgress = c.glowing
      ? Math.sin((c.glowTimer / 60) * Math.PI)
      : 0;

    const baseAlpha = c.bright
      ? c.opacity * (0.7 + 0.3 * glowProgress)
      : c.opacity * (0.5 + 0.5 * glowProgress);

    // gradiente vertical: aparecer no topo, desaparecer na base
    const grad = ctx.createLinearGradient(c.x, c.y, c.x, c.y + c.height);
    grad.addColorStop(0,   `rgba(79,195,247,0)`);
    grad.addColorStop(0.1, `rgba(79,195,247,${(baseAlpha * 0.5).toFixed(3)})`);
    grad.addColorStop(0.5, `rgba(79,195,247,${baseAlpha.toFixed(3)})`);
    grad.addColorStop(0.9, `rgba(79,195,247,${(baseAlpha * 0.6).toFixed(3)})`);
    grad.addColorStop(1,   `rgba(79,195,247,0)`);

    ctx.fillStyle = grad;
    ctx.fillRect(c.x, c.y, COL_W, c.height);

    // ponta brilhante no topo
    if (c.bright || c.glowing) {
      const tipAlpha = 0.7 + 0.3 * glowProgress;
      ctx.fillStyle = `rgba(224,244,255,${tipAlpha.toFixed(2)})`;
      ctx.fillRect(c.x, c.y, COL_W, 4);
    }
  }

  function tick() {
    ctx.clearRect(0, 0, W, H);

    // fundo levemente azul escuro
    ctx.fillStyle = 'rgba(1,6,15,0.0)';
    ctx.fillRect(0, 0, W, H);

    maybeTriggerGlow();

    cols.forEach(c => {
      c.y += c.speed;

      if (c.glowing) {
        c.glowTimer++;
        if (c.glowTimer >= 60) c.glowing = false;
      }

      // resetar quando sai da tela
      if (c.y > H + 50) {
        Object.assign(c, makeCol(c.x, false));
      }

      drawCol(c);
    });

    requestAnimationFrame(tick);
  }

  window.addEventListener('resize', resize);
  resize();
  tick();

  // =====================================================
  //  Injetar wrappers de label + ícone em todos os inputs
  // =====================================================
  const iconMap = {
    'username':    { icon: '▷', label: 'Usuário' },
    'email':       { icon: '◈', label: 'E-mail' },
    'senha':       { icon: '◉', label: 'Senha' },
    'foto_perfil': { icon: '◧', label: 'Foto de Perfil' },
    'bio':         { icon: '≡', label: 'Bio' },
  };

  // Tenta identificar o campo pelo name ou id
  document.querySelectorAll('.user-pass').forEach(div => {
    const el = div.querySelector('input, textarea, select');
    if (!el) return;

    const key = Object.keys(iconMap).find(k =>
      (el.name && el.name.toLowerCase().includes(k)) ||
      (el.id   && el.id.toLowerCase().includes(k))
    );

    const info = key ? iconMap[key] : { icon: '▷', label: el.name || el.id || '' };

    // Adiciona placeholder se não tiver
    if (!el.placeholder) el.placeholder = info.label;

    // Cria label
    const lbl = document.createElement('label');
    lbl.textContent = info.label;
    if (el.id) lbl.htmlFor = el.id;

    // Wrap o input em .input-wrap
    const wrap = document.createElement('div');
    wrap.className = 'input-wrap';
    el.parentNode.insertBefore(wrap, el);
    wrap.appendChild(el);

    // Ícone
    const icon = document.createElement('span');
    icon.className = 'input-icon' + (el.tagName === 'TEXTAREA' ? ' icon-top' : '');
    icon.textContent = info.icon;
    wrap.appendChild(icon);

    // Insere label antes do wrap
    div.insertBefore(lbl, wrap);
  });

  // =====================================================
  //  Efeito de digitação no título
  // =====================================================
  const h1 = document.querySelector('.card h1');
  if (h1) {
    const original = h1.textContent.trim();
    h1.textContent = '';
    let i = 0;
    const type = () => {
      if (i <= original.length) {
        h1.textContent = original.slice(0, i) + (i < original.length ? '█' : '');
        i++;
        setTimeout(type, 70 + Math.random() * 40);
      }
    };
    setTimeout(type, 600);
  }

  // =====================================================
  //  Adiciona logo PS2 estilizado acima do form
  // =====================================================
  const card = document.querySelector('.card');
  if (card) {
    const logo = document.createElement('div');
    logo.className = 'ps2-logo';
    logo.innerHTML = '<span>PS2</span>';
    card.insertBefore(logo, card.firstChild);
  }
})();
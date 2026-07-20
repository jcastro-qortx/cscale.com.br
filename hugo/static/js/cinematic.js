/* ============================================================
   CoreScale — narrativa cinematográfica controlada por rolagem
   GSAP + ScrollTrigger + Lenis (todos servidos localmente).
   Regras:
   - Sem JS o conteúdo permanece 100% visível (estados iniciais
     de animação são definidos aqui, nunca no CSS).
   - prefers-reduced-motion: nada de smooth scroll, pin ou scrub.
   - Mobile (<1000px): sem pin e sem vídeo; reveals leves apenas.
   ============================================================ */
(function () {
  'use strict';
  if (!window.gsap || !window.ScrollTrigger) { return; }

  var gsap = window.gsap;
  var ScrollTrigger = window.ScrollTrigger;
  gsap.registerPlugin(ScrollTrigger);

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var HEADER_OFFSET = 84;

  /* ---------- Lenis (somente sem movimento reduzido) ---------- */
  var lenis = null;
  if (!reduced && window.Lenis) {
    lenis = new window.Lenis({ lerp: 0.11, wheelMultiplier: 1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);
  }

  function scrollToTarget(target, immediate) {
    if (lenis) {
      lenis.scrollTo(target, { offset: -HEADER_OFFSET, immediate: !!immediate, duration: 1.15 });
    } else if (typeof target !== 'number') {
      var el = typeof target === 'string' ? document.querySelector(target) : target;
      if (el) {
        var y = el.getBoundingClientRect().top + window.pageYOffset - HEADER_OFFSET;
        window.scrollTo(0, y);
      }
    }
  }

  /* Âncoras internas (header, CTAs, capítulos) */
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href*="#"]') : null;
    if (!a) { return; }
    var url = new URL(a.href, window.location.href);
    if (url.origin !== window.location.origin || url.pathname !== window.location.pathname || !url.hash) { return; }
    var el = document.querySelector(url.hash);
    if (!el) { return; }
    e.preventDefault();
    history.pushState(null, '', url.hash);
    scrollToTarget(el, false);
  });

  /* ---------- Hero: animação de entrada ---------- */
  var desktopMQ = window.matchMedia('(min-width: 1000px) and (pointer: fine)');
  if (!reduced && desktopMQ.matches) {
    var heroSection = document.querySelector('.cine-hero');
    if (heroSection) {
      var leftCol = heroSection.querySelector('.rm-hero > div:first-child');
      var rightCol = heroSection.querySelector('.rm-hero > div:last-child');
      if (leftCol) {
        gsap.fromTo(leftCol.children,
          { opacity: 0, y: 35 },
          { opacity: 1, y: 0, duration: 0.85, ease: 'power2.out', stagger: 0.1, delay: 0.2 }
        );
      }
      if (rightCol && rightCol !== leftCol) {
        gsap.fromTo(rightCol,
          { opacity: 0, x: 50, scale: 0.96 },
          { opacity: 1, x: 0, scale: 1, duration: 1, ease: 'power2.out', delay: 0.5 }
        );
      }
    }
  }

  /* ---------- Hero: vídeo apenas em desktop sem movimento reduzido ---------- */
  var heroVideo = document.querySelector('[data-cine-video]');
  var saveData = navigator.connection && navigator.connection.saveData;
  if (heroVideo && !reduced && desktopMQ.matches && !saveData) {
    var webm = heroVideo.getAttribute('data-src-webm');
    var mp4 = heroVideo.getAttribute('data-src-mp4');
    var src = (webm && heroVideo.canPlayType('video/webm; codecs="vp9"')) ? webm
      : ((mp4 && heroVideo.canPlayType('video/mp4')) ? mp4 : null);
    if (src) {
      heroVideo.preload = 'auto';
      heroVideo.src = src;
      heroVideo.muted = true;
      heroVideo.setAttribute('playsinline', '');
      heroVideo.addEventListener('canplay', function onCanPlay() {
        heroVideo.removeEventListener('canplay', onCanPlay);
        heroVideo.classList.add('is-ready');
        var p = heroVideo.play();
        if (p && p.catch) { p.catch(function () { /* autoplay bloqueado: poster permanece */ }); }
      });
      /* sem loop: o último quadro (estável) permanece como fundo */
    }
  }

  /* ---------- Campo neural do hero (cloud + IA, decorativo) ---------- */
  function createNeuralField(canvas) {
    var ctx = canvas.getContext('2d');
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var small = window.matchMedia('(max-width: 999px)').matches;
    var N = small ? 36 : 72;
    var K = 3; /* vizinhos conectados por nó */
    var W = 0, H = 0, nodes = [], edges = [], pulses = [];
    var running = false, rafId = 0, t = 0;

    /* sprite de brilho pré-renderizado (evita shadowBlur por frame) */
    function makeGlow(color) {
      var s = document.createElement('canvas'); s.width = s.height = 32;
      var g = s.getContext('2d');
      var grad = g.createRadialGradient(16, 16, 0, 16, 16, 16);
      grad.addColorStop(0, color); grad.addColorStop(1, 'rgba(0,0,0,0)');
      g.fillStyle = grad; g.fillRect(0, 0, 32, 32);
      return s;
    }
    var glowAmber = makeGlow('rgba(255,163,44,0.9)');
    var glowCyan = makeGlow('rgba(120,200,255,0.8)');

    function build() {
      var r = canvas.getBoundingClientRect();
      W = Math.max(1, r.width); H = Math.max(1, r.height);
      canvas.width = Math.floor(W * dpr); canvas.height = Math.floor(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      nodes = []; edges = []; pulses = [];
      for (var i = 0; i < N; i++) {
        /* densidade maior à direita/baixo, longe do título */
        var bias = Math.pow(Math.random(), small ? 1 : 0.62);
        nodes.push({
          x: W * (small ? Math.random() : (0.18 + bias * 0.82)),
          y: H * (0.12 + Math.random() * 0.82),
          ph: Math.random() * Math.PI * 2,
          amp: 4 + Math.random() * 9,
          sp: 0.003 + Math.random() * 0.004,
          hot: Math.random() < 0.45,
          heat: 0
        });
      }
      /* K vizinhos mais próximos */
      for (var a = 0; a < N; a++) {
        var d = [];
        for (var b = 0; b < N; b++) {
          if (a === b) { continue; }
          var dx = nodes[a].x - nodes[b].x, dy = nodes[a].y - nodes[b].y;
          d.push([dx * dx + dy * dy, b]);
        }
        d.sort(function (u, v) { return u[0] - v[0]; });
        for (var k = 0; k < K; k++) {
          var pair = a < d[k][1] ? a + '-' + d[k][1] : d[k][1] + '-' + a;
          if (!edges.some(function (e) { return e.id === pair; })) {
            edges.push({ id: pair, a: a, b: d[k][1] });
          }
        }
      }
    }

    function nx(n) { return n.x + Math.cos(n.ph) * n.amp; }
    function ny(n) { return n.y + Math.sin(n.ph * 1.3) * n.amp; }

    function spawnPulse(fromNode) {
      var out = edges.filter(function (e) { return e.a === fromNode || e.b === fromNode; });
      if (!out.length) { return; }
      var e = out[Math.floor(Math.random() * out.length)];
      pulses.push({ e: e, from: fromNode, p: 0, v: 0.008 + Math.random() * 0.010 });
    }

    function step() {
      if (!running) { return; }
      t += 1;
      ctx.clearRect(0, 0, W, H);
      var i, n, e, a, b;
      for (i = 0; i < nodes.length; i++) { n = nodes[i]; n.ph += n.sp; n.heat *= 0.965; }
      /* arestas */
      ctx.lineWidth = 1;
      for (i = 0; i < edges.length; i++) {
        e = edges[i]; a = nodes[e.a]; b = nodes[e.b];
        var heat = Math.max(a.heat, b.heat);
        ctx.strokeStyle = 'rgba(130,180,255,' + (0.06 + heat * 0.22) + ')';
        ctx.beginPath(); ctx.moveTo(nx(a), ny(a)); ctx.lineTo(nx(b), ny(b)); ctx.stroke();
      }
      /* pulsos de inferência */
      for (i = pulses.length - 1; i >= 0; i--) {
        var p = pulses[i]; p.p += p.v;
        var A = nodes[p.e.a === p.from ? p.e.a : p.e.b];
        var B = nodes[p.e.a === p.from ? p.e.b : p.e.a];
        if (p.p >= 1) {
          var target = p.e.a === p.from ? p.e.b : p.e.a;
          nodes[target].heat = 1;
          if (Math.random() < 0.5 && pulses.length < 26) { spawnPulse(target); } /* propaga */
          pulses.splice(i, 1);
          continue;
        }
        var x = nx(A) + (nx(B) - nx(A)) * p.p;
        var y = ny(A) + (ny(B) - ny(A)) * p.p;
        ctx.drawImage(glowAmber, x - 7, y - 7, 14, 14);
      }
      /* nós */
      for (i = 0; i < nodes.length; i++) {
        n = nodes[i];
        var breathe = 0.5 + 0.5 * Math.sin(n.ph * 2);
        var size = 5 + breathe * 3 + n.heat * 10;
        ctx.globalAlpha = 0.35 + breathe * 0.3 + n.heat * 0.35;
        ctx.drawImage(n.hot ? glowAmber : glowCyan, nx(n) - size / 2, ny(n) - size / 2, size, size);
        ctx.globalAlpha = 1;
      }
      /* novo estímulo periódico */
      if (t % 52 === 0 && pulses.length < 18) { spawnPulse(Math.floor(Math.random() * nodes.length)); }
      rafId = window.requestAnimationFrame(step);
    }

    window.addEventListener('resize', function () { if (running) { build(); } });
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { window.cancelAnimationFrame(rafId); }
      else if (running) { rafId = window.requestAnimationFrame(step); }
    });
    build();
    return {
      start: function () { if (!running) { running = true; rafId = window.requestAnimationFrame(step); } },
      stop: function () { running = false; window.cancelAnimationFrame(rafId); }
    };
  }

  var neuralCanvas = document.querySelector('.cine-neural');
  if (neuralCanvas && !reduced && 'IntersectionObserver' in window) {
    var field = createNeuralField(neuralCanvas);
    var hero = document.querySelector('.cine-hero');
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { en.isIntersecting ? field.start() : field.stop(); });
    }, { threshold: 0.05 }).observe(hero || neuralCanvas);
  }

  /* ---------- Sistema de partículas do palco (decorativo) ---------- */
  function createParticles(canvas) {
    var ctx = canvas.getContext('2d');
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var running = false, rafId = 0, mode = 0, W = 0, H = 0;
    var COUNT = 90;
    var parts = [];

    function resize() {
      var r = canvas.getBoundingClientRect();
      W = Math.max(1, Math.floor(r.width)); H = Math.max(1, Math.floor(r.height));
      canvas.width = Math.floor(W * dpr); canvas.height = Math.floor(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function reset(p) {
      p.x = -20 - Math.random() * W * 0.25;
      p.lane = Math.random();
      p.y = H * (0.30 + p.lane * 0.48);
      p.v = 0.6 + Math.random() * 1.5;
      p.r = 0.8 + Math.random() * 1.7;
      p.tw = Math.random() * Math.PI * 2;
      p.hot = Math.random() < 0.75; /* âmbar vs azul-claro */
      p.anom = false;
    }
    for (var i = 0; i < COUNT; i++) { var p = {}; reset(p); p.x = Math.random() * W; parts.push(p); }

    var anomaly = { t: 0, active: false, x: 0, y: 0, phase: 0 };

    function step() {
      if (!running) { return; }
      ctx.clearRect(0, 0, W, H);
      var speedK = [1.15, 0.55, 0.8, 0.7, 0.9, 0.4][mode] || 1;
      var visible = mode === 3 ? 54 : (mode === 5 ? 44 : COUNT);
      for (var i = 0; i < COUNT; i++) {
        var p = parts[i];
        if (i >= visible) { continue; }
        p.tw += 0.05;
        var conv = mode === 0 || mode === 3 ? (H * 0.5 - p.y) * 0.0016 : 0; /* convergência: migração e finops */
        p.y += Math.sin(p.tw) * 0.18 + conv * p.v;
        p.x += p.v * speedK * (mode === 2 && (p.x % (W / 4)) > (W / 4 - 60) ? 0.35 : 1); /* portões: segurança */
        if (p.x > W + 24) { reset(p); }
        var a = 0.28 + 0.5 * Math.abs(Math.sin(p.tw));
        if (mode === 5) { a *= 0.7; }
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = p.hot ? 'rgba(255,166,44,' + a + ')' : 'rgba(148,199,255,' + a * 0.8 + ')';
        ctx.fill();
      }
      /* Observabilidade: anomalia identificada, isolada e estabilizada */
      if (mode === 4) {
        anomaly.t += 1;
        if (!anomaly.active && anomaly.t > 90) {
          anomaly.active = true; anomaly.phase = 0;
          anomaly.x = W * (0.3 + Math.random() * 0.4); anomaly.y = H * (0.35 + Math.random() * 0.3);
        }
        if (anomaly.active) {
          anomaly.phase += 0.02;
          var ph = anomaly.phase;
          var ringR = 6 + ph * 34;
          var warm = ph < 0.9;
          ctx.beginPath();
          ctx.arc(anomaly.x, anomaly.y, 3.2, 0, Math.PI * 2);
          ctx.fillStyle = warm ? 'rgba(255,120,70,0.9)' : 'rgba(120,220,160,0.85)';
          ctx.fill();
          ctx.beginPath();
          ctx.arc(anomaly.x, anomaly.y, ringR, 0, Math.PI * 2);
          ctx.strokeStyle = warm ? 'rgba(255,140,80,' + (0.5 - ph * 0.22) + ')' : 'rgba(130,220,170,' + Math.max(0, 0.5 - ph * 0.25) + ')';
          ctx.lineWidth = 1.2;
          ctx.stroke();
          if (ph > 2) { anomaly.active = false; anomaly.t = 0; }
        }
      } else { anomaly.t = 0; anomaly.active = false; }
      rafId = window.requestAnimationFrame(step);
    }
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { window.cancelAnimationFrame(rafId); }
      else if (running) { rafId = window.requestAnimationFrame(step); }
    });
    window.addEventListener('resize', resize);
    resize();
    return {
      start: function () { if (!running) { running = true; resize(); rafId = window.requestAnimationFrame(step); } },
      stop: function () { running = false; window.cancelAnimationFrame(rafId); },
      setMode: function (m) { mode = m; }
    };
  }

  /* ---------- matchMedia responsivo do GSAP ---------- */
  var mm = gsap.matchMedia();

  /* Desktop com movimento pleno: jornada fixada + reveals + parallax */
  mm.add('(min-width: 1000px) and (prefers-reduced-motion: no-preference)', function () {
    /* Hero: leve parallax de saída */
    var heroMedia = document.querySelector('.cine-hero-media video, .cine-hero-media img');
    if (heroMedia) {
      gsap.to('.cine-hero-media', {
        scrollTrigger: { trigger: '.cine-hero', start: 'top top', end: 'bottom top', scrub: 0.6 },
        yPercent: 12, scale: 1.06, ease: 'none'
      });
    }

    /* Palco da jornada */
    var stage = document.querySelector('.cine-stage');
    var layers = gsap.utils.toArray('.cine-layer');
    var chapters = gsap.utils.toArray('.cine-chapter');
    var dots = gsap.utils.toArray('.cine-progress span');
    var canvas = document.querySelector('.cine-canvas');
    var particles = canvas ? createParticles(canvas) : null;

    if (stage && layers.length && chapters.length === layers.length) {
      var N = chapters.length;
      var SEG = 2.5;
      gsap.set(layers, { autoAlpha: 0 });
      gsap.set(chapters, { visibility: 'visible', autoAlpha: 0, pointerEvents: 'none' });

      var tl = gsap.timeline({
        defaults: { ease: 'none' },
        scrollTrigger: {
          trigger: stage,
          start: 'top top',
          end: '+=' + (N * 110) + '%',
          pin: true,
          scrub: 0.7,
          anticipatePin: 1,
          onToggle: function (self) { if (particles) { self.isActive ? particles.start() : particles.stop(); } },
          onUpdate: function (self) {
            var idx = Math.min(N - 1, Math.floor(self.progress * N));
            if (particles) { particles.setMode(idx); }
            for (var d = 0; d < dots.length; d++) { dots[d].classList.toggle('is-active', d === idx); }
          }
        }
      });

      for (var i = 0; i < N; i++) {
        var at = i * SEG;
        var dir = i % 2 === 0 ? 1 : -1;
        tl.fromTo(layers[i], { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.55 }, at);
        tl.fromTo(layers[i],
          { scale: 1.16, xPercent: 2.2 * dir, yPercent: 1.2 },
          { scale: 1.03, xPercent: 0, yPercent: 0, duration: SEG }, at);
        tl.fromTo(chapters[i],
          { autoAlpha: 0, y: 54 },
          { autoAlpha: 1, y: 0, duration: 0.5, ease: 'power2.out', pointerEvents: 'auto' }, at + 0.45);
        if (i < N - 1) {
          tl.to(chapters[i], { autoAlpha: 0, y: -40, duration: 0.4, ease: 'power1.in', pointerEvents: 'none' }, at + SEG - 0.55);
          tl.to(layers[i], { autoAlpha: 0, duration: 0.55 }, at + SEG - 0.1);
        }
      }
      /* recuo final de câmera (parceria/resultado) */
      tl.to(layers[N - 1], { scale: 1.0, duration: 0.8 }, N * SEG - 0.8);
    }

    /* Reveals das seções de conteúdo */
    gsap.utils.toArray('[data-reveal]').forEach(function (el) {
      gsap.fromTo(el, { autoAlpha: 0, y: 30 }, {
        autoAlpha: 1, y: 0, duration: 0.8, ease: 'power2.out',
        scrollTrigger: { trigger: el, start: 'top 86%', once: true }
      });
    });

    return function () { if (particles) { particles.stop(); } };
  });

  /* Mobile sem movimento reduzido: reveals leves apenas */
  mm.add('(max-width: 999px) and (prefers-reduced-motion: no-preference)', function () {
    gsap.utils.toArray('[data-reveal]').forEach(function (el) {
      gsap.fromTo(el, { autoAlpha: 0, y: 22 }, {
        autoAlpha: 1, y: 0, duration: 0.6, ease: 'power2.out',
        scrollTrigger: { trigger: el, start: 'top 90%', once: true }
      });
    });
  });

  /* ---------- Entrada direta com âncora (#hash) ---------- */
  window.addEventListener('load', function () {
    ScrollTrigger.refresh();
    if (window.location.hash) {
      var el = document.querySelector(window.location.hash);
      if (el) { window.setTimeout(function () { scrollToTarget(el, true); }, 60); }
    }
  });
})();

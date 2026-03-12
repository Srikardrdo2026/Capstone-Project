/* ═══════════════════════════════════════════
   MATRIX BINARY RAIN — Mr. Robot Style
   Falling 1s and 0s like Lively Wallpaper
   ═══════════════════════════════════════════ */

const canvas = document.getElementById("particles");
const ctx = canvas.getContext("2d");

function resize() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
resize();
window.addEventListener("resize", resize);

// Configuration
const FONT_SIZE = 16;
const COLUMNS = Math.floor(canvas.width / FONT_SIZE);

// Each column tracks its current Y drop position
const drops = Array.from({ length: COLUMNS }, () =>
  Math.random() * -100  // stagger start so they don't all begin together
);

// Speed variation per column (some fall faster)
const speeds = Array.from({ length: COLUMNS }, () =>
  0.4 + Math.random() * 0.8
);

// Brightness per column for depth effect
const brightness = Array.from({ length: COLUMNS }, () =>
  0.3 + Math.random() * 0.7
);

// Character pool: binary digits + occasional hex & symbols for variety
const chars = "01001101010011010100110101001101";

function getRandomChar() {
  // Mostly 0s and 1s, occasionally hex or symbols
  const r = Math.random();
  if (r < 0.85) {
    return Math.random() < 0.5 ? "0" : "1";
  } else if (r < 0.95) {
    return "0123456789ABCDEF"[Math.floor(Math.random() * 16)];
  } else {
    return "{}[]<>$/\\#@!%&"[Math.floor(Math.random() * 14)];
  }
}

function draw() {
  // Semi-transparent black overlay creates the trailing fade effect
  ctx.fillStyle = "rgba(0, 0, 0, 0.06)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.font = `${FONT_SIZE}px 'Share Tech Mono', 'Courier New', monospace`;

  for (let i = 0; i < COLUMNS; i++) {
    const char = getRandomChar();
    const x = i * FONT_SIZE;
    const y = drops[i] * FONT_SIZE;

    // Lead character: bright white-green (the "head" of the stream)
    const alpha = brightness[i];
    ctx.fillStyle = `rgba(180, 255, 180, ${alpha})`;
    ctx.fillText(char, x, y);

    // Trail character (slightly above): classic green with varying opacity
    if (drops[i] > 1) {
      const trailChar = getRandomChar();
      const trailAlpha = alpha * 0.6;
      ctx.fillStyle = `rgba(0, 255, 65, ${trailAlpha})`;
      ctx.fillText(trailChar, x, y - FONT_SIZE);
    }

    // Second trail: dimmer
    if (drops[i] > 2) {
      const trailChar2 = getRandomChar();
      const trailAlpha2 = alpha * 0.3;
      ctx.fillStyle = `rgba(0, 200, 50, ${trailAlpha2})`;
      ctx.fillText(trailChar2, x, y - FONT_SIZE * 2);
    }

    // Move drop down
    drops[i] += speeds[i];

    // Reset drop to top when it goes past the screen + random delay
    if (y > canvas.height && Math.random() > 0.975) {
      drops[i] = Math.random() * -20;
      // Randomize speed & brightness on reset for organic variation
      speeds[i] = 0.4 + Math.random() * 0.8;
      brightness[i] = 0.3 + Math.random() * 0.7;
    }
  }

  requestAnimationFrame(draw);
}

// Recalculate columns on resize
window.addEventListener("resize", () => {
  resize();
  const newCols = Math.floor(canvas.width / FONT_SIZE);
  while (drops.length < newCols) {
    drops.push(Math.random() * -100);
    speeds.push(0.4 + Math.random() * 0.8);
    brightness.push(0.3 + Math.random() * 0.7);
  }
});

draw();

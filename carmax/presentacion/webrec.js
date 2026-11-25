// Record carmaxcordoba.com scrolling on a phone, frame by frame. node webrec.js outdir seconds
const { chromium } = require('playwright');
(async () => {
  const out = process.argv[2], secs = parseFloat(process.argv[3] || '3'), fps = 30;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 390, height: 693 }, deviceScaleFactor: 1080 / 390, isMobile: true, hasTouch: true,
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' });
  await p.goto('https://carmaxcordoba.com/', { waitUntil: 'networkidle', timeout: 60000 });
  await p.waitForTimeout(2500);
  const target = await p.evaluate(() => { const e = document.querySelector('#productos'); return e ? e.getBoundingClientRect().top + scrollY : 2500; });
  // pre-scroll once so scroll-in animations have fired, then go back up
  for (let y = 0; y <= target + 1400; y += 300) { await p.evaluate(v => scrollTo(0, v), y); await p.waitForTimeout(120); }
  await p.evaluate(() => scrollTo(0, 0)); await p.waitForTimeout(1200);
  const n = Math.round(secs * fps), end = target + 120;
  for (let i = 0; i < n; i++) {
    const x = i / (n - 1); const e = x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
    await p.evaluate(v => scrollTo(0, v), Math.round(end * e));
    await p.waitForTimeout(25);
    await p.screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.png` });
  }
  await b.close();
})();

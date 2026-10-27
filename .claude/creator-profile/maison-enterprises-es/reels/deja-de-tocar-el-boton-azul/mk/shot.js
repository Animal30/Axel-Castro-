const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({deviceScaleFactor: 2});
 for (const n of ['post','boost','obj']) { await p.goto('file://' + process.cwd() + '/' + n + '.html'); await p.locator('#c').screenshot({path: n + '.png'}); }
 await b.close(); })();

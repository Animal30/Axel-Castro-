const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({deviceScaleFactor: 1, viewport:{width:1300,height:740}});
 for (const n of ['i1','i2','i3','i4','i5']) { await p.goto('file://' + process.cwd() + '/' + n + '.html'); await p.waitForTimeout(300); await p.locator('#c').screenshot({path: n + '.jpg', quality: 92}); }
 await b.close(); })();

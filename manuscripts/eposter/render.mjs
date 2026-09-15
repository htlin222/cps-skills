// Render eposter.html -> eposter.pdf at exact A4 using headless Chromium over CDP.
// No npm dependencies: uses Node 22's built-in fetch + WebSocket.
import { spawn } from 'node:child_process';
import { writeFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const SRC = resolve(here, process.argv[2] ?? 'eposter.html');
const OUT = resolve(here, process.argv[3] ?? 'eposter.pdf');

const CHROME = [
  '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell',
].find(existsSync);
if (!CHROME) throw new Error('no chromium binary found');
if (!existsSync(SRC)) throw new Error(`missing source: ${SRC}`);

const PORT = 9333;
const proc = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage',
  '--hide-scrollbars', '--force-color-profile=srgb', '--font-render-hinting=none',
  '--allow-file-access-from-files', '--remote-allow-origins=*',
  `--remote-debugging-port=${PORT}`, 'about:blank',
], { stdio: ['ignore', 'ignore', 'pipe'] });
proc.stderr.on('data', () => {});

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function browserWs() {
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/json/version`);
      const j = await r.json();
      if (j.webSocketDebuggerUrl) return j.webSocketDebuggerUrl;
    } catch { /* not up yet */ }
    await sleep(250);
  }
  throw new Error('chromium devtools never came up');
}

function connect(url) {
  const ws = new WebSocket(url);
  let id = 0;
  const pending = new Map();
  const events = new Map();
  ws.addEventListener('message', (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id != null && pending.has(msg.id)) {
      const { ok, bad } = pending.get(msg.id);
      pending.delete(msg.id);
      msg.error ? bad(new Error(JSON.stringify(msg.error))) : ok(msg.result);
    } else if (msg.method && events.has(msg.method)) {
      events.get(msg.method).forEach((fn) => fn(msg.params));
      events.delete(msg.method);
    }
  });
  const ready = new Promise((ok, bad) => {
    ws.addEventListener('open', ok, { once: true });
    ws.addEventListener('error', bad, { once: true });
  });
  return {
    ready,
    send: (method, params = {}, sessionId) =>
      new Promise((ok, bad) => {
        const n = ++id;
        pending.set(n, { ok, bad });
        ws.send(JSON.stringify({ id: n, method, params, sessionId }));
      }),
    once: (method) =>
      new Promise((ok) => {
        if (!events.has(method)) events.set(method, []);
        events.get(method).push(ok);
      }),
    close: () => ws.close(),
  };
}

const MM = 25.4; // mm per inch
const A4 = { w: 210 / MM, h: 297 / MM };

const cdp = connect(await browserWs());
await cdp.ready;

const { targetId } = await cdp.send('Target.createTarget', { url: `file://${SRC}` });
const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });

await cdp.send('Page.enable', {}, sessionId);
const loaded = cdp.once('Page.loadEventFired');
await cdp.send('Page.navigate', { url: `file://${SRC}` }, sessionId);
await loaded;
// let webfonts settle + SVG background decode
await cdp.send('Runtime.evaluate', {
  expression: 'document.fonts.ready.then(() => 1)', awaitPromise: true,
}, sessionId);
await sleep(400);


// ---- fit check: report column overflow in mm before printing ----
const fit = await cdp.send('Runtime.evaluate', {
  expression: `(() => {
    const px2mm = (px) => px * 25.4 / 96;
    const cols = document.querySelector('.cols');
    const out = [...document.querySelectorAll('.col')].map((c, i) => {
      const inner = [...c.children].reduce((a, el) => a + el.getBoundingClientRect().height +
        parseFloat(getComputedStyle(el).marginBottom || 0), 0);
      return 'col' + (i + 1) + ': content ' + px2mm(inner).toFixed(1) +
             'mm / available ' + px2mm(cols.clientHeight).toFixed(1) + 'mm  => ' +
             (inner > cols.clientHeight + 0.5 ? 'OVERFLOW ' + px2mm(inner - cols.clientHeight).toFixed(1) + 'mm' : 'fits');
    });
    const ct = document.querySelector('.content');
    out.push('content box: ' + px2mm(ct.clientHeight).toFixed(1) + 'mm tall');
    return out.join('\\n');
  })()`,
  returnByValue: true,
}, sessionId);
console.log(fit.result.value);

const { data } = await cdp.send('Page.printToPDF', {
  printBackground: true,
  preferCSSPageSize: true,
  paperWidth: A4.w,
  paperHeight: A4.h,
  marginTop: 0, marginBottom: 0, marginLeft: 0, marginRight: 0,
  scale: 1,
  pageRanges: '1',
  transferMode: 'ReturnAsBase64',
}, sessionId);

writeFileSync(OUT, Buffer.from(data, 'base64'));
cdp.close();
proc.kill('SIGTERM');
console.log(`ok ${OUT}`);
process.exit(0);

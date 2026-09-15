import { spawn } from 'node:child_process';
import { writeFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const here = dirname(fileURLToPath(import.meta.url));
const SRC = resolve(here, process.argv[2] ?? 'eposter.html');
const OUT = resolve(here, process.argv[3] ?? 'preview.png');
const CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const PORT = 9344;
const proc = spawn(CHROME, ['--headless=new','--disable-gpu','--no-sandbox','--disable-dev-shm-usage',
  '--hide-scrollbars','--force-color-profile=srgb','--allow-file-access-from-files','--remote-allow-origins=*',
  `--remote-debugging-port=${PORT}`,'about:blank'], { stdio:['ignore','ignore','pipe'] });
proc.stderr.on('data',()=>{});
const sleep=(ms)=>new Promise(r=>setTimeout(r,ms));
let wsUrl;
for (let i=0;i<60;i++){ try{ const j=await (await fetch(`http://127.0.0.1:${PORT}/json/version`)).json(); if(j.webSocketDebuggerUrl){wsUrl=j.webSocketDebuggerUrl;break;} }catch{} await sleep(250); }
const ws=new WebSocket(wsUrl); let id=0; const pending=new Map(); const events=new Map();
ws.addEventListener('message',(ev)=>{const m=JSON.parse(ev.data);
  if(m.id!=null&&pending.has(m.id)){const{ok,bad}=pending.get(m.id);pending.delete(m.id);m.error?bad(new Error(JSON.stringify(m.error))):ok(m.result);}
  else if(m.method&&events.has(m.method)){events.get(m.method).forEach(f=>f(m.params));events.delete(m.method);}});
await new Promise((ok,bad)=>{ws.addEventListener('open',ok,{once:true});ws.addEventListener('error',bad,{once:true});});
const send=(method,params={},sessionId)=>new Promise((ok,bad)=>{const n=++id;pending.set(n,{ok,bad});ws.send(JSON.stringify({id:n,method,params,sessionId}));});
const once=(m)=>new Promise(ok=>{if(!events.has(m))events.set(m,[]);events.get(m).push(ok);});
const {targetId}=await send('Target.createTarget',{url:'about:blank'});
const {sessionId}=await send('Target.attachToTarget',{targetId,flatten:true});
await send('Emulation.setDeviceMetricsOverride',{width:794,height:1123,deviceScaleFactor:2,mobile:false},sessionId);
await send('Page.enable',{},sessionId);
const loaded=once('Page.loadEventFired');
await send('Page.navigate',{url:`file://${SRC}`},sessionId);
await loaded;
await send('Runtime.evaluate',{expression:'document.fonts.ready.then(()=>1)',awaitPromise:true},sessionId);
await sleep(500);
const {data}=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y:0,width:794,height:1123,scale:2}},sessionId);
writeFileSync(OUT,Buffer.from(data,'base64'));
ws.close(); proc.kill('SIGTERM'); console.log('ok '+OUT); process.exit(0);

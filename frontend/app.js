/**
 * VERITAS — Disinformation Intelligence Platform
 * Frontend JavaScript
 */

const API = 'http://localhost:5000/api';

const EXAMPLES = [
  "BREAKING: Scientists discover that drinking bleach cures COVID-19, governments are HIDING this miracle cure from the public to push their vaccine agenda!!!",
  "The Federal Reserve raised interest rates by 0.25 percentage points on Wednesday, citing continued concerns about inflation and a resilient labor market, according to officials.",
  "Area man absolutely certain he could land a plane if pilot passes out, having watched one YouTube video about it last Tuesday evening."
];

const SCENARIOS = {
  covid: {
    stat: '12,400 shares · Peaked in 6h · 3 debunks found',
    nodes: [
      { id:'n0', label:'WorldNewsDaily',  type:'origin',     platform:'website',  timestamp:0,     country:'US', is_bot:false, x:0.50, y:0.10 },
      { id:'n1', label:'TelegramGroup',   type:'amplifier',  platform:'telegram', timestamp:1800,  country:'RU', is_bot:false, x:0.22, y:0.30 },
      { id:'n2', label:'AntiVaxForum',    type:'amplifier',  platform:'forum',    timestamp:2400,  country:'US', is_bot:false, x:0.75, y:0.27 },
      { id:'n3', label:'@CovidTruth99',   type:'amplifier',  platform:'twitter',  timestamp:3600,  country:'UK', is_bot:true,  x:0.10, y:0.52 },
      { id:'n4', label:'@FreedomNow',     type:'amplifier',  platform:'twitter',  timestamp:5400,  country:'US', is_bot:true,  x:0.36, y:0.50 },
      { id:'n5', label:'Local News TV',   type:'mainstream', platform:'website',  timestamp:7200,  country:'US', is_bot:false, x:0.63, y:0.52 },
      { id:'n6', label:'Thread#45922',    type:'amplifier',  platform:'twitter',  timestamp:6000,  country:'CA', is_bot:false, x:0.87, y:0.47 },
      { id:'n7', label:'FactCheck.org',   type:'debunker',   platform:'website',  timestamp:14400, country:'US', is_bot:false, x:0.18, y:0.75 },
      { id:'n8', label:'User A',          type:'recipient',  platform:'facebook', timestamp:9000,  country:'IN', is_bot:false, x:0.44, y:0.78 },
      { id:'n9', label:'User B',          type:'recipient',  platform:'facebook', timestamp:10800, country:'BR', is_bot:false, x:0.64, y:0.82 },
      { id:'n10',label:'User C',          type:'recipient',  platform:'twitter',  timestamp:12000, country:'DE', is_bot:false, x:0.84, y:0.75 },
      { id:'n11',label:'WhatsApp Chain',  type:'amplifier',  platform:'whatsapp', timestamp:4800,  country:'IN', is_bot:false, x:0.53, y:0.35 },
    ],
    edges: [
      {s:'n0',t:'n1'},{s:'n0',t:'n2'},{s:'n0',t:'n11'},
      {s:'n1',t:'n3'},{s:'n1',t:'n4'},{s:'n2',t:'n5'},
      {s:'n2',t:'n6'},{s:'n11',t:'n4'},{s:'n11',t:'n5'},
      {s:'n3',t:'n7'},{s:'n4',t:'n8'},{s:'n5',t:'n9'},
      {s:'n6',t:'n10'},{s:'n7',t:'n8'}
    ]
  },
  election: {
    stat: '8,900 shares · 2 bot networks · 18 countries',
    nodes: [
      { id:'n0', label:'AnonymousBlog',  type:'origin',     platform:'website', timestamp:0,     country:'Unknown', is_bot:false, x:0.50, y:0.08 },
      { id:'n1', label:'BotNetwork #1',  type:'amplifier',  platform:'twitter', timestamp:1200,  country:'RU',      is_bot:true,  x:0.25, y:0.27 },
      { id:'n2', label:'BotNetwork #2',  type:'amplifier',  platform:'twitter', timestamp:1800,  country:'RU',      is_bot:true,  x:0.75, y:0.27 },
      { id:'n3', label:'PoliticalForum', type:'amplifier',  platform:'forum',   timestamp:3600,  country:'US',      is_bot:false, x:0.12, y:0.50 },
      { id:'n4', label:'Reddit Thread',  type:'amplifier',  platform:'reddit',  timestamp:4800,  country:'US',      is_bot:false, x:0.40, y:0.47 },
      { id:'n5', label:'YouTube Video',  type:'amplifier',  platform:'youtube', timestamp:7200,  country:'US',      is_bot:false, x:0.64, y:0.50 },
      { id:'n6', label:'Cable TV Clip',  type:'mainstream', platform:'tv',      timestamp:10800, country:'US',      is_bot:false, x:0.87, y:0.43 },
      { id:'n7', label:'Snopes',         type:'debunker',   platform:'website', timestamp:14400, country:'US',      is_bot:false, x:0.15, y:0.72 },
      { id:'n8', label:'AP Fact Check',  type:'debunker',   platform:'website', timestamp:18000, country:'US',      is_bot:false, x:0.40, y:0.78 },
      { id:'n9', label:'User Shares',    type:'recipient',  platform:'twitter', timestamp:9000,  country:'US',      is_bot:false, x:0.63, y:0.78 },
      { id:'n10',label:'Cross-border',   type:'recipient',  platform:'various', timestamp:12000, country:'Various', is_bot:false, x:0.87, y:0.72 },
    ],
    edges: [
      {s:'n0',t:'n1'},{s:'n0',t:'n2'},{s:'n1',t:'n3'},
      {s:'n1',t:'n4'},{s:'n2',t:'n5'},{s:'n2',t:'n6'},
      {s:'n3',t:'n7'},{s:'n4',t:'n8'},{s:'n4',t:'n9'},
      {s:'n5',t:'n9'},{s:'n6',t:'n10'},{s:'n7',t:'n9'},
      {s:'n8',t:'n9'}
    ]
  },
  celeb: {
    stat: '34,000 shares in 3h · Organic spread · Debunked in 8h',
    nodes: [
      { id:'n0', label:'GossipBlog.io',  type:'origin',     platform:'website',   timestamp:0,    country:'US', is_bot:false, x:0.50, y:0.10 },
      { id:'n1', label:'Twitter Leak',   type:'amplifier',  platform:'twitter',   timestamp:900,  country:'US', is_bot:false, x:0.28, y:0.30 },
      { id:'n2', label:'Instagram Post', type:'amplifier',  platform:'instagram', timestamp:1800, country:'UK', is_bot:false, x:0.72, y:0.28 },
      { id:'n3', label:'TikTok Viral',   type:'amplifier',  platform:'tiktok',    timestamp:3600, country:'US', is_bot:false, x:0.15, y:0.55 },
      { id:'n4', label:'Fan Forum',      type:'amplifier',  platform:'forum',     timestamp:4800, country:'AU', is_bot:false, x:0.46, y:0.52 },
      { id:'n5', label:'TMZ Article',    type:'mainstream', platform:'website',   timestamp:7200, country:'US', is_bot:false, x:0.78, y:0.55 },
      { id:'n6', label:'User D',         type:'recipient',  platform:'twitter',   timestamp:5400, country:'CA', is_bot:false, x:0.10, y:0.80 },
      { id:'n7', label:'User E',         type:'recipient',  platform:'facebook',  timestamp:6000, country:'IN', is_bot:false, x:0.35, y:0.82 },
      { id:'n8', label:'User F',         type:'recipient',  platform:'twitter',   timestamp:6600, country:'BR', is_bot:false, x:0.58, y:0.82 },
      { id:'n9', label:'Reuters Check',  type:'debunker',   platform:'website',   timestamp:9000, country:'UK', is_bot:false, x:0.82, y:0.78 },
    ],
    edges: [
      {s:'n0',t:'n1'},{s:'n0',t:'n2'},{s:'n1',t:'n3'},
      {s:'n1',t:'n4'},{s:'n2',t:'n5'},{s:'n3',t:'n6'},
      {s:'n3',t:'n7'},{s:'n4',t:'n7'},{s:'n4',t:'n8'},
      {s:'n5',t:'n9'},{s:'n2',t:'n4'}
    ]
  }
};

const NODE_COLORS = { origin:'#ff4757', amplifier:'#ffa502', mainstream:'#1e90ff', debunker:'#2ed573', recipient:'#747d8c' };
const NODE_SIZES  = { origin:18, amplifier:14, mainstream:14, debunker:14, recipient:9 };
const TYPE_LABELS = { origin:'Origin source', amplifier:'Amplifier', mainstream:'Mainstream media', debunker:'Fact-checker', recipient:'End recipient' };

let currentScenario = 'covid';
let allSources = [];

// ── Health Check ─────────────────────────────────────────────────────────────
async function checkHealth() {
  const pill = document.getElementById('apiStatus');
  const txt  = document.getElementById('statusText');
  try {
    const r = await fetch(`${API}/health`, { signal: AbortSignal.timeout(3000) });
    const d = await r.json();
    txt.textContent = d.model_trained ? 'ML Mode Active' : 'Heuristic Mode';
    pill.className = 'status-pill ok';
  } catch {
    txt.textContent = 'Offline — Local Mode';
    pill.className = 'status-pill err';
  }
}

// ── Tab Navigation ────────────────────────────────────────────────────────────
function switchTab(id) {
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === id));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.getElementById(`tab-${id}`).classList.add('active');
  if (id === 'network') setTimeout(drawGraph, 60);
  if (id === 'sources') loadSourceList('all');
}

// ── Char counter ──────────────────────────────────────────────────────────────
function updateChar() {
  document.getElementById('charCount').textContent = document.getElementById('newsText').value.length;
}

// ── Example loader ────────────────────────────────────────────────────────────
function loadEx(i) {
  const ta = document.getElementById('newsText');
  ta.value = EXAMPLES[i];
  updateChar();
}

// ── Classify ──────────────────────────────────────────────────────────────────
async function classifyText() {
  const text = document.getElementById('newsText').value.trim();
  if (!text) return;
  const btn = document.getElementById('analyzeBtn');
  btn.disabled = true;
  btn.querySelector('span').textContent = 'Analyzing…';

  let result = null;
  try {
    const res = await fetch(`${API}/classify`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }), signal: AbortSignal.timeout(8000)
    });
    const d = await res.json();
    if (d.success) result = d.result;
  } catch {}

  if (!result) result = localClassify(text);
  showResult(result);

  btn.disabled = false;
  btn.querySelector('span').textContent = 'Run Analysis';
}

function localClassify(text) {
  const t = text.toLowerCase(), words = text.split(/\s+/);
  const SENS = ['shocking','bombshell','exposed','secret','hiding','deep state','miracle','cure','banned','censored','wake up','must share','they dont want','government'];
  const HEDG = ['according to','reportedly','sources say','officials said','study shows','data suggests','experts say','research indicates'];
  const sens = SENS.filter(w => t.includes(w)).length;
  const hed  = HEDG.filter(h => t.includes(h)).length;
  const caps = words.filter(w => w.length > 2 && w === w.toUpperCase()).length;
  const excl = (text.match(/!/g)||[]).length;
  const nums = /\d+(\.\d+)?%|\$[\d,]+/.test(text);
  const lex  = new Set(words.map(w => w.toLowerCase())).size / Math.max(words.length, 1);

  let score = 50;
  score += sens * 9; score += (caps/Math.max(words.length,1)) * 35;
  score += excl * 8; score -= hed * 11; score -= nums ? 9 : 0; score -= lex * 18;
  score = Math.max(3, Math.min(97, Math.round(score)));

  const signals = [];
  if (sens > 0)  signals.push({ signal: `Sensational language detected (×${sens})`, impact: 'negative' });
  if (caps > 1)  signals.push({ signal: 'Excessive ALL-CAPS usage', impact: 'negative' });
  if (excl > 0)  signals.push({ signal: 'Clickbait punctuation (!)' , impact: 'negative' });
  if (hed > 0)   signals.push({ signal: 'Attribution language present', impact: 'positive' });
  if (nums)      signals.push({ signal: 'Specific data / statistics cited', impact: 'positive' });
  if (lex > 0.75)signals.push({ signal: 'High lexical diversity', impact: 'positive' });

  const pats = [];
  if (sens > 2) pats.push({ text: 'Conspiracy framing', cls: 'bad' });
  if (caps > 1) pats.push({ text: 'Shouting pattern', cls: 'bad' });
  if (excl > 1) pats.push({ text: 'Clickbait', cls: 'bad' });
  if (hed > 0)  pats.push({ text: 'Source attribution', cls: 'good' });
  if (nums)     pats.push({ text: 'Verifiable data', cls: 'good' });
  if (t.includes('area man') || t.includes('local man')) pats.push({ text: 'Satire markers', cls: 'warn' });

  return {
    verdict: score >= 55 ? 'FAKE' : 'REAL',
    confidence: score >= 55 ? score : 100 - score,
    fake_probability: score,
    features: { sensational_score: sens, hedge_score: hed, caps_ratio: +(caps/Math.max(words.length,1)).toFixed(2), has_numbers: +nums, lexical_diversity: +lex.toFixed(2), word_count: words.length },
    top_signals: signals,
    patterns: pats,
    mode: 'local_heuristic'
  };
}

function showResult(r) {
  document.getElementById('placeholderCard').classList.add('hidden');
  const rc = document.getElementById('resultCard');
  rc.classList.remove('hidden');

  const isFake = r.verdict === 'FAKE' || r.verdict === 'LIKELY FAKE';
  const isReal = !isFake;
  const conf   = Math.round(r.confidence || 70);
  const fp     = Math.round(r.fake_probability || (isFake ? conf : 100 - conf));

  // Verdict badge
  const vbl = document.getElementById('verdictBadgeLarge');
  vbl.textContent = r.verdict;
  vbl.className = 'verdict-badge-large ' + (isFake ? 'vb-fake' : 'vb-real');

  // Ring
  const circumference = 289;
  const offset = circumference - (conf / 100) * circumference;
  const arc = document.getElementById('ringArc');
  arc.style.strokeDashoffset = offset;
  arc.style.stroke = isFake ? '#ff4757' : '#2ed573';
  document.getElementById('ringPct').textContent = conf + '%';

  // Verdict info
  document.getElementById('verdictTitle').textContent  = r.verdict;
  document.getElementById('verdictTitle').style.color  = isFake ? '#ff4757' : '#2ed573';
  document.getElementById('verdictDesc').textContent   = isFake
    ? 'High likelihood of disinformation. Multiple risk signals detected.'
    : 'Low risk indicators. Article shows credibility markers.';

  // Prob bar
  const fill = document.getElementById('probFill');
  fill.style.width = fp + '%';
  fill.style.background = isFake ? '#ff4757' : '#2ed573';
  document.getElementById('probNum').textContent = fp + '%';

  // Mode tag
  document.getElementById('verdictBadgeLarge').parentElement.querySelector('.card-badge') &&
    (document.getElementById('verdictBadgeLarge').parentElement.querySelector('.card-badge').textContent =
      r.mode === 'local_heuristic' ? 'Heuristic' : 'ML Model');

  // Signals list
  document.getElementById('signalsList').innerHTML = (r.top_signals||[]).map(s => `
    <div class="sig-item">
      <span class="sig-dot" style="background:${s.impact==='positive'?'#2ed573':'#ff4757'}"></span>
      <span class="sig-text">${s.signal}</span>
    </div>`).join('');

  // Signals card
  const sc = document.getElementById('signalsCard');
  const f  = r.features || {};
  sc.classList.remove('hidden');
  document.getElementById('signalsGrid').innerHTML = [
    { name:'Sensationalism index', val:(f.sensational_score||0)+' / 5', sub: f.sensational_score>2?'⚠ High':'✓ Low' },
    { name:'Attribution language', val: (f.hedge_score||0)>0?'Present':'Absent', sub:(f.hedge_score||0)>0?'Good signal':'Missing' },
    { name:'Data density',         val: f.has_numbers?'High':'Low', sub: f.has_numbers?'Specific claims':'Vague assertions' },
    { name:'Lexical diversity',    val: ((f.lexical_diversity||0)*100).toFixed(0)+'%', sub:(f.lexical_diversity||0)>0.7?'Rich vocabulary':'Repetitive' },
  ].map(s => `<div class="sig-box"><div class="sig-name">${s.name}</div><div class="sig-val">${s.val}</div><div class="sig-sub">${s.sub}</div></div>`).join('');

  const pats = r.patterns || [];
  document.getElementById('patternTags').innerHTML = pats.map(p =>
    `<span class="ptag ${p.cls}">${p.text}</span>`).join('');
}

// ── Graph ─────────────────────────────────────────────────────────────────────
function selectScenario(key, btn) {
  currentScenario = key;
  document.querySelectorAll('.scenario-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  drawGraph();
}

function drawGraph() {
  const canvas = document.getElementById('netCanvas');
  const ctx    = canvas.getContext('2d');
  const W = canvas.offsetWidth || 700;
  const H = Math.min(400, Math.round(W * 0.55));
  canvas.width = W; canvas.height = H;

  const data  = SCENARIOS[currentScenario];
  const nodes = data.nodes.map(n => ({ ...n, px: n.x * W, py: n.y * H }));
  const nodeMap = {};
  nodes.forEach(n => nodeMap[n.id] = n);

  ctx.clearRect(0,0,W,H);

  // Edges
  data.edges.forEach(e => {
    const a = nodeMap[e.s], b = nodeMap[e.t];
    if (!a || !b) return;
    const angle = Math.atan2(b.py - a.py, b.px - a.px);
    const rB = NODE_SIZES[b.type] + 4;
    const ex = b.px - rB * Math.cos(angle);
    const ey = b.py - rB * Math.sin(angle);

    ctx.beginPath();
    ctx.moveTo(a.px, a.py);
    ctx.lineTo(ex, ey);
    ctx.strokeStyle = 'rgba(255,255,255,0.07)';
    ctx.lineWidth = 1;
    ctx.stroke();

    // Arrow
    ctx.beginPath();
    ctx.moveTo(ex, ey);
    ctx.lineTo(ex - 7*Math.cos(angle-0.4), ey - 7*Math.sin(angle-0.4));
    ctx.lineTo(ex - 7*Math.cos(angle+0.4), ey - 7*Math.sin(angle+0.4));
    ctx.closePath();
    ctx.fillStyle = 'rgba(255,255,255,0.18)';
    ctx.fill();
  });

  // Nodes
  nodes.forEach(n => {
    const r = NODE_SIZES[n.type];
    const col = NODE_COLORS[n.type] || '#747d8c';

    // Glow
    const grd = ctx.createRadialGradient(n.px,n.py,0, n.px,n.py,r*2.5);
    grd.addColorStop(0, col + '30');
    grd.addColorStop(1, 'transparent');
    ctx.beginPath(); ctx.arc(n.px,n.py,r*2.5,0,Math.PI*2);
    ctx.fillStyle = grd; ctx.fill();

    // Node
    ctx.beginPath(); ctx.arc(n.px,n.py,r,0,Math.PI*2);
    ctx.fillStyle = col + '22';
    ctx.fill();
    ctx.strokeStyle = col;
    ctx.lineWidth = n.type === 'origin' ? 2 : 1.5;
    ctx.stroke();

    // Inner dot
    ctx.beginPath(); ctx.arc(n.px,n.py,r*0.45,0,Math.PI*2);
    ctx.fillStyle = col;
    ctx.fill();

    // Bot indicator
    if (n.is_bot) {
      ctx.beginPath(); ctx.arc(n.px+r*0.65, n.py-r*0.65, 4,0,Math.PI*2);
      ctx.fillStyle = '#ff4757'; ctx.fill();
      ctx.strokeStyle = '#080b14'; ctx.lineWidth = 1.5; ctx.stroke();
    }

    // Label
    ctx.fillStyle = 'rgba(232,234,242,0.75)';
    ctx.font = `${n.type==='origin'?'600':'400'} 10.5px 'JetBrains Mono', monospace`;
    ctx.textAlign = 'center';
    ctx.fillText(n.label, n.px, n.py + r + 13);
  });

  // Stat badge
  document.getElementById('graphStatBadge').textContent = data.stat;

  // Tooltip
  canvas.onmousemove = (e) => {
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left, my = e.clientY - rect.top;
    let found = null;
    nodes.forEach(n => { if (Math.hypot(mx-n.px, my-n.py) < NODE_SIZES[n.type]+6) found = n; });
    const tip = document.getElementById('graphTooltip');
    if (found) {
      tip.style.display = 'block';
      tip.style.left = Math.min(found.px+20, W-180)+'px';
      tip.style.top  = Math.max(found.py-50, 4)+'px';
      tip.innerHTML  = `<strong>${found.label}</strong><span>${TYPE_LABELS[found.type]}${found.is_bot?' · 🤖 Bot':''}<br>${found.platform} · ${found.country}</span>`;
    } else { tip.style.display = 'none'; }
  };
  canvas.onmouseleave = () => { document.getElementById('graphTooltip').style.display='none'; };
}

async function analyzeGraph() {
  const data = SCENARIOS[currentScenario];
  const payload = {
    nodes: data.nodes.map(n => ({ id:n.id, label:n.label, type:n.type, platform:n.platform, timestamp:n.timestamp, country:n.country, is_bot:n.is_bot })),
    edges: data.edges.map(e => ({ source:e.s, target:e.t, timestamp:0 }))
  };

  let report = null;
  try {
    const res = await fetch(`${API}/graph/analyze`, {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify(payload), signal: AbortSignal.timeout(8000)
    });
    const d = await res.json();
    if (d.success) report = d.report;
  } catch {}

  if (!report) report = localGraphAnalyze(payload);
  showGraphMetrics(report);
}

function localGraphAnalyze(payload) {
  const outDeg = {}, inDeg = {};
  payload.nodes.forEach(n => { outDeg[n.id]=0; inDeg[n.id]=0; });
  payload.edges.forEach(e => { outDeg[e.source]=(outDeg[e.source]||0)+1; inDeg[e.target]=(inDeg[e.target]||0)+1; });
  const bots = payload.nodes.filter(n=>n.is_bot).length;
  const countries = new Set(payload.nodes.map(n=>n.country).filter(c=>c&&c!=='Unknown')).size;
  const avgOut = payload.nodes.reduce((s,n)=>s+(outDeg[n.id]||0),0)/Math.max(payload.nodes.length,1);
  const top = payload.nodes.sort((a,b)=>(outDeg[b.id]||0)-(outDeg[a.id]||0))[0];
  return { summary: {
    cascade_depth: 4, viral_coefficient: +avgOut.toFixed(2),
    bot_ratio: +(bots/payload.nodes.length).toFixed(2),
    total_nodes: payload.nodes.length, total_edges: payload.edges.length,
    countries_reached: countries
  }, top_amplifiers: [{ label: top?.label||'—', out_degree: outDeg[top?.id]||0 }] };
}

function showGraphMetrics(r) {
  const s = r.summary, amp = r.top_amplifiers?.[0];
  const vk = r.summary.viral_coefficient;
  document.getElementById('m-depth').textContent    = s.cascade_depth;
  document.getElementById('m-viral').textContent    = vk;
  document.getElementById('m-viral').style.color    = vk > 1 ? '#ff4757' : '#2ed573';
  document.getElementById('m-bot').textContent      = (s.bot_ratio*100).toFixed(0)+'%';
  document.getElementById('m-nodes').textContent    = s.total_nodes+' / '+s.total_edges;
  document.getElementById('m-countries').textContent = s.countries_reached;
  document.getElementById('m-amp').textContent      = amp?.label || '—';
  document.getElementById('m-amp').title            = (amp?.out_degree||0)+' shares sent';
}

// ── Source Profiler ───────────────────────────────────────────────────────────
const KNOWN = {
  fake: new Set(['worldnewsdailyreport.com','thenationalistreview.net','infostorm247.co','empirenews.net','libertywriters.com','yournewswire.com']),
  legit: new Set(['reuters.com','apnews.com','bbc.com','factcheck.org','snopes.com','npr.org','theguardian.com']),
  satire: new Set(['theonion.com','babylonbee.com','clickhole.com','newsthump.com']),
};

async function profileDomain() {
  const domain = document.getElementById('domainInput').value.trim();
  if (!domain) return;

  let profile = null;
  try {
    const res = await fetch(`${API}/source/profile`, {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ domain }), signal: AbortSignal.timeout(6000)
    });
    const d = await res.json();
    if (d.success) profile = d.profile;
  } catch {}

  if (!profile) profile = localProfile(domain);
  showProfile(profile);
}

function localProfile(domain) {
  const d = domain.toLowerCase().replace(/^https?:\/\//,'').replace(/^www\./,'').split('/')[0];
  if (KNOWN.fake.has(d))   return { domain:d, credibility_score:5,  source_type:'fake',       risk_flags:['Listed in known fake news database'], positive_signals:[] };
  if (KNOWN.legit.has(d))  return { domain:d, credibility_score:92, source_type:'legitimate', risk_flags:[], positive_signals:['Established credible outlet'] };
  if (KNOWN.satire.has(d)) return { domain:d, credibility_score:60, source_type:'satire',     risk_flags:[], positive_signals:['Known satire publication'] };
  const flags=[]; const pos=[];
  let score = 50;
  if (/patriot|freedom|truth|nationalist/.test(d)) { flags.push('Uses loaded political keywords'); score-=15; }
  if (d.endsWith('.co.nf')||d.endsWith('.tk')) { flags.push('Suspicious TLD pattern'); score-=20; }
  if (/abc\w+news|cnn\w+|bbc\w+news/.test(d)) { flags.push('Mimics legitimate outlet name'); score-=25; }
  if (/reuters|ap|bbc|guardian/.test(d) && !KNOWN.legit.has(d)) { flags.push('Possible impersonation'); score-=15; }
  if (score > 60) pos.push('No major red flags detected');
  return { domain:d, credibility_score:Math.max(2,Math.min(98,score)), source_type: score<35?'fake':score<55?'suspicious':score<75?'unknown':'legitimate', risk_flags:flags, positive_signals:pos };
}

function showProfile(p) {
  const el = document.getElementById('profileResult');
  el.classList.remove('hidden');
  const scoreColor = p.credibility_score>=70?'#2ed573':p.credibility_score>=40?'#ffa502':'#ff4757';
  el.innerHTML = `
    <div class="pr-row">
      <span class="pr-domain">${p.domain}</span>
      <span class="src-badge sb-${p.source_type}">${p.source_type}</span>
      <span style="margin-left:auto;font-family:var(--font-display);font-size:22px;font-weight:800;color:${scoreColor}">${Math.round(p.credibility_score)}<span style="font-size:13px;color:var(--text3)">/100</span></span>
    </div>
    <div class="pr-score-bar">
      <div class="pr-score-fill" style="width:${p.credibility_score}%;background:${scoreColor}"></div>
    </div>
    <div class="pr-flags">
      ${(p.risk_flags||[]).map(f=>`<div class="pr-flag bad">${f}</div>`).join('')}
      ${(p.positive_signals||[]).map(f=>`<div class="pr-flag good">${f}</div>`).join('')}
    </div>`;
}

// ── Source Database ───────────────────────────────────────────────────────────
const SOURCE_DB = [
  { domain:'reuters.com',              credibility_score:94, source_type:'legitimate', risk_flags:[], positive_signals:['Established credible outlet','Wire service standard'] },
  { domain:'apnews.com',               credibility_score:93, source_type:'legitimate', risk_flags:[], positive_signals:['Established credible outlet'] },
  { domain:'factcheck.org',            credibility_score:91, source_type:'legitimate', risk_flags:[], positive_signals:['Fact-checking organisation'] },
  { domain:'bbc.com',                  credibility_score:88, source_type:'legitimate', risk_flags:[], positive_signals:['Public broadcaster standards'] },
  { domain:'snopes.com',               credibility_score:86, source_type:'legitimate', risk_flags:[], positive_signals:['Dedicated fact-checker'] },
  { domain:'theonion.com',             credibility_score:62, source_type:'satire',     risk_flags:[], positive_signals:['Clearly labelled satire'] },
  { domain:'babylonbee.com',           credibility_score:58, source_type:'satire',     risk_flags:[], positive_signals:['Self-identified satire'] },
  { domain:'thenationalistreview.net', credibility_score: 6, source_type:'fake',       risk_flags:['Listed in known fake news database','Loaded domain keywords'], positive_signals:[] },
  { domain:'worldnewsdailyreport.com', credibility_score: 5, source_type:'fake',       risk_flags:['Listed in known fake news database'], positive_signals:[] },
  { domain:'infostorm247.co',          credibility_score:11, source_type:'fake',       risk_flags:['Suspicious TLD','Loaded keywords','High sensationalism'], positive_signals:[] },
];

async function loadSourceList(filter) {
  let sources = null;
  try {
    const res = await fetch(`${API}/source/list`, { signal: AbortSignal.timeout(5000) });
    const d = await res.json();
    if (d.success) sources = d.sources;
  } catch {}
  allSources = sources || SOURCE_DB;
  renderSources(filter);
}

function filterSrc(type, btn) {
  document.querySelectorAll('.fp').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  renderSources(type);
}

function renderSources(filter) {
  const list = filter === 'all' ? allSources : allSources.filter(s => s.source_type === filter);
  const el   = document.getElementById('sourceList');
  if (!list.length) { el.innerHTML = '<div style="color:var(--text3);padding:16px 0;font-size:13px;font-family:var(--font-mono)">No sources match this filter.</div>'; return; }
  const scoreColor = s => s >= 70 ? '#2ed573' : s >= 40 ? '#ffa502' : '#ff4757';
  el.innerHTML = list.map((s,i) => `
    <div class="src-item">
      <span class="src-rank">${i+1}</span>
      <div class="src-info">
        <div class="src-name">${s.domain}</div>
        <div class="src-meta">${(s.risk_flags||[]).slice(0,1)[0] || (s.positive_signals||[]).slice(0,1)[0] || 'No flags'}</div>
      </div>
      <div class="src-score-wrap">
        <span class="src-score" style="color:${scoreColor(s.credibility_score)}">${Math.round(s.credibility_score)}</span>
        <span class="src-badge sb-${s.source_type}">${s.source_type}</span>
      </div>
    </div>`).join('');
}

// ── Init ──────────────────────────────────────────────────────────────────────
checkHealth();
drawGraph();
loadSourceList('all');
window.addEventListener('resize', () => {
  if (document.getElementById('tab-network').classList.contains('active')) drawGraph();
});

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="电子结构理论可视化工具",
    layout="wide",
    page_icon="⚗️",
)

st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stAppViewContainer"] > section > div.block-container {
    padding: 0 !important; max-width: 100% !important;
}
.eyebrow {
    font-size: 13px; font-weight: 500; color: #534AB7;
    letter-spacing: 0.04em; margin-bottom: 16px;
}
.hero-title {
    font-size: clamp(96px, 11vw, 152px);
    font-weight: 700; letter-spacing: -0.03em;
    line-height: 1.05; margin-bottom: 18px; color: #1a1a1a;
}
.grad {
    background: linear-gradient(135deg, #534AB7 0%, #1D9E75 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 16px; color: #666; line-height: 1.7;
    margin-bottom: 28px; max-width: 440px;
}
.stats { display: flex; gap: 8px; width: fit-content; }
.stat {
    background: #f5f5f7; border: 1px solid #eee;
    border-radius: 14px; padding: 10px 14px; flex: 0 0 auto;
    min-width: 80px; text-align: center;
}
.stat-n {
    font-size: 24px; font-weight: 700;
    letter-spacing: -0.02em; margin-bottom: 3px;
}
.stat-l { font-size: 11px; color: #888; line-height: 1.3; }
.modules { padding: 0 4rem 3rem; }
</style>
""", unsafe_allow_html=True)

# ── 三轨道并排动画 ────────────────────────────────────────
ORBITAL_JS = """
<div style="display:flex;gap:0;width:100%;height:100%">
  <canvas id="c1" style="flex:1;height:100%;display:block"></canvas>
  <canvas id="c2" style="flex:1;height:100%;display:block"></canvas>
  <canvas id="c3" style="flex:1;height:100%;display:block"></canvas>
</div>
<script>
let rotX = 0.38, rotY = 0;

function project(x, y, z, W, H) {
  const cosX = Math.cos(rotX), sinX = Math.sin(rotX);
  const cosY = Math.cos(rotY), sinY = Math.sin(rotY);
  const y1 = y*cosX - z*sinX;
  const z1 = y*sinX + z*cosX;
  const x2 = x*cosY + z1*sinY;
  const z2 = -x*sinY + z1*cosY;
  const fov = Math.min(W, H) * 1.15;
  const s = fov / (fov + z2);
  return { sx: W/2 + x2*s, sy: H/2 + y1*s, z: z2, s };
}

function ang_2pz(theta, phi) {
  return Math.cos(theta);
}

function ang_3dz2(theta, phi) {
  const c = Math.cos(theta);
  return 3*c*c - 1;
}

function ang_4fxy2(theta, phi) {
  const s = Math.sin(theta), c = Math.cos(theta);
  return s * s * c * Math.sin(2 * phi);
}

function buildPts(angFn, sc, N) {
  const pts = [];
  for (let i = 0; i < N; i++) {
    const theta = Math.acos(1 - 2*(i+0.5)/N);
    const phi   = 2 * Math.PI * i * 2.399;
    const val   = angFn(theta, phi);
    const r     = Math.abs(val);
    if (r < 0.04) continue;
    const sinT = Math.sin(theta), cosT = Math.cos(theta);
    pts.push({
      bx: r * sinT * Math.cos(phi) * sc,
      by: r * cosT * sc,
      bz: r * sinT * Math.sin(phi) * sc,
      phase: val >= 0 ? 1 : -1
    });
  }
  return pts;
}

const canvases = [
  document.getElementById('c1'),
  document.getElementById('c2'),
  document.getElementById('c3'),
];
const ctxs = canvases.map(c => c.getContext('2d'));

const colors = [
  { pos: '103,88,210', neg: '210,75,130' },
  { pos: '29,158,117', neg: '55,138,221' },
  { pos: '103,88,210', neg: '210,75,130' },
];

const angFns = [ang_2pz, ang_3dz2, ang_4fxy2];
const Ns     = [2400, 2400, 3600];

let allPts = [];

function resizeAll() {
  allPts = [];
  canvases.forEach((c, i) => {
    const r = c.getBoundingClientRect();
    c.width  = r.width  * (window.devicePixelRatio || 1);
    c.height = r.height * (window.devicePixelRatio || 1);
    const sc = Math.min(c.width, c.height) * 0.34;
    allPts.push(buildPts(angFns[i], sc, Ns[i]));
  });
}

resizeAll();
window.addEventListener('resize', resizeAll);

function drawCanvas(idx) {
  const canvas = canvases[idx];
  const ctx = ctxs[idx];
  const W = canvas.width, H = canvas.height;
  const sc = Math.min(W, H);
  const col = colors[idx];
  const pts = allPts[idx];

  ctx.clearRect(0, 0, W, H);

  const proj = pts.map(p => ({
    ...project(p.bx, p.by, p.bz, W, H),
    phase: p.phase
  }));
  proj.sort((a, b) => a.z - b.z);

  for (const p of proj) {
    const depth = Math.min(1, Math.max(0, (p.z + sc*0.52) / (sc*1.04)));
    const size  = Math.max(1.2, p.s * sc * 0.006);
    const alpha = (0.18 + depth * 0.75).toFixed(2);
    ctx.fillStyle = p.phase > 0
      ? `rgba(${col.pos},${alpha})`
      : `rgba(${col.neg},${alpha})`;
    ctx.beginPath();
    ctx.arc(p.sx, p.sy, size, 0, Math.PI*2);
    ctx.fill();
  }

  ctx.fillStyle = 'rgba(83,74,183,0.9)';
  ctx.beginPath();
  ctx.arc(W/2, H/2, Math.max(2.5, sc*0.009), 0, Math.PI*2);
  ctx.fill();
}

function draw(t) {
  rotY = t * 0.0022;
  rotX = 0.38 + Math.sin(t * 0.00038) * 0.22;
  drawCanvas(0);
  drawCanvas(1);
  drawCanvas(2);
  requestAnimationFrame(draw);
}
requestAnimationFrame(draw);
</script>
"""

# ── Hero ─────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("""
    <div style="padding: 4rem 0 3rem 4rem;">
        <div class="eyebrow">电子结构理论 · 三维可视化学习平台</div>
        <div class="hero-title">看见<br><span class="grad">量子世界</span></div>
        <div class="hero-sub">
            从波函数到配位场，以三维交互图像呈现抽象的电子结构概念，
            构建完整的理论认知体系。
        </div>
        <div class="stats">
            <div class="stat">
                <div class="stat-n" style="color:#534AB7">8</div>
                <div class="stat-l">学习模块</div>
            </div>
            <div class="stat">
                <div class="stat-n" style="color:#1D9E75">4</div>
                <div class="stat-l">交互小工具</div>
            </div>
            <div class="stat">
                <div class="stat-n" style="color:#D85A30">3D</div>
                <div class="stat-l">可视化</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    components.html(ORBITAL_JS, height=480)

st.markdown("<div style='border-bottom:0.5px solid #ebebeb;margin: 0 4rem'></div>",
            unsafe_allow_html=True)

# ── 模块列表 ─────────────────────────────────────────────
modules = [
    ("📘", "引言",           "电子结构理论的发展脉络与研究意义", "#CECBF6", "概览",  "pages/0Intro.py"),
    ("⚛️", "量子力学基础",   "波函数、薛定谔方程与概率密度",     "#7F77DD", "QM",   "pages/1Qm Basic.py"),
    ("🌀", "原子轨道",       "s、p、d 轨道三维形状与节点结构",   "#5DCAA5", "AO",   "pages/2Atomic Orbital.py"),
    ("🔗", "分子轨道理论",   "LCAO 近似、成键与反键轨道",        "#378ADD", "MO",   "pages/3Molecular Orbital.py"),
    ("🧬", "价键理论",       "杂化轨道与 σ、π 键的成键机制",    "#EF9F27", "VB",   "pages/4Valence Bond.py"),
    ("📈", "Hückel 分子轨道","π 共轭体系与能级计算",            "#97C459", "HMO",  "pages/5Huckel.py"),
    ("💎", "晶体场理论",     "配位场中 d 轨道的能级分裂",        "#F0997B", "CFT",  "pages/6Crystal Field.py"),
    ("🌈", "配位场理论",     "金属与配体的分子轨道相互作用",     "#ED93B1", "LFT",  "pages/7Ligand Field.py"),
]

st.markdown('<div class="modules">', unsafe_allow_html=True)

for i, (icon, name, desc, color, tag, path) in enumerate(modules):
    col_main, col_btn = st.columns([12, 1])

    with col_main:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:16px;padding:13px 10px;
                    border-bottom:0.5px solid #f2f2f2;margin:0 -10px">
          <span style="font-size:11px;color:#ccc;width:22px;text-align:right;
                       font-variant-numeric:tabular-nums;flex-shrink:0">0{i+1}</span>
          <div style="width:3px;height:22px;border-radius:2px;
                      background:{color};flex-shrink:0"></div>
          <span style="font-size:18px;width:26px;text-align:center;flex-shrink:0">{icon}</span>
          <span style="font-size:14px;font-weight:600;color:#1a1a1a;
                       width:140px;flex-shrink:0">{name}</span>
          <span style="font-size:13px;color:#888;flex:1">{desc}</span>
          <span style="font-size:10px;padding:3px 9px;border-radius:99px;
                       background:#f5f5f7;color:#666;border:1px solid #eee;
                       white-space:nowrap;font-weight:500;flex-shrink:0">{tag}</span>
        </div>
        """, unsafe_allow_html=True)

    with col_btn:
        if st.button("→", key=f"btn{i}", use_container_width=True):
            st.switch_page(path)

st.markdown('</div>', unsafe_allow_html=True)

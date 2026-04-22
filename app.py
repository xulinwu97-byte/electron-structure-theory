import streamlit as st

st.set_page_config(
    page_title="电子结构理论可视化工具",
    layout="wide",
    page_icon="⚗️",
)

MODULES = [
    {"key": "intro",    "title": "引言",            "tag": "概览", "tag_bg": "#F1EFE8", "tag_col": "#444441", "dot": "#888",    "path": "pages/0Intro.py"},
    {"key": "qm",       "title": "量子力学基础",    "tag": "QM",   "tag_bg": "#EEEDFE", "tag_col": "#3C3489", "dot": "#7F77DD", "path": "pages/1Qm Basic.py"},
    {"key": "ao",       "title": "原子轨道",        "tag": "AO",   "tag_bg": "#E1F5EE", "tag_col": "#085041", "dot": "#5DCAA5", "path": "pages/2Atomic Orbital.py"},
    {"key": "mo",       "title": "分子轨道理论",    "tag": "MO",   "tag_bg": "#E6F1FB", "tag_col": "#0C447C", "dot": "#378ADD", "path": "pages/3Molecular Orbital.py"},
    {"key": "vb",       "title": "价键理论",        "tag": "VB",   "tag_bg": "#FAEEDA", "tag_col": "#633806", "dot": "#EF9F27", "path": "pages/4Valence Bond.py"},
    {"key": "hmo",      "title": "Hückel 分子轨道", "tag": "HMO",  "tag_bg": "#EAF3DE", "tag_col": "#27500A", "dot": "#97C459", "path": "pages/5Huckel.py"},
    {"key": "cft",      "title": "晶体场理论",      "tag": "CFT",  "tag_bg": "#FAECE7", "tag_col": "#712B13", "dot": "#F0997B", "path": "pages/6Crystal Field.py"},
    {"key": "lft",      "title": "配位场理论",      "tag": "LFT",  "tag_bg": "#FBEAF0", "tag_col": "#72243E", "dot": "#ED93B1", "path": "pages/7Ligand Field.py"},
    {"key": "summary",  "title": "理论总结",        "tag": "总结", "tag_bg": "#EEF2F7", "tag_col": "#2C3E50", "dot": "#607D8B", "path": "pages/8Summary.py"},
]

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stAppViewContainer"] > section > div.block-container {
    padding: 0 !important; max-width: 100% !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

/* 与 utils.py 完全一致的侧边栏按钮样式 */
[data-testid="stSidebar"] .stButton {
    position: relative !important;
    height: 40px !important;
    margin: 0 !important;
    z-index: 100 !important;
}
[data-testid="stSidebar"] .stButton button {
    position: absolute !important;
    inset: 0 !important;
    width: 100% !important;
    height: 40px !important;
    opacity: 0 !important;
    z-index: 101 !important;
    cursor: pointer !important;
    border: none !important;
}
.nav-item-container {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 10;
}
.nav-item {
    height: 40px;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0 1rem;
    border-left: 3px solid transparent;
}

/* 主页内容区 */
.hero-screen {
    width: 100%; min-height: 100vh;
    display: grid; grid-template-columns: 1fr 1fr;
    align-items: center; padding: 0 6vw; gap: 4vw;
    box-sizing: border-box; position: relative;
    border-bottom: 0.5px solid #ebebeb;
}
.hero-left { display: flex; flex-direction: column; justify-content: center; padding: 4vh 0; }
.eyebrow { font-size: clamp(11px,1vw,14px); font-weight: 500; color: #534AB7; letter-spacing: 0.05em; margin-bottom: 2vh; }
.hero-title { font-size: clamp(56px,9vw,140px); font-weight: 700; letter-spacing: -0.03em; line-height: 1.05; margin-bottom: 2.5vh; color: #1a1a1a; }
.grad { background: linear-gradient(135deg, #534AB7 0%, #1D9E75 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-sub { font-size: clamp(13px,1.2vw,17px); color: #666; line-height: 1.75; margin-bottom: 3vh; max-width: 44ch; }
.stats { display: flex; gap: 6px; flex-wrap: nowrap; width: fit-content; }
.stat { background: #f5f5f7; border: 1px solid #eee; border-radius: 14px; padding: clamp(6px,0.8vh,10px) clamp(6px,0.7vw,12px); text-align: center; flex-shrink: 0; }
.stat-n { font-size: clamp(13px,1.4vw,20px); font-weight: 700; letter-spacing: -0.02em; margin-bottom: 2px; white-space: nowrap; }
.stat-l { font-size: clamp(9px,0.6vw,11px); color: #888; white-space: nowrap; }
.hero-right { display: flex; align-items: center; justify-content: center; }
.orb-scene { position: relative; width: clamp(260px,38vw,500px); height: clamp(260px,38vw,500px); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.orb { width: 52%; height: 52%; border-radius: 50%; background: radial-gradient(circle at 32% 32%, #AFA9EC 0%, #534AB7 45%, #26215C 100%); box-shadow: 0 0 8vw rgba(83,74,183,0.28); position: relative; z-index: 2; }
.ring { position: absolute; border-radius: 50%; border: 1px solid rgba(83,74,183,0.2); top: 50%; left: 50%; transform: translate(-50%, -50%); }
.r1 { width:71%; height:71%; animation: spin 9s linear infinite; }
.r2 { width:86%; height:86%; animation: spin 16s linear infinite reverse; border-color: rgba(29,158,117,0.15); }
.r3 { width:100%; height:100%; animation: spin 24s linear infinite; border-color: rgba(83,74,183,0.08); }
@keyframes spin { to { transform: translate(-50%,-50%) rotate(360deg); } }
.dot { position: absolute; border-radius: 50%; }
.d1 { width:clamp(7px,0.8vw,12px); height:clamp(7px,0.8vw,12px); background:#5DCAA5; top:-4px; left:50%; transform:translateX(-50%); box-shadow:0 0 8px rgba(29,158,117,0.7); }
.d2 { width:clamp(6px,0.7vw,10px); height:clamp(6px,0.7vw,10px); background:#D4537E; bottom:50%; right:-4px; transform:translateY(50%); box-shadow:0 0 6px rgba(212,83,126,0.6); }
.d3 { width:clamp(5px,0.6vw,9px); height:clamp(5px,0.6vw,9px); background:#EF9F27; top:50%; left:-4px; transform:translateY(-50%); box-shadow:0 0 6px rgba(239,159,39,0.6); }
.scroll-hint { position: absolute; bottom: 5vh; left: 50%; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; gap: 6px; color: #bbb; font-size: clamp(12px,1vw,15px); letter-spacing: 0.05em; animation: fadeup 2s ease-in-out infinite; }
.scroll-hint svg { opacity: 0.5; width: 22px; height: 22px; }
@keyframes fadeup { 0% { opacity:0.3; transform:translateX(-50%) translateY(0); } 50% { opacity:1; transform:translateX(-50%) translateY(-4px); } 100% { opacity:0.3; transform:translateX(-50%) translateY(0); } }
</style>
""", unsafe_allow_html=True)

# ── 侧边栏（与 utils.py 完全一致）───────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="padding:1.5rem 1rem 1rem; border-bottom:0.5px solid #ebebeb; margin-bottom:10px;">'
        '<div style="font-size:10px; font-weight:600; color:#bbb; letter-spacing:0.1em; text-transform:uppercase;">ELECTRONIC THEORY</div>'
        '<div style="font-size:16px; font-weight:700; color:#333; margin-top:4px;">电子结构理论</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="font-size:10px; font-weight:600; color:#bbb; letter-spacing:0.08em; '
        'text-transform:uppercase; padding:0.5rem 1rem 0.5rem">学习模块</div>',
        unsafe_allow_html=True
    )

    for m in MODULES:
        with st.container():
            st.markdown(f"""
            <div class="nav-item-container">
                <div class="nav-item">
                    <div style="width:7px; height:7px; border-radius:50%; background:{m['dot']}; flex-shrink:0;"></div>
                    <span style="font-size:13px; flex:1; color:#333;">{m['title']}</span>
                    <span style="font-size:9px; padding:2px 6px; border-radius:99px; background:{m['tag_bg']}; color:{m['tag_col']};">{m['tag']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(m["title"], key=f"home_mod_{m['key']}", width="stretch"):
                st.switch_page(m["path"])

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown(
            '<div class="nav-item-container" style="margin:0 10px;">'
            '<div style="height:44px; border-radius:10px; background:#534AB7; display:flex; align-items:center; padding:0 12px; width:100%">'
            '<div style="flex:1">'
            '<div style="font-size:10px; color:rgba(255,255,255,0.6)">开始学习</div>'
            '<div style="font-size:12px; font-weight:600; color:white">引言 →</div>'
            '</div></div></div>',
            unsafe_allow_html=True
        )
        if st.button("Next", key="home_start", width="stretch"):
            st.switch_page("pages/0Intro.py")

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

# ── 主页内容（原封不动）───────────────────────────────────
modules_data = [
    ("📘", "引言",            "电子结构理论的发展脉络与研究意义", "#CECBF6", "概览",  "pages/0Intro.py"),
    ("⚛️", "量子力学基础",    "波函数、薛定谔方程与概率密度",     "#7F77DD", "QM",   "pages/1Qm Basic.py"),
    ("🌀", "原子轨道",        "s、p、d 轨道三维形状与节点结构",   "#5DCAA5", "AO",   "pages/2Atomic Orbital.py"),
    ("🔗", "分子轨道理论",    "LCAO 近似、成键与反键轨道",        "#378ADD", "MO",   "pages/3Molecular Orbital.py"),
    ("🧬", "价键理论",        "杂化轨道与 σ、π 键的成键机制",    "#EF9F27", "VB",   "pages/4Valence Bond.py"),
    ("📈", "Hückel 分子轨道", "π 共轭体系与能级计算",            "#97C459", "HMO",  "pages/5Huckel.py"),
    ("💎", "晶体场理论",      "配位场中 d 轨道的能级分裂",        "#F0997B", "CFT",  "pages/6Crystal Field.py"),
    ("🌈", "配位场理论",      "金属与配体的分子轨道相互作用",     "#ED93B1", "LFT",  "pages/7Ligand Field.py"),
    ("📊", "理论总结",        "各理论适用范围与优缺点横向对比",   "#607D8B", "总结", "pages/8Summary.py"),
]

st.markdown("""
<div class="hero-screen">
  <div class="hero-left">
    <div class="eyebrow">电子结构理论 · 三维可视化学习平台</div>
    <div class="hero-title">看见<br><span class="grad">量子世界</span></div>
    <div class="hero-sub">从波函数到配位场，以三维交互图像呈现抽象的电子结构概念，构建完整的理论认知体系。</div>
    <div class="stats">
        <div class="stat"><div class="stat-n" style="color:#534AB7">8</div><div class="stat-l">学习模块</div></div>
        <div class="stat"><div class="stat-n" style="color:#1D9E75">3</div><div class="stat-l">可交互小工具</div></div>
        <div class="stat"><div class="stat-n" style="color:#D85A30">3D</div><div class="stat-l">原子轨道</div></div>
        <div class="stat"><div class="stat-n" style="color:#378ADD">2D</div><div class="stat-l">分子轨道</div></div>
        <div class="stat"><div class="stat-n" style="color:#97C459">HMO</div><div class="stat-l">快速计算</div></div>
    </div>
  </div>
  <div class="hero-right">
    <div class="orb-scene">
      <div class="ring r1"><div class="dot d1"></div></div>
      <div class="ring r2"><div class="dot d2"></div></div>
      <div class="ring r3"><div class="dot d3"></div></div>
      <div class="orb"></div>
    </div>
  </div>
  <div class="scroll-hint">
    下滑查看目录
    <svg width="22" height="22" viewBox="0 0 16 16" fill="none">
      <path d="M8 3v10M4 9l4 4 4-4" stroke="#aaa" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>
</div>
""", unsafe_allow_html=True)

for i, (icon, name, desc, color, tag, path) in enumerate(modules_data):
    col_main, col_btn = st.columns([12, 1])
    with col_main:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:clamp(10px,1.5vw,20px);
                    padding:clamp(10px,1.5vh,15px) clamp(6px,0.6vw,10px);
                    border-bottom:0.5px solid #f2f2f2;margin:0 -10px;">
          <span style="font-size:clamp(10px,0.75vw,12px);color:#ccc;width:22px;
                       text-align:right;flex-shrink:0;font-variant-numeric:tabular-nums;">0{i+1}</span>
          <div style="width:3px;height:22px;border-radius:2px;
                      background:{color};flex-shrink:0;"></div>
          <span style="font-size:clamp(15px,1.4vw,20px);width:26px;
                       text-align:center;flex-shrink:0;">{icon}</span>
          <span style="font-size:clamp(12px,1vw,15px);font-weight:600;color:#1a1a1a;
                       width:clamp(90px,12vw,160px);flex-shrink:0;">{name}</span>
          <span style="font-size:clamp(11px,0.9vw,14px);color:#888;flex:1;">{desc}</span>
          <span style="font-size:clamp(9px,0.7vw,11px);padding:3px 10px;border-radius:99px;
                       background:#f5f5f7;color:#666;border:1px solid #eee;
                       white-space:nowrap;font-weight:500;flex-shrink:0;">{tag}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_btn:
        if st.button("→", key=f"btn{i}", use_container_width=True):
            st.switch_page(path)
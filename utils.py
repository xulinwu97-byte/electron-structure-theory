import streamlit as st

def load_md(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

MODULES = [
    {"key": "intro", "title": "引言",            "en": "Introduction",      "tag": "概览", "tag_bg": "#F1EFE8", "tag_col": "#444441", "accent": "#888780", "dot": "#888",    "path": "pages/0Intro.py"},
    {"key": "qm",    "title": "量子力学基础",    "en": "Quantum Mechanics", "tag": "QM",   "tag_bg": "#EEEDFE", "tag_col": "#3C3489", "accent": "#7F77DD", "dot": "#7F77DD", "path": "pages/1Qm Basic.py"},
    {"key": "ao",    "title": "原子轨道",        "en": "Atomic Orbital",    "tag": "AO",   "tag_bg": "#E1F5EE", "tag_col": "#085041", "accent": "#5DCAA5", "dot": "#5DCAA5", "path": "pages/2Atomic Orbital.py"},
    {"key": "mo",    "title": "分子轨道理论",    "en": "Molecular Orbital", "tag": "MO",   "tag_bg": "#E6F1FB", "tag_col": "#0C447C", "accent": "#378ADD", "dot": "#378ADD", "path": "pages/3Molecular Orbital.py"},
    {"key": "vb",    "title": "价键理论",        "en": "Valence Bond",      "tag": "VB",   "tag_bg": "#FAEEDA", "tag_col": "#633806", "accent": "#EF9F27", "dot": "#EF9F27", "path": "pages/4Valence Bond.py"},
    {"key": "hmo",   "title": "Hückel 分子轨道", "en": "Hückel MO",         "tag": "HMO",  "tag_bg": "#EAF3DE", "tag_col": "#27500A", "accent": "#97C459", "dot": "#97C459", "path": "pages/5Huckel.py"},
    {"key": "cft",   "title": "晶体场理论",      "en": "Crystal Field",     "tag": "CFT",  "tag_bg": "#FAECE7", "tag_col": "#712B13", "accent": "#F0997B", "dot": "#F0997B", "path": "pages/6Crystal Field.py"},
    {"key": "lft",   "title": "配位场理论",      "en": "Ligand Field",      "tag": "LFT",  "tag_bg": "#FBEAF0", "tag_col": "#72243E", "accent": "#ED93B1", "dot": "#ED93B1", "path": "pages/7Ligand Field.py"},
    {"key": "summary", "title": "理论总结",      "en": "Summary",           "tag": "总结", "tag_bg": "#EEF2F7", "tag_col": "#2C3E50", "accent": "#607D8B", "dot": "#607D8B", "path": "pages/8Summary.py"},
    
]

def _get(key):
    for i, m in enumerate(MODULES):
        if m["key"] == key:
            return i, m
    return 0, MODULES[0]

PAGE_CSS = """
<style>
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stAppViewContainer"] > section > div.block-container {
    padding: 0 !important; max-width: 100% !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0 !important; }

/* 侧边栏按钮容器 */
[data-testid="stSidebar"] .stButton {
    position: relative !important;
    height: 40px !important;
    margin: 0 !important;
    z-index: 100 !important;
}

/* 隐藏真实按钮，保持点击区域 */
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

/* 文字装饰层禁止干扰点击 */
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
.nav-item.active { background-color: #EEEDFE; border-left-color: #534AB7; }

/* 内容区样式 */
.page-hero { padding: 2.5rem 3rem 2rem; border-bottom: 0.5px solid #ebebeb; }
.page-eyebrow { font-size: 12px; font-weight: 500; letter-spacing: 0.04em; margin-bottom: 8px; }
.page-title { font-size: 36px; font-weight: 700; color: #1a1a1a; }
.page-desc { font-size: 15px; color: #666; line-height: 1.75; max-width: 600px; }
.page-content { padding: 0.5rem 3rem 1rem; }
.custom-divider { border: none; height: 0.5px; background: linear-gradient(to right, transparent, #ddd, transparent); margin: 2.5rem 0; }
</style>
"""

def page_header(module_key, desc=""):
    idx, mod = _get(module_key)
    prev_mod = MODULES[idx - 1] if idx > 0 else None
    next_mod = MODULES[idx + 1] if idx < len(MODULES) - 1 else None

    st.markdown(PAGE_CSS, unsafe_allow_html=True)

    with st.sidebar:
        # 侧边栏标题
        st.markdown('<div style="padding:1.5rem 1rem 1rem; border-bottom:0.5px solid #ebebeb; margin-bottom: 10px;"><div style="font-size:10px; font-weight:600; color:#bbb; letter-spacing:0.1em; text-transform:uppercase;">ELECTRONIC THEORY</div><div style="font-size:16px; font-weight:700; color:#333; margin-top:4px;">电子结构理论</div></div>', unsafe_allow_html=True)

        # 返回首页按钮
        with st.container():
            st.markdown('<div class="nav-item-container"><div class="nav-item" style="border: 0.5px solid #e0e0e0; background:#fff; border-radius:8px; margin: 0 10px; height:36px;"><span style="font-size:14px; margin-left:4px;">←</span><span style="font-size:13px; color:#555;">返回主页</span></div></div>', unsafe_allow_html=True)
            if st.button("Home", key="sb_home", width="stretch"):
                st.switch_page("app.py")

        st.markdown('<div style="font-size:10px; font-weight:600; color:#bbb; letter-spacing:0.08em; text-transform:uppercase; padding:0.5rem 1rem 0.5rem">学习模块</div>', unsafe_allow_html=True)

        # 模块列表
        for j, m in enumerate(MODULES):
            is_active = m["key"] == module_key
            active_class = "active" if is_active else ""
            title_style = "font-weight:600; color:#3C3489;" if is_active else "color:#333;"

            with st.container():
                st.markdown(f"""
                <div class="nav-item-container">
                    <div class="nav-item {active_class}">
                        <div style="width:7px; height:7px; border-radius:50%; background:{m['dot']}; flex-shrink:0;"></div>
                        <span style="font-size:13px; flex:1; {title_style}">{m['title']}</span>
                        <span style="font-size:9px; padding:2px 6px; border-radius:99px; background:{m['tag_bg']}; color:{m['tag_col']};">{m['tag']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if not is_active:
                    if st.button(m["title"], key=f"sb_mod_{m['key']}", width="stretch"):
                        st.switch_page(m["path"])
                else:
                    st.markdown('<div style="height:40px"></div>', unsafe_allow_html=True)

        # 下一章快捷导航
        if next_mod:
            st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
            with st.container():
                st.markdown(f'<div class="nav-item-container" style="margin: 0 10px;"><div style="height:44px; border-radius:10px; background:#534AB7; display:flex; align-items:center; padding:0 12px; width:100%"><div style="flex:1"><div style="font-size:10px; color:rgba(255,255,255,0.6)">下一章</div><div style="font-size:12px; font-weight:600; color:white">{next_mod["title"]} →</div></div></div></div>', unsafe_allow_html=True)
                if st.button("Next", key="sb_next", width="stretch"):
                    st.switch_page(next_mod["path"])

    # 英雄区
    st.markdown(f'<div class="page-hero"><div class="page-eyebrow" style="color:{mod["accent"]}">{mod["title"]} · {mod["en"]}</div><div class="page-title">{mod["title"]}</div><div class="page-desc">{desc}</div></div><div class="page-content">', unsafe_allow_html=True)

def page_footer(module_key):
    idx, mod = _get(module_key)
    prev_mod = MODULES[idx - 1] if idx > 0 else None
    next_mod = MODULES[idx + 1] if idx < len(MODULES) - 1 else None

    st.markdown('</div>', unsafe_allow_html=True)
    divider()

    col_prev, col_home, col_next = st.columns([1, 1, 1])
    with col_prev:
        if prev_mod:
            if st.button(f"← {prev_mod['title']}", key=f"ftr_prev_{module_key}", width="stretch"):
                st.switch_page(prev_mod["path"])
    with col_home:
        if st.button("⬆ 返回首页", key="ftr_home", width="stretch"):
            st.switch_page("app.py")
    with col_next:
        if next_mod:
            if st.button(f"{next_mod['title']} →", key=f"ftr_next_{module_key}", width="stretch"):
                st.switch_page(next_mod["path"])

def divider():
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
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

/* 把侧边栏所有 Streamlit 按钮变透明覆盖层 */
[data-testid="stSidebar"] .stButton button {
    position: absolute !important;
    inset: 0 !important;
    opacity: 0 !important;
    cursor: pointer !important;
    border: none !important;
    background: transparent !important;
    width: 100% !important;
    height: 100% !important;
    z-index: 10 !important;
}
[data-testid="stSidebar"] .stButton {
    position: relative !important;
}

.page-hero {
    padding: 2.5rem 3rem 2rem;
    border-bottom: 0.5px solid #ebebeb;
}
.page-eyebrow {
    font-size: 12px; font-weight: 500;
    letter-spacing: 0.04em; margin-bottom: 8px;
}
.page-title {
    font-size: 36px; font-weight: 700;
    letter-spacing: -0.02em; line-height: 1.1;
    margin-bottom: 10px; color: #1a1a1a;
}
.page-desc {
    font-size: 15px; color: #666;
    line-height: 1.75; max-width: 600px;
}
.page-content { padding: 0.5rem 3rem 1rem; }
.page-content h1, .page-content h2 {
    font-size: 20px; font-weight: 600;
    color: #1a1a1a; margin: 2rem 0 0.75rem;
}
.page-content h3 {
    font-size: 16px; font-weight: 600;
    color: #333; margin: 1.5rem 0 0.5rem;
}
.page-content p {
    font-size: 15px; line-height: 1.85;
    color: #444; margin-bottom: 1rem;
}
.page-content table {
    width: 100%; border-collapse: collapse;
    margin: 1.25rem 0; font-size: 14px;
}
.page-content th {
    background: #f5f5f7; padding: 9px 14px;
    border: 1px solid #eee; font-weight: 600; text-align: left;
}
.page-content td {
    padding: 9px 14px; border: 1px solid #eee; color: #555;
}
.page-content blockquote {
    border-left: 3px solid #e0e0e0;
    margin: 1rem 0; padding: 0.5rem 1rem;
    color: #666; font-style: italic;
}
.custom-divider {
    border: none; height: 0.5px;
    background: linear-gradient(to right, transparent, #ddd, transparent);
    margin: 2.5rem 0;
}
</style>
"""

def page_header(module_key, desc=""):
    idx, mod = _get(module_key)
    prev_mod = MODULES[idx - 1] if idx > 0 else None
    next_mod = MODULES[idx + 1] if idx < len(MODULES) - 1 else None

    st.markdown(PAGE_CSS, unsafe_allow_html=True)

    # ── 侧边栏 ──────────────────────────────────────────
    with st.sidebar:
        # 顶部 logo + 返回按钮
        st.markdown("""
        <div style="padding:1.2rem 1rem 0.8rem;border-bottom:0.5px solid #ebebeb">
          <div style="font-size:10px;font-weight:600;color:#bbb;letter-spacing:0.08em;
                      text-transform:uppercase;margin-bottom:10px">电子结构理论</div>
        </div>
        """, unsafe_allow_html=True)

        # 返回主页按钮
        st.markdown("""
        <div style="padding:0.6rem 1rem;position:relative">
          <div style="display:flex;align-items:center;gap:8px;padding:8px 12px;
                      border-radius:10px;border:0.5px solid #e0e0e0;background:#fafafa;
                      font-size:13px;color:#555;cursor:pointer">
            <span style="font-size:14px">←</span>
            <span>返回主页</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("返回主页", key="sb_home"):
            st.switch_page("app.py")

        st.markdown("""
        <div style="font-size:10px;font-weight:600;color:#bbb;letter-spacing:0.08em;
                    text-transform:uppercase;padding:1rem 1rem 0.4rem">学习模块</div>
        """, unsafe_allow_html=True)

        # 模块列表
        for j, m in enumerate(MODULES):
            is_active = m["key"] == module_key
            bg = "#EEEDFE" if is_active else "transparent"
            border = f"border-left:3px solid #534AB7;padding-left:calc(1rem - 3px);" if is_active else "border-left:3px solid transparent;padding-left:calc(1rem - 3px);"
            name_w = "font-weight:600;color:#3C3489;" if is_active else "color:#333;"

            st.markdown(f"""
            <div style="position:relative;background:{bg};{border}
                        padding-top:7px;padding-right:1rem;padding-bottom:7px;
                        transition:background 0.1s;height:40px;display:flex;
                        align-items:center;gap:8px;">
              <div style="width:7px;height:7px;border-radius:50%;
                          background:{m['dot']};flex-shrink:0"></div>
              <span style="font-size:13px;flex:1;{name_w}">{m['title']}</span>
              <span style="font-size:9px;padding:2px 6px;border-radius:99px;
                           font-weight:500;background:{m['tag_bg']};
                           color:{m['tag_col']};flex-shrink:0">{m['tag']}</span>
            </div>
            """, unsafe_allow_html=True)

            if not is_active:
                if st.button(m["title"], key=f"sb_mod_{m['key']}"):
                    st.switch_page(m["path"])
            else:
                st.markdown('<div style="height:0"></div>', unsafe_allow_html=True)

        # 底部导航
        st.markdown('<div style="border-top:0.5px solid #ebebeb;padding:0.75rem 1rem 0;margin-top:0.5rem">', unsafe_allow_html=True)

        if prev_mod:
            st.markdown(f"""
            <div style="position:relative;height:36px;display:flex;align-items:center;
                        font-size:12px;color:#888;gap:4px;margin-bottom:6px">
              ← {prev_mod['title']}
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"← {prev_mod['title']}", key="sb_prev"):
                st.switch_page(prev_mod["path"])

        if next_mod:
            st.markdown(f"""
            <div style="position:relative;height:40px;border-radius:10px;
                        background:#534AB7;display:flex;align-items:center;
                        padding:0 12px;gap:4px">
              <div style="flex:1">
                <div style="font-size:10px;color:rgba(255,255,255,0.6)">下一章</div>
                <div style="font-size:12px;font-weight:600;color:white">{next_mod['title']} →</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"{next_mod['title']} →", key="sb_next"):
                st.switch_page(next_mod["path"])

        st.markdown('</div>', unsafe_allow_html=True)

    # ── 页面 Hero ────────────────────────────────────────
    st.markdown(f"""
    <div class="page-hero">
      <div class="page-eyebrow" style="color:{mod['accent']}">
        {mod['title']} · {mod['en']}
      </div>
      <div class="page-title">{mod['title']}</div>
      <div class="page-desc">{desc}</div>
    </div>
    <div class="page-content">
    """, unsafe_allow_html=True)


def page_footer(module_key):
    idx, mod = _get(module_key)
    prev_mod = MODULES[idx - 1] if idx > 0 else None
    next_mod = MODULES[idx + 1] if idx < len(MODULES) - 1 else None

    st.markdown('</div>', unsafe_allow_html=True)
    divider()

    prev_html = ""
    if prev_mod:
        prev_html = f"""
        <div style="font-size:10px;color:#bbb;text-transform:uppercase;
                    letter-spacing:0.06em;margin-bottom:4px">上一章</div>
        <div style="font-size:14px;font-weight:600;color:#555">← {prev_mod['title']}</div>
        """
    next_html = ""
    if next_mod:
        next_html = f"""
        <div style="font-size:10px;color:#bbb;text-transform:uppercase;
                    letter-spacing:0.06em;margin-bottom:4px">下一章</div>
        <div style="font-size:14px;font-weight:600;color:#534AB7">{next_mod['title']} →</div>
        """

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:stretch;
                gap:12px;padding:1.5rem 3rem 2.5rem">
      <div style="flex:1">{prev_html}</div>
      <div style="flex:1;text-align:right">{next_html}</div>
    </div>
    """, unsafe_allow_html=True)

    col_prev, col_home, col_next = st.columns([1, 1, 1])
    with col_prev:
        if prev_mod:
            if st.button(f"← {prev_mod['title']}", key=f"sb_prev_{module_key}"):
                st.switch_page(prev_mod["path"])
    with col_home:
        if st.button("⬆ 返回首页", key="ftr_home", use_container_width=True):
            st.switch_page("app.py")
    with col_next:
        if next_mod:
            if st.button(f"{next_mod['title']} →", key=f"sb_next_{module_key}"):
                st.switch_page(next_mod["path"])


def divider():
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
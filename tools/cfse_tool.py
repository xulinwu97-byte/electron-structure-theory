import streamlit as st

# ── 数据库 ──────────────────────────────────────────────────────────────
# 金属离子：d电子数，配对能P (eV)，常见几何构型
METALS = {
    "Ti³⁺ (d¹)":  {"d": 1, "P": 2.5, "geom": ["八面体"]},
    "V³⁺  (d²)":  {"d": 2, "P": 2.6, "geom": ["八面体"]},
    "Cr³⁺ (d³)":  {"d": 3, "P": 2.3, "geom": ["八面体"]},
    "Mn³⁺ (d⁴)":  {"d": 4, "P": 2.8, "geom": ["八面体"]},
    "Fe³⁺ (d⁵)":  {"d": 5, "P": 3.0, "geom": ["八面体"]},
    "Fe²⁺ (d⁶)":  {"d": 6, "P": 2.1, "geom": ["八面体"]},
    "Co³⁺ (d⁶)":  {"d": 6, "P": 2.8, "geom": ["八面体"]},
    "Co²⁺ (d⁷)":  {"d": 7, "P": 2.2, "geom": ["八面体","四面体"]},
    "Ni²⁺ (d⁸)":  {"d": 8, "P": 2.0, "geom": ["八面体","平面四边形"]},
    "Cu²⁺ (d⁹)":  {"d": 9, "P": 1.8, "geom": ["八面体","平面四边形"]},
    "Zn²⁺ (d¹⁰)": {"d":10, "P": 0.0, "geom": ["四面体"]},
    "Mn²⁺ (d⁵)":  {"d": 5, "P": 2.8, "geom": ["八面体","四面体"]},
    "Pt²⁺ (d⁸)":  {"d": 8, "P": 3.5, "geom": ["平面四边形"]},
    "Pd²⁺ (d⁸)":  {"d": 8, "P": 3.2, "geom": ["平面四边形"]},
    "Rh³⁺ (d⁶)":  {"d": 6, "P": 3.1, "geom": ["八面体"]},
}

# 配体：Δo (eV) for 八面体，说明
LIGANDS = {
    "I⁻":      {"delta_o": 0.90, "type": "π供体（弱场）"},
    "Br⁻":     {"delta_o": 1.05, "type": "π供体（弱场）"},
    "Cl⁻":     {"delta_o": 1.20, "type": "π供体（弱场）"},
    "F⁻":      {"delta_o": 1.40, "type": "π供体（弱场）"},
    "OH⁻":     {"delta_o": 1.55, "type": "π供体（弱场）"},
    "H₂O":     {"delta_o": 1.80, "type": "纯σ供体（中场）"},
    "NCS⁻":    {"delta_o": 2.00, "type": "纯σ供体（中场）"},
    "NH₃":     {"delta_o": 2.20, "type": "纯σ供体（中场）"},
    "en":      {"delta_o": 2.40, "type": "纯σ供体（中场，螯合）"},
    "bipy":    {"delta_o": 2.60, "type": "π受体（较强场）"},
    "phen":    {"delta_o": 2.70, "type": "π受体（较强场）"},
    "NO₂⁻":   {"delta_o": 2.80, "type": "π受体（强场）"},
    "CN⁻":     {"delta_o": 3.20, "type": "π受体（强场）"},
    "CO":      {"delta_o": 3.50, "type": "π受体（最强场）"},
}

# 几何构型的 Δ 缩放因子（相对八面体）
GEOM_SCALE = {
    "八面体":    1.00,
    "四面体":    0.44,
    "平面四边形": 1.30,  # 近似
}

# ── 轨道填充计算 ────────────────────────────────────────────────────────
def fill_octahedral(n, high_spin):
    if high_spin:
        # 先各填1，再配对
        slots = [0]*5  # t2g×3 + eg×2
        rem = n
        for i in range(5):
            if rem > 0: slots[i]=1; rem-=1
        for i in range(5):
            if rem > 0 and slots[i]==1: slots[i]=2; rem-=1
        t2g = sum(slots[:3])
        eg  = sum(slots[3:])
        base_pairs = max(n-5,0)
    else:
        t2g = min(n,6)
        eg  = max(n-6,0)
        def pairs(t,e):
            return max(t-3,0)+max(e-1,0)
        base_pairs = pairs(t2g,eg)
    # 高自旋基准配对数
    hs_base = max(n-5,0)
    extra_pairs = base_pairs - hs_base if not high_spin else 0
    return t2g, eg, extra_pairs

def calc_cfse_oct(n, high_spin):
    t2g, eg, extra_pairs = fill_octahedral(n, high_spin)
    cfse_dq = round(-0.4*t2g + 0.6*eg, 2)
    unpaired = count_unpaired_oct(n, high_spin)
    return t2g, eg, extra_pairs, cfse_dq, unpaired

def count_unpaired_oct(n, high_spin):
    if high_spin:
        slots = [0]*5
        rem = n
        for i in range(5):
            if rem>0: slots[i]=1; rem-=1
        for i in range(5):
            if rem>0 and slots[i]==1: slots[i]=2; rem-=1
    else:
        t=min(n,6); e=max(n-6,0)
        t_slots=[0,0,0]; rem=t
        for i in range(3): t_slots[i]=min(rem,2); rem=max(rem-2,0)
        e_slots=[0,0]; rem=e
        for i in range(2): e_slots[i]=min(rem,2); rem=max(rem-2,0)
        slots=t_slots+e_slots
    return sum(1 for x in slots if x==1)

def spin_str(count):
    return {"0":"□","1":"↑","2":"↑↓"}.get(str(count),"□")

def orbital_html(n, high_spin, color_t, color_e):
    t2g, eg, _ = fill_octahedral(n, high_spin)
    if high_spin:
        slots=[0]*5; rem=n
        for i in range(5):
            if rem>0: slots[i]=1; rem-=1
        for i in range(5):
            if rem>0 and slots[i]==1: slots[i]=2; rem-=1
    else:
        t=min(n,6); e_=max(n-6,0)
        ts=[0,0,0]; rem=t
        for i in range(3): ts[i]=min(rem,2); rem=max(rem-2,0)
        es=[0,0]; rem=e_
        for i in range(2): es[i]=min(rem,2); rem=max(rem-2,0)
        slots=ts+es

    def box(s,col):
        sym = spin_str(s)
        return f'<span style="font-size:18px;color:{col};letter-spacing:2px">{sym}</span>'

    eg_boxes  = "　".join(box(slots[3+i], color_e) for i in range(2))
    t2g_boxes = "　".join(box(slots[i],   color_t) for i in range(3))

    return f"""
    <div style="background:white;border-radius:12px;padding:1rem 1.2rem;
                border:0.5px solid #eee;text-align:center">
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px">
        <div style="font-size:11px;color:{color_e};width:36px;text-align:right;font-weight:600">eₘ</div>
        <div style="border-top:2px solid {color_e};flex:1;padding-top:6px">{eg_boxes}</div>
        <div style="font-size:10px;color:{color_e}">+0.6Δ</div>
      </div>
      <div style="height:16px;text-align:center;font-size:10px;color:#ccc">── Δ ──</div>
      <div style="display:flex;align-items:center;gap:10px">
        <div style="font-size:11px;color:{color_t};width:36px;text-align:right;font-weight:600">t₂ₘ</div>
        <div style="border-top:2px solid {color_t};flex:1;padding-top:6px">{t2g_boxes}</div>
        <div style="font-size:10px;color:{color_t}">−0.4Δ</div>
      </div>
    </div>"""

# ── 主渲染函数 ───────────────────────────────────────────────────────────
def render_cfse_tool():
    col_m, col_l, col_g = st.columns([2, 2, 1.5])
    with col_m:
        metal_key = st.selectbox("选择金属离子", list(METALS.keys()), key="cfse_metal")
    with col_l:
        ligand_key = st.selectbox("选择配体", list(LIGANDS.keys()),
                                   index=5, key="cfse_ligand")
    with col_g:
        metal = METALS[metal_key]
        default_geom = metal["geom"][0]
        geom = st.selectbox("几何构型", metal["geom"], key="cfse_geom")

    metal  = METALS[metal_key]
    ligand = LIGANDS[ligand_key]
    n      = metal["d"]
    P      = metal["P"]

    scale  = GEOM_SCALE.get(geom, 1.0)
    delta  = round(ligand["delta_o"] * scale, 2)

    # 判断高低自旋（仅八面体/d4-d7有意义）
    can_spin = (geom == "八面体" and 4 <= n <= 7)
    if n in [0,1,2,3,8,9,10] or geom == "平面四边形":
        # 这些情况只有一种填充
        auto_spin = "低自旋" if (delta > P or n <= 3 or geom == "平面四边形") else "高自旋"
        high_spin_auto = auto_spin == "高自旋"
        spin_label = "—"
    elif geom == "四面体":
        # 四面体几乎总是高自旋
        high_spin_auto = True
        auto_spin = "高自旋（四面体通常高自旋）"
        spin_label = "高自旋"
    else:
        high_spin_auto = delta < P
        auto_spin = "高自旋" if high_spin_auto else "低自旋"
        spin_label = auto_spin

    # Δ vs P 说明
    if geom == "八面体" and 4 <= n <= 7:
        compare = f"Δₒ ({delta:.2f} eV) {'<' if delta<P else '>'} P ({P:.1f} eV) → {auto_spin}"
    elif geom == "四面体":
        compare = f"Δt ≈ {delta:.2f} eV ≪ P ({P:.1f} eV) → 总是高自旋"
    else:
        compare = f"Δ = {delta:.2f} eV，P = {P:.1f} eV"

    # 计算两种情况（八面体d4-d7显示对比，其他只显示一种）
    hs = calc_cfse_oct(n, True)
    ls = calc_cfse_oct(n, False)

    show_both = (geom == "八面体" and 4 <= n <= 7)

    # ── UI ──────────────────────────────────────────
    st.markdown(f"""
    <style>
    .cr-card{{border-radius:14px;padding:1rem 1.2rem;border:0.5px solid #eee;background:#fafafa}}
    .cr-label{{font-size:11px;color:#aaa;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:5px}}
    .cr-val{{font-size:20px;font-weight:600;color:#1a1a1a;line-height:1.2}}
    .cr-sub{{font-size:12px;color:#888;margin-top:2px}}
    .compare-box{{background:#FAEEDA;border-radius:10px;padding:0.75rem 1.2rem;
        border:0.5px solid #F0C060;font-size:13px;color:#633806;margin:0.75rem 0}}
    </style>
    <div class="compare-box">
      <strong>d 电子数：</strong>d{n} &nbsp;|&nbsp;
      <strong>配对能 P：</strong>{P:.1f} eV &nbsp;|&nbsp;
      <strong>配体类型：</strong>{ligand["type"]} &nbsp;|&nbsp;
      <strong>Δ ({geom})：</strong>{delta:.2f} eV<br>
      <strong>判断：</strong>{compare}
    </div>
    """, unsafe_allow_html=True)

    if show_both:
        col_hs, col_ls = st.columns(2)
        sides = [(col_hs,"高自旋",True,"#D85A30","#185FA5"),
                 (col_ls,"低自旋",False,"#712B13","#0C447C")]
    else:
        col_only = st.columns(1)[0]
        sides = [(col_only, auto_spin, high_spin_auto, "#D85A30","#185FA5")]

    for col, label, hs_flag, col_e, col_t in sides:
        t2g_n, eg_n, extra_p, cfse_dq, unpaired = calc_cfse_oct(n, hs_flag)
        cfse_ev  = round(cfse_dq * delta, 3)
        magnetic = "顺磁性" if unpaired > 0 else "反磁性"
        is_auto  = (label == auto_spin or not show_both)
        border   = "2px solid #EF9F27" if is_auto else "0.5px solid #eee"
        badge    = "✓ 实际构型" if is_auto else ""

        with col:
            st.markdown(f"""
            <div style="border-radius:16px;padding:1.2rem;border:{border};
                        background:{'#FFFDF5' if is_auto else '#fafafa'}">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
                <div style="font-size:14px;font-weight:600;color:{'#633806' if is_auto else '#888'}">{label}</div>
                <div style="font-size:11px;color:#EF9F27;font-weight:600">{badge}</div>
              </div>
            """, unsafe_allow_html=True)

            st.markdown(orbital_html(n, hs_flag, col_t, col_e), unsafe_allow_html=True)

            st.markdown(f"""
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px">
              <div class="cr-card">
                <div class="cr-label">CFSE</div>
                <div class="cr-val" style="color:{'#712B13' if is_auto else '#aaa'}">{cfse_dq}Δ</div>
                <div class="cr-sub">≈ {cfse_ev:.2f} eV</div>
              </div>
              <div class="cr-card">
                <div class="cr-label">未配对电子</div>
                <div class="cr-val" style="color:{'#A32D2D' if unpaired>0 else '#085041'}">{unpaired}</div>
                <div class="cr-sub">{magnetic}</div>
              </div>
              <div class="cr-card">
                <div class="cr-label">额外配对能</div>
                <div class="cr-val">{extra_p}P</div>
                <div class="cr-sub">≈ {round(extra_p*P,2):.2f} eV</div>
              </div>
              <div class="cr-card">
                <div class="cr-label">t₂ₘ / eₘ</div>
                <div class="cr-val">{t2g_n} / {eg_n}</div>
                <div class="cr-sub">d{n} 电子分布</div>
              </div>
            </div>
            </div>
            """, unsafe_allow_html=True)

    if show_both:
        hs_data = calc_cfse_oct(n, True)
        ls_data = calc_cfse_oct(n, False)
        net_cfse = round((ls_data[3]-hs_data[3])*delta, 3)
        net_pair = round((ls_data[2]-hs_data[2])*P, 3)
        net_total= round(net_cfse - net_pair, 3)
        favor = "低自旋更稳定" if net_total < 0 else "高自旋更稳定"
        color  = "#085041" if net_total < 0 else "#712B13"
        st.markdown(f"""
        <div style="background:#f8f8fa;border-radius:10px;padding:0.85rem 1.2rem;
                    border:0.5px solid #eee;font-size:13px;color:#444;margin-top:0.75rem">
          <strong>净能量分析：</strong>
          低→高自旋 CFSE 差 = {net_cfse:+.3f} eV，
          额外配对能代价 = {net_pair:+.3f} eV，
          净收益 = <span style="color:{color};font-weight:600">{net_total:+.3f} eV → {favor}</span>
        </div>
        """, unsafe_allow_html=True)
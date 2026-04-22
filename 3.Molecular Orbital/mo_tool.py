import streamlit as st
import plotly.graph_objects as go

PERIODIC_TABLE = {
    "H": {"EN": 2.20, "val": 1, "label": "H (氢)"},
    "B": {"EN": 2.04, "val": 3, "label": "B (硼)"},
    "C": {"EN": 2.55, "val": 4, "label": "C (碳)"},
    "N": {"EN": 3.04, "val": 5, "label": "N (氮)"},
    "O": {"EN": 3.44, "val": 6, "label": "O (氧)"},
    "F": {"EN": 3.98, "val": 7, "label": "F (氟)"},
}

PRESETS = {
    "自定义": None,
    "H₂": ("H", "H"),
    "N₂": ("N", "N"),
    "O₂": ("O", "O"),
    "F₂": ("F", "F"),
    "NO": ("N", "O"),
    "CO": ("C", "O"),
    "HF": ("H", "F"),
    "BN": ("B", "N"),
}


def _fill_electrons(slots, total_e):
    """从低到高填充：非简并轨道直接填满，简并轨道先各填1个再配对"""
    from itertools import groupby
    n = len(slots)
    occ = [0] * n
    rem = total_e

    # 按能量分组
    groups = []
    for _, grp in groupby(range(n), key=lambda i: round(slots[i]['e'], 4)):
        groups.append(list(grp))

    for grp in groups:
        if len(grp) == 1:
            # 非简并轨道：直接填满（最多2个）
            idx = grp[0]
            fill = min(rem, 2)
            occ[idx] = fill
            rem -= fill
        else:
            # 简并轨道：第一轮先每个填1个
            for idx in grp:
                if rem > 0:
                    occ[idx] = 1
                    rem -= 1
            # 第二轮再配对
            for idx in grp:
                if rem > 0 and occ[idx] == 1:
                    occ[idx] = 2
                    rem -= 1

        if rem <= 0:
            break

    return occ

def _get_mo(de, eas, eap, ebs, ebp):
    mix = max(0, 1.8 - de)
    avg_s = (eas + ebs) / 2
    avg_p = (eap + ebp) / 2
    mos = [
        {"lab": "σ2s",  "e": avg_s - 2.0,       "type": "s", "deg": False, "bond": True},
        {"lab": "σ*2s", "e": avg_s + 1.2,        "type": "s", "deg": False, "bond": False},
        {"lab": "σ2p",  "e": avg_p - 2.5 + mix,  "type": "p", "deg": False, "bond": True},
        {"lab": "π2p",  "e": avg_p - 1.2,        "type": "p", "deg": True,  "bond": True},
        {"lab": "π*2p", "e": avg_p + 1.2,        "type": "p", "deg": True,  "bond": False},
        {"lab": "σ*2p", "e": avg_p + 3.2,        "type": "p", "deg": False, "bond": False},
    ]
    return sorted(mos, key=lambda x: x["e"])


def _bo_str(bo):
    return str(int(bo)) if bo == int(bo) else str(bo)


def render_mo_tool():
    col_pre, col_a, col_b = st.columns([2, 2, 2])

    with col_pre:
        preset = st.selectbox("快捷选择分子", list(PRESETS.keys()), key="mo_preset")

    if PRESETS[preset] is not None:
        default_a, default_b = PRESETS[preset]
        st.session_state["mo_a"] = default_a
        st.session_state["mo_b"] = default_b

    with col_a:
        st.selectbox("原子 A", list(PERIODIC_TABLE.keys()),
                     key="mo_a",
                     format_func=lambda k: PERIODIC_TABLE[k]["label"])
    with col_b:
        st.selectbox("原子 B", list(PERIODIC_TABLE.keys()),
                     key="mo_b",
                     format_func=lambda k: PERIODIC_TABLE[k]["label"])

    a_name = st.session_state.get("mo_a", "O")
    b_name = st.session_state.get("mo_b", "F")

    # ── 计算 ──────────────────────────────────────────
    en_a = PERIODIC_TABLE[a_name]["EN"]
    en_b = PERIODIC_TABLE[b_name]["EN"]
    total_e = PERIODIC_TABLE[a_name]["val"] + PERIODIC_TABLE[b_name]["val"]
    delta_en = abs(en_a - en_b)

    ea_s, ea_p = 2.0, 8.5
    e_shift = (en_b - en_a) * 2.2
    eb_s, eb_p = ea_s - e_shift, ea_p - e_shift

    mo_data = _get_mo(delta_en, ea_s, ea_p, eb_s, eb_p)

    slots = []
    for mo in mo_data:
        if mo["deg"]:
            slots.append({"e": mo["e"], "ref": mo, "pos": -1})
            slots.append({"e": mo["e"], "ref": mo, "pos":  1})
        else:
            slots.append({"e": mo["e"], "ref": mo, "pos":  0})

    slot_occ = _fill_electrons(slots, total_e)

    homo_idx = lumo_idx = -1
    for i in range(len(slots)):
        if slot_occ[i] > 0:
            homo_idx = i
    for i in range(len(slots)):
        if slot_occ[i] == 0:
            lumo_idx = i
            break

    # ── 绘图 ──────────────────────────────────────────
    fig = go.Figure()
    W = 0.035
    AX_X, BX_X, MX_C = [0.1, 0.18], [0.82, 0.9], 0.5

    def draw_ao(x, energies, color, name):
        for e, lbl in zip(energies, ["2s", "2p"]):
            fig.add_trace(go.Scatter(
                x=x, y=[e, e], mode='lines',
                line=dict(color=color, width=6), hoverinfo='skip'))
            fig.add_annotation(
                x=sum(x)/2, y=e+0.7,
                text=f"<b>{name} {lbl}</b>",
                showarrow=False, font=dict(color=color, size=12))
            fig.add_annotation(
                x=x[1], y=e-0.1, text=f"{e:.1f}",
                showarrow=False, xanchor='left', yanchor='top',
                font=dict(size=9, color="gray"))

    draw_ao(AX_X, [ea_s, ea_p], "#185FA5", a_name)
    draw_ao(BX_X, [eb_s, eb_p], "#A32D2D", b_name)

    label_y_raw = [s['e'] for s in slots if s['pos'] <= 0]
    adj_y = label_y_raw.copy()
    for i in range(1, len(adj_y)):
        if adj_y[i] - adj_y[i-1] < 0.55:
            adj_y[i] = adj_y[i-1] + 0.55
    label_ptr = 0

    for i, s in enumerate(slots):
        me = s['e']
        offset = s['pos'] * 0.08
        x_r = [MX_C + offset - W, MX_C + offset + W]
        is_anti = "*" in s['ref']['lab']
        l_col = "#2C3E50" if not is_anti else "#6C7A89"

        fig.add_trace(go.Scatter(
            x=x_r, y=[me, me], mode='lines',
            line=dict(color=l_col, width=5), hoverinfo='skip'))

        fig.add_annotation(
            x=x_r[1], y=me-0.1, text=f"{me:.2f}",
            showarrow=False, xanchor='left', yanchor='top',
            font=dict(size=9, color="#95A5A6"))

        if s['pos'] <= 0:
            ty = adj_y[label_ptr]
            txt = f"<i>{s['ref']['lab']}</i>"
            if i == homo_idx:
                txt = f"<b style='color:#C0392B'>HOMO</b><br>{txt}"
            elif i == lumo_idx:
                txt = f"<b style='color:#185FA5'>LUMO</b><br>{txt}"
            fig.add_annotation(
                x=MX_C-0.22, y=ty, text=txt,
                showarrow=False, align="right", xanchor='right',
                font=dict(size=11))
            if abs(ty - me) > 0.1:
                fig.add_trace(go.Scatter(
                    x=[MX_C-0.21, MX_C-0.18], y=[ty, me], mode='lines',
                    line=dict(color="rgba(150,150,150,0.25)", width=0.6),
                    hoverinfo='skip'))
            label_ptr += 1

        if slot_occ[i] == 2:
            fig.add_annotation(x=MX_C+offset, y=me, text="↑↓",
                showarrow=False, font=dict(size=20, color="#B8860B"))
        elif slot_occ[i] == 1:
            fig.add_annotation(x=MX_C+offset, y=me, text="↑",
                showarrow=False, font=dict(size=20, color="#B8860B"))

        pa = ea_s if s['ref']['type'] == 's' else ea_p
        pb = eb_s if s['ref']['type'] == 's' else eb_p
        dot = dict(color="rgba(180,180,180,0.28)", width=0.8, dash='dot')
        fig.add_trace(go.Scatter(
            x=[AX_X[1], x_r[0]], y=[pa, me],
            mode='lines', line=dot, hoverinfo='skip'))
        fig.add_trace(go.Scatter(
            x=[BX_X[0], x_r[1]], y=[pb, me],
            mode='lines', line=dot, hoverinfo='skip'))

    fig.update_layout(
        template="none", height=780, showlegend=False,
        xaxis=dict(visible=False, range=[-0.05, 1.05]),
        yaxis=dict(
            title="Energy (eV)", ticksuffix=" eV",
            gridcolor="#F4F6F7", zeroline=False,
            showline=True, linecolor="#D5DBDB"),
        margin=dict(l=80, r=80, t=20, b=20),
        plot_bgcolor="white", paper_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ── 分析卡片 ──────────────────────────────────────
    bonding_e  = sum(slot_occ[i] for i, s in enumerate(slots) if s['ref']['bond'])
    antibond_e = sum(slot_occ[i] for i, s in enumerate(slots) if not s['ref']['bond'])
    bo         = (bonding_e - antibond_e) / 2
    bo_str     = _bo_str(bo)
    unpaired   = sum(1 for x in slot_occ if x == 1)
    mag_zh     = "顺磁性" if unpaired > 0 else "反磁性"
    mag_en     = "Paramagnetic" if unpaired > 0 else "Diamagnetic"
    homo_e_str = f"{slots[homo_idx]['e']:.2f} eV" if homo_idx >= 0 else "—"
    lumo_e_str = f"{slots[lumo_idx]['e']:.2f} eV" if lumo_idx >= 0 else "—"
    gap_str    = (f"{slots[lumo_idx]['e'] - slots[homo_idx]['e']:.2f} eV"
                  if homo_idx >= 0 and lumo_idx >= 0 else "—")
    exist      = bo > 0

    st.markdown(f"""
    <style>
    .mo-card {{
        border-radius:14px;padding:1rem 1.2rem;
        border:0.5px solid #eee;background:#fafafa;
    }}
    .mo-card-label {{
        font-size:11px;font-weight:600;color:#aaa;
        letter-spacing:0.07em;text-transform:uppercase;margin-bottom:6px;
    }}
    .mo-card-val {{
        font-size:22px;font-weight:700;letter-spacing:-0.02em;line-height:1.2;
    }}
    .mo-card-sub {{
        font-size:12px;color:#888;margin-top:3px;line-height:1.4;
    }}
    </style>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:1rem">
      <div class="mo-card">
        <div class="mo-card-label">理论键级</div>
        <div class="mo-card-val" style="color:#185FA5">{bo_str}</div>
        <div class="mo-card-sub">{'可稳定存在' if exist else '键级为0，不稳定'}</div>
      </div>
      <div class="mo-card">
        <div class="mo-card-label">磁性</div>
        <div class="mo-card-val" style="color:{'#A32D2D' if unpaired>0 else '#0C447C'}">
          {'↑' if unpaired > 0 else '↑↓'}
        </div>
        <div class="mo-card-sub">{mag_zh}<br>{mag_en}</div>
      </div>
      <div class="mo-card">
        <div class="mo-card-label">未成对电子</div>
        <div class="mo-card-val" style="color:#633806">{unpaired}</div>
        <div class="mo-card-sub">个未配对电子</div>
      </div>
      <div class="mo-card">
        <div class="mo-card-label">HOMO 能量</div>
        <div class="mo-card-val" style="color:#C0392B;font-size:17px">{homo_e_str}</div>
        <div class="mo-card-sub">最高已占据轨道</div>
      </div>
      <div class="mo-card">
        <div class="mo-card-label">HOMO–LUMO 能隙</div>
        <div class="mo-card-val" style="color:#534AB7;font-size:17px">{gap_str}</div>
        <div class="mo-card-sub">LUMO: {lumo_e_str}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
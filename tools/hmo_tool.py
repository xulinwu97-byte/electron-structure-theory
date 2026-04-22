import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx

def build_matrix(n_atoms, mode, bond_input=None):
    adj = np.zeros((n_atoms, n_atoms))
    if mode == "自定义多环" and bond_input:
        try:
            pairs = bond_input.replace(' ', '').split(',')
            for pair in pairs:
                if '-' in pair:
                    u, v = map(int, pair.split('-'))
                    if 1 <= u <= n_atoms and 1 <= v <= n_atoms:
                        adj[u-1, v-1] = adj[v-1, u-1] = 1
        except Exception as e:
            st.error(f"连接关系错误：{e}")
    else:
        for i in range(n_atoms - 1):
            adj[i, i+1] = adj[i+1, i] = 1
        if mode == "单环":
            adj[0, -1] = adj[-1, 0] = 1
    return adj

def solve_hmo(adj, n_atoms, n_electrons, beta):
    H = beta * adj
    E, C = np.linalg.eigh(H)
    idx = np.argsort(E)
    E, C = E[idx], C[:, idx]
    occ = np.zeros(n_atoms)
    rem = n_electrons
    for i in range(n_atoms):
        if rem >= 2: occ[i] = 2; rem -= 2
        elif rem == 1: occ[i] = 1; rem = 0; break
    rho = np.sum((C**2) * occ, axis=1)
    P = C @ np.diag(occ) @ C.T
    Fmax = np.sqrt(3)
    F = np.array([Fmax - np.sum(P[k, np.where(adj[k]==1)[0]]) for k in range(n_atoms)])
    occ_idx = np.where(occ > 0)[0]
    homo_idx = int(np.max(occ_idx)) if occ_idx.size > 0 else None
    lumo_idx = homo_idx + 1 if (homo_idx is not None and homo_idx + 1 < n_atoms) else None
    return E, C, occ, rho, P, F, homo_idx, lumo_idx

def get_layout(n_atoms, mode, adj):
    if mode == "线型链":
        x = np.linspace(-n_atoms/2, n_atoms/2, n_atoms)
        y = np.zeros(n_atoms)
    elif mode == "单环":
        theta = np.linspace(0, 2*np.pi, n_atoms, endpoint=False)
        x = 2.5 * np.cos(theta); y = 2.5 * np.sin(theta)
    else:
        G = nx.from_numpy_array(adj)
        pos = nx.spring_layout(G, seed=42)
        x = np.array([pos[i][0] * 6 for i in range(n_atoms)])
        y = np.array([pos[i][1] * 6 for i in range(n_atoms)])
    return x, y

def plot_mo_levels(E, C, occ, n_atoms, beta, homo_idx, lumo_idx, selected_mo):
    fig = go.Figure()
    unique_e, counts = np.unique(np.round(E, 6), return_counts=True)
    e_offset = {e: 0 for e in unique_e}

    for mo in range(n_atoms):
        curr_e = E[mo]
        xc = curr_e / beta
        elabel = f"α {'+' if xc >= 0 else ''}{xc:.3f}β"
        er = np.round(curr_e, 6)
        ndeg = dict(zip(unique_e, counts))[er]
        jitter = (e_offset[er] - (ndeg-1)/2) * 0.4 if ndeg > 1 else 0
        e_offset[er] += 1
        is_sel = (mo == selected_mo)

        if is_sel:
            if mo == homo_idx: lc = "#1D9E75"
            elif mo == lumo_idx: lc = "#EF9F27"
            else: lc = "#534AB7"
        else:
            lc = "rgba(180,180,180,0.25)"

        bx = np.arange(1, n_atoms+1) + jitter
        fig.add_trace(go.Scatter(
            x=bx, y=[curr_e]*n_atoms, mode='markers',
            marker=dict(
                size=14 + 70*np.abs(C[:, mo]),
                color=['#D85A30' if c > 0 else '#185FA5' for c in C[:, mo]],
                line=dict(width=1, color='black'),
                opacity=1.0 if is_sel else 0.12
            ),
            hovertemplate=[
                f"<b>MO {mo+1}</b><br>能量: {elabel}<br>原子: {i+1}<br>系数 c: {c:.3f}<extra></extra>"
                for i, c in enumerate(C[:, mo])
            ],
            showlegend=False
        ))
        fig.add_shape(type="line",
            x0=min(bx)-0.3, x1=max(bx)+0.3, y0=curr_e, y1=curr_e,
            line=dict(color=lc, width=4 if is_sel else 1,
                      dash=None if is_sel else "dot"))

        # 电子箭头
        if occ[mo] > 0:
            for spin, dx in enumerate([-0.15, 0.15][:int(occ[mo])]):
                fig.add_annotation(
                    x=n_atoms/2+dx, y=curr_e,
                    text="↑" if spin == 0 else "↓",
                    showarrow=False,
                    font=dict(size=14, color="#B8860B"),
                    xref="x", yref="y"
                )

    if homo_idx is not None:
        fig.add_annotation(x=n_atoms+1.2, y=E[homo_idx],
            text=f"<b>HOMO</b>", showarrow=True, arrowhead=2,
            font=dict(color="#1D9E75", size=12))
    if lumo_idx is not None:
        fig.add_annotation(x=n_atoms+1.2, y=E[lumo_idx],
            text=f"<b>LUMO</b>", showarrow=True, arrowhead=2,
            font=dict(color="#EF9F27", size=12))

    fig.update_layout(
        height=500,
        margin=dict(l=20, r=80, t=20, b=40),
        xaxis=dict(title="原子轨道编号", range=[0, n_atoms+2.5]),
        yaxis=dict(title="能量（α + xβ）"),
        paper_bgcolor='white', plot_bgcolor='#fafafa'
    )
    return fig

def plot_pi_system(n_atoms, mode, adj, rho, P, F, x_p, y_p):
    fig = go.Figure()
    rho_min, rho_max = np.min(rho), np.max(rho)
    cs = px.colors.sequential.Teal

    for i in range(n_atoms):
        for j in range(i+1, n_atoms):
            if adj[i, j] == 1:
                lw = 1.5 + 5 * abs(P[i, j])
                fig.add_trace(go.Scatter(
                    x=[x_p[i], x_p[j]], y=[y_p[i], y_p[j]], mode='lines',
                    line=dict(width=lw, color='#ccc'), hoverinfo='skip', showlegend=False))

    for i in range(n_atoms):
        norm = (rho[i]-rho_min)/(rho_max-rho_min) if rho_max != rho_min else 0.5
        ac = cs[int(norm * (len(cs)-1))]
        fig.add_trace(go.Scatter(
            x=[x_p[i]], y=[y_p[i]], mode='markers+text',
            marker=dict(size=42, color=ac, line=dict(width=2, color='#555')),
            text=[f"C{i+1}"],
            textposition="middle center",
            textfont=dict(size=11, color='white'),
            hovertemplate=f"<b>C{i+1}</b><br>电荷密度 ρ = {rho[i]:.3f}<br>自由价 F = {F[i]:.3f}<extra></extra>",
            showlegend=False
        ))

    for i in range(n_atoms):
        for j in range(i+1, n_atoms):
            if adj[i, j] == 1:
                mx, my = (x_p[i]+x_p[j])/2, (y_p[i]+y_p[j])/2
                fig.add_annotation(x=mx, y=my-0.3,
                    text=f"<span style='font-size:10px;color:#534AB7'>p={P[i,j]:.3f}</span>",
                    showarrow=False)

    fig.update_layout(
        height=380,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False, range=[min(x_p)-1.8, max(x_p)+1.8]),
        yaxis=dict(visible=False, range=[min(y_p)-1.2, max(y_p)+1.8]),
        paper_bgcolor='white', plot_bgcolor='white'
    )
    return fig

def render_hmo_tool():
    """主入口，直接调用渲染 HMO 小工具"""

    # ── 参数输入 ─────────────────────────────────────
    col1, col2 = st.columns([1, 1])
    with col1:
        mode = st.radio("体系类型", ["线型链", "单环", "自定义多环"],
                        horizontal=True, key="hmo_mode")
        n_atoms = st.slider("共轭原子数", 2, 20, 6, key="hmo_natoms")
    with col2:
        n_electrons = st.slider("π 电子数", 0, 2*n_atoms, n_atoms, key="hmo_nelec")
        beta = st.slider("β 值（eV，负值）", -3.0, -0.1, -1.0, step=0.1, key="hmo_beta")

    bond_input = None
    if mode == "自定义多环":
        st.info("示例（萘，10个原子）：1-2, 2-3, 3-4, 4-5, 5-6, 6-1, 1-7, 7-8, 8-9, 9-10, 10-2")
        bond_input = st.text_input("定义化学键（格式：原子i-原子j，逗号分隔）",
                                    value="1-2, 2-3, 3-4, 4-5, 5-6, 6-1, 1-7, 7-8, 8-9, 9-10, 10-2",
                                    key="hmo_bonds")

    # ── 计算 ─────────────────────────────────────────
    adj = build_matrix(n_atoms, mode, bond_input)
    E, C, occ, rho, P, F, homo_idx, lumo_idx = solve_hmo(adj, n_atoms, n_electrons, beta)
    x_p, y_p = get_layout(n_atoms, mode, adj)

    # ── 摘要卡片 ─────────────────────────────────────
    total_E = np.sum(E * occ)
    xc_vals = E / beta
    homo_e_str = f"α {'+' if xc_vals[homo_idx]>=0 else ''}{xc_vals[homo_idx]:.3f}β" if homo_idx is not None else "—"
    lumo_e_str = f"α {'+' if xc_vals[lumo_idx]>=0 else ''}{xc_vals[lumo_idx]:.3f}β" if lumo_idx is not None else "—"
    gap = abs(E[lumo_idx] - E[homo_idx]) if (homo_idx is not None and lumo_idx is not None) else 0
    unpaired = int(np.sum(occ == 1))
    mag = "顺磁性" if unpaired > 0 else "反磁性"

    # 离域能（与同数孤立双键对比）
    n_double = n_electrons // 2
    e_ref = n_double * 2 * (beta + 0)  # 孤立乙烯参考：每个双键 2α + 2β
    e_pi = total_E
    deloc_str = f"{(e_pi - n_double*2*beta)/abs(beta):.3f}|β|" if beta != 0 else "—"

    st.markdown(f"""
    <style>
    .hmo-card{{border-radius:12px;padding:0.85rem 1rem;border:0.5px solid #eee;background:#fafafa}}
    .hmo-label{{font-size:11px;color:#aaa;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:4px}}
    .hmo-val{{font-size:17px;font-weight:600;color:#1a1a1a;line-height:1.2}}
    .hmo-sub{{font-size:11px;color:#888;margin-top:2px}}
    </style>
    <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:1rem 0">
      <div class="hmo-card">
        <div class="hmo-label">HOMO 能量</div>
        <div class="hmo-val" style="font-size:14px;color:#1D9E75">{homo_e_str}</div>
        <div class="hmo-sub">最高占据轨道</div>
      </div>
      <div class="hmo-card">
        <div class="hmo-label">LUMO 能量</div>
        <div class="hmo-val" style="font-size:14px;color:#EF9F27">{lumo_e_str}</div>
        <div class="hmo-sub">最低空轨道</div>
      </div>
      <div class="hmo-card">
        <div class="hmo-label">HOMO-LUMO 能隙</div>
        <div class="hmo-val" style="color:#534AB7">{gap:.3f} eV</div>
        <div class="hmo-sub">β = {beta:.1f} eV</div>
      </div>
      <div class="hmo-card">
        <div class="hmo-label">磁性</div>
        <div class="hmo-val" style="color:{'#A32D2D' if unpaired>0 else '#085041'}">{mag}</div>
        <div class="hmo-sub">未配对 {unpaired} 个电子</div>
      </div>
      <div class="hmo-card">
        <div class="hmo-label">离域能</div>
        <div class="hmo-val" style="font-size:14px;color:#712B13">{deloc_str}</div>
        <div class="hmo-sub">相对孤立双键</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MO 能级图 ─────────────────────────────────────
    st.markdown("##### π 分子轨道能级图")
    st.caption("红色 = 正系数，蓝色 = 负系数；圆圈大小表示系数绝对值；金色箭头表示电子")
    selected_mo = st.select_slider(
        "高亮显示 MO", options=range(1, n_atoms+1),
        value=(homo_idx+1 if homo_idx is not None else 1),
        key="hmo_selmo"
    ) - 1
    fig_mo = plot_mo_levels(E, C, occ, n_atoms, beta, homo_idx, lumo_idx, selected_mo)
    st.plotly_chart(fig_mo, use_container_width=True)

    # ── π 体系结构图 ─────────────────────────────────
    st.markdown("##### π 体系结构图")
    st.caption("颜色深浅表示电荷密度 ρ（越深越大）；键上数字为 π 键级；悬停查看详情")
    fig_pi = plot_pi_system(n_atoms, mode, adj, rho, P, F, x_p, y_p)
    st.plotly_chart(fig_pi, use_container_width=True)

    # ── 数据表 ───────────────────────────────────────
    with st.expander("查看原子数据详表"):
        import pandas as pd
        df = pd.DataFrame({
            "原子": [f"C{i+1}" for i in range(n_atoms)],
            "电荷密度 ρ": np.round(rho, 4),
            "自由价 F": np.round(F, 4),
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

    with st.expander("查看 MO 能量表"):
        import pandas as pd
        xc = E / beta
        df2 = pd.DataFrame({
            "MO": [f"MO {i+1}" for i in range(n_atoms)],
            "能量（α + xβ）": [f"α {'+' if xc[i]>=0 else ''}{xc[i]:.4f}β" for i in range(n_atoms)],
            "能量 (eV)": np.round(E, 4),
            "占据电子数": occ.astype(int),
            "标注": ["HOMO" if i==homo_idx else ("LUMO" if i==lumo_idx else "") for i in range(n_atoms)]
        })
        st.dataframe(df2, use_container_width=True, hide_index=True)

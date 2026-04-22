import numpy as np
import streamlit as st
import plotly.graph_objects as go

GRID = 55

ORBITAL_INFO = {
    "1s":  {"desc": "球形对称，无节点，最低能级", "l": 0},
    "2s":  {"desc": "球形对称，1个径向节点（节点球面）", "l": 0},
    "2px": {"desc": "哑铃形，沿 x 轴分布，1个角节点（yz 平面）", "l": 1},
    "2py": {"desc": "哑铃形，沿 y 轴分布，1个角节点（xz 平面）", "l": 1},
    "2pz": {"desc": "哑铃形，沿 z 轴分布，1个角节点（xy 平面）", "l": 1},
    "3s":  {"desc": "球形对称，2个径向节点", "l": 0},
    "3px": {"desc": "哑铃形，沿 x 轴，1角节点 + 1径向节点", "l": 1},
    "3py": {"desc": "哑铃形，沿 y 轴，1角节点 + 1径向节点", "l": 1},
    "3pz": {"desc": "哑铃形，沿 z 轴，1角节点 + 1径向节点", "l": 1},
    "3dxy":   {"desc": "四叶形，位于 xy 平面，2个角节点", "l": 2},
    "3dxz":   {"desc": "四叶形，位于 xz 平面，2个角节点", "l": 2},
    "3dyz":   {"desc": "四叶形，位于 yz 平面，2个角节点", "l": 2},
    "3dz2":   {"desc": "轴向哑铃 + 环状，沿 z 轴，2个角节点", "l": 2},
    "3dx2y2": {"desc": "四叶形，沿 x/y 轴，2个角节点", "l": 2},
    "4s":  {"desc": "球形对称，3个径向节点", "l": 0},
    "4px": {"desc": "哑铃形，沿 x 轴，1角节点 + 2径向节点", "l": 1},
    "4py": {"desc": "哑铃形，沿 y 轴，1角节点 + 2径向节点", "l": 1},
    "4pz": {"desc": "哑铃形，沿 z 轴，1角节点 + 2径向节点", "l": 1},
    "4dxy":   {"desc": "四叶形，位于 xy 平面，2角节点 + 1径向节点", "l": 2},
    "4dxz":   {"desc": "四叶形，位于 xz 平面，2角节点 + 1径向节点", "l": 2},
    "4dyz":   {"desc": "四叶形，位于 yz 平面，2角节点 + 1径向节点", "l": 2},
    "4dz2":   {"desc": "轴向哑铃 + 环状，沿 z 轴，2角节点 + 1径向节点", "l": 2},
    "4dx2y2": {"desc": "四叶形，沿 x/y 轴，2角节点 + 1径向节点", "l": 2},
    "4fxyz":      {"desc": "八叶形，3个角节点", "l": 3},
    "4fxz2":      {"desc": "复杂形态，3个角节点", "l": 3},
    "4fyz2":      {"desc": "复杂形态，3个角节点", "l": 3},
    "4fz3":       {"desc": "沿 z 轴，多层结构，3个角节点", "l": 3},
    "4fx(x2-3y2)": {"desc": "复杂多叶形，3个角节点", "l": 3},
    "4fy(3x2-y2)": {"desc": "复杂多叶形，3个角节点", "l": 3},
    "4fx2-y2z":    {"desc": "复杂多叶形，3个角节点", "l": 3},
}

def _grid(lim):
    x = np.linspace(-lim, lim, GRID)
    X, Y, Z = np.meshgrid(x, x, x)
    R = np.sqrt(X**2 + Y**2 + Z**2) + 1e-12
    return X, Y, Z, R

@st.cache_data(show_spinner=False)
def compute_psi(orbital):
    lim_map = {
        "4f": 70, "4": 40, "3d": 30
    }
    lim = 25
    for k, v in lim_map.items():
        if orbital.startswith(k):
            lim = v; break

    X, Y, Z, R = _grid(lim)

    # 精确波函数
    if orbital == "1s":
        psi = np.exp(-R)
    elif orbital == "2s":
        psi = (2 - R) * np.exp(-R/2)
    elif orbital == "2px":
        psi = R * np.exp(-R/2) * X/R
    elif orbital == "2py":
        psi = R * np.exp(-R/2) * Y/R
    elif orbital == "2pz":
        psi = R * np.exp(-R/2) * Z/R
    elif orbital == "3s":
        rho = 2*R/3
        psi = np.exp(-R/3) * (27 - 18*rho + 2*rho**2)
    elif orbital == "3px":
        rho = 2*R/3; psi = R*(4-rho)*np.exp(-R/3)*X/R
    elif orbital == "3py":
        rho = 2*R/3; psi = R*(4-rho)*np.exp(-R/3)*Y/R
    elif orbital == "3pz":
        rho = 2*R/3; psi = R*(4-rho)*np.exp(-R/3)*Z/R
    elif orbital == "3dxy":
        psi = R**2*np.exp(-R/3)*X*Y/R**2
    elif orbital == "3dxz":
        psi = R**2*np.exp(-R/3)*X*Z/R**2
    elif orbital == "3dyz":
        psi = R**2*np.exp(-R/3)*Y*Z/R**2
    elif orbital == "3dz2":
        psi = R**2*np.exp(-R/3)*(3*Z**2-R**2)/R**2
    elif orbital == "3dx2y2":
        psi = R**2*np.exp(-R/3)*(X**2-Y**2)/R**2
    elif orbital == "4s":
        rho = R/2
        psi = np.exp(-rho)*(24 - 36*rho + 12*rho**2 - rho**3)
    elif orbital == "4px":
        rho = 2*R/4; psi = R*(6-rho)*np.exp(-R/4)*X/R
    elif orbital == "4py":
        rho = 2*R/4; psi = R*(6-rho)*np.exp(-R/4)*Y/R
    elif orbital == "4pz":
        rho = 2*R/4; psi = R*(6-rho)*np.exp(-R/4)*Z/R
    elif orbital == "4dxy":
        psi = R**2*np.exp(-R/4)*X*Y/R**2
    elif orbital == "4dxz":
        psi = R**2*np.exp(-R/4)*X*Z/R**2
    elif orbital == "4dyz":
        psi = R**2*np.exp(-R/4)*Y*Z/R**2
    elif orbital == "4dz2":
        psi = R**2*np.exp(-R/4)*(3*Z**2-R**2)/R**2
    elif orbital == "4dx2y2":
        psi = R**2*np.exp(-R/4)*(X**2-Y**2)/R**2
    elif orbital == "4fxyz":
        psi = R**3*np.exp(-R/4)*X*Y*Z/R**3
    elif orbital == "4fxz2":
        psi = R**3*np.exp(-R/4)*X*(5*Z**2-R**2)/R**3
    elif orbital == "4fyz2":
        psi = R**3*np.exp(-R/4)*Y*(5*Z**2-R**2)/R**3
    elif orbital == "4fz3":
        psi = R**3*np.exp(-R/4)*(5*Z**3-3*Z*R**2)/R**3
    elif orbital == "4fx(x2-3y2)":
        psi = R**3*np.exp(-R/4)*X*(X**2-3*Y**2)/R**3
    elif orbital == "4fy(3x2-y2)":
        psi = R**3*np.exp(-R/4)*Y*(3*X**2-Y**2)/R**3
    elif orbital == "4fx2-y2z":
        psi = R**3*np.exp(-R/4)*(X**2-Y**2)*Z/R**3
    else:
        psi = np.zeros_like(R)

    return psi, lim

def plot_orbital(orbital, axis='iso'):
    psi, lim = compute_psi(orbital)
    pos = np.copy(psi); pos[pos < 0] = 0
    neg = np.abs(np.minimum(psi, 0))

    x = np.linspace(-lim, lim, GRID)
    X, Y, Z, _ = _grid(lim)

    fig = go.Figure()
    if pos.max() > 1e-8:
        fig.add_trace(go.Isosurface(
            x=X.flatten(), y=Y.flatten(), z=Z.flatten(),
            value=pos.flatten(),
            isomin=pos.max()*0.15, isomax=pos.max(),
            surface_count=2,
            colorscale=[[0,'#ffbbbb'],[1,'#cc2200']],
            opacity=0.55, showscale=False, name="正相位"))
    if neg.max() > 1e-8:
        fig.add_trace(go.Isosurface(
            x=X.flatten(), y=Y.flatten(), z=Z.flatten(),
            value=neg.flatten(),
            isomin=neg.max()*0.15, isomax=neg.max(),
            surface_count=2,
            colorscale=[[0,'#bbbbff'],[1,'#1122cc']],
            opacity=0.55, showscale=False, name="负相位"))

    cam_presets = {
        'iso': dict(eye=dict(x=1.6, y=1.6, z=1.2)),
        'x':   dict(eye=dict(x=3,   y=0,   z=0)),
        'y':   dict(eye=dict(x=0,   y=3,   z=0)),
        'z':   dict(eye=dict(x=0,   y=0,   z=3)),
        'xy':  dict(eye=dict(x=1.8, y=1.8, z=0.1)),
    }

    fig.update_layout(
        height=520,
        scene=dict(
            xaxis=dict(title='x', backgroundcolor='rgb(245,245,248)',
                       gridcolor='white', showbackground=True),
            yaxis=dict(title='y', backgroundcolor='rgb(245,245,248)',
                       gridcolor='white', showbackground=True),
            zaxis=dict(title='z', backgroundcolor='rgb(248,248,245)',
                       gridcolor='white', showbackground=True),
            aspectmode='cube',
            camera=cam_presets.get(axis, cam_presets['iso'])
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor='white',
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.8)',
                    bordercolor='#eee', borderwidth=1)
    )
    return fig


def render_tool():
    """主入口，直接调用即可渲染小工具"""

    orbital_options = {
        "n=1": ["1s"],
        "n=2": ["2s","2px","2py","2pz"],
        "n=3": ["3s","3px","3py","3pz","3dxy","3dxz","3dyz","3dz2","3dx2y2"],
        "n=4": ["4s","4px","4py","4pz","4dxy","4dxz","4dyz","4dz2","4dx2y2",
                "4fxyz","4fxz2","4fyz2","4fz3","4fx(x2-3y2)","4fy(3x2-y2)","4fx2-y2z"]
    }

    col_sel, col_view, col_info = st.columns([1.5, 2, 2])

    with col_sel:
        n_group = st.selectbox("主量子数", list(orbital_options.keys()), key="ot_n")
        orbital = st.selectbox("选择轨道", orbital_options[n_group], key="ot_orb")

    with col_view:
        axis = st.radio(
            "观察视角",
            ["iso（默认）","沿 x 轴","沿 y 轴","沿 z 轴","xy 平面俯视"],
            horizontal=False, key="ot_axis"
        )
        axis_map = {"iso（默认）":"iso","沿 x 轴":"x","沿 y 轴":"y","沿 z 轴":"z","xy 平面俯视":"xy"}
        chosen_axis = axis_map[axis]

    with col_info:
        info = ORBITAL_INFO.get(orbital, {})
        st.markdown(f"""
        <div style="background:#fafafa;border:0.5px solid #eee;border-radius:12px;
                    padding:1rem 1.2rem;margin-top:0.5rem">
          <div style="font-size:22px;font-weight:800;color:#534AB7;margin-bottom:6px">
            {orbital}
          </div>
          <div style="font-size:12px;color:#888;margin-bottom:8px">
            角量子数 l = {info.get('l','?')}
          </div>
          <div style="font-size:13px;color:#444;line-height:1.65">
            {info.get('desc','—')}
          </div>
          <div style="margin-top:10px;display:flex;gap:8px">
            <span style="font-size:11px;padding:2px 8px;border-radius:99px;
                         background:#ffeeee;color:#cc2200;font-weight:500">
              红 = 正相位（ψ > 0）
            </span>
            <span style="font-size:11px;padding:2px 8px;border-radius:99px;
                         background:#eeeeff;color:#1122cc;font-weight:500">
              蓝 = 负相位（ψ < 0）
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with st.spinner(f"计算 {orbital} 轨道..."):
        fig = plot_orbital(orbital, chosen_axis)
    st.plotly_chart(fig, use_container_width=True)
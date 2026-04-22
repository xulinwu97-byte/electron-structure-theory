import streamlit as st
import streamlit.components.v1 as components
import base64
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
from orbital_tool import render_tool
from utils import load_md, page_header, page_footer, divider

st.set_page_config(layout="wide", page_title="原子轨道理论", page_icon="🌀")

page_header("ao", desc="求解氢原子薛定谔方程，得到一系列波函数解——每一个解对应一个原子轨道，描述电子在空间中的概率分布。")

def img_b64(path):
    try:
        with open(path, "rb") as f:
            ext = path.split(".")[-1].lower()
            mime = "image/jpeg" if ext in ["jpg","jpeg"] else "image/png"
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"
    except:
        return ""

img_22 = img_b64("images/2.2.png")
img_23 = img_b64("images/2.3.png")
img_p  = img_b64("images/p angular nodes.png")
img_d  = img_b64("images/d angular nodes.png")
img_r  = img_b64("images/radial nodes.jpg")
img_24 = img_b64("images/2.4.png")

HTML = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{
    font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif;
    color:#1a1a1a;background:white;padding:2rem 3rem 4rem;line-height:1.8;
}}
.lead{{
    font-size:16px;color:#555;line-height:1.9;max-width:700px;
    margin-bottom:3rem;padding-left:1.2rem;border-left:3px solid #5DCAA5;
}}
.section{{margin-bottom:3.5rem}}
.section-header{{
    display:flex;align-items:baseline;gap:12px;
    margin-bottom:1.4rem;padding-bottom:0.75rem;
    border-bottom:0.5px solid #f0f0f0;
}}
.section-num{{font-size:12px;font-weight:600;color:#5DCAA5;letter-spacing:0.05em}}
.section-title{{font-size:20px;font-weight:700;letter-spacing:-0.01em;color:#1a1a1a}}
.body-text{{font-size:15px;color:#444;line-height:1.9;max-width:740px;margin-bottom:1rem}}
.body-text strong{{color:#1a1a1a;font-weight:600}}

/* 2.2 节：紧凑表格 + 右侧图 */
.section-22-grid{{display:grid;grid-template-columns:1fr 260px;gap:2rem;align-items:start}}

/* 量子数表格（列更窄）*/
.qn-table{{width:100%;border-collapse:collapse;font-size:13px;margin:1rem 0}}
.qn-table th{{
    background:#E1F5EE;padding:8px 10px;
    border:1px solid #9FE1CB;font-weight:600;
    color:#085041;text-align:left;white-space:nowrap;
}}
.qn-table td{{padding:8px 10px;border:1px solid #eee;color:#444;vertical-align:top;font-size:13px}}
.qn-table tr:hover td{{background:#f8fffe}}
.qn-badge{{
    display:inline-block;font-size:12px;font-weight:700;
    padding:2px 8px;border-radius:6px;white-space:nowrap;
}}

.two-col{{display:grid;grid-template-columns:1fr 340px;gap:2rem;align-items:start}}
.two-col-rev{{display:grid;grid-template-columns:340px 1fr;gap:2rem;align-items:start}}

.img-card{{border-radius:14px;overflow:hidden;border:0.5px solid #eee;background:#fafafa}}
.img-card img{{width:100%;display:block}}
.img-caption{{font-size:11px;color:#aaa;text-align:center;padding:8px 12px;border-top:0.5px solid #eee}}
.img-full{{border-radius:14px;overflow:hidden;border:0.5px solid #eee;background:#fafafa;margin:1.25rem 0}}
.img-full img{{width:100%;display:block}}
.img-full .img-caption{{border-top:0.5px solid #eee}}

.blockquote{{
    border-left:3px solid #5DCAA5;background:#E1F5EE18;
    padding:0.75rem 1.2rem;border-radius:0 10px 10px 0;
    font-size:15px;color:#085041;margin:1rem 0;
}}
.formula-box{{
    background:#E1F5EE;border-radius:14px;padding:1.2rem 1.5rem;
    margin:1rem 0;border:0.5px solid #9FE1CB;
    text-align:center;font-size:20px;color:#085041;
}}

/* 2.3 节：节点卡片 */
.orbital-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:1.25rem 0}}
.orbital-card{{border-radius:14px;padding:1.2rem;border:0.5px solid #eee;background:#fafafa}}
.orbital-card.s{{border-color:#9FE1CB;background:#E1F5EE18}}
.orbital-card.p{{border-color:#CECBF6;background:#EEEDFE18}}
.orbital-card.d{{border-color:#B5D4F4;background:#E6F1FB18}}
.orbital-type{{font-size:22px;font-weight:800;margin-bottom:6px}}
.orbital-title{{font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:6px}}
.orbital-desc{{font-size:12px;color:#555;line-height:1.65}}
.node-badge{{
    display:inline-flex;align-items:center;gap:4px;
    font-size:11px;padding:3px 9px;border-radius:99px;
    font-weight:600;margin-top:8px;
}}

/* 2.4 节：填充规则 */
.rules-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:1.25rem 0}}
.rule-card{{border-radius:14px;padding:1.2rem;border:0.5px solid #eee;background:#fafafa}}
.rule-num{{
    width:28px;height:28px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    font-size:13px;font-weight:700;margin-bottom:10px;
}}
.rule-title{{font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:4px}}
.rule-en{{font-size:11px;color:#aaa;margin-bottom:8px;font-style:italic}}
.rule-desc{{font-size:12px;color:#555;line-height:1.65}}
.energy-order{{
    background:#EEEDFE;border-radius:14px;
    padding:1.2rem 1.5rem;margin:1rem 0;
    border:0.5px solid #CECBF6;
    display:flex;align-items:center;justify-content:center;
    gap:12px;font-size:18px;font-weight:700;color:#534AB7;
}}
.energy-order span{{color:#888;font-weight:400;font-size:14px}}
.quote{{
    background:linear-gradient(135deg,#E1F5EE,#EEEDFE);
    border-radius:16px;padding:1.5rem 2rem;margin-top:2rem;
    font-size:16px;font-weight:600;color:#085041;
    line-height:1.6;text-align:center;
}}
</style>
</head>
<body>

<p class="lead">
  求解氢原子定态薛定谔方程，可以得到一系列物理上允许的波函数解 \(\Psi\)。
  每一个解对应着原子中的一个量子态——<strong>原子轨道</strong>，
  描述电子在空间中的概率分布模式，而非运动轨迹。
</p>

<!-- 2.1 基本概念 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">2.1</span>
    <span class="section-title">原子轨道的基本概念</span>
  </div>

  <p class="body-text">对氢原子建立定态薛定谔方程：</p>
  <div class="formula-box">\( \hat{{H}}\Psi = E\Psi \)</div>
  <p class="body-text">
    每一个可接受解都对应着一个<strong>原子轨道（Atomic Orbital, AO）</strong>。
  </p>
  <div class="blockquote">
    原子轨道描述的是电子在空间中的<strong>概率分布模式</strong>，而不是运动轨迹。
    其平方 \(|\Psi|^2\) 给出了电子在空间某处出现的概率密度。
  </div>
  <p class="body-text">
    不同的原子轨道具有不同的空间形状和对称性，这些形状直接来源于薛定谔方程的数学解。
    在求解过程中会自然引入一组<strong>量子数</strong>，用于唯一标记每一个轨道。
  </p>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:1rem 0 1.5rem">
    <div style="background:#E1F5EE;border-radius:10px;padding:0.75rem;
                text-align:center;border:0.5px solid #9FE1CB">
      <div style="font-size:18px;font-weight:800;color:#085041">s</div>
      <div style="font-size:12px;color:#555;margin-top:4px">球对称分布</div>
    </div>
    <div style="background:#EEEDFE;border-radius:10px;padding:0.75rem;
                text-align:center;border:0.5px solid #CECBF6">
      <div style="font-size:18px;font-weight:800;color:#3C3489">p</div>
      <div style="font-size:12px;color:#555;margin-top:4px">哑铃形分布</div>
    </div>
    <div style="background:#E6F1FB;border-radius:10px;padding:0.75rem;
                text-align:center;border:0.5px solid #B5D4F4">
      <div style="font-size:18px;font-weight:800;color:#0C447C">d</div>
      <div style="font-size:12px;color:#555;margin-top:4px">复杂空间取向</div>
    </div>
  </div>

  <div class="img-full">
    <img src="{img_22}" alt="原子轨道全览">
    <div class="img-caption">各主量子数 n 下的轨道形状全览（红 = 正相位，蓝 = 负相位）</div>
  </div>
</div>

<!-- 2.2 量子数 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">2.2</span>
    <span class="section-title">量子数与原子轨道的具体描述</span>
  </div>
  <p class="body-text">
    波函数的解必须满足特定的边界条件，导致了一组量子数的出现，
    共同决定了原子轨道的<strong>能量、形状和空间取向</strong>。
  </p>

  <table class="qn-table">
    <tr>
      <th>量子数</th>
      <th>符号</th>
      <th>取值范围</th>
      <th>影响</th>
    </tr>
    <tr>
      <td><strong>主量子数</strong></td>
      <td><span class="qn-badge" style="background:#E1F5EE;color:#085041">\(n\)</span></td>
      <td>\(1,2,3,\dots\)</td>
      <td>\(n\) 越大，能量越高、轨道越大</td>
    </tr>
    <tr>
      <td><strong>角量子数</strong></td>
      <td><span class="qn-badge" style="background:#EEEDFE;color:#3C3489">\(l\)</span></td>
      <td>\(0 \sim n-1\)</td>
      <td>\(l=0,1,2,3\) → s, p, d, f</td>
    </tr>
    <tr>
      <td><strong>磁量子数</strong></td>
      <td><span class="qn-badge" style="background:#E6F1FB;color:#0C447C">\(m_l\)</span></td>
      <td>\(-l \sim +l\)</td>
      <td>决定空间取向数目</td>
    </tr>
    <tr>
      <td><strong>自旋量子数</strong></td>
      <td><span class="qn-badge" style="background:#FAEEDA;color:#633806">\(m_s\)</span></td>
      <td>\(\pm\tfrac{{1}}{{2}}\)</td>
      <td>描述电子自旋（↑ 或 ↓）</td>
    </tr>
  </table>

  <div style="background:#fafafa;border-radius:10px;padding:0.85rem 1rem;
              border:0.5px solid #eee;font-size:13px;color:#444;margin-top:0.75rem">
    根据<strong>泡利不相容原理</strong>，每个原子轨道最多容纳
    <strong>两个自旋相反的电子</strong>。
  </div>

  <div class="img-full" style="margin-top:1.5rem">
    <img src="{img_23}" alt="轨道形状对比">
    <div class="img-caption">s、p、d 轨道形状对比</div>
  </div>
</div>

<!-- 2.3 空间形态与节点 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">2.3</span>
    <span class="section-title">轨道的空间形态与节点</span>
  </div>
  <p class="body-text">
    <strong>节点（Node）</strong>是指电子出现概率为零的区域，分为角节点和径向节点两类。
    角量子数 \(l\) 决定角节点数，主量子数与角量子数之差决定径向节点数。
  </p>
  <div class="orbital-grid">
    <div class="orbital-card s">
      <div class="orbital-type" style="color:#085041">s</div>
      <div class="orbital-title">s 轨道（l = 0）</div>
      <div class="orbital-desc">
        <strong>球对称</strong>分布，无角节点。随 n 增大出现<strong>径向节点</strong>（节点球面）。
        1s 无节点，2s 有 1 个，3s 有 2 个。
      </div>
      <div class="node-badge" style="background:#E1F5EE;color:#085041">
        角节点 0 · 径向节点 n−1
      </div>
    </div>
    <div class="orbital-card p">
      <div class="orbital-type" style="color:#3C3489">p</div>
      <div class="orbital-title">p 轨道（l = 1）</div>
      <div class="orbital-desc">
        <strong>哑铃形</strong>分布，1个穿过原子核的<strong>角节点平面</strong>。
        p<sub>x</sub>、p<sub>y</sub>、p<sub>z</sub> 在空间中彼此正交。
      </div>
      <div class="node-badge" style="background:#EEEDFE;color:#3C3489">
        角节点 1 · 径向节点 n−2
      </div>
    </div>
    <div class="orbital-card d">
      <div class="orbital-type" style="color:#0C447C">d</div>
      <div class="orbital-title">d 轨道（l = 2）</div>
      <div class="orbital-desc">
        含<strong>2个角节点</strong>，形态复杂。分为轴向
        （d<sub>z²</sub>、d<sub>x²-y²</sub>）和轴间
        （d<sub>xy</sub>、d<sub>yz</sub>、d<sub>xz</sub>）两类。
      </div>
      <div class="node-badge" style="background:#E6F1FB;color:#0C447C">
        角节点 2 · 径向节点 n−3
      </div>
    </div>
  </div>

  <!-- 2.3 图片：径向节点在左，角节点在右（对调） -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1.25rem 0">
    <div class="img-card">
      <img src="{img_r}" alt="径向节点">
      <div class="img-caption">s 轨道的径向节点：1s、2s、3s 的电子概率分布</div>
    </div>
    <div class="img-card">
      <img src="{img_d}" alt="p d 角节点">
      <div class="img-caption">p 轨道（1个角节点）与 d 轨道（2个角节点）对比</div>
    </div>
  </div>
</div>

<!-- 2.4 能级排布 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">2.4</span>
    <span class="section-title">多电子原子中的能级排布</span>
  </div>
  <div class="two-col-rev">
    <div class="img-card">
      <img src="{img_24}" alt="构造原理能级图">
      <div class="img-caption">轨道能级顺序与构造原理示意</div>
    </div>
    <div>
      <p class="body-text">
        在多电子原子中，电子间的<strong>库仑排斥</strong>导致轨道能量发生分裂，
        使轨道能量不仅依赖于 n，也依赖于 l。在相同 n 下：
      </p>
      <div class="energy-order">
        s <span>&lt;</span> p <span>&lt;</span> d <span>&lt;</span> f
      </div>
      <p class="body-text" style="margin-top:1rem">电子填充遵循以下三个基本规则：</p>
      <div class="rules-grid">
        <div class="rule-card" style="border-color:#9FE1CB">
          <div class="rule-num" style="background:#E1F5EE;color:#085041">①</div>
          <div class="rule-title">构造原理</div>
          <div class="rule-en">Aufbau Principle</div>
          <div class="rule-desc">电子按能量<strong>由低到高</strong>依次填充。</div>
        </div>
        <div class="rule-card" style="border-color:#CECBF6">
          <div class="rule-num" style="background:#EEEDFE;color:#3C3489">②</div>
          <div class="rule-title">泡利不相容原理</div>
          <div class="rule-en">Pauli Exclusion Principle</div>
          <div class="rule-desc">每个轨道最多容纳<strong>两个自旋相反</strong>的电子。</div>
        </div>
        <div class="rule-card" style="border-color:#B5D4F4">
          <div class="rule-num" style="background:#E6F1FB;color:#0C447C">③</div>
          <div class="rule-title">洪特规则</div>
          <div class="rule-en">Hund's Rule</div>
          <div class="rule-desc">简并轨道中电子优先<strong>单独占据</strong>并保持<strong>平行自旋</strong>。</div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="quote">
  原子轨道的形状、能量与对称性，<br>是理解化学键、分子结构与光谱性质的出发点。
</div>

</body>
</html>
"""

components.html(HTML, height=3500, scrolling=False)

divider()


# ── 3D 轨道可视化小工具 ─────────────────────────────────
st.subheader("🌀 原子轨道三维可视化")
st.caption("选择轨道后自动渲染 ·  支持多视角观察")
render_tool()

page_footer("ao")
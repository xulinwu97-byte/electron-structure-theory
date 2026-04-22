import streamlit as st
import streamlit.components.v1 as components
import base64
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '3.molecular orbital'))
from mo_tool import render_mo_tool
import plotly.graph_objects as go
from utils import load_md, page_header, page_footer, divider

st.set_page_config(layout="wide", page_title="分子轨道理论", page_icon="🔗")

page_header("mo", desc="原子轨道通过线性组合形成分子轨道，电子在整个分子范围内离域运动。LCAO 近似是分子轨道理论的核心计算方法。")

def img_b64(path):
    try:
        with open(path, "rb") as f:
            ext = path.split(".")[-1].lower()
            mime = "image/jpeg" if ext in ["jpg","jpeg"] else "image/png"
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"
    except:
        return ""

img_31  = img_b64("3.molecular orbital/3.1.png")
img_321 = img_b64("3.molecular orbital/3.2.1.png")
img_331 = img_b64("3.molecular orbital/3.3.1.png")
img_332 = img_b64("3.molecular orbital/3.3.2.jpg")
img_333 = img_b64("3.molecular orbital/3.3.3.png")

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
    font-size:16px;color:#555;line-height:1.9;max-width:720px;
    margin-bottom:3rem;padding-left:1.2rem;border-left:3px solid #378ADD;
}}
.section{{margin-bottom:3.5rem}}
.section-header{{
    display:flex;align-items:baseline;gap:12px;
    margin-bottom:1.4rem;padding-bottom:0.75rem;
    border-bottom:0.5px solid #f0f0f0;
}}
.section-num{{font-size:12px;font-weight:600;color:#378ADD;letter-spacing:0.05em}}
.section-title{{font-size:20px;font-weight:700;letter-spacing:-0.01em;color:#1a1a1a}}
.sub-num{{font-size:11px;font-weight:600;color:#378ADD;letter-spacing:0.05em}}
.sub-title{{font-size:17px;font-weight:700;color:#1a1a1a}}
.sub-header{{display:flex;align-items:baseline;gap:10px;margin:1.5rem 0 0.75rem;padding-bottom:0.5rem;border-bottom:0.5px solid #f5f5f5}}
.body-text{{font-size:15px;color:#444;line-height:1.9;max-width:740px;margin-bottom:1rem}}
.body-text strong{{color:#1a1a1a;font-weight:600}}

.two-col{{display:grid;grid-template-columns:1fr 320px;gap:2rem;align-items:start}}
.two-col-rev{{display:grid;grid-template-columns:360px 1fr;gap:2rem;align-items:start}}

.img-card{{border-radius:14px;overflow:hidden;border:0.5px solid #eee;background:#fafafa}}
.img-card img{{width:100%;display:block}}
.img-caption{{font-size:11px;color:#aaa;text-align:center;padding:8px 12px;border-top:0.5px solid #eee}}
.img-full{{border-radius:14px;overflow:hidden;border:0.5px solid #eee;background:#fafafa;margin:1.25rem 0}}
.img-full img{{width:100%;display:block}}
.img-full .img-caption{{border-top:0.5px solid #eee}}

.formula-box{{
    background:#E6F1FB;border-radius:14px;
    padding:1.2rem 1.5rem;margin:1rem 0;
    border:0.5px solid #B5D4F4;text-align:center;
    font-size:20px;color:#0C447C;
}}
.formula-terms{{
    display:flex;gap:10px;margin-top:0.75rem;justify-content:center;flex-wrap:wrap;
}}
.f-term{{
    background:white;border-radius:10px;padding:0.6rem 1rem;
    text-align:center;border:0.5px solid #B5D4F4;
    font-size:13px;color:#555;
}}
.f-term strong{{color:#185FA5}}

.blockquote{{
    border-left:3px solid #378ADD;background:#E6F1FB18;
    padding:0.75rem 1.2rem;border-radius:0 10px 10px 0;
    font-size:15px;color:#0C447C;margin:1rem 0;
}}

/* 表格 */
.mo-table{{width:100%;border-collapse:collapse;font-size:13px;margin:1rem 0}}
.mo-table th{{
    background:#E6F1FB;padding:8px 12px;
    border:1px solid #B5D4F4;font-weight:600;
    color:#0C447C;text-align:left;
}}
.mo-table td{{padding:8px 12px;border:1px solid #eee;color:#444;vertical-align:top}}
.mo-table tr:hover td{{background:#f8fbff}}

/* 三原则卡片 */
.principles{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:1.25rem 0}}
.prin-card{{border-radius:14px;padding:1.2rem;border:0.5px solid #eee;background:#fafafa}}
.prin-num{{
    width:32px;height:32px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    font-size:14px;font-weight:700;margin-bottom:10px;
}}
.prin-title{{font-size:14px;font-weight:700;color:#1a1a1a;margin-bottom:4px}}
.prin-en{{font-size:11px;color:#aaa;margin-bottom:8px;font-style:italic}}
.prin-desc{{font-size:12px;color:#555;line-height:1.65}}

/* 成键/反键对比 */
.bond-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1rem 0}}
.bond-card{{border-radius:14px;padding:1.2rem;border:0.5px solid #eee}}
.bond-title{{font-size:13px;font-weight:700;margin-bottom:6px}}
.bond-formula{{font-size:15px;margin:6px 0;text-align:center}}
.bond-desc{{font-size:12px;color:#555;line-height:1.65}}
.bond-badge{{
    display:inline-block;font-size:11px;padding:3px 9px;
    border-radius:99px;font-weight:500;margin-top:8px;
}}

/* HOMO LUMO */
.homo-lumo{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1rem 0}}
.hl-card{{border-radius:14px;padding:1.2rem;text-align:center}}

/* 填充规则 */
.fill-rules{{display:flex;flex-direction:column;gap:8px;margin:1rem 0}}
.fill-rule{{
    display:flex;align-items:center;gap:12px;
    background:#fafafa;border-radius:10px;padding:0.75rem 1rem;
    border:0.5px solid #eee;
}}
.fill-num{{
    width:24px;height:24px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    font-size:12px;font-weight:700;flex-shrink:0;
}}
.fill-text{{font-size:13px;color:#444}}
.fill-text strong{{color:#1a1a1a}}

/* 键级 */
.bond-order-box{{
    background:linear-gradient(135deg,#E6F1FB,#EEEDFE);
    border-radius:16px;padding:1.5rem 2rem;margin:1rem 0;
    border:0.5px solid #B5D4F4;
}}
.bo-formula{{font-size:22px;text-align:center;color:#185FA5;margin-bottom:1rem}}
.bo-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:0.75rem}}
.bo-item{{
    background:white;border-radius:10px;padding:0.75rem;
    text-align:center;border:0.5px solid #B5D4F4;
    font-size:12px;color:#555;
}}
.bo-item strong{{color:#185FA5;font-size:14px;display:block;margin-bottom:2px}}

.quote{{
    background:linear-gradient(135deg,#E6F1FB,#EEEDFE);
    border-radius:16px;padding:1.5rem 2rem;margin-top:2rem;
    font-size:16px;font-weight:600;color:#185FA5;
    line-height:1.6;text-align:center;
}}

.summary-box{{
    background:#fafafa;border-radius:14px;padding:1.2rem 1.5rem;
    border:0.5px solid #eee;margin:1rem 0;
}}
.summary-title{{font-size:12px;font-weight:600;color:#888;text-transform:uppercase;
    letter-spacing:0.07em;margin-bottom:10px}}
.summary-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.summary-item{{font-size:13px;color:#444;line-height:1.6}}
.summary-item strong{{color:#1a1a1a}}
</style>
</head>
<body>

<p class="lead">
  当两个或多个原子相互接近形成分子时，电子不再局限于单个原子，而是在整个分子范围内运动。
  用于描述这种离域状态的轨道称为<strong>分子轨道（Molecular Orbital, MO）</strong>。
  分子轨道理论采用<strong>原子轨道线性组合近似（LCAO）</strong>处理这一问题。
</p>

<!-- 3.1 LCAO 近似 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">3.1</span>
    <span class="section-title">分子轨道的形成：LCAO 近似</span>
  </div>
  <div class="two-col">
    <div>
      <p class="body-text">
        由于直接求解分子体系的薛定谔方程在数学上极其困难，分子轨道理论采用
        <strong>原子轨道线性组合（LCAO）</strong>近似。以双原子分子为例，
        分子轨道波函数可表示为：
      </p>
      <div class="formula-box">
        \( \Psi_{{\text{{MO}}}} = c_A \psi_A + c_B \psi_B \)
        <div class="formula-terms">
          <div class="f-term"><strong>\(\Psi_{{\text{{MO}}}}\)</strong><br>分子轨道波函数</div>
          <div class="f-term"><strong>\(\psi_A, \psi_B\)</strong><br>原子轨道波函数</div>
          <div class="f-term"><strong>\(c_A, c_B\)</strong><br>组合系数（贡献权重）</div>
        </div>
      </div>
      <div class="blockquote">
        LCAO 满足一个基本守恒关系：<br>
        <strong>生成的分子轨道总数 = 参与组合的原子轨道总数</strong><br>
        轨道只会重组与分裂，不会凭空产生或消失。
      </div>
    </div>
    <div class="img-card">
      <img src="{img_31}" alt="H2 分子轨道形成示意">
      <div class="img-caption">H₂ 分子：1s 轨道组合形成 σ 成键轨道与 σ* 反键轨道</div>
    </div>
  </div>
</div>

<!-- 3.2 LCAO 组合规则 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">3.2</span>
    <span class="section-title">LCAO 组合规则</span>
  </div>
  <p class="body-text">
    并非任意原子轨道都能有效组合形成分子轨道。有效的 LCAO 组合需同时满足以下三个基本条件：
  </p>
  <div class="principles">
    <div class="prin-card" style="border-color:#B5D4F4">
      <div class="prin-num" style="background:#E6F1FB;color:#185FA5">①</div>
      <div class="prin-title">对称性匹配原则</div>
      <div class="prin-en">Symmetry Match</div>
      <div class="prin-desc">
        参与组合的原子轨道必须具有<strong>相同的对称性</strong>才能发生有效重叠。
        以键轴（z 轴）为参考，绕轴旋转时波函数符号不变的为 σ 对称，
        符号改变的为 π 对称。只有同类对称性的轨道才能组合。
      </div>
    </div>
    <div class="prin-card" style="border-color:#9FE1CB">
      <div class="prin-num" style="background:#E1F5EE;color:#085041">②</div>
      <div class="prin-title">能量相近原则</div>
      <div class="prin-en">Energy Proximity</div>
      <div class="prin-desc">
        参与组合的原子轨道能量必须<strong>彼此接近</strong>，才能发生显著耦合。
        能量相同时耦合最强（如 H₂ 中两个 1s）；
        能量差越大，耦合越弱，轨道越保持原子特征（如 HF 中 H(1s) 与 F(2p)）。
      </div>
    </div>
    <div class="prin-card" style="border-color:#CECBF6">
      <div class="prin-num" style="background:#EEEDFE;color:#3C3489">③</div>
      <div class="prin-title">最大重叠原则</div>
      <div class="prin-en">Maximum Overlap</div>
      <div class="prin-desc">
        原子轨道之间必须有足够的<strong>空间重叠</strong>。
        重叠积分 \(S_{{AB}} = \int \psi_A^* \psi_B \, d\tau\) 越大，
        成键作用越强，能级分裂越大，体系越稳定。
      </div>
    </div>
  </div>

  <!-- 3.2.1 对称性匹配 -->
  <div class="sub-header">
    <span class="sub-num">3.2.1</span>
    <span class="sub-title">对称性匹配与 σ/π/δ 分类</span>
  </div>
  <div class="two-col-rev">
    <div class="img-card">
      <img src="{img_321}" alt="对称性匹配">
      <div class="img-caption">σ、π 键的形成：轨道对称性决定组合类型</div>
    </div>
    <div>
      <table class="mo-table">
        <tr>
          <th>原子轨道</th>
          <th>对称性</th>
          <th>MO 类型</th>
          <th>成键类型</th>
        </tr>
        <tr><td>\(s\)</td><td>绕 z 轴旋转对称（C∞）</td><td>σ 对称</td><td>σ 键</td></tr>
        <tr><td>\(p_z\)</td><td>绕 z 轴旋转对称</td><td>σ 对称</td><td>σ 键</td></tr>
        <tr><td>\(p_x, p_y\)</td><td>旋转 180° 后符号改变</td><td>π 对称</td><td>π 键</td></tr>
        <tr><td>\(d_{{z^2}}\)</td><td>绕 z 轴旋转对称</td><td>σ 对称</td><td>σ 键</td></tr>
        <tr><td>\(d_{{xz}}, d_{{yz}}\)</td><td>与 p_x, p_y 类似</td><td>π 对称</td><td>π 键</td></tr>
        <tr><td>\(d_{{x^2-y^2}}, d_{{xy}}\)</td><td>旋转 90°/45° 符号改变</td><td>δ 对称</td><td>δ 键</td></tr>
      </table>
      <div style="background:#fafafa;border-radius:10px;padding:0.75rem 1rem;
                  border:0.5px solid #eee;font-size:13px;color:#444;margin-top:0.75rem">
        对于具有反演中心的分子（同核双原子），还需满足<strong>g/u 对称性匹配</strong>：
        g 只与 g 组合，u 只与 u 组合（g = 反演不变，u = 反演改变符号）。
      </div>
    </div>
  </div>

  <!-- 3.2.2 能量相近 + 成键/反键 -->
  <div class="sub-header">
    <span class="sub-num">3.2.2</span>
    <span class="sub-title">能量相近原则与成键/反键轨道</span>
  </div>
  <div class="bond-grid">
    <div class="bond-card" style="border-color:#9FE1CB;background:#E1F5EE18">
      <div class="bond-title" style="color:#085041">✓ 成键轨道（Bonding MO）</div>
      <div class="bond-formula">\( \Psi_b = \psi_A + \psi_B \)</div>
      <div class="bond-desc">
        同相叠加（constructive interference），核间电子密度<strong>增大</strong>，
        能量<strong>低于</strong>原子轨道，有利于稳定分子。
      </div>
      <span class="bond-badge" style="background:#E1F5EE;color:#085041">能量降低 · 稳定分子</span>
    </div>
    <div class="bond-card" style="border-color:#F5C4B3;background:#FAECE718">
      <div class="bond-title" style="color:#712B13">✗ 反键轨道（Antibonding MO）</div>
      <div class="bond-formula">\( \Psi_a = \psi_A - \psi_B \)</div>
      <div class="bond-desc">
        反相叠加（destructive interference），核间出现<strong>节点</strong>，
        能量<strong>高于</strong>原子轨道，削弱化学键。
      </div>
      <span class="bond-badge" style="background:#FAECE7;color:#712B13">能量升高 · 削弱成键</span>
    </div>
  </div>
  <div class="img-full">
    <img src="{img_332}" alt="MO能级图">
    <div class="img-caption">N₂ 分子轨道能级图（左）与各分子轨道形状（右）</div>
  </div>
</div>

<!-- 3.3 MO 排布与键级 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">3.3</span>
    <span class="section-title">分子轨道的排布与键级</span>
  </div>

  <!-- 3.3.1 能级图 -->
  <div class="sub-header">
    <span class="sub-num">3.3.1</span>
    <span class="sub-title">分子轨道能级图</span>
  </div>
  <div class="two-col">
    <div>
      <p class="body-text">
        将所有形成的分子轨道按能量由低到高排列，可得到
        <strong>分子轨道能级图（MO diagram）</strong>。
        能级图中的约定：
      </p>
      <div class="fill-rules">
        <div class="fill-rule">
          <div style="width:8px;height:8px;border-radius:2px;background:#378ADD;flex-shrink:0"></div>
          <div class="fill-text">纵轴表示<strong>能量</strong>，向上能量增加</div>
        </div>
        <div class="fill-rule">
          <div style="width:8px;height:8px;border-radius:2px;background:#5DCAA5;flex-shrink:0"></div>
          <div class="fill-text">越靠<strong>下</strong>的轨道能量越低、越稳定、越先被填充</div>
        </div>
        <div class="fill-rule">
          <div style="width:8px;height:8px;border-radius:2px;background:#F0997B;flex-shrink:0"></div>
          <div class="fill-text">越靠<strong>上</strong>的轨道越难被占据，基态通常为空轨道</div>
        </div>
      </div>

      <!-- 3.3.2 填充规则 -->
      <div class="sub-header" style="margin-top:1.5rem">
        <span class="sub-num">3.3.2</span>
        <span class="sub-title">电子填充规则</span>
      </div>
      <div class="fill-rules">
        <div class="fill-rule">
          <div class="fill-num" style="background:#E6F1FB;color:#185FA5">①</div>
          <div class="fill-text"><strong>Aufbau 原理</strong>：电子优先占据能量最低的分子轨道</div>
        </div>
        <div class="fill-rule">
          <div class="fill-num" style="background:#EEEDFE;color:#3C3489">②</div>
          <div class="fill-text"><strong>泡利不相容原理</strong>：每个 MO 最多容纳两个自旋相反的电子</div>
        </div>
        <div class="fill-rule">
          <div class="fill-num" style="background:#E1F5EE;color:#085041">③</div>
          <div class="fill-text"><strong>洪特规则</strong>：简并 MO 中电子先单占且自旋平行</div>
        </div>
      </div>

      <!-- HOMO / LUMO -->
      <div class="homo-lumo" style="margin-top:1rem">
        <div class="hl-card" style="background:#E6F1FB;border:0.5px solid #B5D4F4">
          <div style="font-size:16px;font-weight:800;color:#185FA5;margin-bottom:4px">HOMO</div>
          <div style="font-size:11px;color:#555;margin-bottom:6px">Highest Occupied MO</div>
          <div style="font-size:12px;color:#444">最高已占据分子轨道<br>基态下能量最高的含电子轨道</div>
        </div>
        <div class="hl-card" style="background:#EEEDFE;border:0.5px solid #CECBF6">
          <div style="font-size:16px;font-weight:800;color:#3C3489;margin-bottom:4px">LUMO</div>
          <div style="font-size:11px;color:#555;margin-bottom:6px">Lowest Unoccupied MO</div>
          <div style="font-size:12px;color:#444">最低未占据分子轨道<br>能量最低的空轨道</div>
        </div>
      </div>
      <div style="background:#fafafa;border-radius:10px;padding:0.75rem 1rem;
                  border:0.5px solid #eee;font-size:13px;color:#444;margin-top:0.75rem">
        <strong>HOMO–LUMO 能隙</strong>越大 → 分子越稳定、化学反应性越低；
        能隙越小 → 分子越活泼、易发生电子跃迁与化学反应。
      </div>
    </div>
    <div class="img-card">
      <img src="{img_331}" alt="第二周期双原子分子MO能级图">
      <div class="img-caption">第二周期同核双原子分子 MO 能级图（B₂ 至 Ne₂）</div>
    </div>
  </div>

  <!-- 3.3.3 键级 -->
  <div class="sub-header">
    <span class="sub-num">3.3.3</span>
    <span class="sub-title">键级（Bond Order）</span>
  </div>
  <div class="two-col-rev">
    <div class="img-card">
      <img src="{img_333}" alt="键级对比表">
      <div class="img-caption">第二周期双原子分子的键级、键长、键能与磁性对比</div>
    </div>
    <div>
      <div class="bond-order-box">
        <div class="bo-formula">
          \( \text{{键级}} = \dfrac{{N_b - N_a}}{{2}} \)
        </div>
        <div class="bo-grid">
          <div class="bo-item"><strong>\(N_b\)</strong>成键轨道中的电子数</div>
          <div class="bo-item"><strong>\(N_a\)</strong>反键轨道中的电子数</div>
          <div class="bo-item"><strong>÷ 2</strong>每个键由两电子组成</div>
        </div>
      </div>
      <p class="body-text">键级越大：</p>
      <div class="fill-rules">
        <div class="fill-rule">
          <div style="width:8px;height:8px;border-radius:50%;background:#378ADD;flex-shrink:0"></div>
          <div class="fill-text"><strong>键长越短</strong> — 原子核间距越小</div>
        </div>
        <div class="fill-rule">
          <div style="width:8px;height:8px;border-radius:50%;background:#5DCAA5;flex-shrink:0"></div>
          <div class="fill-text"><strong>键能越大</strong> — 断键所需能量越高</div>
        </div>
        <div class="fill-rule">
          <div style="width:8px;height:8px;border-radius:50%;background:#534AB7;flex-shrink:0"></div>
          <div class="fill-text"><strong>分子越稳定</strong> — 化学键越牢固</div>
        </div>
      </div>
      <div style="background:#fafafa;border-radius:10px;padding:0.75rem 1rem;
                  border:0.5px solid #eee;font-size:13px;color:#444;margin-top:0.75rem">
        键级 = 0 表示该双原子组合<strong>不能稳定存在</strong>（如 He₂）；
        键级 = 3 表示三键（如 N₂），极为稳定。
      </div>
    </div>
  </div>
</div>

<div class="quote">
  分子轨道理论从量子力学出发，将成键描述为原子轨道的波函数叠加，<br>
  为理解化学键本质、分子磁性与反应活性提供了统一的理论框架。
</div>

</body>
</html>
"""

components.html(HTML, height=4200, scrolling=False)

divider()

st.subheader("🔬 分子轨道能级图可视化")
st.caption("选择分子或自定义两种原子，自动生成 MO 能级图，显示电子填充、HOMO/LUMO 与键级分析")
render_mo_tool()

page_footer("mo")   
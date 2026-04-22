import streamlit as st
import streamlit.components.v1 as components
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '5.Huckel'))
from hmo_tool import render_hmo_tool
from utils import page_header, page_footer, divider

st.set_page_config(layout="wide", page_title="Hückel 分子轨道理论", page_icon="🔬")

page_header("hmo", desc="Hückel 分子轨道理论以极简的近似，揭示了共轭 π 体系的电子结构与芳香性——连接量子力学与有机化学直觉的经典桥梁。")

# ── 所有公式提前定义，完全绕开 f-string 花括号 ──────────
f_alpha   = r'\( \alpha \)'
f_beta    = r'\( \beta \)'
f_Hrr     = r'\( H_{rr} = \alpha \)'
f_Hrs     = r'\( H_{rs} = \beta \)'
f_Srr     = r'\( S_{rr}=1,\; S_{rs}=0 \)'
f_sec1    = r'\( \det(\mathbf{H} - E\mathbf{S}) = 0 \)'
f_sec2    = r'\( \det(\mathbf{H}^{\prime} - E\mathbf{I}) = 0 \)'
f_x       = r'\( x = \dfrac{\alpha - E}{\beta} \)'
f_eform   = r'\( E = \alpha - x\beta \)'
f_det4    = r'''\[
\begin{vmatrix}
\alpha - E & \beta & 0 & 0 \\
\beta & \alpha - E & \beta & 0 \\
0 & \beta & \alpha - E & \beta \\
0 & 0 & \beta & \alpha - E
\end{vmatrix} = 0
\]'''
f_det4x   = r'''\[
\begin{vmatrix}
x & 1 & 0 & 0 \\
1 & x & 1 & 0 \\
0 & 1 & x & 1 \\
0 & 0 & 1 & x
\end{vmatrix} = 0
\]'''
f_poly    = r'\( x^4 - 3x^2 + 1 = 0 \)'
f_y       = r'\( y = x^2 \)'
f_ysol    = r'\( y = \dfrac{3 \pm \sqrt{5}}{2} \)'
f_xsol    = r'\( x = \pm 1.618,\quad \pm 0.618 \)'
f_e1      = r'\( E_1 = \alpha + 1.618\beta \)'
f_e2      = r'\( E_2 = \alpha + 0.618\beta \)'
f_e3      = r'\( E_3 = \alpha - 0.618\beta \)'
f_e4      = r'\( E_4 = \alpha - 1.618\beta \)'
f_etotal  = r'\( E_{\mathrm{total}} = 2E_1 + 2E_2 = 4\alpha + 4.472\beta \)'
f_eref    = r'\( E_{\mathrm{ref}} = 4\alpha + 4\beta \)'
f_edeloc  = r'\( E_{\mathrm{deloc}} = E_{\mathrm{total}} - E_{\mathrm{ref}} = 0.472\beta \)'
f_butadiene = r'\( x^4 - 3x^2 + 1 = 0 \)'

HTML = """
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif;
  color:#1a1a1a;background:white;padding:2rem 3rem 4rem;line-height:1.8;}
.lead{font-size:16px;color:#555;line-height:1.9;max-width:720px;
  margin-bottom:3rem;padding-left:1.2rem;border-left:3px solid #97C459;}
.section{margin-bottom:3.5rem}
.section-header{display:flex;align-items:baseline;gap:12px;
  margin-bottom:1.4rem;padding-bottom:0.75rem;border-bottom:0.5px solid #f0f0f0;}
.section-num{font-size:12px;font-weight:600;color:#97C459;letter-spacing:0.05em}
.section-title{font-size:20px;font-weight:700;letter-spacing:-0.01em;color:#1a1a1a}
.sub-header{display:flex;align-items:baseline;gap:10px;
  margin:1.5rem 0 0.75rem;padding-bottom:0.4rem;border-bottom:0.5px solid #f8f8f8;}
.sub-num{font-size:11px;font-weight:600;color:#97C459}
.sub-title{font-size:16px;font-weight:700;color:#1a1a1a}
.body-text{font-size:15px;color:#444;line-height:1.9;max-width:740px;margin-bottom:1rem}
.body-text strong{color:#1a1a1a;font-weight:600}
.blockquote{border-left:3px solid #97C459;background:#EAF3DE18;
  padding:0.75rem 1.2rem;border-radius:0 10px 10px 0;
  font-size:15px;color:#27500A;margin:1rem 0;}
.formula-box{background:#EAF3DE;border-radius:14px;padding:1.2rem 1.5rem;
  margin:1rem 0;border:0.5px solid #C0DD97;text-align:center;font-size:18px;color:#27500A;}
.formula-wide{background:#fafafa;border-radius:12px;padding:1rem 1.5rem;
  margin:0.75rem 0;border:0.5px solid #eee;text-align:center;font-size:14px;color:#333;overflow-x:auto;}
.formula-step{background:#F5FAF0;border-radius:10px;padding:0.85rem 1.2rem;
  margin:0.5rem 0;border-left:3px solid #97C459;font-size:14px;color:#333;}
.step-label{font-size:11px;font-weight:600;color:#639922;text-transform:uppercase;
  letter-spacing:0.06em;margin-bottom:6px;}

.value-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:1.25rem 0}
.value-card{border-radius:14px;padding:1.1rem;border:0.5px solid #C0DD97;background:#EAF3DE18}
.value-num{width:26px;height:26px;border-radius:50%;background:#EAF3DE;color:#27500A;
  display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;margin-bottom:8px}
.value-title{font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:5px}
.value-desc{font-size:12px;color:#555;line-height:1.65}

.approx-table{width:100%;border-collapse:collapse;font-size:13px;margin:1rem 0}
.approx-table th{background:#EAF3DE;padding:8px 12px;border:1px solid #C0DD97;
  font-weight:600;color:#27500A;text-align:left;}
.approx-table td{padding:8px 12px;border:1px solid #eee;color:#444;vertical-align:middle}
.approx-table tr:hover td{background:#F5FAF0}

.result-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1.25rem 0}
.result-card{border-radius:14px;padding:1.2rem;border:0.5px solid #eee;background:#fafafa}
.result-title{font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:8px}
.result-content{font-size:13px;color:#444;line-height:1.8}

.energy-levels{background:#fafafa;border-radius:14px;padding:1.2rem 1.5rem;
  border:0.5px solid #C0DD97;margin:1rem 0;}
.e-row{display:flex;align-items:center;gap:14px;padding:8px 0;
  border-bottom:0.5px solid #f0f0f0;}
.e-row:last-child{border-bottom:none}
.e-bar{height:4px;border-radius:2px;flex-shrink:0}
.e-formula{font-size:14px;color:#333;flex:1}
.e-tag{font-size:11px;padding:2px 8px;border-radius:99px;font-weight:500;flex-shrink:0}

.note-box{background:#fafafa;border-radius:10px;padding:0.85rem 1.2rem;
  border:0.5px solid #eee;font-size:13px;color:#666;margin:0.75rem 0;line-height:1.65}
.note-box strong{color:#1a1a1a}
.quote{background:linear-gradient(135deg,#EAF3DE,#EEEDFE);border-radius:16px;
  padding:1.5rem 2rem;margin-top:2rem;font-size:16px;font-weight:600;
  color:#27500A;line-height:1.6;text-align:center;}
</style>
</head>
<body>

<p class="lead">
  休克尔分子轨道理论（HMO）是早期量子化学在计算能力有限的背景下，
  为研究有机共轭体系而发展起来的一种高度成功的近似方法。
  尽管模型极度简化，但它在解释 π 电子非定域化、芳香性和反应活性方面发挥了不可替代的作用。
</p>

<!-- 5.0 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">5.0</span>
    <span class="section-title">我们为什么需要 HMO？</span>
  </div>
  <p class="body-text">
    HMO 理论的提出，源于对<strong>共轭 π 体系</strong>的迫切需求。其核心价值主要体现在以下三个方面。
  </p>
  <div class="value-grid">
    <div class="value-card">
      <div class="value-num">①</div>
      <div class="value-title">极大简化复杂 π 体系计算</div>
      <div class="value-desc">
        通过两项关键近似显著降低问题复杂度：
        一是 <strong>σ–π 分离近似</strong>，仅考虑 π 电子；
        二是 <strong>Hückel 近似</strong>，将复杂积分参数化，使问题转化为线性代数本征值问题。
        由此，共轭分子可通过纸笔或简单计算完成分析。
      </div>
    </div>
    <div class="value-card">
      <div class="value-num">②</div>
      <div class="value-title">定量描述 π 电子非定域化</div>
      <div class="value-desc">
        能够计算共轭体系中任意两原子之间的 <strong>π 键级</strong>（如苯中 C–C 键 π 键级为 2/3），
        以及<strong>离域能（Delocalization Energy）</strong>，从能量角度定量解释共轭体系相对于孤立双键体系的额外稳定性。
        这为共振论提供了坚实的量子力学基础。
      </div>
    </div>
    <div class="value-card">
      <div class="value-num">③</div>
      <div class="value-title">直观的定性框架</div>
      <div class="value-desc">
        通过 HMO 得到的能级图和轨道对称性，能够清晰识别
        <strong>HOMO</strong> 与 <strong>LUMO</strong>，从而为前线轨道理论、
        反应活性预测以及 <strong>Hückel 的 4n+2 规则</strong>提供直接依据。
      </div>
    </div>
  </div>
</div>

<!-- 5.1 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">5.1</span>
    <span class="section-title">适用范围与基本前提</span>
  </div>
  <p class="body-text">
    HMO 理论主要适用于<strong>平面共轭烃类分子</strong>，如丁二烯、苯、烯丙基阳离子等。
    这类分子中，每个原子都提供一个未参与 σ 成键的 p 轨道，通过侧向重叠形成离域 π 体系。
  </p>
  <div class="blockquote">
    核心前提：<strong>σ–π 分离近似</strong>——σ 键决定分子几何构型，π 电子在既定骨架上独立运动，
    计算中仅考虑 π 电子体系。
  </div>
</div>

<!-- 5.2 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">5.2</span>
    <span class="section-title">数学基础：Hückel 近似</span>
  </div>
  <p class="body-text">
    HMO 理论基于 LCAO–MO 变分法，其久期方程（Secular Equations）涉及以下三类积分，全部通过参数化处理：
  </p>
  <table class="approx-table">
    <tr><th>积分类型</th><th>符号</th><th>Hückel 近似</th><th>物理意义</th></tr>
    <tr>
      <td><strong>库仑积分</strong></td>
      <td>""" + f_alpha + """</td>
      <td>""" + f_Hrr + """</td>
      <td>原子 r 上 π 电子的能量（选作能量零点）</td>
    </tr>
    <tr>
      <td><strong>交换积分</strong></td>
      <td>""" + f_beta + """</td>
      <td>相邻原子 """ + f_Hrs + """；不相邻 = 0</td>
      <td>原子间相互作用（β &lt; 0，成键稳定化）</td>
    </tr>
    <tr>
      <td><strong>重叠积分</strong></td>
      <td>\( S \)</td>
      <td>""" + f_Srr + """</td>
      <td>正交近似，简化矩阵运算</td>
    </tr>
  </table>
  <div class="note-box">
    其中 """ + f_alpha + """ 和 """ + f_beta + """ 不通过积分计算，而是作为<strong>经验参数</strong>引入。
    通常将 α 选作能量零点，β 为负值，表示相邻原子间成键带来的稳定化效应。
  </div>
</div>

<!-- 5.3 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">5.3</span>
    <span class="section-title">Hückel 行列式与求解方法</span>
  </div>
  <p class="body-text">在上述近似下，久期方程可写为：</p>
  <div class="formula-box">""" + f_sec1 + """</div>
  <p class="body-text">在正交近似下，该方程进一步简化为：</p>
  <div class="formula-box">""" + f_sec2 + """</div>
  <p class="body-text">为便于求解，通常引入无量纲变量：</p>
  <div class="formula-box">""" + f_x + """</div>
  <p class="body-text">
    从而将问题转化为关于 x 的代数方程。解得 x 后，由 """ + f_eform + """ 反推出 π 分子轨道的能量本征值。
  </p>
</div>

<!-- 5.4 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">5.4</span>
    <span class="section-title">HMO 的主要结果与应用</span>
  </div>
  <p class="body-text">通过求解 Hückel 行列式，HMO 理论可以提供以下关键信息：</p>
  <div class="result-grid">
    <div class="result-card" style="border-color:#C0DD97">
      <div class="result-title" style="color:#27500A">结构与电子信息</div>
      <div class="result-content">
        · π 分子轨道的<strong>能级分布</strong><br>
        · 共轭体系的<strong>离域能（Delocalization Energy）</strong><br>
        · 任意原子对之间的 <strong>π 键级</strong>
      </div>
    </div>
    <div class="result-card" style="border-color:#CECBF6">
      <div class="result-title" style="color:#3C3489">反应活性预测</div>
      <div class="result-content">
        · HOMO 与 LUMO 的<strong>能量及波函数</strong><br>
        · 预测化学反应活性位点（<strong>自由价</strong>）<br>
        · 芳香性判断（4n+2 规则）
      </div>
    </div>
  </div>
</div>

<!-- 5.5 严格推导 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">5.5</span>
    <span class="section-title">示例：1,3-丁二烯的 HMO 完整求解</span>
  </div>
  <p class="body-text">
    以 1,3-丁二烯为例，其 π 体系由四个碳原子提供的四个 p 轨道
    \(\psi_1, \psi_2, \psi_3, \psi_4\) 构成。
  </p>

  <div class="sub-header">
    <span class="sub-num">5.5.1</span>
    <span class="sub-title">久期行列式的建立</span>
  </div>
  <p class="body-text">
    对于 \(N=4\) 的体系，久期方程为 """ + f_sec1 + """，
    在 Hückel 近似下，该行列式可写为：
  </p>
  <div class="formula-wide">""" + f_det4 + """</div>

  <div class="sub-header">
    <span class="sub-num">5.5.2</span>
    <span class="sub-title">变量代换与求解</span>
  </div>
  <p class="body-text">引入代换 """ + f_x + """，行列式化为：</p>
  <div class="formula-wide">""" + f_det4x + """</div>
  <p class="body-text">展开后得到代数方程：</p>
  <div class="formula-box">""" + f_butadiene + """</div>

  <div class="formula-step">
    <div class="step-label">令 y = x² 代换</div>
    """ + f_y + """ &nbsp;⟹&nbsp; 二次方程求解：&nbsp; """ + f_ysol + """
  </div>
  <div class="formula-step">
    <div class="step-label">反解 x</div>
    对应四个解：&nbsp; """ + f_xsol + """
  </div>

  <div class="sub-header">
    <span class="sub-num">5.5.3</span>
    <span class="sub-title">π 轨道能量</span>
  </div>
  <p class="body-text">由 """ + f_eform + """ 得到四个 π 轨道能量：</p>
  <div class="energy-levels">
    <div class="e-row">
      <div class="e-bar" style="width:60px;background:#1D9E75"></div>
      <div class="e-formula">""" + f_e1 + """</div>
      <span class="e-tag" style="background:#EAF3DE;color:#27500A">成键 · HOMO−1（2e）</span>
    </div>
    <div class="e-row">
      <div class="e-bar" style="width:40px;background:#5DCAA5"></div>
      <div class="e-formula">""" + f_e2 + """</div>
      <span class="e-tag" style="background:#E1F5EE;color:#085041">成键 · HOMO（2e）</span>
    </div>
    <div class="e-row">
      <div class="e-bar" style="width:40px;background:#EF9F27"></div>
      <div class="e-formula">""" + f_e3 + """</div>
      <span class="e-tag" style="background:#FAEEDA;color:#633806">反键 · LUMO（空）</span>
    </div>
    <div class="e-row">
      <div class="e-bar" style="width:60px;background:#F0997B"></div>
      <div class="e-formula">""" + f_e4 + """</div>
      <span class="e-tag" style="background:#FAECE7;color:#712B13">反键 · LUMO+1（空）</span>
    </div>
  </div>
  <div class="note-box">
    丁二烯具有 4 个 π 电子，依次填充最低的两个成键轨道 \(E_1\) 和 \(E_2\)。
  </div>

  <div class="sub-header">
    <span class="sub-num">5.5.4</span>
    <span class="sub-title">离域能的计算</span>
  </div>
  <p class="body-text">丁二烯的总 π 电子能量为：</p>
  <div class="formula-step">
    <div class="step-label">总 π 能量</div>
    """ + f_etotal + """
  </div>
  <p class="body-text">作为对比，两个孤立双键的参考能量为：</p>
  <div class="formula-step">
    <div class="step-label">参考能量（两个孤立 C=C）</div>
    """ + f_eref + """
  </div>
  <p class="body-text">因此，离域能为：</p>
  <div class="formula-box">""" + f_edeloc + """</div>
  <div class="note-box">
    由于 β &lt; 0，故 \(E_{\mathrm{deloc}} < 0\)，说明丁二烯因 π 电子共轭而获得<strong>额外稳定化</strong>。
    这一结果从能量角度为共振论提供了量子力学依据。
  </div>
</div>

<div class="quote">
  HMO 理论通过极简的模型，成功揭示了 π 电子非定域化的本质，<br>
  是连接量子力学与有机化学直觉的经典桥梁。
</div>

</body>
</html>
"""

components.html(HTML, height=5000, scrolling=False)

divider()

st.subheader("🧪 Hückel MO 计算器")
st.caption("支持线型链、单环和自定义多环体系 · 自动计算能级、键级、电荷密度、离域能")
render_hmo_tool()

page_footer("hmo")
import streamlit as st
import streamlit.components.v1 as components
import base64
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
from resonance_widget import RESONANCE_HTML
from utils import load_md, page_header, page_footer, divider

st.set_page_config(layout="wide", page_title="价键理论", page_icon="🔗")

page_header("vb", desc="价键理论从电子的定域化配对出发描述化学键，以其直观性和对分子几何构型的强解释力，与分子轨道理论形成互补。")

def img_b64(path):
    try:
        with open(path, "rb") as f:
            ext = path.split(".")[-1].lower()
            mime = "image/jpeg" if ext in ["jpg","jpeg"] else "image/png"
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"
    except:
        return ""

img_41  = img_b64("4.valence bond/4.1.jpg")
img_431 = img_b64("4.valence bond/4.3.1.jpeg")
img_432 = img_b64("4.valence bond/4.3.2.jpeg")
img_433 = img_b64("4.valence bond/4.3.3.jpeg")
img_434 = img_b64("4.valence bond/4.3.4.jpeg")
img_441 = img_b64("4.valence bond/4.4.1.jpeg")
img_442 = img_b64("4.valence bond/4.4.2.jpeg")
img_443 = img_b64("4.valence bond/4.4.3.jpeg")
img_444 = img_b64("4.valence bond/4.4.4.jpeg")
img_445 = img_b64("4.valence bond/4.4.5.png")

# 把复杂公式提前定义，避免 f-string 花括号冲突
f_mo = r'\( \Psi_{\mathrm{MO}} \approx \psi_A + \psi_B \)'
f_vb = r'\( \Psi_{\mathrm{VB}} \approx \psi_A \psi_B \)'
f_cov = r'\( \Psi_{\mathrm{cov}} = \frac{1}{\sqrt{2(1+S^2)}} \left[ \psi_A(1)\psi_B(2) + \psi_B(1)\psi_A(2) \right] \)'
f_spin = r'\( \Phi_{\mathrm{spin}} = \frac{1}{\sqrt{2}} \left[ \alpha(1)\beta(2) - \beta(1)\alpha(2) \right] \)'
f_hl = r'\( \Psi_{\mathrm{HL}} = \Psi_{\mathrm{cov}} \cdot \Phi_{\mathrm{spin}} \)'
f_s = r'\( S = \int \psi_A \psi_B \, d\tau \)'

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
    margin-bottom:3rem;padding-left:1.2rem;border-left:3px solid #EF9F27;
}}
.section{{margin-bottom:3.5rem}}
.section-header{{
    display:flex;align-items:baseline;gap:12px;
    margin-bottom:1.4rem;padding-bottom:0.75rem;
    border-bottom:0.5px solid #f0f0f0;
}}
.section-num{{font-size:12px;font-weight:600;color:#EF9F27;letter-spacing:0.05em}}
.section-title{{font-size:20px;font-weight:700;letter-spacing:-0.01em;color:#1a1a1a}}
.body-text{{font-size:15px;color:#444;line-height:1.9;max-width:740px;margin-bottom:1rem}}
.body-text strong{{color:#1a1a1a;font-weight:600}}

.two-col{{display:grid;grid-template-columns:1fr 340px;gap:2rem;align-items:start}}
.two-col-rev{{display:grid;grid-template-columns:360px 1fr;gap:2rem;align-items:start}}
.two-col-eq{{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;align-items:start}}

.img-card{{border-radius:14px;overflow:hidden;border:0.5px solid #eee;background:#fafafa}}
.img-card img{{width:100%;display:block}}
.img-caption{{font-size:11px;color:#aaa;text-align:center;padding:8px 12px;border-top:0.5px solid #eee}}
.img-full{{border-radius:14px;overflow:hidden;border:0.5px solid #eee;background:#fafafa;margin:1.25rem 0}}
.img-full img{{width:100%;display:block}}
.img-full .img-caption{{border-top:0.5px solid #eee}}

.blockquote{{
    border-left:3px solid #EF9F27;background:#FAEEDA18;
    padding:0.75rem 1.2rem;border-radius:0 10px 10px 0;
    font-size:15px;color:#633806;margin:1rem 0;
}}
.formula-box{{
    background:#FAEEDA;border-radius:14px;
    padding:1.2rem 1.5rem;margin:1rem 0;
    border:0.5px solid #F0C060;text-align:center;
    font-size:18px;color:#633806;
}}

/* MO vs VB 对比 */
.compare-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1.25rem 0}}
.compare-card{{border-radius:14px;padding:1.2rem;border:0.5px solid #eee;background:#fafafa}}
.compare-title{{font-size:13px;font-weight:700;margin-bottom:8px}}
.compare-formula{{font-size:16px;text-align:center;margin:8px 0}}
.compare-desc{{font-size:12px;color:#555;line-height:1.65}}
.compare-badge{{
    display:inline-block;font-size:11px;padding:3px 9px;
    border-radius:99px;font-weight:500;margin-top:8px;
}}

/* 基本假设卡片 */
.assume-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:1.25rem 0}}
.assume-card{{border-radius:14px;padding:1.1rem;border:0.5px solid #F0C060;background:#FAEEDA18}}
.assume-num{{
    width:26px;height:26px;border-radius:50%;
    background:#FAEEDA;color:#633806;
    display:flex;align-items:center;justify-content:center;
    font-size:12px;font-weight:700;margin-bottom:8px;
}}
.assume-title{{font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:5px}}
.assume-desc{{font-size:12px;color:#555;line-height:1.65}}

/* 波函数推导 */
.wf-box{{
    background:#fafafa;border-radius:14px;padding:1.25rem 1.5rem;
    border:0.5px solid #eee;margin:1rem 0;
}}
.wf-title{{font-size:12px;font-weight:600;color:#888;text-transform:uppercase;
    letter-spacing:0.07em;margin-bottom:10px;}}
.wf-step{{
    display:flex;align-items:center;gap:12px;
    padding:8px 0;border-bottom:0.5px solid #f5f5f5;
    font-size:14px;color:#444;
}}
.wf-step:last-child{{border-bottom:none}}
.wf-step-label{{
    font-size:11px;color:#aaa;width:60px;flex-shrink:0;text-align:right;
}}

/* σ/π 键对比 */
.bond-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1.25rem 0}}
.bond-card{{border-radius:14px;padding:1.2rem;border:0.5px solid #eee}}
.bond-sym{{font-size:28px;font-weight:800;margin-bottom:6px}}
.bond-title{{font-size:13px;font-weight:700;margin-bottom:6px}}
.bond-desc{{font-size:12px;color:#555;line-height:1.65}}
.bond-ex{{font-size:11px;padding:3px 9px;border-radius:99px;
    font-weight:500;display:inline-block;margin-top:6px}}

/* 重叠类型图示区 */
.overlap-row{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1rem 0}}

/* 杂化类型表格 */
.hyb-table{{width:100%;border-collapse:collapse;font-size:13px;margin:1rem 0}}
.hyb-table th{{
    background:#FAEEDA;padding:8px 12px;
    border:1px solid #F0C060;font-weight:600;
    color:#633806;text-align:left;
}}
.hyb-table td{{padding:8px 12px;border:1px solid #eee;color:#444;vertical-align:top}}
.hyb-table tr:hover td{{background:#FFFDF5}}
.hyb-badge{{
    display:inline-block;font-size:11px;padding:2px 8px;
    border-radius:6px;font-weight:700;
}}

/* 杂化图片组 */
.hyb-imgs{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1.25rem 0}}

/* 共振论 */
.resonance-rules{{
    background:#fafafa;border-radius:14px;padding:1.2rem 1.5rem;
    border:0.5px solid #eee;margin:1rem 0;
}}
.res-title{{font-size:12px;font-weight:600;color:#888;text-transform:uppercase;
    letter-spacing:0.07em;margin-bottom:10px}}
.res-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.res-item{{
    font-size:13px;color:#444;padding:8px 10px;
    background:white;border-radius:8px;border:0.5px solid #eee;
    line-height:1.6;
}}
.res-item strong{{color:#1a1a1a}}

/* MO vs VB 补充 */
.mv-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1rem 0}}
.mv-card{{border-radius:14px;padding:1.2rem;border:0.5px solid #eee;background:#fafafa}}
.mv-title{{font-size:13px;font-weight:700;margin-bottom:8px}}
.mv-formula{{
    background:white;border-radius:10px;padding:0.75rem;
    border:0.5px solid #eee;font-size:14px;text-align:center;
    margin:6px 0;
}}
.mv-desc{{font-size:12px;color:#555;line-height:1.65;margin-top:6px}}

.quote{{
    background:linear-gradient(135deg,#FAEEDA,#EEEDFE);
    border-radius:16px;padding:1.5rem 2rem;margin-top:2rem;
    font-size:16px;font-weight:600;color:#633806;
    line-height:1.6;text-align:center;
}}

.note-box{{
    background:#fafafa;border-radius:10px;padding:0.85rem 1.2rem;
    border:0.5px solid #eee;font-size:13px;color:#666;
    margin:0.75rem 0;line-height:1.65;
}}
.note-box strong{{color:#1a1a1a}}
</style>
</head>
<body>

<p class="lead">
  价键理论从电子的<strong>定域化配对</strong>出发描述化学键，是理解分子结构和成键方式的重要理论框架。
  它与分子轨道理论从不同角度刻画电子行为，在化学中具有高度的互补性。
</p>

<!-- 4.1 为什么需要价键理论 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">4.1</span>
    <span class="section-title">我们为什么需要价键理论？</span>
  </div>
  <div class="two-col">
    <div>
      <p class="body-text">
        分子轨道理论将电子视为<strong>非定域的独立运动粒子</strong>，
        不显式考虑电子间的相关性。以 H₂ 为例，简单 MO 理论等权重地考虑共价结构与离子结构：
      </p>
      <div class="compare-grid">
        <div class="compare-card" style="border-color:#B5D4F4">
          <div class="compare-title" style="color:#185FA5">MO 理论</div>
         <div class="compare-formula">{f_mo}</div>
          <div class="compare-desc">
            电子非定域，等权重考虑共价与离子结构，
            会<strong>高估离子性</strong>，低估电子间排斥。
          </div>
          <span class="compare-badge" style="background:#E6F1FB;color:#0C447C">适合离域体系</span>
        </div>
        <div class="compare-card" style="border-color:#F0C060">
          <div class="compare-title" style="color:#633806">VB 理论</div>
          <div class="compare-formula">{f_vb}</div>
          <div class="compare-desc">
            电子定域化，天然强调共价结构，
            在描述 H₂ 的非极性特征时<strong>更加合理</strong>。
          </div>
          <span class="compare-badge" style="background:#FAEEDA;color:#633806">适合定域键</span>
        </div>
      </div>
    </div>
    <div class="img-card">
      <img src="{img_41}" alt="H2 共价键示意">
      <div class="img-caption">H₂ 分子：两个氢原子的 1s 轨道重叠形成共价键</div>
    </div>
  </div>
</div>

<!-- 4.2 核心思想与基本假设 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">4.2</span>
    <span class="section-title">核心思想与基本假设</span>
  </div>
  <div class="blockquote">
    共价键由两个原子轨道的重叠及一对<strong>自旋相反的电子</strong>形成。
  </div>
  <div class="assume-grid">
    <div class="assume-card">
      <div class="assume-num">①</div>
      <div class="assume-title">电子定域化</div>
      <div class="assume-desc">电子对主要分布在两个原子核之间，而非遍布整个分子。</div>
    </div>
    <div class="assume-card">
      <div class="assume-num">②</div>
      <div class="assume-title">成键条件</div>
      <div class="assume-desc">两个原子轨道中各含一个未配对电子，且自旋方向相反。</div>
    </div>
    <div class="assume-card">
      <div class="assume-num">③</div>
      <div class="assume-title">最大重叠原则</div>
      <div class="assume-desc">轨道重叠越大，化学键越强。键的方向性由最大重叠方向决定。</div>
    </div>
  </div>

  <div class="wf-box" style="margin-top:1.5rem">
    <div class="wf-title">H₂ 分子的 Heitler–London 波函数推导</div>
    <div class="wf-step">
        <div class="wf-step-label">空间部分</div>
        <div>{f_cov}</div>
    </div>
    <div class="wf-step">
        <div class="wf-step-label">自旋部分</div>
        <div>{f_spin}</div>
    </div>
    <div class="wf-step">
         <div class="wf-step-label">完整波函数</div>
        <div>{f_hl}</div>
    </div>
    <div style="font-size:12px;color:#888;margin-top:10px">
        其中 {f_s} 为重叠积分，电子 1、2 不可区分，故取两种分配方式之和。
    </div>
  </div>
</div>

<!-- 4.3 轨道重叠与键的类型 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">4.3</span>
    <span class="section-title">轨道重叠与键的类型</span>
  </div>
  <p class="body-text">
    根据轨道重叠方式，共价键可分为两种基本类型。σ 键总是先形成，π 键在其基础上附加形成，
    因此多重键通常更短、更强。
  </p>
  <div class="bond-grid">
    <div class="bond-card" style="border-color:#F0C060;background:#FAEEDA18">
      <div class="bond-sym" style="color:#633806">σ</div>
      <div class="bond-title">σ 键 — 轴向重叠</div>
      <div class="bond-desc">
        沿核间轴<strong>头对头</strong>重叠，电子密度集中于键轴上。
        键强度大，是单键的基础，也是多重键必有的组成部分。
        可自由旋转（旋转不破坏对称性）。
      </div>
      <span class="bond-ex" style="background:#FAEEDA;color:#633806">
        s–s · s–p · p–p 头对头
      </span>
    </div>
    <div class="bond-card" style="border-color:#CECBF6;background:#EEEDFE18">
      <div class="bond-sym" style="color:#3C3489">π</div>
      <div class="bond-title">π 键 — 侧向重叠</div>
      <div class="bond-desc">
        平行轨道<strong>肩并肩</strong>重叠，电子密度分布于键轴两侧。
        强度小于 σ 键，<strong>不能自由旋转</strong>（旋转会破坏重叠）。
        化学反应常发生在 π 键位置。
      </div>
      <span class="bond-ex" style="background:#EEEDFE;color:#3C3489">
        p–p 侧向 · 多重键中附加形成
      </span>
    </div>
  </div>

  <div class="overlap-row">
    <div class="img-card">
      <img src="{img_431}" alt="σ键重叠方式">
      <div class="img-caption">σ 键的三种重叠方式：s-s、s-p、p-p 头对头</div>
    </div>
    <div class="img-card">
      <img src="{img_432}" alt="π键重叠方式">
      <div class="img-caption">π 键：p-p 侧向重叠，电子密度在键轴两侧</div>
    </div>
  </div>
  <div class="overlap-row">
    <div class="img-card">
      <img src="{img_433}" alt="双键中的σ和π">
      <div class="img-caption">双键（1σ + 1π）：以乙烯 C₂H₄ 为例</div>
    </div>
    <div class="img-card">
      <img src="{img_434}" alt="三键中的σ和π">
      <div class="img-caption">三键（1σ + 2π）：以乙炔 C₂H₂ 为例</div>
    </div>
  </div>
  <div class="note-box">
    一般而言键强度：<strong>σ &gt; π</strong>，因此 σ 键更稳定，π 键更易断裂。
    双键键能 &lt; 单键的两倍，三键键能 &lt; 单键的三倍，说明 π 键比 σ 键弱。
  </div>
</div>

<!-- 4.4 杂化 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">4.4</span>
    <span class="section-title">原子轨道杂化（Hybridization）</span>
  </div>
  <p class="body-text">
    杂化理论用于解释分子的几何构型和键的等价性问题。许多分子（如 CH₄、H₂O）的键角和对称性
    无法仅用原始 s、p 轨道解释。价键理论认为，在成键前原子将能量相近的价层轨道进行
    <strong>线性组合</strong>，形成一组新的杂化轨道，具有更强的方向性和更大的重叠能力。
  </p>

  <table class="hyb-table">
    <tr>
      <th>杂化类型</th>
      <th>组成轨道</th>
      <th>几何构型</th>
      <th>理想键角</th>
      <th>典型例子</th>
    </tr>
    <tr>
      <td><span class="hyb-badge" style="background:#E1F5EE;color:#085041">sp</span></td>
      <td>1s + 1p</td><td>直线形</td><td>180°</td><td>BeCl₂, CO₂, C₂H₂</td>
    </tr>
    <tr>
      <td><span class="hyb-badge" style="background:#E6F1FB;color:#0C447C">sp²</span></td>
      <td>1s + 2p</td><td>平面三角形</td><td>120°</td><td>BCl₃, C₂H₄, 苯</td>
    </tr>
    <tr>
      <td><span class="hyb-badge" style="background:#FAEEDA;color:#633806">sp³</span></td>
      <td>1s + 3p</td><td>正四面体</td><td>109.5°</td><td>CH₄, NH₃, H₂O</td>
    </tr>
    <tr>
      <td><span class="hyb-badge" style="background:#EEEDFE;color:#3C3489">sp³d</span></td>
      <td>1s + 3p + 1d</td><td>三角双锥</td><td>90°/120°</td><td>PCl₅</td>
    </tr>
    <tr>
      <td><span class="hyb-badge" style="background:#FAECE7;color:#712B13">sp³d²</span></td>
      <td>1s + 3p + 2d</td><td>正八面体</td><td>90°</td><td>SF₆</td>
    </tr>
    <tr>
      <td><span class="hyb-badge" style="background:#EAF3DE;color:#27500A">dsp²</span></td>
      <td>1d + 1s + 2p</td><td>平方平面</td><td>90°</td><td>[Ni(CN)₄]²⁻, [PtCl₄]²⁻</td>
    </tr>
  </table>

  <!-- 三张并排 -->
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin:1.25rem 0">
    <div class="img-card">
      <img src="{img_441}" alt="sp杂化">
      <div class="img-caption">sp 杂化：直线形（180°）</div>
    </div>
    <div class="img-card">
      <img src="{img_442}" alt="sp2杂化">
      <div class="img-caption">sp² 杂化：平面三角形（120°）</div>
    </div>
    <div class="img-card">
      <img src="{img_443}" alt="sp3杂化">
      <div class="img-caption">sp³ 杂化：正四面体（109.5°）</div>
    </div>
  </div>

  <!-- 两张并排 -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1.25rem 0">
    <div class="img-card">
      <img src="{img_444}" alt="杂化类型几何构型">
      <div class="img-caption">常见杂化类型几何构型总览</div>
    </div>
    <div class="img-card">
      <img src="{img_445}" alt="分子形状与杂化">
      <div class="img-caption">分子形状、键角与杂化轨道对应关系</div>
    </div>
  </div>

  <div class="note-box">
    <strong>注意：</strong>
    ① 实际分子中孤对电子占据更大空间，会压缩键角（NH₃ ≈ 107°，H₂O ≈ 104.5°）；
    ② 在严格的量子化学计算中，杂化轨道是数学构造而非可观测实体，
    但在结构预测和教学中仍<strong>直观、高效，与 VSEPR 理论互补性强</strong>。
  </div>
</div>

<!-- 4.5 共振论 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">4.5</span>
    <span class="section-title">局限性与共振论（Resonance）</span>
  </div>
  <p class="body-text">
    价键理论在处理<strong>电子非定域化</strong>体系时存在明显不足。
    例如苯分子中所有 C–C 键长完全相等，介于典型单键与双键之间，单一路易斯结构无法解释。
    为此引入<strong>共振论</strong>来描述这类体系。
  </p>

  <div class="blockquote">
    真实分子结构是多个共振式的叠加（共振杂化体），而不是在不同结构之间来回切换。
    共振是一种用定域键语言近似描述非定域电子的方法。
  </div>

  <div class="resonance-rules">
    <div class="res-title">共振式的书写规则</div>
    <div class="res-grid">
      <div class="res-item">✓ <strong>原子核位置不变</strong>，只允许电子移动</div>
      <div class="res-item">✓ <strong>总电子数守恒</strong>，电荷守恒</div>
      <div class="res-item">✓ 允许移动：π 电子、孤对电子、离域电荷</div>
      <div class="res-item">✓ 符合<strong>价键规则</strong>（八隅体等）</div>
    </div>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1.25rem 0">
    <div style="background:#FAEEDA18;border-radius:14px;padding:1.2rem;border:0.5px solid #F0C060">
      <div style="font-size:13px;font-weight:700;color:#633806;margin-bottom:8px">共振能</div>
      <div style="font-size:13px;color:#444;line-height:1.7">
        真实分子的能量低于任一共振式，差值称为<strong>共振能</strong>。
        共振能越大，分子越稳定，电子离域程度越高。
        <br><br>苯的共振能 ≈ <strong>150 kJ/mol</strong>，是其异常稳定的重要来源。
      </div>
    </div>
    <div style="background:#fafafa;border-radius:14px;padding:1.2rem;border:0.5px solid #eee">
      <div style="font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:8px">贡献更大的共振式</div>
      <div style="font-size:13px;color:#444;line-height:1.7">
        · 满足八隅体<br>
        · 电荷分离最小<br>
        · 负电荷位于电负性大的原子上<br>
        · 形式电荷较小
        <br><br>共振杂化体更接近"优势共振式"，而非简单平均。
      </div>
    </div>
  </div>

  <div class="note-box">
    <strong>常见误区：</strong>
    共振不是分子在结构间快速切换；共振式不是真实可分离的结构；
    键也不会在单键与双键之间交替——真实情况是电子离域，键级为分数值。
  </div>
     </div>  <!-- 4.5 section 结束 -->
    """ + RESONANCE_HTML + """
    <div class="quote">    
</div>

<!-- 4.6 MO 与 VB 的关系 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">4.6</span>
    <span class="section-title">MO 理论与 VB 理论的关系</span>
  </div>
  <p class="body-text">
    严格地说，MO 理论与 VB 理论在数学上是<strong>等价</strong>的，
    差异主要来源于对电子相关性的处理方式。两者可以通过修正相互逼近：
  </p>
  <div class="mv-grid">
    <div class="mv-card" style="border-color:#B5D4F4">
      <div class="mv-title" style="color:#185FA5">MO → VB（CI 修正）</div>
      <div class="mv-formula">
        \( \Psi_{{\text{{MO}}}}^{{\text{{CI}}}} = c_1 \Psi_{{\text{{共价}}}} + c_2 \Psi_{{\text{{离子}}}} \)
      </div>
      <div class="mv-desc">
        引入<strong>组态相互作用（CI）</strong>修正简单 MO 对离子性的高估。
        当 \(c_1 \gg c_2\) 时，修正后的 MO 波函数逐渐接近 VB 形式。
      </div>
    </div>
    <div class="mv-card" style="border-color:#F0C060">
      <div class="mv-title" style="color:#633806">VB → MO（引入离子结构）</div>
      <div class="mv-formula">
        \( \Psi_{{\text{{VB}}}} = C_{{\text{{共价}}}} \Psi_{{\text{{共价}}}} + C_{{\text{{离子}}}} \Psi_{{\text{{离子}}}} \)
      </div>
      <div class="mv-desc">
        VB 理论通过引入<strong>离子结构与共振</strong>提高描述精度，
        适当调整权重后可逼近 MO 描述。
      </div>
    </div>
  </div>
  <div class="note-box">
    从分子轨道理论看，共振的本质是<strong>电子离域</strong>，是 π 轨道在多个原子上的展开，
    不需要多个路易斯结构来描述。但在教学中，共振论简单直观、预测能力强，仍被广泛使用。
  </div>
</div>

<div class="quote">
  价键理论以其直观性和对分子几何构型的强解释力，在化学中占据重要地位。<br>
  其核心思想——电子定域化配对与最大重叠原则，是理解分子结构不可或缺的理论工具。
</div>

</body>
</html>
"""

components.html(HTML, height=7000, scrolling=False)
page_footer("vb")
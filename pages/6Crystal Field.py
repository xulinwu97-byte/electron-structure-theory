import streamlit as st
import streamlit.components.v1 as components
import sys, os, base64
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '6.crystal field'))
from cfse_tool import render_cfse_tool
from utils import page_header, page_footer, divider

st.set_page_config(layout="wide", page_title="晶体场理论", page_icon="🔮")

page_header("cft", desc="晶体场理论以简洁的静电模型，解释了过渡金属配合物的颜色、磁性与稳定性——配位化学最重要的理论基础之一。")

# ── 图片 base64 加载 ──────────────────────────────────
def img_b64(rel_path):
    base = os.path.join(os.path.dirname(__file__), '..', rel_path)
    with open(base, 'rb') as f:
        return base64.b64encode(f.read()).decode()

img_61  = img_b64('6.crystal field/6_1.png')
img_62  = img_b64('6.crystal field/6_2.png')
img_63  = img_b64('6.crystal field/6_3.png')
img_641 = img_b64('6.crystal field/6_4_1.png')
img_642 = img_b64('6.crystal field/6_4_2.png')
img_65  = img_b64('6.crystal field/6_5.png')

# ── 公式变量 ─────────────────────────────────────────
f_dd   = r'\( E_{\mathrm{photon}} = h\nu = \Delta_o \)'
f_bc   = r'\( 2 \times (+0.6\,\Delta_o) + 3 \times (-0.4\,\Delta_o) = 0 \)'
f_eg   = r'\( +0.6\,\Delta_o \)'
f_t2g  = r'\( -0.4\,\Delta_o \)'
f_dt   = r'\( \Delta_t \approx \dfrac{4}{9}\,\Delta_o \)'
f_sq   = r'\( E(d_{x^2-y^2}) \gg E(d_{xy}) > E(d_{z^2}) > E(d_{xz},\,d_{yz}) \)'
f_tbp  = r'\( E(d_{z^2}) \gg E(d_{x^2-y^2},\,d_{xy}) > E(d_{xz},\,d_{yz}) \)'
f_sp   = r'\( E(d_{x^2-y^2}) \gg E(d_{z^2}) > E(d_{xy}) > E(d_{xz},\,d_{yz}) \)'
f_cfse = r'\( \mathrm{CFSE} = \left[-0.4\,n(t_{2g}) + 0.6\,n(e_g)\right]\Delta_o - \text{extra pairing energy} \)'
f_spec = r'\( \mathrm{I}^- < \mathrm{Br}^- < \mathrm{Cl}^- < \mathrm{F}^- < \mathrm{OH}^- < \mathrm{H_2O} < \mathrm{NH_3} < \mathrm{en} < \mathrm{CN}^- < \mathrm{CO} \)'

HTML = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif;
  color:#1a1a1a;background:white;padding:2rem 3rem 4rem;line-height:1.8;}}
.lead{{font-size:16px;color:#555;line-height:1.9;max-width:720px;
  margin-bottom:3rem;padding-left:1.2rem;border-left:3px solid #F0997B;}}
.section{{margin-bottom:3.5rem}}
.section-header{{display:flex;align-items:baseline;gap:12px;
  margin-bottom:1.4rem;padding-bottom:0.75rem;border-bottom:0.5px solid #f0f0f0;}}
.section-num{{font-size:12px;font-weight:600;color:#F0997B;letter-spacing:0.05em}}
.section-title{{font-size:20px;font-weight:700;letter-spacing:-0.01em;color:#1a1a1a}}
.sub-header{{display:flex;align-items:baseline;gap:10px;
  margin:1.5rem 0 0.75rem;padding-bottom:0.4rem;border-bottom:0.5px solid #f8f8f8;}}
.sub-num{{font-size:11px;font-weight:600;color:#F0997B}}
.sub-title{{font-size:16px;font-weight:700;color:#1a1a1a}}
.body-text{{font-size:15px;color:#444;line-height:1.9;max-width:740px;margin-bottom:1rem}}
.body-text strong{{color:#1a1a1a;font-weight:600}}
.blockquote{{border-left:3px solid #F0997B;background:#FAECE718;
  padding:0.75rem 1.2rem;border-radius:0 10px 10px 0;
  font-size:15px;color:#712B13;margin:1rem 0;}}
.formula-box{{background:#FAECE7;border-radius:14px;padding:1.2rem 1.5rem;
  margin:1rem 0;border:0.5px solid #F0997B;text-align:center;font-size:18px;color:#712B13;}}
.formula-wide{{background:#fafafa;border-radius:12px;padding:1rem 1.5rem;
  margin:0.75rem 0;border:0.5px solid #eee;text-align:center;font-size:14px;color:#333;overflow-x:auto;}}
.two-col{{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;align-items:start}}
.two-col-rev{{display:grid;grid-template-columns:1fr 340px;gap:2rem;align-items:start}}
.app-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1.25rem 0}}
.app-card{{border-radius:14px;padding:1.2rem;border:0.5px solid #eee;background:#fafafa}}
.app-title{{font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:8px}}
.app-desc{{font-size:13px;color:#444;line-height:1.7}}
.assume-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:1.25rem 0}}
.assume-card{{border-radius:14px;padding:1.1rem;border:0.5px solid #F5C4B3;background:#FAECE718}}
.assume-num{{width:26px;height:26px;border-radius:50%;background:#FAECE7;color:#712B13;
  display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;margin-bottom:8px}}
.assume-title{{font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:5px}}
.assume-desc{{font-size:12px;color:#555;line-height:1.65}}
.orb-card{{border-radius:14px;padding:1.2rem;border:0.5px solid #eee}}
.orb-sym{{font-size:18px;font-weight:800;margin-bottom:6px}}
.orb-title{{font-size:13px;font-weight:700;margin-bottom:6px}}
.orb-desc{{font-size:12px;color:#555;line-height:1.65}}
.orb-badge{{display:inline-block;font-size:11px;padding:2px 9px;border-radius:99px;font-weight:500;margin-top:8px}}
.img-full{{border-radius:14px;overflow:hidden;border:0.5px solid #eee;background:#fafafa;margin:1.25rem 0}}
.img-full img{{width:100%;display:block}}
.img-caption{{font-size:11px;color:#aaa;text-align:center;padding:8px 12px;border-top:0.5px solid #eee}}
.cft-table{{width:100%;border-collapse:collapse;font-size:13px;margin:1rem 0}}
.cft-table th{{background:#FAECE7;padding:8px 12px;border:1px solid #F5C4B3;
  font-weight:600;color:#712B13;text-align:left;}}
.cft-table td{{padding:8px 12px;border:1px solid #eee;color:#444;vertical-align:middle}}
.cft-table tr:hover td{{background:#FFFAF8}}
.color-examples{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:1.25rem 0}}
.color-card{{border-radius:12px;padding:0.9rem;text-align:center;border:0.5px solid #eee}}
.color-dot{{width:36px;height:36px;border-radius:50%;margin:0 auto 8px}}
.color-name{{font-size:12px;font-weight:600;color:#1a1a1a;margin-bottom:3px}}
.color-info{{font-size:11px;color:#888;line-height:1.5}}
.selection-rule{{border-radius:12px;padding:1rem 1.2rem;border:0.5px solid #eee;background:#fafafa;margin:8px 0}}
.rule-title{{font-size:13px;font-weight:700;margin-bottom:6px}}
.rule-desc{{font-size:12px;color:#555;line-height:1.65}}
.rule-badge{{display:inline-block;font-size:11px;padding:2px 8px;border-radius:99px;font-weight:500;margin-top:6px}}
.note-box{{background:#fafafa;border-radius:10px;padding:0.85rem 1.2rem;
  border:0.5px solid #eee;font-size:13px;color:#666;margin:0.75rem 0;line-height:1.65}}
.note-box strong{{color:#1a1a1a}}
.cfse-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:1rem 0}}
.cfse-card{{border-radius:12px;padding:1rem 1.2rem;border:0.5px solid #eee;background:#fafafa}}
.cfse-title{{font-size:12px;font-weight:700;color:#888;margin-bottom:6px;text-transform:uppercase;letter-spacing:0.06em}}
.spec-seq{{background:linear-gradient(to right,#FAECE7,#E1F5EE);border-radius:14px;
  padding:1.25rem 1.5rem;margin:1rem 0;border:0.5px solid #eee;overflow-x:auto;}}
.spec-arrow{{display:flex;align-items:center;margin-top:0.75rem;gap:8px;font-size:12px;}}
.spec-line{{flex:1;height:2px;background:linear-gradient(to right,#F0997B,#5DCAA5)}}
.quote{{background:linear-gradient(135deg,#FAECE7,#EEEDFE);border-radius:16px;
  padding:1.5rem 2rem;margin-top:2rem;font-size:16px;font-weight:600;
  color:#712B13;line-height:1.6;text-align:center;}}
</style>
</head>
<body>

<p class="lead">
  晶体场理论以简洁的静电图像，成功弥补了价键理论在配位化学领域的不足。
  它首次为过渡金属配合物的颜色、磁性与稳定性提供了统一而定量的解释框架。
</p>

<!-- 6.0 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">6.0</span>
    <span class="section-title">我们为什么需要晶体场理论？</span>
  </div>
  <p class="body-text">
    过渡金属配合物展现出一系列令人困惑的性质：颜色鲜艳而多变，同一金属在不同配体环境中颜色迥异，
    某些配合物具有顺磁性而另一些则呈抗磁性。这些现象用传统价键理论难以解释。
    晶体场理论通过引入 <strong>d 轨道分裂能（Δ）</strong> 的概念，为上述现象提供了统一的定量框架。
  </p>
  <div class="app-grid">
    <div class="app-card" style="border-color:#F5C4B3">
      <div class="app-title" style="color:#712B13">颜色的来源</div>
      <div class="app-desc">
        配合物颜色来源于 <strong>d–d 跃迁</strong>：电子从低能级 d 轨道跃迁至高能级时，
        吸收满足 {f_dd} 的可见光，人眼观察到其<strong>补色</strong>。
      </div>
    </div>
    <div class="app-card" style="border-color:#F5C4B3">
      <div class="app-title" style="color:#712B13">磁性的预测</div>
      <div class="app-desc">
        CFT 引入<strong>高自旋与低自旋</strong>概念，通过比较分裂能 Δ 与配对能 P 的大小，
        直接预测未配对电子数与磁矩。
      </div>
    </div>
    <div class="app-card" style="border-color:#F5C4B3">
      <div class="app-title" style="color:#712B13">稳定性的量化</div>
      <div class="app-desc">
        通过定义<strong>晶体场稳定化能（CFSE）</strong>，
        解释不同 d 电子构型在各几何构型下的相对稳定性。
      </div>
    </div>
    <div class="app-card" style="border-color:#F5C4B3">
      <div class="app-title" style="color:#712B13">光谱化学序列</div>
      <div class="app-desc">
        系统揭示配体性质对分裂能大小的规律性影响，建立配体强弱的定量排列。
      </div>
    </div>
  </div>
</div>

<!-- 6.1 静电模型 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">6.1</span>
    <span class="section-title">理论的核心假设：静电模型</span>
  </div>
  <div class="two-col-rev">
    <div>
      <p class="body-text">晶体场理论是纯粹的静电模型，其精妙之处在于：
        仅凭几何关系和静电排斥，便能推导出 d 轨道分裂，进而解释颜色、磁性和稳定性。
      </p>
      <div class="assume-grid" style="grid-template-columns:1fr">
        <div class="assume-card">
          <div class="assume-num">①</div>
          <div class="assume-title">纯离子键合假设</div>
          <div class="assume-desc">金属与配体之间的相互作用被视为静电吸引，完全忽略共价成分。</div>
        </div>
        <div class="assume-card">
          <div class="assume-num">②</div>
          <div class="assume-title">配体视为点电荷或偶极子</div>
          <div class="assume-desc">
            阴离子配体（如 Cl⁻）→ 负点电荷；中性配体（如 H₂O）→ 偶极子，负端朝向金属。
          </div>
        </div>
        <div class="assume-card">
          <div class="assume-num">③</div>
          <div class="assume-title">静电排斥导致轨道分裂</div>
          <div class="assume-desc">配体静电场与 d 电子之间的排斥，因各 d 轨道空间取向不同而强弱各异，打破五重简并。</div>
        </div>
      </div>
    </div>
    <div class="img-full">
      <img src="data:image/png;base64,{img_61}" alt="晶体场静电模型">
      <div class="img-caption">晶体场理论静电模型：配体视为点电荷，以静电场作用于中心金属的 d 轨道</div>
    </div>
  </div>
</div>

<!-- 6.2 d 轨道空间取向 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">6.2</span>
    <span class="section-title">d 轨道的空间取向</span>
  </div>
  <p class="body-text">
    五个 d 轨道根据电子云的分布方向分为两组——这一空间取向差异，正是 d 轨道分裂的几何根源。
  </p>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
    <div class="orb-card" style="border-color:#F5C4B3;background:#FAECE718;padding:1.4rem 1.4rem 1.2rem">
      <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:4px">
        <div class="orb-sym" style="color:#712B13;margin:0">e<sub>g</sub></div>
        <div class="orb-title" style="margin:0">轴向轨道组</div>
        <span class="orb-badge" style="background:#FAECE7;color:#712B13;margin-left:auto">能量升高 {f_eg}</span>
      </div>
      <div class="orb-desc">
        \( d_{{z^2}} \)、\( d_{{x^2-y^2}} \)
        · 电子云沿 x、y、z 轴方向延伸，<strong>正对轴向配体</strong>，受到的排斥最强。
      </div>
    </div>
    <div class="orb-card" style="border-color:#B5D4F4;background:#E6F1FB18;padding:1.4rem 1.4rem 1.2rem">
      <div style="display:flex;align-items:baseline;gap:10px;margin-bottom:4px">
        <div class="orb-sym" style="color:#0C447C;margin:0">t<sub>2g</sub></div>
        <div class="orb-title" style="margin:0">轴间轨道组</div>
        <span class="orb-badge" style="background:#E6F1FB;color:#0C447C;margin-left:auto">能量降低 {f_t2g}</span>
      </div>
      <div class="orb-desc">
        \( d_{{xy}} \)、\( d_{{xz}} \)、\( d_{{yz}} \)
        · 电子云分布在轴之间，<strong>避开配体方向</strong>，受到的排斥较弱。
      </div>
    </div>
  </div>
  <div class="img-full" style="margin-top:14px">
    <img src="data:image/png;base64,{img_62}" alt="d轨道空间取向">
    <div class="img-caption">五个 d 轨道的空间取向：e_g 组指向轴（配体方向），t_2g 组位于轴间；蓝点表示配体位置</div>
  </div>
</div>

<!-- 6.3 八面体分裂 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">6.3</span>
    <span class="section-title">八面体晶体场中的分裂（Δ<sub>o</sub>）</span>
  </div>
  <div class="two-col-rev">
    <div>
      <p class="body-text">
        在八面体场中，六个配体分别沿 ±x、±y、±z 轴接近中心金属离子。
        e<sub>g</sub> 轨道正对配体、能量升高，t<sub>2g</sub> 轨道避开配体、能量降低，
        两组之间的能量差称为 <strong>八面体场分裂能 Δ<sub>o</sub></strong>（或 10Dq）。
      </p>
      <div class="app-grid">
        <div style="background:#FAECE718;border-radius:14px;padding:1.2rem;border:0.5px solid #F5C4B3;text-align:center">
          <div style="font-size:12px;color:#888;margin-bottom:8px">e<sub>g</sub>（2个轨道）</div>
          <div style="font-size:15px;color:#712B13;font-weight:600">{f_eg} 每个轨道</div>
        </div>
        <div style="background:#E6F1FB18;border-radius:14px;padding:1.2rem;border:0.5px solid #B5D4F4;text-align:center">
          <div style="font-size:12px;color:#888;margin-bottom:8px">t<sub>2g</sub>（3个轨道）</div>
          <div style="font-size:15px;color:#0C447C;font-weight:600">{f_t2g} 每个轨道</div>
        </div>
      </div>
      <div class="note-box">
        遵循<strong>重心原理</strong>：{f_bc}
      </div>
    </div>
    <div class="img-full">
      <img src="data:image/png;base64,{img_63}" alt="八面体分裂能级图">
      <div class="img-caption">八面体晶体场 d 轨道分裂：e_g 升高 +0.6Δₒ，t_2g 降低 −0.4Δₒ，总能量守恒</div>
    </div>
  </div>
</div>

<!-- 6.4 应用 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">6.4</span>
    <span class="section-title">晶体场理论的应用</span>
  </div>

  <div class="sub-header">
    <span class="sub-num">A</span>
    <span class="sub-title">配合物颜色的来源</span>
  </div>
  <p class="body-text">
    当光子能量恰好等于 Δ<sub>o</sub> 时，电子发生 <strong>d–d 跃迁</strong>，
    配合物吸收对应波长的可见光，人眼观察到的是其<strong>补色</strong>。
    由于 Δ<sub>o</sub> 受金属种类、氧化态和配体性质共同影响，同一金属与不同配体结合时便呈现截然不同的颜色。
  </p>

  <!-- 典型例子 -->
  <div class="color-examples">
    <div class="color-card" style="background:#F0F8FF">
      <div class="color-dot" style="background:#6495ED"></div>
      <div class="color-name">[Ti(H₂O)₆]³⁺</div>
      <div class="color-info">紫色<br>Δₒ ≈ 2.0 eV<br>吸收黄绿光</div>
    </div>
    <div class="color-card" style="background:#FFF0F5">
      <div class="color-dot" style="background:#FF69B4"></div>
      <div class="color-name">[Co(H₂O)₆]²⁺</div>
      <div class="color-info">粉红色<br>Δₒ ≈ 1.1 eV<br>吸收绿光</div>
    </div>
    <div class="color-card" style="background:#F0FFF0">
      <div class="color-dot" style="background:#228B22"></div>
      <div class="color-name">[Ni(H₂O)₆]²⁺</div>
      <div class="color-info">绿色<br>Δₒ ≈ 1.0 eV<br>吸收红光</div>
    </div>
    <div class="color-card" style="background:#FFF8DC">
      <div class="color-dot" style="background:#4169E1"></div>
      <div class="color-name">[Cu(H₂O)₆]²⁺</div>
      <div class="color-info">蓝色<br>Δₒ ≈ 1.6 eV<br>吸收橙红光</div>
    </div>
  </div>

  <!-- 选择定则文字 -->
  <p class="body-text" style="margin-top:1.5rem">
    尽管 d–d 跃迁是配合物颜色的来源，但量子力学对跃迁有严格的<strong>选择定则</strong>约束，
    使得大多数 d–d 跃迁在形式上是"禁阻"的——这也解释了为什么过渡金属配合物的颜色通常较浅（摩尔吸光系数 ε 较小）。
  </p>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:0.75rem 0">
    <div class="app-card" style="border-color:#F5C4B3">
      <div class="app-title" style="color:#712B13">Laporte 禁阻（宇称禁阻）</div>
      <div class="app-desc">
        跃迁只允许发生在<strong>宇称不同</strong>的轨道之间。d–d 跃迁属于 g→g，违反 Laporte 规则，因此禁阻。
        分子振动耦合可使配合物短暂失去反演中心而部分解禁。<br>
        <span style="font-size:11px;color:#888">ε ≈ 1–100 L·mol⁻¹·cm⁻¹</span>
      </div>
    </div>
    <div class="app-card" style="border-color:#CECBF6">
      <div class="app-title" style="color:#3C3489">自旋禁阻（Spin 禁阻）</div>
      <div class="app-desc">
        跃迁要求前后<strong>自旋多重度不变</strong>（ΔS = 0）。若跃迁涉及自旋翻转则为自旋禁阻。
        自旋-轨道耦合（在重金属中较显著）可部分解禁。<br>
        <span style="font-size:11px;color:#888">ε &lt; 1 L·mol⁻¹·cm⁻¹（双重禁阻）</span>
      </div>
    </div>
  </div>
  <div class="note-box">
    总结：d–d 跃迁通常是 <strong>Laporte 禁阻</strong> 的，有时还是<strong>自旋禁阻</strong>的，
    因此配合物的颜色往往较浅（ε 值小）。相比之下，电荷转移跃迁（LMCT/MLCT）是 Laporte 允许的，
    颜色更深（ε ≈ 10³–10⁵），如 KMnO₄ 的深紫色。
  </div>

  <!-- 两张图左右并排 -->
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1.25rem 0">
    <div class="img-full" style="margin:0">
      <img src="data:image/png;base64,{img_641}" alt="d-d跃迁原理">
      <div class="img-caption">d–d 跃迁原理与互补色轮</div>
    </div>
    <div class="img-full" style="margin:0">
      <img src="data:image/png;base64,{img_642}" alt="选择定则">
      <div class="img-caption">Laporte 禁阻与自旋禁阻选择定则</div>
    </div>
  </div>

  <div class="sub-header">
    <span class="sub-num">B</span>
    <span class="sub-title">高自旋与低自旋</span>
  </div>
  <p class="body-text">
    对于 d⁴–d⁷ 构型，电子面临选择：配对进入已占 t<sub>2g</sub> 轨道（代价：配对能 P），
    还是进入高能级 e<sub>g</sub> 轨道（代价：分裂能 Δ<sub>o</sub>）？
  </p>
  <table class="cft-table">
    <tr><th>场强</th><th>条件</th><th>电子排布</th><th>未配对电子</th><th>磁性</th></tr>
    <tr>
      <td>弱场</td>
      <td>\( \Delta_o &lt; P \)</td>
      <td>高自旋（电子尽量分散）</td>
      <td>多</td>
      <td>顺磁性强</td>
    </tr>
    <tr>
      <td>强场</td>
      <td>\( \Delta_o &gt; P \)</td>
      <td>低自旋（电子优先配对）</td>
      <td>少</td>
      <td>顺磁性弱或抗磁性</td>
    </tr>
  </table>
</div>

<!-- 6.5 其他构型 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">6.5</span>
    <span class="section-title">其他几何构型中的 d 轨道分裂</span>
  </div>
  <p class="body-text">由于配体的空间排列不同，d 轨道的分裂方式在各种构型中各不相同。</p>

  <div class="img-full">
    <img src="data:image/png;base64,{img_65}" alt="不同几何构型能级图与球棍模型">
    <div class="img-caption">五种常见配位构型的 d 轨道分裂能级图（上）与球棍结构模型（下）对比</div>
  </div>

  <div class="app-grid" style="margin-top:1rem">
    <div class="app-card">
      <div class="app-title">四面体晶体场（Δ<sub>t</sub>）</div>
      <div class="app-desc">
        分裂方向与八面体相反，分裂能关系：{f_dt}
        <br>由于 Δ<sub>t</sub> 远小于 Δ<sub>o</sub>，<strong>四面体配合物几乎总是高自旋</strong>。
      </div>
    </div>
    <div class="app-card">
      <div class="app-title">平面四边形晶体场</div>
      <div class="app-desc">
        能级顺序：{f_sq}
        <br>常见于 d⁸ 强场体系（Pt²⁺、Pd²⁺），通常为<strong>低自旋、抗磁性</strong>。
      </div>
    </div>
    <div class="app-card">
      <div class="app-title">三角双锥体（D₃h）</div>
      <div class="app-desc">
        能级顺序：{f_tbp}
        <br>轴向与赤道向配体位置不等价，d_z² 因正对轴向配体而能量最高。
      </div>
    </div>
    <div class="app-card">
      <div class="app-title">四方锥体（C₄v）</div>
      <div class="app-desc">
        能级顺序：{f_sp}
        <br>可视为移去一个轴向配体的八面体，常与三角双锥存在能量竞争。
      </div>
    </div>
  </div>
</div>

<!-- 6.6 CFSE -->
<div class="section">
  <div class="section-header">
    <span class="section-num">6.6</span>
    <span class="section-title">晶体场稳定化能（CFSE）</span>
  </div>
  <p class="body-text">
    d 电子在分裂后的轨道中填充，相较于未分裂的假想状态，体系所获得的净能量降低称为
    <strong>晶体场稳定化能（CFSE）</strong>。CFSE 越大，配合物越稳定。
  </p>
  <div class="formula-box">{f_cfse}</div>
  <p class="body-text" style="margin-top:1rem">以 d⁶ 体系为例：</p>
  <div class="cfse-grid">
    <div class="cfse-card">
      <div class="cfse-title">高自旋 \( t_{{2g}}^4\,e_g^2 \)</div>
      <div style="font-size:13px;color:#444">CFSE = \( -1.6\,\Delta_o \)（+ 1 额外配对能 P）</div>
    </div>
    <div class="cfse-card" style="border-color:#B5D4F4;background:#E6F1FB18">
      <div class="cfse-title" style="color:#0C447C">低自旋 \( t_{{2g}}^6\,e_g^0 \)</div>
      <div style="font-size:13px;color:#444">CFSE = \( -2.4\,\Delta_o \)（+ 3 额外配对能 3P）</div>
    </div>
  </div>
  <div class="note-box">
    当 Δ<sub>o</sub> 足够大时，低自旋的 CFSE 增益超过配对能代价，低自旋构型变得更稳定。
  </div>
</div>

<!-- 6.7 光谱化学序列 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">6.7</span>
    <span class="section-title">光谱化学序列</span>
  </div>
  <p class="body-text">
    通过实验测定不同配体在同一金属上引起的 Δ<sub>o</sub> 大小，得到如下经验性排列：
  </p>
  <div class="spec-seq">
    <div style="font-size:14px;text-align:center;color:#333">{f_spec}</div>
    <div class="spec-arrow">
      <span style="color:#712B13;font-weight:500">← 弱场（高自旋）</span>
      <div class="spec-line"></div>
      <span style="color:#085041;font-weight:500">强场（低自旋）→</span>
    </div>
  </div>
  <div class="note-box">
    CO 和 CN⁻ 虽是中性或带负电的配体，却产生最大的分裂能——这与纯静电模型完全矛盾。
    这一悖论的答案隐藏在 <strong>π 反馈键合</strong>中，将在第七章配位场理论中详细阐述。
  </div>
</div>

<div class="quote">
  晶体场理论以极简洁的静电模型，成功建立起配合物电子结构<br>
  与颜色、磁性、稳定性等宏观性质之间的定量联系。
</div>

</body>
</html>
"""

components.html(HTML, height=5800, scrolling=False)

divider()

st.subheader("🧮 CFSE 计算工具")
st.caption("选择金属离子、配体和几何构型，自动计算晶体场稳定化能与轨道填充情况")
render_cfse_tool()

page_footer("cft")
import streamlit as st
import streamlit.components.v1 as components
import os, base64
from utils import page_header, page_footer, divider

st.set_page_config(layout="wide", page_title="配位场理论", page_icon="⚗️")

page_header("lft", desc="配位场理论将分子轨道理论引入配合物体系，从根本上解释了晶体场理论无法回答的光谱化学序列悖论——Δ 的大小由 π 键合决定，而非静电排斥。")

def img_b64(rel_path):
    base = rel_path
    with open(base, 'rb') as f:
        return base64.b64encode(f.read()).decode()

img_71 = img_b64('images/7_1.png')

f_do   = r'\( \Delta_o = E(e_g^*) - E(t_{2g}) \)'
f_t2g  = r'\( t_{2g} \)'
f_eg   = r'\( e_g^* \)'
f_spec = r'\( \underbrace{\mathrm{I}^- < \mathrm{Br}^- < \mathrm{Cl}^-}_{\pi\text{ 供体，减小}\,\Delta_o} < \underbrace{\mathrm{F}^- < \mathrm{OH}^- < \mathrm{H_2O}}_{\pi\text{ 供体（弱）}} < \underbrace{\mathrm{NH_3} < \mathrm{en}}_{\text{纯}\,\sigma\text{ 供体}} < \underbrace{\mathrm{CN}^- < \mathrm{CO}}_{\pi\text{ 受体，增大}\,\Delta_o} \)'

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
  margin-bottom:3rem;padding-left:1.2rem;border-left:3px solid #ED93B1;}}
.section{{margin-bottom:3.5rem}}
.section-header{{display:flex;align-items:baseline;gap:12px;
  margin-bottom:1.4rem;padding-bottom:0.75rem;border-bottom:0.5px solid #f0f0f0;}}
.section-num{{font-size:12px;font-weight:600;color:#ED93B1;letter-spacing:0.05em}}
.section-title{{font-size:20px;font-weight:700;letter-spacing:-0.01em;color:#1a1a1a}}
.sub-header{{display:flex;align-items:baseline;gap:10px;
  margin:1.5rem 0 0.75rem;padding-bottom:0.4rem;border-bottom:0.5px solid #f8f8f8;}}
.sub-num{{font-size:11px;font-weight:600;color:#ED93B1}}
.sub-title{{font-size:16px;font-weight:700;color:#1a1a1a}}
.body-text{{font-size:15px;color:#444;line-height:1.9;max-width:740px;margin-bottom:1rem}}
.body-text strong{{color:#1a1a1a;font-weight:600}}
.blockquote{{border-left:3px solid #ED93B1;background:#FBEAF018;
  padding:0.75rem 1.2rem;border-radius:0 10px 10px 0;
  font-size:15px;color:#72243E;margin:1rem 0;}}
.two-col{{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;align-items:start}}
.contra-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:1.25rem 0}}
.contra-card{{border-radius:14px;padding:1.2rem;border:0.5px solid #F4C0D1;background:#FBEAF018}}
.contra-num{{width:28px;height:28px;border-radius:50%;background:#FBEAF0;color:#72243E;
  display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:700;margin-bottom:8px}}
.contra-title{{font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:6px}}
.contra-desc{{font-size:12px;color:#555;line-height:1.65}}
.contra-key{{font-size:11px;color:#72243E;margin-top:8px;font-weight:600}}
.ligand-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:1.25rem 0}}
.lig-card{{border-radius:14px;padding:1.1rem;text-align:center}}
.lig-type{{font-size:13px;font-weight:700;margin-bottom:6px}}
.lig-examples{{font-size:13px;color:#555;margin-bottom:8px}}
.lig-effect{{font-size:12px;font-weight:600;padding:3px 10px;border-radius:99px;display:inline-block}}
.mo-table{{width:100%;border-collapse:collapse;font-size:13px;margin:1rem 0}}
.mo-table th{{background:#FBEAF0;padding:8px 12px;border:1px solid #F4C0D1;
  font-weight:600;color:#72243E;text-align:left;}}
.mo-table td{{padding:8px 12px;border:1px solid #eee;color:#444;vertical-align:middle}}
.mo-table tr:hover td{{background:#FFFBFD}}
.pi-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:1.25rem 0}}
.pi-card{{border-radius:14px;padding:1.4rem;border:0.5px solid #eee}}
.pi-title{{font-size:14px;font-weight:700;margin-bottom:10px}}
.pi-desc{{font-size:13px;color:#444;line-height:1.7;margin-bottom:10px}}
.pi-result{{font-size:13px;font-weight:600;padding:6px 12px;border-radius:10px;text-align:center}}
.pi-badge{{font-size:11px;padding:2px 8px;border-radius:99px;font-weight:500;margin-top:8px;display:inline-block}}
.compare-table{{width:100%;border-collapse:collapse;font-size:13px;margin:1rem 0}}
.compare-table th{{padding:10px 14px;font-weight:600;text-align:left;border-bottom:2px solid #f0f0f0}}
.compare-table th:first-child{{color:#888}}
.compare-table th:nth-child(2){{color:#F0997B}}
.compare-table th:nth-child(3){{color:#ED93B1}}
.compare-table td{{padding:10px 14px;border-bottom:0.5px solid #f5f5f5;color:#444}}
.compare-table td:nth-child(2){{color:#712B13}}
.compare-table td:nth-child(3){{color:#72243E;font-weight:500}}
.compare-table tr:last-child td{{border-bottom:none}}
.note-box{{background:#fafafa;border-radius:10px;padding:0.85rem 1.2rem;
  border:0.5px solid #eee;font-size:13px;color:#666;margin:0.75rem 0;line-height:1.65}}
.note-box strong{{color:#1a1a1a}}
.spec-seq{{background:linear-gradient(to right,#FBEAF0,#E1F5EE);border-radius:14px;
  padding:1.25rem 1.5rem;margin:1rem 0;border:0.5px solid #eee;overflow-x:auto;}}
.spec-arrow{{display:flex;align-items:center;margin-top:0.75rem;gap:8px;font-size:12px;}}
.spec-line{{flex:1;height:2px;background:linear-gradient(to right,#ED93B1,#5DCAA5)}}
.quote{{background:linear-gradient(135deg,#FBEAF0,#E6F1FB);border-radius:16px;
  padding:1.5rem 2rem;margin-top:2rem;font-size:16px;font-weight:600;
  color:#72243E;line-height:1.6;text-align:center;}}
.img-full{{border-radius:14px;overflow:hidden;border:0.5px solid #eee;background:#fafafa;margin:1.25rem 0}}
.img-full img{{width:100%;display:block}}
.img-caption{{font-size:11px;color:#aaa;text-align:center;padding:8px 12px;border-top:0.5px solid #eee}}

/* canvas 容器：固定宽高，居中 */
.cv-wrap{{
  border-radius:12px;border:0.5px solid #eee;background:#fafafa;
  margin:0.75rem 0;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;
}}
.cv-title{{
  font-size:12px;font-weight:600;color:#72243E;
  padding:0.75rem 1rem 0.5rem;align-self:flex-start;
}}
.cv-caption{{
  font-size:11px;color:#aaa;text-align:center;
  padding:6px 12px 10px;
}}
.cv-btns{{display:flex;justify-content:center;gap:10px;padding:6px 0;flex-wrap:wrap}}
.info3{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;padding:6px 1rem 8px;width:100%}}
.icard{{background:white;border-radius:8px;padding:0.6rem;text-align:center;border:0.5px solid #eee}}
.icard-l{{font-size:10px;color:#aaa;margin-bottom:3px}}
.icard-v{{font-size:14px;font-weight:500;color:#1a1a1a}}
.abtn{{padding:5px 14px;border-radius:9px;border:0.5px solid #e0e0e0;
  background:white;color:#666;font-size:12px;cursor:pointer;}}
.abtn:hover{{background:#f5f5f5}}
.abtn.on{{background:#FBEAF0;border-color:#F4C0D1;color:#72243E;font-weight:500}}
</style>
</head>
<body>

<p class="lead">
  晶体场理论在解释 d 轨道分裂方面取得了巨大成功，但其"纯静电"假设与实验事实之间存在根本矛盾。
  配位场理论将分子轨道理论引入配合物体系，在保留 CFT 直观图像的同时，赋予其真正的量子力学基础。
</p>

<!-- 7.0 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">7.0</span>
    <span class="section-title">我们为什么需要配位场理论？</span>
  </div>
  <p class="body-text">随着实验精度的提升，CFT 与实验事实之间的矛盾日益凸显，主要体现在三个方面：</p>
  <div class="contra-grid">
    <div class="contra-card">
      <div class="contra-num">①</div>
      <div class="contra-title">光谱化学序列的悖论</div>
      <div class="contra-desc">
        按纯静电模型，电荷密度越高的配体排斥越强，Δ 应越大。
        但实验表明：<strong>中性配体</strong> CO、CN⁻ 是最强场配体，
        <strong>带负电的</strong> I⁻、Br⁻ 却是最弱场配体，与静电模型完全相反。
      </div>
      <div class="contra-key">→ Δ 的大小不取决于静电排斥</div>
    </div>
    <div class="contra-card">
      <div class="contra-num">②</div>
      <div class="contra-title">电子离域化的实验证据</div>
      <div class="contra-desc">
        ESR 实验明确表明：金属 d 电子并非完全定域在金属离子上，
        而是在<strong>金属与配体之间存在电子离域</strong>，说明存在真实的共价相互作用。
      </div>
      <div class="contra-key">→ CFT"纯离子键合"假设不成立</div>
    </div>
    <div class="contra-card">
      <div class="contra-num">③</div>
      <div class="contra-title">键合性质的定量失败</div>
      <div class="contra-desc">
        CFT 无法可靠预测金属–配体键能、键长变化与 σ 键强度，应用范围受到根本性限制。
      </div>
      <div class="contra-key">→ 需要引入轨道重叠与共价性</div>
    </div>
  </div>
  <div class="blockquote">
    <strong>LFT 的核心突破：</strong>Δ 不仅来自静电排斥，更关键地来自<strong>金属–配体之间的 π 键合</strong>。
  </div>
  <p class="body-text">根据配体与金属 d 轨道之间 π 相互作用的性质，LFT 将配体分为三类：</p>
  <div class="ligand-grid">
    <div class="lig-card" style="border:0.5px solid #eee;background:#fafafa">
      <div class="lig-type">σ 供体（非 π）</div>
      <div class="lig-examples">NH₃、en、H₂O</div>
      <span class="lig-effect" style="background:#f0f0f0;color:#666">Δ 基准值</span>
    </div>
    <div class="lig-card" style="border:0.5px solid #F5C4B3;background:#FAECE718">
      <div class="lig-type" style="color:#712B13">π 供体配体</div>
      <div class="lig-examples">Cl⁻、Br⁻、F⁻、OH⁻</div>
      <span class="lig-effect" style="background:#FAECE7;color:#712B13">↓ 减小 Δ</span>
    </div>
    <div class="lig-card" style="border:0.5px solid #9FE1CB;background:#E1F5EE18">
      <div class="lig-type" style="color:#085041">π 受体配体</div>
      <div class="lig-examples">CO、CN⁻、bipy</div>
      <span class="lig-effect" style="background:#E1F5EE;color:#085041">↑ 增大 Δ</span>
    </div>
  </div>

  <!-- CFT 悖论动图 -->
  <div class="cv-wrap">
    <div class="cv-title">交互演示：CFT 静电预测 vs 实验测量值</div>
    <canvas id="c-pd" width="680" height="230"
      style="max-width:680px;width:100%"></canvas>
    <div id="pd-btns" class="cv-btns"></div>
    <div class="cv-caption">点击配体，查看 CFT 静电预测（灰色虚线）与实验测量值（彩色）的差异。CFT 预测"电荷越高 Δ 越大"，但实验完全相反。</div>
  </div>
</div>

<!-- 7.1 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">7.1</span>
    <span class="section-title">核心思想：将 MO 理论应用于配合物</span>
  </div>
  <div class="blockquote">
    将八面体配合物视为一个"超级分子"，用 <strong>LCAO–MO 方法</strong> 描述其整体电子结构。
  </div>
  <p class="body-text">参与分子轨道组合的轨道包括：</p>
  <div class="two-col" style="margin-bottom:1.2rem">
    <div style="background:#FBEAF018;border-radius:12px;padding:0.85rem;border:0.5px solid #F4C0D1">
      <div style="font-size:12px;font-weight:700;color:#72243E;margin-bottom:6px">中心金属价轨道</div>
      <div style="font-size:12px;color:#555;line-height:1.65">
        · 4s（a₁g 对称）<br>· 4p（t₁u 对称）<br>· 3d — eg + t₂g
      </div>
    </div>
    <div style="background:#E1F5EE18;border-radius:12px;padding:0.85rem;border:0.5px solid #9FE1CB">
      <div style="font-size:12px;font-weight:700;color:#085041;margin-bottom:6px">配体轨道</div>
      <div style="font-size:12px;color:#555;line-height:1.65">
        · σ 轨道（沿键轴）<br>· π 轨道（p 轨道）<br>· π* 反键轨道（CO等）
      </div>
    </div>
  </div>
  <p class="body-text">
    通过对称性匹配原则，金属轨道与配体群轨道线性组合，
    生成一套<strong>成键、非键与反键分子轨道</strong>。金属 d 电子的行为正是由这套 MO 能级结构决定的。
  </p>
  <div class="img-full">
    <img src="data:image/png;base64,{img_71}" alt="八面体σ键合MO能级图">
    <div class="img-caption">八面体配合物 σ 键合 MO 能级图：t₂g 保持非键，eg* 因 σ 反键化升高，Δo 由此产生</div>
  </div>
</div>

<!-- 7.2 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">7.2</span>
    <span class="section-title">八面体配合物中的 σ 键合</span>
  </div>
  <p class="body-text">
    首先只考虑六个配体 σ 轨道（沿 ±x、±y、±z 轴指向金属）与金属轨道的相互作用。
  </p>
  <table class="mo-table">
    <tr><th>金属轨道</th><th>对称性</th><th>配体 σ 群轨道</th><th>键合性质</th></tr>
    <tr><td>4s</td><td>\( a_{{1g}} \)</td><td>完全对称的 σ 组合</td><td>σ 成键</td></tr>
    <tr><td>4p</td><td>\( t_{{1u}} \)</td><td>沿 x、y、z 轴的 σ 组合</td><td>σ 成键</td></tr>
    <tr><td>\( d_{{z^2}},\,d_{{x^2-y^2}} \)（eg）</td><td>\( e_g \)</td><td>轴向 σ 组合</td><td><strong>形成 eg* 反键 MO</strong></td></tr>
    <tr><td>\( d_{{xy}},\,d_{{yz}},\,d_{{xz}} \)（t₂g）</td><td>\( t_{{2g}} \)</td><td>无匹配 σ 组合</td><td><strong>非键，能量不变</strong></td></tr>
  </table>
  <div class="blockquote">
    在 LFT 图像中，{f_do}。
    Δo 的本质是 <strong>σ 键合导致的 eg 轨道反键化</strong>，而非纯静电排斥——这是 LFT 与 CFT 最根本的区别。
  </div>
</div>

<!-- 7.3 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">7.3</span>
    <span class="section-title">π 键合：解释光谱化学序列</span>
  </div>
  <p class="body-text">
    σ 键合确定了 Δo 的基准值，但无法解释为什么不同配体能使 Δo 在极大范围内变化。
    答案隐藏在 <strong>π 键合</strong>中——它专门作用于 {f_t2g} 轨道的能量，从而直接调控 Δo 的大小。
  </p>
  <div class="pi-grid">
    <div class="pi-card" style="border-color:#F5C4B3;background:#FAECE718">
      <div class="pi-title" style="color:#712B13">A. π 供体配体（如 Cl⁻、F⁻）</div>
      <div class="pi-desc">
        配体拥有<strong>充满电子的 p 轨道</strong>，与金属 t₂g 轨道发生 π 重叠，
        t₂g 被推向较高能量（成为 π* 反键轨道），t₂g 与 eg* 之间的能量差减小。
      </div>
      <div class="pi-result" style="background:#FAECE7;color:#712B13">Δo 减小 → 弱场配体</div>
      <span class="pi-badge" style="background:#FAECE7;color:#712B13">解释卤素虽带负电却是弱场配体</span>
    </div>
    <div class="pi-card" style="border-color:#9FE1CB;background:#E1F5EE18">
      <div class="pi-title" style="color:#085041">B. π 受体配体（如 CO、CN⁻）</div>
      <div class="pi-desc">
        配体拥有<strong>空置的低能 π* 轨道</strong>，金属 t₂g 电子"反馈"进入这些空轨道，
        形成 <strong>π 反馈键合（back-bonding）</strong>，t₂g 能量被向下稳定化，Δo 增大。
      </div>
      <div class="pi-result" style="background:#E1F5EE;color:#085041">Δo 增大 → 强场配体</div>
      <span class="pi-badge" style="background:#E1F5EE;color:#085041">解释 CO、CN⁻ 为最强场配体</span>
    </div>
  </div>

  <!-- π 反馈键合动画 -->
  <div class="cv-wrap">
    <div class="cv-title">动态演示：π 键合如何调控 t₂g 能级与 Δo</div>
    <canvas id="c-bb" width="680" height="250"
      style="max-width:680px;width:100%"></canvas>
    <div class="cv-btns">
      <button class="abtn on" id="bb-donor"    onclick="setBB('donor',this)">π 供体（Cl⁻）</button>
      <button class="abtn"    id="bb-none"     onclick="setBB('none',this)">纯 σ 供体（NH₃）</button>
      <button class="abtn"    id="bb-acceptor" onclick="setBB('acceptor',this)">π 受体（CO）</button>
    </div>
    <div class="info3">
      <div class="icard"><div class="icard-l">配体类型</div><div class="icard-v" id="bb-type">π 供体</div></div>
      <div class="icard"><div class="icard-l">t₂g 能级</div><div class="icard-v" id="bb-t2g">↑ 升高</div></div>
      <div class="icard"><div class="icard-l">Δo 变化</div><div class="icard-v" id="bb-delta">↓ 减小</div></div>
    </div>
    <div class="cv-caption">切换配体类型，观察 π 键合如何推高或拉低 t₂g 能级，以及 Δo 随之变化的全过程。</div>
  </div>

  <div class="sub-header">
    <span class="sub-num">7.3.3</span>
    <span class="sub-title">光谱化学序列的 LFT 解读</span>
  </div>
  <div class="spec-seq">
    <div style="font-size:13px;text-align:center;color:#333;overflow-x:auto">{f_spec}</div>
    <div class="spec-arrow">
      <span style="color:#712B13;font-weight:500">← π 供体（推高 t₂g，减小 Δo）</span>
      <div class="spec-line"></div>
      <span style="color:#085041;font-weight:500">π 受体（拉低 t₂g，增大 Δo）→</span>
    </div>
  </div>

  <!-- 光谱化学序列交互 -->
  <div class="cv-wrap">
    <div class="cv-title">交互演示：点击配体查看其 π 作用类型与能级变化</div>
    <canvas id="c-sp" width="680" height="340"
      style="max-width:680px;width:100%;cursor:pointer"></canvas>
    <div class="cv-caption">点击序列上的配体，查看其 π 相互作用类型、机制描述，以及 t₂g / eg* 能级的变化示意。</div>
  </div>

  <div class="note-box">
    序列从左到右 Δo 增大，背后是 <strong>π 相互作用性质的系统性变化</strong>：
    π 供体（推高 t₂g）→ 纯 σ 供体（不影响 t₂g）→ π 受体（拉低 t₂g）。
    这彻底修复了 CFT 在光谱化学序列上的根本性失败。
  </div>
</div>

<!-- 7.4 总结 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">7.4</span>
    <span class="section-title">总结：CFT 与 LFT 的关系</span>
  </div>
  <table class="compare-table">
    <tr>
      <th>比较维度</th>
      <th>晶体场理论（CFT）</th>
      <th>配位场理论（LFT）</th>
    </tr>
    <tr><td>键合模型</td><td>纯静电，无共价</td><td>MO 理论，含共价与轨道重叠</td></tr>
    <tr><td>Δ 的来源</td><td>配体静电排斥</td><td>σ 反键化 + π 键合调控</td></tr>
    <tr><td>光谱化学序列</td><td>无法解释</td><td>从 π 键合机制自然导出</td></tr>
    <tr><td>电子离域</td><td>不考虑</td><td>显式包含，与实验一致</td></tr>
    <tr><td>定量预测能力</td><td>仅定性，键能/键长失败</td><td>定量描述，理论完备</td></tr>
    <tr><td>特点</td><td>直观简洁，教学友好</td><td>严格，是向量化学计算的桥梁</td></tr>
  </table>
  <div class="note-box" style="margin-top:1rem">
    两者并非取代关系：<strong>CFT 保留其在定性预测中的价值</strong>，
    LFT 则在需要更精确解释时提供量子力学基础。
  </div>
</div>

<div class="quote">
  配位场理论是对晶体场理论的量子力学修正与扩展：<br>
  保留了 CFT 简洁的 d 轨道分裂图像，将其纳入 MO 理论框架，<br>
  通过引入 π 键合，修复了光谱化学序列的根本性矛盾。
</div>

</body>
</html>

<script>
(function(){{
const amber='#EF9F27', red='#D85A30', green='#1D9E75', blue='#185FA5';

// canvas 尺寸直接用 width/height 属性值（不做 dpr 缩放，避免居左）
// 用 imageSmoothingEnabled 保证清晰度

// ═══ ① π 反馈键合动画 ═══════════════════════
const bb = document.getElementById('c-bb');
const bx = bb.getContext('2d');
bx.imageSmoothingEnabled = false;
const BW = bb.width, BH = bb.height;
let bbMode='donor', bbT=0, bbCur=0, bbTgt=0;
const BB = {{
  donor:    {{label:'π 供体（Cl⁻）',   shift:+28, col:red,   type:'π 供体',    t2g:'↑ 升高', dlt:'↓ 减小'}},
  none:     {{label:'纯 σ 供体（NH₃）', shift:0,   col:blue,  type:'纯 σ 供体', t2g:'— 不变', dlt:'— 基准'}},
  acceptor: {{label:'π 受体（CO）',     shift:-32, col:green, type:'π 受体',    t2g:'↓ 降低', dlt:'↑ 增大'}},
}};
window.setBB = function(m, el) {{
  document.querySelectorAll('[id^=bb-]').forEach(b => b.classList.remove('on'));
  el.classList.add('on');
  bbMode = m; bbTgt = BB[m].shift;
  document.getElementById('bb-type').textContent  = BB[m].type;
  document.getElementById('bb-t2g').textContent   = BB[m].t2g;
  document.getElementById('bb-delta').textContent = BB[m].dlt;
}};
function drawBB() {{
  bx.clearRect(0, 0, BW, BH);
  bbCur += (bbTgt - bbCur) * 0.055;
  const cfg = BB[bbMode], cx = BW/2, eg_y = 70, base = 188, t2g_y = base - bbCur;

  // 列标题
  bx.fillStyle='rgba(0,0,0,0.5)'; bx.font='11px system-ui'; bx.textAlign='center';
  bx.fillText('金属轨道', 80, 16);
  bx.fillText('分子轨道（MO）', cx, 16);
  bx.fillText('配体轨道', BW-80, 16);

  // eg* 两段
  [[cx-80,cx-16],[cx+16,cx+80]].forEach(([a,b2]) => {{
    bx.strokeStyle=red; bx.lineWidth=2.5;
    bx.beginPath(); bx.moveTo(a,eg_y); bx.lineTo(b2,eg_y); bx.stroke();
  }});
  bx.fillStyle=red; bx.font='500 11px system-ui'; bx.textAlign='left';
  bx.fillText('eg*（σ反键）', cx+86, eg_y+4);

  // t2g 三段（动态）
  [[cx-80,cx-22],[cx-6,cx+30],[cx+46,cx+80]].forEach(([a,b2]) => {{
    bx.strokeStyle=cfg.col; bx.lineWidth=2.5;
    bx.beginPath(); bx.moveTo(a,t2g_y); bx.lineTo(b2,t2g_y); bx.stroke();
  }});
  bx.fillStyle=cfg.col; bx.font='500 11px system-ui'; bx.textAlign='left';
  bx.fillText('t₂g', cx+86, t2g_y+4);

  // 基准虚线（左侧金属轨道参考）
  bx.strokeStyle='#ccc'; bx.lineWidth=1.2; bx.setLineDash([4,3]);
  bx.beginPath(); bx.moveTo(30, base); bx.lineTo(128, base); bx.stroke();
  bx.setLineDash([]);
  bx.fillStyle='#bbb'; bx.font='9px system-ui'; bx.textAlign='center';
  bx.fillText('t₂g 基准', 79, base+13);

  // Δo 双箭头
  bx.strokeStyle=amber; bx.lineWidth=1.8;
  bx.beginPath(); bx.moveTo(cx-98, eg_y+2); bx.lineTo(cx-98, t2g_y-2); bx.stroke();
  const mh=7; bx.fillStyle=amber;
  [[cx-98,eg_y+2,1],[cx-98,t2g_y-2,-1]].forEach(([x,y,d]) => {{
    bx.beginPath(); bx.moveTo(x,y); bx.lineTo(x-mh/2,y+d*mh); bx.lineTo(x+mh/2,y+d*mh); bx.closePath(); bx.fill();
  }});
  bx.fillStyle=amber; bx.font='500 13px system-ui'; bx.textAlign='right';
  bx.fillText('Δo', cx-104, (eg_y+t2g_y)/2+5);

  // 配体侧
  if (bbMode === 'donor') {{
    bx.strokeStyle=red; bx.lineWidth=2;
    bx.beginPath(); bx.moveTo(BW-140,228); bx.lineTo(BW-20,228); bx.stroke();
    bx.fillStyle=red; bx.font='10px system-ui'; bx.textAlign='center';
    bx.fillText('π 满占轨道', BW-80, 242);
    const ep = (bbT*0.022) % 1;
    const ex = (BW-140) + ep*(cx+80-(BW-140)), ey = 228 + ep*(t2g_y-228);
    bx.beginPath(); bx.arc(ex,ey,6,0,Math.PI*2); bx.fillStyle='rgba(216,90,48,0.85)'; bx.fill();
    bx.strokeStyle=red; bx.lineWidth=1.4;
    bx.beginPath(); bx.moveTo(cx+92,t2g_y+4); bx.lineTo(cx+92,base-4); bx.stroke();
    bx.fillStyle=red; bx.font='10px system-ui'; bx.textAlign='center'; bx.fillText('推高',cx+92,t2g_y-10);
  }} else if (bbMode === 'acceptor') {{
    bx.strokeStyle=green; bx.lineWidth=2; bx.setLineDash([5,3]);
    bx.beginPath(); bx.moveTo(BW-140,70); bx.lineTo(BW-20,70); bx.stroke(); bx.setLineDash([]);
    bx.fillStyle=green; bx.font='10px system-ui'; bx.textAlign='center'; bx.fillText('π* 空轨道',BW-80,60);
    const ep2 = (bbT*0.018) % 1;
    const ex2 = cx + ep2*((BW-140)-cx), ey2 = t2g_y + ep2*(70-t2g_y);
    bx.beginPath(); bx.arc(ex2,ey2,6,0,Math.PI*2); bx.fillStyle='rgba(29,158,117,0.85)'; bx.fill();
    bx.strokeStyle=green; bx.lineWidth=1.4;
    bx.beginPath(); bx.moveTo(cx+92,base-4); bx.lineTo(cx+92,t2g_y+4); bx.stroke();
    bx.fillStyle=green; bx.font='10px system-ui'; bx.textAlign='center'; bx.fillText('拉低',cx+92,t2g_y+18);
    bx.fillStyle='rgba(29,158,117,0.55)'; bx.font='9px system-ui'; bx.fillText('back-bonding ↑',BW-80,46);
  }} else {{
    bx.strokeStyle='#ccc'; bx.lineWidth=1.5;
    bx.beginPath(); bx.moveTo(BW-140,155); bx.lineTo(BW-20,155); bx.stroke();
    bx.fillStyle='#bbb'; bx.font='10px system-ui'; bx.textAlign='center'; bx.fillText('σ 轨道（无π）',BW-80,170);
  }}

  bx.fillStyle='rgba(0,0,0,0.25)'; bx.font='500 12px system-ui'; bx.textAlign='center';
  bx.fillText(cfg.label, cx, BH-8);
  bbT++;
  requestAnimationFrame(drawBB);
}}
drawBB();

// ═══ ② CFT 悖论 ═════════════════════════════
const pd = document.getElementById('c-pd');
const px = pd.getContext('2d');
px.imageSmoothingEnabled = false;
const PW = pd.width, PH = pd.height;
const LPDS = [
  {{name:'I⁻',  charge:-1, exp:0.90, cft:2.80, col:'#534AB7'}},
  {{name:'Br⁻', charge:-1, exp:1.05, cft:2.60, col:'#7F77DD'}},
  {{name:'Cl⁻', charge:-1, exp:1.20, cft:2.40, col:'#185FA5'}},
  {{name:'F⁻',  charge:-1, exp:1.40, cft:2.20, col:'#378ADD'}},
  {{name:'OH⁻', charge:-1, exp:1.55, cft:2.00, col:'#5DCAA5'}},
  {{name:'H₂O', charge:0,  exp:1.80, cft:1.50, col:'#1D9E75'}},
  {{name:'NH₃', charge:0,  exp:2.20, cft:1.30, col:'#EF9F27'}},
  {{name:'CN⁻', charge:-1, exp:3.20, cft:2.50, col:'#D85A30'}},
  {{name:'CO',  charge:0,  exp:3.50, cft:1.20, col:'#A32D2D'}},
];
let pdSel = null;
const pdBtns = document.getElementById('pd-btns');
LPDS.forEach((l,i) => {{
  const b = document.createElement('button');
  b.className = 'abtn'; b.textContent = l.name; b.style.borderColor = l.col;
  b.onclick = () => {{ pdSel = i; drawPD(); }};
  pdBtns.appendChild(b);
}});
function drawPD() {{
  px.clearRect(0,0,PW,PH);
  const maxV=4.2, bW=46, gap=13, sx0=32;
  // 网格
  px.strokeStyle='#f0f0f0'; px.lineWidth=1;
  for (let v=0; v<=4; v++) {{
    const y = PH-45 - (v/maxV)*(PH-78);
    px.beginPath(); px.moveTo(28,y); px.lineTo(PW-10,y); px.stroke();
    px.fillStyle='#bbb'; px.font='9px system-ui'; px.textAlign='right'; px.fillText(v+'',26,y+3);
  }}
  px.fillStyle='#888'; px.font='10px system-ui'; px.textAlign='left'; px.fillText('Δo (eV)',4,16);
  LPDS.forEach((l,i) => {{
    const x = sx0+i*(bW+gap);
    const isSel = pdSel===i, alpha = pdSel===null||isSel ? 1 : 0.25;
    const expH=(l.exp/maxV)*(PH-78), cftH=(l.cft/maxV)*(PH-78);
    const ey=PH-45-expH, cy=PH-45-cftH;
    // CFT 预测虚线
    px.globalAlpha = alpha*0.55; px.strokeStyle='#bbb'; px.lineWidth=1.5; px.setLineDash([4,3]);
    px.beginPath(); px.moveTo(x+bW/2,PH-45); px.lineTo(x+bW/2,cy); px.stroke(); px.setLineDash([]);
    px.beginPath(); px.moveTo(x+2,cy); px.lineTo(x+bW-2,cy); px.stroke();
    // 实验柱
    px.globalAlpha = alpha; px.fillStyle = l.col; px.fillRect(x, ey, bW, expH);
    // 选中标注
    if (isSel) {{
      const diff = l.cft-l.exp, midY = (cy+ey)/2;
      px.strokeStyle=amber; px.lineWidth=1.5;
      px.beginPath(); px.moveTo(x+bW+6,cy); px.lineTo(x+bW+6,ey); px.stroke();
      px.fillStyle=amber; px.font='500 10px system-ui'; px.textAlign='left';
      px.fillText(diff>0 ? `CFT 高估 ${{diff.toFixed(2)}} eV` : `CFT 低估 ${{Math.abs(diff).toFixed(2)}} eV`, x+bW+10, midY+4);
    }}
    px.globalAlpha=1;
    px.fillStyle = isSel ? l.col : '#555';
    px.font = isSel ? '500 11px system-ui' : '10px system-ui'; px.textAlign='center';
    px.fillText(l.name, x+bW/2, PH-28);
    px.fillStyle='#bbb'; px.font='9px system-ui';
    px.fillText(l.charge===0?'中性':'阴离子', x+bW/2, PH-16);
  }});
  px.globalAlpha=1;
  // 图例
  px.setLineDash([4,3]); px.strokeStyle='#bbb'; px.lineWidth=1.5;
  px.beginPath(); px.moveTo(PW-142,12); px.lineTo(PW-118,12); px.stroke(); px.setLineDash([]);
  px.fillStyle='#888'; px.font='10px system-ui'; px.textAlign='left'; px.fillText('CFT 预测',PW-114,16);
  px.fillStyle=red; px.fillRect(PW-142,24,20,9); px.fillStyle='#888'; px.fillText('实验值',PW-114,33);
  if (pdSel===null) {{
    px.fillStyle='#bbb'; px.font='11px system-ui'; px.textAlign='center';
    px.fillText('← 点击配体查看差异 →', PW/2, PH-3);
  }}
}}
drawPD();

// ═══ ③ 光谱化学序列 ═════════════════════════
const sp = document.getElementById('c-sp');
const sx = sp.getContext('2d');
sx.imageSmoothingEnabled = false;
const SW = sp.width, SH = sp.height;
const SPEC = [
  {{name:'I⁻',  type:'donor',    delta:0.90, desc:['强 π 供体','满占 p 轨道推高 t₂g','Δo 最小，弱场']}},
  {{name:'Br⁻', type:'donor',    delta:1.05, desc:['强 π 供体','满占 p 轨道推高 t₂g']}},
  {{name:'Cl⁻', type:'donor',    delta:1.20, desc:['π 供体','推高 t₂g，减小 Δo']}},
  {{name:'F⁻',  type:'wdonor',   delta:1.40, desc:['弱 π 供体','推高 t₂g（程度较弱）']}},
  {{name:'OH⁻', type:'wdonor',   delta:1.55, desc:['弱 π 供体','孤对电子参与 π 作用']}},
  {{name:'H₂O', type:'sigma',    delta:1.80, desc:['纯 σ 供体','无 π 作用，基准 Δo']}},
  {{name:'NH₃', type:'sigma',    delta:2.20, desc:['纯 σ 供体','无 π 轨道，Δo 中等']}},
  {{name:'en',  type:'sigma',    delta:2.40, desc:['螯合纯 σ 供体','螯合效应略增强']}},
  {{name:'CN⁻', type:'acceptor', delta:3.20, desc:['强 π 受体','π* 轨道拉低 t₂g','Δo 大，强场']}},
  {{name:'CO',  type:'acceptor', delta:3.50, desc:['最强 π 受体','back-bonding 极强','Δo 最大']}},
];
const TC = {{donor:red, wdonor:amber, sigma:'#888780', acceptor:green}};
const TL = {{donor:'π 供体（弱场）', wdonor:'弱 π 供体', sigma:'纯 σ 供体', acceptor:'π 受体（强场）'}};
let spSel=null, spHov=-1;
const DOT_Y=200, RV=16;  // 节点在200，上方有足够空间放弹出卡片

function getMousePos(e) {{
  const r = sp.getBoundingClientRect();
  return {{
    x: (e.clientX-r.left) / r.width  * SW,
    y: (e.clientY-r.top)  / r.height * SH,
  }};
}}
sp.addEventListener('mousemove', e => {{
  const {{x,y}} = getMousePos(e);
  const step = (SW-80)/(SPEC.length-1);
  let f=-1;
  SPEC.forEach((_,i) => {{ const px2=40+i*step; if(Math.abs(x-px2)<RV+6&&Math.abs(y-DOT_Y)<RV+6) f=i; }});
  if(f!==spHov){{ spHov=f; drawSP(); }}
}});
sp.addEventListener('click', e => {{
  const {{x,y}} = getMousePos(e);
  const step = (SW-80)/(SPEC.length-1);
  let f=-1;
  SPEC.forEach((_,i) => {{ const px2=40+i*step; if(Math.abs(x-px2)<RV+6&&Math.abs(y-DOT_Y)<RV+6) f=i; }});
  spSel = (f===spSel) ? null : f; drawSP();
}});
function drawSP() {{
  sx.clearRect(0,0,SW,SH);
  const step = (SW-80)/(SPEC.length-1);
  // 渐变背景条
  const g = sx.createLinearGradient(40,0,SW-40,0);
  g.addColorStop(0,'rgba(216,90,48,0.07)'); g.addColorStop(0.5,'rgba(136,135,128,0.04)'); g.addColorStop(1,'rgba(29,158,117,0.07)');
  sx.fillStyle=g; sx.beginPath(); sx.roundRect(40,DOT_Y-RV-4,SW-80,RV*2+8,8); sx.fill();
  // 渐变轴线
  const ag = sx.createLinearGradient(40,0,SW-40,0);
  ag.addColorStop(0,TC.donor); ag.addColorStop(0.5,TC.sigma); ag.addColorStop(1,TC.acceptor);
  sx.strokeStyle=ag; sx.lineWidth=3; sx.beginPath(); sx.moveTo(40,DOT_Y); sx.lineTo(SW-40,DOT_Y); sx.stroke();
  // 底部标签
  sx.fillStyle=TC.donor;    sx.font='11px system-ui'; sx.textAlign='left';  sx.fillText('← 弱场 / 高自旋',44,SH-8);
  sx.fillStyle=TC.acceptor; sx.textAlign='right'; sx.fillText('强场 / 低自旋 →',SW-44,SH-8);
  sx.fillStyle='#bbb'; sx.font='10px system-ui'; sx.textAlign='center'; sx.fillText('Δo 依次增大 →',SW/2,DOT_Y-30);
  // 节点
  SPEC.forEach((l,i) => {{
    const x=40+i*step, col=TC[l.type], isSel=spSel===i, isHov=spHov===i;
    const sc=isSel?1.3:isHov?1.15:1, cr=RV*sc;
    sx.beginPath(); sx.arc(x,DOT_Y,cr,0,Math.PI*2);
    sx.fillStyle = isSel||isHov ? col : col+'88'; sx.fill();
    if(isSel){{ sx.strokeStyle=col; sx.lineWidth=2; sx.stroke(); }}
    sx.fillStyle = isSel?col:'#555';
    sx.font = isSel?'500 11px system-ui':'10px system-ui'; sx.textAlign='center';
    sx.fillText(l.name, x, DOT_Y+cr+15);
    sx.fillStyle='#aaa'; sx.font='9px system-ui'; sx.fillText(l.delta.toFixed(2), x, DOT_Y+cr+27);
  }});
  // 弹出卡片（始终向上）
  if (spSel!==null) {{
    const l=SPEC[spSel], x=40+spSel*step, col=TC[l.type];
    const cW=205, cH=l.desc.length*18+60;
    let cx2 = x-cW/2; cx2=Math.max(6,Math.min(SW-cW-6,cx2));
    const cy2 = DOT_Y-RV-18-cH;  // 上方弹出，留足空间
    // 卡片
    sx.fillStyle='white'; sx.strokeStyle=col; sx.lineWidth=1.5;
    sx.beginPath(); sx.roundRect(cx2,cy2,cW,cH,10); sx.fill(); sx.stroke();
    // 标题
    sx.fillStyle=col; sx.font='500 12px system-ui'; sx.textAlign='left';
    sx.fillText(l.name+' — '+TL[l.type], cx2+10, cy2+20);
    // 描述行
    sx.fillStyle='#555'; sx.font='11px system-ui';
    l.desc.forEach((ln,li) => sx.fillText(ln, cx2+10, cy2+38+li*18));
    // 能级小图（右侧）
    const base_y=cy2+cH-26, eg2=base_y-40;
    const shift = l.type==='donor'?12 : l.type==='wdonor'?6 : l.type==='acceptor'?-14 : 0;
    const t2g_y2 = base_y+shift;
    sx.strokeStyle='#e0e0e0'; sx.lineWidth=1.5;
    sx.beginPath(); sx.moveTo(cx2+cW-62,base_y); sx.lineTo(cx2+cW-10,base_y); sx.stroke();
    sx.strokeStyle=col; sx.lineWidth=2;
    sx.beginPath(); sx.moveTo(cx2+cW-62,t2g_y2); sx.lineTo(cx2+cW-10,t2g_y2); sx.stroke();
    sx.strokeStyle=red; sx.lineWidth=1.5;
    sx.beginPath(); sx.moveTo(cx2+cW-62,eg2); sx.lineTo(cx2+cW-10,eg2); sx.stroke();
    sx.fillStyle=red;  sx.font='9px system-ui'; sx.textAlign='right'; sx.fillText('eg*',  cx2+cW-6,eg2+3);
    sx.fillStyle=col;  sx.fillText('t₂g',  cx2+cW-6, t2g_y2+3);
    sx.fillStyle='#ccc'; sx.fillText('基准', cx2+cW-6, base_y+3);
  }}
}}
drawSP();
}})();
</script>
"""

components.html(HTML, height=5000, scrolling=False)
page_footer("lft")
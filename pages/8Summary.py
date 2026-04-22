import sys
sys.path.insert(0, "tools/")

import streamlit as st
from utils import page_header, page_footer

st.set_page_config(page_title="理论总结", layout="wide")

page_header("📊 理论总结", "各理论的适用范围与优缺点对比")

st.markdown("""
<style>
/* ── 全局表格美化 ── */
.summary-section h2 {
    font-size: 1.15rem;
    font-weight: 600;
    margin: 2rem 0 0.6rem;
    padding-left: 0.6rem;
    border-left: 4px solid #534AB7;
    color: #2c2c3e;
}
.highlight-box {
    background: linear-gradient(135deg, #f0efff 0%, #e8f4ff 100%);
    border: 1px solid #c5c0f0;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin: 1rem 0 1.6rem;
    font-size: 0.9rem;
    color: #3a3560;
    line-height: 1.7;
}
.badge-mo   { background:#534AB7; color:#fff; padding:2px 10px; border-radius:99px; font-size:12px; }
.badge-vb   { background:#2e86ab; color:#fff; padding:2px 10px; border-radius:99px; font-size:12px; }
.badge-cft  { background:#e07b39; color:#fff; padding:2px 10px; border-radius:99px; font-size:12px; }
.badge-lft  { background:#3aaa6e; color:#fff; padding:2px 10px; border-radius:99px; font-size:12px; }

table { width:100%; border-collapse:collapse; font-size:0.875rem; margin-bottom:1.2rem; }
thead th {
    background: #534AB7;
    color: white;
    padding: 10px 14px;
    text-align: left;
    font-weight: 500;
}
tbody tr:nth-child(even) { background: #f7f7fb; }
tbody tr:hover           { background: #eeedfe; }
tbody td { padding: 9px 14px; border-bottom: 1px solid #e4e4ee; vertical-align:top; line-height:1.55; }
.pro  { color: #2a7a4f; font-weight:500; }
.con  { color: #b0400e; font-weight:500; }
.vs-box {
    border: 2px solid #534AB7;
    border-radius: 12px;
    padding: 1.2rem 1.6rem;
    margin: 1.2rem 0;
    background: #fafafe;
}
.vs-box h3 { font-size:1rem; font-weight:600; margin-bottom:0.8rem; color:#534AB7; }
.vs-grid { display:grid; grid-template-columns:1fr 40px 1fr; gap:0.5rem; align-items:start; }
.vs-col  { font-size:0.85rem; }
.vs-col b { display:block; font-size:0.95rem; margin-bottom:0.4rem; }
.vs-sep  { display:flex; align-items:center; justify-content:center; font-size:1.4rem; color:#aaa; padding-top:1.5rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="summary-section">', unsafe_allow_html=True)

# ─── 1. 原子轨道 ───────────────────────────────────────────
st.markdown("## 1. 原子轨道理论 (Atomic Orbital Theory)")
st.markdown("""
<div class="highlight-box">
基于量子力学的薛定谔方程，用波函数 ψ 描述电子在原子核周围的概率分布。
是理解所有化学键理论的基础出发点。
</div>
""", unsafe_allow_html=True)

st.markdown("""
| 维度 | 内容 |
|------|------|
| **适用范围** | 孤立原子的电子结构；解释元素周期律；为 MO / VB 理论提供轨道基组 |
| **✅ 优点** | 严格量子力学推导；物理图像清晰（s/p/d/f 形状）；普适所有元素 |
| **❌ 缺点** | 仅适用于氢原子的精确解；多电子原子需近似（屏蔽效应）；不描述化学键 |
""")

# ─── 2. 分子轨道 vs 价键 ───────────────────────────────────
st.markdown("## 2. 分子轨道理论 vs 价键理论")

st.markdown("""
<div class="vs-box">
<h3>⚔️ MO vs VB — 核心对比</h3>
<div class="vs-grid">
  <div class="vs-col">
    <b><span class="badge-mo">MO 分子轨道理论</span></b>
    电子属于整个分子，轨道离域遍布全分子；
    自然解释磁性（O₂顺磁性）、离域π体系、芳香性；
    为计算化学主流框架（HF / DFT 基础）
  </div>
  <div class="vs-sep">VS</div>
  <div class="vs-col">
    <b><span class="badge-vb">VB 价键理论</span></b>
    电子定域在两原子之间形成键；
    直观描述共价键（σ/π 键、杂化轨道）；
    共振结构解释部分离域；
    与化学家日常结构式思维最契合
  </div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
|  | **MO 理论** | **VB / 杂化轨道理论** |
|---|---|---|
| **适用范围** | 所有分子；特别适合共轭/芳香体系、开壳层分子、过渡态 | 饱和有机分子；σ 骨架描述；定性解释分子几何 |
| **✅ 优点** | 定量精度高；自然处理离域；可拓展至计算化学 | 直观、符合直觉；轨道杂化解释空间构型；共振清晰 |
| **❌ 缺点** | 物理图像抽象（轨道无定域感）；计算量大 | 无法精确处理离域（需引入大量共振式）；磁性预测失败（如 O₂） |
| **典型例子** | O₂ 顺磁性、苯π体系、H₂⁺ | CH₄ 的 sp³ 杂化、H₂O 的 sp³ 键角解释 |
| **与计算化学关系** | ⭐⭐⭐⭐⭐ 直接基础 | ⭐⭐ 需大量修正（GVB 等） |
""")

st.info("💡 **现代观点**：MO 与 VB 在极限条件下等价，可相互转换；实际研究中 MO 框架主导计算，VB 框架主导概念交流。")

# ─── 3. Hückel ─────────────────────────────────────────────
st.markdown("## 3. Hückel 分子轨道理论 (HMO)")
st.markdown("""
| 维度 | 内容 |
|------|------|
| **适用范围** | 平面共轭π体系（苯、丁二烯、萘等）；判断芳香性（4n+2规则） |
| **✅ 优点** | 计算极简（仅需拓扑矩阵）；芳香性判据直观；历史意义重大 |
| **❌ 缺点** | 仅限平面π电子，完全忽略σ骨架；无法处理杂原子修正不充分；精度有限 |
| **延伸** | 扩展 Hückel（EHM）纳入所有价电子；现代 DFT 取代定量计算 |
""")

# ─── 4. CFT vs LFT ─────────────────────────────────────────
st.markdown("## 4. 晶体场理论 vs 配位场理论")

st.markdown("""
<div class="vs-box">
<h3>⚔️ CFT vs LFT — 核心对比</h3>
<div class="vs-grid">
  <div class="vs-col">
    <b><span class="badge-cft">CFT 晶体场理论</span></b>
    纯静电模型：配体视为点电荷，只考虑对 d 轨道的静电排斥；
    成功解释 d 轨道分裂（Δ）、颜色、磁性；
    模型简单，参数少（仅 Δ）
  </div>
  <div class="vs-sep">VS</div>
  <div class="vs-col">
    <b><span class="badge-lft">LFT 配位场理论</span></b>
    结合 MO 思想：允许金属–配体共价成键（σ + π）；
    用配体场参数（Dq、Ds、Dt 或 AOM 参数）描述；
    解释光谱化学序列中共价性贡献；
    可处理 π 给体/受体配体（CO、CN⁻ 等）
  </div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
|  | **CFT 晶体场理论** | **LFT 配位场理论** |
|---|---|---|
| **模型本质** | 纯静电（离子模型） | 静电 + 共价（MO 框架） |
| **适用范围** | 八面体/四面体等高对称过渡金属配合物的定性分析 | 所有过渡金属配合物；特别适合含π配体体系 |
| **✅ 优点** | 概念简单；Δ₀ 直接解释颜色与磁性；参数少易用 | 物理图像更真实；可解释光谱化学序列顺序；处理 π 反馈键 |
| **❌ 缺点** | 忽略共价性——无法解释为何 CO（中性）Δ 极大；无法描述 π 键 | 参数增多，模型复杂；AOM 参数需拟合实验 |
| **关键参数** | Δ（分裂能）、CFSE | Dq, Ds, Dt；AOM: eσ, eπ |
| **π 配体处理** | ❌ 无法处理 | ✅ π 给体→减小 Δ；π 受体→增大 Δ |
| **典型应用** | 高/低自旋判断；[Fe(H₂O)₆]²⁺ 颜色 | [Fe(CN)₆]⁴⁻、[Cr(CO)₆] 光谱解释 |
""")

st.info("💡 **关键洞察**：CFT 无法解释为何 CN⁻ 和 CO（弱静电配体）却产生最大 Δ——这正是 LFT 的 π 反馈成键概念的必要性所在。")

# ─── 5. 全览对比表 ─────────────────────────────────────────
st.markdown("## 5. 全理论横向对比速查表")

st.markdown("""
| 理论 | 层级 | 核心思想 | 最适场景 | 精度 | 复杂度 |
|------|------|----------|----------|------|--------|
| 原子轨道 | 原子 | 薛定谔方程/ψ | 元素性质、周期律 | 精确(H)→近似(多e⁻) | ⭐ |
| VB/杂化轨道 | 分子 | 定域键、杂化 | 饱和分子构型 | 定性 | ⭐⭐ |
| MO 理论 | 分子 | 离域轨道、LCAO | 共轭体系、磁性 | 定量 | ⭐⭐⭐ |
| Hückel HMO | π体系 | 拓扑矩阵 | 芳香性判断 | 半定量 | ⭐ |
| CFT 晶体场 | 配合物 | 静电排斥 d 分裂 | 颜色/磁性定性 | 定性 | ⭐⭐ |
| LFT 配位场 | 配合物 | MO + 静电混合 | π配体、光谱 | 半定量 | ⭐⭐⭐⭐ |
""")

st.markdown('</div>', unsafe_allow_html=True)

page_footer("summary")

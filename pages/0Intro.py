import streamlit as st
import streamlit.components.v1 as components
import base64
from utils import page_header, page_footer, divider, load_md

st.set_page_config(layout="wide", page_title="引言", page_icon="📘")

page_header("intro", desc="从道尔顿原子论到量子力学模型，追溯人类理解分子结构的历史脉络。")

# ── 把图片转成 base64，才能嵌进 components.html ──────────
def img_to_b64(path):
    try:
        with open(path, "rb") as f:
            ext = path.split(".")[-1].lower()
            mime = "image/png" if ext == "png" else "image/jpeg"
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"
    except:
        return ""

img1 = img_to_b64("0.intro/1.png")
img2 = img_to_b64("0.intro/2.png")
img3 = img_to_b64("0.intro/3.png")
img4 = img_to_b64("0.intro/4.png")
img5 = img_to_b64("0.intro/5.png")

# ── 主体 HTML ────────────────────────────────────────────
HTML = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC',
                 'Hiragino Sans GB', sans-serif;
    color: #1a1a1a; background: white; padding: 2rem 3rem 4rem;
    line-height: 1.8;
}}

/* ── 引言段落 ── */
.intro-lead {{
    font-size: 17px; color: #555; max-width: 720px;
    line-height: 1.9; margin-bottom: 3rem;
    border-left: 3px solid #e0e0e0;
    padding-left: 1.2rem;
}}

/* ── 时间线容器 ── */
.timeline {{ display: flex; flex-direction: column; gap: 0; }}

/* ── 每个时间线节点 ── */
.tl-item {{
    display: grid;
    grid-template-columns: 1fr 48px 1fr;
    min-height: 320px;
    align-items: stretch;
}}

/* 左右内容区 */
.tl-content {{
    padding: 2.5rem 2rem;
    display: flex; flex-direction: column; justify-content: center;
}}
.tl-content.right {{ text-align: left; }}

/* 中间轴 */
.tl-axis {{
    display: flex; flex-direction: column;
    align-items: center; position: relative;
}}
.tl-line {{
    width: 1px; background: #e8e8e8;
    flex: 1;
}}
.tl-node {{
    width: 12px; height: 12px; border-radius: 50%;
    border: 2px solid white;
    flex-shrink: 0; z-index: 1;
    margin: 0;
}}

/* 年份徽章 */
.tl-year {{
    font-size: 11px; font-weight: 600; color: #bbb;
    letter-spacing: 0.06em; margin-bottom: 8px;
    text-transform: uppercase;
}}

/* 标题 */
.tl-title {{
    font-size: 20px; font-weight: 700;
    letter-spacing: -0.01em; margin-bottom: 12px;
    color: #1a1a1a; line-height: 1.3;
}}

/* 正文 */
.tl-body {{
    font-size: 14px; color: #555; line-height: 1.85;
}}
.tl-body strong {{ color: #1a1a1a; font-weight: 600; }}

/* 贡献/局限标签 */
.tag-row {{ display: flex; gap: 8px; margin-top: 14px; flex-wrap: wrap; }}
.tag {{
    font-size: 11px; padding: 3px 10px; border-radius: 99px;
    font-weight: 500;
}}
.tag.contrib {{ background: #E1F5EE; color: #085041; }}
.tag.limit  {{ background: #FAECE7; color: #712B13; }}

/* 图片区 */
.tl-img {{
    display: flex; align-items: center; justify-content: center;
    padding: 1.5rem;
    background: #fafafa;
    border-radius: 16px;
    margin: 1rem;
}}
.tl-img img {{
    max-width: 100%; max-height: 240px;
    object-fit: contain; border-radius: 8px;
}}

/* 公式块 */
.formula {{
    background: #f8f8fa; border-radius: 10px;
    padding: 1rem 1.2rem; margin: 12px 0;
    font-size: 15px; text-align: center;
    border: 0.5px solid #eee;
}}

/* 最后结语 */
.conclusion {{
    background: linear-gradient(135deg, #EEEDFE 0%, #E1F5EE 100%);
    border-radius: 16px; padding: 2rem 2.5rem;
    margin-top: 1rem;
}}
.conclusion h3 {{
    font-size: 18px; font-weight: 700; color: #3C3489;
    margin-bottom: 10px;
}}
.conclusion p {{
    font-size: 14px; color: #444; line-height: 1.85;
}}

/* 奇偶交替背景 */
.tl-item:nth-child(odd)  .tl-content.left  {{ background: white; border-radius: 16px 0 0 16px; }}
.tl-item:nth-child(odd)  .tl-content.right {{ background: #fafafa; border-radius: 0 16px 16px 0; }}
.tl-item:nth-child(even) .tl-content.left  {{ background: #fafafa; border-radius: 16px 0 0 16px; }}
.tl-item:nth-child(even) .tl-content.right {{ background: white; border-radius: 0 16px 16px 0; }}
</style>
</head>
<body>

<p class="intro-lead">
  对分子结构与性质的理解，建立在对原子结构不断深化的认识之上。现代电子结构理论并非一蹴而就，而是经历了两个多世纪的逐步发展与修正。
</p>

<div class="timeline">

  <!-- 0.1 道尔顿 -->
  <div class="tl-item">
    <div class="tl-content left">
      <div class="tl-year">1803</div>
      <div class="tl-title">原子概念的提出<br>道尔顿原子理论</div>
      <div class="tl-body">
        道尔顿提出了第一个具有科学基础的现代原子理论，标志着化学作为一门定量科学的正式开端。
        物质由不可再分割的微小粒子——原子构成；同一元素的原子质量和性质完全相同；
        化学反应本质上是原子之间的重新排列与组合。
        <br><br>
        该理论成功解释了<strong>质量守恒定律</strong>和<strong>定比定律</strong>，
        建立了现代化学的定量基础。
      </div>
      <div class="tag-row">
        <span class="tag contrib">✓ 建立定量化学基础</span>
        <span class="tag limit">✗ 无法解释原子内部结构</span>
      </div>
    </div>
    <div class="tl-axis">
      <div class="tl-line"></div>
      <div class="tl-node" style="background:#888"></div>
      <div class="tl-line"></div>
    </div>
    <div class="tl-content right">
      <div class="tl-img">
        <img src="{img1}" alt="道尔顿原子理论">
      </div>
    </div>
  </div>

  <!-- 0.2 汤姆孙 -->
  <div class="tl-item">
    <div class="tl-content left">
      <div class="tl-img">
        <img src="{img2}" alt="汤姆孙模型">
      </div>
    </div>
    <div class="tl-axis">
      <div class="tl-line"></div>
      <div class="tl-node" style="background:#7F77DD"></div>
      <div class="tl-line"></div>
    </div>
    <div class="tl-content right">
      <div class="tl-year">1897</div>
      <div class="tl-title">原子内部结构的初步探索<br>汤姆孙"葡萄干布丁"模型</div>
      <div class="tl-body">
        汤姆孙发现电子后提出，原子是一个带正电的均匀球体，
        带负电的电子像"葡萄干"一样镶嵌在其中，整体呈电中性。
        首次将电子引入原子结构模型，证明原子并非不可分割。
      </div>
      <div class="tag-row">
        <span class="tag contrib">✓ 首次引入电子概念</span>
        <span class="tag limit">✗ 无法解释 α 粒子散射</span>
      </div>
    </div>
  </div>

  <!-- 0.3 卢瑟福 -->
  <div class="tl-item">
    <div class="tl-content left">
      <div class="tl-year">1911</div>
      <div class="tl-title">有核原子模型的建立<br>卢瑟福模型</div>
      <div class="tl-body">
        通过金箔 α 粒子散射实验，卢瑟福发现原子的绝大部分质量和全部正电荷
        集中在一个体积极小的区域——<strong>原子核</strong>中，
        电子则在核外广阔的空间中高速运动。原子大部分空间是空的。
      </div>
      <div class="tag-row">
        <span class="tag contrib">✓ 提出原子核概念</span>
        <span class="tag limit">✗ 无法解释原子稳定性</span>
        <span class="tag limit">✗ 无法解释线状光谱</span>
      </div>
    </div>
    <div class="tl-axis">
      <div class="tl-line"></div>
      <div class="tl-node" style="background:#5DCAA5"></div>
      <div class="tl-line"></div>
    </div>
    <div class="tl-content right">
      <div class="tl-img">
        <img src="{img3}" alt="卢瑟福模型">
      </div>
    </div>
  </div>

  <!-- 0.4 玻尔 -->
  <div class="tl-item">
    <div class="tl-content left">
      <div class="tl-img">
        <img src="{img4}" alt="玻尔模型">
      </div>
    </div>
    <div class="tl-axis">
      <div class="tl-line"></div>
      <div class="tl-node" style="background:#378ADD"></div>
      <div class="tl-line"></div>
    </div>
    <div class="tl-content right">
      <div class="tl-year">1913</div>
      <div class="tl-title">量子化思想的引入<br>玻尔定态模型</div>
      <div class="tl-body">
        玻尔引入量子化思想，提出电子只能在特定能量的定态轨道上运动，
        轨道间跃迁时吸收或放出能量：
      </div>
      <div class="formula">
        \( \Delta E = h\nu \)
      </div>
      <div class="tl-body">
        成功解释了氢原子光谱的线状结构。
      </div>
      <div class="tag-row">
        <span class="tag contrib">✓ 解释氢原子光谱</span>
        <span class="tag contrib">✓ 解决原子稳定性问题</span>
        <span class="tag limit">✗ 仅适用于单电子体系</span>
      </div>
    </div>
  </div>

  <!-- 0.5 量子力学 -->
  <div class="tl-item">
    <div class="tl-content left">
      <div class="tl-year">1926 至今</div>
      <div class="tl-title">现代量子力学模型<br>与原子轨道理论</div>
      <div class="tl-body">
        薛定谔、海森堡和狄拉克等人建立了完整的量子力学框架。
        电子具有<strong>波粒二象性</strong>，其状态由波函数 \(\Psi\) 描述，
        满足定态薛定谔方程：
      </div>
      <div class="formula">
        \( \hat{{H}}\Psi = E\Psi \)
      </div>
      <div class="tl-body">
        \(|\Psi|^2\) 表示电子在空间中的概率密度。由于不确定性原理，
        经典"轨道"被概率性的<strong>原子轨道（AO）</strong>所取代。
        电子状态由四个量子数 \((n, l, m_l, m_s)\) 完整描述。
      </div>
      <div class="tag-row">
        <span class="tag contrib">✓ 彻底解决原子稳定性</span>
        <span class="tag contrib">✓ 适用于所有元素</span>
        <span class="tag contrib">✓ 为 MO、VB 理论奠基</span>
      </div>
    </div>
    <div class="tl-axis">
      <div class="tl-line"></div>
      <div class="tl-node" style="background:#534AB7"></div>
      <div class="tl-line" style="background:transparent"></div>
    </div>
    <div class="tl-content right">
      <div class="tl-img">
        <img src="{img5}" alt="量子力学模型">
      </div>
    </div>
  </div>

</div>

<!-- 结语 -->
<div class="conclusion" style="margin-top:2.5rem">
  <h3>理论意义与研究动机</h3>
  <p>
    量子力学原子模型彻底解决了原子稳定性与光谱分立性的问题，
    能够精确解释元素的电子排布与周期性规律，并成功预测不同原子轨道的空间形状和对称性。
    更重要的是，该模型为后续发展的<strong>分子轨道理论</strong>和<strong>价键理论</strong>
    奠定了严密的数学与物理基础。正是基于这一现代电子结构理论，
    我们才能理解原子如何结合形成分子，并进一步研究分子的结构、性质及其反应行为。
  </p>
</div>

</body>
</html>
"""

components.html(HTML, height=2500, scrolling=False)

page_footer("intro")
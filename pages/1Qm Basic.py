import streamlit as st
import streamlit.components.v1 as components
import base64
from utils import load_md, page_header, page_footer, divider

st.set_page_config(layout="wide", page_title="量子力学基础", page_icon="⚛️")

page_header("qm", desc="经典力学无法描述微观粒子的行为，量子力学为电子结构理论提供了最根本的物理基础。")

def img_b64(path):
    try:
        with open(path, "rb") as f:
            ext = path.split(".")[-1].lower()
            mime = "image/png" if ext == "png" else "image/jpeg"
            return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"
    except:
        return ""

img1 = img_b64("images/1.1.png")
img2 = img_b64("images/1.2.png")
img3 = img_b64("images/1.3.png")

HTML = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{
    font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB',sans-serif;
    color:#1a1a1a;background:white;padding:2rem 3rem 4rem;line-height:1.8;
}}
.lead{{
    font-size:16px;color:#555;line-height:1.9;max-width:700px;
    margin-bottom:3rem;padding-left:1.2rem;border-left:3px solid #e0e0e0;
}}
.section{{margin-bottom:3.5rem}}
.section-header{{
    display:flex;align-items:baseline;gap:12px;
    margin-bottom:1.4rem;padding-bottom:0.75rem;
    border-bottom:0.5px solid #f0f0f0;
}}
.section-num{{font-size:12px;font-weight:600;color:#7F77DD;letter-spacing:0.05em}}
.section-title{{font-size:20px;font-weight:700;letter-spacing:-0.01em;color:#1a1a1a}}
.body-text{{font-size:15px;color:#444;line-height:1.9;max-width:740px;margin-bottom:1rem}}
.body-text strong{{color:#1a1a1a;font-weight:600}}

.two-col{{display:grid;grid-template-columns:1fr 300px;gap:2rem;align-items:start}}
.two-col-rev{{display:grid;grid-template-columns:340px 1fr;gap:2rem;align-items:start}}

.img-card{{
    border-radius:14px;overflow:hidden;
    border:0.5px solid #eee;background:#fafafa;
}}
.img-card img{{width:100%;display:block}}
.img-caption{{
    font-size:11px;color:#aaa;text-align:center;
    padding:8px 12px;border-top:0.5px solid #eee;
}}

.formula-card{{
    background:#EEEDFE;border-radius:16px;
    padding:1.75rem 2rem;margin:1.25rem 0;
    border:0.5px solid #CECBF6;
}}
.formula-main{{font-size:22px;text-align:center;color:#3C3489;margin-bottom:1.2rem}}
.formula-terms{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}}
.f-term{{
    background:white;border-radius:10px;padding:0.7rem 0.75rem;
    text-align:center;border:0.5px solid #CECBF6;
}}
.f-sym{{font-size:15px;color:#534AB7;font-weight:700;margin-bottom:3px}}
.f-desc{{font-size:11px;color:#666;line-height:1.4}}

.formula-extra{{
    background:#f8f8fa;border-radius:12px;
    padding:1.2rem 1.5rem;margin:1rem 0;
    border:0.5px solid #eee;
}}
.formula-extra-label{{
    font-size:11px;color:#aaa;font-weight:600;
    letter-spacing:0.06em;text-transform:uppercase;margin-bottom:8px;
}}

.debroglie-box{{
    background:#EEEDFE;border-radius:14px;
    padding:1.2rem 1.5rem;margin:1rem 0;
    border:0.5px solid #CECBF6;
    display:grid;grid-template-columns:1fr 1fr;gap:1rem;align-items:center;
}}
.debroglie-formula{{font-size:20px;text-align:center;color:#534AB7}}
.debroglie-terms{{display:flex;flex-direction:column;gap:5px}}
.debroglie-term{{font-size:13px;color:#555;line-height:1.5}}

.standing-wave{{
    background:#fafafa;border-radius:14px;
    padding:1.2rem 1.5rem;margin:1rem 0;
    border-left:3px solid #7F77DD;
}}
.sw-title{{font-size:13px;font-weight:600;color:#534AB7;margin-bottom:8px}}
.sw-list{{list-style:none;display:flex;flex-direction:column;gap:6px}}
.sw-list li{{
    font-size:13px;color:#555;padding-left:16px;position:relative;
}}
.sw-list li::before{{
    content:'›';position:absolute;left:0;color:#7F77DD;font-weight:700;
}}

.highlight-box{{
    background:linear-gradient(135deg,#EEEDFE,#E1F5EE);
    border-radius:12px;padding:1rem 1.5rem;
    margin:1rem 0;font-size:14px;color:#3C3489;font-weight:600;
    text-align:center;
}}

.conditions{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:1.25rem 0}}
.cond-card{{border-radius:14px;padding:1.2rem 1rem;border:0.5px solid #eee;background:#fafafa}}
.cond-num{{
    width:24px;height:24px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    font-size:12px;font-weight:700;margin-bottom:8px;
}}
.cond-title{{font-size:13px;font-weight:700;color:#1a1a1a;margin-bottom:6px}}
.cond-desc{{font-size:12px;color:#555;line-height:1.65}}
.cond-intuition{{
    margin-top:8px;font-size:11px;color:#888;
    padding:6px 8px;background:white;border-radius:8px;
    border:0.5px solid #eee;line-height:1.5;
}}

.psi-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:1.25rem 0}}
.psi-card{{border-radius:14px;padding:1.2rem;border:0.5px solid #eee}}
.psi-label{{
    font-size:10px;font-weight:600;color:#aaa;
    letter-spacing:0.07em;text-transform:uppercase;margin-bottom:8px;
}}
.psi-content{{font-size:14px;color:#444;line-height:1.7}}
.psi-content strong{{color:#1a1a1a}}

.born-box{{
    background:#fafafa;border-radius:14px;
    padding:1.2rem 1.5rem;margin:1rem 0;
    border:0.5px solid #eee;
}}
.born-title{{font-size:12px;font-weight:600;color:#888;margin-bottom:10px;text-transform:uppercase;letter-spacing:0.06em}}
.born-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.born-item{{
    background:white;border-radius:10px;padding:0.75rem 1rem;
    border:0.5px solid #eee;font-size:13px;color:#555;line-height:1.6;
}}
.born-item strong{{color:#1a1a1a}}

.quote{{
    background:linear-gradient(135deg,#EEEDFE,#E1F5EE);
    border-radius:16px;padding:1.5rem 2rem;
    margin-top:2rem;font-size:16px;font-weight:600;
    color:#3C3489;line-height:1.6;text-align:center;
}}
</style>
</head>
<body>

<p class="lead">
  量子力学为现代电子结构理论提供了最根本的物理基础。
  经典力学无法正确描述微观粒子的行为，电子等微观粒子必须在量子力学框架下加以理解。
</p>

<!-- 1.1 波粒二象性 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">1.1</span>
    <span class="section-title">电子的波粒二象性</span>
  </div>

  <div class="two-col">
    <div>
      <p class="body-text">
        德布罗意（de Broglie）提出，微观粒子（如电子）不仅具有粒子性，同时也表现出波动性。
        这一观点被称为<strong>波粒二象性</strong>，是量子力学诞生的重要起点之一。
        他给出了粒子与波之间的定量关系：
      </p>

      <div class="debroglie-box">
        <div class="debroglie-formula">\( \lambda = \dfrac{{h}}{{p}} \)</div>
        <div class="debroglie-terms">
          <div class="debroglie-term">\(\lambda\) — 粒子的波长</div>
          <div class="debroglie-term">\(h\) — 普朗克常数</div>
          <div class="debroglie-term">\(p\) — 粒子的动量</div>
        </div>
      </div>

      <p class="body-text">
        该关系表明：<strong>动量越小，波长越长；动量越大，波长越短。</strong>
        对于质量极小的电子，这种波动性在原子尺度上变得尤为显著。
      </p>
      <p class="body-text">
        电子的波动性后来被 <strong>Davisson–Germer 实验</strong>所证实——
        电子束通过晶体时产生衍射图样，这种现象只能用波动理论解释，
        从而直接证明了电子具有波动性。
      </p>
    </div>
    <div>
      <div class="img-card">
        <img src="{img1}" alt="波粒二象性示意图">
        <div class="img-caption">电子的波粒二象性示意</div>
      </div>
      <canvas id="wave-canvas" width="280" height="140"
        style="width:100%;border-radius:12px;border:0.5px solid #eee;
               margin-top:10px;background:#fafafa;display:block"></canvas>
      <div style="font-size:10px;color:#bbb;text-align:center;margin-top:4px">
        驻波示意（动态）
      </div>
    </div>
  </div>

  <div class="standing-wave">
    <div class="sw-title">为什么电子能量是量子化的？</div>
    <ul class="sw-list">
      <li>经典粒子绕核运动会不断辐射能量并坠入核，量子力学用波动性解释了原子稳定性</li>
      <li>电子在原子中以<strong>驻波形式</strong>分布，就像琴弦只能振动固定的谐波一样</li>
      <li>电子波必须在绕核一周后与自身相位一致，只有满足此条件的波长才能稳定存在</li>
      <li>这直接导致允许的状态是有限的，从而产生<strong>能量量子化</strong></li>
    </ul>
  </div>
</div>

<!-- 1.2 薛定谔方程 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">1.2</span>
    <span class="section-title">薛定谔方程</span>
  </div>

  <div class="two-col-rev">
    <div class="img-card">
      <img src="{img2}" alt="薛定谔方程推导">
      <div class="img-caption">薛定谔方程的推导形式</div>
    </div>
    <div>
      <p class="body-text">
        薛定谔方程是描述微观粒子状态随时间演化的基本方程。在研究原子和分子中
        稳定存在的电子状态时，通常采用<strong>定态薛定谔方程</strong>：
      </p>
      <div class="formula-card">
        <div class="formula-main">\( \hat{{H}}\Psi = E\Psi \)</div>
        <div class="formula-terms">
          <div class="f-term">
            <div class="f-sym">\(\hat{{H}}\)</div>
            <div class="f-desc">哈密顿算符<br>体系总能量<br>（动能 + 势能）</div>
          </div>
          <div class="f-term">
            <div class="f-sym">\(\Psi\)</div>
            <div class="f-desc">波函数<br>描述粒子的<br>量子态</div>
          </div>
          <div class="f-term">
            <div class="f-sym">\(E\)</div>
            <div class="f-desc">能量本征值<br>体系在该状态<br>下的总能量</div>
          </div>
        </div>
      </div>
      <p class="body-text">
        该方程本质上是一个<strong>本征值问题</strong>：只有在特定能量 \(E\) 下，
        体系才存在可接受的波函数解。这些解共同决定了原子和分子的电子结构与性质，
        是理解化学键、光谱和材料性质的基础。
      </p>
    </div>
  </div>
</div>

<!-- 1.3 波函数的数学条件 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">1.3</span>
    <span class="section-title">波函数的数学条件</span>
  </div>
  <p class="body-text">
    薛定谔方程的解 \(\Psi\) 并非任意函数，必须同时满足以下三个数学条件，
    才能对应物理上可实现的量子态：
  </p>
  <div class="conditions">
    <div class="cond-card" style="border-color:#CECBF6">
      <div class="cond-num" style="background:#EEEDFE;color:#534AB7">①</div>
      <div class="cond-title">单值性</div>
      <div class="cond-desc">
        在空间任意一点，波函数 \(\Psi\) 只能取一个确定值，不允许出现歧义。
      </div>
      <div class="cond-intuition">
        就像温度场一样，一个点只能有一个温度值。
        若 \(\Psi\) 在某点有两个值，\(|\Psi|^2\) 所代表的概率密度就失去意义。
      </div>
    </div>
    <div class="cond-card" style="border-color:#9FE1CB">
      <div class="cond-num" style="background:#E1F5EE;color:#085041">②</div>
      <div class="cond-title">有限性</div>
      <div class="cond-desc">
        \(\Psi\) 在整个空间内必须是有限的，并在无穷远处趋近于零。
      </div>
      <div class="cond-intuition">
        若波函数在某处发散，意味着粒子在该处出现的概率无限大，这在物理上不可能。
        有限性保证了归一化条件 \(\int |\Psi|^2 d\tau = 1\) 成立。
      </div>
    </div>
    <div class="cond-card" style="border-color:#B5D4F4">
      <div class="cond-num" style="background:#E6F1FB;color:#0C447C">③</div>
      <div class="cond-title">连续性</div>
      <div class="cond-desc">
        \(\Psi\) 必须是连续函数，其一阶导数在势能不发散处也应连续。
      </div>
      <div class="cond-intuition">
        薛定谔方程是二阶微分方程，若波函数突变，导数将发散，
        导致动能项无穷大。电子云密度在空间中是平滑变化的，不会突然断裂。
      </div>
    </div>
  </div>
  <div class="born-box" style="margin-top:1.5rem">
    <div class="born-title">这些条件确保了什么？</div>
    <div class="born-grid">
      <div class="born-item"><strong>概率解释成立</strong> — \(|\Psi|^2\) 能作为有效的概率密度</div>
      <div class="born-item"><strong>体系能量有限</strong> — 避免出现无穷大能量</div>
      <div class="born-item"><strong>符合物理现实</strong> — 与实际观测一致</div>
      <div class="born-item"><strong>可归一化</strong> — 总概率等于 1 有意义</div>
    </div>
  </div>
</div>

<!-- 1.4 波函数的物理意义 -->
<div class="section">
  <div class="section-header">
    <span class="section-num">1.4</span>
    <span class="section-title">波函数的物理意义</span>
  </div>
  <div class="two-col">
    <div>
      <p class="body-text">
        波函数 \(\Psi\) 本身不具有直接的物理意义，但其平方的绝对值具有明确的统计解释——
        这一解释由 <strong>Max Born 提出</strong>，称为 <em>Born 概率诠释</em>：
      </p>
      <div class="formula-card" style="padding:1.25rem 1.5rem">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;align-items:center">
          <div style="text-align:center">
            <div style="font-size:20px;color:#534AB7">\( |\Psi|^2 \)</div>
            <div style="font-size:12px;color:#888;margin-top:4px">概率密度（单位体积内的概率）</div>
          </div>
          <div style="font-size:20px;text-align:center;color:#534AB7">
            \( P = \int_{{\tau}} |\Psi|^2 d\tau \)
          </div>
        </div>
        <div style="border-top:0.5px solid #CECBF6;margin-top:1rem;padding-top:0.75rem;
                    text-align:center;font-size:14px;color:#534AB7">
          归一化条件：\( \int |\Psi|^2 d\tau = 1 \)
        </div>
      </div>
      <p class="body-text">
        量子力学并不预测单次测量的确定结果，而是给出不同结果出现的<strong>概率</strong>。
        在原子和分子中，人们常用<strong>电子云模型</strong>来形象理解：
      </p>
      <div class="born-box">
        <div class="born-grid">
          <div class="born-item">
            \(|\Psi|^2\) <strong>大</strong>的区域<br>
            <span style="color:#534AB7">→ 电子更可能出现</span>
          </div>
          <div class="born-item">
            \(|\Psi|^2\) <strong>小</strong>的区域<br>
            <span style="color:#888">→ 电子出现概率较低</span>
          </div>
        </div>
      </div>
    </div>
    <div class="img-card">
      <img src="{img3}" alt="波函数三维图">
      <div class="img-caption">波函数 \(\Psi\) 的三维分布示意</div>
    </div>
  </div>

  <div class="quote">
    量子力学描述的不是「电子在哪里」，<br>而是「电子可能在哪里」。
  </div>
</div>

</body>
</html>

<script>
const canvas = document.getElementById('wave-canvas');
const ctx = canvas.getContext('2d');
const W = canvas.width, H = canvas.height;
let t = 0;

function drawWave() {{
  ctx.clearRect(0, 0, W, H);
  const modes = [1, 2, 3];
  const colors = ['rgba(83,74,183,0.7)', 'rgba(29,158,117,0.6)', 'rgba(212,83,126,0.5)'];
  modes.forEach((n, idx) => {{
    ctx.beginPath();
    ctx.strokeStyle = colors[idx];
    ctx.lineWidth = 1.5;
    for (let x = 0; x <= W; x++) {{
      const phase = (x / W) * Math.PI * n;
      const amp = (H/2 - 16) * (1 - idx * 0.2);
      const y = H/2 + amp * Math.sin(phase) * Math.cos(t * 0.008 + idx * 0.8);
      if (x === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }}
    ctx.stroke();
  }});
  ctx.fillStyle = 'rgba(83,74,183,0.4)';
  ctx.font = '10px monospace';
  ctx.fillText('n=1', 4, H/2 - 35);
  ctx.fillStyle = 'rgba(29,158,117,0.7)';
  ctx.fillText('n=2', 4, H/2 - 20);
  ctx.fillStyle = 'rgba(212,83,126,0.7)';
  ctx.fillText('n=3', 4, H/2 - 5);
  t++;
  requestAnimationFrame(drawWave);
}}
drawWave();
</script>
"""

components.html(HTML, height=2900, scrolling=False)

page_footer("qm")
# 把这段代码插入 4Valence_Bond.py 的 page_footer("vb") 前面
# 调用方式：直接把 RESONANCE_HTML 嵌进主 HTML 的 4.5 节里
# 或者单独用 components.html(RESONANCE_HTML, height=600, scrolling=False) 渲染

RESONANCE_HTML = """
<style>
*{box-sizing:border-box;margin:0;padding:0}
.res-wrap{padding:1rem 0;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif}
.res-tabs{display:flex;gap:8px;margin-bottom:1.25rem;flex-wrap:wrap}
.res-tab{
    padding:6px 16px;border-radius:10px;
    border:0.5px solid #e0e0e0;
    background:white;color:#666;
    font-size:13px;cursor:pointer;transition:all 0.15s;
}
.res-tab.active{background:#FAEEDA;border-color:#F0C060;color:#633806;font-weight:500}
.res-panel{display:none}.res-panel.active{display:block}
canvas{display:block;margin:0 auto;max-width:100%}
.res-caption{
    font-size:12px;color:#888;text-align:center;
    margin-top:8px;line-height:1.6;padding:0 1rem;
}
.res-controls{display:flex;justify-content:center;gap:12px;margin:10px 0}
.res-btn{
    padding:6px 16px;border-radius:10px;
    border:0.5px solid #e0e0e0;background:white;
    color:#666;font-size:13px;cursor:pointer;
}
.res-btn:hover{background:#f5f5f5}
.res-info{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:1rem}
.res-card{background:#fafafa;border-radius:10px;padding:0.75rem;text-align:center;border:0.5px solid #eee}
.res-card-label{font-size:11px;color:#aaa;margin-bottom:4px;letter-spacing:0.04em}
.res-card-val{font-size:15px;font-weight:500;color:#1a1a1a}
</style>

<div class="res-wrap">
  <div class="res-tabs">
    <div class="res-tab active" onclick="rTab('benzene',this)">苯的共振</div>
    <div class="res-tab" onclick="rTab('no3',this)">NO₃⁻ 共振</div>
    <div class="res-tab" onclick="rTab('energy',this)">共振能</div>
  </div>

  <div id="rp-benzene" class="res-panel active">
    <canvas id="rc1" width="560" height="240"></canvas>
    <div class="res-controls">
      <button class="res-btn" onclick="bToggle()">▶ 播放 / 暂停</button>
      <button class="res-btn" onclick="bReset()">重置</button>
    </div>
    <div class="res-caption">
      两个 Kekulé 共振式之间，π 电子连续离域流动，形成真实的共振杂化体。<br>
      虚线圆圈表示均匀离域的电子云，键长 139 pm（介于单键 154 pm 与双键 134 pm 之间）。
    </div>
    <div class="res-info">
      <div class="res-card"><div class="res-card-label">C–C 键长</div><div class="res-card-val">139 pm</div></div>
      <div class="res-card"><div class="res-card-label">共振能</div><div class="res-card-val">≈150 kJ/mol</div></div>
      <div class="res-card"><div class="res-card-label">键级</div><div class="res-card-val">1.5</div></div>
    </div>
  </div>

  <div id="rp-no3" class="res-panel">
    <canvas id="rc2" width="560" height="240"></canvas>
    <div class="res-controls">
      <button class="res-btn" onclick="nToggle()">▶ 播放 / 暂停</button>
      <button class="res-btn" onclick="nReset()">重置</button>
    </div>
    <div class="res-caption">
      硝酸根 NO₃⁻ 有三个等价共振式，双键在三个 N–O 键之间均匀分布。<br>
      实测三个 N–O 键长完全相等（125 pm），验证了电子离域的存在。
    </div>
    <div class="res-info">
      <div class="res-card"><div class="res-card-label">N–O 键长</div><div class="res-card-val">125 pm</div></div>
      <div class="res-card"><div class="res-card-label">键级</div><div class="res-card-val">4/3 ≈ 1.33</div></div>
      <div class="res-card"><div class="res-card-label">共振式数目</div><div class="res-card-val">3</div></div>
    </div>
  </div>

  <div id="rp-energy" class="res-panel">
    <canvas id="rc3" width="560" height="260"></canvas>
    <div class="res-caption">
      共振能 = 假想定域结构的能量 − 真实分子的能量<br>
      苯的实测氢化热（208 kJ/mol）远低于三个孤立双键的预测值（360 kJ/mol），差值约 150 kJ/mol 即共振稳定化能。
    </div>
  </div>
</div>

<script>
(function(){
const amber='#EF9F27', blue='#378ADD', red='#D85A30', green='#085041';
const HEX=[[0,-60],[52,-30],[52,30],[0,60],[-52,-30],[-52,-30]];
const HEXR=[
  [0,-60],[52,-30],[52,30],[0,60],[-52,30],[-52,-30]
];
function hpt(i,cx,cy){return [cx+HEXR[i][0],cy+HEXR[i][1]];}

// ── 苯 ──────────────────────────────────────────
const rc1=document.getElementById('rc1');
const bx=rc1.getContext('2d');
let bT=0,bPlay=true;

function drawBenzene(t){
  bx.clearRect(0,0,560,240);
  const phase=(Math.sin(t*0.035)+1)/2;
  drawKekule(bx,120,120,0,phase);
  drawHybrid(bx,280,120,t);
  drawKekule(bx,440,120,1,1-phase);

  // 双箭头
  [[195,205],[355,365]].forEach(function(seg){
    const x1=seg[0],x2=seg[1],y=120;
    bx.strokeStyle=amber;bx.lineWidth=1.5;
    bx.beginPath();bx.moveTo(x1,y);bx.lineTo(x2,y);bx.stroke();
    bx.beginPath();
    bx.moveTo(x2,y);bx.lineTo(x2-6,y-4);bx.moveTo(x2,y);bx.lineTo(x2-6,y+4);
    bx.moveTo(x1,y);bx.lineTo(x1+6,y-4);bx.moveTo(x1,y);bx.lineTo(x1+6,y+4);
    bx.stroke();
  });

  bx.fillStyle='#888';bx.font='11px sans-serif';bx.textAlign='center';
  bx.fillText('Kekulé 式 I',120,205);
  bx.fillText('共振杂化体',280,205);
  bx.fillText('Kekulé 式 II',440,205);
}

function drawKekule(ctx,cx,cy,mode,alpha){
  ctx.strokeStyle='#333';ctx.lineWidth=2;
  for(var i=0;i<6;i++){
    var a=hpt(i,cx,cy),b=hpt((i+1)%6,cx,cy);
    ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);ctx.stroke();
  }
  var doubles=mode===0?[0,2,4]:[1,3,5];
  ctx.strokeStyle=blue;ctx.lineWidth=2.5;ctx.globalAlpha=0.35+alpha*0.65;
  doubles.forEach(function(i){
    var a=hpt(i,cx,cy),b=hpt((i+1)%6,cx,cy);
    var dx=b[1]-a[1],dy=-(b[0]-a[0]);
    var len=Math.sqrt(dx*dx+dy*dy);
    var px=dx/len*7,py=dy/len*7;
    ctx.beginPath();ctx.moveTo(a[0]+px,a[1]+py);ctx.lineTo(b[0]+px,b[1]+py);ctx.stroke();
  });
  ctx.globalAlpha=1;
}

function drawHybrid(ctx,cx,cy,t){
  ctx.strokeStyle='#333';ctx.lineWidth=2;
  for(var i=0;i<6;i++){
    var a=hpt(i,cx,cy),b=hpt((i+1)%6,cx,cy);
    ctx.beginPath();ctx.moveTo(a[0],a[1]);ctx.lineTo(b[0],b[1]);ctx.stroke();
  }
  for(var i=0;i<72;i++){
    var angle=(i/72)*Math.PI*2+t*0.04;
    var nx=cx+36*Math.cos(angle),ny=cy+36*Math.sin(angle);
    var a=Math.abs(Math.sin(angle*3+t*0.08));
    ctx.beginPath();ctx.arc(nx,ny,3,0,Math.PI*2);
    ctx.fillStyle='rgba(55,138,221,'+(0.25+a*0.55)+')';
    ctx.fill();
  }
  ctx.strokeStyle=amber;ctx.lineWidth=1.5;ctx.setLineDash([4,3]);
  ctx.beginPath();ctx.arc(cx,cy,36,0,Math.PI*2);ctx.stroke();
  ctx.setLineDash([]);
}

function bTick(){bPlay&&(bT++,drawBenzene(bT));requestAnimationFrame(bTick);}
window.bToggle=function(){bPlay=!bPlay;};
window.bReset=function(){bT=0;bPlay=true;};
bTick();

// ── NO3- ────────────────────────────────────────
const rc2=document.getElementById('rc2');
const nx2=rc2.getContext('2d');
let nT=0,nPlay=true;
var Nxy=[280,110];
var Oxyz=[[280,200],[196,58],[364,58]];

function drawNO3(t){
  nx2.clearRect(0,0,560,240);
  var step=Math.floor(t/90)%3;
  var prog=(t%90)/90;

  nx2.font='500 15px sans-serif';nx2.textAlign='center';

  for(var i=0;i<3;i++){
    var isDbl=(i===step);
    var O=Oxyz[i],N=Nxy;
    var dx=O[0]-N[0],dy=O[1]-N[1],len=Math.sqrt(dx*dx+dy*dy);
    var ux=dx/len,uy=dy/len;

    nx2.lineWidth=isDbl?3:1.8;
    nx2.strokeStyle=isDbl?blue:'#bbb';
    nx2.beginPath();nx2.moveTo(N[0],N[1]);nx2.lineTo(O[0],O[1]);nx2.stroke();

    if(isDbl){
      var px=-uy*7,py=ux*7;
      nx2.lineWidth=2;nx2.strokeStyle=blue;nx2.globalAlpha=0.5;
      nx2.beginPath();nx2.moveTo(N[0]+px,N[1]+py);nx2.lineTo(O[0]+px,O[1]+py);nx2.stroke();
      nx2.globalAlpha=1;

      var ex=N[0]+dx*prog,ey=N[1]+dy*prog;
      nx2.beginPath();nx2.arc(ex,ey,5,0,Math.PI*2);
      nx2.fillStyle=amber;nx2.fill();
    }

    nx2.fillStyle='#1a1a1a';
    nx2.fillText('O',O[0],O[1]+5);
    if(!isDbl){
      nx2.fillStyle=red;nx2.font='11px sans-serif';
      nx2.fillText('−',O[0]+14,O[1]-7);
      nx2.font='500 15px sans-serif';
    }
  }

  nx2.fillStyle='#1a1a1a';nx2.fillText('N',Nxy[0],Nxy[1]+5);
  nx2.fillStyle=red;nx2.font='11px sans-serif';
  nx2.fillText('+',Nxy[0]+12,Nxy[1]-7);

  var labels=['共振式 I','共振式 II','共振式 III'];
  nx2.fillStyle='#aaa';nx2.font='12px sans-serif';nx2.textAlign='center';
  nx2.fillText('当前: '+labels[step],280,232);
}

function nTick(){nPlay&&(nT++,drawNO3(nT));requestAnimationFrame(nTick);}
window.nToggle=function(){nPlay=!nPlay;};
window.nReset=function(){nT=0;nPlay=true;};
nTick();

// ── 共振能 ──────────────────────────────────────
function drawEnergy(){
  var c=document.getElementById('rc3'),ctx=c.getContext('2d');
  ctx.clearRect(0,0,560,260);
  var yRef=55,yReal=185;

  ctx.strokeStyle='#e0e0e0';ctx.lineWidth=1;
  ctx.setLineDash([4,3]);
  ctx.beginPath();ctx.moveTo(60,yRef);ctx.lineTo(500,yRef);ctx.stroke();
  ctx.setLineDash([]);

  ctx.fillStyle=red;ctx.globalAlpha=0.1;
  ctx.fillRect(190,yRef,80,yReal-yRef);
  ctx.globalAlpha=1;

  ctx.strokeStyle=red;ctx.lineWidth=2.5;
  ctx.beginPath();ctx.moveTo(90,yRef);ctx.lineTo(270,yRef);ctx.stroke();
  ctx.strokeStyle=green;ctx.lineWidth=2.5;
  ctx.beginPath();ctx.moveTo(290,yReal);ctx.lineTo(470,yReal);ctx.stroke();

  var mh=7;
  ctx.strokeStyle=amber;ctx.lineWidth=1.8;
  ctx.beginPath();ctx.moveTo(230,yRef+4);ctx.lineTo(230,yReal-4);ctx.stroke();
  ctx.fillStyle=amber;
  ctx.beginPath();ctx.moveTo(230,yRef+3);ctx.lineTo(230-mh/2,yRef+3+mh);ctx.lineTo(230+mh/2,yRef+3+mh);ctx.closePath();ctx.fill();
  ctx.beginPath();ctx.moveTo(230,yReal-3);ctx.lineTo(230-mh/2,yReal-3-mh);ctx.lineTo(230+mh/2,yReal-3-mh);ctx.closePath();ctx.fill();

  ctx.font='500 13px sans-serif';ctx.textAlign='left';
  ctx.fillStyle=red;
  ctx.fillText('假想 Kekulé 结构  360 kJ/mol',280,yRef+5);
  ctx.fillStyle=green;
  ctx.fillText('真实苯分子  208 kJ/mol',280,yReal+5);
  ctx.fillStyle=amber;
  ctx.fillText('共振能',246,(yRef+yReal)/2-8);
  ctx.fillText('≈ 150 kJ/mol',238,(yRef+yReal)/2+8);

  ctx.strokeStyle='#ccc';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(60,25);ctx.lineTo(60,240);ctx.stroke();
  ctx.beginPath();ctx.moveTo(55,30);ctx.lineTo(60,23);ctx.lineTo(65,30);ctx.closePath();ctx.fillStyle='#ccc';ctx.fill();
  ctx.fillStyle='#aaa';ctx.font='11px sans-serif';ctx.textAlign='center';
  ctx.fillText('能量 E',60,252);
  ctx.textAlign='left';
  ctx.fillStyle='#aaa';ctx.font='11px sans-serif';
  ctx.fillText('能量较高（不稳定）',90,yRef-8);
  ctx.fillText('能量较低（更稳定）',300,yReal+22);
}

window.rTab=function(id,el){
  document.querySelectorAll('.res-tab').forEach(function(t){t.classList.remove('active');});
  document.querySelectorAll('.res-panel').forEach(function(p){p.classList.remove('active');});
  el.classList.add('active');
  document.getElementById('rp-'+id).classList.add('active');
  if(id==='energy') setTimeout(drawEnergy,50);
};
setTimeout(drawEnergy,100);
})();
</script>
"""

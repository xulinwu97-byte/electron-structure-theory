LFT_WIDGET_HTML = r"""
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif}
.lft-tabs{display:flex;gap:8px;margin-bottom:1.25rem;flex-wrap:wrap}
.lft-tab{padding:6px 16px;border-radius:10px;border:0.5px solid #e0e0e0;
  background:white;color:#666;font-size:13px;cursor:pointer;transition:all 0.15s}
.lft-tab.active{background:#FBEAF0;border-color:#F4C0D1;color:#72243E;font-weight:500}
.lft-panel{display:none}.lft-panel.active{display:block}
canvas{display:block}
.lft-caption{font-size:12px;color:#888;text-align:center;
  margin-top:8px;line-height:1.6;padding:0 0.5rem}
.lft-ctrl{display:flex;justify-content:center;gap:10px;margin:10px 0;flex-wrap:wrap}
.lft-btn{padding:6px 16px;border-radius:10px;border:0.5px solid #e0e0e0;
  background:white;color:#666;font-size:13px;cursor:pointer}
.lft-btn:hover{background:#f5f5f5}
.lft-btn.lft-active{background:#FBEAF0;border-color:#F4C0D1;color:#72243E}
.lft-info{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:1rem}
.lft-ic{background:#fafafa;border-radius:10px;padding:0.75rem;text-align:center;border:0.5px solid #eee}
.lft-ic-label{font-size:11px;color:#aaa;margin-bottom:4px}
.lft-ic-val{font-size:15px;font-weight:500;color:#1a1a1a}
</style>

<div style="padding:1rem">
<div class="lft-tabs">
  <div class="lft-tab active" onclick="lftTab('bb',this)">① π 反馈键合</div>
  <div class="lft-tab" onclick="lftTab('pd',this)">② CFT 悖论</div>
  <div class="lft-tab" onclick="lftTab('sp',this)">③ 光谱化学序列</div>
</div>

<div id="lft-bb" class="lft-panel active">
  <canvas id="lft-c-bb" width="620" height="290"
    style="width:100%;border-radius:12px;border:0.5px solid #eee"></canvas>
  <div class="lft-ctrl">
    <button class="lft-btn lft-active" id="lft-bb-donor" onclick="lftBBMode('donor',this)">π 供体（Cl⁻）</button>
    <button class="lft-btn" id="lft-bb-none" onclick="lftBBMode('none',this)">纯 σ 供体（NH₃）</button>
    <button class="lft-btn" id="lft-bb-acceptor" onclick="lftBBMode('acceptor',this)">π 受体（CO）</button>
  </div>
  <div class="lft-info">
    <div class="lft-ic"><div class="lft-ic-label">配体类型</div><div class="lft-ic-val" id="lft-bb-type">π 供体</div></div>
    <div class="lft-ic"><div class="lft-ic-label">t₂g 能级</div><div class="lft-ic-val" id="lft-bb-t2g">↑ 升高</div></div>
    <div class="lft-ic"><div class="lft-ic-label">Δo 变化</div><div class="lft-ic-val" id="lft-bb-delta">↓ 减小</div></div>
  </div>
  <div class="lft-caption">
    动画展示 π 键合如何影响 t₂g 能级：π 供体推高 t₂g（Δo 减小），π 受体拉低 t₂g（Δo 增大）。
  </div>
</div>

<div id="lft-pd" class="lft-panel">
  <canvas id="lft-c-pd" width="620" height="290"
    style="width:100%;border-radius:12px;border:0.5px solid #eee"></canvas>
  <div class="lft-ctrl" id="lft-pd-btns"></div>
  <div class="lft-caption">
    点击配体查看 CFT 静电预测值（灰色虚线）与实验测量值（彩色实线）的差异。<br>
    CFT 预测"电荷越高 Δ 越大"，但实验结果完全相反。
  </div>
</div>

<div id="lft-sp" class="lft-panel">
  <canvas id="lft-c-sp" width="620" height="290"
    style="width:100%;border-radius:12px;border:0.5px solid #eee"></canvas>
  <div class="lft-caption">
    点击配体，查看其 π 相互作用类型及 t₂g / eg* 能级的变化方式。
  </div>
</div>
</div>

<script>
(function(){
const amber='#EF9F27', red='#D85A30', green='#1D9E75', blue='#185FA5';

// ── ① π 反馈键合 ────────────────────────────────────
const bb=document.getElementById('lft-c-bb');
const bx=bb.getContext('2d');
let bbMode='donor',bbT=0,bbCur=0,bbTgt=0;
const BB={
  donor:   {label:'π 供体（Cl⁻）', shift:+24,col:red,  type:'π 供体',   t2g:'↑ 升高', dlt:'↓ 减小'},
  none:    {label:'纯 σ 供体（NH₃）',shift:0, col:blue, type:'纯 σ 供体', t2g:'— 不变', dlt:'— 基准'},
  acceptor:{label:'π 受体（CO）',  shift:-30,col:green,type:'π 受体',   t2g:'↓ 降低', dlt:'↑ 增大'},
};
window.lftBBMode=function(m,el){
  document.querySelectorAll('[id^=lft-bb-]').forEach(b=>b.classList.remove('lft-active'));
  el.classList.add('lft-active');
  bbMode=m; bbTgt=BB[m].shift;
  document.getElementById('lft-bb-type').textContent=BB[m].type;
  document.getElementById('lft-bb-t2g').textContent=BB[m].t2g;
  document.getElementById('lft-bb-delta').textContent=BB[m].dlt;
};
function drawBB(){
  const W=bb.width,H=bb.height;
  bx.clearRect(0,0,W,H);
  bbCur+=(bbTgt-bbCur)*0.06;
  const cfg=BB[bbMode], cx=W/2, eg_y=75, base=190, t2g_y=base-bbCur;
  bx.fillStyle='rgba(0,0,0,0.08)'; bx.font='10px sans-serif'; bx.textAlign='center';
  bx.fillText('金属轨道',80,18); bx.fillText('分子轨道（MO）',cx,18); bx.fillText('配体轨道',W-80,18);
  [[cx-75,cx-15],[cx+15,cx+75]].forEach(([a,b2])=>{
    bx.strokeStyle=red; bx.lineWidth=2.5;
    bx.beginPath(); bx.moveTo(a,eg_y); bx.lineTo(b2,eg_y); bx.stroke();
  });
  bx.fillStyle=red; bx.font='11px sans-serif'; bx.textAlign='left';
  bx.fillText('eg* (σ反键)',cx+80,eg_y+4);
  [[cx-75,cx-20],[cx,cx+30],[cx+45,cx+75]].forEach(([a,b2])=>{
    bx.strokeStyle=cfg.col; bx.lineWidth=2.5;
    bx.beginPath(); bx.moveTo(a,t2g_y); bx.lineTo(b2,t2g_y); bx.stroke();
  });
  bx.fillStyle=cfg.col; bx.font='500 11px sans-serif'; bx.textAlign='left';
  bx.fillText('t₂g',cx+80,t2g_y+4);
  bx.strokeStyle='#aaa'; bx.lineWidth=1.5; bx.setLineDash([4,3]);
  bx.beginPath(); bx.moveTo(30,base); bx.lineTo(120,base); bx.stroke();
  bx.setLineDash([]);
  bx.fillStyle='#aaa'; bx.font='10px sans-serif'; bx.textAlign='center';
  bx.fillText('t₂g 基准',75,base+14);
  bx.strokeStyle=amber; bx.lineWidth=1.5;
  bx.beginPath(); bx.moveTo(cx-90,eg_y+2); bx.lineTo(cx-90,t2g_y-2); bx.stroke();
  const mh=6; bx.fillStyle=amber;
  [[cx-90,eg_y+2,1],[cx-90,t2g_y-2,-1]].forEach(([x,y,d])=>{
    bx.beginPath(); bx.moveTo(x,y); bx.lineTo(x-mh/2,y+d*mh); bx.lineTo(x+mh/2,y+d*mh); bx.closePath(); bx.fill();
  });
  bx.fillStyle=amber; bx.font='500 12px sans-serif'; bx.textAlign='right';
  bx.fillText('Δo',cx-95,(eg_y+t2g_y)/2+4);
  if(bbMode==='donor'){
    bx.strokeStyle=red; bx.lineWidth=2;
    bx.beginPath(); bx.moveTo(W-120,230); bx.lineTo(W-30,230); bx.stroke();
    bx.fillStyle=red; bx.font='10px sans-serif'; bx.textAlign='center';
    bx.fillText('π 满占轨道',W-75,244);
    const ep=((bbT*0.025)%1);
    const ex=(W-120)+ep*(cx+75-(W-120)), ey=230+ep*(t2g_y-230);
    bx.beginPath(); bx.arc(ex,ey,5,0,Math.PI*2);
    bx.fillStyle='rgba(216,90,48,0.75)'; bx.fill();
    bx.strokeStyle=red; bx.lineWidth=1.5;
    bx.beginPath(); bx.moveTo(cx+85,t2g_y+4); bx.lineTo(cx+85,base-4); bx.stroke();
    bx.fillStyle=red; bx.font='10px sans-serif'; bx.textAlign='center';
    bx.fillText('推高',cx+85,t2g_y-8);
  } else if(bbMode==='acceptor'){
    bx.strokeStyle=green; bx.lineWidth=2; bx.setLineDash([4,3]);
    bx.beginPath(); bx.moveTo(W-120,78); bx.lineTo(W-30,78); bx.stroke();
    bx.setLineDash([]);
    bx.fillStyle=green; bx.font='10px sans-serif'; bx.textAlign='center';
    bx.fillText('π* 空轨道',W-75,68);
    const ep2=((bbT*0.02)%1);
    const ex2=cx+ep2*((W-120)-cx), ey2=t2g_y+ep2*(78-t2g_y);
    bx.beginPath(); bx.arc(ex2,ey2,5,0,Math.PI*2);
    bx.fillStyle='rgba(29,158,117,0.75)'; bx.fill();
    bx.strokeStyle=green; bx.lineWidth=1.5;
    bx.beginPath(); bx.moveTo(cx+85,base-4); bx.lineTo(cx+85,t2g_y+4); bx.stroke();
    bx.fillStyle=green; bx.font='10px sans-serif'; bx.textAlign='center';
    bx.fillText('拉低',cx+85,t2g_y+18);
    bx.fillStyle='rgba(29,158,117,0.6)'; bx.font='9px sans-serif';
    bx.fillText('↑ back-bonding',W-75,56);
  } else {
    bx.strokeStyle='#bbb'; bx.lineWidth=1.5;
    bx.beginPath(); bx.moveTo(W-120,155); bx.lineTo(W-30,155); bx.stroke();
    bx.fillStyle='#bbb'; bx.font='10px sans-serif'; bx.textAlign='center';
    bx.fillText('σ 轨道（无π）',W-75,170);
  }
  bx.fillStyle='rgba(0,0,0,0.3)'; bx.font='500 12px sans-serif'; bx.textAlign='center';
  bx.fillText(cfg.label,cx,H-8);
  bbT++;
  requestAnimationFrame(drawBB);
}
drawBB();

// ── ② CFT 悖论 ──────────────────────────────────────
const pd=document.getElementById('lft-c-pd');
const px=pd.getContext('2d');
const LPDS=[
  {name:'I⁻',  charge:-1,exp:0.90,cft:2.8,col:'#534AB7'},
  {name:'Br⁻', charge:-1,exp:1.05,cft:2.6,col:'#7F77DD'},
  {name:'Cl⁻', charge:-1,exp:1.20,cft:2.4,col:'#185FA5'},
  {name:'F⁻',  charge:-1,exp:1.40,cft:2.2,col:'#378ADD'},
  {name:'OH⁻', charge:-1,exp:1.55,cft:2.0,col:'#5DCAA5'},
  {name:'H₂O', charge:0, exp:1.80,cft:1.5,col:'#1D9E75'},
  {name:'NH₃', charge:0, exp:2.20,cft:1.3,col:'#EF9F27'},
  {name:'CN⁻', charge:-1,exp:3.20,cft:2.5,col:'#D85A30'},
  {name:'CO',  charge:0, exp:3.50,cft:1.2,col:'#A32D2D'},
];
let pdSel=null;
const pdBtns2=document.getElementById('lft-pd-btns');
LPDS.forEach((l,i)=>{
  const b=document.createElement('button');
  b.className='lft-btn'; b.textContent=l.name;
  b.style.borderColor=l.col;
  b.onclick=()=>{pdSel=i;drawPD();};
  pdBtns2.appendChild(b);
});
function drawPD(){
  const W=pd.width,H=pd.height,n=LPDS.length;
  px.clearRect(0,0,W,H);
  const maxV=4,bW=44,gap=16,sx0=30;
  px.strokeStyle='#f0f0f0'; px.lineWidth=1;
  for(let v=0;v<=4;v++){
    const y=H-50-((v/maxV)*(H-80));
    px.beginPath(); px.moveTo(28,y); px.lineTo(W-8,y); px.stroke();
    px.fillStyle='#aaa'; px.font='10px sans-serif'; px.textAlign='right';
    px.fillText(v.toFixed(1),26,y+4);
  }
  px.fillStyle='#888'; px.font='11px sans-serif'; px.textAlign='left';
  px.fillText('Δo (eV)',6,18);
  LPDS.forEach((l,i)=>{
    const x=sx0+i*(bW+gap);
    const isSel=pdSel===i, alpha=pdSel===null||isSel?1:0.3;
    const expH=(l.exp/maxV)*(H-80), cftH=(l.cft/maxV)*(H-80);
    px.globalAlpha=alpha*0.55;
    px.strokeStyle='#bbb'; px.lineWidth=1.5; px.setLineDash([4,3]);
    const cy=H-50-cftH;
    px.beginPath(); px.moveTo(x+bW/2,H-50); px.lineTo(x+bW/2,cy); px.stroke();
    px.setLineDash([]);
    px.beginPath(); px.moveTo(x,cy); px.lineTo(x+bW,cy); px.stroke();
    px.globalAlpha=alpha;
    px.fillStyle=l.col;
    px.fillRect(x,H-50-expH,bW,expH);
    if(isSel){
      const diff=l.cft-l.exp, midY=(cy+(H-50-expH))/2;
      px.strokeStyle=amber; px.lineWidth=1.5;
      px.beginPath(); px.moveTo(x+bW+6,cy); px.lineTo(x+bW+6,H-50-expH); px.stroke();
      px.fillStyle=amber; px.font='500 10px sans-serif'; px.textAlign='left';
      px.fillText(diff>0?`CFT高估${diff.toFixed(2)}eV`:`CFT低估${Math.abs(diff).toFixed(2)}eV`,x+bW+10,midY+4);
    }
    px.globalAlpha=1;
    px.fillStyle=isSel?l.col:'#666';
    px.font=isSel?'500 11px sans-serif':'10px sans-serif';
    px.textAlign='center';
    px.fillText(l.name,x+bW/2,H-34);
    px.fillStyle='#aaa'; px.font='9px sans-serif';
    px.fillText(l.charge===0?'中性':'阴离子',x+bW/2,H-22);
  });
  px.globalAlpha=1;
  px.strokeStyle='#bbb'; px.lineWidth=1.5; px.setLineDash([4,3]);
  px.beginPath(); px.moveTo(W-135,15); px.lineTo(W-115,15); px.stroke(); px.setLineDash([]);
  px.fillStyle='#888'; px.font='10px sans-serif'; px.textAlign='left';
  px.fillText('CFT 静电预测',W-110,19);
  px.fillStyle=red; px.fillRect(W-135,27,18,10);
  px.fillStyle='#888'; px.fillText('实验测量值',W-110,37);
  if(pdSel===null){
    px.fillStyle='#bbb'; px.font='12px sans-serif'; px.textAlign='center';
    px.fillText('← 点击配体查看差异 →',W/2,H-8);
  }
}
drawPD();

// ── ③ 光谱化学序列 ──────────────────────────────────
const sp2=document.getElementById('lft-c-sp');
const sx2=sp2.getContext('2d');
const SPEC=[
  {name:'I⁻', type:'donor',   delta:0.90,desc:'强 π 供体\n满占 p 轨道推高 t₂g\nΔo 最小'},
  {name:'Br⁻',type:'donor',   delta:1.05,desc:'强 π 供体\n满占 p 轨道推高 t₂g'},
  {name:'Cl⁻',type:'donor',   delta:1.20,desc:'π 供体\n推高 t₂g，减小 Δo'},
  {name:'F⁻', type:'wdonor',  delta:1.40,desc:'弱 π 供体\n推高 t₂g（程度较弱）'},
  {name:'OH⁻',type:'wdonor',  delta:1.55,desc:'弱 π 供体\n孤对电子 π 作用'},
  {name:'H₂O',type:'sigma',   delta:1.80,desc:'纯 σ 供体\n无 π 作用，基准 Δo'},
  {name:'NH₃',type:'sigma',   delta:2.20,desc:'纯 σ 供体\n无 π 轨道，Δo 中等'},
  {name:'en', type:'sigma',   delta:2.40,desc:'螯合纯 σ 供体\n螯合效应略增强'},
  {name:'CN⁻',type:'acceptor',delta:3.20,desc:'强 π 受体\nπ* 轨道拉低 t₂g\nΔo 大'},
  {name:'CO', type:'acceptor',delta:3.50,desc:'最强 π 受体\nback-bonding 极强\nΔo 最大'},
];
const TC={donor:red,wdonor:amber,sigma:'#888',acceptor:green};
const TL={donor:'π 供体（弱场）',wdonor:'弱 π 供体',sigma:'纯 σ 供体',acceptor:'π 受体（强场）'};
let spSel=null,spHov=-1;
sp2.addEventListener('mousemove',e=>{
  const r=sp2.getBoundingClientRect(),mx=(e.clientX-r.left)*(sp2.width/r.width),my=(e.clientY-r.top)*(sp2.height/r.height);
  const step=(sp2.width-80)/(SPEC.length-1),dotY=155,rv=16;
  let f=-1;
  SPEC.forEach((_,i)=>{const x=40+i*step;if(Math.abs(mx-x)<rv+4&&Math.abs(my-dotY)<rv+4)f=i;});
  if(f!==spHov){spHov=f;drawSP();}
});
sp2.addEventListener('click',e=>{
  const r=sp2.getBoundingClientRect(),mx=(e.clientX-r.left)*(sp2.width/r.width),my=(e.clientY-r.top)*(sp2.height/r.height);
  const step=(sp2.width-80)/(SPEC.length-1),dotY=155,rv=16;
  let f=-1;
  SPEC.forEach((_,i)=>{const x=40+i*step;if(Math.abs(mx-x)<rv+4&&Math.abs(my-dotY)<rv+4)f=i;});
  spSel=(f===spSel)?null:f; drawSP();
});
function drawSP(){
  const W=sp2.width,H=sp2.height,n=SPEC.length,step=(W-80)/(n-1),dotY=155,rv=14;
  sx2.clearRect(0,0,W,H);
  const g=sx2.createLinearGradient(40,0,W-40,0);
  g.addColorStop(0,'rgba(216,90,48,0.07)'); g.addColorStop(0.5,'rgba(136,135,128,0.04)'); g.addColorStop(1,'rgba(29,158,117,0.07)');
  sx2.fillStyle=g; sx2.beginPath(); sx2.roundRect(40,dotY-rv-4,W-80,rv*2+8,8); sx2.fill();
  const ag=sx2.createLinearGradient(40,0,W-40,0);
  ag.addColorStop(0,TC.donor); ag.addColorStop(0.5,TC.sigma); ag.addColorStop(1,TC.acceptor);
  sx2.strokeStyle=ag; sx2.lineWidth=3;
  sx2.beginPath(); sx2.moveTo(40,dotY); sx2.lineTo(W-40,dotY); sx2.stroke();
  sx2.fillStyle=TC.donor; sx2.font='11px sans-serif'; sx2.textAlign='left'; sx2.fillText('← 弱场 / 高自旋',44,H-8);
  sx2.fillStyle=TC.acceptor; sx2.textAlign='right'; sx2.fillText('强场 / 低自旋 →',W-44,H-8);
  sx2.fillStyle='#bbb'; sx2.font='10px sans-serif'; sx2.textAlign='center'; sx2.fillText('Δo 依次增大 →',W/2,dotY-26);
  SPEC.forEach((l,i)=>{
    const x=40+i*step,col=TC[l.type],isSel=spSel===i,isHov=spHov===i;
    const sc=isSel?1.3:isHov?1.15:1,cr=rv*sc;
    sx2.beginPath(); sx2.arc(x,dotY,cr,0,Math.PI*2);
    sx2.fillStyle=isSel||isHov?col:col+'88'; sx2.fill();
    if(isSel){sx2.strokeStyle=col;sx2.lineWidth=2;sx2.stroke();}
    sx2.fillStyle=isSel?col:'#666'; sx2.font=isSel?'500 11px sans-serif':'10px sans-serif'; sx2.textAlign='center';
    sx2.fillText(l.name,x,dotY+rv+14);
    sx2.fillStyle='#aaa'; sx2.font='9px sans-serif'; sx2.fillText(l.delta.toFixed(2),x,dotY+rv+26);
  });
  if(spSel!==null){
    const l=SPEC[spSel],x=40+spSel*step,col=TC[l.type];
    const cW=185,cH=112;
    let cx2=x-cW/2; cx2=Math.max(6,Math.min(W-cW-6,cx2));
    const cy2=spSel<5?dotY+rv+38:dotY-rv-42-cH;
    sx2.fillStyle='white'; sx2.strokeStyle=col; sx2.lineWidth=1.5;
    sx2.beginPath(); sx2.roundRect(cx2,cy2,cW,cH,10); sx2.fill(); sx2.stroke();
    sx2.fillStyle=col; sx2.font='500 12px sans-serif'; sx2.textAlign='left';
    sx2.fillText(l.name+' — '+TL[l.type],cx2+8,cy2+18);
    sx2.fillStyle='#555'; sx2.font='11px sans-serif';
    l.desc.split('\n').forEach((ln,li)=>sx2.fillText(ln,cx2+8,cy2+36+li*16));
    const ey2=cy2+cH-25,t2b=ey2,eg2=ey2-38;
    const ts=l.type==='donor'?12:l.type==='acceptor'?-14:0,ty=t2b+ts;
    sx2.strokeStyle='#ddd'; sx2.lineWidth=1.5;
    sx2.beginPath(); sx2.moveTo(cx2+cW-58,t2b); sx2.lineTo(cx2+cW-10,t2b); sx2.stroke();
    sx2.strokeStyle=col; sx2.lineWidth=2;
    sx2.beginPath(); sx2.moveTo(cx2+cW-58,ty); sx2.lineTo(cx2+cW-10,ty); sx2.stroke();
    sx2.strokeStyle=red; sx2.lineWidth=1.5;
    sx2.beginPath(); sx2.moveTo(cx2+cW-58,eg2); sx2.lineTo(cx2+cW-10,eg2); sx2.stroke();
    sx2.fillStyle=red; sx2.font='9px sans-serif'; sx2.textAlign='right'; sx2.fillText('eg*',cx2+cW-6,eg2+3);
    sx2.fillStyle=col; sx2.fillText('t₂g',cx2+cW-6,ty+3);
  }
}
drawSP();

window.lftTab=function(id,el){
  document.querySelectorAll('.lft-tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.lft-panel').forEach(p=>p.classList.remove('active'));
  el.classList.add('active');
  document.getElementById('lft-'+id).classList.add('active');
};
})();
</script>
"""

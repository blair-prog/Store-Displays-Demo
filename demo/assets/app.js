
(function(){
'use strict';
var money=function(n){return '$'+Math.round(n).toLocaleString('en-US');};
/* Gondola builder (SAMPLE pricing, concept only). Option lists mirror the live Gondola Shelving page. */
var b=document.querySelector('[data-builder]');
if(b){
  var steps=[
    {k:'store',l:'Store type',q:'What kind of store is it?',o:[['Supermarket','Long runs'],['Liquor store','Heavy loads'],['Pharmacy','Mixed goods'],['Apparel store','Light merchandise'],['Other','Tell us more']]},
    {k:'unit',l:'Unit type',q:'Which unit type?',o:[['Single sided','Against a wall',1],['Double sided','Freestanding aisle',1.7],['Wall unit','Wall run',0.9],['End unit','Ends a run',1.1]]},
    {k:'len',l:'Length',q:'How long is each section?',o:[['30 in','Compact',0.9],['36 in','Standard',1],['48 in','Wide',1.3]]},
    {k:'h',l:'Height',q:'How tall?',o:[['48 in','',1],['54 in','',1.05],['60 in','',1.12],['72 in','Most popular',1.3],['84 in','',1.5],['96 in','Max display',1.7]]},
    {k:'fin',l:'Finish',q:'Choose a finish',o:[['Black','Powder coat'],['Antique white','Powder coat']]},
    {k:'secs',l:'Sections',q:'How many sections?',o:[['2 sections','',2],['4 sections','',4],['6 sections','',6],['8 sections','',8]]},
    {k:'acc',l:'Add-ons',q:'Add anything?',multi:true,o:[['Upper shelves','$25 per section',25],['End units','$236 for a pair',236],['Accessories','$12 per section',12]]}
  ];
  var st={},i=0,qs=function(s){return b.querySelector(s)};
  var stepsEl=qs('[data-steps]'),q=qs('[data-q]'),opts=qs('[data-opts]'),sum=qs('[data-sum]'),total=qs('[data-total]');
  function calc(){
    var secs=(st.secs&&st.secs[2])||0,u=(st.unit&&st.unit[2])||1,l=(st.len&&st.len[2])||1,h=(st.h&&st.h[2])||1;
    var t=secs*107*u*l*h;
    (st.acc||[]).forEach(function(a){t+=a[0]==='End units'?a[2]:a[2]*secs});
    return t;
  }
  function render(){
    stepsEl.innerHTML='';
    steps.forEach(function(s,n){var x=document.createElement('button');x.type='button';x.textContent=(n+1)+'. '+s.l;
      x.className=(n===i?'on ':'')+(st[s.k]&&(!s.multi||st[s.k].length)?'done':'');x.onclick=function(){i=n;render()};stepsEl.appendChild(x)});
    var s=steps[i];q.textContent=s.q;opts.innerHTML='';
    s.o.forEach(function(o){var x=document.createElement('button');x.type='button';x.innerHTML=o[0]+(o[1]?'<small>'+o[1]+'</small>':'');
      var cur=st[s.k];var sel=s.multi?(cur||[]).some(function(c){return c[0]===o[0]}):(cur&&cur[0]===o[0]);if(sel)x.className='sel';
      x.onclick=function(){if(s.multi){var a=st[s.k]||[];var ix=a.findIndex(function(c){return c[0]===o[0]});if(ix>-1)a.splice(ix,1);else a.push(o);st[s.k]=a}else{st[s.k]=o}render()};opts.appendChild(x)});
    sum.innerHTML='';
    steps.forEach(function(s){var v=st[s.k];if(!v||(s.multi&&!v.length))return;var li=document.createElement('li');li.innerHTML='<span>'+s.l+'</span><strong>'+(s.multi?v.map(function(c){return c[0]}).join(', '):v[0])+'</strong>';sum.appendChild(li)});
    total.textContent=money(calc());
    qs('[data-back]').disabled=i===0;qs('[data-next]').textContent=i===steps.length-1?'Finish':'Next';
  }
  qs('[data-back]').onclick=function(){if(i>0){i--;render()}};
  qs('[data-next]').onclick=function(){if(i<steps.length-1){i++;render()}else{qs('[data-cta]').focus()}};
  render();
}

/* Collection filters and sort */
var fl=document.querySelector('[data-filters]');
if(fl){
  var gridWrap=document.querySelector('[data-grid]'),cards=[].slice.call(gridWrap.querySelectorAll('.pcard')),cnt=document.querySelector('[data-count]'),emp=document.querySelector('[data-empty]'),sel=document.querySelector('[data-sort]');
  var gridEl=gridWrap.querySelector('.pgrid');
  function apply(){
    var kinds=[].slice.call(fl.querySelectorAll('[data-f=kind]:checked')).map(function(x){return x.value});
    var fins=[].slice.call(fl.querySelectorAll('[data-f=fin]:checked')).map(function(x){return x.value});
    var pr=fl.querySelector('[data-f=price]:checked');pr=pr&&pr.value?pr.value.split('-').map(Number):null;
    var shown=0;
    cards.forEach(function(c){var ok=true;
      if(kinds.length&&kinds.indexOf(c.dataset.kind)<0)ok=false;
      if(fins.length&&!fins.some(function(f){return (' '+c.dataset.fin+' ').indexOf(' '+f+' ')>-1}))ok=false;
      var p=+c.dataset.price;if(pr&&(p<pr[0]||p>=pr[1]))ok=false;
      c.hidden=!ok;if(ok)shown++});
    cnt.textContent=shown+' product'+(shown===1?'':'s');emp.hidden=shown>0;
    var s=sel.value,list=cards.slice();
    if(s==='lo')list.sort(function(a,b){return a.dataset.price-b.dataset.price});
    if(s==='hi')list.sort(function(a,b){return b.dataset.price-a.dataset.price});
    if(s==='new')list.sort(function(a,b){return b.dataset.new-a.dataset.new});
    list.forEach(function(c){gridEl.appendChild(c)});
  }
  fl.addEventListener('change',apply);sel.addEventListener('change',apply);
  document.querySelector('[data-clear]').onclick=function(){[].forEach.call(fl.querySelectorAll('input'),function(x){x.checked=x.dataset.f==='price'&&x.value===''});apply()};
}
/* Product page */
var pp=document.querySelector('[data-price]'),qty=document.querySelector('[data-qty]');
if(pp&&qty){
  var unit=parseFloat(pp.dataset.base)||0;
  function up(){var add=0;[].forEach.call(document.querySelectorAll('[data-opt]:checked'),function(r){add+=+r.dataset.add||0});pp.textContent=money((unit+add)*(+qty.value||1))}
  qty.addEventListener('input',up);document.addEventListener('change',up);
  var add=document.querySelector('[data-add]');if(add)add.onclick=function(){var c=document.querySelector('.cart span');if(c)c.textContent=(+c.textContent)+(+qty.value||1);add.textContent='Added (demo)'};
}
})();


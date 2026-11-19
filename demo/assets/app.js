
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
    list.forEach(function(c){gridEl.appendChild(c)});var pr=gridEl.querySelector('.promo-card');var vis=[].filter.call(gridEl.querySelectorAll('.pcard'),function(c){return !c.hidden});if(pr){gridEl.insertBefore(pr,vis[7]||null)}var tp=gridEl.querySelector('.cc-tip');if(tp){gridEl.insertBefore(tp,vis[7]||null)}
  }
  fl.addEventListener('change',apply);sel.addEventListener('change',apply);
  document.querySelector('[data-clear]').onclick=function(){[].forEach.call(fl.querySelectorAll('input'),function(x){x.checked=x.dataset.f==='price'&&x.value===''});apply()};
}
/* Modals: shipping estimate, bulk pricing, newsletter popup (SAMPLE rates and offer) */
var openM=function(id){var m=document.getElementById('m-'+id);if(m){m.hidden=false;var f=m.querySelector('input');if(f)f.focus()}};
var closeM=function(){[].forEach.call(document.querySelectorAll('.modal'),function(m){m.hidden=true})};
document.addEventListener('click',function(e){var t=e.target.closest('[data-modal]');if(t){e.preventDefault();closeM();openM(t.dataset.modal);return}
  if(e.target.closest('[data-close]')||e.target.classList.contains('modal'))closeM()});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeM()});
var shipF=document.querySelector('[data-ship]');
if(shipF){shipF.addEventListener('submit',function(e){e.preventDefault();
  var z=shipF.querySelector('input').value.trim(),lb=+shipF.querySelector('input[type=number]').value||1,out=document.querySelector('[data-ship-out]');out.hidden=false;
  if(!/^\d{5}$/.test(z)){out.textContent='Enter a 5-digit ZIP code.';return}
  var n=+z.slice(0,3),d=+z[0];
  if((n>=967&&n<=968)||(n>=995&&n<=999)){out.textContent='Sample rule: this concept does not ship to Alaska or Hawaii.';return}
  var reg=d<=3?'East':d<=7?'Central':'West',f=reg==='East'?1:reg==='Central'?1.25:1.6,ltl=lb>=150;
  var est=ltl?Math.round((120+0.9*lb)*f):Math.round((14+0.28*lb)*f);
  out.innerHTML='<strong>'+reg+' zone, '+(ltl?'LTL freight':'Ground')+'</strong><br>Estimated shipping: '+money(est)+' <small>(SAMPLE rate)</small><br>'+(ltl?'LTL orders ship the next day.':'Order by 2 pm ET and Ground orders ship the same day.')})}
[].forEach.call(document.querySelectorAll('.modal form:not([data-ship])'),function(f){f.addEventListener('submit',function(e){e.preventDefault();var b=f.querySelector('button');b.textContent='Thanks (demo)';b.disabled=true})});
if(document.querySelector('.hero-c,.hero-r,.hero-p')){try{if(!sessionStorage.getItem('sd-pop')){setTimeout(function(){if(!document.querySelector('.modal:not([hidden])')){openM('pop');sessionStorage.setItem('sd-pop','1')}},6000)}}catch(e){}}
/* Appointment booking (SAMPLE availability, demo only) */
var bk=document.querySelector('[data-book]');
if(bk){
  var type='Free layout call',day=null,time=null,days=[],dt=new Date();
  while(days.length<7){dt.setDate(dt.getDate()+1);if(dt.getDay()%6)days.push(new Date(dt))}
  var times=['9:00 AM','10:30 AM','12:00 PM','1:30 PM','3:00 PM','4:30 PM'];
  var fmt=function(x){return x.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric'})};
  var bout=bk.querySelector('[data-bk-out]');
  var draw=function(){
    var t=bk.querySelector('[data-bk-types]'),dd=bk.querySelector('[data-bk-days]'),tt=bk.querySelector('[data-bk-times]');
    var mk=function(host,label,on,fn){var b=document.createElement('button');b.type='button';b.textContent=label;if(on)b.className='bk-sel';b.onclick=fn;host.appendChild(b)};
    t.innerHTML='';dd.innerHTML='';tt.innerHTML='';
    ['Free layout call','Showroom visit'].forEach(function(x){mk(t,x,x===type,function(){type=x;draw()})});
    days.forEach(function(x,i){mk(dd,fmt(x),day===i,function(){day=i;draw()})});
    times.forEach(function(x){mk(tt,x+' ET',time===x,function(){time=x;draw()})});
    bout.hidden=!(day!==null&&time);
    if(!bout.hidden)bout.innerHTML='<strong>'+type+'</strong><br>'+fmt(days[day])+' at '+time+' ET (SAMPLE availability, demo only)';
  };
  draw();
}
/* Hero slider (Concept) */
var sl=document.querySelector('[data-slider]');
if(sl){var slides=[].slice.call(sl.querySelectorAll('.slide')),dots=[].slice.call(sl.querySelectorAll('.dot')),cur=0,timer=null;
  var go=function(n){cur=(n+slides.length)%slides.length;slides.forEach(function(s,i){s.classList.toggle('on',i===cur)});dots.forEach(function(d,i){d.classList.toggle('on',i===cur)})};
  var stop=function(){clearInterval(timer)},play=function(){stop();timer=setInterval(function(){go(cur+1)},6000)};
  sl.querySelector('[data-prev]').onclick=function(){go(cur-1);play()};sl.querySelector('[data-next]').onclick=function(){go(cur+1);play()};
  dots.forEach(function(d,i){d.onclick=function(){go(i);play()}});sl.addEventListener('mouseenter',stop);sl.addEventListener('mouseleave',play);play();}
/* Toast and quick add */
var toastEl=document.querySelector('[data-toast]');
var toast=function(t){if(!toastEl)return;toastEl.textContent=t;toastEl.hidden=false;clearTimeout(toastEl._t);toastEl._t=setTimeout(function(){toastEl.hidden=true},2200)};
document.addEventListener('click',function(e){var q=e.target.closest('[data-qadd]');if(q){e.preventDefault();var c=document.querySelector('.cart span');if(c)c.textContent=(+c.textContent)+1;toast('Added to cart (demo)')}});
/* SEO view panel */
var seoBtn=document.querySelector('[data-seo-toggle]'),seoPanel=document.querySelector('[data-seo-panel]');
if(seoBtn&&seoPanel){
  var sd={};try{sd=JSON.parse(document.getElementById('seo-data').textContent)}catch(e){}
  var metaEl=document.querySelector('meta[name=description]'),h1El=document.querySelector('h1');
  var il=0,el=0;[].forEach.call(document.querySelectorAll('main a[href]'),function(a){var h=a.getAttribute('href');if(a.hasAttribute('data-modal')||h==='#')return;if(/^https?:/.test(h))el++;else il++});
  var imgs=document.querySelectorAll('main img'),noAlt=[].filter.call(imgs,function(i){return !i.alt}).length;
  var chip=function(a){return '<div class="sp-chips">'+(a||[]).map(function(x){return '<span>'+x+'</span>'}).join('')+'</div>'};
  var lenNote=function(s,max){return '<em class="'+(s.length>max?'bad':'ok')+'">'+s.length+' characters (aim for '+max+' or fewer)</em>'};
  var row=function(l,v,e){return '<div class="sp-row"><span>'+l+'</span><div>'+v+'</div>'+(e||'')+'</div>'};
  var ttl=document.title,mt=metaEl?metaEl.content:'';
  seoPanel.querySelector('[data-seo-body]').innerHTML=
    row('Title tag',ttl,lenNote(ttl,60))+row('Meta description',mt,lenNote(mt,155))+row('H1',h1El?h1El.textContent:'')+row('Suggested live URL',sd.path||'')+
    row('Primary keyword',sd.kw||'')+row('Secondary keywords',chip(sd.sec))+row('Schema',chip(sd.schema))+
    row('Links in main content',il+' internal, '+el+' external')+row('Images',imgs.length+' ('+noAlt+' missing alt text)')+
    row('Strategy notes','<ul>'+(sd.notes||[]).map(function(x){return '<li>'+x+'</li>'}).join('')+'</ul>');
  seoBtn.onclick=function(){var on=seoPanel.hidden;seoPanel.hidden=!on;document.body.classList.toggle('seo-on',on);seoBtn.setAttribute('aria-pressed',on?'true':'false');seoBtn.textContent=on?'Hide SEO view':'SEO view';
    [].forEach.call(document.querySelectorAll('h1,h2,h3'),function(h){h.setAttribute('data-seo',h.tagName)})};
}
var ft=document.querySelector('[data-filter-toggle]'),fp=document.querySelector('[data-filters]');
if(ft&&fp){ft.onclick=function(){fp.hidden=!fp.hidden;ft.setAttribute('aria-expanded',fp.hidden?'false':'true');ft.querySelector('span').textContent=fp.hidden?'Show filters':'Hide filters'}}
var hm=document.querySelector('[data-hmenu]');
if(hm){hm.onclick=function(){var h=hm.closest('.hdr');var on=!h.classList.contains('nav-open');h.classList.toggle('nav-open',on);hm.setAttribute('aria-expanded',on?'true':'false')}}
/* Product page */
var pp=document.querySelector('[data-price]'),qty=document.querySelector('[data-qty]');
if(pp&&qty){
  var unit=parseFloat(pp.dataset.base)||0;
  function up(){var add=0;[].forEach.call(document.querySelectorAll('[data-opt]:checked'),function(r){add+=+r.dataset.add||0});pp.textContent=money((unit+add)*(+qty.value||1))}
  qty.addEventListener('input',up);document.addEventListener('change',up);
  var add=document.querySelector('[data-add]');if(add)add.onclick=function(){var c=document.querySelector('.cart span');if(c)c.textContent=(+c.textContent)+(+qty.value||1);add.textContent='Added (demo)';toast('Added to cart (demo)')};
}
})();


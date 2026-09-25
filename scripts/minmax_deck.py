"""Student-facing HTML slide deck; task data is supplied by minmax_materials."""
from html import escape

STYLE = '''
:root{--ink:#17233d;--muted:#65708a;--paper:#fffdf7;--violet:#6c5ce7;--line:#dde2ee}
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#111a2e;color:var(--ink);font-family:"Segoe UI",Arial,sans-serif}button{font:inherit;cursor:pointer}button:disabled{opacity:.35;cursor:default}button:focus-visible,a:focus-visible{outline:3px solid #e39327;outline-offset:4px}.deck{height:100dvh}.slide{position:absolute;inset:0;display:none;overflow:auto;padding:clamp(28px,5vh,65px) clamp(28px,6vw,100px) 100px;background:radial-gradient(circle at 94% 8%,rgba(108,92,231,.11) 0 9%,transparent 9.3%),radial-gradient(circle at 4% 94%,rgba(72,167,255,.11) 0 10%,transparent 10.3%),var(--paper)}.slide.active{display:flex;flex-direction:column;gap:clamp(18px,3vh,32px)}header{flex-shrink:0}.kicker{font-size:clamp(12px,1.2vw,18px);color:var(--violet);letter-spacing:.13em;text-transform:uppercase;font-weight:800;margin:0 0 12px}h1,h2,h3,p{margin-top:0}h1{font-size:clamp(52px,7vw,106px);line-height:1;letter-spacing:-.05em;margin-bottom:26px}h2{font-size:clamp(32px,4.4vw,66px);line-height:1.07;letter-spacing:-.04em;margin:0;max-width:1200px}h3{font-size:clamp(24px,2.4vw,36px);line-height:1.2;margin-bottom:16px}p,li{font-size:clamp(21px,2.1vw,31px);line-height:1.48;margin-bottom:20px}.content{width:100%;max-width:1400px;margin:auto}.columns{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,4vw,65px);align-items:center}.cover .content{margin:auto 0}.lead{max-width:850px;font-size:clamp(25px,2.7vw,40px)}.card{padding:clamp(20px,2.7vw,38px);background:white;border:1px solid var(--line);border-radius:24px}.mint{background:#e3f8f1}.orange{background:#fff0dc}.violet{background:#eeeafe}.numbers{display:flex;flex-wrap:wrap;gap:15px;align-items:center;margin:20px 0}.number{font:800 clamp(35px,4vw,68px) Consolas,monospace;padding:15px 24px;border-radius:18px;background:white;border:2px solid var(--line)}.number.hot{background:#eeeafe;border-color:var(--violet)}.number.stop{border-style:dashed;color:var(--muted)}.big{font:800 clamp(50px,6vw,90px) Consolas,monospace;margin:16px 0}code,pre{font-family:Consolas,"Courier New",monospace}p code{color:var(--violet);font-size:.95em}pre{background:#172238;color:#f7f8ff;border-radius:23px;padding:clamp(20px,2.5vw,36px);font-size:clamp(18px,1.9vw,29px);line-height:1.55;white-space:pre;overflow:auto;margin:0}.action{background:var(--violet);color:white;border:0;border-radius:12px;padding:12px 22px;font-size:clamp(17px,1.5vw,23px);font-weight:700}.action.secondary{background:white;border:1px solid var(--line);color:var(--ink)}.answer{margin-top:20px;padding:18px 24px;border-radius:16px;background:#e3f8f1;font-size:clamp(20px,1.9vw,28px);line-height:1.5}[hidden]{display:none!important}.question{font-size:clamp(26px,3vw,44px);font-weight:700;line-height:1.25}.registers{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin:22px 0}.registers div{padding:20px;border-radius:18px;background:#eeeafe}.registers div:nth-child(2){background:#e3f8f1}.registers div:nth-child(3){background:#fff0dc}.registers span{font:700 clamp(20px,2vw,30px) Consolas,monospace}.registers strong{font:800 clamp(44px,5vw,74px) Consolas,monospace;display:block}.trace-message{min-height:2.8em;margin-bottom:12px;font-size:clamp(20px,2vw,29px)}.trace .numbers{margin-top:0}.io{display:grid;grid-template-columns:1fr 1fr;gap:20px}.io h3{font-size:20px;color:var(--muted)}.io pre{background:white;color:var(--ink);border:1px solid var(--line);min-height:155px;font-size:clamp(24px,2.8vw,40px);line-height:1.32}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;font-size:clamp(20px,2vw,30px)}th,td{text-align:left;padding:clamp(9px,1.2vh,17px) 20px;border-bottom:1px solid var(--line)}th{color:var(--muted);font-size:.75em}td{font-family:Consolas,monospace}tr:last-child td{border:0}.small{font-size:clamp(18px,1.65vw,25px)}.nav-shell{position:fixed;z-index:20;bottom:20px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:12px;padding:8px 12px;background:white;box-shadow:0 7px 35px #17233d22;border:1px solid var(--line);border-radius:18px}.nav-button{border:0;border-radius:10px;width:44px;height:40px;background:#f0edff;color:var(--violet);font-size:24px;font-weight:750}.counter{font:700 17px Consolas,monospace;min-width:70px;text-align:center}.progress-track{position:fixed;bottom:0;left:0;width:100%;height:4px;background:#dfe3f0;z-index:20}.progress-bar{height:100%;background:var(--violet)}.home-link{position:fixed;left:22px;bottom:28px;z-index:20;color:var(--muted);text-decoration:none;font-size:22px}
@media(max-width:800px){.slide{padding:25px 26px 100px}.columns{grid-template-columns:1fr;gap:22px}.content{margin:0 auto}.cover .content{margin:auto 0}h2{font-size:34px}p,li{font-size:22px}.registers{gap:9px}.registers div{padding:12px}.number{padding:12px 18px}.io pre{min-height:100px}.home-link{left:14px}.nav-shell{gap:7px}.nav-button{width:38px}.trace-message{min-height:0}}
@media(max-height:650px) and (min-width:801px){.slide{padding-top:25px;padding-bottom:88px;gap:18px!important}h2{font-size:38px}p,li{font-size:23px}pre{font-size:20px;padding:20px}.number{font-size:40px;padding:10px 17px}.registers{margin:12px 0}.registers strong{font-size:45px}.registers div{padding:12px}.content{margin:auto}.io pre{font-size:28px}.big{font-size:56px}}
@media print{html,body{height:auto;overflow:visible;background:white}.deck{height:auto}.slide,.slide.active{position:relative;display:block;overflow:visible;min-height:95vh;break-after:page;padding:25px;background:white}header{margin-bottom:30px}.nav-shell,.progress-track,.home-link,.action{display:none}.columns{grid-template-columns:1fr 1fr}.content{margin:0}.answer[hidden]{display:block!important}h1{font-size:48pt}h2{font-size:30pt}p,li{font-size:19pt}pre{font-size:17pt;white-space:pre-wrap}}
'''

STYLE += '.answer{margin-top:16px;padding:16px 22px;font-size:clamp(19px,1.8vw,26px);line-height:1.45}'

SCRIPT = '''
(() => {
 'use strict';
 const slides=[...document.querySelectorAll('.slide')];let current=0;
 function goTo(index,writeHash=true){
  current=Math.max(0,Math.min(slides.length-1,index));
  slides.forEach((s,i)=>{const active=i===current;s.classList.toggle('active',active);s.setAttribute('aria-hidden',String(!active));s.inert=!active;if(active)s.scrollTop=0;});
  document.getElementById('counter').textContent=`${current+1} / ${slides.length}`;
  document.getElementById('prevBtn').disabled=current===0;document.getElementById('nextBtn').disabled=current===slides.length-1;
  document.getElementById('progressBar').style.width=`${(current+1)/slides.length*100}%`;
  if(writeHash)history.replaceState(null,'','#'+(current+1));
 }
 document.getElementById('prevBtn').addEventListener('click',()=>goTo(current-1));
 document.getElementById('nextBtn').addEventListener('click',()=>goTo(current+1));
 async function fullscreen(){try{if(document.fullscreenElement)await document.exitFullscreen?.();else await document.documentElement.requestFullscreen?.();}catch(_){}}
 document.getElementById('fullBtn').addEventListener('click',fullscreen);
 document.querySelectorAll('[data-reveal]').forEach(b=>b.addEventListener('click',()=>{const a=b.nextElementSibling;a.hidden=!a.hidden;b.textContent=a.hidden?(b.dataset.label||'Ответ'):'Скрыть';b.setAttribute('aria-expanded',String(!a.hidden));}));
 document.querySelectorAll('.trace').forEach(t=>{
  const values=t.dataset.values.split(',').map(Number);let cursor=0,mn=null,mx=null;
  const nums=t.querySelector('.numbers'),regs=t.querySelectorAll('.registers strong'),msg=t.querySelector('.trace-message'),next=t.querySelector('[data-trace-next]');
  nums.replaceChildren(...values.map(x=>{const el=document.createElement('span');el.className='number'+(x===0?' stop':'');el.textContent=x;return el;}));
  next.addEventListener('click',()=>{
   if(cursor>=values.length)return;const x=values[cursor];[...nums.children].forEach((el,i)=>el.classList.toggle('hot',i===cursor));
   if(x===0)msg.textContent=`Стоп. Ноль не меняет рекорды. Вывод: ${mx} ${mn}.`;
   else if(mn===null){mn=mx=x;msg.textContent='Первое число задаёт оба рекорда.';}
   else{const changes=[];if(x<mn){mn=x;changes.push('Новый минимум: '+mn);}if(x>mx){mx=x;changes.push('Новый максимум: '+mx);}msg.textContent=changes.length?changes.join('. ')+'.':'Рекорды не изменились.';}
   regs[0].textContent=x;regs[1].textContent=mn;regs[2].textContent=mx;cursor++;next.disabled=cursor===values.length;
  });
  t.querySelector('[data-trace-reset]').addEventListener('click',()=>{cursor=0;mn=mx=null;regs.forEach(el=>el.textContent='?');[...nums.children].forEach(el=>el.classList.remove('hot'));msg.textContent='Первое число ещё не прочитано.';next.disabled=false;});
 });
 document.addEventListener('keydown',e=>{
  const tag=document.activeElement?.tagName;if(['INPUT','TEXTAREA','SELECT'].includes(tag))return;
  if(['ArrowRight','PageDown'].includes(e.key)){e.preventDefault();goTo(current+1);}
  else if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();goTo(current-1);}
  else if(e.key==='Home'){e.preventDefault();goTo(0);}
  else if(e.key==='End'){e.preventDefault();goTo(slides.length-1);}
  else if(e.key===' '&&!['BUTTON','A'].includes(tag)){e.preventDefault();const trace=slides[current].querySelector('[data-trace-next]:not(:disabled)');const reveal=[...slides[current].querySelectorAll('[data-reveal]')].find(el=>el.nextElementSibling.hidden);if(trace)trace.click();else if(reveal)reveal.click();else goTo(current+1);}
  else if(e.key.toLowerCase()==='f')fullscreen();
 });
 let touch=null;
 document.addEventListener('touchstart',e=>{touch=null;if(e.target.closest('button,a,pre,.table-wrap'))return;const p=e.changedTouches[0];touch={x:p.clientX,y:p.clientY};},{passive:true});
 document.addEventListener('touchend',e=>{if(!touch)return;const p=e.changedTouches[0],dx=p.clientX-touch.x,dy=p.clientY-touch.y;if(Math.abs(dx)>80&&Math.abs(dx)>Math.abs(dy)*1.5)goTo(current+(dx<0?1:-1));touch=null;},{passive:true});
 function fromHash(){const n=Number(location.hash.slice(1));goTo(Number.isInteger(n)&&n>=1&&n<=slides.length?n-1:0,false);}
 window.addEventListener('hashchange',fromHash);fromHash();
})();
'''

def code(text):
    return '<pre><code>'+escape(text)+'</code></pre>'

def reveal(text,label='Ответ'):
    return f'<button class="action" type="button" data-reveal data-label="{label}" aria-expanded="false">{label}</button><div class="answer" hidden>{text}</div>'

def numbers(*values):
    return '<div class="numbers">'+''.join(f'<span class="number">{v}</span>' for v in values)+'</div>'

def columns(left,right):
    return f'<div class="columns"><div>{left}</div><div>{right}</div></div>'

def render(tasks):
    slides=[]
    def add(title,body,kicker='',extra=''):
        slides.append(f'<section class="slide" data-title="{escape(title)}" {extra}><header><p class="kicker">{kicker}</p><h2>{escape(title)}</h2></header><div class="content">{body}</div></section>')
    def task(n):
        t=tasks[n-1];nums,answer=t['tests'][0]
        io=f'<div class="io"><div><h3>Ввод</h3>{code(chr(10).join(map(str,nums)))}</div><div><h3>Вывод</h3>{code(answer)}</div></div>'
        add(t['title'],columns('<p>'+escape(t['text'])+'</p>'+reveal(escape(t['hint']),'Подсказка'),io),f'Задача {n}',f'id="task-{n}" data-task="{n}"')
    def trace(title,values):
        body=f'<div class="trace" data-values="{values}"><div class="numbers"></div><div class="registers"><div><span>x</span><strong>?</strong></div><div><span>mn</span><strong>?</strong></div><div><span>mx</span><strong>?</strong></div></div><p class="trace-message" role="status">Первое число ещё не прочитано.</p><button class="action" data-trace-next type="button">Следующее число</button> <button class="action secondary" data-trace-reset type="button" aria-label="Повторить пример">↺</button></div>'
        add(title,body,'Пример')
    slides.append('<section class="slide cover active" data-title="Минимум и максимум"><div class="content"><p class="kicker">Python · 6–8 классы</p><h1>Минимум<br>и максимум</h1><p class="lead">Как находить рекорды,<br>когда числа приходят по одному</p>'+numbers(7,'−2',9)+'</div></section>')
    add('Что останется на табло?',columns('<p>Игроки набрали 6, 2 и 8 очков.</p>'+numbers(6,2,8)+'<p class="question">Как запомнить лучший результат?</p>','<div class="card orange"><h3>Текущий максимум</h3><p class="big">?</p>'+reveal('Сначала 6. После 2 рекорд не меняется. После 8 новый рекорд равен 8.')+'</div>'),'Рекорды')
    add('Ноль завершает ввод',columns(code('x = int(input())\nwhile x != 0:\n    print(x)\n    x = int(input())'),'<p>Каждое число вводится с новой строки.</p><p>Условие <code>x != 0</code> проверяется перед телом цикла.</p><p class="question">Что случится без последнего input()?</p>'+reveal('При ненулевом x цикл будет бесконечно печатать одно и то же число.')),'Вспомним while')
    add('Две переменные для рекордов',columns('<div class="card mint"><h3>Минимум · mn</h3><p>Самое маленькое из уже прочитанных чисел.</p>'+code('if x < mn:\n    mn = x')+'</div>','<div class="card orange"><h3>Максимум · mx</h3><p>Самое большое из уже прочитанных чисел.</p>'+code('if x > mx:\n    mx = x')+'</div>'),'Переменные')
    add('Первое число задаёт оба рекорда',columns(numbers(6)+'<p>Пока прочитано одно число, оно и самое маленькое, и самое большое.</p>',code('x = int(input())\nmn = x\nmx = x')),'Начальные значения')
    trace('Как меняются mn и mx?','6,2,8')
    add('Почему mx = 0 не подходит?',columns(numbers('−8','−3')+'<p>Ни одно число не больше нуля. Переменная mx так и останется равной 0.</p><p class="question">Но нуля среди данных нет.</p>','<div class="card orange"><p>Максимум этого потока</p><p class="big">−3</p><p>Начальное значение рекорда берём из самого потока.</p></div>'),'Частая ошибка')
    add('Поиск в потоке до нуля',columns(code('mx = int(input())\nx = int(input())\nwhile x != 0:\n    # сравнение и обновление mx\n    x = int(input())\nprint(mx)'),'<p>Первый ввод задаёт рекорд.</p><p>Цикл обрабатывает следующие числа, пока не встретит 0.</p><p>Итоговый вывод находится после цикла.</p>'),'Один рекорд')
    task(1);task(2)
    add('Один поток, две проверки',columns(code('if x > mx:\n    mx = x\nif x < mn:\n    mn = x'),'<p>mn и mx начинаются с первого числа.</p><p>Каждое следующее число сравнивается с обоими рекордами.</p><p>После цикла:</p>'+code('print(mx, mn)')),'Минимум и максимум')
    trace('Ноль не участвует в поиске','7,-2,9,0')
    add('А если число только одно?',columns('<div class="card mint"><h3>6, затем 0</h3><p>Минимум и максимум равны 6.</p></div>','<div class="card orange"><h3>4, 4, 4, затем 0</h3><p>Оба рекорда равны 4.</p></div>')+'<p style="margin-top:28px">Если первым пришёл 0, данных нет. У пустого потока нет минимума и максимума. В наших задачах поток непустой.</p>','Проверка алгоритма')
    task(3);task(4)
    rows=''.join(f'<tr data-test="{i}"><td>{", ".join(map(str,nums))}</td><td>{ans}</td></tr>' for i,(nums,ans) in enumerate(tasks[3]['tests'],1))
    add('Шесть проверок','<div class="table-wrap"><table><thead><tr><th>Ввод по одному числу на строке</th><th>Вывод: mx mn</th></tr></thead><tbody>'+rows+'</tbody></table></div>','Задача 4')
    add('Значение 7, первый индекс 1',columns('<div class="table-wrap"><table><thead><tr><th>Индекс i</th><th>0</th><th>1</th><th>2</th></tr></thead><tbody><tr><th>Число</th><td>2</td><td>7</td><td>7</td></tr></tbody></table></div><p style="margin-top:25px">При равенстве рекорд не обновляется. Поэтому сохраняется первая позиция.</p>',code('if x > mx:\n    mx = x\n    pos = i')+'<p class="small" style="margin-top:20px">i — текущий индекс, pos — индекс рекорда. Счёт начинается с 0.</p>'),'Позиция рекорда')
    for n in range(5,10):task(n)
    add('Рекорды хранятся в переменных',columns('<p>Начальные значения — первое число.</p><p>Новое число улучшает рекорд только при строгом сравнении.</p><p>Ноль завершает поток. Итог выводится после цикла.</p>','<div class="card violet"><h3>После каждого шага</h3><p>mn и mx — минимум и максимум среди всех прочитанных данных.</p><p class="small">Для поиска достаточно переменных и while. Список и встроенные min() / max() не нужны.</p></div>'),'Главное')
    add('Размах потока',columns('<p>Непустой поток целых чисел заканчивается 0.</p><p>Найдите разность максимального и минимального значений. Ноль не учитывается.</p>'+code('размах = mx - mn'),'<div class="table-wrap"><table><thead><tr><th>Ввод</th><th>Вывод</th></tr></thead><tbody><tr><td>7, −2, 9, 0</td><td>11</td></tr><tr><td>−8, −3, −5, 0</td><td>5</td></tr><tr><td>6, 0</td><td>0</td></tr></tbody></table></div>'),'Домашняя задача')
    return '''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#17233d"><meta name="description" content="Урок-презентация о поиске минимума и максимума в Python"><title>Минимум и максимум — Python, 6–8 классы</title><style>'''+STYLE+'''</style></head><body><main class="deck" aria-label="Урок о минимуме и максимуме">'''+ '\n'.join(slides)+'''</main><a class="home-link" href="../index.html" aria-label="Каталог уроков" title="Каталог уроков">⌂</a><nav class="nav-shell" aria-label="Навигация по презентации"><button class="nav-button" id="prevBtn" aria-label="Предыдущий слайд" title="Предыдущий слайд (←)">←</button><span class="counter" id="counter" aria-live="polite">1 / 24</span><button class="nav-button" id="nextBtn" aria-label="Следующий слайд" title="Следующий слайд (→)">→</button><button class="nav-button" id="fullBtn" aria-label="Полноэкранный режим" title="Полноэкранный режим (F)">⛶</button></nav><div class="progress-track" aria-hidden="true"><div class="progress-bar" id="progressBar"></div></div><script>'''+SCRIPT+'''</script></body></html>'''

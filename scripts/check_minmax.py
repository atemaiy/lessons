"""Verify the lesson's Python solutions against independent reference answers."""
import ast
import contextlib
import io
import random
import re
from html.parser import HTMLParser
from pathlib import Path
from minmax_materials import TASKS, HOME, ROOT

def run(code, nums):
    inputs=iter(map(str,nums))
    output=io.StringIO()
    with contextlib.redirect_stdout(output):
        exec(compile(code,'<solution>','exec'),{'input':lambda:next(inputs)})
    assert next(inputs,None) is None, 'Input was not fully consumed'
    return output.getvalue().strip()

rng=random.Random(20260925)
total=0
for task in TASKS+[HOME]:
    tree=ast.parse(task['code'])
    assert not any(isinstance(n,(ast.List,ast.ListComp,ast.SetComp,ast.DictComp)) for n in ast.walk(tree))
    assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {'min','max','sorted','list'} for n in ast.walk(tree))
    for nums,answer in task['tests']:
        assert run(task['code'],nums)==answer,(task['id'],nums,answer)
        total+=1
    for _ in range(200):
        ident=task['id']
        if ident=='1':
            values=[rng.randint(-10**9,10**9) for _ in range(3)]
        elif ident=='7':
            values=rng.sample(range(1,1000),rng.randint(2,25))
        elif ident in {'5','6','8'}:
            values=[rng.randint(1,20) for _ in range(rng.randint(2 if ident=='8' else 1,25))]
        else:
            values=[rng.choice([-1,1])*rng.randint(1,20) for _ in range(rng.randint(1,25))]
        expected={
            '1':lambda:min(values),'2':lambda:max(values),'3':lambda:min(values),
            '4':lambda:f'{max(values)} {min(values)}','5':lambda:values.index(max(values)),
            '6':lambda:values.count(max(values)),'7':lambda:sorted(values)[-2],
            '8':lambda:sorted(values)[1],
            '9':lambda:abs(values.index(min(values))-values.index(max(values))),
            'Д1':lambda:max(values)-min(values)
        }[ident]()
        nums=values if ident=='1' else values+[0]
        assert run(task['code'],nums)==str(expected),(ident,nums,expected)
        total+=1
print(f'PASS: {total} solution executions, 10 solutions, no lists or built-in extrema.')

class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])

path=ROOT/'lessons/python-min-max.html'
html=path.read_text(encoding='utf-8')
assert '{{' not in html,'Unexpanded template'
parser=Links();parser.feed(html)
assert len(parser.ids)==len(set(parser.ids)),'Duplicate HTML IDs'
for href in parser.links:
    if href.startswith('#'):assert href[1:] in parser.ids,href
    elif not re.match(r'https?://',href):assert (path.parent/href).exists(),href
assert len(re.findall('data-task="',html))==9
assert len(re.findall('data-test="',html))==6
assert len(re.findall('<section class="slide',html))==24
assert not re.search(r'<aside|timer-|data-reflection|data-note|localStorage|минут|преподавател|чек-лист',html,re.I)
from pypdf import PdfReader
pdf=PdfReader(ROOT/'output/pdf/minmax-solutions.pdf')
assert len(pdf.pages)==11
for i,t in enumerate(TASKS+[HOME],1):
    assert t['title'] in ' '.join(pdf.pages[i].extract_text().split())
print('PASS: lesson links, 9 task cards, 6 core tests, PDF pagination and task headings.')
temp=ROOT/'tmp/minmax-browser.js'
temp.parent.mkdir(parents=True,exist_ok=True)
temp.write_text(re.search(r'<script>(.*?)</script>',html,re.S).group(1),encoding='utf-8')

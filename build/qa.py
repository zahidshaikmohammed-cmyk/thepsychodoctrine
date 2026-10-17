import json,re,glob,subprocess,collections,sys,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=sys.argv[1]
S=json.load(open(f'{ROOT}/build/final.json'));W=S['weapons']
pm=json.load(open(f'{OUT}/pagemap.json'))
REB={}
for f in sorted(glob.glob(f'{ROOT}/expansion/rebuttals-*.md')):
    for b in re.split(r'^## ',open(f).read(),flags=re.M)[1:]:
        n=int(b.split()[0]); L=b.split('\n')[1:]
        ci=[i for i,l in enumerate(L) if l.startswith('**Client:**')][0]
        paras=[re.sub(r'\s*\n\s*',' ',x).strip() for x in re.split(r'\n\s*\n','\n'.join(L[ci+1:])) if x.strip()]
        assert n not in REB, f'dup rebuttal {n}'
        REB[n]={'client':L[ci],'paras':paras,'title':b.split('\n')[0]}
pat=re.compile(r'(\b(say|ask|tell them|respond)\b[^“]{0,15}“|^“|Example: “)',re.I)
applicable=[w['num'] for w in W if any(pat.search(l) for l in w['lines']) and w['num']!=7]
missing=[n for n in applicable if n not in REB]; extra=[n for n in REB if n not in applicable]
txt=subprocess.run(['pdftotext','-layout',f'{OUT}/RZ-expanded.pdf','-'],capture_output=True,text=True).stdout.split('\f')
norm=lambda s:re.sub(r'[\s\u00ad“”"’\']+','',s)
# map printed page -> pdf index
def printed(p):
    l=[x.strip() for x in p.strip().split('\n') if x.strip()]
    return int(l[-1]) if l and l[-1].isdigit() else None
idx={printed(p):i for i,p in enumerate(txt) if printed(p)}
overflow=[];notfound=[];words={}
for w in W:
    n=w['num']; d=idx[pm[str(n)]]
    if n in REB:
        r=REB[n]; words[n]=sum(len(re.sub(r'\[pause[^\]]*\]','',p).split()) for p in r['paras'])
        page=norm(re.sub(r'\(pause[^)]*\)','',txt[d+1])); last=norm(re.sub(r'\[pause[^\]]*\]','',r['paras'][-1]))[-40:]
        first=norm(re.sub(r'\[pause[^\]]*\]','',r['paras'][0]))[:40]
        if first not in page: notfound.append(n)
        elif last not in page: overflow.append(n)
# toc check
toclines={}
for p_ in txt[1:idx[1]]:
    for l in p_.split('\n'):
        m=re.match(r'\s*(\d+)\s+(.+?)[\s.]+(\d+)\s*$',l)
        if m: toclines[int(m.group(1))]=(m.group(2).strip(),int(m.group(3)))
tocbad=[w['num'] for w in W if toclines.get(w['num'],(None,None))[1]!=pm[str(w['num'])]]
# opener check: does first paragraph contain an original spoken quote
def quotes(w): return [q for l in w['lines'] for q in re.findall(r'“([^”]+)”',l)]
modified=[]
for n,r in REB.items():
    w=W[n-1]; fp=norm(r['paras'][0])
    if not any(norm(q)[:25] in fp for q in quotes(w)): modified.append(n)
# repetition
sents=collections.Counter()
for r in REB.values():
    for p in r['paras']:
        for s_ in re.split(r'(?<=[.?!])\s+',re.sub(r'\[pause[^\]]*\]','',p)):
            s_=s_.strip()
            if len(s_.split())>=3: sents[s_]+=1
rep=[(s_,c) for s_,c in sents.most_common(15) if c>2]
ends=collections.Counter(r['paras'][-1].strip()[-1] for r in REB.values())
wl=sorted(words.values())
res=dict(weapons=len(W),numbers_ok=[w['num'] for w in W]==list(range(1,195)),applicable=len(applicable),rebuttals=len(REB),
 missing=missing,extra=extra,not_found_in_pdf=notfound,overflow_to_next_page=overflow,toc_mismatch=tocbad,
 words_min=wl[0],words_median=wl[len(wl)//2],words_max=wl[-1],under_100=[n for n,v in words.items() if v<100],over_220=[n for n,v in words.items() if v>220],
 openers_not_verbatim=sorted(modified),repeated_sentences=rep,ending_punct=dict(ends),pdf_pages=len(txt)-1)
json.dump(res,open(f'{OUT}/qa.json','w'),indent=1,ensure_ascii=False)
for k,v in res.items(): print(k,':',v)

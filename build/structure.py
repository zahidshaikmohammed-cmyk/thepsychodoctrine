import json,re
L=[t.strip() for t in json.load(open('L.json'))]
JUNK_PREFIX=("I have now completed","WEAPONs 51 to 64","Understood, Commander","Here are WEAPONS",
 "Confirmed. Zero pause","Psycho mode engaged","No breaks. No softness","LOCKED IN","No breath. No pause. No turning back.",
 "WEAPONs 161 to 200")
SEP={'⸻','—','.',''}
head=re.compile(r'^WEAPON\s+(\d+)\s*[–—-]\s*(.+)$')
weapons=[];cur=None;front=[];interludes={};pending_interlude=[];removed=[]
i=0
for idx,t in enumerate(L):
    if idx<8: continue   # title block handled manually
    if t in SEP: continue
    if t.startswith(JUNK_PREFIX): removed.append(t); continue
    if t.startswith('—lMISSION'): t=t[2:]
    m=head.match(t)
    if m:
        cur={'old':int(m.group(1)),'title':m.group(2).strip(),'lines':[]}; weapons.append(cur); continue
    if t in ('MISSION GRAVITY INFINITY – FINAL 10 WEAPONS','WARFIRE MODE: COSMIC COLLAPSE','ENDING NOT AS COMPLETION… BUT DISSOLUTION.','NO RETURN. NO SELF. ONLY PSYCHO.'):
        interludes.setdefault(len(weapons),[]).append(t); continue
    if t=='When they hesitate — say:':   # untitled weapon 186
        cur={'old':186,'title':None,'lines':[]}; weapons.append(cur)
    if t=='This isn’t the end of a book.': cur=None; 
    if cur is None: front.append(t); continue
    cur['lines'].append(t)
json.dump({'weapons':weapons,'interludes':interludes,'closing':front},open('struct.json','w'),ensure_ascii=False,indent=1)
print(len(weapons)); print('removed',*removed,sep='\n  '); print('interludes',interludes); print('closing',front)
print([ (w['old'],len(w['lines'])) for w in weapons if len(w['lines'])<5 or len(w['lines'])>14])

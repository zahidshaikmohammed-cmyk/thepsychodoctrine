import json,re
S=json.load(open('struct.json'))
W=S['weapons']
EXACT={
 'Just verbal Pressure they can’t escape.':'Just verbal pressure they can’t escape.',
 'The final yes is not bright. It’s quiet and Controlled.':'The final yes is not bright. It’s quiet and controlled.',
 'Silence is not absence. It’s WEAPONized delay.':'Silence is not absence. It’s weaponized delay.',
 'You are not theory. You are trauma turned WEAPON.':'You are not theory. You are trauma turned weapon.',
 'This WEAPON removes time from the equation.':'This weapon removes time from the equation.',
 'Your eyes, even on phone, must pierce their pattern.':'Your eyes, even on the phone, must pierce their pattern.',
 'Even when they scroll Insta, your tone plays in background.':'Even when they scroll Insta, your tone plays in the background.',
 'Make them pause, tilt their head, and hold breath.':'Make them pause, tilt their head, and hold their breath.',
 'Not sales tactic.':'Not a sales tactic.',
 'Sales happens before the payment.':'The sale happens before the payment.',
 'The close is never an ending, it’s completion.':'The close is never an ending — it’s completion.',
 'Necessity is not just a word, it’s a feeling.':'Necessity is not just a word — it’s a feeling.',
 'This imprint is forever permanent.':'This imprint is permanent.',
 'The decision is final, and the future seals.':'The decision is final, and the future is sealed.',
 'Every decision they make is a step towards their true destiny.':'Every decision they make is a step toward their true destiny.',
 'Pressure is not a force. It’s a truth.':'Pressure is not a force. It’s a truth.',
}
changed=[]
for w in W:
    out=[]
    for l in w['lines']:
        n=EXACT.get(l,l)
        n=re.sub(r'^(Say|Ask|Tell them)[,]?\s+“',r'\1: “',n)
        n=re.sub(r'\s+\.',r'.',n)
        n=n.replace('judgement','judgment')
        if n!=l: changed.append((l,n))
        out.append(n)
    w['lines']=out
S['closing']=[c.replace('Book sleep mode . ','Book sleep mode. ') for c in S['closing']]
# titles
SMALL={'a','an','the','and','or','of','to','in','on','for','at','by','as'}
def tc(t):
    t=t.replace('JUDGEMENT','JUDGMENT')
    words=t.split(' ')
    res=[]
    for k,wd in enumerate(words):
        parts=wd.split('-')
        pp=[]
        for j,p in enumerate(parts):
            low=p.lower()
            if (k>0 and j==0 and low in SMALL): pp.append(low)
            elif low=='b' and k>0: pp.append('B')
            else: pp.append(low[:1].upper()+low[1:])
        res.append('-'.join(pp))
    return ' '.join(res)
W[[w['old'] for w in W].index(186)]['title']='THE SINGLE LADDER'
for n,w in enumerate(W,1):
    w['num']=n; w['title_tc']=tc(w['title'])
json.dump(S,open('final.json','w'),ensure_ascii=False,indent=1)
for a,b in changed: print('-',a,'\n+',b)
print(len(changed))
for w in W: print(w['num'],w['old'],w['title_tc'])

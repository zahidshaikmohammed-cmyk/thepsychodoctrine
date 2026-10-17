import json,csv,re,sys
S=json.load(open('build/final.json'));W=S['weapons']
BP={int(r['num']):r for r in csv.DictReader(open('expansion/blueprint.tsv'),delimiter='\t')}
assert len(BP)==len(W)==194
spoken=lambda w:[l for l in w['lines'] if '“' in l]
def verdict(w):
    sp=spoken(w)
    if not sp: return 'No spoken line','Build a full rebuttal from the weapon concept'
    words=sum(len(l.split()) for l in sp)
    if len(sp)==1: return f'One-line strike ({words} w)','Expand into full rebuttal'
    return f'Partial exchange, {len(sp)} lines ({words} w)','Expand into a complete conversation'
CLUSTERS=[
 ('Silence after a key moment',[17,23,62,113,142,189],'Six weapons use silence; each is assigned a different moment (after the proposal, after "I don\'t know", after asking for the decision, after an excuse, at the final summary, after a hard truth).'),
 ('Delay / "later" objections',[4,22,37,57,66,72,106,112,115,128],'Ten weapons handle postponement. Triggers are split by the exact words used (next month, no rush, why today, market correction, eventually, today-only, wait and see, think about it, need time, when less busy).'),
 ('Uncertain yes',[87,134,161],'Reluctant yes, unsure yes, terse yes by text. Close to each other; review whether all three are needed.'),
 ('Lasting impression at call end',[29,120,173],'Very similar purpose. Strategies differ slightly (not ready / has to go / overwhelmed). Review.'),
 ('Pressure and consent',[71,103,146],'"Are you pressuring me", "Let me breathe", "Why are you so sure". Distinct triggers, related concept.'),
 ('Funding and payment',[125,151,170],'How to pay safely, hesitation to transfer, pause at the payment step.'),
 ('Comparing brokers',[14,131],'Same core situation. Review.'),
 ('Inherited beliefs about markets',[77,140],'Family view now vs. upbringing. Close; review.'),
 ('Purpose / goal',[43,55],'"Why do I need this" vs "I have no goal". Bodies overlap heavily; review.'),
 ('One path',[50,53],'Original bodies share five lines. Triggers split: "send five plans" vs "what if I pick wrong".'),
 ('Follow-up after silence',[121,160],'Unreplied for a week vs. ghosted after a good call. Close; review.'),
 ('Status quo is fine',[82,117,154],'Happy as is / staying put is safe / going back to old ways.'),
 ('Market prediction',[7,187],'"How do you know it goes up" vs "where is the market going". Related; review.'),
 ('Duplicate titles (different text)',[4,65,31,66,56,73,69,81],'Final Push 4/65, Pressure of Decision 31/66, Final Judgment 56/73, Invisible Contract 69/81. Titles should be renamed before publishing.'),
 ('"Decision is inevitable" theme in original text',[31,34,35,39,44,45,53,56,59,60,74,81,87,92,93],'These original bodies repeat the same idea in near-identical sentences ("Psycho doesn\'t X. He makes them Y."). The new rebuttals give each a different job, but the doctrine lines themselves stay similar.'),
]
inc={}
for name,nums,_ in CLUSTERS:
    for n in nums: inc.setdefault(n,[]).append(name)
FLAGS=[('insider leak','Implies the caller has inside information, which can be illegal and invites regulatory trouble.'),
 ('You need to sound like you do','Advises bluffing expertise; conflicts with the "factual integrity" standard.'),
 ('financial insecurity and twist it','Instructs exploiting insecurity; conflicts with "without manipulation".'),
 ('voice of limited availability','Encourages manufactured scarcity.'),
 ('seal the deal mid-collapse','Closing while the client is distressed; conflicts with informed consent.'),
 ('Twist the knife','Shame as a closing lever.'),
 ('Let them sweat','Deliberately inducing physical anxiety to close.'),
 ('End the call without warning','Hanging up abruptly; poor practice and reflects on the firm.'),
 ('Swipe the card. Kill the doubt.','Pushes payment as a way to end doubt.'),
 ('Imagine this is your last month alive','Mortality pressure as a sales lever.'),
 ('The mind is now coerced','States coercion as the goal.'),
 ('emotional masturbation','Crude; may limit where the book can be sold.'),
 ('Not fucking beg','Profanity; fine if intended, may limit distribution.')]
flag_rows=[]
for w in W:
    for l in w['lines']:
        for k,why in FLAGS:
            if k.lower() in l.lower(): flag_rows.append((w['num'],w['title_tc'],l,why))
# ---- audit
A=['# Stage A — Audit of all 194 weapons','',
'Every weapon was read individually. "Spoken lines" are the existing quoted lines the seller says aloud; everything else in a weapon is doctrine (instruction to the seller).','',
'**Finding:** none of the 194 weapons contains a complete rebuttal. The longest spoken passage is a short exchange of a few lines. Every weapon needs expansion; none needs its doctrine rewritten to do so.','']
cnt={'No spoken line':0,'One-line':0,'Partial':0}
for w in W:
    v=verdict(w)[0]; cnt['No spoken line' if v.startswith('No') else 'One-line' if v.startswith('One') else 'Partial']+=1
A+=[f"| Status | Weapons |","|---|---|",f"| No spoken line at all | {cnt['No spoken line']} |",f"| One-line strike | {cnt['One-line']} |",f"| Partial exchange (2+ short lines) | {cnt['Partial']} |",'',
'## Lines to review before publishing','','These doctrine lines conflict with the standard in the Phase 2 brief (factual integrity, no manipulation). They are **unchanged**; the new rebuttals simply don\'t follow them. Decide whether to keep, soften or cut each.','',
'| # | Weapon | Line | Why it\'s flagged |','|---|---|---|---|']
A+=[f"| {n} | {t} | {l} | {why} |" for n,t,l,why in flag_rows]
A+=['','## Inventory','','| # | Weapon | Original purpose | Current spoken lines | Status | Need |','|---|---|---|---|---|---|']
for w in W:
    v,need=verdict(w); sp=' / '.join(spoken(w)) or '—'
    A.append(f"| {w['num']} | {w['title_tc']} | {BP[w['num']]['purpose']} | {sp.replace('|','/')} | {v} | {need} |")
open('expansion/01-audit.md','w').write('\n'.join(A)+'\n')
# ---- blueprint
B=['# Stage B — Blueprint','',
'## The standard every rebuttal follows','',
'1. **Opening strike** — engages the client\'s exact words in the first sentence.',
'2. **Psychological read** — names the likely concern underneath, as a question or possibility, never as mind-reading.',
'3. **Substance** — real facts, costs, risks or process. Confidence never stands in for an answer.',
'4. **Counter-layer** — anticipates the most reasonable follow-up and answers it.',
'5. **Decisive close** — ends on a clear next step or a direct question. No recycled catchphrases.','',
'**Integrity rules** (from your brief: "factual integrity", "without manipulation"):','',
'- No promised or implied returns; no "insider" framing.',
'- No invented deadlines or scarcity. If a real deadline exists, state it.',
'- Leverage and loss risk are always stated plainly when relevant.',
'- "No" and "not now" are treated as legitimate outcomes, and the rebuttal says so.',
'- Firm-specific facts (name, regulator, registration, fees) are left as `[placeholders]` until you supply them.','',
'## Overlap map','','Repeated concepts were mapped before any writing. Nothing has been deleted or merged; where two weapons do the same job, they are flagged for your decision.','',
'| Cluster | Weapons | Note |','|---|---|---|']
B+=[f"| {n} | {', '.join(map(str,nums))} | {note} |" for n,nums,note in CLUSTERS]
B+=['','## Per-weapon plan','','Each weapon gets its own client trigger, so no two rebuttals answer the same sentence.','',
'| # | Weapon | Client trigger | Rebuttal strategy | Close | Overlap flag |','|---|---|---|---|---|---|']
for w in W:
    b=BP[w['num']]; f='; '.join(inc.get(w['num'],[])) or ''
    B.append(f"| {w['num']} | {w['title_tc']} | {b['trigger']} | {b['strategy']} | {b['close']} | {f} |")
open('expansion/02-blueprint.md','w').write('\n'.join(B)+'\n')
# trigger uniqueness check
tr=[b['trigger'].lower() for b in BP.values()]
print('dup triggers',[t for t in set(tr) if tr.count(t)>1]); print('flags',len(flag_rows)); print(cnt)

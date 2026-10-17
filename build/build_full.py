"""Two-pass build of the expanded edition: render, read real page numbers, rebuild contents."""
import json, os, re, subprocess, sys, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'out')
os.makedirs(OUT, exist_ok=True)
S = json.load(open(f'{ROOT}/build/final.json')); W = S['weapons']
reb = ','.join(sorted(glob.glob(f'{ROOT}/expansion/rebuttals-*.md')))
env = dict(os.environ, REBUTTALS=reb, EDITION='Expanded Edition', NODE_PATH='/usr/local/lib/node_modules_global')
docx, pdf = f'{OUT}/RZ-expanded.docx', f'{OUT}/RZ-expanded.pdf'
norm = lambda s: re.sub(r'[\s­]+', '', s)

def build(pagemap=None):
    e = dict(env)
    if pagemap: e['PAGEMAP'] = pagemap
    subprocess.run(['node', f'{ROOT}/build/book.js', f'{ROOT}/build/final.json', docx], env=e, check=True, capture_output=True)
    if os.path.exists(pdf): os.remove(pdf)
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', OUT, docx], check=True, capture_output=True, timeout=900)

def pages():
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.split('\f')
    return txt[:n]

def pagemap(P):
    # main matter starts on the page whose printed number is 1; find doctrine page of each weapon
    def printed(p):
        lines = [l.strip() for l in p.strip().split('\n') if l.strip()]
        return int(lines[-1]) if lines and lines[-1].isdigit() else None
    pm = {}; start = 0
    for w in W:
        key1, key2 = norm(w['title_tc']), norm(w['lines'][0])
        for i in range(start, len(P)):
            t = norm(P[i])
            if key1 in t and key2 in t and 'THEREBUTTAL' not in t.replace(' ', ''):
                pm[w['num']] = printed(P[i]); start = i + 1; break
        else:
            raise SystemExit(f'weapon {w["num"]} not found')
    for i in range(len(P) - 1, 0, -1):
        if 'Only silence follows' in P[i]: pm['final'] = printed(P[i]); break
    return pm

build(); P = pages(); pm1 = pagemap(P)
json.dump(pm1, open(f'{OUT}/pagemap.json', 'w'))
build(f'{OUT}/pagemap.json'); P = pages(); pm2 = pagemap(P)
print('pages', len(P), 'stable', pm1 == pm2, 'final', pm2.get('final'))

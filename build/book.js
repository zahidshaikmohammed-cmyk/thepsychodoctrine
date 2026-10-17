const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, Header, Footer, PageNumber,
  TabStopType, LeaderType, BorderStyle, NumberFormat, SectionType,
} = require('docx');

const S = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const OUT = process.argv[3];
// Optional expanded rebuttals (markdown) and pilot mode
const REB = {};
if (process.env.REBUTTALS) for (const f of process.env.REBUTTALS.split(',')) {
  const md = fs.readFileSync(f, 'utf8');
  for (const block of md.split(/^## /m).slice(1)) {
    const m = block.match(/^(\d+)\s/); if (!m) continue;
    const lines = block.split('\n').slice(1);
    const ci = lines.findIndex(l => l.startsWith('**Client:**'));
    const client = lines[ci].replace('**Client:**', '').trim();
    const paras = lines.slice(ci + 1).join('\n').split(/\n\s*\n/).map(x => x.replace(/\s*\n\s*/g, ' ').trim()).filter(x => x && !x.startsWith('---'));
    REB[Number(m[1])] = { client, paras };
  }
}
const PILOT = !!process.env.PILOT;
const W = PILOT ? S.weapons.filter(w => REB[w.num]) : S.weapons;
if (PILOT) S.interludes = {};
const FONT = 'Cambria';
const INK = '1A1A1A', ACCENT = '8B1A1A', GREY = '7A7A7A';

// 6 x 9 in trade paperback
const PAGE = { size: { width: 8640, height: 12960 },
  margin: { top: 1080, bottom: 1080, left: 1188, right: 1188, header: 576, footer: 576 } };
const TEXT_W = 8640 - 1188 * 2;

const r = (text, o = {}) => new TextRun({ text, font: FONT, color: INK, ...o });
const P = (children, o = {}) => new Paragraph({ children: Array.isArray(children) ? children : [children], ...o });

// ---------- page plan (each weapon on its own page) ----------
const interludeAt = Object.keys(S.interludes).map(Number); // index in weapons list
let page = 1; const pageOf = [];
W.forEach((w, i) => { if (interludeAt.includes(i)) page++; pageOf[i] = page++; });
let interludePage = pageOf[interludeAt[0]] - 1;
let finalPage = pageOf[W.length - 1] + 1;
if (process.env.PAGEMAP) {
  const pm = JSON.parse(fs.readFileSync(process.env.PAGEMAP, 'utf8'));
  W.forEach((w, i) => { if (pm[w.num]) pageOf[i] = pm[w.num]; });
  if (pm.final) finalPage = pm.final;
}

// ---------- front matter ----------
const front = [];
front.push(P(r('MISSION ZERØ TO 9', { size: 22, color: ACCENT, characterSpacing: 120, bold: true }),
  { alignment: AlignmentType.CENTER, spacing: { before: 2600, after: 360 } }));
front.push(P(r('THE PSYCHO', { size: 64, bold: true, characterSpacing: 40 }), { alignment: AlignmentType.CENTER, spacing: { after: 0 } }));
front.push(P(r('SELLER DOCTRINE', { size: 64, bold: true, characterSpacing: 40 }), { alignment: AlignmentType.CENTER, spacing: { after: 360 } }));
front.push(P([], { alignment: AlignmentType.CENTER, indent: { left: 2200, right: 2200 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: ACCENT, space: 1 } }, spacing: { after: 360 } }));
front.push(P(r('The Full Scripture', { size: 28, italics: true }), { alignment: AlignmentType.CENTER, spacing: { after: 120 } }));
front.push(P(r(`${W.length} Weapons`, { size: 22, color: GREY, characterSpacing: 60 }), { alignment: AlignmentType.CENTER, spacing: { after: 2400 } }));
front.push(P(r('Layered. Dominant. Stock-Market-Coded. Human-Written. No AI.', { size: 17, color: GREY, italics: true }),
  { alignment: AlignmentType.CENTER }));

if (!PILOT && process.env.EDITION) front.splice(5, 1,
  P(r(`${W.length} Weapons · ${process.env.EDITION}`, { size: 22, color: GREY, characterSpacing: 60 }), { alignment: AlignmentType.CENTER, spacing: { after: 2400 } }));
if (PILOT) front.splice(4, 2,
  P(r('Expanded Edition', { size: 28, italics: true }), { alignment: AlignmentType.CENTER, spacing: { after: 120 } }),
  P(r(`PILOT DRAFT · WEAPONS ${W[0].num}–${W[W.length - 1].num}`, { size: 18, color: ACCENT, characterSpacing: 60, bold: true }), { alignment: AlignmentType.CENTER, spacing: { after: 2400 } }));
// Contents
if (!PILOT) front.push(P(r('CONTENTS', { size: 26, bold: true, characterSpacing: 100, color: ACCENT }),
  { pageBreakBefore: true, alignment: AlignmentType.CENTER, spacing: { before: 240, after: 360 } }));
const tocLine = (num, title, pg) => P([
  r(num, { size: 18, color: ACCENT, bold: true }), r('\t' + title, { size: 19 }), r('\t' + pg, { size: 18, color: GREY }),
], { tabStops: [{ type: TabStopType.LEFT, position: 520 }, { type: TabStopType.RIGHT, position: TEXT_W, leader: LeaderType.DOT }],
  spacing: { after: 30, line: 264 } });
if (!PILOT) W.forEach((w, i) => {
  if (interludeAt.includes(i)) {
    front.push(P(r('MISSION GRAVITY INFINITY — THE FINAL TEN', { size: 16, bold: true, characterSpacing: 60, color: ACCENT }),
      { spacing: { before: 160, after: 80 }, tabStops: [{ type: TabStopType.RIGHT, position: TEXT_W }] }));
  }
  front.push(tocLine(String(w.num), w.title_tc, String(pageOf[i])));
});
if (!PILOT) front.push(tocLine('', 'Final Word', String(finalPage)));

// ---------- main matter ----------
const SPEECH = /^((?:Then |Now |And then )?(?:say|Say|ask|Ask|Tell them|respond)):\s/;
function bodyLine(t) {
  const m = t.match(SPEECH);
  const runs = m ? [r(m[1] + ': ', { bold: true, color: ACCENT, size: 22 }), r(t.slice(m[0].length), { size: 22 })] : [r(t, { size: 22 })];
  return P(runs, { spacing: { after: 100, line: 300 } });
}
const main = [];
const spacer = (after, brk = true) => P([], { pageBreakBefore: brk, spacing: { before: 0, after, line: 240 } });
W.forEach((w, i) => {
  if (interludeAt.includes(i)) {
    const lines = S.interludes[String(i)];
    main.push(spacer(2400));
    main.push(P(r('MISSION GRAVITY INFINITY', { size: 40, bold: true, characterSpacing: 60 }),
      { alignment: AlignmentType.CENTER, spacing: { before: 3000, after: 200 } }));
    main.push(P(r('The Final Ten Weapons', { size: 26, italics: true, color: ACCENT }), { alignment: AlignmentType.CENTER, spacing: { after: 360 } }));
    main.push(P([], { alignment: AlignmentType.CENTER, indent: { left: 2400, right: 2400 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: ACCENT, space: 1 } }, spacing: { after: 360 } }));
    lines.slice(1).forEach(l => main.push(P(r(l, { size: 16, characterSpacing: 30, color: GREY }), { alignment: AlignmentType.CENTER, spacing: { after: 120 } })));
  }
  main.push(spacer(500, i !== 0));
  main.push(P(r(String(w.num), { size: 60, bold: true, color: ACCENT }),
    { spacing: { before: 900, after: 0 }, keepNext: true }));
  main.push(P(r('WEAPON', { size: 16, bold: true, color: GREY, characterSpacing: 160 }), { spacing: { before: 0, after: 120 }, keepNext: true }));
  main.push(P(r(w.title_tc, { size: 34, bold: true }), { spacing: { after: 300 }, keepNext: true,
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: ACCENT, space: 10 } } }));
  w.lines.forEach(l => main.push(bodyLine(l)));
  const rb = REB[w.num];
  if (rb) {
    main.push(spacer(500));
    main.push(P(r(`WEAPON ${w.num} · ${w.title_tc.toUpperCase()}`, { size: 14, color: GREY, characterSpacing: 60 }), { spacing: { after: 60 }, keepNext: true }));
    main.push(P(r('THE REBUTTAL', { size: 30, bold: true, color: ACCENT, characterSpacing: 40 }),
      { spacing: { after: 300 }, keepNext: true, border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: ACCENT, space: 10 } } }));
    main.push(P([r('CLIENT  ', { size: 15, bold: true, color: GREY, characterSpacing: 80 }), r(rb.client, { size: 22, italics: true, color: '444444' })],
      { spacing: { after: 200, line: 300 }, keepNext: true }));
    rb.paras.forEach((t, k) => {
      const parts = t.split(/(\[pause[^\]]*\])/);
      const runs = (k === 0 ? [r('Say: ', { bold: true, color: ACCENT, size: 22 })] : []).concat(parts.filter(Boolean).map(x => x.startsWith('[pause') ?
        r(x.replace(/^\[/, '(').replace(/\]$/, ')'), { size: 18, italics: true, color: GREY }) : r(x, { size: 22 })));
      main.push(P(runs, { spacing: { after: 160, line: 312 }, indent: { left: 200 },
        border: { left: { style: BorderStyle.SINGLE, size: 12, color: ACCENT, space: 10 } } }));
    });
  }
});
// Final word
const closing = PILOT ? [] : S.closing;
if (!PILOT) main.push(spacer(2400));
if (!PILOT) main.push(P(r('FINAL WORD', { size: 17, bold: true, color: ACCENT, characterSpacing: 140 }),
  { alignment: AlignmentType.CENTER, spacing: { before: 2600, after: 480 } }));
closing.forEach(l => {
  const strong = l.startsWith('Mission Psycho');
  main.push(P(r(l, { size: strong ? 26 : 23, bold: strong, italics: !strong, color: strong ? ACCENT : INK }),
    { alignment: AlignmentType.CENTER, spacing: { before: strong ? 240 : 0, after: strong ? 240 : 140, line: 300 } }));
});

const header = new Header({ children: [P(r('THE PSYCHO SELLER DOCTRINE', { size: 14, color: GREY, characterSpacing: 120 }), { alignment: AlignmentType.CENTER })] });
const footer = new Footer({ children: [P(new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 18, color: GREY }), { alignment: AlignmentType.CENTER })] });

const doc = new Document({
  title: 'The Psycho Seller Doctrine', creator: 'Mission Zerø to 9',
  styles: { default: { document: { run: { font: FONT, size: 22, color: INK } } } },
  sections: [
    { properties: { page: PAGE }, children: front },
    { properties: { page: { ...PAGE, pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL } }, type: SectionType.NEXT_PAGE },
      headers: { default: header }, footers: { default: footer }, children: main },
  ],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('ok', OUT, 'interludePage', interludePage, 'lastWeaponPage', pageOf[W.length - 1]); });

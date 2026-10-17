# Expanded Edition — Change Report

**Files:** `RZ-expanded.docx`, `RZ-expanded.pdf` (6×9 in, 379 pages).
**Source of every rebuttal:** `expansion/rebuttals-*.md`. Rebuild with `python3 build/build_full.py out/` and check with `python3 build/qa.py out/`.
**Cleaned edition, unchanged:** branch `cleaned-edition` and `RZ.docx` / `RZ.pdf` in this branch.

## What changed

- Every weapon with a spoken line (**176 of 194**) now has a full **Rebuttal** page facing its doctrine page: the client's words, then the complete spoken response, opening with **Say:**.
- The doctrine text of all 194 weapons is **unchanged**: same lines, titles and numbering. No weapon was deleted, merged or renamed.
- Contents and page numbers were regenerated from the rendered PDF (two-pass build, verified stable).
- Title page now reads "194 Weapons · Expanded Edition".

## Quality assurance

| Check | Result |
|---|---|
| Weapons present, numbered 1–194 in order | 194 ✓ |
| Weapons with a spoken line | 176 |
| Rebuttals written | 176 — none missing, none extra ✓ |
| Rebuttals found intact in the PDF | all ✓ |
| Rebuttals spilling past their page | 0 ✓ |
| Contents page numbers matching the PDF | all 194 ✓ |
| Rebuttal length (words) | min 78, median 144, max 185 |
| Endings | 166 close on a direct question, 10 on a decisive statement |
| Sentences repeated across rebuttals | only "You've already decided." (3×, the original Say line of Weapons 65, 67, 90) |

## Weapons without a rebuttal (no spoken line in the original)

1 The Fireline of Origin, 2 The Reason for War, 3 The Vibration Structure, 4 The Final Push, 5 The First Strike, 6 The Entry Trigger, 7 The Breath of Confidence, 8 The Focus Lock, 9 The 3-Second Kill Zone, 16 The Noise Shield, 17 The Silence Slab, 23 The Priceless Void, 29 The Presence Grip, 113 The Unholy Pause, 123 The Absence Close, 124 The Systemic Strike, 175 The Sound of Battle, 189 The Grave of Sound. These are doctrine about voice, silence or presence, and are left as written.

## Openings that adjust the original line

The brief ruled out invented urgency, guarantees and exploiting insecurity. Where an original Say line would break that if spoken as written, the rebuttal opens with an honest version, or uses the original line and then corrects it in the next sentence. The original line still appears unchanged on the doctrine page. Affected: 13, 84, 100, 120, 125, 129, 133, 135, 140, 141, 144, 146, 148, 154, 155, 157, 158, 162, 164, 165, 168, 169, 170, 172, 173, 174, 176, 178, 182, 183, 184, 187, 188, 190, 192, 193, 194.

Examples: 36 ("the price increases" → "the price changes"), 110 ("the last door before you lose access" → you can almost certainly join later), 155 (crude line replaced), 157 ("a wound talking" → "a feeling talking"), 159 (mortality used to raise nomination and insurance, not as pressure).

## Placeholders to fill before publishing

Rebuttals use `[Firm]`, `[regulator]`, `[registration no.]`, `[product]`, fee, funding-channel and withdrawal placeholders wherever a real fact is needed. They show in the PDF as bracketed text. Weapon 149 needs a true personal loss story, and Weapon 169 needs an honest yes or no.

## Unresolved, for your decision

- **Duplicate titles kept** (not renamed, since renaming wasn't strictly necessary): Final Push 4/65, Pressure of Decision 31/66, Final Judgment 56/73, Invisible Contract 69/81.
- **Doctrine lines that conflict with the brief's standard**, unchanged and listed in `expansion/01-audit.md` (for example "Find their financial insecurity and twist it", "insider leak", "seal the deal mid-collapse").
- **Weapon 142 (The Void Close)** is 78 words on purpose: the weapon is a closing silence.

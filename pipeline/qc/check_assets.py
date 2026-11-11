"""Check a video's asset register (templates/asset_register.md format).

usage: python3 pipeline/qc/check_assets.py ASSET_REGISTER.md [--root DIR] [--out DIR]

For every row: source and licence filled (RS-07), native size known, on-screen scale <= 1.0 (LAY-05),
AI or composite rows labelled (ART-02), files that are named actually exist under --root, and sounds
are in sfx/catalog.json (SD-04). Whether a licence is actually correct is a human check.
"""
import argparse, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import Report, PASS, FAIL, REVIEW, NP, REPO, md_tables

AUDIO = ('.wav', '.mp3', '.m4a', '.flac', '.ogg')


def col(row, *names):
    for k, v in row.items():
        if any(n in k.lower() for n in names): return v.strip()
    return ''


def size(s):
    m = re.search(r'(\d{2,5})\s*[x×]\s*(\d{2,5})', s)
    return (int(m.group(1)), int(m.group(2))) if m else None


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('register'); ap.add_argument('--root'); ap.add_argument('--out')
    a = ap.parse_args(argv)
    R = Report('check_assets', a.register)
    if not os.path.exists(a.register):
        R.add('asset register', NP, 'no asset register for this video; assets must be checked by hand', 'ART-08'); return R.finish(a.out)
    tabs = [t for t in md_tables(open(a.register).read()) if any('licence' in h.lower() or 'license' in h.lower() for h in t[0])]
    rows = [r for t in tabs for r in t[1] if any(v.strip() for v in r.values())]
    if not rows:
        R.add('asset rows', NP, 'register has no filled asset table', 'ART-08'); return R.finish(a.out)
    cat = json.load(open(os.path.join(REPO, 'sfx', 'catalog.json')))
    sfx_files = set(os.listdir(os.path.join(REPO, 'sfx')))
    bad_src, bad_scale, unk_scale, unlabelled, missing, uncat = [], [], [], [], [], []
    for r in rows:
        aid = col(r, 'id') or col(r, 'asset')
        name = col(r, 'asset'); src = col(r, 'source'); lic = col(r, 'licence', 'license')
        if not src or not lic: bad_src.append(aid)
        nat, show = size(col(r, 'native')), size(col(r, 'largest', 'on-screen'))
        if name.lower().endswith(AUDIO) or aid.upper().startswith('SFX'):
            stem = os.path.splitext(os.path.basename(name))[0]
            if stem not in cat: (uncat if os.path.basename(name) in sfx_files else missing).append(name)
            continue
        if nat and show:
            sc = max(show[0] / nat[0], show[1] / nat[1])
            if sc > 1.0 + 1e-6: bad_scale.append(f'{aid} {sc:.2f}x')
        else: unk_scale.append(aid)
        lab = col(r, 'label')
        if re.search(r'\bAI\b|generated|gemini|chatgpt|composite|reconstruct', ' '.join(r.values()), re.I) and not lab: unlabelled.append(aid)
        if a.root and name and re.search(r'\.(png|jpe?g|webp|tif+|mp4|mov)$', name, re.I) and not os.path.exists(os.path.join(a.root, name)):
            missing.append(name)
    R.add('source and licence recorded', FAIL if bad_src else PASS, f'missing for: {bad_src}' if bad_src else f'{len(rows)} rows', 'RS-07')
    R.add('image scale <= 1.0 (no enlargement)', FAIL if bad_scale else PASS, f'enlarged: {bad_scale}' if bad_scale else 'none enlarged', 'LAY-05')
    if unk_scale: R.add('scale known for every image', REVIEW, f'native or on-screen size missing for: {unk_scale}', 'LAY-05')
    R.add('AI and composite images labelled', REVIEW if unlabelled else PASS, f'no label for: {unlabelled}' if unlabelled else 'ok', 'ART-02')
    if a.root or missing: R.add('named files exist', FAIL if missing else PASS, f'missing: {missing}' if missing else 'all found', 'ART-08')
    if uncat: R.add('sounds in catalog', REVIEW, f'in sfx/ but not catalogued: {uncat}', 'SD-04')
    R.add('licences are actually correct', NP, 'human check of each source page', 'RS-07')
    R.coverage = dict(rows=len(rows))
    return R.finish(a.out)


if __name__ == '__main__':
    sys.exit(main())

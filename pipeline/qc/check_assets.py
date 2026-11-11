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


class SoundCatalog:
    """sfx/catalog.json lookups by catalog key or by the catalogued file path (e.g. amb/village.mp3)"""
    def __init__(self, path, root):
        self.root = root; c = json.load(open(path))
        self.entries = {k: v for k, v in c.items() if isinstance(v, dict) and 'file' in v}
        self.keys = set(self.entries); self.files = {k: v['file'] for k, v in self.entries.items()}
        self.by_path = {os.path.normpath(v): k for k, v in self.files.items()}

    def physical(self, key):
        """the file on disk for a catalog key: the catalogued path, or the same name stored flat in sfx/
        (older entries record 'lib/<name>' from the folder the library was built in)"""
        f = self.files[key]
        for c in (os.path.join(self.root, f), os.path.join(self.root, os.path.basename(f))):
            if os.path.exists(c): return c
        return None

    def resolve(self, name):
        n = os.path.normpath(name.strip().strip('`'))
        if n.startswith('sfx' + os.sep): n = n[4:]
        key = n if n in self.entries else self.by_path.get(n)
        if key is None and os.sep not in n:   # a bare file name: match a flat-stored catalogued file
            hits = [k for p, k in self.by_path.items() if os.path.basename(p) == n]
            if len(hits) == 1: key = hits[0]
        if key is None:
            return ('review', 'file exists in sfx/ but is not catalogued') if os.path.exists(os.path.join(self.root, n)) \
                else ('fail', 'not in the catalog and no such file in sfx/')
        e = self.entries[key]
        if self.physical(key) is None: return 'fail', f'catalog entry {key} points at a missing file {e["file"]}'
        if e.get('approved_for_new_work') is False: return 'fail', f'{key}: provenance {e.get("licence_status", "UNKNOWN")}, not cleared for new work'
        return 'ok', key


def catalog_integrity(R, SC):
    gone = [f'{k} -> {v}' for k in SC.files if SC.physical(k) is None for v in [SC.files[k]]]
    stale = [k for k in SC.files if SC.physical(k) and not os.path.exists(os.path.join(SC.root, SC.files[k]))]
    if stale: R.add('catalog paths match the repository layout', REVIEW, f'{len(stale)} entries record a path that only exists flat in sfx/ (e.g. {SC.files[stale[0]]})', 'SD-04')
    R.add('catalog integrity (every entry has its file)', FAIL if gone else PASS, gone or f'{len(SC.files)} entries', 'SD-04')


def col(row, *names):
    for k, v in row.items():
        if any(n in k.lower() for n in names): return v.strip()
    return ''


def size(s):
    m = re.search(r'(\d{2,5})\s*[x×]\s*(\d{2,5})', s)
    return (int(m.group(1)), int(m.group(2))) if m else None


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('register'); ap.add_argument('--root'); ap.add_argument('--out')
    ap.add_argument('--catalog', default=os.path.join(REPO, 'sfx', 'catalog.json')); ap.add_argument('--sfx-root', default=os.path.join(REPO, 'sfx'))
    ap.add_argument('--catalog-integrity', action='store_true', help='also check that every catalog entry points at an existing file')
    a = ap.parse_args(argv)
    R = Report('check_assets', a.register)
    SC = SoundCatalog(a.catalog, a.sfx_root)
    if a.catalog_integrity: catalog_integrity(R, SC)
    if not os.path.exists(a.register):
        R.add('asset register', NP, 'no asset register for this video; assets must be checked by hand', 'ART-08'); return R.finish(a.out)
    tabs = [t for t in md_tables(open(a.register).read()) if any('licence' in h.lower() or 'license' in h.lower() for h in t[0])]
    rows = [r for t in tabs for r in t[1] if any(v.strip() for v in r.values())]
    if not rows:
        R.add('asset rows', NP, 'register has no filled asset table', 'ART-08'); return R.finish(a.out)
    bad_src, bad_scale, unk_scale, unlabelled, missing, uncat = [], [], [], [], [], []
    snd_ok, snd_fail, snd_review = [], [], []
    for r in rows:
        aid = col(r, 'id') or col(r, 'asset')
        name = col(r, 'asset'); src = col(r, 'source'); lic = col(r, 'licence', 'license')
        if not src or not lic: bad_src.append(aid)
        nat, show = size(col(r, 'native')), size(col(r, 'largest', 'on-screen'))
        if name.lower().endswith(AUDIO) or aid.upper().startswith('SFX') or name in SC.keys:
            st, why = SC.resolve(name)
            {'ok': snd_ok, 'fail': snd_fail, 'review': snd_review}[st].append(f'{name}: {why}')
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
    if snd_ok or snd_fail or snd_review:
        R.add('sounds: catalogued, file present, cleared for new work', FAIL if snd_fail else (REVIEW if snd_review else PASS),
              '; '.join(snd_fail + snd_review) if (snd_fail or snd_review) else f'{len(snd_ok)} sounds', 'SD-04')
    R.add('licences are actually correct', NP, 'human check of each source page', 'RS-07')
    R.coverage = dict(rows=len(rows))
    return R.finish(a.out)


if __name__ == '__main__':
    sys.exit(main())

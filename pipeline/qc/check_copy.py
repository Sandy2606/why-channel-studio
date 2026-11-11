"""Check a post-copy Markdown file against platform limits and publishing rules.

usage: python3 pipeline/qc/check_copy.py POST_COPY.md [--out DIR]

Expected layout (as in the existing post-copy files): sections headed "## ENGLISH · YouTube ...",
"## TELUGU · Instagram ..." etc., with bold labels **Title**, **Description**, **Tags** (YouTube)
and **Caption** (Instagram). Limits come from platform_rules.md (PLT-02 to PLT-05).
Rules: PUB-01 to PUB-05, PLT-02 to PLT-05, PLT-09.
"""
import argparse, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import Report, PASS, FAIL, REVIEW, NP

LIMITS = dict(ig_caption=2200, ig_hashtags=5, yt_title=100, yt_tags=500)
BRAND = {'ENGLISH': '#whyeveryquestionhasastory', 'TELUGU': '#whytelugu'}
HASHTAG = re.compile(r'(?<![\w&])#[^\s#.,;:!?()\[\]"]+')


def blocks(section):
    """split a section into {label: text} using bold-only label lines"""
    out, cur = {}, None
    for line in section.splitlines():
        m = re.fullmatch(r'\*\*([A-Za-z][A-Za-z ()]*)\*\*\s*', line.strip())
        if m: cur = m.group(1).strip().lower(); out[cur] = []; continue
        if cur is not None:
            if line.strip() == '---': cur = None; continue
            out[cur].append(line)
    return {k: '\n'.join(v).strip() for k, v in out.items()}


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('copy'); ap.add_argument('--out')
    a = ap.parse_args(argv)
    R = Report('check_copy', a.copy)
    text = open(a.copy).read()
    secs = re.split(r'^## ', text, flags=re.M)
    seen = 0
    for s in secs[1:]:
        head = s.splitlines()[0]; body = s[len(head):]
        lang = 'ENGLISH' if 'ENGLISH' in head.upper() else 'TELUGU' if 'TELUGU' in head.upper() else None
        plat = 'YT' if 'YOUTUBE' in head.upper() else 'IG' if 'INSTAGRAM' in head.upper() else None
        if not lang or not plat: continue
        seen += 1; b = blocks(body); tag = f'{lang.title()} {plat}'
        if plat == 'YT':
            t = b.get('title')
            if t is None: R.add(f'{tag} title', FAIL, 'no **Title** block', 'PUB-01')
            else: R.add(f'{tag} title length', PASS if len(t) <= LIMITS['yt_title'] else FAIL, f'{len(t)} characters (limit {LIMITS["yt_title"]})', 'PLT-05')
            tg = b.get('tags')
            if tg is None: R.add(f'{tag} tags', REVIEW, 'no **Tags** block', 'PUB-01')
            else: R.add(f'{tag} tags length', PASS if len(tg) <= LIMITS['yt_tags'] else FAIL, f'{len(tg)} characters (limit {LIMITS["yt_tags"]}; a ceiling, not a target)', 'PLT-04')
            d = b.get('description', '')
            miss = [w for w in ('SOURCES', 'CREDITS') if w not in d.upper()]
            R.add(f'{tag} description has sources and credits', PASS if not miss else (FAIL if 'SOURCES' in miss else REVIEW),
                  'present' if not miss else f'missing: {", ".join(miss)}', 'PUB-01')
            hs = HASHTAG.findall(d)
        else:
            c = b.get('caption')
            if c is None: R.add(f'{tag} caption', FAIL, 'no **Caption** block', 'PUB-01'); continue
            n16 = len(c.encode('utf-16-le')) // 2
            R.add(f'{tag} caption length', PASS if len(c) <= LIMITS['ig_caption'] else FAIL,
                  f'{len(c)} characters ({n16} UTF-16 units; limit {LIMITS["ig_caption"]})', 'PLT-03')
            hs = HASHTAG.findall(c)
            R.add(f'{tag} hashtags', PASS if len(hs) <= LIMITS['ig_hashtags'] else FAIL, f'{len(hs)} (limit {LIMITS["ig_hashtags"]})', 'PLT-02')
        brand = BRAND[lang]
        R.add(f'{tag} brand hashtag', PASS if any(h.lower() == brand for h in hs) else REVIEW,
              f'{brand} present' if any(h.lower() == brand for h in hs) else f'{brand} not found (preferred, PUB-03)', 'PUB-03')
    if not seen: R.add('copy sections', FAIL, 'no "## ENGLISH/TELUGU · YouTube/Instagram" sections found', 'PUB-01')
    disc = re.search(r'altered or synthetic content[^\n]*', text, re.I)
    R.add('disclosure decision recorded', PASS if disc else FAIL, disc.group(0)[:160] if disc else 'no "Altered or synthetic content" decision in the file', 'PUB-05')
    ver = re.search(r'(verified|checked)[^\n]{0,60}20\d\d-\d\d-\d\d', text, re.I)
    R.add('platform limits verification date', PASS if ver else FAIL, ver.group(0)[:120] if ver else 'no "verified/checked YYYY-MM-DD" line for the limits used', 'PUB-02')
    R.add('claims match the video; tone; Telugu naturalness', NP, 'human review', 'PUB-07')
    R.coverage = dict(sections=seen)
    return R.finish(a.out)


if __name__ == '__main__':
    sys.exit(main())

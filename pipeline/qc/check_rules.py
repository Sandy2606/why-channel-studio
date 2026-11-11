"""Documentation lint for the rule system (the Phase 2A acceptance checks, made permanent).

usage: python3 pipeline/qc/check_rules.py [--root REPO] [--out DIR]

1 every rule ID is defined exactly once and listed in the master's index ranges
2 every cited rule ID exists
3 no retired wording (retired_phrases.txt) outside the record files
4 history.md is never in the load list and carries its "not instructions" banner; templates define no rules
5 MIGRATION.md maps every old playbook line exactly once and points only at existing IDs
Known benign hits can be listed in retired_allow.txt as "path:line" entries.
"""
import argparse, collections, glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import Report, PASS, FAIL, REVIEW, NP, REPO

PFX = 'WF|FMT|CR|BR|LAY|RS|ST|DIR|ART|MO|MU|SD|ED|QC|PUB|PLT|AN|GS'
DEF = re.compile(r'\*\*\[((?:%s)-\d+)\]\*\*' % PFX)
REF = re.compile(r'\b((?:%s)-\d+)\b' % PFX)


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('--root', default=REPO); ap.add_argument('--out')
    ap.add_argument('--old-lines', type=int, default=396)
    a = ap.parse_args(argv); root = a.root; j = lambda *p: os.path.join(root, *p)
    R = Report('check_rules', root)
    rulefiles = [j('playbook/why-channel-video-SKILL.md'), j('playbook/brand.md'), j('playbook/platform_rules.md')] + \
        sorted(glob.glob(j('plans/*.md'))) + sorted(glob.glob(j('playbook/roles/*.md')))
    loaded = rulefiles + sorted(glob.glob(j('playbook/templates/*.md'))) + sorted(glob.glob(j('playbook/methods/*.md'))) + [j('CLAUDE.md'), j('README.md')]
    defs = collections.defaultdict(list)
    for f in rulefiles:
        for m in DEF.finditer(open(f).read()): defs[m.group(1)].append(os.path.relpath(f, root))
    master = open(j('playbook/why-channel-video-SKILL.md')).read()
    exp = set()
    for p, n1, n2 in re.findall(r'\|\s*((?:%s))-(\d+) – (?:%s)-(\d+)\s*\|' % (PFX, PFX), master):
        exp |= {f'{p}-{i:02d}' for i in range(int(n1), int(n2) + 1)}
    dup = {k: v for k, v in defs.items() if len(v) > 1}
    probs = []
    if dup: probs.append(f'defined more than once: {dup}')
    if exp - set(defs): probs.append(f'in index but not defined: {sorted(exp - set(defs))}')
    if set(defs) - exp: probs.append(f'defined but not in index: {sorted(set(defs) - exp)}')
    R.add('one owner per rule; index complete', FAIL if probs else PASS, '; '.join(probs) if probs else f'{len(defs)} rules', 'master')
    bad, n = collections.defaultdict(set), 0
    for f in loaded:
        if not os.path.exists(f): continue
        for m in REF.finditer(DEF.sub('', open(f).read())):
            n += 1
            if m.group(1) not in defs: bad[os.path.relpath(f, root)].add(m.group(1))
    R.add('citations resolve', FAIL if bad else PASS, dict(bad) if bad else f'{n} citations in {len(loaded)} files', 'master')
    pats = [l.rstrip('\n') for l in open(os.path.join(os.path.dirname(__file__), 'retired_phrases.txt')) if l.strip() and not l.startswith('#')]
    allow_f = os.path.join(os.path.dirname(__file__), 'retired_allow.txt')
    allow = set(l.split('#')[0].strip() for l in open(allow_f)) if os.path.exists(allow_f) else set()
    g = subprocess.run(['git', '-C', root, 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
    if g.returncode == 0 and os.path.realpath(g.stdout.strip()) == os.path.realpath(root):
        files = subprocess.run(['git', '-C', root, 'ls-files', '*.md'], capture_output=True, text=True).stdout.split()
        files += subprocess.run(['git', '-C', root, 'ls-files', '--others', '--exclude-standard', '*.md'], capture_output=True, text=True).stdout.split()
    else:  # not a git checkout (e.g. a test copy): walk the tree
        files = [os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs if f.endswith('.md')]
    scope = [f for f in sorted(set(files)) if not f.startswith('videos/') and not f.startswith('playbook/reports/')
             and f not in ('playbook/history.md', 'playbook/MIGRATION.md')]
    hits = []
    for f in scope:
        for i, l in enumerate(open(j(f)).read().splitlines(), 1):
            for p in pats:
                if re.search(p, l) and f'{f}:{i}' not in allow: hits.append(f'{f}:{i} [{p}]')
    R.add('no retired wording outside the record files', FAIL if hits else PASS,
          hits[:10] if hits else f'{len(pats)} phrases, {len(scope)} files', 'master (replace, don\'t append)')
    cl = open(j('CLAUDE.md')).read(); hist = open(j('playbook/history.md')).read()
    tdefs = [os.path.basename(f) for f in glob.glob(j('playbook/templates/*.md')) if DEF.search(open(f).read())]
    ok = ('Never load `playbook/history.md` as instructions' in cl and 'Never load `history.md` as instructions' in master
          and hist.startswith('# History (record only') and not tdefs)
    R.add('history never loaded; templates hold no rules', PASS if ok else FAIL, 'ok' if ok else f'templates defining rules: {tdefs}', 'master')
    mig = open(j('playbook/MIGRATION.md')).read()
    rows = re.findall(r'^\| (\d+) \| (\w+) \| ([^|]*) \|', mig, re.M)
    c = collections.Counter(int(r[0]) for r in rows)
    tids = set(REF.findall(' '.join(r[2] for r in rows))) - set(defs)
    okm = all(c[i] == 1 for i in range(1, a.old_lines + 1)) and len(c) == a.old_lines and not tids
    R.add('migration record complete', PASS if okm else FAIL, f'{len(rows)} rows' + (f'; unknown targets {tids}' if tids else ''), 'MIGRATION.md')
    try:
        from common import platform_limits
        cfg = platform_limits(j('playbook/platform_rules.md'))
        refs = {v['rule'] for v in cfg['limits'].values()}
        okc = refs <= set(defs) and all({'value', 'rule', 'status', 'source', 'checked'} <= set(v) for v in cfg['limits'].values())
        R.add('machine-readable platform limits parse and cite existing rules', PASS if okc else FAIL,
              f"{len(cfg['limits'])} limits" if okc else f'unknown rules {sorted(refs - set(defs))} or missing fields', 'PLT')
    except Exception as e:
        R.add('machine-readable platform limits parse and cite existing rules', FAIL, str(e)[:200], 'PLT')
    R.coverage = dict(rules=len(defs), files_scanned=len(scope))
    return R.finish(a.out)


if __name__ == '__main__':
    sys.exit(main())

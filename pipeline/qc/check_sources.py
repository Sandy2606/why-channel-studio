"""Check that every claim marked in a script has a source-register entry.

usage: python3 pipeline/qc/check_sources.py SCRIPT.md --brief PRODUCTION_BRIEF.md [--out DIR]

Convention (templates/production_brief.md): mark claims in the script as [C1], [C2]...; the brief's
source register has an ID column with the same IDs, plus source and date checked.
This verifies that a register entry exists and is filled. Whether the source supports the claim is
a human check (researcher, then the user). Rules: RS-01, RS-02.
"""
import argparse, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import Report, PASS, FAIL, REVIEW, NP, md_tables


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('script'); ap.add_argument('--brief'); ap.add_argument('--out')
    a = ap.parse_args(argv)
    R = Report('check_sources', a.script)
    marks = sorted(set(re.findall(r'\[(C\d+)\]', open(a.script).read())), key=lambda x: int(x[1:]))
    if not marks:
        R.add('claim markers', NP, 'script has no [C#] claim markers; sources must be checked by hand', 'RS-02')
        return R.finish(a.out)
    reg = {}
    if a.brief and os.path.exists(a.brief):
        for hdr, rows in md_tables(open(a.brief).read()):
            if any(h.strip().lower() == 'id' for h in hdr) and any('source' in h.lower() for h in hdr):
                for r in rows:
                    rid = next((v for k, v in r.items() if k.strip().lower() == 'id'), '').strip()
                    if rid: reg[rid] = r
    if not reg:
        R.add('source register', FAIL, 'no register table with ID and Source columns in the brief', 'RS-02'); return R.finish(a.out)
    missing = [m for m in marks if m not in reg]
    empty = [m for m in marks if m in reg and not all(next((v for k, v in reg[m].items() if key in k.lower()), '').strip() for key in ('source', 'date'))]
    unused = [k for k in reg if k not in marks]
    R.add('every marked claim has a register entry', FAIL if missing else PASS, f'no entry: {missing}' if missing else f'{len(marks)} claims', 'RS-02')
    R.add('entries have a source and a check date', FAIL if empty else PASS, f'incomplete: {empty}' if empty else 'ok', 'RS-01')
    if unused: R.add('register entries not used in the script', REVIEW, str(unused), 'RS-02')
    R.add('sources actually support the claims', NP, 'human check', 'RS-01')
    R.coverage = dict(claims=len(marks), register_entries=len(reg))
    return R.finish(a.out)


if __name__ == '__main__':
    sys.exit(main())

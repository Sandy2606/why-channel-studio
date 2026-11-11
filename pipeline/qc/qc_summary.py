"""Combine the automated QC reports with the human review sign-off into one honest QC summary.

usage: python3 pipeline/qc/qc_summary.py QC_DIR --type short|long --signoff qc_signoff.md [--out QC_SUMMARY.md]
       [--manifest manifest.json]   (another production type: must include a "justification")

QC_DIR is searched recursively for the <tool>.json files the checkers write.
- An automated NOT PERFORMED item stays NOT PERFORMED; it is only "covered" when the matching human check
  (templates/qc_signoff.md) is signed PASS with a reviewer and a date.
- A human row without a reviewer or a date does not count, whatever it says.
- Required reports (MANIFEST below, per production type) and every human row H1-H13 must be present. A missing
  report or row keeps the result INCOMPLETE; a fully signed form never compensates for missing automated reports.
  A human row may be N/A only with a reviewer, a date and a written reason (format-specific applicability).
- Overall: FAIL if any automated or human check failed; INCOMPLETE while anything is outstanding or missing;
  PASS only when every automated check passed or is covered by a signed human check, and every human row is signed PASS.
"""
import argparse, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import md_tables

# required automated reports per production type: tool -> list of target tokens (one report per token),
# or an integer = number of distinct reports needed
MANIFEST = {
    'short': dict(qc_video=['EN_YT', 'EN_IG', 'TE_YT', 'TE_IG'], qc_layout=2, check_exports=1, check_copy=1, check_assets=1, check_sources=1),
    'long':  dict(qc_video=['EN', 'TE'], qc_layout=2, check_exports=1, check_copy=1, check_assets=1, check_sources=1),
}
REQUIRED_ROWS = [f'H{i}' for i in range(1, 14)]

# which human check covers which automated NOT PERFORMED / REVIEW item (matched on the check name)
COVER = [
    ('professional visual QC', 'H1'), ('font and colour', 'H3'), ('unregistered elements', 'H3'),
    ('frames with no registered text', 'H3'), ('claims match the video', 'H12'), ('sources actually support', 'H5'),
    ('claim markers', 'H5'), ('licences are actually correct', 'H11'), ('asset register', 'H11'), ('asset rows', 'H11'),
]


def human_rows(path):
    rows = {}
    if not path or not os.path.exists(path): return rows
    for hdr, rs in md_tables(open(path).read()):
        if 'ID' not in hdr: continue
        for r in rs:
            hid = r.get('ID', '').strip()
            if not hid: continue
            res = r.get('Result (PASS / FAIL / NOT DONE)', r.get('Result', '')).strip().upper().replace('N/A', 'NA')
            who, when, notes = r.get('Reviewer', '').strip(), r.get('Date', '').strip(), r.get('Notes / evidence', '').strip()
            valid = res in ('PASS', 'FAIL', 'NA') and who and re.fullmatch(r'20\d\d-\d\d-\d\d', when) and (res != 'NA' or notes)
            rows[hid] = dict(check=r.get('Human check', ''), result=(res if res != 'NA' else 'N/A') if valid else 'NOT DONE', reviewer=who, date=when,
                             notes=notes, invalid=(res in ('PASS', 'FAIL', 'NA') and not valid))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('qc_dir'); ap.add_argument('--signoff'); ap.add_argument('--out')
    ap.add_argument('--type', choices=list(MANIFEST)); ap.add_argument('--manifest')
    a = ap.parse_args(argv)
    missing = []
    if a.manifest:
        m = json.load(open(a.manifest))
        if not str(m.get('justification', '')).strip(): missing.append('custom manifest has no justification'); man = None
        else: man = m['required']
    elif a.type: man = MANIFEST[a.type]
    else: man = None; missing.append('production type not given (--type short|long); required reports cannot be verified')
    reports = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(a.qc_dir, '**', '*.json'), recursive=True))
               if os.path.basename(p)[:-5] in ('qc_video', 'qc_layout', 'check_exports', 'check_copy', 'check_assets', 'check_sources', 'check_rules')]
    H = human_rows(a.signoff)
    if man:
        for tool, need in man.items():
            got = [str(r['target']) for r in reports if r['tool'] == tool]
            if isinstance(need, list):
                for tok in need:
                    if not any(re.search(rf'(?<![A-Za-z]){tok}(?![A-Za-z])', os.path.basename(g)) for g in got):
                        missing.append(f'{tool} report for {tok}')
            elif len(set(got)) < need: missing.append(f'{tool}: {len(set(got))} of {need} reports')
    for hid in REQUIRED_ROWS:
        if a.signoff and os.path.exists(a.signoff) and hid not in H: missing.append(f'human row {hid} absent from the sign-off form')
    auto_fail, outstanding, covered, review_items = [], [], [], []
    lines = ['# QC summary', '', '## Automated checks', '', '| Tool | Target | Overall | Not performed | Review |', '|---|---|---|---|---|']
    for r in reports:
        nps = [c['check'] for c in r['checks'] if c['status'] == 'NOT PERFORMED']
        rvs = [c['check'] for c in r['checks'] if c['status'] == 'REVIEW']
        lines.append(f"| {r['tool']} | {os.path.basename(str(r['target']))} | {r['overall']} | {len(nps)} | {len(rvs)} |")
        auto_fail += [f"{r['tool']}: {c['check']}" for c in r['checks'] if c['status'] == 'FAIL']
        for n in nps:
            hid = next((h for k, h in COVER if k in n), None)
            if hid and H.get(hid, {}).get('result') == 'PASS': covered.append(f"{r['tool']}: {n} → {hid} ({H[hid]['reviewer']}, {H[hid]['date']})")
            else: outstanding.append(f"{r['tool']}: {n}" + (f' (needs {hid})' if hid else ' (no human check maps to it)'))
        review_items += [f"{r['tool']}: {n}" for n in rvs]
    if review_items and H.get('H13', {}).get('result') != 'PASS':
        outstanding.append(f'{len(review_items)} automated REVIEW item(s) not yet resolved (H13)')
    lines += ['', '## Human review', '', '| ID | Check | Result | Reviewer | Date | Notes |', '|---|---|---|---|---|---|']
    if not H: lines.append('| — | no sign-off file | NOT DONE | | | |'); outstanding.append('no human review sign-off recorded')
    for hid, h in H.items():
        lines.append(f"| {hid} | {h['check']} | {h['result']}{' (invalid: missing reviewer or date)' if h['invalid'] else ''} | {h['reviewer']} | {h['date']} | {h['notes']} |")
        if h['result'] == 'NOT DONE': outstanding.append(f"{hid} {h['check']}")
    outstanding = missing + outstanding
    human_fail = [f"{k} {h['check']}" for k, h in H.items() if h['result'] == 'FAIL']
    overall = 'FAIL' if (auto_fail or human_fail) else ('INCOMPLETE' if outstanding else 'PASS (automated checks + signed human review)')
    lines[1:1] = ['', f'**Overall: {overall}**', '', 'Contact sheets and other inspection aids are not inspections; only signed human rows count.']
    for title, items in (('Failed', auto_fail + human_fail), ('Missing (required but absent)', missing), ('Outstanding', [o for o in outstanding if o not in missing]), ('Covered by signed human review', covered), ('Automated REVIEW items', review_items)):
        if items: lines += ['', f'## {title}', ''] + [f'- {i}' for i in items]
    text = '\n'.join(lines) + '\n'
    if a.out: open(a.out, 'w').write(text)
    print(text)
    return {'FAIL': 1, 'INCOMPLETE': 2}.get(overall.split()[0], 0)


if __name__ == '__main__':
    sys.exit(main())

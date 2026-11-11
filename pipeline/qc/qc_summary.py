"""Combine the automated QC reports with the human review sign-off into one honest QC summary.

usage: python3 pipeline/qc/qc_summary.py QC_DIR --signoff qc_signoff.md [--out QC_SUMMARY.md]

QC_DIR is searched recursively for the <tool>.json files the checkers write.
- An automated NOT PERFORMED item stays NOT PERFORMED; it is only "covered" when the matching human check
  (templates/qc_signoff.md) is signed PASS with a reviewer and a date.
- A human row without a reviewer or a date does not count, whatever it says.
- Overall: FAIL if any automated or human check failed; INCOMPLETE while anything is outstanding;
  PASS only when every automated check passed or is covered by a signed human check, and every human row is signed PASS.
"""
import argparse, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import md_tables

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
            res = r.get('Result (PASS / FAIL / NOT DONE)', r.get('Result', '')).strip().upper()
            who, when = r.get('Reviewer', '').strip(), r.get('Date', '').strip()
            valid = res in ('PASS', 'FAIL') and who and re.fullmatch(r'20\d\d-\d\d-\d\d', when)
            rows[hid] = dict(check=r.get('Human check', ''), result=res if valid else 'NOT DONE', reviewer=who, date=when,
                             notes=r.get('Notes / evidence', ''), invalid=(res in ('PASS', 'FAIL') and not valid))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(); ap.add_argument('qc_dir'); ap.add_argument('--signoff'); ap.add_argument('--out')
    a = ap.parse_args(argv)
    reports = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(a.qc_dir, '**', '*.json'), recursive=True))
               if os.path.basename(p)[:-5] in ('qc_video', 'qc_layout', 'check_exports', 'check_copy', 'check_assets', 'check_sources', 'check_rules')]
    H = human_rows(a.signoff)
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
    human_fail = [f"{k} {h['check']}" for k, h in H.items() if h['result'] == 'FAIL']
    overall = 'FAIL' if (auto_fail or human_fail) else ('INCOMPLETE' if outstanding else 'PASS (automated checks + signed human review)')
    lines[1:1] = ['', f'**Overall: {overall}**', '', 'Contact sheets and other inspection aids are not inspections; only signed human rows count.']
    for title, items in (('Failed', auto_fail + human_fail), ('Outstanding', outstanding), ('Covered by signed human review', covered), ('Automated REVIEW items', review_items)):
        if items: lines += ['', f'## {title}', ''] + [f'- {i}' for i in items]
    text = '\n'.join(lines) + '\n'
    if a.out: open(a.out, 'w').write(text)
    print(text)
    return {'FAIL': 1, 'INCOMPLETE': 2}.get(overall.split()[0], 0)


if __name__ == '__main__':
    sys.exit(main())

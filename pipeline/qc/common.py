"""Shared helpers for the Why? QC scripts (pipeline/qc).

Every check reports one of four statuses, so a report can never claim more than was inspected:
  PASS           checked, and it meets the rule
  FAIL           checked, and it breaks the rule
  REVIEW         checked, but a person must look (likely false positive, or a judgment call)
  NOT PERFORMED  could not be checked automatically (missing metadata, unregistered graphics,
                 human-only review); it must be inspected by a person

Overall verdict:
  FAIL                 if any check FAILs
  INCOMPLETE           if any check is NOT PERFORMED (never shown as a pass)
  PASS WITH REVIEW     if every check passed but some need a person to look
  PASS                 only when every check was performed and passed
"""
import json, os, subprocess, sys, datetime

PASS, FAIL, REVIEW, NP = 'PASS', 'FAIL', 'REVIEW', 'NOT PERFORMED'
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

PLATFORM_RULES = os.path.join(REPO, 'playbook', 'platform_rules.md')


def platform_limits(path=None):
    """the single machine-readable limits block in platform_rules.md (```json qc-limits)"""
    import re
    text = open(path or PLATFORM_RULES).read()
    m = re.search(r'```json qc-limits\s*\n(.*?)\n```', text, re.S)
    if not m: raise RuntimeError('platform_rules.md has no ```json qc-limits block')
    return json.loads(m.group(1))


def limit(name, path=None):
    return platform_limits(path)['limits'][name]['value']


# Format profiles (brand.md LAY-03, FMT-01, PLT-01). Regions are fractions of the frame height.
# The Short duration ceiling comes from platform_rules.md, not from this file.
PROFILES = {
    'short': dict(W=1080, H=1920, max_duration=float(limit('short_max_seconds')), top_band=(0.057, 0.130), caption_band=(0.708, 0.802), phone_w=390),
    'long':  dict(W=1920, H=1080, max_duration=None,  top_band=(0.0, 0.12),    caption_band=(0.80, 0.95),   phone_w=640),
}


class Report:
    def __init__(self, tool, target):
        self.tool, self.target, self.items, self.coverage = tool, target, [], {}

    def add(self, check, status, detail='', rule=None):
        self.items.append(dict(check=check, status=status, detail=detail, rule=rule))
        return status

    def overall(self):
        st = [i['status'] for i in self.items]
        if FAIL in st: return 'FAIL'
        if NP in st: return 'INCOMPLETE'
        if REVIEW in st: return 'PASS WITH REVIEW'
        return 'PASS' if st else 'INCOMPLETE'

    def to_dict(self):
        return dict(tool=self.tool, target=self.target, overall=self.overall(),
                    generated=datetime.datetime.now().isoformat(timespec='seconds'),
                    coverage=self.coverage, checks=self.items)

    def markdown(self):
        out = [f"## {self.tool}: {os.path.basename(str(self.target))}", '', f"**Overall: {self.overall()}**", '']
        if self.coverage:
            out += ['Coverage: ' + '; '.join(f"{k}: {v}" for k, v in self.coverage.items()), '']
        out += ['| Check | Rule | Status | Detail |', '|---|---|---|---|']
        for i in self.items:
            d = str(i['detail']).replace('|', '\\|').replace('\n', ' ')
            out.append(f"| {i['check']} | {i['rule'] or ''} | {i['status']} | {d[:400]} |")
        return '\n'.join(out) + '\n'

    def finish(self, outdir=None, quiet=False):
        if outdir:
            os.makedirs(outdir, exist_ok=True)
            json.dump(self.to_dict(), open(os.path.join(outdir, f'{self.tool}.json'), 'w'), indent=1, ensure_ascii=False)
            open(os.path.join(outdir, f'{self.tool}.md'), 'w').write(self.markdown())
        if not quiet: print(self.markdown())
        return {'FAIL': 1, 'INCOMPLETE': 2}.get(self.overall(), 0)


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', path],
                       capture_output=True, text=True)
    if r.returncode: return None
    j = json.loads(r.stdout)
    v = next((s for s in j['streams'] if s['codec_type'] == 'video'), None)
    a = next((s for s in j['streams'] if s['codec_type'] == 'audio'), None)
    fps = None
    if v and v.get('avg_frame_rate', '0/0') != '0/0':
        n, d = v['avg_frame_rate'].split('/'); fps = float(n) / float(d) if float(d) else None
    return dict(duration=float(j['format'].get('duration', 0)),
                width=v and int(v['width']), height=v and int(v['height']), fps=fps,
                vcodec=v and v['codec_name'], acodec=a and a['codec_name'],
                channels=a and a.get('channels'), sample_rate=a and a.get('sample_rate'))


def detect_format(info):
    if not info or not info['width']: return None
    if (info['width'], info['height']) == (1080, 1920): return 'short'
    if (info['width'], info['height']) == (1920, 1080): return 'long'
    return None


def frame(path, t, w, h):
    import numpy as np
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{max(0, t):.3f}', '-i', path, '-frames:v', '1',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    if len(b) < w * h * 3: return None
    return np.frombuffer(b[:w * h * 3], np.uint8).reshape(h, w, 3)


def last_frames(path, w, h, seconds=0.5, scale=4):
    """every decoded frame of the last `seconds` (downscaled by `scale`), in order; the final item is the
    actual last decoded frame of the file"""
    import numpy as np
    sw, sh = w // scale, h // scale
    b = subprocess.run(['ffmpeg', '-v', 'error', '-sseof', f'-{seconds + 0.2:.2f}', '-i', path, '-vf', f'scale={sw}:{sh}',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    n = len(b) // (sw * sh * 3)
    return [np.frombuffer(b[i * sw * sh * 3:(i + 1) * sw * sh * 3], np.uint8).reshape(sh, sw, 3) for i in range(n)]


def load_json(path, default=None):
    if not path: return default
    return json.load(open(path))


def md_tables(text):
    """parse every markdown table in text -> list of (header list, rows as dicts)"""
    tables, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        l = lines[i].strip()
        if l.startswith('|') and i + 1 < len(lines) and set(lines[i + 1].replace('|', '').strip()) <= set('-: '):
            hdr = [c.strip() for c in l.strip('|').split('|')]
            rows, i = [], i + 2
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                rows.append(dict(zip(hdr, cells + [''] * (len(hdr) - len(cells)))))
                i += 1
            tables.append((hdr, rows))
        else:
            i += 1
    return tables

"""Automated layout QC, reusing the shared registry and checks in pipeline/style_v2/layout.py (reg/check).

Two ways to supply the registered boxes:
  1) --dump layout.json   {"W":1080,"H":1920,
                            "frames": {"12.25": [{"kind","box","ink","owner","group"}, ...], ...},
                            "not_covered": [{"t0":..,"t1":..,"what":"Remotion Globe Arcs clip (text baked in)"}]}
  2) --render-script PATH --start A --end B [--step 0.25] [--dump-out layout.json]
     executes the project's render script up to `if __name__ == '__main__':`, then calls its render(t)
     for each sampled time and reads the boxes registered through layout.reg().

Coverage is reported honestly: frames sampled, components per kind, frames with no registered text,
and declared not-covered intervals (Remotion clips, text baked into images). Those are NOT PERFORMED
and need human inspection. Font and colour tokens are not recorded by layout.reg(), so that check is
NOT PERFORMED here (see README).
Rules: QC-05, LAY-02, BR-04.
"""
import argparse, collections, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import Report, PASS, FAIL, REVIEW, NP, REPO, load_json

sys.path.insert(0, os.path.join(REPO, 'pipeline', 'styles')); sys.path.insert(0, os.path.join(REPO, 'pipeline', 'style_v2'))
import layout as LY  # the shared module: one registry, one set of checks
TEXT_KINDS = ('badge', 'caption', 'credit', 'card', 'label')


def from_render_script(path, a0, a1, step):
    src = open(path).read().split("if __name__ == '__main__':")[0]
    d = os.path.dirname(os.path.abspath(path)); sys.path.insert(0, d); cwd = os.getcwd(); os.chdir(d)
    ns = {'__name__': 'qc_render', '__file__': path}; sys.argv = [path]
    exec(compile(src, path, 'exec'), ns)
    mod = sys.modules.get('layout', LY)
    frames, t = {}, a0
    while t < a1 + 1e-9:
        ns['render'](t)
        frames[f'{t:.2f}'] = [dict(e) for e in mod.LAYOUT]
        t += step
    os.chdir(cwd)
    W = ns.get('W', 1080); H = ns.get('H', 1920)
    return dict(W=W, H=H, frames=frames, not_covered=ns.get('QC_NOT_COVERED', []))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--dump'); ap.add_argument('--render-script'); ap.add_argument('--start', type=float, default=0.0)
    ap.add_argument('--end', type=float); ap.add_argument('--step', type=float, default=0.25)
    ap.add_argument('--dump-out'); ap.add_argument('--out'); ap.add_argument('--not-covered')
    ap.add_argument('--edge', type=int, default=40); ap.add_argument('--min-pad', type=int, default=8)
    a = ap.parse_args(argv)
    target = a.dump or a.render_script
    R = Report('qc_layout', target)
    if a.dump: data = load_json(a.dump)
    elif a.render_script and a.end is not None: data = from_render_script(a.render_script, a.start, a.end, a.step)
    else:
        R.add('layout data', NP, 'no --dump and no --render-script with --end given', 'QC-05'); return R.finish(a.out)
    if a.dump_out: json.dump(data, open(a.dump_out, 'w'), indent=0, ensure_ascii=False)
    W, H = data.get('W', 1080), data.get('H', 1920)
    nc = data.get('not_covered', []) + (load_json(a.not_covered, []) if a.not_covered else [])
    frames = data.get('frames', {})
    defects, kinds, empty = collections.OrderedDict(), collections.Counter(), []
    for t, boxes in frames.items():
        LY.LAYOUT.clear()
        for e in boxes:
            LY.LAYOUT.append(dict(kind=e['kind'], box=tuple(e['box']), ink=tuple(e['ink']) if e.get('ink') else None,
                                  owner=e.get('owner'), group=e.get('group')))
            kinds[e['kind']] += 1
        if not any(e['kind'] in TEXT_KINDS for e in boxes): empty.append(t)
        d = LY.check(W, H, edge=a.edge, min_pad=a.min_pad)
        if d: defects[t] = d
    R.coverage = dict(frames_sampled=len(frames), frame_size=f'{W}x{H}', registered_components=dict(kinds),
                      frames_without_registered_text=len(empty), declared_not_covered=len(nc))
    if not frames:
        R.add('registered layout', NP, 'no frames supplied', 'QC-05'); return R.finish(a.out)
    groups = collections.defaultdict(list)
    for t, d in defects.items():
        for x in d: groups[x.split("'")[0].strip() if "'" in x else x].append(t)
    if defects:
        R.add('containment, padding, edges, overlaps, badge alignment', FAIL,
              f'{len(defects)} frame(s) with defects; first: {list(defects.items())[:3]}', 'QC-05')
    else:
        R.add('containment, padding, edges, overlaps, badge alignment', PASS, f'0 defects in {len(frames)} sampled frames (registered components only)', 'QC-05')
    if empty:
        R.add('frames with no registered text', REVIEW, f'{len(empty)} frame(s), e.g. {empty[:6]}: nothing registered there, so layout was not checked; inspect visually', 'QC-05')
    if nc:
        R.add('unregistered elements (Remotion clips, text baked into images)', NP, '; '.join(f"{x.get('t0')}-{x.get('t1')} s: {x.get('what')}" for x in nc)[:400] + ' -> visual inspection required', 'QC-05')
    R.add('font and colour tokens', NP, 'layout.reg() does not record font or colour; check by eye (QC-01 items 5-6)', 'QC-01')
    if a.out:
        os.makedirs(a.out, exist_ok=True); json.dump(defects, open(os.path.join(a.out, 'layout_defects.json'), 'w'), indent=1, ensure_ascii=False)
    return R.finish(a.out)


if __name__ == '__main__':
    sys.exit(main())

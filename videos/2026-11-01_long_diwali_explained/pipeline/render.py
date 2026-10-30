"""DIWALI, EXPLAINED — long video renderer. LANGV=en|te python3 render.py [part parts] | still t1,t2,..."""
import os, sys, json, math, re, subprocess
import numpy as np, cairo
from base import *
import room as RM
import gfx1 as G1
import gfx2 as G2
sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2'); import cta_card as CT

LEAD, TAIL = 0.15, 5.5
TL = json.load(open(ROOT + f'tl_{LANG}.json')); TLE = json.load(open(ROOT + 'tl_en.json'))
ENV = np.load(ROOT + f'env_{LANG}.npy')
DUR = LEAD + TL['dur'] + TAIL
LN = {l['n']: l for l in TL['lines']}; LNE = {l['n']: l for l in TLE['lines']}
ORDER = [l['n'] for l in TL['lines']]
EV = []   # sfx events (name, time, gain)


def t0(n): return LN[n]['t0'] + LEAD
def t1(n): return LN[n]['t1'] + LEAD
def nz(w): return re.sub(r'[^\w]', '', w.lower())


def A(n, word, k=1, frac_add=0.0):
    """time of k-th occurrence of an EN word in line n (TE: number match, else EN char fraction)."""
    le = LNE[n]; target = nz(word)
    if LANG == 'en':
        j = 0
        for s, e, w in le['words']:
            if nz(w) == target or (target.isdigit() and nz(w).startswith(target)):
                j += 1
                if j == k: return s + LEAD
        raise KeyError((n, word))
    lt = LN[n]
    if target.isdigit():
        j = 0
        for s, e, w in lt['words']:
            if nz(w).startswith(target):
                j += 1
                if j == k: return s + LEAD
    # EN fraction
    txt_ = le['text']; pos = -1; j = 0; words = txt_.split(); acc = 0
    for w in words:
        if nz(w) == target:
            j += 1
            if j == k: pos = acc; break
        acc += len(w) + 1
    f = pos / max(1, len(txt_)) if pos >= 0 else 0.5
    return lt['t0'] + LEAD + (f + frac_add) * (lt['t1'] - lt['t0'])


def F(n, f): return t0(n) + f * (t1(n) - t0(n))


def qstarts(n):
    """start times of each question in a line (after each '?')."""
    ws = LN[n]['words']; out = [ws[0][0] + LEAD]
    for i, (s, e, w) in enumerate(ws[:-1]):
        if w.endswith('?'): out.append(ws[i + 1][0] + LEAD)
    return out


def sfx(name, t, g=0.5): EV.append((name, round(t, 3), g))


# ---------------- scenes ----------------
SC = []   # (start, fn)  fn(c, t) draws full frame. ROOM scenes use dict
CH_LINES = {'6': 1, '22': 2, '30': 3, '41': 4, '48': 5, '56': 6}
CHT = {1: ('WHY DOES DIWALI KEEP CHANGING ITS DATE?', 'దీపావళి తేదీ ఎందుకు మారుతుంది?'),
       2: ('WHY DOES EVERY HOME GET DEEP-CLEANED?', 'దీపావళికి ముందు ఇల్లంతా ఎందుకు శుభ్రం చేస్తాం?'),
       3: ('IS YOUR DIWALI BONUS A GIFT?', 'దీపావళి bonus బహుమతా?'),
       4: ('IS THAT "INDIA FROM SPACE" PHOTO REAL?', 'Space నుంచి India photo నిజమా?'),
       5: ('WHY DOES THE STOCK MARKET OPEN ON DIWALI?', 'దీపావళి రోజు stock market ఎందుకు open?'),
       6: ("WHY CAN'T DELHI BREATHE AFTER DIWALI?", 'దీపావళి తర్వాత Delhi కి ఊపిరి ఎందుకు ఆడదు?')}
ROOMSPEC = {}   # line -> cam


def room(n, cam=None, **kw):
    sp = LN[n]['sp']
    ROOMSPEC[n] = dict(cam=cam or ('anna' if sp == 'ANNA' else 'chelli'), **kw)
    SC.append((t0(n) - 0.08, ('room', n)))


def gfx(n, fn, start=None):
    SC.append(((start if start is not None else t0(n) - 0.08), ('gfx', fn)))


# cold open
room('1', 'two'); room('2', 'anna'); room('3', 'two'); room('4', 'two'); room('5', 'anna'); room('5b', 'two'); room('5c', 'phone')
QT = qstarts('3')
for i, q in enumerate(QT[:9]): sfx('paper_slide', q, 0.35)
sfx('footsteps_soft_indoor', 0.0, 0.5)
T_REC = A('5b', 'record'); sfx('camera_shutter', T_REC, 0.55)
# title + chapter 1 card
T_TITLE = t1('5c') + 0.25
SC.append((T_TITLE, ('gfx', lambda c, t: G1.title_slide(c, t, T_TITLE, 0))))
for i in range(9): sfx('pin_push', T_TITLE + 0.15 + i * 0.12 + 0.2, 0.25)
sfx('firework_whistle_echo', T_TITLE - 0.2, 0.10); sfx('impact_trailer', T_TITLE + 1.25, 0.5)
CHCARD = {}


def chapter(k, n):
    prev = ORDER[ORDER.index(n) - 1]
    s = t1(prev) + 0.15 if k > 1 else T_TITLE + 2.6
    CHCARD[k] = s
    SC.append((s, ('chap', k)))
    sfx('page_turn', s, 0.5); sfx('impact_big', s + 0.35, 0.45)


for n, k in CH_LINES.items(): chapter(k, n)
CH_END = {k: CHCARD[k] + (2.25 if k == 1 else 1.65) for k in CHCARD}

# chapter 1
room('6', 'two')
room('7', 'chelli', over=lambda c, t: G1.g_dates(c, t, A('7', 'october'), A('7', 'november')))
sfx('paper_drop', A('7', 'october'), 0.35); sfx('paper_drop', A('7', 'november'), 0.35)
gfx('8', lambda c, t: G1.g_sunmoon(c, t, t0('8'), A('8', 'moon'))); sfx('swoosh_slow', A('8', 'moon') - 0.3, 0.35)
room('9', 'anna')
gfx('10', lambda c, t: G1.g_moons(c, t, t0('10'), A('10', '29'), A('10', '354'))); sfx('ticker_run', A('10', '354'), 0.25)
room('11', 'chelli', over=lambda c, t: G1.g_eleven(c, t, A('11', 'eleven'))); sfx('sub_knock', A('11', 'eleven'), 0.4)
gfx('12', lambda c, t: G1.g_drift(c, t, t0('12'))); sfx('swoosh_slow', t0('12') + 0.8, 0.3)
room('13', 'chelli')
gfx('14', lambda c, t: G1.g_adhik(c, t, t0('14'), A('14', 'extra'))); sfx('paper_slide', A('14', 'extra'), 0.45)
gfx('15', lambda c, t: G1.g_watch(c, t, t0('15'), A('15', 'fix'))); sfx('tick', t0('15') + 0.2, 0.35); sfx('stamp', A('15', 'fix') + 0.2, 0.45)
gfx('16', lambda c, t: G1.g_window(c, t, t0('16'))); sfx('marker', t0('16') + 0.1, 0.3)
gfx('16b', lambda c, t: G1.g_sankranti(c, t, t0('16b')))
gfx('16c', lambda c, t: G1.g_eid(c, t, t0('16c'))); sfx('swoosh_slow', t0('16c') + 0.3, 0.25)
room('17', 'chelli')
gfx('18', lambda c, t: G1.g_amavasya(c, t, t0('18'), A('18', 'no', 1))); sfx('match_light', A('18', 'no', 1), 0.7)
SC.append((t1('18') + 0.05, ('gfx', lambda c, t: G1.g_amavasya(c, t, t0('18'), A('18', 'no', 1)))))
room('20', 'chelli')
gfx('21', lambda c, t: G1.g_2027(c, t, t0('21'), A('21', 'earlier'))); sfx('stamp', A('21', 'earlier'), 0.5)
# chapter 2
room('22', 'two', broom=True); sfx('broom_sweep', t0('22') + 0.3, 0.45)
room('23', 'anna')
gfx('24', lambda c, t: G1.g_damp(c, t, t0('24'))); sfx('rain_light_loop', t0('24'), 0.12)
gfx('25', lambda c, t: G1.g_dry(c, t, t0('25'))); sfx('swoosh_slow', t0('25') + 0.2, 0.3)
gfx('26', lambda c, t: G1.g_lime(c, t, t0('26')))
gfx('26b', lambda c, t: G1.g_split(c, t, t0('26b')))
gfx('27', lambda c, t: G1.g_ledger(c, t, t0('27'), L('OLD BOOKS CLOSE', 'పాత పుస్తకాలు మూస్తారు'), L('NEW BOOKS BEGIN', 'కొత్త పుస్తకాలు మొదలు')))
sfx('page_turn', t0('27') + 0.3, 0.4); sfx('page_turn', t0('27') + 1.2, 0.4)
room('28', 'chelli'); room('29', 'two')
# chapter 3
room('30', 'chelli')
gfx('31', lambda c, t: G1.g_giftlaw(c, t, t0('31'), A('31', 'law'))); sfx('marker', A('31', 'law') - 0.6, 0.35); sfx('stamp', A('31', 'law'), 0.6)
gfx('32', lambda c, t: (board_bg(c), big_num(c, '1965', W / 2, 260, 150, t, A('32', '1965')),
                        draw_clip(c, 'bonus_h', W / 2, 640, 1250, t, t0('32') + 0.3, rot=-1.2, src='EZYLEGAL · PAYMENT OF BONUS ACT, 1965')))
sfx('paper_slide', t0('32') + 0.3, 0.45); sfx('sub_knock', A('32', '1965'), 0.3)
CK = [A('33', '21000') if LANG == 'en' and False else A('33', '21'), A('33', '30'), A('33', '20')]
gfx('33', lambda c, t: G1.g_checklist(c, t, t0('33'), CK))
for x in CK: sfx('tick', x + 0.15, 0.45)
gfx('34', lambda c, t: G1.g_pct(c, t, t0('34'), A('34', '8'), A('34', '20'), A('34', '20') + 0.6)); sfx('sub_knock', A('34', '8'), 0.3); sfx('sub_knock', A('34', '20'), 0.3); sfx('paper_slide', A('34', '20') + 0.6, 0.4)
room('35', 'chelli')
gfx('36', lambda c, t: G1.g_tiles(c, t, t0('36'), A('36', 'one'))); sfx('impact_big', A('36', 'one') + 0.0, 0.2)
gfx('36b', lambda c, t: G1.g_formula(c, t, t0('36b'))); sfx('typing_run', t0('36b') + 0.4, 0.2)
gfx('37', lambda c, t: G1.g_months8(c, t, t0('37'))); sfx('paper_slide', t0('37') + 0.8, 0.35)
room('38', 'chelli', bags=True); sfx('paper_drop', t0('38') + 0.2, 0.3)
gfx('39', lambda c, t: G1.g_counter(c, t, t0('39'), A('39', '6'))); sfx('ticker_run', t0('39') + 0.2, 0.3); sfx('paper_slide', A('39', '6'), 0.4)
gfx('40', lambda c, t: G1.g_jobs(c, t, t0('40')))
# chapter 4
gfx('41', lambda c, t: G2.g_viral(c, t, t0('41'))); sfx('shutter', t0('41'), 0.45)
gfx('42', lambda c, t: G2.g_viral(c, t, t0('41'), tstamp=A('42', 'not'))); sfx('stamp', A('42', 'not'), 0.6)
gfx('43', lambda c, t: G2.g_viral(c, t, t0('41'), tstamp=A('42', 'not'), legend_t=t0('43')))
room('44', 'anna', tocam=True, over=lambda c, t: G2.nasa_panel(c, t, A('44', 'this'))); sfx('polaroid', A('44', 'this'), 0.45)
gfx('45', lambda c, t: G2.g_earthk(c, t, t0('45'))); sfx('paper_slide', t0('45') + 0.4, 0.4); sfx('marker', t0('45') + 1.0, 0.25)
room('46', 'chelli')
gfx('46b', lambda c, t: G2.g_compare(c, t, t0('46b'))); sfx('stamp', t0('46b') + 1.2, 0.35); sfx('stamp', t0('46b') + 2.0, 0.35)
room('47', 'anna')
# chapter 5
room('48', 'chelli')
gfx('49', lambda c, t: G2.g_ticker(c, t, t0('49'), A('49', 'muhurat'))); sfx('bell_ring', A('49', 'muhurat'), 0.35)
gfx('50', lambda c, t: G2.g_datecard(c, t, t0('50'))); sfx('paper_drop', t0('50'), 0.35); sfx('paper_slide', t0('50') + 1.0, 0.4)
gfx('51', lambda c, t: G1.g_ledger(c, t, t0('51'), L('OLD YEAR', 'పాత సంవత్సరం'), L('NEW FINANCIAL YEAR', 'కొత్త ఆర్థిక సంవత్సరం'))); sfx('page_turn', t0('51') + 0.3, 0.4)
gfx('51b', lambda c, t: G1.g_ledger(c, t, t0('51b') - 1.1, '', L('CHOPDA PUJAN', 'చోప్డా పూజన్'), symbol=True))
gfx('52', lambda c, t: G2.g_trade(c, t, t0('52'), A('52', 'first') + 0.4)); sfx('ui_click', A('52', 'first') + 0.38, 0.6); sfx('ui_pop', A('52', 'first') + 0.5, 0.4)
gfx('53', lambda c, t: G2.g_history(c, t, t0('53'), A('53', '1957'), A('53', '1992'))); sfx('tick', A('53', '1957'), 0.4); sfx('tick', A('53', '1992'), 0.4)
room('54', 'chelli', notebook=True); room('55', 'anna')
# chapter 6
room('56', 'chelli'); room('56b', 'anna', tocam=True, locked=True); room('56c', 'chelli'); room('57', 'anna')
sfx('firework_whistle_echo', t0('57') + 0.3, 0.08)
gfx('58', lambda c, t: G2.g_map(c, t, t0('58'))); sfx('map_unfold', t0('58'), 0.4)
gfx('59', lambda c, t: G2.g_lid(c, t, t0('59'))); sfx('wind_ambience', t0('59'), 0.12)
gfx('59b', lambda c, t: G2.g_mumdel(c, t, t0('59b')))
gfx('60', lambda c, t: G2.g_iit(c, t, t0('60'), A('60', '12'))); sfx('paper_slide', t0('60'), 0.4); sfx('marker', t0('60') + 0.6, 0.25)
gfx('61', lambda c, t: G2.g_sc(c, t, t0('61'))); sfx('paper_slide', t0('61'), 0.45)
room('62', 'chelli'); room('63', 'anna')
# ending
TS_B = [F('63b', f) for f in (0.10, 0.24, 0.38, 0.52, 0.66, 0.82)]
gfx('63b', lambda c, t: G2.g_board(c, t, t0('63b'), TS_B))
for x in TS_B: sfx('page_turn', x, 0.18)
room('63c', 'anna'); room('64', 'chelli', locked=True)
QL = qstarts('65')[:3]
gfx('65', lambda c, t: G2.g_locked(c, t, t0('65'), QL))
for x in QL: sfx('sub_knock', x, 0.3)
room('66', 'anna'); room('67', 'anna', tocam=True, over=lambda c, t: G2.like_comment(c, t, A('67', 'like'), A('67', 'comment')))
sfx('ui_click', A('67', 'like') + 0.5, 0.5); sfx('typing_run', A('67', 'comment') + 0.3, 0.2)
T_SUB = t0('69s')
gfx('68', lambda c, t: G2.g_series(c, t, t0('68'), sub_t=T_SUB))
for e in CT.events(T_SUB - 1.05, 'yt'): sfx(*e)
T_END = t1('69s') + 0.8
SC.append((T_END, ('gfx', lambda c, t: (G2.g_series(c, t, t0('68'), sub_t=T_SUB) if t < T_END + 0.01 else None, G2.end_card(c, t, T_END)))))
SC.sort(key=lambda x: x[0])

# mini subscribe card every ~2 minutes (after a payoff line)
PAYOFF = [n for n in ORDER if ORDER.index(n) > ORDER.index('6') and n not in ('63b', '63c', '64', '65', '66', '67', '68', '69', '69s') and not LNE[n]['text'].rstrip().endswith('?') and LNE[n]['sp'] == 'ANNA']
MINI = []
for target in range(120, int(DUR) - 60, 120):
    best = min(PAYOFF, key=lambda n: abs(t1(n) - target))
    if best not in [m[1] for m in MINI]: MINI.append((t1(best) + 0.3, best))
for tm, _ in MINI:
    for e in CT.events(tm, 'yt'): sfx(e[0], e[1], e[2] * 0.5)


def scene_at(t):
    cur = SC[0]
    for s in SC:
        if s[0] <= t: cur = s
        else: break
    return cur


def active_line(t):
    for l in TL['lines']:
        if l['t0'] + LEAD - 0.05 <= t <= l['t1'] + LEAD + 0.05: return l
    return None


def chapter_at(t):
    k = 0
    for kk, s in CHCARD.items():
        if t >= s: k = max(k, kk)
    if t >= t0('63b') - 0.1: k = 7
    return k


# ---------------- room drawing ----------------
CAST = RM.Cast()
CAMS = {'two': (1.0, W / 2, H / 2), 'anna': (1.42, RM.AX + 60, 560), 'chelli': (1.42, RM.CX - 40, 610), 'phone': (1.08, W / 2, H / 2 + 20)}


def draw_room_scene(c, t, n, s0):
    sp = ROOMSPEC[n]; ln = active_line(t)
    fi = min(len(ENV) - 1, max(0, int((t - LEAD) * 30)))
    talk = float(ENV[fi]) if ln else 0.0
    A_, C_ = CAST.anna, CAST.chelli
    A_['talk'] = talk if (ln and ln['sp'] == 'ANNA') else 0; C_['talk'] = talk if (ln and ln['sp'] == 'CHELLI') else 0
    tocam = sp.get('tocam') or n in ('5c',)
    A_['look'] = (0, 0.1) if tocam and ln and ln['sp'] == 'ANNA' else (0.55, 0.05)
    C_['look'] = (0, 0.1) if n == '5c' else (-0.55, 0.05)
    A_['gesture'] = (0.35 + 0.3 * math.sin(t * 1.3)) if A_['talk'] or (ln and ln['sp'] == 'ANNA') else 0.05
    if sp.get('tocam') and n == '44': A_['gesture'] = 0.9
    C_['gesture'] = (0.45 + 0.25 * math.sin(t * 1.7)) if (ln and ln['sp'] == 'CHELLI') else 0.0
    A_['tilt'] = 4 * math.sin(t * 0.7) if A_['talk'] else 0
    if n == '56b': A_['tilt'] = -8; A_['look'] = (0.0, 0.1)
    # entrance
    C_['x'] = RM.CX; C_['y'] = RM.BY
    if n == '1' and t < 1.0:
        u = e_out(prog(t, 0.0, 0.9)); C_['x'] = lerp(1780, RM.CX, u); C_['y'] = RM.BY - abs(math.sin(t * 14)) * 18 * (1 - u)
    C_['qpop'] = max(0.0, 1 - abs(t - 0.6) * 4) if n == '1' else (0.6 * max(0, 1 - abs(t - t0(n) - 0.2) * 4) if ln and ln['sp'] == 'CHELLI' and '?' in ln['text'] else 0)
    if n == '5c':
        w = 0.65 + 0.35 * math.sin(t * 11); A_['gesture'] = w; C_['gesture'] = 0.65 + 0.35 * math.sin(t * 11 + 1)
    cam = CAMS[sp['cam']]; u = prog(t, s0, s0 + 6); z = cam[0] * (1 + 0.035 * u)
    def props(c, t):
        if sp.get('broom'): RM.broom(c, RM.CX + 150, RM.BY - 260, 0.35 + 0.12 * math.sin(t * 6), 1.0); RM.dust(c, RM.CX + 230, RM.BY - 20, t, s0 + 0.2)
        if sp.get('bags'): RM.bags(c, RM.CX - 190, RM.BY - 10, t, s0 + 0.1)
        if sp.get('notebook'): RM.notebook(c, RM.CX + 160, RM.BY - 360, t, s0 + 0.1)
    RM.draw_room(c, t, CAST, cam=(z, cam[1], cam[2]), rec=T_REC if t >= T_REC else None, props=props)
    # question cards (cold open)
    if n in ('3', '4', '5'):
        fade = 1.0
        for i, q in enumerate(QT[:9]):
            x, y = G1.QPOS[i]; G1.qcard(c, i, x, y, t, q, wob=1.0 if n == '4' else 0.0, a=fade, locked=False)
    if sp.get('locked'):
        for k in range(3):
            G1.qcard(c, 6 + k, 1480 + k * 40 - 40, 300 + k * 110, t, s0 + 0.1 + k * 0.1, wob=0.6, locked=True, sc=0.8)
    if 'over' in sp: sp['over'](c, t)
    if t >= T_REC: RM.rec_overlay(c, t, T_REC, full=(n == '5c'))


# ---------------- overlays ----------------
def chapter_card(c, t, k):
    s = CHCARD[k]; board_bg(c, 0.12)
    u = e_back(prog(t, s + 0.25, s + 0.6))
    c.save(); c.translate(W / 2, 400); c.scale(max(0.01, u), max(0.01, u)); txt(c, str(k), 0, 0, 260, grad=True, stroke=6); c.restore()
    txt(c, L(f'CHAPTER {k} / 6', f'అధ్యాయం {k} / 6'), W / 2, 620, 30, CREAM, prog(t, s + 0.4, s + 0.7), kind='monob')
    txt(c, L(*CHT[k]), W / 2, 720, 58, CREAM, prog(t, s + 0.5, s + 0.8), maxw=1700, stroke=4)
    progress(c, t, k, y=880, big=True)


def progress(c, t, k, y=42, big=False):
    n = 9; sp = 64 if big else 46; x0 = W / 2 - sp * (n - 1) / 2; r = 16 if big else 11
    if not big:
        c.set_source_rgba(0, 0, 0, 0.45); rrect(c, x0 - 34, y - 24, sp * (n - 1) + 68, 48, 24); c.fill()
    c.set_source_rgba(1, 1, 1, 0.18); c.set_line_width(3); c.move_to(x0, y); c.line_to(x0 + sp * (n - 1), y); c.stroke()
    if k > 1:
        c.set_source(agrad(x0, y, x0 + sp * 5, y)); c.set_line_width(4); c.move_to(x0, y); c.line_to(x0 + sp * min(k - 1, 5), y); c.stroke()
    for i in range(n):
        x = x0 + i * sp
        if i >= 6:
            c.set_source_rgba(0.6, 0.6, 0.6, 0.8); c.set_line_width(3); c.arc(x, y - r * 0.35, r * 0.55, math.pi, 2 * math.pi); c.stroke()
            rrect(c, x - r * 0.75, y - r * 0.35, r * 1.5, r * 1.1, 3); c.fill(); continue
        done = i + 1 < k; cur = i + 1 == k
        if cur: glowdot(c, x, y, r)
        c.set_source_rgb(*(AMBER if (done or cur) else (0.25, 0.25, 0.27))); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
        txt(c, str(i + 1), x, y, r * 1.1, INK if (done or cur) else CREAM, kind='monob')


TAGTXT = L('DIWALI · FULL STORY', 'దీపావళి · FULL STORY')


def tag(c):
    w = text_w(c, TAGTXT, 22, 'monob') + 74
    glass(c, 36, 20, w, 46, 23, edge=False); glowdot(c, 60, 43, 6)
    txt(c, TAGTXT, 80, 43, 22, CREAM, anchor='l', kind='monob')


# captions
WORDS = [(s + LEAD, e + LEAD, w) for l in TL['lines'] for s, e, w in l['words']]
GROUPS = []; g = []; MAXC = 30 if LANG == 'en' else 30
for i, (s, e, w) in enumerate(WORDS):
    g.append((s, e, w)); nxt = WORDS[i + 1][0] if i + 1 < len(WORDS) else 1e9
    if len(g) >= (5 if LANG == 'en' else 4) or w[-1] in '.,?!…' or nxt - e > 0.35 or sum(len(x[2]) + 1 for x in g) > MAXC:
        GROUPS.append(g); g = []
if g: GROUPS.append(g)
_CAPC = {}


def captions(c, t, y=975):
    for gi, gr in enumerate(GROUPS):
        end = min(GROUPS[gi + 1][0][0] if gi + 1 < len(GROUPS) else 1e9, gr[-1][1] + 0.5)
        if gr[0][0] - 0.03 <= t < end:
            act = -1
            for k, (s, e, _) in enumerate(gr):
                if s - 0.03 <= t: act = k
            words = [x[2] for x in gr]; px = 54 if LANG == 'en' else 52
            key = (gi, act)
            if key not in _CAPC:
                if LANG == 'te':
                    from PIL import Image, ImageDraw
                    f = base._tefont(px)
                    d0 = ImageDraw.Draw(Image.new('L', (4, 4))); sp_ = 20; ws = [d0.textlength(w, font=f) for w in words]; tot = sum(ws) + sp_ * (len(ws) - 1)
                    im = Image.new('RGBA', (W, 160), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = W / 2 - tot / 2
                    for k, (w, wd) in enumerate(zip(words, ws)):
                        d.text((x, 80), w, font=f, fill=(255, 178, 36, 255) if k == act else (244, 241, 234, 255), anchor='lm', stroke_width=7, stroke_fill=(0, 0, 0, 230)); x += wd + sp_
                    _CAPC[key] = ('te', surf_from_pil(im))
                else:
                    _CAPC[key] = ('en', None)
            kind, sf = _CAPC[key]
            g_ = cairo.LinearGradient(0, y - 90, 0, H); g_.add_color_stop_rgba(0, 0, 0, 0, 0); g_.add_color_stop_rgba(1, 0, 0, 0, 0.55)
            c.set_source(g_); c.rectangle(0, y - 90, W, H - y + 90); c.fill()
            if kind == 'te':
                c.set_source_surface(sf[0], 0, y - 80); c.paint()
            else:
                font(c, 'head', px); sw = c.text_extents(' ').x_advance
                ws = [c.text_extents(w).x_advance for w in words]; tot = sum(ws) + sw * (len(ws) - 1); x = W / 2 - tot / 2
                for k, (w, wd) in enumerate(zip(words, ws)):
                    c.move_to(x, y + px * 0.36); c.text_path(w); c.set_line_join(cairo.LINE_JOIN_ROUND)
                    c.set_source_rgba(0, 0, 0, 0.9); c.set_line_width(9); c.stroke_preserve()
                    c.set_source_rgb(*(AMBER if k == act else CREAM)); c.fill(); x += wd + sw
            return


import base


def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.set_source_rgb(0.05, 0.05, 0.05); c.paint()
    st, sc = scene_at(t)
    k = chapter_at(t)
    in_chap = any(CHCARD[kk] <= t < CH_END[kk] for kk in CHCARD)
    if in_chap:
        kk = max(kk for kk in CHCARD if CHCARD[kk] <= t); chapter_card(c, t, kk)
    elif sc[0] == 'room': draw_room_scene(c, t, sc[1], st)
    elif sc[0] == 'gfx': sc[1](c, t)
    elif sc[0] == 'chap': chapter_card(c, t, sc[1])
    title = T_TITLE <= t < CHCARD[1]
    if not in_chap and not title:
        tag(c)
        if 1 <= k <= 6: progress(c, t, k)
    for tm, _ in MINI:
        if tm - 0.1 <= t < tm + 4.2:
            c.save(); sc_ = 0.5; c.translate(1500 - 540 * sc_, 260 - 180 * sc_); c.scale(sc_, sc_)
            CT.draw(c, t, tm, 'yt', LANG, y=180, t_out=tm + 3.8); c.restore()
    if not title and not in_chap:
        captions(c, t, y=1000 if st >= t0('68') - 0.2 and t < T_END else 975)
    return s


def to_rgb(s):
    a = np.ndarray((H, W, 4), np.uint8, s.get_data()); return a[:, :, [2, 1, 0]].tobytes()


def main():
    args = sys.argv[1:]
    if args and args[0] == 'still':
        from PIL import Image
        ts = [float(x) for x in args[1].split(',')]; ims = []
        for t in ts:
            s = frame(t); a = np.ndarray((H, W, 4), np.uint8, s.get_data())[:, :, [2, 1, 0]].copy(); ims.append(Image.fromarray(a))
        cols = 3; tw, th = 640, 360; sheet = Image.new('RGB', (cols * tw, ((len(ims) + cols - 1) // cols) * th))
        for i, im in enumerate(ims): sheet.paste(im.resize((tw, th)), ((i % cols) * tw, (i // cols) * th))
        sheet.save(args[2] if len(args) > 2 else ROOT + f'stills_{LANG}.jpg', quality=88)
        if len(ts) == 1: ims[0].save(ROOT + f'still1_{LANG}.png')
        return
    part, parts = (int(args[0]), int(args[1])) if len(args) >= 2 else (0, 1)
    nf = int(DUR * FPS); a, b = nf * part // parts, nf * (part + 1) // parts
    out = ROOT + f'v_{LANG}_{part}.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(a, b):
        p.stdin.write(to_rgb(frame(i / FPS)))
        if i % 300 == 0: print(LANG, part, i, '/', b, flush=True)
    p.stdin.close(); p.wait()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'events':
        json.dump(dict(ev=EV, dur=DUR, lead=LEAD, mini=MINI, chapters=CHCARD, t_title=T_TITLE), open(ROOT + f'events_{LANG}.json', 'w'), indent=0)
        print(len(EV), 'events', 'dur', round(DUR, 1), 'mini', MINI)
    else: main()

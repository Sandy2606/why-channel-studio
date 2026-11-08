import React from 'react';
import {z} from 'zod';
import {evolvePath} from '@remotion/paths';
import en from '../../../samples/stat-chart.en.json';
import te from '../../../samples/stat-chart.te.json';
import {defineEffect} from '../../lib/define';
import {Backdrop, baseProps, Ease, fit, lerp, Pill, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage} from '../../lib/kit';
import {GREY, usePalette} from '../../lib/brand';

const schema = z.object({...baseProps, title: z.string(), unit: z.string().default(''), unitPosition: z.enum(['before', 'after']).default('after'), decimals: z.number().int().min(0).max(3).default(0),
  series: z.array(z.object({label: z.string(), value: z.number()})).min(2),
  /** Index in series to highlight, plus its short label. */
  event: z.object({index: z.number().int().min(0), label: z.string()}).optional(),
  /** Start zoomed to the points before the event, then visibly rescale to the full range. */
  rescale: z.boolean().default(false), rescaleLabel: z.string().optional(), source: z.string().optional()});
type P = z.output<typeof schema>;
const beats = {reveal: [0, 18], draw: [19, 50], event: [51, 69], hold: [70, 89]} as Record<string, [number, number]>;

function nice(lo: number, hi: number) {
  const span = hi - lo || 1, raw = span / 4, mag = 10 ** Math.floor(Math.log10(raw)), step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((x) => x >= raw)!;
  const a = Math.floor(Math.min(lo, 0 < lo && lo / span < .5 ? 0 : lo) / step) * step, b = Math.ceil(hi / step) * step; const ticks: number[] = [];
  for (let t = a; t <= b + step * .001; t += step) ticks.push(+t.toFixed(6));
  return {a, b, ticks};
}

const textW = (t: string, px: number) => textWidth(t, `${weightOf(t, 'head')} ${px}px ${famOf(t, 'head')}`);

const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const P_ = s.portrait;
  const rev = beat('reveal', Ease.out), draw = beat('draw', Ease.linear), ev = beat('event', Ease.io), hold = beat('hold', Ease.io);
  const v = p.series.map((d) => d.value), n = v.length, ei = p.event ? Math.min(p.event.index, n - 1) : n - 1;
  const full = nice(Math.min(...v), Math.max(...v)); const early = p.rescale ? nice(Math.min(...v.slice(0, ei + 1)), Math.max(...v.slice(0, ei + 1))) : full;
  const a = lerp(early.a, full.a, ev), b = lerp(early.b, full.b, ev), ticks = ev > .5 ? full.ticks : early.ticks, tickA = !p.rescale || ev <= 0 || ev >= 1 ? 1 : ev < .5 ? Math.max(0, 1 - ev * 6) : Math.max(0, (ev - .84) * 6);
  const X0 = P_ ? s.x0 + 112 : s.x0 + 690, X1 = s.x1 - 20, Y0 = P_ ? s.y0 + 520 : s.y0 + 150, Y1 = P_ ? s.y1 - 130 : s.y1 - 130;
  const X = (i: number) => lerp(X0, X1, i / (n - 1)), Y = (y: number) => lerp(Y1, Y0, (y - a) / (b - a || 1));
  const d = v.map((y, i) => `${i ? 'L' : 'M'}${X(i).toFixed(2)} ${Y(y).toFixed(2)}`).join(' ');
  const evo = evolvePath(Math.max(.0001, draw), d);
  // The big figure only shows real readings: it steps to the last point the line has reached.
  const idx = Math.min(n - 1, Math.floor(draw * (n - 1) + 1e-6)); const shown = v[idx];
  const fmt = (x: number) => { const t = Math.abs(x).toLocaleString('en-IN', {minimumFractionDigits: p.decimals, maximumFractionDigits: p.decimals}); const sign = x < 0 ? '−' : ''; return p.unitPosition === 'before' ? `${sign}${p.unit}${t}` : `${sign}${t}${p.unit}`; };
  const tip = draw * (n - 1), i0 = Math.min(n - 2, Math.floor(tip)), k = tip - i0, tx = lerp(X(i0), X(i0 + 1), k), ty = lerp(Y(v[i0]), Y(v[i0 + 1]), k);
  const nLab = P_ ? 4 : 6, step = Math.max(1, Math.round((n - 1) / (nLab - 1))); const labs = p.series.map((_, i) => i).filter((i) => i % step === 0 || i === n - 1).filter((i, _j, arr) => i === n - 1 || arr.indexOf(n - 1) < 0 || n - 1 - i >= step * .7);
  const evX = X(ei), evY = Y(v[ei]); const evMax = P_ ? 540 : 620; const evPx = p.event ? fit(p.event.label, 'head', 38, evMax - 52) : 38; const evW = p.event ? Math.min(evMax, textW(p.event.label, evPx) + 52) : 0;
  return <Backdrop inner="#26221d" outer="#090909" cy="46%">
    <div style={{position: 'absolute', left: s.x0, top: P_ ? s.y0 : s.y0 + 44, width: P_ ? s.sw : 600}}>
      <Text px={P_ ? 66 : 56} maxW={P_ ? s.sw : 620}>{p.title}</Text>
      <div style={{marginTop: P_ ? 44 : 110}}><Text px={P_ ? 190 : 150} maxW={P_ ? s.sw : 600} color={pal.amber}>{fmt(shown)}</Text></div>
      <div style={{marginTop: 4}}><Text px={46} maxW={P_ ? s.sw : 600} kind="mono" bold>{p.series[idx].label}</Text></div>
    </div>
    <svg width={s.W} height={s.H} style={{position: 'absolute', inset: 0}}>
      <defs><clipPath id="plot"><rect x={X0 - 24} y={Y0 - 30} width={X1 - X0 + 48} height={Y1 - Y0 + 44} /></clipPath></defs>
      <g opacity={Math.max(.45, rev)}>{ticks.filter((t) => t >= a - 1e-6 && t <= b + 1e-6).map((t) => <line key={t} x1={X0} x2={X1} y1={Y(t)} y2={Y(t)} stroke={t === 0 ? pal.cream : '#3a3631'} strokeWidth={t === 0 ? 3 : 2} opacity={tickA} />)}
        <line x1={X0} x2={X1} y1={Y1} y2={Y1} stroke={pal.cream} strokeWidth={3} /></g>
      <g clipPath="url(#plot)"><path d={d} fill="none" stroke={pal.amber} strokeWidth={22} opacity={.16} strokeLinejoin="round" strokeLinecap="round" strokeDasharray={evo.strokeDasharray} strokeDashoffset={evo.strokeDashoffset} />
      <path d={d} fill="none" stroke={pal.amber} strokeWidth={8} strokeLinejoin="round" strokeLinecap="round" strokeDasharray={evo.strokeDasharray} strokeDashoffset={evo.strokeDashoffset} />
      {v.map((y, i) => tip >= i - 1e-6 ? <circle key={i} cx={X(i)} cy={Y(y)} r={i === ei && p.event ? 10 + ev * 8 : 7} fill={i === ei && p.event ? pal.amber : pal.cream} /> : null)}
      {draw > 0 && draw < 1 ? <circle cx={tx} cy={ty} r={15} fill="#FFF3D6" /> : null}</g>
      {p.event ? <><line x1={evX} x2={evX} y1={Y0 - 10} y2={Y1} stroke={pal.cream} strokeWidth={3} strokeDasharray="10 12" opacity={ev} /><circle cx={evX} cy={evY} r={18 + ev * 26} fill="none" stroke={pal.amber} strokeWidth={4} opacity={ev * (1 - hold * .55)} /></> : null}
    </svg>
    {ticks.filter((t) => t >= a - 1e-6 && t <= b + 1e-6).map((t) => <div key={t} style={{position: 'absolute', right: s.W - X0 + 14, top: Y(t) - 26, opacity: rev * tickA}}><Text px={34} kind="mono" color={GREY}>{t.toLocaleString('en-IN')}</Text></div>)}
    {labs.map((i) => <div key={i} style={{position: 'absolute', left: X(i), top: Y1 + 12, transform: `translateX(${i === 0 ? '-20%' : i === n - 1 ? '-80%' : '-50%'})`, opacity: rev}}><Text px={34} kind="mono" color={pal.cream}>{p.series[i].label}</Text></div>)}
    {p.event ? <div style={{position: 'absolute', left: Math.max(s.x0 + (P_ ? (p.rescale ? 290 : 0) : 980), Math.min(evX - 40, s.x1 - evW)), top: Math.max(Y0 - 92, s.y0 + 8), opacity: ev, transform: `scale(${lerp(.8, 1, ev)})`, transformOrigin: 'left center'}}><Pill px={38} maxW={evMax}>{p.event.label}</Pill></div> : null}
    {p.rescale && ev > 0 ? <div style={{position: 'absolute', left: P_ ? s.x0 : X0, top: Y0 - 92, opacity: Math.min(1, ev * 3) * (1 - hold * .25)}}><Pill px={34} bg={pal.cream} kind="mono">{p.rescaleLabel ?? (p.language === 'te' ? 'స్కేల్ మారింది' : 'SCALE CHANGED')}</Pill></div> : null}
    <SourceLine x={P_ ? s.cx : (X0 + X1) / 2} y={s.y1 - 58} maxW={P_ ? s.sw : X1 - X0} a={Math.max(hold, rev * .6)}>{p.source}</SourceLine>
  </Backdrop>;
};

export default defineEffect({number: 22, slug: 'stat-chart', name: 'Stat Chart', group: 'Data & Counters', frames: 90, beats, schema, Component, samples: {en, te},
  facts: (p) => [{what: `series "${p.title}"`, source: p.source}]});

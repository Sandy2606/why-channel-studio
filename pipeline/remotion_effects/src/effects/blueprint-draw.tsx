import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
import {getLength, getPointAtLength} from '@remotion/paths';
const schema = z.object({...baseProps, subject: z.string(), labels: z.array(z.object({text: z.string(), at: z.number().int().min(0)})).max(3), scaleNote: z.string().default('SCHEMATIC, NOT TO SCALE'),
  /** One continuous closed outline in 0..100 coordinates. Default is a star-fort plan. */
  outline: z.array(z.tuple([z.number(), z.number()])).min(3).default([[50, 4], [62, 22], [86, 16], [82, 40], [98, 52], [80, 64], [84, 88], [62, 80], [50, 98], [38, 80], [16, 88], [20, 64], [2, 52], [18, 40], [14, 16], [38, 22]]), source: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {frame: [0, 8], draw: [9, 38], extra: [39, 51], hold: [52, 59]};
const BLUE = '#0D2C54', LINE = '#CFE4FF';
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const P_ = s.portrait;
  const fr = beat('frame', Ease.out), dr = beat('draw', Ease.linear), ex = beat('extra', Ease.out), ho = beat('hold');
  const size = P_ ? s.sw - 130 : s.sh - 190, ox = P_ ? s.cx - size / 2 : s.x0 + 140, oy = P_ ? s.y0 + 240 : s.y0 + 130, M = (v: number) => v / 100 * size;
  const q = p.outline.map(([x, y]) => [ox + M(x), oy + M(y)] as [number, number]); const d = q.map((v, i) => `${i ? 'L' : 'M'}${v[0].toFixed(1)} ${v[1].toFixed(1)}`).join(' ') + ' Z';
  const L = getLength(d), tip = getPointAtLength(d, Math.min(L, dr * L)); const c = [ox + size / 2, oy + size / 2];
  const lx = P_ ? s.x0 : ox + size + 130;
  return <AbsoluteFill style={{background: BLUE, backgroundImage: `linear-gradient(rgba(207,228,255,.10) 2px, transparent 2px), linear-gradient(90deg, rgba(207,228,255,.10) 2px, transparent 2px)`, backgroundSize: '60px 60px'}}>
    <svg width={s.W} height={s.H} style={{position: 'absolute'}}>
      <rect x={s.x0} y={s.y0 + 100} width={s.sw} height={s.sh - 100} fill="none" stroke={LINE} strokeWidth={3} opacity={Math.max(.5, fr)} />
      <path d={d} fill="none" stroke={LINE} strokeWidth={7} strokeLinejoin="round" pathLength={1} strokeDasharray={`${Math.max(.0005, dr)} 1`} />
      {q.map((v, i) => <line key={i} x1={lerp(c[0], v[0], .42)} y1={lerp(c[1], v[1], .42)} x2={lerp(c[0], v[0], .42 + ex * .3)} y2={lerp(c[1], v[1], .42 + ex * .3)} stroke={LINE} strokeWidth={2} opacity={.6} />)}
      <circle cx={c[0]} cy={c[1]} r={M(14) * ex} fill="none" stroke={LINE} strokeWidth={3} strokeDasharray="10 10" />
      <g opacity={ex}><line x1={ox} x2={lerp(ox, ox + size, ex)} y1={oy + size + 34} y2={oy + size + 34} stroke={pal.amber} strokeWidth={3} /><line x1={ox} x2={ox} y1={oy + size + 20} y2={oy + size + 48} stroke={pal.amber} strokeWidth={3} /><line x1={ox + size} x2={ox + size} y1={oy + size + 20} y2={oy + size + 48} stroke={pal.amber} strokeWidth={3} /></g>
      {dr < 1 && tip ? <circle cx={tip.x} cy={tip.y} r={13} fill="#fff" /> : null}
      {p.labels.map((l, i) => { const a = q[l.at % q.length]; const k = clamp(ex * 3 - i); const ty = P_ ? s.y1 - 200 + i * 62 : oy + 60 + i * 150; return <polyline key={i} points={P_ ? `${a[0]},${a[1]} ${a[0]},${a[1]}` : `${a[0]},${a[1]} ${lx - 18},${ty + 24}`} fill="none" stroke={pal.amber} strokeWidth={3} opacity={k} />; })}
      {p.labels.map((l, i) => { const a = q[l.at % q.length]; return <circle key={'c' + i} cx={a[0]} cy={a[1]} r={10} fill={pal.amber} opacity={clamp(ex * 3 - i)} />; })}
    </svg>
    <div style={{position: 'absolute', left: s.x0 + 20, top: s.y0 + 8}}><Text px={P_ ? 66 : 64} maxW={s.sw - 40} color={LINE}>{p.subject}</Text></div>
    {p.labels.map((l, i) => { const k = clamp(ex * 3 - i); return <div key={i} style={{position: 'absolute', left: P_ ? s.x0 + 30 : lx, top: P_ ? s.y1 - 226 + i * 62 : oy + 30 + i * 150, opacity: k}}><Text px={P_ ? 42 : 44} maxW={P_ ? s.sw - 60 : s.x1 - lx - 30} color={pal.amber}>{`${i + 1}. ${l.text}`}</Text></div>; })}
    <div style={{position: 'absolute', right: s.W - s.x1 + 20, top: P_ ? s.y0 + 116 : s.y1 - 70, opacity: Math.max(ex, ho)}}><Text px={34} kind="mono" bold maxW={s.sw - 60} color={LINE}>{p.scaleNote}</Text></div>
  </AbsoluteFill>;
};
export default defineEffect({number: 17, slug: 'blueprint-draw', name: 'Blueprint Draw', group: 'Ink & Paper', frames: 60, beats, schema, Component, samples: S('blueprint-draw'), facts: (p) => [{what: `drawing of ${p.subject}`, source: p.source}]});

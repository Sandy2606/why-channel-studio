import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const schema = z.object({...baseProps, tasks: z.array(z.object({label: z.string(), done: z.boolean().default(true)})).min(2).max(8), doneLabel: z.string().optional(), source: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {pulse: [0, 12], spread: [13, 32], done: [33, 49], hold: [50, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const P_ = s.portrait; const pu = beat('pulse', Ease.out), sp = beat('spread', Ease.linear), dn = beat('done', Ease.linear), ho = beat('hold');
  const n = p.tasks.length; const cx = P_ ? s.cx : s.x0 + 240, cy = P_ ? s.y0 + 110 : s.cy; const slotH = P_ ? (s.sh - 330) / n : (s.sh - 130) / n, sx = P_ ? s.x0 : s.x0 + 680, sw = P_ ? s.sw : 900;
  const slot = (i: number) => [P_ ? sx + 30 : sx, (P_ ? s.y0 + 250 : s.y0 + 20) + slotH * i + slotH / 2] as const; const stagger = (i: number) => clamp(sp * (n + 1.2) - i * 1);
  const tally = p.tasks.filter((t, i) => t.done && dn >= (i + 1) / n - 1e-6).length; const total = p.tasks.filter((t) => t.done).length;
  return <Backdrop inner="#1d2a33" outer="#07090b" cy={P_ ? '20%' : '50%'}>
    <svg width={s.W} height={s.H} style={{position: 'absolute'}}>
      {p.tasks.map((t, i) => { const [x, y] = slot(i); const m = (P_ ? cy + 80 : cy); const mx = P_ ? (cx + x) / 2 : (cx + x) / 2; const d = P_ ? `M ${cx} ${cy + 30} C ${cx} ${y}, ${mx} ${y}, ${x} ${y}` : `M ${cx} ${cy} C ${mx} ${cy}, ${mx} ${y}, ${x} ${y}`; const k = Ease.io(stagger(i)); const isDone = t.done && dn >= (i + .6) / n; void m;
        return <path key={i} d={d} fill="none" stroke={isDone ? pal.amber : '#5f7380'} strokeWidth={4} pathLength={1} strokeDasharray={`${Math.max(.001, k)} 1`} />; })}
      <circle cx={cx} cy={cy} r={34 + 14 * Math.sin(pu * 3.14)} fill={pal.amber} /><circle cx={cx} cy={cy} r={70 + 56 * pu} fill="none" stroke={pal.amber} strokeWidth={4} opacity={1 - pu * .75} />
    </svg>
    {p.tasks.map((t, i) => { const [x, y] = slot(i); const k = Ease.out(clamp(stagger(i) * 2 - 1)); const on = dn >= (i + .6) / n; const isDone = t.done && on; const h = Math.min(slotH - 14, P_ ? 90 : 92);
      return <div key={i} style={{position: 'absolute', left: x, top: y - h / 2, width: sw - (P_ ? 30 : 0), height: h, opacity: k, transform: `translateX(${(1 - k) * 30}px)`, background: isDone ? pal.amber : 'rgba(255,255,255,.08)', borderRadius: 16, display: 'flex', alignItems: 'center', padding: '0 24px', boxSizing: 'border-box', justifyContent: 'space-between'}}>
        <Text px={42} maxW={sw - 180} color={isDone ? pal.ink : pal.cream}>{t.label}</Text><Text px={44} color={isDone ? pal.ink : GREY}>{isDone ? '✓' : on ? '…' : '○'}</Text></div>; })}
    <div style={{position: 'absolute', left: P_ ? s.x0 : s.x0 + 30, top: P_ ? s.y0 + 58 : s.cy + 90, opacity: Math.max(dn, ho)}}><Text px={P_ ? 76 : 84} color={pal.amber}>{`${tally}/${total}`}</Text><div><Text px={36} kind="mono" bold maxW={P_ ? 280 : 480}>{p.doneLabel ?? (p.language === 'te' ? 'పూర్తయ్యాయి' : 'DONE')}</Text></div></div>
  </Backdrop>;
};
export default defineEffect({number: 23, slug: 'agent-swarm', name: 'Agent Swarm', group: 'Data & Counters', frames: 60, beats, schema, Component, samples: S('agent-swarm'), facts: (p) => [{what: 'task statuses', source: p.source}]});

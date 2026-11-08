import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const schema = z.object({...baseProps, notifications: z.array(z.object({id: z.string(), app: z.string(), text: z.string(), amount: z.number().optional()})).min(2).max(12), title: z.string(), totalLabel: z.string().optional(), unit: z.string().default(''), time: z.string().default('9:41'), source: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {first: [0, 11], arrive: [12, 37], pile: [38, 50], hold: [51, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {range, frame, beat} = useBeats(beats, p); const P_ = s.portrait; const ho = beat('hold'); const n = p.notifications.length; const [a, b] = range.arrive;
  const at = (i: number) => i === 0 ? 4 : Math.round(a + (range.pile[1] - 4 - a) * Math.pow((i - 1) / Math.max(1, n - 1), .62));
  const landed = p.notifications.filter((_, i) => frame >= at(i) + 5); const hasAmt = p.notifications.every((x) => x.amount !== undefined); const total = hasAmt ? landed.reduce((v, x) => v + (x.amount ?? 0), 0) : landed.length; const showNum = `${hasAmt ? p.unit : ''}${total.toLocaleString('en-IN')}`;
  const pw = P_ ? s.sw : 620, ph = P_ ? s.sh - 30 : s.sh + 80, px = P_ ? s.x0 : s.x0 + 1020, py = P_ ? s.y0 + 15 : s.y0 - 30; const cardH = 118, gap = 14; void b;
  return <Backdrop inner="#22303d" outer="#07090d" cy="30%">
    <div style={{position: 'absolute', left: px, top: py, width: pw, height: ph, borderRadius: 44, background: 'linear-gradient(170deg,#2c3a4a,#11161d)', overflow: 'hidden', boxShadow: '0 30px 70px rgba(0,0,0,.6)'}}>
      <div style={{textAlign: 'center', marginTop: 56}}><Text px={150} color={pal.cream}>{p.time}</Text></div>
      {p.notifications.map((c, i) => { const t = frame - at(i); if (t < 0) return null; const k = Ease.out(clamp(t / 6)); const later = p.notifications.filter((_, j) => j > i && frame >= at(j)).reduce((acc, _x, j) => acc + clamp((frame - at(i + 1 + j)) / 5), 0); const y = ph - 150 - later * (cardH + gap) + (1 - k) * 170; const comp = 1 - Math.max(0, Math.sin(clamp(t / 7) * 3.14)) * .03;
        const lim = P_ ? 430 : 250; if (y < lim) return null; const fade = clamp((y - lim) / 90);
        return <div key={c.id} style={{position: 'absolute', left: 22, right: 22, top: y, height: cardH, borderRadius: 26, background: 'rgba(244,241,234,.94)', padding: '14px 24px', boxSizing: 'border-box', transform: `scale(${comp})`, opacity: k * fade}}><Text px={34} kind="mono" bold color="#5b5850" maxW={pw - 90}>{c.app}</Text><div><Text px={40} maxW={pw - 90} color={pal.ink}>{c.text}</Text></div></div>; })}
    </div>
    <div style={{position: 'absolute', left: P_ ? s.x0 + 30 : s.x0 + 30, top: P_ ? s.y0 + 250 : s.y0 + 240, width: P_ ? s.sw - 60 : 900}}>{!P_ ? <Text px={70} maxW={900}>{p.title}</Text> : null}<div><div style={{display: 'inline-block', background: P_ ? 'rgba(10,10,10,.8)' : 'transparent', borderRadius: 18, padding: P_ ? '4px 26px' : 0}}><Text px={P_ ? 104 : 190} maxW={P_ ? 640 : 900} color={pal.amber}>{showNum}</Text></div></div>{p.totalLabel ? <div style={{opacity: Math.max(.9, ho)}}><Text px={40} kind="mono" bold maxW={P_ ? s.sw - 60 : 900}>{p.totalLabel}</Text></div> : null}</div>
    {P_ ? <div style={{position: 'absolute', left: s.cx, top: s.y0 - 70 + 0, transform: 'translateX(-50%)'}} /> : null}
  </Backdrop>;
};
export default defineEffect({number: 27, slug: 'lock-screen-notifications', name: 'Lock-Screen Notifications', group: 'UI & Typography', frames: 60, beats, schema, Component, samples: S('lock-screen-notifications'), facts: (p) => [{what: 'notification figures', source: p.source}]});

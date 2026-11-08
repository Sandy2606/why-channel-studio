import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const card = z.object({title: z.string(), date: z.string().optional(), source: z.string().optional(), body: z.string().optional()});
const schema = z.object({...baseProps, cards: z.array(card).length(3), highlightCard: z.number().int().min(0).max(2).default(1), highlight: z.string(), takeaway: z.string()});
type P = z.output<typeof schema>;
const beats: Beats = {first: [0, 18], third: [19, 31], mark: [32, 48], hold: [49, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const P_ = s.portrait; const f = beat('first', Ease.linear), t = beat('third', Ease.out), m = beat('mark', Ease.linear), ho = beat('hold');
  const cw = P_ ? s.sw - 120 : 560, ch = P_ ? 310 : 400;
  const pos = P_ ? [[s.x0 + 10, s.y0 + 20, -3], [s.x0 + 110, s.y0 + 350, 2.4], [s.x0 + 20, s.y0 + 680, -1.6]] : [[s.x0 + 10, s.y0 + 60, -3], [s.x0 + 590, s.y0 + 30, 2], [s.x0 + 1150, s.y0 + 80, -1.6]];
  const prog = [clamp(f / .55), clamp((f - .42) / .58), t];
  const h = p.highlightCard, hx = pos[h][0] + 34, hy = pos[h][1] + (P_ ? 148 : 170), hPx = fit(p.highlight, 'head', P_ ? 50 : 46, cw - 90); const hw = Math.min(cw - 70, textWidth(p.highlight, `${weightOf(p.highlight, 'head')} ${hPx}px ${famOf(p.highlight, 'head')}`));
  const cxr = hx + hw / 2, cyr = hy + hPx * .72; const loop = wobble(circlePts(cxr, cyr, hw / 2 + 34, hPx * .95, 13), 'loop', 4, true);
  const tk = [P_ ? s.cx : s.cx, P_ ? s.y1 - 90 : s.y1 - 86]; const arrowD = wobble(linePts([cxr + hw * .1, cyr + hPx * .95], [tk[0], tk[1] - 60], 3), 'arrow', 8);
  const loopK = clamp(m / .6), arrK = clamp((m - .55) / .45);
  return <AbsoluteFill style={{background: 'radial-gradient(100% 80% at 50% 40%, #3b3127 0%, #15110d 100%)'}}>
    {p.cards.map((c, i) => { const k = Ease.out(prog[i]); return <div key={i} style={{position: 'absolute', left: pos[i][0], top: pos[i][1], width: cw, height: ch, background: i === 1 ? '#FBF3DA' : '#F1EDE1', padding: 30, boxSizing: 'border-box', transform: `translate(${(1 - k) * (i % 2 ? 1 : -1) * (s.W + 700)}px, ${(1 - k) * 90}px) rotate(${pos[i][2] + (1 - k) * 9}deg)`, boxShadow: `0 ${6 + (1 - k) * 34}px ${16 + (1 - k) * 50}px rgba(0,0,0,${.55 - .2 * (1 - k)})`, overflow: 'hidden'}}>
      <Text px={P_ ? 46 : 42} maxW={cw - 64} color="#14110C">{c.title}</Text>
      <div style={{marginTop: 2}}><Text px={34} maxW={cw - 64} kind="mono" color="#5a5140">{[c.date].filter(Boolean).join('') || ' '}</Text></div>
      {i === h ? <div style={{marginTop: P_ ? 14 : 22}}><Text px={hPx} color="#14110C">{p.highlight}</Text></div> : c.body ? <div style={{marginTop: 14}}><Para px={36} width={cw - 64} kind="mono" color="#3a3428">{c.body}</Para></div> : null}
      <div style={{position: 'absolute', left: 30, bottom: 18}}><Text px={34} maxW={cw - 64} kind="mono" bold color="#6b6250">{c.source ?? ''}</Text></div></div>; })}
    <svg width={s.W} height={s.H} style={{position: 'absolute'}}><Ink d={loop} k={loopK} w={9} color={pal.amber === '#FFB224' ? '#E0920B' : pal.amber} /><Ink d={arrowD} k={arrK} w={9} color={pal.amber} /></svg>
    <div style={{position: 'absolute', left: tk[0], top: tk[1] - 56, transform: `translateX(-50%) scale(${lerp(.86, 1, ho)})`, opacity: ho}}><Pill px={P_ ? 50 : 54} maxW={s.sw}>{p.takeaway}</Pill></div>
  </AbsoluteFill>;
};
export default defineEffect({number: 18, slug: 'paper-desk', name: 'Paper Desk', group: 'Ink & Paper', frames: 60, beats, schema, Component, samples: S('paper-desk'), facts: (p) => p.cards.map((c) => ({what: `card "${c.title}"`, source: c.source}))});

import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const schema = z.object({...baseProps, words: z.array(z.string()).length(3), message: z.string(), accent: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {grid: [0, 9], rails: [10, 25], shift: [26, 40], lock: [41, 54], hold: [55, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const ac = p.accent ?? pal.amber; const P_ = s.portrait;
  const cols = P_ ? 6 : 12, rows = P_ ? 10 : 6, cw = s.sw / cols, ch = s.sh / rows, g = beat('grid', Ease.out), r = beat('rails', Ease.out), sh = beat('shift', Ease.io), lk = beat('lock', Ease.io);
  const X = (c: number) => Math.round(s.x0 + c * cw), Y = (c: number) => Math.round(s.y0 + c * ch);
  const px = P_ ? 190 : 170, w0 = s.sw - 30, size = Math.min(...p.words.map((t) => fit(t, 'head', px, w0, 60))); const fs = TELUGU.test(p.words.join('')) ? Math.round(size) : size;
  const place = P_ ? [[0, 1.1], [0, 3.2], [0, 5.3]] : [[0, .3], [0, 2.3], [5.4, 2.3]];
  const start = P_ ? [[2.4, 3.2], [0, 1.1], [0, 5.3]] : [[6, 2.3], [0, .3], [0, 4.2]];
  const wordXY = (i: number) => { const k = i < 2 ? sh : lk; return [lerp(X(start[i][0]), X(place[i][0]), k), lerp(Y(start[i][1]), Y(place[i][1]), k)]; };
  const blocks = P_ ? [{c: [0, 7.45, 6, 2.55], col: pal.ink, d: 'x'}, {c: [4, 0, 2, 1], col: ac, d: 'y'}, {c: [5, 3.1, 1, 2], col: ac, d: 'y'}] : [{c: [0, 4.3, 12, 1.7], col: pal.ink, d: 'x'}, {c: [10, 0, 2, 2], col: ac, d: 'y'}, {c: [4.2, 2.45, .8, 1.5], col: ac, d: 'y'}];
  return <AbsoluteFill style={{background: pal.cream}}>
    <svg width={s.W} height={s.H} style={{position: 'absolute'}} opacity={Math.max(.5, g) * (1 - lk * .62)}>
      {Array.from({length: cols + 1}, (_, i) => <line key={i} x1={X(i)} x2={X(i)} y1={0} y2={s.H} stroke="#bcb6a8" strokeWidth={2} />)}
      {Array.from({length: rows + 1}, (_, i) => <line key={'r' + i} y1={Y(i)} y2={Y(i)} x1={0} x2={s.W} stroke="#bcb6a8" strokeWidth={2} />)}</svg>
    {blocks.map((b, i) => { const k = interpolate(r, [i * .22, Math.min(1, i * .22 + .55)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}); const off = (1 - k) * (b.d === 'x' ? -s.W : -s.H);
      return <div key={i} style={{position: 'absolute', left: X(b.c[0]), top: Y(b.c[1]), width: b.c[2] * cw, height: b.c[3] * ch, background: b.col, transform: b.d === 'x' ? `translateX(${Math.round(off)}px)` : `translateY(${Math.round(off)}px)`}} />; })}
    {p.words.map((t, i) => { const [x, y] = wordXY(i); const k = i === 0 ? 1 : clamp(r * 3 - i * .7); return <div key={i} style={{position: 'absolute', left: Math.round(x), top: Math.round(y), opacity: k}}><Text px={fs} color={pal.ink}>{t}</Text></div>; })}
    <div style={{position: 'absolute', left: P_ ? X(0) + 30 : X(0) + 30, top: P_ ? Y(7.45) + 36 : Y(4.3) + 30, width: s.sw - 60, opacity: lk, transform: `translateY(${(1 - lk) * 14}px)`}}><Para px={P_ ? 58 : 58} width={s.sw - 60} kind="head" color={pal.cream}>{p.message}</Para></div>
  </AbsoluteFill>;
};
export default defineEffect({number: 16, slug: 'swiss-grid', name: 'Swiss Grid', group: 'Ink & Paper', frames: 60, beats, schema, Component, samples: S('swiss-grid'), facts: () => []});

import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const schema = z.object({...baseProps, one: z.string(), two: z.string(), keyWord: z.string(), finalColor: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {one: [0, 11], two: [12, 25], three: [26, 39], fill: [40, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat, range, frame} = useBeats(beats, p); const c = p.finalColor ?? pal.amber; const P_ = s.portrait;
  const o = beat('one', Ease.out, 0, .55), t = beat('two', Ease.out, 0, .55), k = beat('three', Ease.out, 0, .55), fi = beat('fill', Ease.io);
  const px1 = fit(p.one, 'head', P_ ? 170 : 170, s.sw, 60), px2 = fit(p.two, 'head', P_ ? 170 : 170, s.sw, 60); const big = fit(p.keyWord, 'head', P_ ? 300 : 420, s.sw, 60); const te = TELUGU.test(p.keyWord);
  const shakeAt = (f: number) => { const d = frame - f; return d >= 0 && d < 6 ? Math.sin(d * 2.6) * (6 - d) * 1.6 : 0; }; const sh = shakeAt(range.two[0] + 7) + shakeAt(range.three[0] + 7) * 1.3;
  const blurOf = (x: number) => x > 0 && x < 1 ? (1 - x) * 12 : 0, scaleOf = (x: number) => lerp(2.1, 1, x);
  const off = k * (P_ ? -340 : -300);
  const h = big * (te ? 1.55 : 1.15);
  const family = famOf(p.keyWord, 'head'), weight = weightOf(p.keyWord, 'head');
  return <AbsoluteFill style={{background: '#121212', transform: `translate(${sh}px, ${sh * .6}px)`}}>
    <div style={{position: 'absolute', left: s.cx, top: s.cy - (P_ ? 120 : 110) + off * .6, transform: `translate(-50%,-50%) scale(${scaleOf(o) * (1 - k * .34)})`, filter: `blur(${blurOf(o)}px)`, opacity: Math.max(.0001, 1 - k * .35)}}><Text px={px1}>{p.one}</Text></div>
    {t > 0 ? <div style={{position: 'absolute', left: s.cx, top: s.cy + (P_ ? 90 : 80) + off * .75, transform: `translate(-50%,-50%) scale(${scaleOf(t) * (1 - k * .34)})`, filter: `blur(${blurOf(t)}px)`, opacity: 1 - k * .35}}><Text px={px2}>{p.two}</Text></div> : null}
    {k > 0 ? <div style={{position: 'absolute', left: s.cx, top: s.cy + (P_ ? 190 : 150), transform: `translate(-50%,-50%) scale(${scaleOf(k)})`, filter: `blur(${blurOf(k)}px)`, whiteSpace: 'nowrap'}}>
      <div style={{position: 'relative', fontFamily: family, fontWeight: weight, fontSize: big, lineHeight: `${h}px`, height: h}}>
        <span style={{color: 'transparent', WebkitTextStroke: `3px ${pal.cream}`}}>{p.keyWord}</span>
        <span style={{position: 'absolute', left: 0, top: 0, color: c, clipPath: `inset(${(1 - fi) * 100}% 0 0 0)`}}>{p.keyWord}</span></div></div> : null}
  </AbsoluteFill>;
};
export default defineEffect({number: 28, slug: 'type-slam', name: 'Type Slam', group: 'UI & Typography', frames: 60, beats, schema, Component, samples: S('type-slam'), facts: () => []});

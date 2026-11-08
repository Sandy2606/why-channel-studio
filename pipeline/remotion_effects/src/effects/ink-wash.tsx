import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const schema = z.object({...baseProps, title: z.string(), sun: z.tuple([z.number(), z.number()]).default([.68, .3]), ridges: z.number().int().min(2).max(4).default(3)});
type P = z.output<typeof schema>;
const beats: Beats = {wash: [0, 14], far: [15, 28], near: [29, 43], title: [44, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const {beat} = useBeats(beats, p); const P_ = s.portrait; const w = beat('wash', Ease.out), fa = beat('far', Ease.out), ne = beat('near', Ease.out), ti = beat('title', Ease.io, 0, .6);
  const W = s.W, H = s.H;
  const ridge = (y: number, amp: number, seed: string) => { const r = seeded(seed); const n = 16; let d = `M -40 ${H + 40} L -40 ${y}`; for (let i = 0; i <= n; i++) { const x = i / n * (W + 80) - 40; d += ` L ${x.toFixed(0)} ${(y + (r(i) - .5) * amp * 2 + Math.sin(i * .8 + r('p') * 6) * amp).toFixed(0)}`; } return d + ` L ${W + 40} ${H + 40} Z`; };
  const layers = [{y: H * (P_ ? .58 : .55), amp: 46, col: '#9fa39b', k: fa, seed: 'a', op: .62}, {y: H * (P_ ? .68 : .68), amp: 60, col: '#5e625c', k: ne * .9 + fa * .1, seed: 'b', op: .78}, {y: H * (P_ ? .8 : .84), amp: 54, col: '#23241f', k: ne, seed: 'c', op: .92}].slice(3 - p.ridges > 0 ? 3 - p.ridges : 0);
  return <AbsoluteFill style={{background: '#EFE8D8'}}>
    <svg width={W} height={H} style={{position: 'absolute'}}>
      <defs><filter id="ink" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency=".012 .03" numOctaves={4} seed={9} /><feDisplacementMap in="SourceGraphic" scale={46} /><feGaussianBlur stdDeviation={2.2} /></filter>
        <filter id="wash"><feTurbulence type="fractalNoise" baseFrequency=".004" numOctaves={3} seed={3} /><feColorMatrix values="0 0 0 0 .78 0 0 0 0 .66 0 0 0 0 .48 0 0 0 .9 -.15" /></filter>
        {layers.map((l, i) => <linearGradient key={i} id={`g${i}`} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={l.col} /><stop offset=".5" stopColor={l.col} stopOpacity={.72} /><stop offset="1" stopColor={l.col} stopOpacity={.3} /></linearGradient>)}</defs>
      <rect width={W} height={H} filter="url(#wash)" opacity={.55 * Math.max(.25, w)} />
      <circle cx={W * p.sun[0]} cy={H * p.sun[1]} r={(P_ ? 150 : 120) * Math.max(.0, fa)} fill="#C96E3F" opacity={.62} filter="url(#ink)" />
      {layers.map((l, i) => { if (l.k <= 0) return null; const yoff = (1 - l.k) * 140; return <path key={i} d={ridge(l.y, l.amp, l.seed)} fill={`url(#g${i})`} opacity={l.op * clamp(l.k * 1.6)} transform={`translate(0 ${yoff})`} filter="url(#ink)" />; })}
    </svg>
    <div style={{position: 'absolute', left: s.cx, top: s.y0 + (P_ ? 90 : 90), transform: `translateX(-50%) translateY(${(1 - ti) * 12}px)`, opacity: ti}}><Text px={P_ ? 104 : 118} maxW={s.sw} color="#1b1a16">{p.title}</Text></div>
  </AbsoluteFill>;
};
export default defineEffect({number: 20, slug: 'ink-wash', name: 'Ink Wash', group: 'Ink & Paper', frames: 60, beats, schema, Component, samples: S('ink-wash'), facts: () => []});

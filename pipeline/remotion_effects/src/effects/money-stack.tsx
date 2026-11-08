import React, {useMemo} from 'react';
import {AbsoluteFill, continueRender, delayRender, staticFile} from 'remotion';
import {z} from 'zod';
import * as THREE from 'three';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, clamp, Ease, lerp, Para, Pill, seeded, SourceLine, Text, useBeats, useStage, Beats} from '../lib/kit';
import {GREY, usePalette} from '../lib/brand';
import {project, Stage3D, useCamera, useOrtho} from '../lib/three';
const Lights = () => <><ambientLight intensity={.8} /><directionalLight position={[-6, 14, 9]} intensity={2.2} castShadow shadow-mapSize-width={1024} shadow-mapSize-height={1024} shadow-camera-left={-14} shadow-camera-right={14} shadow-camera-top={14} shadow-camera-bottom={-14} /><directionalLight position={[8, 4, -6]} intensity={.7} /></>;

const schema = z.object({...baseProps, amounts: z.array(z.object({label: z.string().optional(), value: z.number().positive(), source: z.string().optional()})).min(1).max(14), currency: z.string().default('₹'), displayUnit: z.string().default(''), context: z.string(), estimate: z.boolean().default(false)});
type P = z.output<typeof schema>;
const beats: Beats = {empty: [0, 12], land: [13, 43], count: [44, 53], hold: [54, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat, frame, range} = useBeats(beats, p); const P_ = s.portrait; const co = beat('count', Ease.out); const n = p.amounts.length, [a, b] = range.land;
  const at = (i: number) => Math.round(a + (b - a - 6) * Math.pow(i / Math.max(1, n - 1), .68)); const K = p.amounts.reduce((t, x) => t + x.value, 0), HT = P_ ? 6.4 : 5.8, W_ = 3.6, D_ = 2.2; const unitH = HT / K;
  const landedSum = p.amounts.filter((_, i) => frame >= at(i) + 7).reduce((t, x) => t + x.value, 0); const shown = co > 0 ? lerp(landedSum, K, co) : landedSum;
  let y = 0; const blocks = p.amounts.map((x, i) => { const t = frame - at(i); const h = x.value * unitH; const base = y; y += h; if (t < 0) return null; const fall = clamp(t / 7); const yy = base + (1 - fall * fall) * 8; const sq = t >= 7 && t < 12 ? 1 - Math.sin((t - 7) / 5 * Math.PI) * .13 : 1; return {i, h, y: yy, sq, base}; }).filter(Boolean) as {i: number; h: number; y: number; sq: number; base: number}[];
  const top = blocks.length ? blocks[blocks.length - 1].base + blocks[blocks.length - 1].h : 0; const hiI = n - 1;
  const ang = -.55 + frame * .004; const R = P_ ? 25 : 14.5; const lookY = lerp(.9, HT * (P_ ? .66 : .46), clamp(top / HT)); const cam = useCamera({pos: [Math.sin(ang) * R + (P_ ? 0 : 3.2), lookY + (P_ ? 6.5 : 4.8), Math.cos(ang) * R], look: [P_ ? 0 : 3.2, lookY, 0], fov: P_ ? 34 : 30});
  const fmt = (v: number) => `${p.currency}${Math.round(v).toLocaleString('en-IN')}${p.displayUnit ? ' ' + p.displayUnit : ''}`;
  return <AbsoluteFill style={{background: 'radial-gradient(90% 72% at 50% 60%, #33302a 0%, #0a0a09 100%)'}}>
    <Stage3D cam={cam} shadows><Lights /><mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow position={[0, -.27, 0]}><planeGeometry args={[60, 60]} /><meshStandardMaterial color="#1a1815" /></mesh><mesh receiveShadow castShadow position={[0, -.13, 0]}><boxGeometry args={[W_ + 1.6, .26, D_ + 1.6]} /><meshStandardMaterial color="#3f3b34" /></mesh>
      {blocks.map((c) => { const hot = c.i === hiI && co > 0; return <group key={c.i} position={[0, c.y, 0]} scale={[2 - c.sq, c.sq, 2 - c.sq]}><mesh position={[0, c.h / 2, 0]} castShadow receiveShadow><boxGeometry args={[W_, Math.max(.05, c.h - .04), D_]} /><meshStandardMaterial color={hot ? pal.amber : c.i % 2 ? '#A9B48E' : '#8FA077'} roughness={.55} emissive={hot ? pal.amber : '#000'} emissiveIntensity={hot ? .3 * co : 0} /></mesh><mesh position={[0, c.h / 2, 0]}><boxGeometry args={[W_ * .16, Math.max(.05, c.h - .01), D_ + .03]} /><meshStandardMaterial color="#F0E7CF" /></mesh></group>; })}</Stage3D>
    <div style={{position: 'absolute', left: P_ ? s.cx : s.x1 - 20, top: P_ ? s.y0 + 8 : s.y0 + 250, transform: P_ ? 'translateX(-50%)' : 'translateX(-100%)', textAlign: P_ ? 'center' : 'right', width: P_ ? s.sw : 760}}><Text px={P_ ? 150 : 138} maxW={P_ ? s.sw : 740} color={pal.amber}>{fmt(shown)}</Text><div><Text px={44} maxW={P_ ? s.sw : 740}>{p.context}</Text></div>{p.estimate ? <div><Text px={36} kind="mono" bold color={GREY}>{p.language === 'te' ? 'అంచనా' : 'ESTIMATE'}</Text></div> : null}</div>
  </AbsoluteFill>;
};
export default defineEffect({number: 12, slug: 'money-stack', name: 'Money Stack', group: '3D Scenes', frames: 60, beats, schema, Component, samples: S('money-stack'), facts: (p) => p.amounts.map((a, i) => ({what: `amount ${i + 1}`, source: a.source}))});

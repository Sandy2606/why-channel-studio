import React, {useMemo} from 'react';
import {AbsoluteFill, continueRender, delayRender, staticFile} from 'remotion';
import {z} from 'zod';
import * as THREE from 'three';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, clamp, Ease, lerp, Para, Pill, seeded, SourceLine, Text, useBeats, useStage, Beats} from '../lib/kit';
import {GREY, usePalette} from '../lib/brand';
import {project, Stage3D, useCamera, useOrtho} from '../lib/three';
const Stem: React.FC<{a: {x: number; y: number}; b: {x: number; y: number}; k: number; color: string}> = ({a, b, k, color}) => <line x1={a.x} y1={a.y} x2={lerp(a.x, b.x, k)} y2={lerp(a.y, b.y, k)} stroke={color} strokeWidth={3} />;
const Lights = () => <><ambientLight intensity={.8} /><directionalLight position={[-6, 14, 9]} intensity={2.2} castShadow shadow-mapSize-width={1024} shadow-mapSize-height={1024} shadow-camera-left={-14} shadow-camera-right={14} shadow-camera-top={14} shadow-camera-bottom={-14} /><directionalLight position={[8, 4, -6]} intensity={.7} /></>;

const part = z.object({label: z.string(), shape: z.enum(['disc', 'box', 'gear']).default('disc'), r: z.number().default(1.8), h: z.number().default(.5), color: z.string().optional()});
const schema = z.object({...baseProps, object: z.string(), purpose: z.string().optional(), parts: z.array(part).min(2).max(6), schematic: z.boolean().default(true), source: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {materialize: [0, 18], assemble: [19, 32], separate: [33, 66], callouts: [67, 89]};
const Part: React.FC<{d: z.output<typeof part>; col: string; op: number}> = ({d, col, op}) => {
  const m = <meshStandardMaterial color={col} metalness={.35} roughness={.45} transparent={op < 1} opacity={op} />;
  if (d.shape === 'box') return <mesh castShadow receiveShadow><boxGeometry args={[d.r * 1.7, d.h, d.r * 1.7]} />{m}</mesh>;
  if (d.shape === 'gear') return <group><mesh castShadow><cylinderGeometry args={[d.r * .86, d.r * .86, d.h, 48]} />{m}</mesh>{Array.from({length: 14}, (_, i) => <mesh key={i} castShadow rotation={[0, i / 14 * 6.283, 0]} position={[Math.cos(i / 14 * 6.283) * d.r * .95, 0, -Math.sin(i / 14 * 6.283) * d.r * .95]}><boxGeometry args={[d.r * .22, d.h, d.r * .24]} />{m}</mesh>)}</group>;
  return <mesh castShadow receiveShadow><cylinderGeometry args={[d.r, d.r, d.h, 64]} />{m}</mesh>;
};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const P_ = s.portrait; const ma = beat('materialize', Ease.out), as = beat('assemble', Ease.out), se = beat('separate', Ease.linear), ca = beat('callouts', Ease.out);
  const n = p.parts.length; const tones = ['#D9D2C2', '#FFB224', '#8A8579', '#C97B3A', '#5F6F73', '#EADFC8'];
  const heights = p.parts.map((d) => d.h); const closed = heights.reduce((a, b) => a + b, 0); const gapMax = P_ ? 1.5 : .95;
  const sep = (i: number) => Ease.io(clamp(se * (n + 1) / 2 - i * (n - 1) / (2 * Math.max(1, n - 1)) * 1)); const gapOf = (i: number) => sep(n - 1 - i) * gapMax;
  let y = 0; const ys = [...p.parts].reverse().map((d, ri) => { const c = y + d.h / 2 + gapOf(ri) * ri; y += d.h; return c; }).reverse();
  const total = ys[0] + p.parts[0].h / 2; const a = lerp(-.6, -.15, as) + se * .35 + ca * .05; const R = P_ ? 19.5 : 16.5;
  const lookX = P_ ? 0 : -2.3; const cam = useCamera({pos: [Math.sin(a) * R + lookX, total / 2 + (P_ ? 5.6 : 4), Math.cos(a) * R], look: [lookX, total / 2, 0], fov: P_ ? 38 : 28});
  void closed;
  const labels = p.parts.map((d, i) => { const anchor = project(cam, P_ ? [0, ys[i] + d.h / 2 + .44, 0] : [-d.r * .96, ys[i], 0], s.W, s.H); return {anchor, d, i}; }).sort((x, y2) => x.anchor.y - y2.anchor.y);
  const lx = P_ ? s.x1 - 8 : s.x0 + 30; let last = -1e9; const placed = labels.map((l) => { const yy = Math.max(l.anchor.y, last + 88, s.y0 + 180); last = yy; return {...l, y: yy}; });
  return <AbsoluteFill style={{background: 'radial-gradient(90% 70% at 50% 46%, #2b2925 0%, #070707 100%)'}}>
    <Stage3D cam={cam} shadows><Lights />{p.parts.map((d, i) => <group key={i} position={[0, ys[i], 0]} rotation={[0, se * (i % 2 ? .3 : -.3), 0]}><Part d={d} col={d.color ?? tones[i % 6]} op={lerp(clamp(ma), 1, as)} /></group>)}</Stage3D>
    <svg width={s.W} height={s.H} style={{position: 'absolute'}}>{P_ ? null : placed.map((l, j) => <Stem key={l.i} a={l.anchor} b={{x: P_ ? l.anchor.x : lx + 420, y: l.y}} k={clamp(ca * n - j)} color={pal.amber} />)}</svg>
    {placed.map((l, j) => { const k = clamp(ca * n - j); return <div key={l.i} style={{position: 'absolute', left: P_ ? l.anchor.x : lx, top: P_ ? l.anchor.y - 34 : l.y - 34, opacity: k, background: 'rgba(10,10,10,.82)', borderRadius: 12, padding: '4px 16px', transform: P_ ? 'translateX(-50%)' : undefined}}><Text px={40} maxW={P_ ? 420 : 400}>{l.d.label}</Text></div>; })}
    <div style={{position: 'absolute', left: s.x0, top: s.y0 + 20}}><Text px={P_ ? 62 : 58} maxW={s.sw}>{p.object}</Text></div>
    {p.schematic ? <div style={{position: 'absolute', left: s.x0, top: s.y0 + (P_ ? 100 : 88)}}><Text px={34} kind="mono" bold color={GREY}>{p.language === 'te' ? 'నమూనా చిత్రం' : 'SCHEMATIC'}</Text></div> : null}
  </AbsoluteFill>;
};
export default defineEffect({number: 2, slug: 'teardown', name: 'Teardown', group: '3D Scenes', frames: 90, beats, schema, Component, samples: S('teardown'), facts: (p) => [{what: `anatomy of ${p.object}`, source: p.source}]});

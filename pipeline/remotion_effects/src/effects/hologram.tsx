import React, {useMemo} from 'react';
import {AbsoluteFill, continueRender, delayRender, staticFile} from 'remotion';
import {z} from 'zod';
import * as THREE from 'three';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, clamp, Ease, lerp, Para, Pill, seeded, SourceLine, Text, useBeats, useStage, Beats} from '../lib/kit';
import {GREY, usePalette} from '../lib/brand';
import {project, Stage3D, useCamera, useOrtho} from '../lib/three';
const Stem: React.FC<{a: {x: number; y: number}; b: {x: number; y: number}; k: number; color: string}> = ({a, b, k, color}) => <line x1={a.x} y1={a.y} x2={lerp(a.x, b.x, k)} y2={lerp(a.y, b.y, k)} stroke={color} strokeWidth={3} />;

const schema = z.object({...baseProps, title: z.string(), targets: z.array(z.object({label: z.string(), part: z.enum(['dish', 'panel', 'body'])})).length(2), schematic: z.boolean().default(true), source: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {emit: [0, 20], glow: [21, 34], target: [35, 49], hold: [50, 59]};
const TEAL = '#5FF3E4';
type Pc = {g: THREE.BufferGeometry; pos: [number, number, number]; rot?: [number, number, number]; key: string};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat, frame} = useBeats(beats, p); const P_ = s.portrait; const em = beat('emit', Ease.linear), gl = beat('glow', Ease.out), ta = beat('target', Ease.out), ho = beat('hold', Ease.linear);
  const H_ = 6.2, y0 = .35; const scanY = y0 + em * H_; const secondary = ho > 0 && ho < 1 ? y0 + ho * H_ : null; const plane = useMemo(() => new THREE.Plane(new THREE.Vector3(0, -1, 0), 0), []); plane.constant = scanY;
  const parts: Pc[] = useMemo(() => [{g: new THREE.CylinderGeometry(.95, .95, 2.3, 16, 3), pos: [0, 2.7, 0], key: 'body'}, {g: new THREE.BoxGeometry(2.4, .08, 1.0, 6, 1, 3), pos: [-2.2, 2.9, 0], key: 'panel'}, {g: new THREE.BoxGeometry(2.4, .08, 1.0, 6, 1, 3), pos: [2.2, 2.9, 0], key: 'panelR'}, {g: new THREE.ConeGeometry(1.25, .75, 24, 2, true), pos: [0, 4.95, 0], rot: [Math.PI, 0, 0], key: 'dish'}, {g: new THREE.CylinderGeometry(.06, .06, 1, 8), pos: [0, 4.2, 0], key: 'mast'}, {g: new THREE.CylinderGeometry(.5, .95, .55, 16, 1), pos: [0, 1.28, 0], key: 'base'}], []);
  const spin = Math.max(0, frame - 21) * .028; const G = useMemo(() => new THREE.Group(), []); G.rotation.y = spin - .4; G.updateMatrixWorld(true);
  const lift = P_ ? 0 : 0; const cam = useCamera({pos: [0, P_ ? 6.2 : 6, P_ ? 17.5 : 13.5], look: [P_ ? 0 : 2.3, 3.15 + lift, 0], fov: P_ ? 34 : 30});
  const anchor = (k: string) => { const c = parts.find((x) => x.key === k)!; const v = new THREE.Vector3(...c.pos); const w = v.applyMatrix4(G.matrixWorld); return project(cam, [w.x, w.y, w.z], s.W, s.H); };
  const col = (t: number) => new THREE.Color(TEAL).lerp(new THREE.Color(pal.amber), t);
  return <AbsoluteFill style={{background: 'radial-gradient(80% 62% at 50% 62%, #0d2a2f 0%, #040708 100%)'}}>
    <Stage3D cam={cam} clip><mesh position={[0, .08, 0]}><cylinderGeometry args={[2.6, 2.9, .16, 64]} /><meshBasicMaterial color="#14312f" /></mesh><mesh position={[0, .18, 0]} rotation={[-Math.PI / 2, 0, 0]}><ringGeometry args={[2.1, 2.5, 72]} /><meshBasicMaterial color={TEAL} toneMapped={false} transparent opacity={.45 + em * .5} /></mesh>
      <mesh position={[0, y0 + (H_ * Math.max(em, .001)) / 2, 0]}><cylinderGeometry args={[2.35, 2.5, H_ * Math.max(em, .001), 48, 1, true]} /><meshBasicMaterial color={TEAL} transparent opacity={.025 + .03 * gl} side={THREE.DoubleSide} depthWrite={false} toneMapped={false} /></mesh>
      <primitive object={G}>{parts.map((c) => { const hot = p.targets.some((t) => c.key.startsWith(t.part)); const lc = hot ? col(ta) : new THREE.Color(TEAL); return <group key={c.key} position={c.pos} rotation={c.rot ?? [0, 0, 0]}><mesh geometry={c.g}><meshBasicMaterial color={lc} transparent opacity={.07 + gl * .1} clippingPlanes={[plane]} side={THREE.DoubleSide} depthWrite={false} toneMapped={false} /></mesh><lineSegments><edgesGeometry args={[c.g, 8]} /><lineBasicMaterial color={lc} clippingPlanes={[plane]} toneMapped={false} /></lineSegments></group>; })}</primitive>
      {em < 1 ? <mesh position={[0, scanY, 0]} rotation={[-Math.PI / 2, 0, 0]}><ringGeometry args={[2.0, 3.1, 64]} /><meshBasicMaterial color="#d8fff9" transparent opacity={.75} side={THREE.DoubleSide} toneMapped={false} depthWrite={false} /></mesh> : null}
      {secondary !== null ? <mesh position={[0, secondary, 0]} rotation={[-Math.PI / 2, 0, 0]}><ringGeometry args={[2.5, 2.9, 64]} /><meshBasicMaterial color={TEAL} transparent opacity={.4} side={THREE.DoubleSide} depthWrite={false} toneMapped={false} /></mesh> : null}</Stage3D>
    <svg width={s.W} height={s.H} style={{position: 'absolute'}}>{p.targets.map((t, i) => { const a = anchor(t.part); const k = clamp(ta * 2 - i * .8); const R = 44; return <g key={i} opacity={k} stroke={pal.amber} strokeWidth={4} fill="none"><circle cx={a.x} cy={a.y} r={R + (1 - k) * 60} /><line x1={a.x - R - 16} x2={a.x - R + 10} y1={a.y} y2={a.y} /><line x1={a.x + R - 10} x2={a.x + R + 16} y1={a.y} y2={a.y} /><Stem a={{x: a.x, y: a.y - R}} b={{x: P_ ? (i ? s.x1 - 60 : s.x0 + 60) : s.x1 - 330, y: P_ ? (i ? s.y0 + 210 : s.y0 + 134) : s.y0 + 240 + i * 150}} k={k} color={pal.amber} /></g>; })}</svg>
    {p.targets.map((t, i) => { const k = clamp(ta * 2 - i * .8); return <div key={i} style={{position: 'absolute', ...(P_ ? (i ? {right: s.W - s.x1, top: s.y0 + 170} : {left: s.x0, top: s.y0 + 96}) : {left: s.x1 - 480, top: s.y0 + 200 + i * 150}), opacity: k}}><Pill px={40} maxW={P_ ? 480 : 470}>{t.label}</Pill></div>; })}
    <div style={{position: 'absolute', left: s.x0, top: s.y0 + 8}}><Text px={P_ ? 66 : 64} maxW={s.sw - (P_ ? 0 : 320)}>{p.title}</Text></div>
    {p.schematic ? <div style={{position: 'absolute', left: s.x0, top: s.y1 - 58}}><Text px={34} kind="mono" bold color={GREY}>{p.language === 'te' ? 'నమూనా భాగాలు' : 'SCHEMATIC PARTS'}</Text></div> : null}
  </AbsoluteFill>;
};
export default defineEffect({number: 5, slug: 'hologram', name: 'Hologram', group: '3D Scenes', frames: 60, beats, schema, Component, samples: S('hologram'), facts: (p) => [{what: `model of ${p.title}`, source: p.source}]});

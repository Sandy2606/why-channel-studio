import React, {useMemo} from 'react';
import {AbsoluteFill, continueRender, delayRender, staticFile} from 'remotion';
import {z} from 'zod';
import * as THREE from 'three';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, clamp, Ease, lerp, Para, Pill, seeded, SourceLine, Text, useBeats, useStage, Beats} from '../lib/kit';
import {GREY, usePalette} from '../lib/brand';
import {project, Stage3D, useCamera, useOrtho} from '../lib/three';
const Stem: React.FC<{a: {x: number; y: number}; b: {x: number; y: number}; k: number; color: string}> = ({a, b, k, color}) => <line x1={a.x} y1={a.y} x2={lerp(a.x, b.x, k)} y2={lerp(a.y, b.y, k)} stroke={color} strokeWidth={3} />;

const schema = z.object({...baseProps, object: z.string(), facts: z.array(z.object({text: z.string(), detail: z.string().optional(), height: z.number().min(0).max(1), source: z.string().optional()})).length(3), provenance: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {light: [0, 13], first: [14, 30], more: [31, 46], finish: [47, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat, frame} = useBeats(beats, p); const P_ = s.portrait; const li = beat('light', Ease.out), f1 = beat('first', Ease.out), mo = beat('more', Ease.linear), fi = beat('finish', Ease.out);
  const prof = useMemo(() => [[0, 0], [.9, 0], [1.05, .1], [1.0, .4], [1.5, 1.1], [1.72, 2], [1.5, 3], [.95, 3.6], [.85, 4], [1.05, 4.35], [1.15, 4.5], [1.0, 4.45], [.72, 4.0], [0, 3.9]].map(([x, y]) => new THREE.Vector2(x, y)), []); const geo = useMemo(() => new THREE.LatheGeometry(prof, 96), [prof]);
  const rot = frame * .022 - .5; const cam = useCamera({pos: [0, 4.2, P_ ? 15.5 : 12.5], look: [P_ ? 0 : 2.3, 2.15, 0], fov: P_ ? 36 : 28});
  const profR = (h: number) => { const Y = h * 4.5; for (let i = 1; i < prof.length; i++) if (prof[i].y >= Y && prof[i].y > prof[i - 1].y) { const k = (Y - prof[i - 1].y) / ((prof[i].y - prof[i - 1].y) || 1); return lerp(prof[i - 1].x, prof[i].x, k); } return 1; };
  const anchors = p.facts.map((f, i) => project(cam, [profR(f.height) * .94 * (i === 1 ? -1 : 1), f.height * 4.5, profR(f.height) * .34], s.W, s.H));
  const ks = [f1, clamp(mo * 2), clamp(mo * 2 - 1)];
  const tx = (i: number) => P_ ? (i === 1 ? s.x0 + 10 : s.x1 - 10) : s.x1 - 16, ty = (i: number) => P_ ? [s.y0 + 150, s.y0 + 250, s.y1 - 96][i] : s.y0 + 190 + i * 196;
  return <AbsoluteFill style={{background: `radial-gradient(70% 62% at 50% 56%, rgb(${lerp(46, 94, li)},${lerp(40, 80, li)},${lerp(32, 62, li)}) 0%, #0d0b09 100%)`}}>
    <Stage3D cam={cam} shadows><ambientLight intensity={.55 + li * .6} /><spotLight position={[-5, 12, 7]} intensity={li * 260} angle={.6} penumbra={.7} castShadow shadow-mapSize-width={1024} shadow-mapSize-height={1024} /><directionalLight position={[6, 4, 6]} intensity={.9} />
      <group rotation={[0, rot, 0]}><mesh position={[0, -.14, 0]} receiveShadow><cylinderGeometry args={[3.1, 3.3, .28, 96]} /><meshStandardMaterial color="#2C2A26" metalness={.2} roughness={.55} /></mesh><mesh geometry={geo} castShadow receiveShadow><meshStandardMaterial color="#B56A32" metalness={.62} roughness={.36} side={THREE.DoubleSide} /></mesh>
        {[1.2, 2.0, 2.8].map((y, i) => <mesh key={i} position={[0, y, 0]} rotation={[Math.PI / 2, 0, 0]}><torusGeometry args={[profR(y / 4.5) + .012, .018, 8, 96]} /><meshStandardMaterial color="#E3B765" metalness={.8} roughness={.3} /></mesh>)}<mesh position={[1.72, 2, 0]}><sphereGeometry args={[.2, 20, 16]} /><meshStandardMaterial color="#E3B765" metalness={.8} roughness={.3} /></mesh><mesh position={[-1.72, 2, 0]}><sphereGeometry args={[.2, 20, 16]} /><meshStandardMaterial color="#E3B765" metalness={.8} roughness={.3} /></mesh></group></Stage3D>
    <svg width={s.W} height={s.H} style={{position: 'absolute'}}>{p.facts.map((f, i) => { const k = ks[i]; const a = anchors[i]; return <g key={i}><Stem a={a} b={{x: P_ ? tx(i) + (i === 1 ? 170 : -170) : s.x1 - 500, y: ty(i) + (P_ ? (i === 2 ? -10 : 56) : 30)}} k={k} color={pal.amber} /><circle cx={a.x} cy={a.y} r={9 * k} fill={pal.amber} /></g>; })}</svg>
    {p.facts.map((f, i) => { const k = ks[i]; return <div key={i} style={{position: 'absolute', ...(P_ ? (i === 1 ? {left: tx(i)} : {right: s.W - tx(i)}) : {left: s.x1 - 500}), top: ty(i), opacity: k, background: 'rgba(10,10,10,.8)', padding: '8px 18px', borderRadius: 12, maxWidth: P_ ? 620 : 500}}><Text px={46} maxW={P_ ? 570 : 460} color={pal.amber}>{f.text}</Text>{f.detail ? <div><Text px={34} kind="mono" maxW={P_ ? 570 : 460}>{f.detail}</Text></div> : null}</div>; })}
    <div style={{position: 'absolute', left: s.cx, top: s.y0 + 18, transform: `translateX(-50%) translateY(${(1 - fi) * 12}px)`, opacity: fi}}><Text px={P_ ? 66 : 62} maxW={s.sw}>{p.object}</Text></div>
    <SourceLine x={P_ ? s.cx : s.x0} y={P_ ? s.y0 + 96 : s.y1 - 58} anchor={P_ ? 'center' : 'left'} maxW={P_ ? s.sw : 900} a={fi}>{p.provenance}</SourceLine>
  </AbsoluteFill>;
};
export default defineEffect({number: 11, slug: 'turntable', name: 'Turntable', group: '3D Scenes', frames: 60, beats, schema, Component, samples: S('turntable'), facts: (p) => p.facts.map((f) => ({what: `fact "${f.text}"`, source: f.source}))});

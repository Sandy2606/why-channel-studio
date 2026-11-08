import React, {useMemo} from 'react';
import {AbsoluteFill, continueRender, delayRender, staticFile} from 'remotion';
import {z} from 'zod';
import * as THREE from 'three';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, clamp, Ease, lerp, Para, Pill, seeded, SourceLine, Text, useBeats, useStage, Beats} from '../lib/kit';
import {GREY, usePalette} from '../lib/brand';
import {project, Stage3D, useCamera, useOrtho} from '../lib/three';
const schema = z.object({...baseProps, topic: z.string(), visible: z.string(), deeper: z.array(z.string()).length(3), scaleNote: z.string().optional(), source: z.string().optional()});
type P = z.output<typeof schema>;
const WL = .18, DEEP = 8.3, TIP = 2.5; const underW = (v: number) => (1.8 + 2.4 * Math.sin(Math.PI * v * .9)) * Math.pow(Math.max(0, 1 - v), .35);
const beats: Beats = {surface: [0, 14], dive: [15, 36], pull: [37, 52], hold: [53, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const P_ = s.portrait; const di = beat('dive', Ease.io), pu = beat('pull', Ease.io), ho = beat('hold');
  const geo = useMemo(() => { const g = new THREE.IcosahedronGeometry(1, 18); const pos = g.attributes.position; for (let i = 0; i < pos.count; i++) { const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i), rxz = Math.hypot(x, z) || 1e-6; const m = 1 + Math.sin(x * 6 + 1.3) * .08 + Math.cos(z * 7 + .7) * .08 + Math.sin(y * 9 + x * 5) * .06; const under = y < WL; const v = under ? (WL - y) / (1 + WL) : (y - WL) / (1 - WL); const wide = (under ? underW(v) : 1.8 * Math.pow(Math.max(0, 1 - v), .8)) * m; pos.setXYZ(i, x / rxz * wide, under ? -v * DEEP : v * TIP, z / rxz * wide); } const out = g.index ? g.toNonIndexed() : g; out.computeVertexNormals(); return out; }, []);
  const camY = lerp(lerp(2.2, -5.2, di), -.06, pu), camZ = lerp(lerp(P_ ? 12 : 10, P_ ? 11 : 10, di), P_ ? 27 : 18.5, pu), lookY = lerp(lerp(1.5, -4.2, di), P_ ? -3 : -2.6, pu); const lookX = P_ ? 0 : lerp(0, 2.4, pu);
  const cam = useCamera({pos: [lookX * .3, camY, camZ], look: [lookX, lookY, 0], fov: P_ ? 36 : 32});
  const hz = project(cam, [0, 0, -400], s.W, s.H).y; const line = project(cam, [0, 0, 0], s.W, s.H).y; const depths = [-1.8, -4.8, -7.8];
  const anchors = depths.map((y, i) => project(cam, [underW(-y / DEEP) * .82 * (P_ ? (i % 2 ? -1 : 1) : 1), y, underW(-y / DEEP) * .3], s.W, s.H)); const tipP = project(cam, [0, 2.5, 0], s.W, s.H);
  const ks = depths.map((_, i) => clamp((di - .32 - i * .2) / .2 ) * clamp(1)); const waterBelow = clamp(line / s.H);
  return <AbsoluteFill style={{background: `linear-gradient(180deg, #BFE2EF 0%, #E8F2F2 ${Math.max(0, hz / s.H * 100)}%, #1B6D87 ${Math.max(0, hz / s.H * 100) + .05}%, #0A3346 ${Math.min(100, waterBelow * 100 + 45)}%, #041522 100%)`}}>
    <Stage3D cam={cam}><ambientLight intensity={1.1} /><directionalLight position={[-6, 10, 10]} intensity={2.2} /><directionalLight position={[5, -8, 8]} intensity={1.0} color="#7fd4f0" /><mesh geometry={geo}><meshStandardMaterial color="#E9F7FB" roughness={.55} flatShading /></mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[400, 400]} /><meshBasicMaterial color="#2A8AA8" transparent opacity={.34} side={THREE.DoubleSide} depthWrite={false} /></mesh></Stage3D>
    <svg width={s.W} height={s.H} style={{position: 'absolute'}}>{p.deeper.map((_, i) => <circle key={i} cx={anchors[i].x} cy={anchors[i].y} r={9 * ks[i]} fill={pal.amber} />)}{p.deeper.map((_, i) => { const lblX = P_ ? anchors[i].x + (i % 2 ? -24 : 24) : s.x1 - 470; return <line key={i} x1={anchors[i].x} y1={anchors[i].y} x2={lerp(anchors[i].x, lblX, ks[i])} y2={anchors[i].y} stroke={pal.amber} strokeWidth={3} />; })}</svg>
    {p.deeper.map((t, i) => <div key={i} style={{position: 'absolute', ...(P_ ? (i % 2 ? {left: Math.max(s.x0, anchors[i].x - 460)} : {left: Math.min(s.x1 - 460, anchors[i].x + 20)}) : {left: s.x1 - 470}), top: Math.max(s.y0 + 100, Math.min(s.y1 - 170 - (2 - i) * 84, anchors[i].y - 36)), opacity: ks[i]}}><Pill px={40} maxW={P_ ? 460 : 460}>{t}</Pill></div>)}
    {tipP.y > s.y0 + 40 && tipP.y < s.y1 ? <div style={{position: 'absolute', left: s.cx, top: Math.max(s.y0 + 104, tipP.y - 104), transform: 'translateX(-50%)'}}><Pill px={42} bg={pal.ink} color={pal.cream} maxW={s.sw}>{p.visible}</Pill></div> : null}
    <div style={{position: 'absolute', left: s.cx, top: s.y0 + 8, transform: 'translateX(-50%)', opacity: 1 - di * .0}}><Text px={P_ ? 62 : 62} maxW={s.sw} color={di > .5 ? pal.cream : pal.ink}>{p.topic}</Text></div>
    {p.scaleNote ? <div style={{position: 'absolute', left: s.cx, top: s.y1 - 64, transform: 'translateX(-50%)', opacity: Math.max(pu, ho), background: 'rgba(4,21,34,.82)', borderRadius: 10, padding: '2px 16px'}}><Text px={34} kind="mono" maxW={s.sw - 40} color={pal.cream}>{p.scaleNote}</Text></div> : null}
  </AbsoluteFill>;
};
export default defineEffect({number: 14, slug: 'iceberg', name: 'Iceberg', group: '3D Scenes', frames: 60, beats, schema, Component, samples: S('iceberg'), facts: (p) => [{what: `factors for ${p.topic}`, source: p.source}]});

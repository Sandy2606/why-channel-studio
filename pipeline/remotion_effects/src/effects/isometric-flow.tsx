import React, {useMemo} from 'react';
import {AbsoluteFill, continueRender, delayRender, staticFile} from 'remotion';
import {z} from 'zod';
import * as THREE from 'three';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, clamp, Ease, lerp, Para, Pill, seeded, SourceLine, Text, useBeats, useStage, Beats} from '../lib/kit';
import {GREY, usePalette} from '../lib/brand';
import {project, Stage3D, useCamera, useOrtho} from '../lib/three';
const Lights = () => <><ambientLight intensity={.8} /><directionalLight position={[-6, 14, 9]} intensity={2.2} castShadow shadow-mapSize-width={1024} shadow-mapSize-height={1024} shadow-camera-left={-14} shadow-camera-right={14} shadow-camera-top={14} shadow-camera-bottom={-14} /><directionalLight position={[8, 4, -6]} intensity={.7} /></>;

const schema = z.object({...baseProps, stages: z.array(z.string()).min(3).max(5), simplified: z.boolean().default(true), source: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {drop: [0, 12], travel: [13, 35], connect: [36, 49], pull: [50, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat, frame, range} = useBeats(beats, p); const P_ = s.portrait; const pu = beat('pull', Ease.io); const n = p.stages.length;
  const pts = useMemo(() => p.stages.map((_, i) => { const u = i / (n - 1) - .5; const swing = (i % 2 ? 1 : -1) * 1.7; return P_ ? new THREE.Vector3(u * 10 + swing * .7, 0, u * 10 - swing * .7) : new THREE.Vector3(u * 11 + swing * .75, 0, -u * 11 + swing * .75); }), [n, P_]);
  const curve = useMemo(() => new THREE.CatmullRomCurve3(pts, false, 'catmullrom', .45), [pts]); const a = range.drop[0], b = range.connect[1]; const u = clamp((frame - 6 - a) / (b - 6 - a)); const uE = Ease.io(u); const tok = curve.getPointAt(uE); curve.arcLengthDivisions = 240;
  const arrive = (i: number) => a + i / (n - 1) * (b - a - 6) + 2 - (i ? 4 : 0); const landK = (i: number) => Ease.back(clamp((frame - arrive(i)) / 8));
  const trackPts = useMemo(() => curve.getSpacedPoints(160), [curve]); const showN = Math.max(2, Math.ceil(uE * 160)); const prog = useMemo(() => new THREE.CatmullRomCurve3(trackPts.slice(0, showN + 1)), [trackPts, showN]);
  const viewH = lerp(P_ ? 21 : 16.5, P_ ? 24 : 18.5, pu), lookOff = lerp(.6, 0, pu); const cam = useOrtho({pos: [24, 24, 24], look: [lookOff, 0, lookOff], viewH});
  const bh = [1.2, 2.2, 1.5, 2.6, 1.3];
  return <AbsoluteFill style={{background: pal.cream}}>
    <Stage3D cam={cam} shadows><Lights />
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -.02, 0]} receiveShadow><planeGeometry args={[70, 70]} /><shadowMaterial opacity={.2} /></mesh>
      <mesh><tubeGeometry args={[curve, 160, .13, 8, false]} /><meshStandardMaterial color="#C8BFAB" /></mesh>
      <mesh position={[0, .08, 0]}><tubeGeometry args={[prog, 160, .15, 8, false]} /><meshBasicMaterial color={pal.amber} toneMapped={false} /></mesh>
      {p.stages.map((_, i) => { const k = landK(i); if (frame < arrive(i)) return null; const h = bh[i % 5]; return <group key={i} position={[pts[i].x, Math.max(0, (1 - k) * 8), pts[i].z]}><mesh position={[0, .15, 0]} receiveShadow castShadow><cylinderGeometry args={[1.5, 1.5, .3, 48]} /><meshStandardMaterial color="#F8F4E8" /></mesh><mesh position={[0, .3 + h / 2, 0]} castShadow><boxGeometry args={[1.45, h, 1.45]} /><meshStandardMaterial color={i === n - 1 ? pal.amber : '#4A4640'} /></mesh></group>; })}
      <group position={[tok.x, .42, tok.z]}><mesh castShadow><boxGeometry args={[.72, .42, .72]} /><meshStandardMaterial color={pal.amber} emissive={pal.amber} emissiveIntensity={.3} /></mesh></group>
    </Stage3D>
    {p.stages.map((t, i) => { const k = clamp((frame - arrive(i) - 2) / 6); if (k <= 0) return null; const q = project(cam, [pts[i].x, .3 + bh[i % 5] + 1.2, pts[i].z], s.W, s.H); return <div key={i} style={{position: 'absolute', left: Math.min(s.x1 - 150, Math.max(s.x0 + 150, q.x)), top: q.y - 34, transform: `translateX(-50%) scale(${k})`}}><Pill px={P_ ? 44 : 42} bg={i === n - 1 ? pal.amber : pal.ink} color={i === n - 1 ? pal.ink : pal.cream} maxW={420}>{t}</Pill></div>; })}
    {p.simplified ? <div style={{position: 'absolute', left: s.x0, top: s.y1 - 58}}><Text px={34} kind="mono" bold color="#5b5650">{p.language === 'te' ? 'సులభీకరించిన ప్రయాణం' : 'SIMPLIFIED JOURNEY'}</Text></div> : null}
  </AbsoluteFill>;
};
export default defineEffect({number: 10, slug: 'isometric-flow', name: 'Isometric Flow', group: '3D Scenes', frames: 60, beats, schema, Component, samples: S('isometric-flow'), facts: (p) => [{what: 'journey stages', source: p.source}]});

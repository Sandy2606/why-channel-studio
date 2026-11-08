import React, {useMemo} from 'react';
import {z} from 'zod';
import * as THREE from 'three';
import en from '../../../samples/map-route.en.json';
import te from '../../../samples/map-route.te.json';
import {defineEffect} from '../../lib/define';
import {baseProps, clamp, Ease, lerp, Pill, seeded, SourceLine, Text, useBeats, useStage} from '../../lib/kit';
import {usePalette} from '../../lib/brand';
import {project, Stage3D, useCamera} from '../../lib/three';

const schema = z.object({...baseProps, origin: z.string(), destination: z.string(), distance: z.string().optional(), travelLabel: z.string().optional(),
  /** Grid points on street lines (even numbers, -10..10). */
  route: z.array(z.tuple([z.number(), z.number()])).min(2).default([[-8, 8], [-8, 2], [-2, 2], [-2, -4], [6, -4], [6, -8]]),
  routeSource: z.string().optional(), distanceSource: z.string().optional()});
type P = z.output<typeof schema>;
const beats = {establish: [0, 14], draw: [15, 50], arrive: [51, 73], widen: [74, 89]} as Record<string, [number, number]>;

const riverX = (z_: number) => 11.5 + 2.2 * Math.sin(z_ / 4.2);

function along(route: [number, number][], k: number) {
  const seg = route.slice(1).map((b, i) => Math.hypot(b[0] - route[i][0], b[1] - route[i][1])); const L = seg.reduce((a, b) => a + b, 0); let d = k * L; const pts: [number, number][] = [route[0]];
  for (let i = 0; i < seg.length; i++) {
    if (d >= seg[i]) { pts.push(route[i + 1]); d -= seg[i]; continue; }
    pts.push([lerp(route[i][0], route[i + 1][0], d / seg[i]), lerp(route[i][1], route[i + 1][1], d / seg[i])]); break;
  }
  return pts;
}

const distTo = (x: number, z: number, r: [number, number][]) => Math.min(...r.slice(1).map((b, i) => { const a = r[i], dx = b[0] - a[0], dz = b[1] - a[1], t = clamp(((x - a[0]) * dx + (z - a[1]) * dz) / (dx * dx + dz * dz || 1)); return Math.hypot(x - a[0] - t * dx, z - a[1] - t * dz); }));

const City: React.FC<{route: [number, number][]}> = ({route}) => {
  const data = useMemo(() => { const r = seeded('city'); const out: {x: number; z: number; h: number; w: number; d: number; tone: number}[] = []; const trees: [number, number][] = [];
    for (let x = -11; x <= 11; x += 2) for (let z = -13; z <= 13; z += 2) {
      if (Math.abs(x - riverX(z)) < 2.4) continue;
      if (r(`p${x}${z}`) < .14) { trees.push([x - .4, z + .3], [x + .4, z - .3], [x, z + .5]); continue; }
      const near = distTo(x, z, route) < 2.3;
      out.push({x, z, h: near ? .22 + r(`h${x}${z}`) * .3 : .35 + Math.pow(r(`h${x}${z}`), 2.2) * 2.6, w: 1.1 + r(`w${x}${z}`) * .35, d: 1.1 + r(`d${x}${z}`) * .35, tone: r(`t${x}${z}`)}); }
    return {out, trees}; }, [route]);
  const river = useMemo(() => { const s = new THREE.Shape(); const N = 40; const a: [number, number][] = [];
    for (let i = 0; i <= N; i++) { const z = lerp(-30, 30, i / N); a.push([riverX(z), z]); }
    a.forEach(([x, z], i) => i ? s.lineTo(x - 1.3, -z) : s.moveTo(x - 1.3, -z)); [...a].reverse().forEach(([x, z]) => s.lineTo(x + 1.3, -z)); s.closePath(); return new THREE.ShapeGeometry(s); }, []);
  return <group>
    <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow position={[0, -.02, 0]}><planeGeometry args={[140, 140]} /><meshStandardMaterial color="#141311" /></mesh>
    <mesh geometry={river} rotation={[-Math.PI / 2, 0, 0]} position={[0, .005, 0]}><meshStandardMaterial color="#17414d" roughness={.35} /></mesh>
    {Array.from({length: 17}, (_, i) => -16 + i * 2).filter((v) => v % 2 === 0).map((v) => <React.Fragment key={v}>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[v, .012, 0]}><planeGeometry args={[.46, 60]} /><meshStandardMaterial color="#2c2a27" /></mesh>
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, .012, v]}><planeGeometry args={[60, .46]} /><meshStandardMaterial color="#2c2a27" /></mesh></React.Fragment>)}
    {data.out.map((b, i) => <mesh key={i} position={[b.x, b.h / 2, b.z]} castShadow receiveShadow><boxGeometry args={[b.w, b.h, b.d]} /><meshStandardMaterial color={new THREE.Color('#3f3c37').lerp(new THREE.Color('#756f65'), b.tone)} roughness={.8} /></mesh>)}
    {data.trees.map(([x, z], i) => <mesh key={'t' + i} position={[x, .3, z]} castShadow><coneGeometry args={[.26, .7, 7]} /><meshStandardMaterial color="#4c7a5f" /></mesh>)}
  </group>;
};

const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const pT = s.portrait;
  const est = beat('establish', Ease.out), draw = beat('draw', Ease.io), arrive = beat('arrive', Ease.out), widen = beat('widen', Ease.io);
  const pts = along(p.route, draw); const tip = pts[pts.length - 1]; const end = p.route[p.route.length - 1]; const start = p.route[0];
  const mid: [number, number] = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2];
  // overhead over the origin, then riding the tip, then pulled back over both ends
  const fx = lerp(lerp(start[0], tip[0], clamp(draw * 1.05)), mid[0], widen), fz = lerp(lerp(start[1], tip[1], clamp(draw * 1.05)), mid[1], widen);
  const h = lerp(lerp(pT ? 13 : 9, pT ? 15 : 11, est), pT ? 34 : 33, widen), back = lerp(lerp(2, pT ? 8 : 9, est), pT ? 15 : 21, widen);
  const cam = useCamera({pos: [fx + lerp(0, -2.5, est), h, fz + back], look: [fx, 0, fz + lerp(0, -1, est)], fov: pT ? 46 : 34});
  const drop = 1 - arrive; const pinY = 1.25 + drop * 7;
  const P3 = (x: number, y: number, z: number) => project(cam, [x, y, z], s.W, s.H);
  const op = P3(start[0], .9, start[1]), dp = P3(end[0], pinY + 1.0, end[1]);
  const bound = (v: number, a: number, b: number) => Math.max(a, Math.min(b, v));
  const labelW = s.portrait ? 520 : 620;
  return <div style={{position: 'absolute', inset: 0, background: pal.ink}}>
    <Stage3D cam={cam} shadows>
      <ambientLight intensity={.75} /><directionalLight position={[-14, 24, 12]} intensity={2.1} castShadow shadow-mapSize-width={1024} shadow-mapSize-height={1024} shadow-camera-left={-40} shadow-camera-right={40} shadow-camera-top={40} shadow-camera-bottom={-40} />
      <City route={p.route} />
      {pts.slice(1).map((b, i) => { const a = pts[i]; const len = Math.hypot(b[0] - a[0], b[1] - a[1]); const cx = (a[0] + b[0]) / 2, cz = (a[1] + b[1]) / 2, ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
        return <group key={i} position={[cx, .05, cz]} rotation={[0, -ang, 0]}>
          <mesh><boxGeometry args={[len + .34, .05, .34]} /><meshBasicMaterial color={pal.amber} toneMapped={false} /></mesh>
          <mesh position={[0, -.01, 0]}><boxGeometry args={[len + .9, .02, .9]} /><meshBasicMaterial color={pal.amber} transparent opacity={.22} toneMapped={false} /></mesh></group>; })}
      {pts.slice(1, -1).map((c, i) => <mesh key={'j' + i} position={[c[0], .05, c[1]]}><cylinderGeometry args={[.17, .17, .05, 16]} /><meshBasicMaterial color={pal.amber} toneMapped={false} /></mesh>)}
      <mesh position={[tip[0], .3, tip[1]]}><sphereGeometry args={[.26 * (1 - arrive * .9), 24, 18]} /><meshBasicMaterial color="#FFF3D6" toneMapped={false} /></mesh>
      <mesh position={[tip[0], .3, tip[1]]}><sphereGeometry args={[.72 * (1 - arrive * .9), 24, 18]} /><meshBasicMaterial color={pal.amber} transparent opacity={.32} toneMapped={false} depthWrite={false} /></mesh>
      <mesh position={[start[0], .06, start[1]]}><cylinderGeometry args={[.55, .55, .05, 32]} /><meshBasicMaterial color={pal.cream} toneMapped={false} /></mesh>
      {arrive > 0 ? <group position={[end[0], pinY, end[1]]}>
        <mesh position={[0, .55, 0]} castShadow><sphereGeometry args={[.62, 28, 20]} /><meshStandardMaterial color={pal.amber} emissive={pal.amber} emissiveIntensity={.45} /></mesh>
        <mesh position={[0, -.32, 0]} rotation={[Math.PI, 0, 0]} castShadow><coneGeometry args={[.5, 1.3, 24]} /><meshStandardMaterial color={pal.amber} emissive={pal.amber} emissiveIntensity={.45} /></mesh>
        <mesh position={[0, .55, 0]}><sphereGeometry args={[.24, 18, 14]} /><meshBasicMaterial color={pal.ink} /></mesh></group> : null}
    </Stage3D>
    <div style={{position: 'absolute', left: bound(op.x, s.x0 + labelW / 2, s.x1 - labelW / 2), top: bound(op.y - 90, s.y0 + 80, s.y1 - 80), transform: 'translateX(-50%)', opacity: 1 - arrive * .0}}><Pill bg={pal.cream} maxW={labelW}>{p.origin}</Pill></div>
    {arrive > .25 ? <div style={{position: 'absolute', left: bound(dp.x, s.x0 + labelW / 2, s.x1 - labelW / 2), top: bound(dp.y - 96, s.y0 + 80, s.y1 - 80), transform: `translateX(-50%) scale(${clamp((arrive - .25) * 2.2)})`}}><Pill maxW={labelW}>{p.destination}</Pill></div> : null}
    {widen > 0 && (p.distance || p.travelLabel) ? (() => {
      // Sit in whichever safe corner is furthest from both map labels, so a route can never collide with it.
      const corners: [number, number, string, string][] = [[s.x0, s.y0 + 64, '0', 'left'], [s.x1, s.y0 + 64, '-100%', 'right'], [s.x0, s.y1 - 96, '0', 'left'], [s.x1, s.y1 - 96, '-100%', 'right']];
      const score = (c: [number, number, string, string]) => Math.min(Math.hypot(c[0] - op.x, c[1] - op.y), Math.hypot(c[0] - dp.x, c[1] - dp.y));
      const c = corners.reduce((best, x) => score(x) > score(best) ? x : best);
      return <div style={{position: 'absolute', left: c[0], top: c[1], transform: `translateX(${c[2]}) translateY(${(1 - widen) * 26}px)`, opacity: widen, background: 'rgba(10,10,10,.82)', borderRadius: 18, padding: '12px 30px', whiteSpace: 'nowrap'}}><Text px={52} maxW={s.sw - 140} color={pal.amber}>{[p.distance, p.travelLabel].filter(Boolean).join('  ·  ')}</Text></div>;
    })() : null}
    <SourceLine x={s.cx} y={s.y0 + 8} maxW={s.sw} a={1}>{p.routeSource}</SourceLine>
  </div>;
};

export default defineEffect({number: 1, slug: 'map-route', name: 'Map Route', group: '3D Scenes', frames: 90, beats, schema, Component, samples: {en, te},
  facts: (p) => [{what: `route ${p.origin} to ${p.destination}`, source: p.routeSource}, ...(p.distance ? [{what: `distance ${p.distance}`, source: p.distanceSource}] : [])]});

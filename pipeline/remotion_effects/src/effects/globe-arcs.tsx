import React, {useMemo} from 'react';
import {AbsoluteFill, continueRender, delayRender, staticFile} from 'remotion';
import {z} from 'zod';
import * as THREE from 'three';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, clamp, Ease, lerp, Para, Pill, seeded, SourceLine, Text, useBeats, useStage, Beats} from '../lib/kit';
import {GREY, usePalette} from '../lib/brand';
import {project, Stage3D, useCamera, useOrtho} from '../lib/three';
const point = z.object({name: z.string(), lat: z.number().min(-90).max(90), lon: z.number().min(-180).max(180)});
const schema = z.object({...baseProps, origin: point, destinations: z.array(point).min(1).max(12), metric: z.string(), dataSource: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {locate: [0, 10], launch: [11, 39], land: [40, 52], drift: [53, 59]};
const D2R = Math.PI / 180, R0 = 3;
const toV = (lat: number, lon: number) => new THREE.Vector3(Math.cos(lat * D2R) * Math.cos(lon * D2R), Math.sin(lat * D2R), -Math.cos(lat * D2R) * Math.sin(lon * D2R));
/** One landmass texture: every polygon the same fill and no outline, so no political borders can appear. */
function useLand() {
  const [tex, setTex] = React.useState<THREE.CanvasTexture | null>(null); const [h] = React.useState(() => delayRender('land texture'));
  React.useEffect(() => { fetch(staticFile('geo/land.geojson')).then((r) => r.json()).then((g) => { const c = document.createElement('canvas'); c.width = 2048; c.height = 1024; const x = c.getContext('2d')!; x.fillStyle = '#10222c'; x.fillRect(0, 0, 2048, 1024); x.fillStyle = '#6e7a68'; x.strokeStyle = '#6e7a68'; x.lineWidth = 2.5; x.lineJoin = 'round'; const ring = (r: number[][]) => { x.beginPath(); r.forEach(([lo, la], i) => { const px = (lo + 180) / 360 * 2048, py = (90 - la) / 180 * 1024; i ? x.lineTo(px, py) : x.moveTo(px, py); }); x.closePath(); x.fill(); x.stroke(); }; for (const f of g.features) { const co = f.geometry.type === 'MultiPolygon' ? f.geometry.coordinates : [f.geometry.coordinates]; for (const poly of co) ring(poly[0]); } const t = new THREE.CanvasTexture(c); t.anisotropy = 4; t.colorSpace = THREE.SRGBColorSpace; setTex(t); continueRender(h); }); }, [h]);
  return tex;
}
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat, frame, range} = useBeats(beats, p); const P_ = s.portrait; const tex = useLand(); const dr = beat('drift', Ease.io); const launchA = range.launch[0], launchLen = range.launch[1] - launchA; const n = p.destinations.length;
  const startOf = (i: number) => launchA + (launchLen * .55) * i / Math.max(1, n - 1 || 1), dur = launchLen * .45;
  const prog = (i: number) => Ease.io(clamp((frame - startOf(i)) / dur)); const landed = p.destinations.filter((_, i) => prog(i) >= 1).length;
  const o = toV(p.origin.lat, p.origin.lon); const dv = p.destinations.map((d) => toV(d.lat, d.lon));
  const avgLon = p.origin.lon; const turn = -(90 + avgLon) * D2R + frame * .0035; const tilt = p.origin.lat * D2R * .55;
  const cam = useCamera({pos: [0, 0, lerp(P_ ? 13.5 : 10.5, P_ ? 12.3 : 9.6, dr)], look: [0, 0, 0], fov: P_ ? 34 : 30}); const G = useMemo(() => new THREE.Group(), []); G.rotation.set(tilt, turn, 0, 'XYZ'); G.updateMatrixWorld(true);
  const arcs = useMemo(() => dv.map((v) => { const ang = o.angleTo(v); const pts: THREE.Vector3[] = []; const N = 80; const sinA = Math.sin(ang) || 1e-6; for (let i = 0; i <= N; i++) { const t = i / N; const q = o.clone().multiplyScalar(Math.sin((1 - t) * ang) / sinA).add(v.clone().multiplyScalar(Math.sin(t * ang) / sinA)).normalize().multiplyScalar(R0 * (1 + Math.sin(t * Math.PI) * .22 * Math.min(1, ang / 1.4) + .004)); pts.push(q); } return pts; }), [p.origin, p.destinations]);
  const screen = (v: THREE.Vector3, alt = 1.04) => { const w = v.clone().multiplyScalar(R0 * alt).applyMatrix4(G.matrixWorld); const front = w.z > .4; return {...project(cam, [w.x, w.y, w.z], s.W, s.H), front}; };
  const sp = screen(o);
  return <AbsoluteFill style={{background: 'radial-gradient(70% 55% at 50% 50%, #17242e 0%, #05070a 100%)'}}>
    <Stage3D cam={cam}><ambientLight intensity={1.9} /><directionalLight position={[-5, 4, 8]} intensity={1.6} />
      <primitive object={G}><mesh><sphereGeometry args={[R0, 96, 64]} />{tex ? <meshStandardMaterial map={tex} roughness={.85} /> : <meshStandardMaterial color="#10222c" />}</mesh>
        <mesh position={o.clone().multiplyScalar(R0 * 1.012)}><sphereGeometry args={[.1, 16, 12]} /><meshBasicMaterial color={pal.amber} toneMapped={false} /></mesh>
        {arcs.map((a, i) => { const k = prog(i); if (k <= 0) return null; const m = Math.max(2, Math.ceil(k * (a.length - 1))); const c = new THREE.CatmullRomCurve3(a.slice(0, m + 1)); return <React.Fragment key={i}><mesh><tubeGeometry args={[c, Math.max(4, m), .024, 8, false]} /><meshBasicMaterial color={pal.amber} toneMapped={false} /></mesh>{k < 1 ? <mesh position={a[m]}><sphereGeometry args={[.07, 12, 10]} /><meshBasicMaterial color="#FFF3D6" toneMapped={false} /></mesh> : <mesh position={dv[i].clone().multiplyScalar(R0 * 1.01)} quaternion={new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 0, 1), dv[i])}><ringGeometry args={[.07 + Ease.out(clamp((frame - startOf(i) - dur) / 8)) * .08, .1 + Ease.out(clamp((frame - startOf(i) - dur) / 8)) * .08, 32]} /><meshBasicMaterial color={pal.amber} transparent opacity={.95} toneMapped={false} side={THREE.DoubleSide} /></mesh>}</React.Fragment>; })}</primitive></Stage3D>
    {sp.front ? <div style={{position: 'absolute', left: Math.min(s.x1 - 260, Math.max(s.x0 + 160, sp.x)), top: sp.y + 28, transform: 'translateX(-50%)'}}><Pill px={38} bg={pal.cream}>{p.origin.name}</Pill></div> : null}
    {p.destinations.map((d, i) => { const q = screen(dv[i]); const k = clamp((frame - startOf(i) - dur) / 8); return k > 0 && q.front ? <div key={i} style={{position: 'absolute', left: Math.min(s.x1 - 180, Math.max(s.x0 + 130, q.x)), top: q.y - 66, transform: `translateX(-50%) scale(${k})`}}><Pill px={36}>{d.name}</Pill></div> : null; })}
    <div style={{position: 'absolute', left: s.cx, top: s.y0 + 20, transform: 'translateX(-50%)', textAlign: 'center'}}><Text px={P_ ? 150 : 110} color={pal.amber}>{`${landed}/${n}`}</Text><div style={{background: 'rgba(6,10,14,.72)', borderRadius: 12, padding: '2px 18px', display: 'inline-block'}}><Text px={46} maxW={s.sw - 40}>{p.metric}</Text></div></div>
    <SourceLine x={s.cx} y={s.y1 - 58} maxW={s.sw}>{p.dataSource}</SourceLine>
  </AbsoluteFill>;
};
export default defineEffect({number: 4, slug: 'globe-arcs', name: 'Globe Arcs', group: '3D Scenes', frames: 60, beats, schema, Component, samples: S('globe-arcs'), facts: (p) => [{what: 'connections and coordinates', source: p.dataSource}]});

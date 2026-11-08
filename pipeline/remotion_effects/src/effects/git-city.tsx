import React, {useMemo} from 'react';
import {AbsoluteFill, continueRender, delayRender, staticFile} from 'remotion';
import {z} from 'zod';
import * as THREE from 'three';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, clamp, Ease, lerp, Para, Pill, seeded, SourceLine, Text, useBeats, useStage, Beats} from '../lib/kit';
import {GREY, usePalette} from '../lib/brand';
import {project, Stage3D, useCamera, useOrtho} from '../lib/three';
const Lights = () => <><ambientLight intensity={.8} /><directionalLight position={[-6, 14, 9]} intensity={2.2} castShadow shadow-mapSize-width={1024} shadow-mapSize-height={1024} shadow-camera-left={-14} shadow-camera-right={14} shadow-camera-top={14} shadow-camera-bottom={-14} /><directionalLight position={[8, 4, -6]} intensity={.7} /></>;

const schema = z.object({...baseProps, metric: z.string(), unit: z.string().default(''), dateRange: z.string(), values: z.array(z.array(z.number().min(0))).optional(), source: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {grid: [0, 15], rise: [16, 38], orbit: [39, 69], peak: [70, 89]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat, frame} = useBeats(beats, p); const P_ = s.portrait; const ri = beat('rise', Ease.linear), or = beat('orbit', Ease.io), pe = beat('peak', Ease.out);
  const grid = useMemo(() => { if (p.values) return p.values; const r = seeded('gitcity'); return Array.from({length: P_ ? 12 : 18}, (_, a) => Array.from({length: 9}, (_x, b) => Math.round(Math.pow(r(`${a}-${b}`), 3) * 40))); }, [p.values, P_]);
  const rows = grid.length, cols = grid[0].length, flat = grid.flat(), max = Math.max(...flat, 1), n = flat.length, ST = 1.15; const MAXH = P_ ? 7 : 5.2; const peakV = Math.max(...flat); const span = Math.max(rows, cols) * ST;
  const w = (r: number, c: number) => { const k = (r + c) / (rows + cols - 2); return Ease.out(clamp(ri * 1.6 - k * .6)); };
  const low = useMemo(() => new THREE.Color('#3b3833'), []), hi = useMemo(() => new THREE.Color(pal.amber), [pal.amber]);
  const D = useMemo(() => new THREE.Object3D(), []); const tmp = useMemo(() => new THREE.Color(), []);
  const setRef = (m: THREE.InstancedMesh | null) => { if (!m) return; let i = 0; for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) { const v = grid[r][c], h = Math.max(.05, v / max * MAXH * w(r, c)); D.position.set((r - (rows - 1) / 2) * ST, h / 2, (c - (cols - 1) / 2) * ST); D.scale.set(1, h, 1); D.updateMatrix(); m.setMatrixAt(i, D.matrix); tmp.copy(low).lerp(hi, Math.pow(v / max, .6)); if (pe > 0 && v === peakV) tmp.lerp(new THREE.Color('#FFF4D6'), pe); m.setColorAt(i, tmp); i++; } m.instanceMatrix.needsUpdate = true; if (m.instanceColor) m.instanceColor.needsUpdate = true; };
  const ang = lerp(0, .75, or); const el = lerp(P_ ? 40 : 32, P_ ? 17 : 13, Ease.io(clamp(ri * .6 + or * .7))); const look: [number, number, number] = [0, or * MAXH * .22, 0]; const Rr = span * (P_ ? 3.05 : 1.55);
  const cam = useCamera({pos: [Math.sin(ang) * Rr * Math.cos(el * .0) * .78, el * (P_ ? 1.25 : .9), Math.cos(ang) * Rr * .78 + 1], look, fov: P_ ? 44 : 30}); void frame;
  return <AbsoluteFill style={{background: 'radial-gradient(90% 70% at 50% 55%, #24221f 0%, #070707 100%)'}}>
    <Stage3D cam={cam} shadows><Lights /><mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -.02, 0]} receiveShadow><planeGeometry args={[rows * ST + 2, cols * ST + 2]} /><meshStandardMaterial color="#191816" /></mesh>
      <instancedMesh ref={setRef} args={[undefined as any, undefined as any, n]} castShadow receiveShadow><boxGeometry args={[.96, 1, .96]} /><meshStandardMaterial roughness={.55} /></instancedMesh></Stage3D>
    <div style={{position: 'absolute', left: s.x0, top: s.y0 + 20}}><Text px={P_ ? 66 : 62} maxW={s.sw}>{p.metric}</Text><div><Text px={36} kind="mono" bold maxW={s.sw} color={GREY}>{p.dateRange}</Text></div></div>
    <div style={{position: 'absolute', left: s.x0, top: s.y1 - 96, opacity: pe}}><Pill px={46} maxW={s.sw}>{`${p.language === 'te' ? 'గరిష్ఠం' : 'PEAK'} ${peakV.toLocaleString('en-IN')}${p.unit ? ' ' + p.unit : ''}`}</Pill></div>
    <SourceLine x={s.x1} y={s.y1 - 76} anchor="right" maxW={P_ ? 360 : 800} a={pe}>{p.source}</SourceLine>
  </AbsoluteFill>;
};
export default defineEffect({number: 3, slug: 'git-city', name: 'Git City', group: '3D Scenes', frames: 90, beats, schema, Component, samples: S('git-city'), facts: (p) => [{what: `data for ${p.metric}`, source: p.values ? p.source : undefined}]});

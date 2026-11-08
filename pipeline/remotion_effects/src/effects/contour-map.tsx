import React, {useMemo} from 'react';
import {AbsoluteFill, continueRender, delayRender, staticFile} from 'remotion';
import {z} from 'zod';
import * as THREE from 'three';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, clamp, Ease, lerp, Para, Pill, seeded, SourceLine, Text, useBeats, useStage, Beats} from '../lib/kit';
import {GREY, usePalette} from '../lib/brand';
import {project, Stage3D, useCamera, useOrtho} from '../lib/three';
const schema = z.object({...baseProps, terrain: z.string(), crest: z.string(), keyLabels: z.tuple([z.string(), z.string()]), schematic: z.boolean().default(true), source: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {draw: [0, 12], lift: [13, 37], camera: [38, 52], reveal: [53, 59]};
function field(N: number) { const r = seeded('terrain'); const hash = (x: number, y: number) => r(`${x},${y}`); const vn = (x: number, y: number) => { const i = Math.floor(x), j = Math.floor(y), f = x - i, g = y - j, u = f * f * (3 - 2 * f), v = g * g * (3 - 2 * g); return lerp(lerp(hash(i, j), hash(i + 1, j), u), lerp(hash(i, j + 1), hash(i + 1, j + 1), u), v); };
  const h = new Float32Array((N + 1) * (N + 1)); let peak = 0, pi = 0; for (let j = 0; j <= N; j++) for (let i = 0; i <= N; i++) { const x = i / N, y = j / N, d = Math.hypot(x - .5, y - .5); const dome = Math.max(0, 1 - d * 2.05) ** 1.5; const n = vn(x * 5, y * 5) * .5 + vn(x * 10, y * 10) * .25 + vn(x * 20, y * 20) * .1; const v = dome * (.62 + n * .85) ; h[j * (N + 1) + i] = v; if (v > peak) { peak = v; pi = j * (N + 1) + i; } } for (let k = 0; k < h.length; k++) h[k] /= peak; return {h, pi}; }
const vs = 'attribute float aH; varying float vH; void main(){ vH=aH; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }';
const fsh = 'varying float vH; uniform float uShade; uniform float uDraw; void main(){ float lv=vH*11.; float w=fwidth(lv); float l=abs(fract(lv)-.5)/max(w,1e-4); float line=1.-smoothstep(.9,1.9,l); vec3 base=mix(vec3(.937,.902,.812),mix(vec3(.72,.56,.34),vec3(.97,.74,.33),vH),uShade*smoothstep(.0,.14,vH)); float ok=step(vH,uDraw+0.001)*smoothstep(.0,.03,vH); vec3 c=mix(base,vec3(.2,.13,.06),line*ok*.9); gl_FragColor=vec4(c,1.);} ';
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const P_ = s.portrait; const dr = beat('draw', Ease.out), li = beat('lift', Ease.io), ca = beat('camera', Ease.io), re = beat('reveal', Ease.out); const N = 200, SZ = 14, HM = 4.6;
  const {h, pi} = useMemo(() => field(N), []); const geo = useMemo(() => { const g = new THREE.PlaneGeometry(SZ, SZ, N, N); g.rotateX(-Math.PI / 2); g.setAttribute('aH', new THREE.BufferAttribute(h, 1)); return g; }, [h]);
  const pos = geo.attributes.position as THREE.BufferAttribute; for (let i = 0; i < pos.count; i++) pos.setY(i, h[i] * HM * li); pos.needsUpdate = true; geo.computeBoundingSphere();
  const uni = useMemo(() => ({uShade: {value: 0}, uDraw: {value: 0}}), []); uni.uShade.value = li; uni.uDraw.value = Math.max(.08, dr * 1.02);
  const yA = P_ ? 30 : 23, cam = useCamera({pos: [lerp(0, -4.5, ca), lerp(yA, P_ ? 12 : 9.2, ca), lerp(.01, P_ ? 21 : 16, ca)], look: [0, lerp(0, 1.6, ca), 0], fov: P_ ? 38 : 32});
  const px = pos.getX(pi), pz = pos.getZ(pi), py = pos.getY(pi), c = project(cam, [px, py + .1, pz], s.W, s.H);
  return <AbsoluteFill style={{background: '#EFE6CF'}}>
    <Stage3D cam={cam}><mesh geometry={geo}><shaderMaterial vertexShader={vs} fragmentShader={fsh} uniforms={uni} side={THREE.DoubleSide} /></mesh></Stage3D>
    <div style={{position: 'absolute', left: s.cx, top: s.y0 + 12, transform: 'translateX(-50%)', background: 'rgba(239,230,207,.9)', padding: '4px 22px', borderRadius: 12}}><Text px={P_ ? 66 : 64} maxW={s.sw - 60} color="#21170b">{p.terrain}</Text></div>
    {re > 0 ? <div style={{position: 'absolute', left: Math.min(s.x1 - 240, Math.max(s.x0 + 240, c.x)), top: Math.max(s.y0 + 110, c.y - 110), transform: `translateX(-50%) scale(${re})`}}><Pill px={44} maxW={560}>{p.crest}</Pill></div> : null}
    {re > 0 ? <div style={{position: 'absolute', left: s.x0, bottom: s.H - s.y1 + 16, display: 'flex', alignItems: 'center', gap: 14, opacity: re, background: 'rgba(239,230,207,.92)', borderRadius: 12, padding: '6px 18px'}}><Text px={34} kind="mono" bold color="#21170b">{p.keyLabels[0]}</Text><div style={{width: 150, height: 18, borderRadius: 9, background: 'linear-gradient(90deg,#B78F57,#F7BD54)'}} /><Text px={34} kind="mono" bold color="#21170b">{p.keyLabels[1]}</Text></div> : null}
    {p.schematic ? <div style={{position: 'absolute', right: s.W - s.x1, bottom: s.H - s.y1 + 24, opacity: Math.max(.9, re)}}><Text px={34} kind="mono" bold color="#21170b">{p.language === 'te' ? 'నమూనా భూభాగం' : 'SCHEMATIC'}</Text></div> : null}
  </AbsoluteFill>;
};
export default defineEffect({number: 7, slug: 'contour-map', name: 'Contour Map', group: '3D Scenes', frames: 60, beats, schema, Component, samples: S('contour-map'), facts: (p) => [{what: `terrain ${p.terrain}`, source: p.source}]});

import React, {useMemo} from 'react';
import {AbsoluteFill, continueRender, delayRender, staticFile} from 'remotion';
import {z} from 'zod';
import * as THREE from 'three';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, clamp, Ease, lerp, Para, Pill, seeded, SourceLine, Text, useBeats, useStage, Beats} from '../lib/kit';
import {GREY, usePalette} from '../lib/brand';
import {project, Stage3D, useCamera, useOrtho} from '../lib/three';
const schema = z.object({...baseProps, title: z.string(), headline: z.string(), tags: z.array(z.string()).max(3).default([]), panels: z.array(z.string()).length(2)});
type P = z.output<typeof schema>;
const beats: Beats = {approach: [0, 16], open: [17, 39], ui: [40, 52], settle: [53, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const P_ = s.portrait; const ap = beat('approach', Ease.out), op = beat('open', (t) => { const b = 1 - Math.pow(1 - t, 3); return b + Math.sin(t * 3.14) * .05; }), ui = beat('ui', Ease.linear), se = beat('settle', Ease.io);
  const W_ = 5.6, D_ = 3.8, TH = .2, LIDT = .14; const hinge = -Math.PI / 2 * 1.16 * op + 0;
  const cv = useMemo(() => { const c = document.createElement('canvas'); c.width = 1280; c.height = 830; return c; }, []); const tex = useMemo(() => { const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t; }, [cv]);
  const x = cv.getContext('2d')!; const fnt = (t: string, sz: number, mono?: boolean) => /[ఀ-౿]/.test(t) ? `900 ${Math.round(sz * .86)}px 'Noto Sans Telugu'` : mono ? `700 ${sz}px 'Space Mono'` : `400 ${sz}px 'Archivo Black'`; const fit = (t: string, sz: number, w: number, mono?: boolean) => { let z_ = sz; x.font = fnt(t, z_, mono); while (x.measureText(t).width > w && z_ > 16) { z_ -= 2; x.font = fnt(t, z_, mono); } };
  const wake = Math.max(0, (op - .55) / .45); x.fillStyle = `rgb(${10 + 8 * wake},${10 + 8 * wake},${11 + 8 * wake})`; x.fillRect(0, 0, 1280, 830); x.globalAlpha = 1; x.textBaseline = 'middle';
  if (wake > .4) { x.fillStyle = '#1b1a18'; x.fillRect(0, 0, 1280, 80); x.fillStyle = pal.amber; fit(p.title, 40, 900, true); x.fillText(p.title, 40, 42); }
  const a1 = clamp(ui / .4); x.globalAlpha = a1; x.fillStyle = pal.cream; fit(p.headline, 92, 1190); x.fillText(p.headline, 44, 208 + (1 - a1) * 18); x.globalAlpha = 1; p.panels.forEach((t, i) => { const k = clamp((ui - .35 - i * .22) / .3); x.globalAlpha = k; x.fillStyle = i ? '#26231d' : pal.amber; const px = 44 + i * 610, wd = 582; x.fillRect(px, 340 + (1 - k) * 26, wd, 420); x.fillStyle = i ? pal.cream : pal.ink; fit(t, 54, wd - 60); x.fillText(t, px + 30, 410 + (1 - k) * 26); x.globalAlpha = k * .35; for (let j = 0; j < 4; j++) x.fillRect(px + 30, 500 + j * 58 + (1 - k) * 26, (wd - 100) * (1 - j * .16), 22); }); x.globalAlpha = 1; tex.needsUpdate = true;
  const camA = lerp(0, .62, se) + lerp(.18, 0, ap); const R = lerp(P_ ? 22 : 12.5, P_ ? 18 : 10.2, ap); const cam = useCamera({pos: [Math.sin(camA) * R, lerp(5.6, 4, op), Math.cos(camA) * R + 1], look: [P_ ? 0 : 1.5 * se, lerp(.1, 1.5, op), -.3], fov: P_ ? 36 : 32});
  return <AbsoluteFill style={{background: 'radial-gradient(90% 75% at 50% 50%, #F8F4EA 0%, #D8D0C0 100%)'}}>
    <Stage3D cam={cam} shadows><ambientLight intensity={1.6} /><directionalLight position={[-5, 12, 8]} intensity={1.9} castShadow shadow-mapSize-width={1024} shadow-mapSize-height={1024} /><directionalLight position={[6, 3, 8]} intensity={.5} />
      <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -.01, 0]} receiveShadow><planeGeometry args={[60, 60]} /><shadowMaterial opacity={.26} /></mesh>
      <mesh position={[0, TH / 2, 0]} castShadow><boxGeometry args={[W_, TH, D_]} /><meshStandardMaterial color="#B7B2A8" metalness={.45} roughness={.4} /></mesh>
      <mesh position={[0, TH + .002, .25]}><boxGeometry args={[W_ - .5, .012, D_ - 1.5]} /><meshStandardMaterial color="#35332f" /></mesh>
      <mesh position={[0, TH + .002, D_ / 2 - .42]}><boxGeometry args={[1.5, .012, .62]} /><meshStandardMaterial color="#99948a" /></mesh>
      <group position={[0, TH + .0, -D_ / 2]} rotation={[hinge, 0, 0]}><mesh position={[0, LIDT / 2, D_ / 2]} castShadow><boxGeometry args={[W_, LIDT, D_]} /><meshStandardMaterial color="#C4BFB4" metalness={.5} roughness={.38} /></mesh>
        <mesh position={[0, -.003, D_ / 2]} rotation={[Math.PI / 2, 0, 0]}><planeGeometry args={[W_ - .2, D_ - .22]} /><meshBasicMaterial map={tex} toneMapped={false} /></mesh></group></Stage3D>
    {p.tags.map((t, i) => { const k = Ease.out(clamp((se + ui * .6) * 1.6 - i * .3)); const pos = P_ ? {left: s.x0 + i * 30, top: s.y1 - 250 + i * 86} : {left: s.x1 - 480 + (i % 2) * 70, top: s.y0 + 110 + i * 120}; return <div key={i} style={{position: 'absolute', ...pos, opacity: k, transform: `translateY(${(1 - k) * 18}px)`}}><Pill px={40} bg={pal.ink} color={pal.cream} maxW={P_ ? s.sw : 470}>{t}</Pill></div>; })}
  </AbsoluteFill>;
};
export default defineEffect({number: 9, slug: 'laptop-reveal', name: 'Laptop Reveal', group: '3D Scenes', frames: 60, beats, schema, Component, samples: S('laptop-reveal'), facts: () => []});

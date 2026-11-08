import React, {useMemo} from 'react';
import {AbsoluteFill, continueRender, delayRender, staticFile} from 'remotion';
import {z} from 'zod';
import * as THREE from 'three';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, clamp, Ease, lerp, Para, Pill, seeded, SourceLine, Text, useBeats, useStage, Beats} from '../lib/kit';
import {GREY, usePalette} from '../lib/brand';
import {project, Stage3D, useCamera, useOrtho} from '../lib/three';
const schema = z.object({...baseProps, event: z.string(), timeFrom: z.string(), timeTo: z.string(), caption: z.string(), uncertainty: z.string().optional(), source: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {establish: [0, 16], tighten: [17, 34], slow: [35, 47], resolve: [48, 59]};
const vs = 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0); }';
const fs = `varying vec2 vUv; uniform float uT; float n(vec2 p){ return fract(sin(dot(p,vec2(12.9898,78.233)))*43758.5453);} float vn(vec2 p){ vec2 i=floor(p),f=fract(p); f=f*f*(3.-2.*f); return mix(mix(n(i),n(i+vec2(1,0)),f.x),mix(n(i+vec2(0,1)),n(i+vec2(1,1)),f.x),f.y);} void main(){ vec2 p=vUv*2.-1.; float r=length(p); if(r>1.||r<.27) discard; float a=atan(p.y,p.x); float sp=a*2.+7./(r+.25)+uT; float b=vn(vec2(cos(sp),sin(sp))*2.4+r*7.)*.55+.45; float heat=pow(1.-(r-.27)/.73,1.5); vec3 c=mix(vec3(.5,.13,.02),vec3(1.,.7,.2),heat); c=mix(c,vec3(1.,.95,.78),pow(heat,5.)); float edge=smoothstep(1.,.74,r)*smoothstep(.27,.33,r); gl_FragColor=vec4(c*b*1.35,edge);} `;
const glowF = 'varying vec2 vUv; uniform vec3 uC; uniform float uA; void main(){ float r=length(vUv*2.-1.); float a=pow(max(0.,1.-r),2.2)*uA; gl_FragColor=vec4(uC,a);} ';
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat, frame, range} = useBeats(beats, p); const P_ = s.portrait; const ti = beat('tighten', Ease.io), sl = beat('slow', Ease.io), re = beat('resolve', Ease.out);
  const cam = useCamera({pos: [0, P_ ? 11 : 6.5, P_ ? 13.5 : 9], look: [0, 0, 0], fov: P_ ? 36 : 32});
  // Time pace: quick while tightening, then slowed through the decisive moment.
  const a0 = range.tighten[0], a1 = range.slow[0], clock = frame <= a1 ? frame * 1 : a1 + (frame - a1) * .28; void a0;
  const t = clamp(ti * .72 + sl * .28), R = lerp(5.4, 1.1, Math.pow(t, 1.3)); const ang = 2.2 + clock * .14 + t * 3.2; const body = [Math.cos(ang) * R, .06, Math.sin(ang) * R] as const; const fade = 1 - clamp(sl * 1.4 - .4);
  const uni = useMemo(() => ({uT: {value: 0}}), []); uni.uT.value = clock * .09;
  const r = seeded('stream'); const N = 900; const P = useMemo(() => new Float32Array(N * 3), []); let live = 0;
  for (let i = 0; i < N; i++) { const b = r(`b${i}`), lag = b * .95; const a = ang - lag * 2.1 - clock * .002; const rr = lerp(R, 1.08 + r(`z${i}`) * 1.8, Math.pow(b, 1.4)) + (r(`j${i}`) - .5) * .18; P[live * 3] = Math.cos(a) * rr; P[live * 3 + 1] = .06 + (r(`y${i}`) - .5) * .08; P[live * 3 + 2] = Math.sin(a) * rr; live++; }
  const key = Math.round(frame); const geo = useMemo(() => { const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(P, 3)); return g; }, [key]);
  const glowU = useMemo(() => ({uC: {value: new THREE.Color('#FFC070')}, uA: {value: 1}}), []); glowU.uA.value = fade;
  const yrs = t >= .999 ? p.timeTo : t > .01 ? p.timeFrom : p.timeFrom; const sta = clamp(t);
  return <AbsoluteFill style={{background: '#030308'}}>
    <Stage3D cam={cam}><mesh rotation={[-Math.PI / 2, 0, 0]}><planeGeometry args={[9.6, 9.6]} /><shaderMaterial vertexShader={vs} fragmentShader={fs} uniforms={uni} transparent side={THREE.DoubleSide} depthWrite={false} /></mesh>
      <mesh><sphereGeometry args={[1.3, 56, 40]} /><meshBasicMaterial color="#000000" /></mesh>
      <points geometry={geo}><pointsMaterial color={pal.amber} size={.05 * fade} transparent opacity={.85 * fade} sizeAttenuation depthWrite={false} toneMapped={false} /></points>
      {fade > 0 ? <group position={[body[0], body[1], body[2]]}><mesh><sphereGeometry args={[.18, 22, 16]} /><meshBasicMaterial color="#FFF1CC" toneMapped={false} /></mesh><mesh lookAt={cam.position as any}><planeGeometry args={[1.8, 1.8]} /><shaderMaterial vertexShader={vs} fragmentShader={glowF} uniforms={glowU} transparent depthWrite={false} /></mesh></group> : null}</Stage3D>
    <div style={{position: 'absolute', left: s.cx, top: s.y0 + 16, transform: 'translateX(-50%)', textAlign: 'center'}}><Text px={P_ ? 66 : 62} maxW={s.sw}>{p.event}</Text></div>
    <div style={{position: 'absolute', left: s.cx - (P_ ? s.sw / 2 - 30 : 320), width: P_ ? s.sw - 60 : 640, top: s.y0 + (P_ ? 112 : 88)}}><div style={{height: 6, background: '#34323a', borderRadius: 3}}><div style={{height: 6, width: `${sta * 100}%`, background: pal.amber, borderRadius: 3}} /></div><div style={{display: 'flex', justifyContent: 'space-between', marginTop: 8}}><Text px={36} kind="mono" bold color={pal.cream}>{p.timeFrom}</Text><Text px={36} kind="mono" bold color={t > .98 ? pal.amber : GREY}>{p.timeTo}</Text></div></div>
    <div style={{position: 'absolute', left: s.cx, top: P_ ? s.y1 - 140 : s.y1 - 120, transform: `translateX(-50%) translateY(${(1 - re) * 16}px)`, opacity: re, textAlign: 'center'}}><Text px={P_ ? 56 : 58} maxW={s.sw}>{p.caption}</Text>{p.uncertainty ? <div><Text px={34} kind="mono" maxW={s.sw} color={GREY}>{p.uncertainty}</Text></div> : null}</div>
    <span style={{display: 'none'}}>{yrs}</span>
  </AbsoluteFill>;
};
export default defineEffect({number: 6, slug: 'deep-time', name: 'Deep Time', group: '3D Scenes', frames: 60, beats, schema, Component, samples: S('deep-time'), facts: (p) => [{what: `time scale of ${p.event}`, source: p.source}]});

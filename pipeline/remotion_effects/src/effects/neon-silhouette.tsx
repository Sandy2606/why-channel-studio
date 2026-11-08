import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const schema = z.object({...baseProps, caption: z.string(), time: z.string().regex(/^\d{1,2}:\d{2}$/).default('3:47'), startTime: z.string().regex(/^\d{1,2}:\d{2}$/).default('3:12')});
type P = z.output<typeof schema>;
const beats: Beats = {pan: [0, 14], lamp: [15, 31], flip: [32, 48], settle: [49, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const P_ = s.portrait; const pa = beat('pan', Ease.out), la = beat('lamp', Ease.out), fl = beat('flip', Ease.linear), se = beat('settle', Ease.io);
  const r = seeded('sky'); const W = s.W, H = s.H, horizon = H * .62;
  const skyline = (seed: string, base: number, col: string, shift: number, mw: number) => { const q = seeded(seed); const out: React.ReactNode[] = []; let x = -160; let i = 0; while (x < W + 160) { const w = mw * (.6 + q(`w${i}`)), h = base * (.45 + q(`h${i}`)); out.push(<rect key={i} x={x + shift} y={horizon - h} width={w} height={h + H} fill={col} />); if (col !== '#120e22') for (let wy = 0; wy < 5; wy++) if (q(`l${i}-${wy}`) > .68) out.push(<rect key={`${i}w${wy}`} x={x + shift + w * .3} y={horizon - h + 24 + wy * 38} width={w * .22} height={14} fill={pal.amber} opacity={.5} />); x += w + 6; i++; } return out; };
  const [hh0, mm0] = p.startTime.split(':').map(Number), [hh1, mm1] = p.time.split(':').map(Number); const a = hh0 * 60 + mm0, b = hh1 * 60 + mm1, cur = Math.round(lerp(a, b, fl)); const tm = `${Math.floor(cur / 60)}:${String(cur % 60).padStart(2, '0')}`; void r;
  const deskY = P_ ? H * .74 : H * .74, cx = P_ ? s.cx : s.cx + 180; const phase = (fl * ((b - a) || 1)) % 1; const flipA = fl > 0 && fl < 1 ? phase * 180 : 0; const cw = P_ ? 380 : 460, chh = P_ ? 200 : 220;
  return <AbsoluteFill style={{background: 'linear-gradient(180deg,#120a2e 0%,#3a1458 42%,#b43a78 60%,#e06a54 64%,#150f1f 65%)'}}>
    <svg width={W} height={H} style={{position: 'absolute'}}>{skyline('far', 420, '#2c1a4e', (1 - pa) * -40 + pa * -8, 110)}{skyline('mid', 300, '#1b1436', (1 - pa) * -110 + pa * -24, 140)}{skyline('near', 190, '#120e22', (1 - pa) * -190 + pa * -44, 180)}
      <rect x={0} y={deskY} width={W} height={H - deskY} fill="#0a0810" />
      <g fill="#050408"><ellipse cx={cx - (P_ ? 280 : 390)} cy={deskY - 330 + se * 3} rx={92} ry={108} /><path d={`M ${cx - (P_ ? 450 : 560)} ${deskY} C ${cx - (P_ ? 440 : 550)} ${deskY - 210}, ${cx - (P_ ? 370 : 480)} ${deskY - 240 + se * 3}, ${cx - (P_ ? 280 : 390)} ${deskY - 240 + se * 3} C ${cx - (P_ ? 190 : 300)} ${deskY - 240 + se * 3}, ${cx - (P_ ? 120 : 230)} ${deskY - 200}, ${cx - (P_ ? 110 : 220)} ${deskY} Z`} /></g>
      <ellipse cx={cx + 40} cy={deskY + 6} rx={500 * la} ry={70 * la} fill={pal.amber} opacity={.28} />
      <path d={`M ${cx + 260} ${deskY - 330} L ${cx - 280} ${deskY + 8} L ${cx + 390} ${deskY + 8} Z`} fill={pal.amber} opacity={.13 * la} />
      <g stroke="#050408" strokeWidth={12} fill="#050408"><line x1={cx + 300} y1={deskY} x2={cx + 300} y2={deskY - 300} /><line x1={cx + 300} y1={deskY - 300} x2={cx + 240} y2={deskY - 330} /><path d={`M ${cx + 190} ${deskY - 320} L ${cx + 300} ${deskY - 360} L ${cx + 330} ${deskY - 310} Z`} /></g>
      <circle cx={cx + 252} cy={deskY - 312} r={26} fill="#FFE9B8" opacity={la} /></svg>
    <div style={{position: 'absolute', left: cx - cw / 2 + (P_ ? 10 : 0), top: deskY - chh - 20, width: cw, height: chh, perspective: 900, opacity: Math.max(.25, la), background: '#14110c', borderRadius: 14, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: `0 0 ${60 * la}px rgba(255,178,36,.4)`}}>
      <Text px={P_ ? 130 : 156} color="#FFE9B8">{tm}</Text>
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: chh / 2, background: '#1e1a13', transformOrigin: 'bottom', transform: `rotateX(${-flipA}deg)`, opacity: flipA > 0 ? .9 : 0, backfaceVisibility: 'hidden', borderRadius: '14px 14px 0 0'}} /><div style={{position: 'absolute', left: 0, right: 0, top: chh / 2 - 2, height: 4, background: '#000'}} /></div>
    <div style={{position: 'absolute', left: s.cx, top: s.y0 + 30, transform: 'translateX(-50%)', opacity: se}}><Text px={P_ ? 66 : 70} maxW={s.sw}>{p.caption}</Text></div>
  </AbsoluteFill>;
};
export default defineEffect({number: 8, slug: 'neon-silhouette', name: 'Neon Silhouette', group: '3D Scenes', frames: 60, beats, schema, Component, samples: S('neon-silhouette'), facts: () => []});

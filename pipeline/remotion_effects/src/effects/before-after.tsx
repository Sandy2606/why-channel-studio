import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const state = z.object({title: z.string(), lines: z.array(z.string()).min(1).max(4), url: z.string().default('example.test')});
const schema = z.object({...baseProps, old: state, next: state, change: z.string(), disclaimer: z.string().optional(), highlightLine: z.number().int().min(0).default(0), source: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {old: [0, 12], sweep: [13, 34], pause: [35, 47], finish: [48, 59]};
const Screen: React.FC<{d: z.output<typeof state>; v: 'old' | 'next'; w: number; h: number; hl?: number; hk?: number; amber: string; ink: string; cream: string}> = ({d, v, w, h, hl, hk = 0, amber, ink, cream}) => {
  const isOld = v === 'old', bg = isOld ? '#CFCABD' : ink, fg = isOld ? '#4a463e' : cream;
  return <div style={{position: 'absolute', left: 0, top: 0, width: w, height: h, background: bg}}>
    <div style={{height: 76, background: isOld ? '#b4aea0' : '#1f1d1a', display: 'flex', alignItems: 'center', padding: '0 24px', gap: 12}}>{[0, 1, 2].map((i) => <div key={i} style={{width: 22, height: 22, borderRadius: 11, background: isOld ? '#8f897b' : amber}} />)}<div style={{marginLeft: 16}}><Text px={34} kind="mono" maxW={w - 220} color={fg}>{d.url}</Text></div></div>
    <div style={{padding: 34}}><Text px={isOld ? 58 : 72} maxW={w - 68} color={isOld ? fg : amber}>{d.title}</Text>
      <div style={{marginTop: 28, display: 'flex', flexDirection: 'column', gap: 16}}>{d.lines.map((l, i) => <div key={i} style={{background: !isOld && hl === i ? `rgba(255,178,36,${.28 * hk})` : isOld ? 'rgba(0,0,0,.08)' : 'rgba(255,255,255,.07)', borderRadius: isOld ? 0 : 14, padding: '14px 20px', outline: !isOld && hl === i ? `4px solid rgba(255,178,36,${hk})` : 'none'}}><Text px={40} maxW={w - 110} kind={isOld ? 'mono' : 'head'} color={fg}>{l}</Text></div>)}</div></div></div>;
};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const P_ = s.portrait; const a = beat('old', Ease.out), sw = beat('sweep', Ease.io), fi = beat('finish', Ease.io);
  const w = P_ ? s.sw : 1320, h = P_ ? 880 : 680, x = s.cx - w / 2, y = P_ ? s.y0 + 170 : s.y0 + 90; const pos = (.04 * a + sw * .66 + fi * .30) * w;
  const te = p.language === 'te', labOld = te ? 'పాతది' : 'OLD', labNew = te ? 'కొత్తది' : 'NEW';
  return <Backdrop inner="#2e2a25" outer="#0a0a0a" cy="50%">
    <div style={{position: 'absolute', left: s.x0, top: s.y0 + 30}}><Text px={P_ ? 62 : 58} maxW={s.sw}>{p.change}</Text></div>
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: 20, overflow: 'hidden', boxShadow: '0 30px 70px rgba(0,0,0,.6)'}}>
      <Screen d={p.old} v="old" w={w} h={h} amber={pal.amber} ink={pal.ink} cream={pal.cream} />
      <div style={{position: 'absolute', inset: 0, clipPath: `inset(0 0 0 ${w - pos}px)`}}><Screen d={p.next} v="next" w={w} h={h} hl={p.highlightLine} hk={fi} amber={pal.amber} ink={pal.ink} cream={pal.cream} /></div>
      <div style={{position: 'absolute', left: w - pos - 3, top: 0, width: 6, height: h, background: pal.amber}} />
      <div style={{position: 'absolute', left: w - pos - 42, top: h / 2 - 42, width: 84, height: 84, borderRadius: 42, background: pal.amber, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Text px={44} color={pal.ink}>↔</Text></div>
      <div style={{position: 'absolute', left: 18, bottom: 18, opacity: pos < w * .92 ? 1 : 0}}><Pill px={36} bg="#3a3731" color={pal.cream}>{labOld}</Pill></div>
      <div style={{position: 'absolute', right: 18, bottom: 18, opacity: pos > w * .1 ? 1 : 0}}><Pill px={36}>{labNew}</Pill></div>
    </div>
    <SourceLine x={s.cx} y={y + h + 18} maxW={s.sw}>{p.disclaimer ?? p.source}</SourceLine>
  </Backdrop>;
};
export default defineEffect({number: 26, slug: 'before-after', name: 'Before & After', group: 'UI & Typography', frames: 60, beats, schema, Component, samples: S('before-after'), facts: (p) => [{what: 'comparison', source: p.source}]});

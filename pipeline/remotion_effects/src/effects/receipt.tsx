import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const schema = z.object({...baseProps, business: z.string(), date: z.string(), currency: z.string().default('₹'), items: z.array(z.object({label: z.string(), amount: z.number(), source: z.string().optional()})).min(1).max(8), totalLabel: z.string().optional()});
type P = z.output<typeof schema>;
const beats: Beats = {start: [0, 12], print: [13, 40], total: [41, 51], tear: [52, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const P_ = s.portrait; const st = beat('start'), pr = beat('print', Ease.linear), to = beat('total', Ease.out), te = beat('tear', Ease.io);
  const total = p.items.reduce((a, b) => a + b.amount, 0); const fm = (v: number) => `${p.currency}${v.toLocaleString('en-IN')}`; const n = p.items.length; const rowH = 66, headH = 150, totalH = 120, w = P_ ? 620 : 640; const fullH = headH + n * rowH + totalH + 30;
  const steps = (n + 2); const stepK = Math.floor(pr * steps + 1e-6); const shownH = stepK === 0 ? 30 + st * 40 : Math.min(fullH, headH + Math.max(0, stepK - 1) * rowH + (stepK >= steps ? totalH + 30 : 0) ); const px = s.cx - w / 2 + (P_ ? 0 : 0), py = P_ ? s.y0 + 110 : s.y0 + 96; const slot = 30; const drop = te * (P_ ? 70 : 40); const rot = te * -2.6;
  const tl = p.totalLabel ?? (p.language === 'te' ? 'మొత్తం' : 'TOTAL');
  return <AbsoluteFill style={{background: 'repeating-linear-gradient(92deg,#3a2616 0 60px,#402b19 60px 128px,#35220f 128px 170px)'}}>
    <AbsoluteFill style={{background: 'radial-gradient(90% 70% at 50% 40%, transparent 30%, rgba(0,0,0,.6) 100%)'}} />
    <div style={{position: 'absolute', left: px, top: py + slot + drop, width: w, height: shownH, overflow: 'hidden', transform: `rotate(${rot}deg)`, transformOrigin: 'top center', filter: 'drop-shadow(0 16px 26px rgba(0,0,0,.55))'}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: fullH, background: '#F8F4E8', padding: '20px 34px', boxSizing: 'border-box'}}>
        <div style={{textAlign: 'center'}}><Text px={46} maxW={w - 68} color={pal.ink}>{p.business}</Text><div><Text px={34} kind="mono" maxW={w - 68} color="#57514a">{p.date}</Text></div></div>
        <div style={{borderTop: '3px dashed #807a70', margin: '12px 0 8px'}} />
        {p.items.map((it, i) => <div key={i} style={{display: 'flex', justifyContent: 'space-between', height: rowH, alignItems: 'center'}}><Text px={38} kind="mono" bold maxW={w - 270} color={pal.ink}>{it.label}</Text><Text px={38} kind="mono" bold color={pal.ink}>{fm(it.amount)}</Text></div>)}
        <div style={{borderTop: '3px dashed #807a70', marginTop: 8}} />
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: 100, background: `rgba(255,178,36,${to})`, padding: '0 12px', marginTop: 10}}><Text px={54} maxW={w * .42} color={pal.ink}>{tl}</Text><Text px={62} maxW={w * .5} color={pal.ink}>{fm(total)}</Text></div>
      </div></div>
    <div style={{position: 'absolute', left: px - 50, top: py - 92, width: w + 100, height: 130, background: 'linear-gradient(180deg,#34322e,#191816)', borderRadius: 18, boxShadow: '0 16px 30px rgba(0,0,0,.6)'}}>
      <div style={{position: 'absolute', right: 34, top: 28, width: 26, height: 26, borderRadius: 13, background: st > 0 ? pal.amber : '#55524b', boxShadow: st > 0 ? `0 0 26px ${pal.amber}` : 'none'}} />
      <div style={{position: 'absolute', left: 42, right: 42, bottom: 16, height: 12, background: '#000', borderRadius: 6}} /></div>
  </AbsoluteFill>;
};
export default defineEffect({number: 13, slug: 'receipt', name: 'Receipt', group: '3D Scenes', frames: 60, beats, schema, Component, samples: S('receipt'), facts: (p) => p.items.map((i) => ({what: `line "${i.label}"`, source: i.source}))});

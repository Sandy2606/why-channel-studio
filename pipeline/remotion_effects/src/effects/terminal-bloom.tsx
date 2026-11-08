import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const secret = /(ghp_|gho_|github_pat_|sk-[a-z0-9]{8}|xox[bp]-|AKIA[0-9A-Z]{8}|password=|token=|api[_-]?key=)/i;
const schema = z.object({...baseProps, command: z.string().max(60).refine((c) => !secret.test(c) && !/github\.com\/[^\s]+/i.test(c), 'command must not contain secrets or repository URLs'), productTitle: z.string(), headline: z.string(), buttons: z.array(z.string()).length(2), cards: z.array(z.string()).length(3), lowPower: z.boolean().default(false)});
type P = z.output<typeof schema>;
const beats: Beats = {type: [0, 11], scatter: [12, 30], fill: [31, 47], settle: [48, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat, frame} = useBeats(beats, p); const P_ = s.portrait; const ty = beat('type', Ease.linear), sc = beat('scatter', Ease.io), fi = beat('fill', Ease.linear), se = beat('settle', Ease.io);
  const r = seeded('tb'); const chars = p.command.split(''); const n = Math.ceil(ty * chars.length); const cmdPx = P_ ? 44 : 46; const cw = cmdPx * .6; const X0 = s.x0 + (P_ ? 40 : 80), Y0 = s.cy;
  const w = P_ ? s.sw : 1240, h = P_ ? 1120 : 760, ox = s.cx - w / 2, oy = s.cy - h / 2; const rows: [number, number, number, number][] = [[30, 24, w - 60, 54], [30, 110, w * .72, 110], [30, 250, 230, 72], [290, 250, 230, 72], ...[0, 1, 2].map((i) => (P_ ? [30, 360 + i * 240, w - 60, 216] : [30 + i * ((w - 60) / 3), 360, (w - 60) / 3 - 18, 350]) as [number, number, number, number])];
  const seq = (a: number, b: number) => clamp((fi - a) / (b - a)); const pageOp = clamp(sc * 2 - 1);
  return <AbsoluteFill style={{background: '#0b0d0c'}}>
    <div style={{position: 'absolute', left: ox, top: oy, width: w, height: h, borderRadius: 20, background: '#14130f', opacity: pageOp, transform: `scale(${1 + se * .025})`, boxShadow: `0 0 ${60 * se}px rgba(255,178,36,${.3 * se})`, overflow: 'hidden'}}>
      {rows.map((b, i) => <div key={i} style={{position: 'absolute', left: b[0], top: b[1], width: b[2], height: b[3], border: `2px solid rgba(255,178,36,${.55 * (1 - fi)})`, borderRadius: 10}} />)}
      <div style={{position: 'absolute', left: 34, top: 28, opacity: seq(0, .2)}}><Text px={40} maxW={w - 70} kind="mono" bold color={pal.amber}>{p.productTitle}</Text></div>
      <div style={{position: 'absolute', left: 30, top: 110, opacity: seq(.1, .4)}}><Para px={P_ ? 58 : 58} width={w - 60}>{p.headline}</Para></div>
      {p.buttons.map((b, i) => <div key={i} style={{position: 'absolute', left: 30 + i * 260, top: 250, width: 230, height: 72, borderRadius: 12, display: 'flex', alignItems: 'center', justifyContent: 'center', background: i ? 'transparent' : pal.amber, border: `3px solid ${pal.amber}`, opacity: seq(.3, .5), boxSizing: 'border-box'}}><Text px={36} maxW={200} color={i ? pal.amber : pal.ink}>{b}</Text></div>)}
      {p.cards.map((c, i) => { const b = rows[4 + i]; const k = Ease.out(seq(.45 + i * .15, .7 + i * .15)); return <div key={i} style={{position: 'absolute', left: b[0], top: b[1], width: b[2], height: b[3], background: '#23211b', borderRadius: 14, opacity: k, transform: `translateY(${(1 - k) * 26}px)`, padding: 24, boxSizing: 'border-box'}}><Para px={P_ ? 46 : 40} width={b[2] - 48}>{c}</Para></div>; })}
    </div>
    <div style={{position: 'absolute', left: X0 - 56, top: Y0 - 30, opacity: 1 - clamp(sc * 3)}}><Text px={cmdPx} kind="mono" bold color={pal.amber}>$</Text></div>
    {chars.slice(0, n).map((c, i) => { const hx = X0 + i * cw, hy = Y0 - 26; const t = rows[i % rows.length]; const tx = ox + t[0] + r(`u${i}`) * t[2], ty2 = oy + t[1] + (r(`v${i}`) > .5 ? 0 : t[3]); const mx = (hx + tx) / 2 + (r(`m${i}`) - .5) * 300, my = (hy + ty2) / 2 + (r(`n${i}`) - .5) * 300; const u = p.lowPower ? 0 : sc; const x = (1 - u) ** 2 * hx + 2 * (1 - u) * u * mx + u * u * tx, y = (1 - u) ** 2 * hy + 2 * (1 - u) * u * my + u * u * ty2; const op = p.lowPower ? 1 - clamp(sc * 2) : 1 - clamp((sc - .75) * 4); return <div key={i} style={{position: 'absolute', left: x, top: y, opacity: op}}><Text px={cmdPx} kind="mono" bold>{c === ' ' ? ' ' : c}</Text></div>; })}
    {ty < 1 || (sc === 0 && Math.floor(frame / 8) % 2 === 0) ? <div style={{position: 'absolute', left: X0 + n * cw + 6, top: Y0 - 18, width: 24, height: 46, background: pal.amber}} /> : null}
  </AbsoluteFill>;
};
export default defineEffect({number: 30, slug: 'terminal-bloom', name: 'Terminal Bloom', group: 'UI & Typography', frames: 60, beats, schema, Component, samples: S('terminal-bloom'), facts: () => []});

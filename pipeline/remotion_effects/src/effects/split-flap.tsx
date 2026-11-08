import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const schema = z.object({...baseProps, rows: z.array(z.string()).min(1).max(4), width: z.number().int().min(4).max(24).optional(), order: z.enum(['down', 'up']).default('down')});
type P = z.output<typeof schema>;
const beats: Beats = {warm: [0, 18], settle: [19, 58], last: [59, 76], hold: [77, 89]};
const EN = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '.split(''); const TE_ = 'కగచజటడతదనపబమయరలవసహఅఆఇఉఎఒ '.split('');
const Flap: React.FC<{target: string; pool: string[]; frame: number; settle: number; id: string; w: number; h: number; fs: number; family: string; weight: number; color: string; flash: boolean}> = ({target, pool, frame, settle, id, w, h, fs, family, weight, color}) => {
  const r = seeded(id); const STEP = 2; const at = (n: number) => { if (n * STEP >= settle) return target; return pool[Math.floor(r(`g${n}`) * pool.length)]; };
  const n = Math.floor(frame / STEP), ph = (frame % STEP) / STEP, cur = at(n), next = at(n + 1), moving = n * STEP < settle;
  const half = (c: string, top: boolean, extra?: React.CSSProperties) => <div style={{position: 'absolute', left: 0, width: w, height: h / 2, top: top ? 0 : h / 2, overflow: 'hidden', background: top ? '#3A362F' : '#2E2B25', borderRadius: top ? '8px 8px 0 0' : '0 0 8px 8px', transformOrigin: top ? 'bottom' : 'top', backfaceVisibility: 'hidden', ...extra}}><div style={{position: 'absolute', top: top ? 0 : -h / 2, width: w, height: h, lineHeight: `${h}px`, textAlign: 'center', fontFamily: family, fontWeight: weight, fontSize: fs, color}}>{c}</div></div>;
  return <div style={{position: 'relative', width: w, height: h, perspective: 500}}>{half(next, true)}{half(cur, false)}
    {moving && ph < .5 ? half(cur, true, {transform: `rotateX(${-ph * 180}deg)`, zIndex: 2}) : null}{moving && ph >= .5 ? half(next, false, {transform: `rotateX(${(1 - ph) * 180}deg)`, zIndex: 2}) : null}
    <div style={{position: 'absolute', left: 0, right: 0, top: h / 2 - 1.5, height: 3, background: '#000', zIndex: 3}} /></div>;
};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {range, frame} = useBeats(beats, p); const te = p.language === 'te';
  const cells = p.rows.map(graphemes); const cols = p.width ?? Math.max(...cells.map((c) => c.length)); const gap = 8; const w = Math.floor(Math.min((s.sw - (cols - 1) * gap) / cols, s.portrait ? 110 : 120)), h = Math.round(w * (te ? 1.75 : 1.5)), fs = Math.round(w * (te ? .62 : .98));
  const rGap = 22, blockH = cells.length * h + (cells.length - 1) * rGap, top = s.cy - blockH / 2; const totalW = cols * w + (cols - 1) * gap, left = s.cx - totalW / 2;
  const n = cells.length, [a, b] = range.settle, lastB = range.last[1]; const order = p.order === 'down' ? (i: number) => i : (i: number) => n - 1 - i;
  const pool = te ? TE_ : EN;
  return <AbsoluteFill style={{background: 'radial-gradient(90% 70% at 50% 50%, #26231f 0%, #0a0a0a 100%)'}}>
    {cells.map((c, ri) => { const pad = Math.floor((cols - c.length) / 2); const row = [...Array(pad).fill(' '), ...c, ...Array(cols - pad - c.length).fill(' ')]; const isLast = order(ri) === n - 1 && n > 1;
      return <div key={ri} style={{position: 'absolute', left, top: top + ri * (h + rGap), display: 'flex', gap}}>{row.map((g: string, ci: number) => { const base = isLast ? range.last[0] : a + (b - a) * order(ri) / Math.max(1, n); const span = isLast ? lastB - range.last[0] - 2 : (b - a) / Math.max(1, n); const settle = Math.round(base + span * ci / cols); return <Flap key={ci} id={`${ri}-${ci}`} target={g} pool={pool} frame={frame} settle={settle} w={w} h={h} fs={fs} family={TELUGU.test(p.rows.join('')) ? TE : HEAD} weight={te ? 900 : 400} color={pal.cream} flash={false} />; })}</div>; })}
  </AbsoluteFill>;
};
export default defineEffect({number: 25, slug: 'split-flap', name: 'Split-Flap', group: 'Data & Counters', frames: 90, beats, schema, Component, samples: S('split-flap'), facts: () => []});

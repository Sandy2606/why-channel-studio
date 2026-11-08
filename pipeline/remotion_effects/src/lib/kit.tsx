import React, {useMemo} from 'react';
import {AbsoluteFill, Easing, interpolate, random, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {GREY, HEAD, MONO, TE, TELUGU, usePalette} from './brand';

export const baseProps = {
  language: z.enum(['en', 'te']).default('en'),
  captionSafe: z.boolean().default(true),
  brandPalette: z.object({ink: z.string(), cream: z.string(), amber: z.string()}).partial().optional(),
  durationFrames: z.number().int().positive().optional(),
  /** Voice alignment: beat name -> frame. Later beats keep their spacing after the cued beat. */
  cues: z.record(z.number().int().min(0)).optional(),
  /** true shows a DEMO / ILLUSTRATION stamp and waives the source requirement. */
  demo: z.boolean().default(false),
};
export type Base = {language: 'en' | 'te'; captionSafe: boolean; brandPalette?: Partial<{ink: string; cream: string; amber: string}>; durationFrames?: number; cues?: Record<string, number>; demo: boolean};
export const source = z.string().min(1).optional();

export type Beats = Record<string, [number, number]>;
export type Fact = {what: string; source?: string};

export function resolveBeats(beats: Beats, cues?: Record<string, number>) {
  const out: Record<string, [number, number]> = {}; let shift = 0;
  for (const [k, [a, b]] of Object.entries(beats)) {
    if (cues && cues[k] !== undefined) shift = cues[k] - a;
    out[k] = [a + shift, b + shift];
  }
  return out;
}

export function totalFrames(frames: number, beats: Beats, p: Base) {
  const r = resolveBeats(beats, p.cues); const last = Math.max(...Object.values(r).map((x) => x[1])) + 1;
  return Math.max(p.durationFrames ?? 0, Math.max(last, p.durationFrames ? 1 : frames));
}

export const Ease = {out: Easing.bezier(.16, 1, .3, 1), io: Easing.bezier(.65, 0, .35, 1), linear: Easing.linear, back: Easing.bezier(.34, 1.56, .64, 1)};

/** beat('draw') is the eased 0..1 progress of that beat at the current frame. */
export function useBeats(beats: Beats, p: Base) {
  const frame = useCurrentFrame(); const r = useMemo(() => resolveBeats(beats, p.cues), [beats, p.cues]);
  const beat = (k: string, ease: (t: number) => number = Ease.io, from = 0, to = 1) => {
    const [a, b] = r[k]; const len = Math.max(1, b - a); const s = a + from * len; const e = a + to * len;
    return interpolate(frame, [s, Math.max(s + .001, e)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});
  };
  return {beat, frame, range: r};
}

/** Channel safe zones: same numbers as pipeline/styles/core.py Stage. */
export function useStage(captionSafe = true) {
  const {width: W, height: H, fps} = useVideoConfig(); const portrait = H > W;
  const [x0, y0, x1, y1] = portrait ? (captionSafe ? [70, 220, 900, 1500] : [50, 120, 1030, 1800]) : (captionSafe ? [90, 60, 1830, 900] : [60, 40, 1860, 1040]);
  return {W, H, fps, portrait, x0, y0, x1, y1, sw: x1 - x0, sh: y1 - y0, cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, label: portrait ? 36 : 34};
}

let _c: CanvasRenderingContext2D | null = null;
export function textWidth(s: string, font: string) {
  _c ??= document.createElement('canvas').getContext('2d'); _c!.font = font; return _c!.measureText(s).width;
}
export const famOf = (s: string, kind: 'head' | 'mono') => TELUGU.test(s) ? TE : kind === 'head' ? HEAD : MONO;
export const weightOf = (s: string, kind: 'head' | 'mono', bold?: boolean) => TELUGU.test(s) ? 900 : kind === 'mono' ? (bold ? 700 : 400) : 400;
/** Largest size that fits maxW, measured with the real font. Telugu is scaled to match Latin visual size. */
export function fit(s: string, kind: 'head' | 'mono', px: number, maxW: number, min = 34, bold?: boolean) {
  let size = TELUGU.test(s) ? Math.round(px * .86) : px;
  while (size > min && textWidth(s, `${weightOf(s, kind, bold)} ${size}px ${famOf(s, kind)}`) > maxW) size -= 2;
  return size;
}

type TP = {children: string; px: number; maxW?: number; kind?: 'head' | 'mono'; color?: string; bold?: boolean; style?: React.CSSProperties};
/** Single-line text fitted to width with the correct font for its script. */
export const Text: React.FC<TP> = ({children: s, px, maxW, kind = 'head', color, bold, style}) => {
  const p = usePalette(); const size = maxW ? fit(s, kind, px, maxW, 34, bold) : (TELUGU.test(s) ? Math.round(px * .86) : px);
  return <span style={{fontFamily: famOf(s, kind), fontWeight: weightOf(s, kind, bold), fontSize: size, color: color ?? p.cream, lineHeight: TELUGU.test(s) ? 1.45 : 1.1, whiteSpace: 'nowrap', display: 'inline-block', ...style}}>{s}</span>;
};
/** Multi-line text. Use for headlines and sentences. */
export const Para: React.FC<Omit<TP, 'maxW' | 'children'> & {width: number; children: React.ReactNode; sample?: string}> = ({children, px, width, kind = 'head', color, bold, style, sample}) => {
  const p = usePalette(); const t = typeof children === 'string' ? children : sample ?? ''; const te = TELUGU.test(t);
  return <div style={{width, fontFamily: famOf(t, kind), fontWeight: weightOf(t, kind, bold), fontSize: te ? Math.round(px * .86) : px, color: color ?? p.cream, lineHeight: te ? 1.5 : 1.14, ...style}}>{children}</div>;
};

export const Pill: React.FC<{children: string; px?: number; bg?: string; color?: string; maxW?: number; style?: React.CSSProperties; kind?: 'head' | 'mono'}> = ({children, px = 40, bg, color, maxW, style, kind = 'head'}) => {
  const p = usePalette();
  return <div style={{background: bg ?? p.amber, borderRadius: 16, padding: '12px 26px', display: 'inline-block', whiteSpace: 'nowrap', ...style}}><Text px={px} maxW={maxW ? maxW - 52 : undefined} color={color ?? p.ink} kind={kind} bold>{children}</Text></div>;
};

export const DemoStamp: React.FC<{lang: 'en' | 'te'; captionSafe: boolean}> = ({lang, captionSafe}) => {
  const s = useStage(captionSafe); const p = usePalette();
  return <div style={{position: 'absolute', right: s.W - s.x1, top: s.portrait ? s.y0 - 74 : s.y0 - 44, background: p.ink, border: `3px solid ${p.amber}`, borderRadius: 10, padding: '2px 16px', zIndex: 50}}>
    <Text px={34} kind="mono" bold color={p.amber}>{lang === 'te' ? 'డెమో / ఊహాచిత్రం' : 'DEMO / ILLUSTRATION'}</Text></div>;
};

export const Backdrop: React.FC<{inner?: string; outer?: string; cy?: string; children?: React.ReactNode}> = ({inner = '#2a2622', outer = '#080808', cy = '45%', children}) =>
  <AbsoluteFill style={{background: `radial-gradient(120% 75% at 50% ${cy}, ${inner} 0%, ${outer} 100%)`}}>{children}</AbsoluteFill>;

export const SourceLine: React.FC<{children?: string; x: number; y: number; maxW: number; anchor?: 'left' | 'center' | 'right'; a?: number; color?: string}> = ({children, x, y, maxW, anchor = 'center', a = 1, color}) => {
  if (!children) return null;
  const tx = anchor === 'center' ? '-50%' : anchor === 'right' ? '-100%' : '0';
  return <div style={{position: 'absolute', left: x, top: y, transform: `translateX(${tx})`, opacity: a}}><Text px={34} kind="mono" maxW={maxW} color={color ?? GREY}>{children}</Text></div>;
};

export const seeded = (seed: string | number) => (i: number | string) => random(`${seed}-${i}`);
export const lerp = (a: number, b: number, k: number) => a + (b - a) * k;
export const clamp = (x: number, a = 0, b = 1) => Math.max(a, Math.min(b, x));

/** Hand-drawn strokes with a fixed seed: lines never crawl between frames. */
export function wobble(pts: [number, number][], seed: string, amp = 5, closed = false) {
  const r = seeded(seed); const q = pts.map(([x, y], i) => [x + (r(`x${i}`) - .5) * amp * 2, y + (r(`y${i}`) - .5) * amp * 2] as [number, number]);
  if (closed) q.push(q[0]);
  let d = `M${q[0][0].toFixed(1)} ${q[0][1].toFixed(1)}`;
  for (let i = 1; i < q.length; i++) { const [a, b] = q[i - 1], [c, e] = q[i]; const mx = (a + c) / 2 + (r(`m${i}`) - .5) * amp, my = (b + e) / 2 + (r(`n${i}`) - .5) * amp; d += ` Q${mx.toFixed(1)} ${my.toFixed(1)} ${c.toFixed(1)} ${e.toFixed(1)}`; }
  return d;
}
export const circlePts = (cx: number, cy: number, rx: number, ry = rx, n = 12): [number, number][] => Array.from({length: n}, (_, i) => [cx + Math.cos(i / n * 6.283) * rx, cy + Math.sin(i / n * 6.283) * ry]);
export const linePts = (a: [number, number], b: [number, number], n = 3): [number, number][] => Array.from({length: n + 1}, (_, i) => [lerp(a[0], b[0], i / n), lerp(a[1], b[1], i / n)]);
export const Ink: React.FC<{d: string; k?: number; w?: number; color?: string; fill?: string}> = ({d, k = 1, w = 7, color = '#14110C', fill = 'none'}) => k <= 0 ? null :
  <path d={d} pathLength={1} fill={k >= 1 ? fill : 'none'} stroke={color} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={k >= 1 ? undefined : `${k} 1`} />;
export const graphemes = (s: string): string[] => Array.from(new (Intl as any).Segmenter('te', {granularity: 'grapheme'}).segment(s), (x: any) => x.segment);

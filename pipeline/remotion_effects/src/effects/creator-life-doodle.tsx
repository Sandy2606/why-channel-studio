import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const schema = z.object({...baseProps, task: z.string(), objects: z.array(z.enum(['cup', 'note', 'calendar'])).min(1).default(['cup', 'note', 'calendar']), punchline: z.string()});
type P = z.output<typeof schema>;
const beats: Beats = {draw: [0, 11], add: [12, 34], wobble: [35, 46], punch: [47, 59]};
const Glyph: React.FC<{kind: string; id: string}> = ({kind, id}) => kind === 'cup' ? <><Ink d={wobble([[-30, -34], [30, -34], [24, 34], [-24, 34]], id, 2.5, true)} w={6} fill="#fff" /><Ink d={wobble(circlePts(42, 0, 16, 20, 8), id + 'h', 1.5, true)} w={5} /></> : kind === 'note' ? <Ink d={wobble([[-38, -38], [38, -38], [38, 38], [-38, 38]], id, 3, true)} w={6} fill="#FFE9A8" /> : <><Ink d={wobble([[-40, -40], [40, -40], [40, 44], [-40, 44]], id, 3, true)} w={6} fill="#fff" /><Ink d={wobble(linePts([-40, -18] as [number, number], [40, -18], 2), id + 'l', 2)} w={5} /></>;
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const {beat, frame} = useBeats(beats, p); const P_ = s.portrait; const dr = beat('draw', Ease.linear), ad = beat('add', Ease.linear), wo = beat('wobble', Ease.linear), pu = beat('punch', Ease.out);
  const size = P_ ? 830 : 600, ox = P_ ? s.x0 : s.cx - size / 2, oy = P_ ? s.y0 + 150 : s.y0 + 100; const n = 22; const shown = Math.floor(stepOf(ad) * n); const r = seeded('clutter');
  function stepOf(k: number) { return Math.floor(k * 8) / 8; }
  const sway = wo > 0 && wo < 1 ? Math.sin(Math.floor(frame / 3) * 2.4) * 3.5 * (1 - wo * .4) : 0;
  return <AbsoluteFill style={{background: '#F4F1EA'}}>
    <div style={{position: 'absolute', left: s.cx, top: s.y0 + 20, transform: 'translateX(-50%)'}}><Text px={P_ ? 64 : 60} maxW={s.sw} color="#14110C">{p.task}</Text></div>
    <svg width={size} height={size} viewBox="0 0 1000 1000" style={{position: 'absolute', left: ox, top: oy}}>
      <Ink d={wobble(linePts([50, 760], [950, 760], 6), 'desk', 6)} k={dr} w={9} /><Ink d={wobble(linePts([130, 760], [120, 990], 3), 'a', 4)} k={dr} w={9} /><Ink d={wobble(linePts([870, 760], [880, 990], 3), 'b', 4)} k={dr} w={9} />
      <Ink d={wobble(circlePts(500, 430, 104, 112, 12), 'head', 5, true)} k={dr} w={9} fill="#fff" /><Ink d={wobble(linePts([500, 540], [500, 760], 3), 'b2', 5)} k={dr} w={9} />
      <Ink d={wobble(linePts([465, 410], [487, 410], 1), 'e1', 2)} k={dr} w={8} /><Ink d={wobble(linePts([520, 410], [542, 410], 1), 'e2', 2)} k={dr} w={8} /><Ink d={wobble(linePts([470, 480], [535, 480], 2), 'm', 3)} k={dr} w={8} />
      <g transform={`rotate(${sway} 500 760)`}>{Array.from({length: shown}, (_, i) => { const col = i % 11, row = Math.floor(i / 11), kind = p.objects[i % p.objects.length]; const x = 115 + col * 77 + (r(`x${i}`) - .5) * 26, y = 716 - row * 86 - (col % 2) * 8, rot = (r(`r${i}`) - .5) * 15; return (x > 395 && x < 610 && row > 0 && y > 320) ? null : <g key={i} transform={`translate(${x} ${y}) rotate(${rot})`}><Glyph kind={kind} id={`g${i}`} /></g>; })}</g>
    </svg>
    <div style={{position: 'absolute', left: s.cx, top: P_ ? s.y1 - 96 : s.y1 - 78, transform: 'translateX(-50%)', opacity: pu}}><Text px={P_ ? 62 : 62} maxW={s.sw} color="#14110C">{p.punchline}</Text></div>
  </AbsoluteFill>;
};
export default defineEffect({number: 21, slug: 'creator-life-doodle', name: 'Creator Life, Drawn Badly', group: 'Ink & Paper', frames: 60, beats, schema, Component, samples: S('creator-life-doodle'), facts: () => []});

import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const schema = z.object({...baseProps, caption: z.string(), action: z.enum(['write', 'type']).default('write'), props: z.array(z.string()).length(3).default(['note', 'note', 'cup'])});
type P = z.output<typeof schema>;
const beats: Beats = {sketch: [0, 10], cycle: [11, 31], pile: [32, 45], punch: [46, 59]};
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const {beat, frame} = useBeats(beats, p); const P_ = s.portrait; const sk = beat('sketch', Ease.linear), cy = beat('cycle', Ease.linear), pi = beat('pile', Ease.linear), pu = beat('punch', Ease.back);
  const phase = (cy * 3 + pi * 10) * 6.283; const lift = (Math.sin(phase) + 1) / 2; const pose = lift > .5 ? 1 : 0; const hand: [number, number] = [640, 560 - pose * 62];
  const size = P_ ? 830 : 640, ox = P_ ? s.x0 : s.cx - size / 2, oy = P_ ? s.y0 + 70 : s.y0 + 30; const r = seeded('sheet'); const count = Math.floor(pi * 16) + Math.floor(cy * 3);
  return <AbsoluteFill style={{background: '#F4F1EA'}}>
    <svg width={size} height={size} viewBox="0 0 1000 1000" style={{position: 'absolute', left: ox, top: oy}}>
      <Ink d={wobble(linePts([70, 720], [930, 720], 6), 'desk', 6)} k={sk} w={9} /><Ink d={wobble(linePts([150, 720], [130, 960], 3), 'l1', 5)} k={sk} w={9} /><Ink d={wobble(linePts([850, 720], [870, 960], 3), 'l2', 5)} k={sk} w={9} />
      <Ink d={wobble(circlePts(450, 300, 110, 118, 12), 'head', 5, true)} k={sk} w={9} fill="#fff" /><Ink d={wobble(linePts([450, 418], [440, 720], 4), 'body', 6)} k={sk} w={9} />
      <circle cx={418} cy={285} r={9} fill="#14110C" opacity={sk} /><circle cx={492} cy={285} r={9} fill="#14110C" opacity={sk} />
      <Ink d={wobble(linePts([420, 348], [495, 340], 2), 'mouth', 4)} k={sk} w={7} />
      <Ink d={wobble(linePts([445, 480], [hand[0] - 90, hand[1] - 40 + pose * 12], 2), `arm-${pose}`, 4)} w={9} k={sk} /><Ink d={wobble(linePts([hand[0] - 90, hand[1] - 40 + pose * 12], hand, 2), `fore-${pose}`, 4)} w={9} k={sk} />
      <Ink d={wobble([[590, 700], [760, 700], [760, 640], [590, 640]], 'pad', 3, true)} k={sk} w={7} fill="#fff" />
      {Array.from({length: count}, (_, i) => { const x = 220 + r(`x${i}`) * 560, y = 900 - (Math.floor(r(`c${i}`) * 3)) * 12 - i * 2.4, rot = (r(`a${i}`) - .5) * 40; return <g key={i} transform={`translate(${x} ${y}) rotate(${rot})`}><Ink d={wobble([[-46, -32], [46, -32], [46, 32], [-46, 32]], `s${i}`, 3, true)} w={5} fill="#FFFDF4" /></g>; })}
      {pu > 0 ? <text /> : null}
    </svg>
    <div style={{position: 'absolute', left: s.cx, top: P_ ? s.y0 + 900 : s.y1 - 120, transform: `translateX(-50%) rotate(-2deg) scale(${pu})`}}><Text px={P_ ? 76 : 72} maxW={s.sw} color="#14110C">{p.caption}</Text></div>
    <div style={{display: 'none'}}>{frame}</div>
  </AbsoluteFill>;
};
export default defineEffect({number: 19, slug: 'ink-doodle', name: 'Ink Doodle', group: 'Ink & Paper', frames: 60, beats, schema, Component, samples: S('ink-doodle'), facts: () => []});

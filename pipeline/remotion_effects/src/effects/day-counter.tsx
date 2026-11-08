import React from 'react';
import {AbsoluteFill, interpolate} from 'remotion';
import {z} from 'zod';
import {defineEffect, S} from '../lib/define';
import {Backdrop, baseProps, circlePts, clamp, Ease, fit, graphemes, Ink, lerp, linePts, Para, Pill, seeded, SourceLine, Text, textWidth, famOf, weightOf, useBeats, useStage, wobble, Beats} from '../lib/kit';
import {GREY, HEAD, TE, TELUGU, usePalette} from '../lib/brand';
const schema = z.object({...baseProps, startDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/), endDate: z.string().regex(/^\d{4}-\d{2}-\d{2}$/), event: z.string(), calendarBasis: z.string().default('GREGORIAN CALENDAR'), dayWord: z.string().optional(), source: z.string().optional()}).refine((v) => Date.parse(v.endDate + 'T00:00:00Z') >= Date.parse(v.startDate + 'T00:00:00Z'), 'endDate is before startDate');
type P = z.output<typeof schema>;
const beats: Beats = {one: [0, 10], flip: [11, 37], land: [38, 50], hold: [51, 59]};
const DAY = 86400000; const MON = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
const MON_TE = ['జనవరి', 'ఫిబ్రవరి', 'మార్చి', 'ఏప్రిల్', 'మే', 'జూన్', 'జులై', 'ఆగస్టు', 'సెప్టెంబర్', 'అక్టోబర్', 'నవంబర్', 'డిసెంబర్'];
const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat} = useBeats(beats, p); const P_ = s.portrait; const fl = beat('flip', (t) => (t * t * .55 + t * .15) / .7), la = beat('land', Ease.out), ho = beat('hold');
  const t0 = Date.parse(p.startDate + 'T00:00:00Z'), t1 = Date.parse(p.endDate + 'T00:00:00Z'), total = Math.round((t1 - t0) / DAY) + 1;
  const prog = clamp(fl * .7 + la * .3), idx = prog * (total - 1), day = Math.min(total - 1, Math.floor(idx + 1e-6)), frac = day === total - 1 ? 0 : idx - day;
  const date = (i: number) => new Date(t0 + i * DAY); const m = (d: Date) => (p.language === 'te' ? MON_TE : MON)[d.getUTCMonth()];
  const w = P_ ? 560 : 500, h = P_ ? 620 : 560, x = P_ ? s.cx - w / 2 : s.x0 + 980, y = P_ ? s.y0 + 390 : s.y0 + 150;
  const face = (i: number) => { const d = date(i); return <><div style={{height: 118, background: pal.amber, display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '16px 16px 0 0'}}><Text px={62} color={pal.ink}>{`${m(d)} ${d.getUTCFullYear()}`}</Text></div><div style={{height: h - 118, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><Text px={300} color={pal.ink} style={{lineHeight: 1}}>{String(d.getUTCDate())}</Text></div></>; };
  const sheet: React.CSSProperties = {position: 'absolute', left: 0, top: 0, width: w, height: h, background: '#F7F2E6', borderRadius: 16, overflow: 'hidden', backfaceVisibility: 'hidden'};
  const count = (day + 1).toLocaleString('en-IN'); const word = p.dayWord ?? (p.language === 'te' ? 'రోజు' : 'DAY');
  return <AbsoluteFill style={{background: 'radial-gradient(100% 75% at 50% 45%, #5a4630 0%, #1a130c 100%)'}}>
    <div style={{position: 'absolute', left: P_ ? s.x0 : s.x0 + 20, top: P_ ? s.y0 + 20 : s.y0 + 240, width: P_ ? s.sw : 880}}><Text px={46} kind="mono" bold maxW={P_ ? s.sw : 860}>{word}</Text><div><Text px={P_ ? 250 : 290} maxW={P_ ? s.sw : 860} color={pal.amber} style={{lineHeight: 1}}>{count}</Text></div></div>
    <div style={{position: 'absolute', left: x, top: y, width: w, height: h, perspective: 1600}}>
      {[3, 2, 1].map((n) => <div key={n} style={{position: 'absolute', left: n * 3, top: n * 7, width: w, height: h, background: `hsl(42 34% ${86 - n * 7}%)`, borderRadius: 16}} />)}
      <div style={sheet}>{face(Math.min(total - 1, day + 1))}</div>
      <div style={{...sheet, transformOrigin: 'top center', transform: `rotateX(${frac * 160}deg)`, boxShadow: '0 20px 40px rgba(0,0,0,.3)'}}>{face(day)}</div>
      {la > .55 ? <div style={{position: 'absolute', right: -20, bottom: -10, width: 190, height: 190, borderRadius: 95, background: pal.amber, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `rotate(-12deg) scale(${lerp(1.7, 1, clamp((la - .55) / .45))})`, boxShadow: '0 12px 26px rgba(0,0,0,.5)'}}><Text px={130} color={pal.ink}>✓</Text></div> : null}
    </div>
    <div style={{position: 'absolute', left: P_ ? s.cx : s.x0 + 20, top: P_ ? s.y0 + 1062 : s.y0 + 620, transform: P_ ? 'translateX(-50%)' : undefined, opacity: Math.max(ho, la)}}><Text px={P_ ? 56 : 56} maxW={P_ ? s.sw : 880}>{p.event}</Text></div>
    <SourceLine x={P_ ? s.cx : s.x0 + 20} y={P_ ? s.y0 + 1150 : s.y0 + 710} anchor={P_ ? 'center' : 'left'} maxW={P_ ? s.sw : 880} a={Math.max(.75, ho)}>{p.calendarBasis}</SourceLine>
  </AbsoluteFill>;
};
export default defineEffect({number: 24, slug: 'day-counter', name: 'Day Counter', group: 'Data & Counters', frames: 60, beats, schema, Component, samples: S('day-counter'), facts: (p) => [{what: `interval ${p.startDate} to ${p.endDate}`, source: p.source}]});

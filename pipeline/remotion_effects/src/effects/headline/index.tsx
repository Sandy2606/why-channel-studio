import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {z} from 'zod';
import en from '../../../samples/headline.en.json';
import te from '../../../samples/headline.te.json';
import {defineEffect} from '../../lib/define';
import {baseProps, Ease, lerp, Para, Text, useBeats, useStage} from '../../lib/kit';
import {usePalette} from '../../lib/brand';

const schema = z.object({...baseProps, publication: z.string(), headline: z.string(), subhead: z.string().optional(), date: z.string(),
  /** Exact words inside headline to underline. Must come from the source. */
  emphasis: z.string().optional(), citation: z.string().optional(), photo: z.string().optional(),
  /** true prints ILLUSTRATIVE MOCK ARTICLE on the page. Use whenever this is not a real cited screenshot. */
  mock: z.boolean().default(true)});
type P = z.output<typeof schema>;
const beats = {paper: [0, 14], set: [15, 39], spot: [40, 68], hold: [69, 89]} as Record<string, [number, number]>;
const INK = '#16140F';

const Component: React.FC<P> = (p) => {
  const s = useStage(p.captionSafe); const pal = usePalette(); const {beat, frame} = useBeats(beats, p);
  const pap = beat('paper', Ease.out), set = beat('set', Ease.linear), spot = beat('spot', Ease.io), hold = beat('hold', Ease.io);
  const w = s.portrait ? s.sw : 1120, h = s.portrait ? 1180 : 800, pad = s.portrait ? 44 : 50;
  const tw = w - pad * 2;
  const seq = (a: number, b: number) => Math.max(0, Math.min(1, (set - a) / (b - a)));
  const rev = (k: number): React.CSSProperties => ({opacity: k, transform: `translateY(${(1 - k) * 18}px)`});
  const rx = lerp(26, 4, pap) + hold * 1.2, rz = lerp(-7, -1.6, pap), scale = lerp(.9, 1, pap) * (1 + spot * .035);
  let body: React.ReactNode = p.headline;
  if (p.emphasis && p.headline.includes(p.emphasis)) { const [a, ...r] = p.headline.split(p.emphasis);
    body = <>{a}<span style={{backgroundImage: `linear-gradient(${pal.amber},${pal.amber})`, backgroundRepeat: 'no-repeat', backgroundPosition: '0 92%', backgroundSize: `${spot * 100}% 16%`, WebkitBoxDecorationBreak: 'clone', boxDecorationBreak: 'clone'}}>{p.emphasis}</span>{r.join(p.emphasis)}</>; }
  const px = s.portrait ? 84 : 76;
  return <AbsoluteFill style={{background: 'radial-gradient(90% 70% at 50% 42%, #38322a 0%, #0b0a09 100%)', perspective: 1900}}>
    <div style={{position: 'absolute', left: s.cx - w / 2, top: s.cy - h / 2 + (s.portrait ? 30 : -6), width: w, height: h, background: '#F4F0E4', borderRadius: 6, padding: pad, boxSizing: 'border-box', transform: `rotateX(${rx}deg) rotateZ(${rz}deg) scale(${scale})`, boxShadow: '0 50px 90px rgba(0,0,0,.65)', overflow: 'hidden'}}>
      <svg style={{position: 'absolute', inset: 0, opacity: .22, mixBlendMode: 'multiply'}} width={w} height={h}><filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves={3} seed={4} /><feColorMatrix values="0 0 0 0 .45 0 0 0 0 .4 0 0 0 0 .3 0 0 0 .9 0" /></filter><rect width={w} height={h} filter="url(#paper)" /></svg>
      <div style={{position: 'relative', textAlign: 'center'}}>
        <Text px={s.portrait ? 76 : 62} maxW={tw} color={INK}>{p.publication}</Text>
        <div style={{height: 6, background: INK, margin: '10px 0 6px'}} /><div style={{height: 2, background: INK}} />
        <div style={{marginTop: 8}}><Text px={34} maxW={tw} kind="mono" bold color={INK}>{p.date}</Text></div>
        <div style={{height: 2, background: INK, marginTop: 8}} /></div>
      <div style={{position: 'relative', marginTop: 30, ...rev(seq(0, .45))}}><Para px={px} width={tw} color={INK} sample={p.headline}>{body}</Para></div>
      {p.subhead ? <div style={{position: 'relative', marginTop: 20, ...rev(seq(.35, .7))}}><Para px={s.portrait ? 40 : 36} width={tw} kind="mono" bold color="#463f33">{p.subhead}</Para></div> : null}
      <div style={{position: 'relative', marginTop: 28, height: s.portrait ? 260 : 150, ...rev(seq(.6, 1)), background: p.photo ? undefined : 'repeating-linear-gradient(135deg,#d6cfbd 0 16px,#cbc3af 16px 32px)', overflow: 'hidden', borderRadius: 3}}>
        {p.photo ? <Img src={staticFile(p.photo)} style={{width: '100%', height: '100%', objectFit: 'cover'}} /> : null}</div>
      {p.mock ? <div style={{position: 'absolute', right: pad, bottom: pad + (p.citation ? 78 : 4), transform: `rotate(-3deg) scale(${lerp(1.5, 1, hold)})`, opacity: hold, border: `4px solid ${INK}`, padding: '2px 12px'}}><Text px={34} kind="mono" bold color={INK}>{p.language === 'te' ? 'ఊహా వ్యాసం' : 'ILLUSTRATIVE MOCK'}</Text></div> : null}
      {p.citation ? <div style={{position: 'absolute', left: pad, right: pad, bottom: pad - 4, opacity: hold || spot, borderTop: `2px solid ${INK}`, paddingTop: 8}}><Text px={34} maxW={tw} kind="mono" color={INK}>{p.citation}</Text></div> : null}
    </div>
  </AbsoluteFill>;
};

export default defineEffect({number: 15, slug: 'headline', name: 'Headline', group: 'Ink & Paper', frames: 90, beats, schema, Component, samples: {en, te},
  facts: (p) => [{what: 'headline', source: p.citation}]});

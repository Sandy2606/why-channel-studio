import React from 'react';
import {AbsoluteFill, CalculateMetadataFunction} from 'remotion';
import {z} from 'zod';
import {BRAND, Pal} from './brand';
import {FontGate} from './fonts';
import {Base, Beats, DemoStamp, Fact, totalFrames} from './kit';

declare const require: any;
/** Sample props for an effect, used as Studio defaults and by the CLI. */
export const S = (slug: string) => ({en: require(`../../samples/${slug}.en.json`), te: require(`../../samples/${slug}.te.json`)});

export type EffectDef = {
  number: number; slug: string; name: string; group: string; frames: number; beats: Beats;
  schema: z.ZodTypeAny; Component: React.FC<any>; facts: (p: any) => Fact[]; samples: {en: object; te: object};
};

export function defineEffect<S extends z.ZodTypeAny>(d: Omit<EffectDef, 'schema' | 'Component' | 'facts'> & {schema: S; Component: React.FC<z.output<S>>; facts: (p: z.output<S>) => Fact[]}): EffectDef { return d as unknown as EffectDef; }

/** Throws on bad props or unsourced facts, so no render can skip the check. */
export function checkProps(e: EffectDef, input: unknown) {
  const r = e.schema.safeParse(input);
  if (!r.success) throw new Error(`[${e.slug}] invalid props: ` + r.error.issues.map((i) => `${i.path.join('.')}: ${i.message}`).join('; '));
  const p = r.data as Base;
  if (!p.demo) {
    const placeholder = /\bdemo\b|\bsample\b|placeholder|డెమో|నమూనా/i;   // a sample string is never a real source
    const missing = e.facts(p).filter((f) => !f.source?.trim() || placeholder.test(f.source)).map((f) => f.what);
    if (missing.length) throw new Error(`[${e.slug}] add a source or set demo:true. Unsourced: ${missing.join(', ')}`);
  }
  return p;
}

export const metadata = (e: EffectDef): CalculateMetadataFunction<any> => ({props}) => {
  const p = checkProps(e, props); return {durationInFrames: totalFrames(e.frames, e.beats, p), props: p};
};

export function shell(e: EffectDef): React.FC<any> {
  const C = e.Component;
  return (p: Base) => <FontGate><Pal.Provider value={{...BRAND, ...p.brandPalette}}>
    <AbsoluteFill lang={p.language}><C {...p} />{p.demo ? <DemoStamp lang={p.language} captionSafe={p.captionSafe} /> : null}</AbsoluteFill>
  </Pal.Provider></FontGate>;
}

import React from 'react';
import {Composition} from 'remotion';
import {EFFECTS} from './effects';
import {metadata, shell} from './lib/define';

const SIZES = {'9x16': [1080, 1920], '16x9': [1920, 1080]} as const;
const wrapped = EFFECTS.map((e) => ({e, C: shell(e), meta: metadata(e)}));

export const Root: React.FC = () => <>{wrapped.flatMap(({e, C, meta}) => (Object.keys(SIZES) as (keyof typeof SIZES)[]).map((a) =>
  <Composition key={e.slug + a} id={`${e.slug}-${a}`} component={C} width={SIZES[a][0]} height={SIZES[a][1]} fps={30} durationInFrames={e.frames} defaultProps={e.samples.en as any} calculateMetadata={meta} />))}</>;

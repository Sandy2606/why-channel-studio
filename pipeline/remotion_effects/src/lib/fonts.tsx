import React, {useEffect, useState} from 'react';
import {continueRender, delayRender, staticFile} from 'remotion';
// Fonts are copied from brand/fonts by cli/sync-fonts.mjs, so the repo keeps one copy.
const FACES: [string, string, string][] = [
  ['Archivo Black', 'ArchivoBlack-Regular.ttf', '400'],
  ['Space Mono', 'SpaceMono-Regular.ttf', '400'],
  ['Space Mono', 'SpaceMono-Bold.ttf', '700'],
  ['Noto Sans Telugu', 'NotoSansTelugu.ttf', '100 900'],
];
let ready: Promise<void> | null = null;
const load = () => (ready ??= Promise.all(FACES.map(async ([fam, file, weight]) => {
  const f = new FontFace(fam, `url(${staticFile('fonts/' + file)})`, {weight});
  await f.load(); document.fonts.add(f);
})).then(() => undefined));

/** Children render only after real fonts exist, so text measurement uses real glyph metrics. */
export const FontGate: React.FC<{children: React.ReactNode}> = ({children}) => {
  const [handle] = useState(() => delayRender('Loading brand fonts'));
  const [ok, setOk] = useState(false);
  useEffect(() => { load().then(() => { setOk(true); continueRender(handle); }); }, [handle]);
  return ok ? <>{children}</> : null;
};

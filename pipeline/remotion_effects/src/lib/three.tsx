import React, {useMemo} from 'react';
import {ThreeCanvas} from '@remotion/three';
import * as THREE from 'three';
import {useVideoConfig} from 'remotion';

export type CamPose = {pos: [number, number, number]; look: [number, number, number]; fov: number};
export function useCamera(pose: CamPose) {
  const {width, height} = useVideoConfig();
  const cam = useMemo(() => { const c = new THREE.PerspectiveCamera(); (c as any).manual = true; return c; }, []);
  cam.fov = pose.fov; cam.aspect = width / height; cam.near = .1; cam.far = 400; cam.position.set(...pose.pos); cam.lookAt(...pose.look); cam.updateProjectionMatrix(); cam.updateMatrixWorld(true);
  return cam;
}
/** World point to screen pixels, for DOM labels that stay locked to the 3D scene. */
export function project(cam: THREE.Camera, p: [number, number, number], W: number, H: number) {
  const v = new THREE.Vector3(...p).project(cam); return {x: (v.x + 1) / 2 * W, y: (1 - v.y) / 2 * H};
}
export const Stage3D: React.FC<{cam: THREE.Camera; children: React.ReactNode; shadows?: boolean; clip?: boolean}> = ({cam, children, shadows, clip}) => {
  const {width, height} = useVideoConfig();
  return <ThreeCanvas width={width} height={height} camera={cam as any} shadows={shadows} gl={{antialias: true, preserveDrawingBuffer: true}} onCreated={clip ? ((st: any) => { st.gl.localClippingEnabled = true; }) : undefined} style={{position: 'absolute'}}>{children}</ThreeCanvas>;
};

/** Orthographic camera for isometric scenes. viewH is the visible world height. */
export function useOrtho(pose: {pos: [number, number, number]; look: [number, number, number]; viewH: number}) {
  const {width, height} = useVideoConfig();
  const cam = useMemo(() => { const c = new THREE.OrthographicCamera(); (c as any).manual = true; return c; }, []);
  const h = pose.viewH / 2, w = h * width / height;
  cam.left = -w; cam.right = w; cam.top = h; cam.bottom = -h; cam.near = .1; cam.far = 300; cam.position.set(...pose.pos); cam.lookAt(...pose.look); cam.updateProjectionMatrix(); cam.updateMatrixWorld(true);
  return cam;
}

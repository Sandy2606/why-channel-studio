"""GOLD · 5/6 'Why do Indians trust gold more than banks?' — kinetic data + evidence, style v2."""
import sys, os, json, math, subprocess
import numpy as np, cairo
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
_argv = sys.argv; sys.argv = sys.argv[:1]
LANGV = os.environ.get('LANGV', 'en'); PLAT = os.environ.get('PLAT', 'yt')
sys.path.insert(0, '/home/claude/g3'); sys.path.insert(0, '/home/claude/rv')
import render3 as R3
import render2 as K
import host
sys.argv = _argv
W, H, FPS = 1080, 1920, 30
LEAD, TAIL = 0.15, 0.7
ROOT = '/home/claude/g5/'
CREAM, AMBER, AMBER2, INK = K.CREAM, K.AMBER, K.AMBER2, K.INK
prog, e_out, e_io, e_back, clamp = K.prog, K.e_out, K.e_io, K.e_back, K.clamp
font, mono, head, rrect = K.font, K.mono, K.head, K.rrect
glowdot, glass_dark, agrad = K.glowdot, K.glass_dark, K.agrad
surf_from_pil, torn, thread, board_bg = R3.surf_from_pil, R3.torn, R3.thread, R3.board_bg
def pill(c, *a, **k):
    if k.get('s', 1.0) <= 0.01: return
    K.pill(c, *a, **k)


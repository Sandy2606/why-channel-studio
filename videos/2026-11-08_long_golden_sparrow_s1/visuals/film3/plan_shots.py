# Shot plan per narration line (film order). Shorthands build ('st', key, z0, z1, fx0, fy0, fx1, fy1, par, fit).
def IN(k, fx=.5, fy=.5, z=1.12, par=.10): return ('st', k, 1.0, z, fx, fy, fx, fy, par, False)
def OUT(k, fx=.5, fy=.5, z=1.14, par=.08): return ('st', k, z, 1.0, fx, fy, .5, .5, par, False)
def PAN(k, x0, x1, y=.5, z=1.15, par=.06): return ('st', k, z, z, x0, y, x1, y, par, False)
def CLOSE(k, fx, fy, z0=1.5, z1=1.7, par=.0): return ('st', k, z0, z1, fx, fy, fx, fy, par, False)
def FIT(k, z0=1.0, z1=1.06, fx=.5, fy=.5): return ('st', k, z0, z1, fx, fy, fx, fy, 0.0, True)
def DOC(k, fx, fy, z0=1.0, z1=1.25): return ('st', k, z0, z1, .5, .5, fx, fy, 0.0, True)
def MAP(key): return ('map', key)
def CARD(n): return ('card', n)
def TEXT(en, te=''): return ('text', en, te)

# --- places (lon, lat)
P = dict(Machilipatnam=(81.14, 16.17), Golconda=(78.40, 17.38), Kollur=(80.02, 16.72), Srikalahasti=(79.70, 13.75), Pedana=(81.17, 16.26),
         Madras=(80.28, 13.08), Surat=(72.83, 21.17), Swally=(72.62, 21.08), Bombay=(72.88, 19.08), Calcutta=(88.36, 22.57), Plassey=(88.25, 23.80),
         Buxar=(83.98, 25.57), Calicut=(75.78, 11.25), Malindi=(40.12, -3.22), Malacca=(102.25, 2.19), Aden=(45.03, 12.8), Hormuz=(56.45, 27.1),
         Aceh=(95.32, 5.55), Arakan=(93.19, 20.6), Venice=(12.33, 45.44), Lisbon=(-9.14, 38.72), London=(-0.12, 51.5), Pondicherry=(79.83, 11.93),
         Talikota=(76.31, 16.47), Vijayanagara=(76.46, 15.33), Penukonda=(77.6, 14.08), Chandragiri=(79.31, 13.58), Vellore=(79.13, 12.92),
         Arcot=(79.32, 12.9), Hyderabad=(78.47, 17.38), Delhi=(77.2, 28.6), Agra=(78.0, 27.18), Mehrgarh=(67.6, 29.38), Dhaka=(90.4, 23.8),
         Isfahan=(51.67, 32.65), Mocha=(43.25, 13.32), Pegu=(96.48, 17.33), Panigiri=(79.47, 17.22))
GOLDC = (214, 168, 74)
def pin(n, cue, side='r'): return (n, P[n][0], P[n][1], cue, side)
COAST = (76.0, 86.5, 10.5, 20.5)
SA = (60, 100, 4, 37)
OCEAN = (25, 125, -20, 38)
# map specs: cues are FRACTIONS of the shot (resolved to seconds in film.py)
MAPS = {
 'india_glow': dict(box0=(-20, 150, -25, 62), box1=(40, 115, -5, 45), gold=True, pins=[]),
 'london_route': dict(box0=(-15, 100, -38, 58), box1=(-15, 100, -38, 58), pins=[pin('Machilipatnam', .1, 'r'), pin('London', .55, 'u')],
                      routes=[([P['Machilipatnam'], (80, 5), (73, -8), (40, -36), (18, -36), (-5, -10), (-18, 15), (-12, 40), (-5, 49), P['London']], .2)]),
 'mehrgarh': dict(box0=SA, box1=(62, 82, 20, 35), pins=[pin('Mehrgarh', .25)]),
 'golconda': dict(box0=(70, 92, 8, 26), box1=COAST, pins=[pin('Golconda', .1, 'l'), pin('Machilipatnam', .55)],
                  glows=[('Golconda kingdom', 79.3, 17.0, 3.2, (200, 150, 40), .05)], routes=[([P['Golconda'], (79.6, 16.9), P['Machilipatnam']], .45, GOLDC, 'land')]),
 'port_routes': dict(box0=OCEAN, box1=OCEAN, pins=[pin('Machilipatnam', 0.0)],
                     routes=[([P['Machilipatnam'], (82, 8), (70, 10), (58, 18), P['Hormuz'], P['Isfahan']], .12), ([P['Machilipatnam'], (80, 8), (60, 12), P['Mocha']], .3),
                             ([P['Machilipatnam'], (90, 16), P['Pegu']], .45), ([P['Machilipatnam'], (92, 8), P['Aceh'], P['Malacca']], .6)],
                     glows=[('Persia', 53, 32, 4, (120, 140, 178), .12), ('Arabia', 45, 20, 4, (120, 140, 178), .3), ('Burma', 96, 20, 3, (120, 140, 178), .45), ('Southeast Asia', 104, 4, 5, (120, 140, 178), .6)]),
 'kalamkari_today': dict(box0=COAST, box1=(78.5, 83, 12.5, 18), pins=[pin('Srikalahasti', .15), pin('Machilipatnam', .45), pin('Pedana', .6, 'u')]),
 'kollur': dict(box0=(-10, 130, -20, 40), box1=(77, 83.5, 14.5, 19), pins=[pin('Kollur', .35, 'l')]),
 'mughal_golconda': dict(box0=(68, 92, 8, 32), box1=COAST, glows=[('Mughal empire', 77, 25, 7, (150, 70, 60), .05), ('', 79.3, 17.0, 3.2, (150, 70, 60), .4)], pins=[pin('Golconda', .1, 'l'), pin('Machilipatnam', .2)]),
 'deccan': dict(box0=(68, 90, 8, 30), box1=(72, 86, 10, 22), pins=[pin('Vijayanagara', .12), pin('Talikota', .22, 'u'), pin('Penukonda', .35), pin('Chandragiri', .42), pin('Vellore', .5, 'd'), pin('Golconda', .62), pin('Delhi', .78)],
                glows=[('Deccan sultanates', 77, 18, 3, (120, 140, 178), .62), ('Mughal empire', 77, 26, 6, (150, 70, 60), .78)]),
 'ocean_wide': dict(box0=(70, 92, 8, 24), box1=OCEAN, pins=[pin('Machilipatnam', .0)]),
 'ocean_routes': dict(box0=OCEAN, box1=OCEAN, pins=[pin('Calicut', .1), pin('Malacca', .55), pin('Aden', .2, 'u'), pin('Hormuz', .3), pin('Malindi', .4, 'l')],
                      routes=[([P['Malindi'], (55, 2), P['Calicut']], .1), ([P['Aden'], (60, 14), P['Calicut']], .2), ([P['Hormuz'], (65, 20), P['Surat']], .3),
                              ([P['Calicut'], (82, 6), (95, 6), P['Malacca']], .5), ([P['Machilipatnam'], (92, 10), P['Malacca']], .6)]),
 'roman': dict(box0=SA, box1=(74, 86, 12, 22), pins=[pin('Panigiri', .4, 'l')], glows=[('', 80, 16.5, 2.5, (200, 150, 40), .3)]),
 'monsoon': dict(box0=OCEAN, box1=OCEAN, arrows=[(50, -5, 70, 10, .05, .55), (55, 2, 78, 14, .1, .55), (85, 15, 62, 5, .58, 1.2), (78, 20, 55, 10, .62, 1.2)],
                 glows=[('SW monsoon · summer', 62, -6, 0.1, (10, 10, 10), .1), ('NE monsoon · winter', 70, 22, 0.1, (10, 10, 10), .6)]),
 'malindi': dict(box0=OCEAN, box1=(30, 85, -12, 20), pins=[pin('Malindi', .05, 'l'), pin('Calicut', .4)], routes=[([P['Malindi'], (52, 2), (66, 8), P['Calicut']], .1)]),
 'cape': dict(box0=(-25, 120, -40, 50), box1=(-25, 120, -40, 50), pins=[pin('Venice', .05, 'u'), pin('Lisbon', .45, 'l')],
              routes=[([P['Calicut'], (60, 12), P['Aden'], (38, 22), (32, 30), (25, 34), P['Venice']], .05, (110, 106, 120)), ([P['Lisbon'], (-18, 20), (-5, -20), (18, -36), (40, -20), (55, 2), P['Calicut']], .45)]),
 'surat': dict(box0=SA, box1=(66, 82, 16, 30), pins=[pin('Surat', .1, 'l'), pin('Swally', .4, 'd'), pin('Agra', .25)], routes=[([P['Surat'], (75, 24), P['Agra']], .15, GOLDC, 'land')]),
 'madras': dict(box0=SA, box1=COAST, pins=[pin('Machilipatnam', .1), pin('Madras', .5)]),
 'company_war': dict(box0=SA, box1=SA, pins=[pin('Bombay', .1, 'l'), pin('Surat', .15, 'l'), pin('Calcutta', .7)], glows=[('Mughal empire', 78, 24, 8, (150, 70, 60), .2)]),
 'carnatic': dict(box0=SA, box1=(72, 86, 8, 22), pins=[pin('Pondicherry', .15), pin('Madras', .2, 'u'), pin('Arcot', .45, 'l'), pin('Hyderabad', .55)],
                  glows=[('Hyderabad (Nizam)', 78.5, 17.5, 1.8, (120, 140, 178), .5), ('Arcot (Carnatic)', 79, 12.5, 1.4, (186, 84, 60), .45)]),
 'circars': dict(box0=SA, box1=COAST, glows=[('Northern Circars · French 1753', 82.2, 17.2, 1.7, (90, 110, 200), .2)], pins=[pin('Machilipatnam', .3)]),
 'bengal_1756': dict(box0=SA, box1=(76, 96, 10, 28), pins=[pin('Calcutta', .15), pin('Madras', .6, 'l')], routes=[([P['Madras'], (84, 14), (88, 19), P['Calcutta']], .65)]),
 'masuli_1759': dict(box0=SA, box1=COAST, pins=[pin('Machilipatnam', .2)]),
 'diwani': dict(box0=SA, box1=(76, 96, 16, 30), pins=[pin('Plassey', .05), pin('Buxar', .35, 'u')], glows=[('Bengal · Bihar · Orissa', 86, 23.5, 3.5, (200, 150, 40), .6)]),
}

SHOTS = {
 # ---- cold open
 '0.1': [('seq', '0.1')],
 '0.2': [('seq', '0.2')],
 '0.3': [('seq', '0.3')],
 '0.4': [MAP('india_glow')],
 '0.5': [('seq', '0.5')],
 # ---- trunk
 'F1.1': [IN('T3', .5, .55, 1.08)],
 'F1.2': [('seq', 'F1.2')],
 'F1.3': [IN('T4', .5, .5, 1.2), CLOSE('MET1', .5, .35, 1.6, 1.8), IN('G01', .5, .6, 1.1, .14)],
 # ---- ch1
 '1.0': [CARD(1)],
 '1.1': [IN('G01', .5, .55, 1.1, .14)],
 '1.2': [IN('G02', .55, .55, 1.12, .12)],
 '1.3': [OUT('PD01', .5, .6, 1.2), MAP('mehrgarh')],
 '1.4': [('poc',)], '1.4e': [('poc',)], '1.5': [('poc',)], '1.6': [('poc',)],
 '1.7': [('poc',), PAN('G03', .3, .7, .55, 1.12, .08)],
 '1.8': [CLOSE('G04', .55, .45, 1.0, 1.12), IN('T5', .45, .55, 1.12, .1)],
 # ---- ch2
 '2.0': [CARD(2)],
 '2.1': [('seq', '2.1')],
 '2.2': [('seq', '2.2')],
 '2.3': [('seq', '2.3')],
 '2.4': [('seq', '2.4')],
 '2.5': [('split25',)],
 '2.6': [('seq', '2.6')],
 '2.7': [MAP('kalamkari_today'), IN('CC06', .5, .5, 1.12)],
 '2.8': [TEXT('COEURDOUX · LETTERS FROM PONDICHERRY · 1740s', 'కర్డూ · పాండిచ్చేరి నుంచి ఉత్తరాలు · 1740లు'), IN('G06', .7, .5, 1.12)],
 '2.9': [IN('G07', .5, .45, 1.1)],
 '2.10': [FIT('PD04', 1.0, 1.12, .5, .4)],
 '2.11': [('bantl',), IN('G08', .5, .5, 1.12, .1)],
 '2.12': [DOC('PD03', .5, .14, 1.0, 2.2)],
 '2.13': [('bantl',)],
 '2.14': [OUT('MET1', .5, .45, 1.4)],
 '2.15': [('seq', '2.15')],
 '2.16': [CLOSE('G14', .7, .4, 1.15, 1.25), IN('T1', .5, .6, 1.1)],
 # ---- ch3
 '3.0': [CARD(3)],
 '3.1': [IN('CC01', .5, .5, 1.12)],
 '3.2': [('seq', '3.2')],
 '3.3': [('seq', '3.3')],
 '3.4': [IN('CC02', .5, .5, 1.12), FIT('PD07', 1.0, 1.15)],
 '3.5': [IN('G11', .5, .5, 1.15)],
 '3.6': [MAP('kollur')],
 '3.7': [IN('G12', .5, .55, 1.1, .1), FIT('PD02', 1.0, 1.2)],
 '3.8': [TEXT('KOH-I-NOOR · MINE OF ORIGIN · DEBATED', 'కోహినూర్ · ఏ గని? · చర్చనీయాంశం')],
 '3.9': [('split39',)],
 '3.10': [MAP('mughal_golconda')],
 '3.11': [IN('G14', .45, .5, 1.12, .1), CLOSE('G14', .3, .55, 1.3, 1.45)],
 '3.12': [('seq', '3.12')],
 'F2.1': [IN('G15', .55, .35, 1.1)],
 'F2.2': [('lang', FIT('PD18a', 1.0, 1.12), FIT('PD18b', 1.0, 1.12))],
 # ---- ch4
 '4.0': [CARD(4)],
 '4.1': [IN('G16', .4, .55, 1.1)],
 '4.2': [('seq', '4.2')],
 '4.3': [IN('CC03', .5, .5, 1.12), FIT('PD07', 1.05, 1.2)],
 '4.4': [FIT('PD08', 1.0, 1.12, .5, .4)],
 '4.5': [OUT('G02', .5, .5, 1.2)],
 '4.6': [('seq', '4.6')],
 '4.7': [IN('G18', .5, .5, 1.12, .1)],
 '4.8': [IN('G19', .45, .5, 1.12, .1), CLOSE('G19', .55, .6, 1.3, 1.4)],
 '4.9': [('seq', '4.9')],
 '4.10': [('seq', '4.10')],
 '4.11': [IN('G21', .5, .45, 1.12, .1)],
 # ---- ch5
 '5.0': [CARD(5)],
 '5.1': [FIT('PD10', 1.0, 1.25, .5, .5)],
 '5.2': [IN('T1', .5, .55, 1.12, .1), MAP('ocean_wide')],
 '5.3': [MAP('ocean_routes')],
 '5.4': [MAP('roman'), FIT('PD19', 1.0, 1.15)],
 '5.5': [('seq', '5.5')],
 '5.6': [('seq', '5.6')],
 '5.7': [('seq', '5.7')],
 '5.8': [('seq', '5.8')],
 '5.9': [MAP('cape')],
 '5.10': [('seq', '5.10')],
 # ---- ch6
 '6.0': [CARD(6)],
 '6.1': [FIT('PD12', 1.0, 1.12)],
 '6.2': [IN('G24', .5, .5, 1.12, .1), CLOSE('G24', .45, .62, 1.3, 1.4)],
 '6.3': [('seq', '6.3')],
 '6.4': [DOC('FARMAN', .7, .1, 1.0, 1.3)],
 '6.5': [('seq', '6.5')],
 '6.6': [IN('G25', .55, .55, 1.12, .1)],
 '6.7': [('seq', '6.7')],
 '6.8': [CLOSE('G26', .7, .5, 1.3, 1.4)],
 '6.8b': [('seq', '6.8b')],
 '6.9': [IN('G27', .4, .5, 1.12, .1), CLOSE('G27', .62, .55, 1.25, 1.4)],
 '6.10': [('seq', '6.10')],
 '6.11': [MAP('circars')],
 '6.12': [('seq', '6.12')],
 '6.13': [('seq', '6.13')],
 # ---- ending
 '7.1': [('seq', '7.1')],
 '7.2': [('seq', '7.2')],
 '7.3': [('seq', '7.3')],
 '7.4': [('seq', '7.4')],
 '7.5': [('seq', '7.5')],
 '7.6': [('seq', '7.6')],
 '7.7': [CLOSE('T7', .7, .4, 1.3, 1.4)],
 '7.8': [CLOSE('T7', .3, .4, 1.3, 1.4)],
 '7.9': [IN('T8', .5, .5, 1.12)],
}

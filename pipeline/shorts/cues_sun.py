# Sunday Short cues: "Why do we burn Ravana's effigy?"
CREAM = (244, 241, 234); AMBER = (255, 178, 36); RED = (240, 72, 56)
FIT = (1080, 1420, 1060)
C10a = 'Ramlila performance · PKritika · CC BY-SA 4.0 · Wikimedia Commons'
C10b = 'A scene of Ramlila · TarunNTL1998 · CC BY-SA 4.0 · Wikimedia Commons'
C11 = 'Tulsidas composing the Ramcharitmanas · bazaar art, 1940s · Public domain'
C12 = 'Ramcharitmanas illustration, Jodhpur c.1775 · Mehrangarh Museum Trust · Public domain'
C13 = 'Ram Leela at Ramnagar · James Prinsep, 1834 · Public domain'
C14 = 'Ramnagar Fort · Dksahani18 · CC BY-SA 4.0 · Wikimedia Commons'
C15 = 'Burning effigy, Vijayadashami · Dhruv Khichi · Pexels'
CE2 = 'Ravana erupts · Pete Birkinshaw · CC BY 2.0 · Wikimedia Commons'
CE3 = 'Ravana fizzles · Pete Birkinshaw · CC BY 2.0 · Wikimedia Commons'
CE4 = 'Ravan Dahan · Hetavee · CC0 · Wikimedia Commons'
CE5 = 'Burning of Ravan · DiplomatTesterMan · CC BY-SA 4.0 · Wikimedia Commons'
S_UN = 'UNESCO, 2008'; S_RL = 'UNESCO · RAMLILA (WIKIPEDIA)'
CARDS = dict(un=dict(source='UNESCO', date='2008', head='Ramlila, the traditional performance of the Ramayana', hl=(0,)))

def get_cues(lang):
    if lang == 'en':
        SC = [
            dict(t=0.0, kind='big', bg=('img', 'AI07_Valmiki_writing_Ramayana_9x16.png', .2), lab='IN THE RAMAYANA', big='NEVER', bcol=RED, bpx=230, bd=1.2, by=640, ai=True, sfx=False),
            dict(t=4.9, kind='head', bg=('img', 'P15.jpg', .25, (.5, .35)), credit=C15),
            dict(t=7.5, kind='big', bg=('img', 'P10a.jpg', .3, (.5, .5)), lab='THE RAMAYANA AS A PLAY', big='RAMLILA', bpx=170, bd=.6, by=640, credit=C10a, src=S_RL),
            dict(t=9.0, kind='head', bg=('img', 'P10b.jpg', .3, (.5, .5)), credit=C10b, src=S_RL),
            dict(t=11.95, kind='head', bg=('img', 'P12.jpg', .3, (.5, .5), FIT), credit=C12, src=S_RL),
            dict(t=13.9, kind='big', bg=('img', 'P11.jpg', .3, (.5, .3)), big='1500s', bpx=220, bd=1.6, by=640, lab='TULSIDAS', credit=C11, src=S_RL),
            dict(t=16.45, kind='big', bg=('img', 'P10a.jpg', .6, (.3, .5)), lab='UNESCO WORLD HERITAGE', big='2008', bpx=260, bd=.9, by=600, src=S_UN, card='un', card_t=17.6, card_y=1520),
            dict(t=20.0, kind='big', bg=('img', 'P14.jpg', .3, (.5, .5)), lab='NEAR VARANASI', big='RAMNAGAR', bpx=128, bd=.2, by=600, credit=C14),
            dict(t=21.9, kind='big', bg=('img', 'P13.jpg', .35, (.5, .5), FIT), lab='PAINTED IN 1834', big='1 MONTH', bpx=200, bd=.5, by=560, credit=C13, src=S_RL),
            dict(t=23.1, kind='head', bg=('img', 'AI03_Rama_vs_Ravana.png', .3, (.4, .5)), ai=True, drop=True),
            dict(t=25.0, kind='head', bg=('img', 'AI03_Rama_vs_Ravana.png', .2, (.7, .2)), ai=True, sfx=False),
            dict(t=25.65, kind='head', bg=('img', 'E3.jpg', .1, (.45, .5)), credit=CE3),
            dict(t=28.85, kind='head', bg=('img', 'E2.jpg', .05, (.5, .5)), credit=CE2, boom=True),
            dict(t=29.7, kind='head', bg=('img', 'E4.jpg', .1, (.62, .5)), credit=CE4),
            dict(t=31.0, kind='head', bg=('img', 'E5.jpg', .1, (.55, .5)), credit=CE5),
            dict(t=32.3, kind='head', bg=('img', 'AI08_Ravana_ten_heads_emotions_9x16.png', .25), ai=True),
            dict(t=34.6, kind='big', bg=('img', 'AI08_Ravana_ten_heads_emotions_9x16.png', .45, (.5, .25)), big='10', bpx=380, bd=.8, by=700, lab='THINGS INSIDE US', ai=True),
            dict(t=38.3, kind='head', bg=('img', 'P15.jpg', .25, (.5, .5)), credit=C15),
            dict(t=40.6, kind='head', bg=('img', 'AI09_Ravana_inside_us_shadow_9x16.png', .2), ai=True, boom=True),
            dict(t=44.25, kind='big', bg=('clip', 'R02', .3), big='FULL VIDEO', bpx=130, bd=.2, by=640, lab='DUSSEHRA · THE FULL STORY', bcol=AMBER),
            dict(t=45.9, kind='cta', bg=('grid', ['S07', 'S02', 'S08', 'R02'], .75), src='SOURCES & CREDITS IN DESCRIPTION'),
        ]
    else:
        SC = [
            dict(t=0.0, kind='big', bg=('img', 'AI07_Valmiki_writing_Ramayana_9x16.png', .2), lab='రామాయణంలో', big='ఎక్కడా లేదు', bcol=RED, bpx=150, bd=2.6, by=640, ai=True, sfx=False),
            dict(t=5.82, kind='head', bg=('img', 'P15.jpg', .25, (.5, .35)), credit=C15),
            dict(t=8.35, kind='big', bg=('img', 'P10a.jpg', .3, (.5, .5)), lab='రామాయణ నాటకం', big='RAMLILA', bpx=170, bd=.4, by=640, credit=C10a, src=S_RL),
            dict(t=9.89, kind='head', bg=('img', 'P10b.jpg', .3, (.5, .5)), credit=C10b, src=S_RL),
            dict(t=12.6, kind='head', bg=('img', 'P12.jpg', .3, (.5, .5), FIT), credit=C12, src=S_RL),
            dict(t=13.8, kind='big', bg=('img', 'P11.jpg', .3, (.5, .3)), big='1500s', bpx=220, bd=.3, by=640, lab='తులసీదాస్', credit=C11, src=S_RL),
            dict(t=17.47, kind='big', bg=('img', 'P10a.jpg', .6, (.3, .5)), lab='UNESCO WORLD HERITAGE', big='2008', bpx=260, bd=1.6, by=600, src=S_UN, card='un', card_t=18.6, card_y=1520),
            dict(t=21.5, kind='big', bg=('img', 'P14.jpg', .3, (.5, .5)), lab='వారణాసి దగ్గర', big='RAMNAGAR', bpx=128, bd=.4, by=600, credit=C14),
            dict(t=23.3, kind='big', bg=('img', 'P13.jpg', .35, (.5, .5), FIT), lab='1834 నాటి చిత్రం', big='నెల మొత్తం', bpx=150, bd=.6, by=560, credit=C13, src=S_RL),
            dict(t=25.13, kind='head', bg=('img', 'AI03_Rama_vs_Ravana.png', .3, (.4, .5)), ai=True, drop=True),
            dict(t=27.4, kind='head', bg=('img', 'AI03_Rama_vs_Ravana.png', .2, (.7, .2)), ai=True, sfx=False),
            dict(t=28.53, kind='head', bg=('img', 'E3.jpg', .1, (.45, .5)), credit=CE3),
            dict(t=31.38, kind='head', bg=('img', 'E2.jpg', .05, (.5, .5)), credit=CE2, boom=True),
            dict(t=32.09, kind='head', bg=('img', 'E4.jpg', .1, (.62, .5)), credit=CE4),
            dict(t=33.2, kind='head', bg=('img', 'E5.jpg', .1, (.55, .5)), credit=CE5),
            dict(t=34.16, kind='head', bg=('img', 'AI08_Ravana_ten_heads_emotions_9x16.png', .25), ai=True),
            dict(t=35.33, kind='big', bg=('img', 'AI08_Ravana_ten_heads_emotions_9x16.png', .45, (.5, .25)), big='10', bpx=380, bd=.8, by=700, lab='మనలో చెడు గుణాలు', ai=True),
            dict(t=40.65, kind='head', bg=('img', 'P15.jpg', .25, (.5, .5)), credit=C15),
            dict(t=42.54, kind='head', bg=('img', 'AI09_Ravana_inside_us_shadow_9x16.png', .2), ai=True, boom=True),
            dict(t=45.66, kind='big', bg=('clip', 'R02', .3), big='FULL VIDEO', bpx=130, bd=.3, by=640, lab='దసరా పూర్తి కథ', bcol=AMBER),
            dict(t=47.3, kind='cta', bg=('grid', ['S07', 'S02', 'S08', 'R02'], .75), src='SOURCES & CREDITS IN DESCRIPTION'),
        ]
    EV = []
    for i, s in enumerate(SC):
        if s.get('card') and s.get('card_t', 0) < 900:
            d = dict(CARDS[s['card']]); d['t'] = s['card_t']; d['t1'] = SC[i + 1]['t']; d['y'] = s.get('card_y', 1500); EV.append(d)
    return SC, EV

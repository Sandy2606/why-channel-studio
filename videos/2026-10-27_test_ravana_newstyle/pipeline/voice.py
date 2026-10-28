import sys, json
sys.path.insert(0,'/home/claude/sandy2606/why-channel-studio/pipeline/shorts')
import proasm
proasm.ROOT='/home/claude/rv/'
KEEP=[
 (54.38,59.12,'raw'),   # 0 There is a 35-foot statue of him, and women cover their heads when they pass it,
 (70.12,72.70),   # 1 just like they do in front of their in-laws.
 (12.62,12.90),   # 2 Why?
 (47.60,53.86),   # 3 Mandodari ... son-in-law
 (5.28,12.36),    # 4 On Dasara all over India we burn Ravana... They pray to him.
 (73.35,74.12,'raw'), # 5a In Jodhpur
 (75.72,79.66),   # 5b Rajasthan, Dev Goda descendants
 (102.86,112.10), # 6 On Dasara... funeral... Ravana temple
 (133.60,144.50), # 7 Baijnath penance
 (168.16,175.30), # 8 burning Shiva's biggest devotee... stopped doing it
 (182.70,185.56), # 9 Ravana wasn't only a villain
 (193.58,196.20), # 10 So yes, in these places, Ravana is family.
 (249.97,255.60,'raw'), # 11 whenever you get a question ... answer
]
proasm.build('ravana',KEEP,'/home/claude/rv/voice0.wav',gap=0.07)

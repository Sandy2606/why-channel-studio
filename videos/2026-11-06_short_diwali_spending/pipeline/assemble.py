h=open('part_head.py').read(); hp=open('part_helpers.py').read(); tl=open('part_tail.py').read(); sc=open('part_scenes.py').read()
open('render_b5.py','w').write(h+sc.replace('"""HELPERS"""',hp)+'\n'+tl)

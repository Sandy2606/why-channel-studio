import sys, traceback
lang=sys.argv[1]; sys.argv=['film.py',lang,'none']
exec(open('film.py').read().split("if __name__ == '__main__':")[0])
bad=[]
for (a,b,sp,i) in SHOTLIST:
    for t in (a+0.01,(a+b)/2,b-0.02):
        try: frame(t)
        except Exception as e:
            bad.append((i,sp[:2],round(t,2),repr(e)[:120])); break
for x in bad: print(x)
print('checked',len(SHOTLIST),'bad',len(bad))

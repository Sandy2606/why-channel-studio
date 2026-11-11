import sys, os
os.environ['LANGV']=sys.argv[1]
import cues as c
T=lambda k,en,te,n=1,off=0: round(c.AT(k,en,te,n=n)+off,2)
ts=[T('5.5','Their','వాళ్ల',off=1.0), T('5.5','back','మిగతా',off=.35), T('5.5','back','మిగతా',off=1.6), T('5.5','Sailors','నావికులు',off=1.2),
    T('PILOT',"His","డ",off=.6), T('PILOT',"'Christian'…","'క్రైస్తవుడు'",off=1.4), T('PILOT','so','అందుకే',off=1.0),
    T('PILOT','Later','తర్వాతి',off=1.0), T('PILOT','Malemo','మాలెమో',off=1.0), T('PILOT','title,','బిరుదు:',off=1.0),
    T('PILOT','famous','అతను',off=1.0), T('PILOT','unlikely.','కానీ',n=1 if sys.argv[1]=='en' else 2,off=1.0), T('PILOT','Gujarat,','గుజరాత్‌కు',n=2,off=.9)]
print(','.join(map(str,ts)))

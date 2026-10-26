# Reps vs posts per author (log-log), one bubble per distinct
# (posts, reps) pair, area ~ members. Data: reps.tsv (Usenet full
# run r2, S1 final snapshot; address, posts, posting_days, reps).
# Usage: python3 reps.py > reps.svg; inkscape reps.svg --export-type=pdf
#        (or: soffice --headless --convert-to pdf reps.svg)
# Fonts are sized for the figure at ~1/4 scale (one column, 900 px -> 240 pt).
import math, collections
W,H=900,520; L,R,T,B=110,30,30,80
INK='#000000'; INK2='#555555'; GRID='#dddddd'; FILL='#777777'; SURF='#ffffff'
FONT='font-family="Helvetica, Arial, sans-serif"'
CAP=50000; TICK=1000
c=collections.Counter()
for i,l in enumerate(open('reps.tsv')):
    if i: _,p,_,r=l.split('\t'); c[(int(p),int(r))]+=1
x0,x1=math.log10(0.8),math.log10(500); y0,y1=math.log10(400),math.log10(70000)
def X(v): return L+(math.log10(v)-x0)/(x1-x0)*(W-L-R)
def Y(v): return H-B-(math.log10(v)-y0)/(y1-y0)*(H-T-B)
def txt(x,y,s,size=26,anchor='start',fill=INK2,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" {FONT} font-size="{size}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
   f'<rect width="{W}" height="{H}" fill="{SURF}"/>']
for v in [500,1000,2000,5000,10000,20000,50000]:
    p.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{GRID}"/>')
    p.append(txt(L-10,Y(v)+9,f'{v//1000}k' if v>=1000 else str(v),anchor='end'))
for v in [1,2,5,10,20,50,100,200,400]:
    p.append(f'<line y1="{T}" y2="{H-B}" x1="{X(v):.1f}" x2="{X(v):.1f}" stroke="{GRID}"/>')
    p.append(txt(X(v),H-B+32,str(v),anchor='middle'))
p.append(txt((L+W-R)/2,H-16,'posts per author',size=28,anchor='middle',fill=INK))
p.append(txt(30,(T+H-B)/2,'reps',size=28,anchor='middle',fill=INK,extra=f'transform="rotate(-90 30 {(T+H-B)/2})"'))
# minting line: reps = TICK x posts, capped
p.append(f'<polyline fill="none" stroke="{INK2}" stroke-width="1.5" stroke-dasharray="6 4" '
         f'points="{X(0.8):.1f},{Y(0.8*TICK):.1f} {X(CAP/TICK):.1f},{Y(CAP):.1f} {X(500):.1f},{Y(CAP):.1f}"/>')
ax,ay=X(2.0),Y(5000)-14
p.append(txt(ax,ay,'1,000 reps per posting day',size=24,extra=f'transform="rotate(-37 {ax:.0f} {ay:.0f})"'))
p.append(txt(X(280),Y(CAP)-14,'cap 50,000',size=24,anchor='middle'))
# bubbles: small first so large ones do not hide them
for (pp,r),n in sorted(c.items(), key=lambda kv: -kv[1]):
    rad=max(2.5,math.sqrt(n)/3.0)
    p.append(f'<circle cx="{X(pp):.1f}" cy="{Y(r):.1f}" r="{rad:.1f}" fill="{FILL}" fill-opacity="0.55" stroke="{SURF}" stroke-width="1"/>')
for pp,r,lab,dy in [(1,1000,'8,465 authors',9),(2,2000,'1,687',9),(3,3000,'645',9)]:
    p.append(txt(X(pp)+max(2.5,math.sqrt(c[(pp,r)])/3.0)+6,Y(r)+dy,lab,size=24,fill=INK))
p.append(txt(X(5.5),Y(1150),'below the line: several posts in one tick',size=22))
p.append(txt(W-R-6,Y(CAP)+40,'39 authors at the cap',size=22,anchor='end'))
p.append('</svg>'); print('\n'.join(p))

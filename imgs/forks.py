# Usenet forks (SVGs for the paper, one column; classes colored G/Y/R).
# Data: fork-miss.tsv (per post: author class, earlier posts missing) and
# fork-merges.tsv (per merge: reorders, fork life in hours). Both from r5.
# Usage: python3 forks.py   -> fork-depth.svg, fork-time.svg; soffice --headless --convert-to pdf fork-*.svg
import math, collections
W,H=900,520; L,R,T,B=110,30,30,80
INK='#000000'; INK2='#555555'; GRID='#dddddd'; SURF='#ffffff'
FONT='font-family="Helvetica, Arial, sans-serif"'
COL={'all':('#cccccc','',8),'on':('#1e8449','',4),'ps':('#d4a017','6 3',3),'lf':('#c0392b','2 3',3)}
NAME={'all':'All authors','on':'Green authors','ps':'Yellow authors','lf':'Red authors'}
def txt(x,y,s,size=26,anchor='start',fill=INK2):
    return f'<text x="{x:.1f}" y="{y:.1f}" {FONT} font-size="{size}" text-anchor="{anchor}" fill="{fill}">{s}</text>'
def Y(f): return H-B-f*(H-T-B)
def frame(X,ticks,xlab,ylab):
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',f'<rect width="{W}" height="{H}" fill="{SURF}"/>']
    for f in [0,0.25,0.5,0.75,1]:
        p.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(f):.1f}" y2="{Y(f):.1f}" stroke="{GRID}"/>'); p.append(txt(L-10,Y(f)+9,f'{int(f*100)}%',anchor='end'))
    for v,lab in ticks:
        p.append(f'<line y1="{T}" y2="{H-B}" x1="{X(v):.1f}" x2="{X(v):.1f}" stroke="{GRID}"/>'); p.append(txt(X(v),H-B+32,lab,anchor='middle'))
    p.append(txt((L+W-R)/2,H-16,xlab,size=28,anchor='middle',fill=INK)); p.append(txt(L+12,T+28,ylab,size=24,fill=INK))
    return p
def dash(d): return f'stroke-dasharray="{d}"' if d else ''
def cdf(X,vals,color,d,wd=3):   # smooth CDF, ~600 points
    vals=sorted(vals); n=len(vals); step=max(1,n//600)
    pts=[f'{X(vals[i]):.1f},{Y((i+1)/n):.1f}' for i in range(0,n,step)]+[f'{X(vals[-1]):.1f},{Y(1):.1f}']
    return f'<polyline fill="none" stroke="{color}" stroke-width="{wd}" {dash(d)} points="{" ".join(pts)}"/>'
def points(X,vals,color,d,wd=3,mk=5):   # CDF at each count, joined by a curve, with markers
    c=collections.Counter(vals); n=len(vals); acc=0; xy=[]
    for v in sorted(c): acc+=c[v]; xy.append((X(v),Y(acc/n)))
    q=[f'<polyline fill="none" stroke="{color}" stroke-width="{wd}" {dash(d)} points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in xy)}"/>']
    if mk: q+=[f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{mk}" fill="{color}"/>' for x,y in xy]
    return '\n'.join(q)
def legend(p,items,x,y0):
    for i,(name,color,d,wd) in enumerate(items):
        y=y0+i*34; p.append(f'<line x1="{x}" x2="{x+50}" y1="{y}" y2="{y}" stroke="{color}" stroke-width="{wd}" {dash(d)}/>'); p.append(txt(x+60,y+8,name,size=24,fill=INK))
rows=lambda f: [l.rstrip('\n').split('\t') for l in open(f) if l[0].isdigit()]
M=collections.defaultdict(list)
for a,c,m in rows('fork-miss.tsv'):
    if int(m)>0: M[c].append(int(m)); M['all'].append(int(m))
mg=rows('fork-merges.tsv'); reord=[int(r[1]) for r in mg if r[1] not in ('','0')]; life=[float(r[2]) for r in mg if r[2]!='']
# (a) depth: missing posts per forking post (per class) and reorders per merge
X0,X1=math.log10(1),math.log10(50)
def Xa(v): return L+(math.log10(max(v,1))-X0)/(X1-X0)*(W-L-R)
p=frame(Xa,[(1,'1'),(2,'2'),(5,'5'),(10,'10'),(20,'20'),(50,'50')],'missing posts (log)','forking posts')
for k in ['all','on','ps','lf']: p.append(points(Xa,M[k],*COL[k],mk=0 if k=='all' else 5))
p.append(points(Xa,reord,INK,'10 4 2 4',2,4))
legend(p,[(NAME[k]+' (missing)',)+COL[k] for k in ['all','on','ps','lf']]+[('reorders per merge',INK,'10 4 2 4',2)],L+330,T+260)
p.append('</svg>'); open('fork-depth.svg','w').write('\n'.join(p))
# (b) time: fork life per merge, with the 7-day settling window
X0,X1=math.log10(0.1),math.log10(200)
def Xb(v): return L+(math.log10(max(v,0.1))-X0)/(X1-X0)*(W-L-R)
p=frame(Xb,[(0.1,'6min'),(1,'1h'),(6,'6h'),(24,'24h'),(168,'7d')],'hours (log)','merges')
p.append(f'<line y1="{T}" y2="{H-B}" x1="{Xb(168):.1f}" x2="{Xb(168):.1f}" stroke="{INK2}" stroke-dasharray="2 4"/>')
p.append(txt(Xb(168)-10,Y(0.5),'settling window',size=22,anchor='end'))
p.append(cdf(Xb,life,INK,'',3)); legend(p,[('fork life',INK,'',3)],L+20,T+70)
life.sort()
for f in [0.25,0.90]:   # marks: share of merges, label left of the point
    h=life[int(f*len(life))-1]; cx,cy=Xb(h),Y(f)
    p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{SURF}" stroke="{INK}" stroke-width="3"/>')
    p.append(txt(cx-18,cy+8,f'{round(h)}h→{round(f*100)}%',size=24,anchor='end',fill=INK))
p.append('</svg>'); open('fork-time.svg','w').write('\n'.join(p))

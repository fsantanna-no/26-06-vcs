# Usenet forks (SVGs for the paper, one column; classes colored G/Y/R).
# Data: fork-miss.tsv (per post: author class, earlier posts missing) and
# fork-merges.tsv (per merge: reorders, fork life in hours). Both from r5.
# fork-clamps.tsv (per clamped post: clamp delay P_i - S_i in hours, r5 20k).
# fork-time stacks two panels: fork life and clamp delay (top), reorders (bottom).
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
def cdf(X,vals,color,d,wd=3,start=None):   # smooth CDF, ~600 points; start: first (x,share)
    vals=sorted(vals); n=len(vals); step=max(1,n//600)
    xy=[(X(vals[i]),Y((i+1)/n)) for i in range(0,n,step)]+[(X(vals[-1]),Y(1))]
    xy=[q for k,q in enumerate(xy) if k+1==len(xy) or xy[k+1][0]!=q[0]]   # no vertical run at a clamped x
    if start: xy=[(X(start[0]),Y(start[1]))]+xy
    pts=[f'{x:.1f},{y:.1f}' for x,y in xy]
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
    M[c].append(int(m)); M['all'].append(int(m))
mg=rows('fork-merges.tsv'); reord=[int(r[1]) for r in mg if r[1]!='']; life=[float(r[2]) for r in mg if r[2]!='']
# (a) depth: missing posts per post (per class; 0 = no fork)
# linear axis up to 10; the tail (>10) is folded into one last point
CAP=11
def Xa(v): return L+min(v,CAP)/CAP*(W-L-R)
p=frame(Xa,[(v,str(v)) for v in range(0,11)]+[(CAP,'&gt;10')],'missing posts','posts')
for k in ['all','on','ps','lf']: p.append(points(Xa,[min(v,CAP) for v in M[k]],*COL[k],mk=0 if k=='all' else 5))
legend(p,[(NAME[k],)+COL[k] for k in ['all','on','ps','lf']],L+430,T+240)
# marks: share up to a count, circled, with a leader line to the arrow of its label at (lx,lf)
def le(vals,x): return sum(1 for v in vals if v<=x)/len(vals)
def mark(vals,x,lx,lf,anchor,X=Xa):
    f=le(vals,x); cx,cy=X(x),Y(f); s=f'{x}→{round(f*100)}%'
    cw=lambda c: 24*{'→':1.0,'%':0.889}.get(c,0.556)   # Helvetica advance widths
    tx,ty=X(lx),Y(lf); w=sum(map(cw,s)); x0={'start':tx,'middle':tx-w/2,'end':tx-w}[anchor]
    i=s.index('→'); ex,ey=x0+sum(map(cw,s[:i]))+cw('→')/2,min(max(cy,ty-26),ty+10)   # at the arrow, 6px gap
    p.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{INK2}" stroke-width="1.5"/>')
    p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{SURF}" stroke="{INK}" stroke-width="3"/>')
    p.append(txt(tx,ty,s,size=24,anchor=anchor,fill=INK))
mark(M['all'],0,1.1,0.10,'middle'); mark(M['on'],0,2.3,0.21,'middle'); mark(M['lf'],7,7.9,0.66,'middle')
p.append('</svg>'); open('fork-depth.svg','w').write('\n'.join(p))
# (b) time: fork life per merge and clamp delay per clamped post (shorter than (a))
H=520
# clamp delay over all posts: unclamped posts have delay 0 (19,998 posts in S1 list order at 20k)
POSTS=19998; clamp=sorted(float(r[2]) for r in rows('fork-clamps.tsv')); clamp=[0.0]*(POSTS-len(clamp))+clamp
# x: "0" in its own slot, a gap with a break mark, then 30min-60h (log);
# unclamped posts (delay 0) at 0, delays in (0,30min) at 30min
E=0.5; X0,X1=math.log10(E),math.log10(60); G=70
def Xb(v): return L if v<=0 else L+G+(math.log10(max(v,E))-X0)/(X1-X0)*(W-L-R-G)
p=frame(Xb,[(0,'0'),(E,'30min'),(1,'1h'),(2,'2h'),(4,'4h'),(8,'8h'),(16,'16h'),(32,'32h')],'time (log)','share')   # doubling: evenly spaced
bx=L+G/2   # break mark on the x axis
p.append(f'<rect x="{bx-8:.1f}" y="{H-B-12:.1f}" width="16" height="24" fill="{SURF}"/>')
p+=[f'<line x1="{bx+d-6:.1f}" y1="{H-B+10:.1f}" x2="{bx+d+6:.1f}" y2="{H-B-10:.1f}" stroke="{INK2}" stroke-width="2"/>' for d in (-4,4)]
p.append(cdf(Xb,life,INK,'',3)); p.append(cdf(Xb,clamp,INK2,'8 5',3,(0,sum(1 for v in clamp if v<=0)/len(clamp))))   # from the unclamped share
legend(p,[('merges',INK,'',3),('clamps',INK2,'8 5',3)],L+500,T+260)
life.sort()
def at(vals,f): return vals[int(f*len(vals))-1]                 # value at share f
def share(vals,h): return sum(1 for v in vals if v<=h)/len(vals)  # share at value h
for vals,h,f,dx,dy in [(life,at(life,0.25),0.25,-18,8),(life,at(life,0.90),0.90,18,34),
                       (clamp,0,share(clamp,0),18,34),(clamp,at(clamp,0.90),0.90,18,34)]:   # marks, label beside
    cx,cy=Xb(h),Y(f); lab=('0' if h<=0 else f'{round(h)}h')+f'→{round(f*100)}%'
    p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{SURF}" stroke="{INK}" stroke-width="3"/>')
    p.append(txt(cx+dx,cy+dy,lab,size=24,anchor='end' if dx<0 else 'start',fill=INK))
# (c) reorders per merge, as a shorter panel below (same x scale as (a))
H0=H; H=260
q=frame(Xa,[(v,str(v)) for v in range(0,11)]+[(CAP,'&gt;10')],'actions reordered','merges')[2:]
top=p; p=q
p.append(points(Xa,[min(v,CAP) for v in reord],INK,'',3,5))
mark(reord,2,3.4,0.50,'middle')
H=H0+H; top[0]=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'; top[1]=f'<rect width="{W}" height="{H}" fill="{SURF}"/>'
top+=[f'<g transform="translate(0,{H0})">']+p+['</g>','</svg>']; open('fork-time.svg','w').write('\n'.join(top))

# Usenet propagation (SVGs for the paper, one column; prop-cov colors classes G/Y/R).
# Data: prop-posts.tsv (per post: hours to first/half/all peers, r4 30k checkpoint)
# and prop-cov.tsv (delivery delay quantiles per author class, r5 dump).
# Usage: python3 prop.py [chat]   -> prop-cdf.svg, prop-cov[-chat].svg; soffice --headless --convert-to pdf prop-*.svg
# chat: prop-cov-chat.tsv only (no classes, delays in seconds): prop-cov-chat.svg
import math, sys
CHAT=len(sys.argv)>1 and sys.argv[1]=='chat'
W,H=900,520; L,R,T,B=110,30,30,80
INK='#000000'; INK2='#555555'; GRID='#dddddd'; SURF='#ffffff'
FONT='font-family="Helvetica, Arial, sans-serif"'
LO,HI=(1/3600,24) if CHAT else (30/3600,120)   # chat: 1s .. 24h; usenet: 30s .. 120h
X0,X1=math.log10(LO),math.log10(HI)
def X(h): return L+(math.log10(max(h,LO))-X0)/(X1-X0)*(W-L-R)
def Y(f): return H-B-f*(H-T-B)
def txt(x,y,s,size=26,anchor='start',fill=INK2):
    return f'<text x="{x:.1f}" y="{y:.1f}" {FONT} font-size="{size}" text-anchor="{anchor}" fill="{fill}">{s}</text>'
def frame(ylab):
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',f'<rect width="{W}" height="{H}" fill="{SURF}"/>']
    for f in [0,0.25,0.5,0.75,1]:
        p.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(f):.1f}" y2="{Y(f):.1f}" stroke="{GRID}"/>'); p.append(txt(L-10,Y(f)+9,f'{int(f*100)}%',anchor='end'))
    TK=[(1/3600,'1s'),(10/3600,'10s'),(1/60,'1min'),(10/60,'10min'),(1,'1h'),(24,'24h')] if CHAT else [(30/3600,'30s'),(5/60,'5min'),(1,'1h'),(12,'12h'),(120,'120h')]   # x10-x12: nearly even
    for h,lab in TK:
        p.append(f'<line y1="{T}" y2="{H-B}" x1="{X(h):.1f}" x2="{X(h):.1f}" stroke="{GRID}"/>'); p.append(txt(X(h),H-B+32,lab,anchor='middle'))
    p.append(txt((L+W-R)/2,H-16,'time after the post (log)',size=28,anchor='middle',fill=INK))
    p.append(txt(L+12 if not CHAT else W-R-12,T+28 if not CHAT else H-B-12,ylab,size=24,fill=INK,anchor='start' if not CHAT else 'end'))   # chat: curve hugs the top
    return p
def cdf(vals,color,dash,wd=3):   # vals sorted; ~600 points
    n=len(vals); step=max(1,n//600)
    pts=[f'{X(vals[i]):.1f},{Y((i+1)/n):.1f}' for i in range(0,n,step)]+[f'{X(vals[-1]):.1f},{Y(1):.1f}']
    d=f'stroke-dasharray="{dash}"' if dash else ''
    return f'<polyline fill="none" stroke="{color}" stroke-width="{wd}" {d} points="{" ".join(pts)}"/>'
def lab(p,vals,f,name,color,dx=10,dy=-10,anchor='start'):   # label next to the curve at quantile f
    h=vals[int(f*(len(vals)-1))]; p.append(txt(X(h)+dx,Y(f)+dy,name,size=24,anchor=anchor,fill=color))
def chat():   # coverage, a single black series, marks at 5s, 50%, 90%, 99%
    a=sorted(float(l.split()[1]) for l in open('prop-cov-chat.tsv') if l[0].isdigit())
    p=frame('peers reached'); p.append(cdf(a,INK,'',3))
    def at(f): return a[int(f*len(a))-1]
    for h,f,s,dx,dy,anc in [(at(0.5),0.5,f'{round(at(0.5)*3600)}s→50%',20,40,'start'),(at(0.9),0.9,f'{round(at(0.9)*3600)}s→90%',20,40,'start'),
                            (at(0.99),0.99,f'{round(at(0.99)*60)}min→99%',-20,40,'end')]:
        cx,cy=X(h),Y(f)
        p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{SURF}" stroke="{INK}" stroke-width="3"/>'); p.append(txt(cx+dx,cy+dy,s,size=24,anchor=anc,fill=INK))
    p.append('</svg>'); open('prop-cov-chat.svg','w').write('\n'.join(p)); sys.exit()
if CHAT: chat()
# (a) CDF over posts: time until the first peer, half of the peers, all peers
rows=[list(map(float,l.split())) for l in open('prop-posts.tsv') if l[0].isdigit()]
first,half,all_=(sorted(r[i] for r in rows) for i in range(3))
p=frame('posts')
p.append(cdf(first,INK2,'6 3')); p.append(cdf(half,INK2,'')); p.append(cdf(all_,INK,''))
lab(p,first,0.6,'first peer',INK2,dx=-12,anchor='end'); lab(p,half,0.35,'half of the peers',INK2,dx=12); lab(p,all_,0.3,'all peers',INK,dx=12)
p.append('</svg>'); open('prop-cdf.svg','w').write('\n'.join(p))
# (b) coverage: fraction of deliveries done by time t, per author class and all
q=[list(map(float,l.split())) for l in open('prop-cov.tsv') if l[0].isdigit()]
cls={k:[r[i] for r in q] for i,k in enumerate(['on','ps','lf','all'],1)}
p=frame('peers reached')
for i,(k,name,color,dash,wd) in enumerate([('all','All authors','#cccccc','',8),('on','Green authors','#1e8449','',4),('ps','Yellow authors','#d4a017','6 3',3),('lf','Red authors','#c0392b','2 3',3)]):
    p.append(cdf(cls[k],color,dash,wd)); y=T+70+i*34; d=f'stroke-dasharray="{dash}"' if dash else ''
    p.append(f'<line x1="{L+20}" x2="{L+70}" y1="{y}" y2="{y}" stroke="{color}" stroke-width="{wd}" {d}/>'); p.append(txt(L+80,y+8,name,size=24,fill=INK))
def mark(h,f,s,dx,dy,anchor,at=None):   # circled point on a curve with a leader line to its label (at: label at (h,f))
    cx,cy=X(h),Y(f); x,y=(X(at[0]),Y(at[1])) if at else (cx+dx,cy+dy)
    w=0.55*24*len(s); x0={'start':x,'middle':x-w/2,'end':x-w}[anchor]
    lx,ly=x0+w/2,min(max(cy,y-26),y+10)   # middle of the label, 6px gap
    p.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{lx:.1f}" y2="{ly:.1f}" stroke="{INK2}" stroke-width="1.5"/>')
    p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{SURF}" stroke="{INK}" stroke-width="3"/>')
    p.append(txt(x,y,s,size=24,anchor=anchor,fill=INK))
a=cls['all']; f3=sum(1 for h in a if h<=3/60)/len(a); h50=a[int(0.50*len(a))-1]
mark(3/60,f3,f'3min→{round(f3*100)}%',30,-30,'start'); mark(h50,0.50,f'{round(h50)}h→50%',-10,110,'middle'); h90=a[int(0.90*len(a))-1]; mark(h90,0.90,f'{round(h90)}h→90%',0,0,'middle',(50,0.55))
# jumps: thin brackets |---| near the 0% line, in class colors
for x0,x1,f,c in [(30/3600,3/60,0.05,'#1e8449'),(1,6,0.05,'#d4a017'),(6,30,0.11,'#c0392b')]:
    y=Y(f); a,b=X(x0),X(x1)
    p.append(f'<path d="M{a:.1f},{y-8:.1f}V{y+8:.1f}M{a:.1f},{y:.1f}H{b:.1f}M{b:.1f},{y-8:.1f}V{y+8:.1f}" fill="none" stroke="{c}" stroke-width="2"/>')
p.append('</svg>'); open('prop-cov.svg','w').write('\n'.join(p))

# Usenet propagation (grayscale SVGs for the paper, one column).
# Data: prop-posts.tsv (per post: hours to first/half/all peers, r4 30k checkpoint)
# and prop-cov.tsv (delivery delay quantiles per author class, r5 dump).
# Usage: python3 prop.py   -> prop-cdf.svg, prop-cov.svg; soffice --headless --convert-to pdf prop-*.svg
import math
W,H=900,520; L,R,T,B=110,30,30,80
INK='#000000'; INK2='#555555'; GRID='#dddddd'; SURF='#ffffff'
FONT='font-family="Helvetica, Arial, sans-serif"'
X0,X1=math.log10(0.01),math.log10(100)   # 36 s .. 100 h
def X(h): return L+(math.log10(max(h,0.01))-X0)/(X1-X0)*(W-L-R)
def Y(f): return H-B-f*(H-T-B)
def txt(x,y,s,size=26,anchor='start',fill=INK2):
    return f'<text x="{x:.1f}" y="{y:.1f}" {FONT} font-size="{size}" text-anchor="{anchor}" fill="{fill}">{s}</text>'
def frame(ylab):
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',f'<rect width="{W}" height="{H}" fill="{SURF}"/>']
    for f in [0,0.25,0.5,0.75,1]:
        p.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(f):.1f}" y2="{Y(f):.1f}" stroke="{GRID}"/>'); p.append(txt(L-10,Y(f)+9,f'{int(f*100)}%',anchor='end'))
    for h,lab in [(0.01,'36s'),(0.1,'6min'),(1,'1h'),(6,'6h'),(24,'24h'),(100,'100h')]:
        p.append(f'<line y1="{T}" y2="{H-B}" x1="{X(h):.1f}" x2="{X(h):.1f}" stroke="{GRID}"/>'); p.append(txt(X(h),H-B+32,lab,anchor='middle'))
    p.append(txt((L+W-R)/2,H-16,'time after the post (log)',size=28,anchor='middle',fill=INK))
    p.append(txt(L+12,T+28,ylab,size=24,fill=INK))
    return p
def cdf(vals,color,dash,wd=3):   # vals sorted; ~600 points
    n=len(vals); step=max(1,n//600)
    pts=[f'{X(vals[i]):.1f},{Y((i+1)/n):.1f}' for i in range(0,n,step)]+[f'{X(vals[-1]):.1f},{Y(1):.1f}']
    d=f'stroke-dasharray="{dash}"' if dash else ''
    return f'<polyline fill="none" stroke="{color}" stroke-width="{wd}" {d} points="{" ".join(pts)}"/>'
def lab(p,vals,f,name,color,dx=10,dy=-10,anchor='start'):   # label next to the curve at quantile f
    h=vals[int(f*(len(vals)-1))]; p.append(txt(X(h)+dx,Y(f)+dy,name,size=24,anchor=anchor,fill=color))
# (a) CDF over posts: time until the first peer, half of the peers, all peers
rows=[list(map(float,l.split())) for l in open('prop-posts.tsv') if l[0].isdigit()]
first,half,all_=(sorted(r[i] for r in rows) for i in range(3))
p=frame('posts')
p.append(cdf(first,INK2,'6 3')); p.append(cdf(half,INK2,'')); p.append(cdf(all_,INK,''))
lab(p,first,0.6,'first peer',INK2,dx=-12,anchor='end'); lab(p,half,0.35,'half of the peers',INK2,dx=12); lab(p,all_,0.3,'all peers',INK,dx=12)
p.append('</svg>'); open('prop-cdf.svg','w').write('\n'.join(p))
# (b) coverage: fraction of deliveries done by time t, per author class
q=[list(map(float,l.split())) for l in open('prop-cov.tsv') if l[0].isdigit()]
cls={k:[r[i] for r in q] for i,k in enumerate(['on','ps','lf'],1)}
p=frame('peers reached')
for i,(k,name,color,dash,wd) in enumerate([('on','Green authors',INK,'',4),('ps','Yellow authors',INK2,'6 3',3),('lf','Red authors','#888888','2 3',3)]):
    p.append(cdf(cls[k],color,dash,wd)); y=T+70+i*34; d=f'stroke-dasharray="{dash}"' if dash else ''
    p.append(f'<line x1="{L+20}" x2="{L+70}" y1="{y}" y2="{y}" stroke="{color}" stroke-width="{wd}" {d}/>'); p.append(txt(L+80,y+8,name,size=24,fill=INK))
p.append('</svg>'); open('prop-cov.svg','w').write('\n'.join(p))

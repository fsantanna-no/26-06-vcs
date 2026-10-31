# Usenet operation times vs chain size (grayscale SVG for the paper).
# Data: ops.tsv (r4 per 1k: median/p90/max) or ops-r2/ops-chat (mean/max). Fonts for one column.
# Usage: python3 ops.py [ops.tsv] > ops.svg; soffice --headless --convert-to pdf ops.svg
import math, sys
DATA=sys.argv[1] if len(sys.argv)>1 else 'ops.tsv'
W,H=900,520; L,R,T,B=110,30,30,80
INK='#000000'; INK2='#555555'; GRID='#dddddd'; SURF='#ffffff'
FONT='font-family="Helvetica, Arial, sans-serif"'
rows=[list(map(float,l.split())) for l in open(DATA) if not l.startswith('#')]
YMAX=20 if max(r[2] for r in rows)<=20 else 100
x0,x1=0,35000; y0,y1=math.log10(0.05),math.log10(YMAX)
def X(v): return L+(v-x0)/(x1-x0)*(W-L-R)
def Y(v): return H-B-(math.log10(v)-y0)/(y1-y0)*(H-T-B)
def txt(x,y,s,size=26,anchor='start',fill=INK2,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" {FONT} font-size="{size}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
   f'<rect width="{W}" height="{H}" fill="{SURF}"/>']
for v in [t for t in [0.05,0.1,0.2,0.5,1,2,5,10,20,50,100] if t<=YMAX]:
    p.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{GRID}"/>')
    p.append(txt(L-10,Y(v)+9,f'{v:g}s',anchor='end'))
for v in [5000,10000,15000,20000,25000,30000]:
    p.append(f'<line y1="{T}" y2="{H-B}" x1="{X(v):.1f}" x2="{X(v):.1f}" stroke="{GRID}"/>')
    p.append(txt(X(v),H-B+32,f'{v//1000}k',anchor='middle'))
p.append(txt((L+W-R)/2,H-16,'chain size (posts)',size=28,anchor='middle',fill=INK))
hdr=open(DATA).readline()
if 'ff_median' in hdr:   # r4 format: median / p90 / max
    series=[('sync max',10,'#999999','4 4',2),('sync P90',9,INK2,'6 3',3),('sync mean',7,'#999999','2 3',2,7000),('sync median',8,INK,'',3),('post median',3,INK2,'',3)]  # TODO: drop 'sync mean' at END
else:                    # r2 / chat format: mean / max
    series=[('sync max',2,'#999999','4 4',2),('sync mean',1,INK,'',3),('post mean',3,INK2,'',3)]
for name,col,color,dash,wd,*dy in series:
    pts=' '.join(f'{X(r[0]):.1f},{Y(r[col]):.1f}' for r in rows)
    d=f'stroke-dasharray="{dash}"' if dash else ''
    p.append(f'<polyline fill="none" stroke="{color}" stroke-width="{wd}" {d} points="{pts}"/>')
    for r in rows:
        p.append(f'<circle cx="{X(r[0]):.1f}" cy="{Y(r[col]):.1f}" r="3.5" fill="{color}" stroke="{SURF}" stroke-width="1.5"/>')
    last=rows[-1]
    lx,ly=(X(last[0])-12,Y(last[col])-14)
    if dy:   # label at a given x (middle of the plot), above the line
        r=min(rows,key=lambda r:abs(r[0]-dy[0])); lx,ly=X(r[0]),Y(r[col])-12
    p.append(txt(lx,ly,name,size=24,anchor='middle' if dy else 'end',fill=color if color!='#999999' else INK2))
p.append('</svg>'); print('\n'.join(p))

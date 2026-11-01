# Operation times vs chain size (grayscale SVG for the paper). Fonts for one column.
# Data: 16-col per-1k tsv (r4 format: n/mean/median/p90/max per op) or the old
# 4-col format (slice_end sync_mean sync_max post_mean). Empty cells are skipped.
# Usage: python3 ops.py [ops.tsv] [--all] > ops.svg; soffice --headless --convert-to pdf ops.svg
#   default (16 cols): linear axis, sync P90 / sync median / post median
#   --all   (16 cols): log axis, also sync max and sync mean
import math, sys
args=[a for a in sys.argv[1:] if not a.startswith('--')]
DATA=args[0] if args else 'ops.tsv'; ALL='--all' in sys.argv
W,H=900,520; L,R,T,B=110,30,30,80
INK='#000000'; INK2='#555555'; GRID='#dddddd'; SURF='#ffffff'
FONT='font-family="Helvetica, Arial, sans-serif"'
def num(v): return float(v) if v.strip() else None
lines=[l for l in open(DATA) if not l.startswith('#')]
hdr=lines[0] if 'slice_end' in lines[0] else open(DATA).readline()
rows=[list(map(num,l.rstrip('\n').split('\t'))) for l in lines if l[0].isdigit()]
NEW='ff_median' in hdr        # 16-col format
LIN=NEW and not ALL           # linear axis from 0
if NEW:
    series=[('sync P90',9,INK2,'6 3',3),('sync median',8,INK,'',3),('post median',3,INK2,'',3)]
    if ALL: series=[('sync max',10,'#999999','4 4',2),('sync mean',7,INK2,'2 3',2)]+series[1:]   # mean/max instead of P90
else:
    series=[('sync max',2,'#999999','4 4',2),('sync mean',1,INK,'',3),('post mean',3,INK2,'',3)]
vals=[r[c] for _,c,*_ in series for r in rows if r[c] is not None]
YMAX=0.6 if LIN else (20 if max(vals)<=20 else 100)
x0=0; x1=5000*math.ceil(rows[-1][0]/5000); y0,y1=math.log10(0.05),math.log10(YMAX)
def X(v): return L+(v-x0)/(x1-x0)*(W-L-R)
def Y(v): return H-B-(v/YMAX if LIN else (math.log10(v)-y0)/(y1-y0))*(H-T-B)
def txt(x,y,s,size=26,anchor='start',fill=INK2,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" {FONT} font-size="{size}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
   f'<rect width="{W}" height="{H}" fill="{SURF}"/>']
for v in ([0,0.1,0.2,0.3,0.4,0.5,0.6] if LIN else [t for t in [0.05,0.1,0.2,0.5,1,2,5,10,20,50,100] if t<=YMAX]):
    p.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{GRID}"/>')
    p.append(txt(L-10,Y(v)+9,f'{v:g}s',anchor='end'))
step=5000 if x1<=40000 else 25000
for v in range(step,int(rows[-1][0]*1.01)+1,step):   # ticks up to the last point
    p.append(f'<line y1="{T}" y2="{H-B}" x1="{X(v):.1f}" x2="{X(v):.1f}" stroke="{GRID}"/>')
    p.append(txt(X(v),H-B+32,f'{v//1000}k',anchor='middle'))
p.append(txt((L+W-R)/2,H-16,'chain size (posts)',size=28,anchor='middle',fill=INK))
LABEL={'sync P90':(None,32)}   # name -> (x or None=line end, dy); default above the end
if ALL: LABEL={'sync mean':(x1*0.45,-14),'post median':(None,32)}   # mean ~ median: mean mid-plot
for name,col,color,dash,wd in series:
    pts=[r for r in rows if r[col] is not None]
    d=f'stroke-dasharray="{dash}"' if dash else ''
    p.append(f'<polyline fill="none" stroke="{color}" stroke-width="{wd}" {d} points="{" ".join(f"{X(r[0]):.1f},{Y(r[col]):.1f}" for r in pts)}"/>')
    for r in pts:
        p.append(f'<circle cx="{X(r[0]):.1f}" cy="{Y(r[col]):.1f}" r="3.5" fill="{color}" stroke="{SURF}" stroke-width="1.5"/>')
    lx,dy=LABEL.get(name,(None,-14)); fill=color if color!='#999999' else INK2
    if lx:   # mid-plot label
        m=min(pts,key=lambda r:abs(r[0]-lx)); p.append(txt(X(m[0]),Y(m[col])+dy,name,size=24,anchor='middle',fill=fill))
    else:    # at the line end
        last=pts[-1]; p.append(txt(X(last[0])-12,Y(last[col])+dy,name,size=24,anchor='end',fill=fill))
p.append('</svg>'); print('\n'.join(p))

# Usenet storage vs chain size (grayscale SVG for the paper).
# Data: stor.tsv (cumulative disk MB per 1k posts). Fonts sized for one column.
# Usage: python3 stor.py [stor.tsv] > stor.svg; soffice --headless --convert-to pdf stor.svg
import sys
DATA=sys.argv[1] if len(sys.argv)>1 else 'stor.tsv'
W,H=900,640; L,R,T,B=110,30,30,80
S=130; G=40   # overhead strip height and gap above it
INK='#000000'; INK2='#555555'; GRID='#dddddd'; SURF='#ffffff'
FONT='font-family="Helvetica, Arial, sans-serif"'
rows=[list(map(float,l.split())) for l in open(DATA) if not l.startswith('#')]
# the index residual (last row only) is prorated to slices by snapshot share
res=rows[-1][4]; tot=rows[-1][3]
for r in rows:
    share=res*r[3]/tot; r[3]+=share; r[5]+=share-r[4]; r[4]=0
YMAX=50*(int(max(r[5] for r in rows)/50)+1)
x0,x1=0,35000
def X(v): return L+(v-x0)/(x1-x0)*(W-L-R)
HM=H-B-S-G   # bottom of the main plot
def Y(v): return HM-v/YMAX*(HM-T)
R0,R1=1,5    # overhead range (x)
def YR(v): return H-B-(v-R0)/(R1-R0)*S
def txt(x,y,s,size=26,anchor='start',fill=INK2,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" {FONT} font-size="{size}" text-anchor="{anchor}" fill="{fill}" {extra}>{s}</text>'
p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
   f'<rect width="{W}" height="{H}" fill="{SURF}"/>']
for v in range(0,YMAX+1,50):
    p.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{GRID}"/>')
    p.append(txt(L-10,Y(v)+9,f'{v}MB',anchor='end'))
for v in [5000,10000,15000,20000,25000,30000]:
    p.append(f'<line y1="{T}" y2="{HM}" x1="{X(v):.1f}" x2="{X(v):.1f}" stroke="{GRID}"/>')
    p.append(f'<line y1="{H-B-S}" y2="{H-B}" x1="{X(v):.1f}" x2="{X(v):.1f}" stroke="{GRID}"/>')
    p.append(txt(X(v),H-B+32,f'{v//1000}k',anchor='middle'))
p.append(txt((L+W-R)/2,H-16,'chain size (posts)',size=28,anchor='middle',fill=INK))
series=[('total',5,INK,'',3),('snapshots',3,INK2,'6 3',3),('payloads',1,INK2,'',3),('commits',2,'#999999','4 4',2)]
for name,col,color,dash,wd in series:
    pts=' '.join(f'{X(r[0]):.1f},{Y(r[col]):.1f}' for r in rows)
    d=f'stroke-dasharray="{dash}"' if dash else ''
    p.append(f'<polyline fill="none" stroke="{color}" stroke-width="{wd}" {d} points="{pts}"/>')
    for r in rows:
        p.append(f'<circle cx="{X(r[0]):.1f}" cy="{Y(r[col]):.1f}" r="3.5" fill="{color}" stroke="{SURF}" stroke-width="1.5"/>')
    last=rows[-1]
    p.append(txt(X(last[0])+10,Y(last[col])+9,name,size=24,anchor='start',fill=color if color!='#999999' else INK2))
# overhead strip: total / payloads, cumulative
for v in range(R0,R1+1):
    p.append(f'<line x1="{L}" x2="{W-R}" y1="{YR(v):.1f}" y2="{YR(v):.1f}" stroke="{GRID}"/>')
    p.append(txt(L-10,YR(v)+9,f'{v}&#215;',anchor='end'))
R0,R1=1,5
for name,f,color,dash in [('with snapshots',lambda r:r[5]/r[1],INK,''),('without',lambda r:(r[1]+r[2])/r[1],INK2,'6 3')]:
    pts=' '.join(f'{X(r[0]):.1f},{YR(f(r)):.1f}' for r in rows)
    d=f'stroke-dasharray="{dash}"' if dash else ''
    p.append(f'<polyline fill="none" stroke="{color}" stroke-width="3" {d} points="{pts}"/>')
    for r in rows:
        p.append(f'<circle cx="{X(r[0]):.1f}" cy="{YR(f(r)):.1f}" r="3.5" fill="{color}" stroke="{SURF}" stroke-width="1.5"/>')
    last=rows[-1]
    p.append(txt(X(last[0])+10,YR(f(last))+9,name,size=24,anchor='start',fill=color))
p.append(txt(L+8,H-B-S+26,'overhead over payloads',size=22,fill=INK2))
p.append('</svg>'); print('\n'.join(p))

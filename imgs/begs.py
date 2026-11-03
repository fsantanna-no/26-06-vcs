# Usenet begs per returning author (admission beg + extra begs), like 500 (rule 4.a min).
# Data: begs.tsv (like, begs, authors), r4 final S1, from 2606-sims p2p/ev/begs.py.
# Returning authors only; the first beg (x=1) is the welcome.
# Usage: python3 begs.py > begs.svg; soffice --headless --convert-to pdf begs.svg
import math
W,H=900,560; L,R,T,B=130,30,70,80
INK='#000000'; INK2='#555555'; GRID='#dddddd'; SURF='#ffffff'
FONT='font-family="Helvetica, Arial, sans-serif"'
def txt(x,y,s,size=26,anchor='start',fill=INK2):
    return f'<text x="{x:.1f}" y="{y:.1f}" {FONT} font-size="{size}" text-anchor="{anchor}" fill="{fill}">{s}</text>'
rows=[l.split() for l in open('begs.tsv') if l[0].isdigit() and l.split()[0]=='500']
LIKES=sorted({int(r[0]) for r in rows}); N=max(int(r[1]) for r in rows)+1
cnt={(int(r[0]),int(r[1])):int(r[2]) for r in rows}
tot={w:sum(n for (x,b),n in cnt.items() if x==w) for w in LIKES}
pct={k:100*n/tot[k[0]] for k,n in cnt.items()}
Y0,Y1=-2,2   # log10 of 0.01% .. 100%
def Y(v): return H-B-(math.log10(v)-Y0)/(Y1-Y0)*(H-T-B)
p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',f'<rect width="{W}" height="{H}" fill="{SURF}"/>']
for e,lab in zip(range(Y0,Y1+1),['0.01%','0.1%','1%','10%','100%']):
    p.append(f'<line x1="{L}" x2="{W-R}" y1="{Y(10**e):.1f}" y2="{Y(10**e):.1f}" stroke="{GRID}"/>'); p.append(txt(L-10,Y(10**e)+9,lab,anchor='end'))
FILL={500:INK}; CW=(W-L-R)/N; BW=CW*0.4
for b in range(N):
    cx=L+CW*(b+0.5); p.append(txt(cx,H-B+32,str(b+1),anchor='middle'))   # +1: the admission beg
    for i,w in enumerate(LIKES):
        v=pct.get((w,b),0); x=cx+(i-len(LIKES)/2)*BW
        if v<=0: p.append(txt(x+BW/2,Y(10**Y0)-8,'0',size=22,anchor='middle')); continue
        p.append(f'<rect x="{x:.1f}" y="{Y(v):.1f}" width="{BW:.1f}" height="{Y(10**Y0)-Y(v):.1f}" fill="{FILL[w]}"/>')
        lab=f'{cnt[(w,b)]:,} ('+(f'{v:.1f}%' if v>=1 else f'{v:.2f}%')+')'
        p.append(txt(x+BW/2,Y(v)-8,lab,size=20,anchor='middle',fill=INK))
p.append(txt((L+W-R)/2,H-16,'begs per author',size=28,anchor='middle',fill=INK))
p.append(txt(L-110,30,'authors (log)',size=24,fill=INK))
p.append('</svg>'); print('\n'.join(p))

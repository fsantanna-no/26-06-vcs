import gzip
objs=[]; nid=[0]
def oid():
    nid[0]+=1; return "O%d"%nid[0]
def box(x,y,w,h):
    i=oid(); objs.append(f'''
    <dia:object type="Standard - Box" version="0" id="{i}">
      <dia:attribute name="obj_pos"><dia:point val="{x},{y}"/></dia:attribute>
      <dia:attribute name="obj_bb"><dia:rectangle val="{x-.05},{y-.05};{x+w+.05},{y+h+.05}"/></dia:attribute>
      <dia:attribute name="elem_corner"><dia:point val="{x},{y}"/></dia:attribute>
      <dia:attribute name="elem_width"><dia:real val="{w}"/></dia:attribute>
      <dia:attribute name="elem_height"><dia:real val="{h}"/></dia:attribute>
      <dia:attribute name="show_background"><dia:boolean val="false"/></dia:attribute>
      <dia:attribute name="line_style"><dia:enum val="1"/></dia:attribute>
      <dia:attribute name="dashlength"><dia:real val="0.5"/></dia:attribute>
    </dia:object>'''); return i
def ell(x,y,d=2.0):
    i=oid(); objs.append(f'''
    <dia:object type="Standard - Ellipse" version="0" id="{i}">
      <dia:attribute name="obj_pos"><dia:point val="{x},{y}"/></dia:attribute>
      <dia:attribute name="obj_bb"><dia:rectangle val="{x-.05},{y-.05};{x+d+.05},{y+d+.05}"/></dia:attribute>
      <dia:attribute name="elem_corner"><dia:point val="{x},{y}"/></dia:attribute>
      <dia:attribute name="elem_width"><dia:real val="{d}"/></dia:attribute>
      <dia:attribute name="elem_height"><dia:real val="{d}"/></dia:attribute>
    </dia:object>'''); return i
def line(x1,y1,x2,y2,style=4,arrow=22,sarrow=0,width=0.1):
    i=oid()
    ea = f'<dia:attribute name="end_arrow"><dia:enum val="{arrow}"/></dia:attribute><dia:attribute name="end_arrow_length"><dia:real val="0.6"/></dia:attribute><dia:attribute name="end_arrow_width"><dia:real val="0.6"/></dia:attribute>' if arrow else ''
    sa = f'<dia:attribute name="start_arrow"><dia:enum val="{sarrow}"/></dia:attribute><dia:attribute name="start_arrow_length"><dia:real val="0.5"/></dia:attribute><dia:attribute name="start_arrow_width"><dia:real val="0.5"/></dia:attribute>' if sarrow else ''
    objs.append(f'''
    <dia:object type="Standard - Line" version="0" id="{i}">
      <dia:attribute name="obj_pos"><dia:point val="{x1},{y1}"/></dia:attribute>
      <dia:attribute name="obj_bb"><dia:rectangle val="{min(x1,x2)-.5},{min(y1,y2)-.5};{max(x1,x2)+.5},{max(y1,y2)+.5}"/></dia:attribute>
      <dia:attribute name="conn_endpoints"><dia:point val="{x1},{y1}"/><dia:point val="{x2},{y2}"/></dia:attribute>
      <dia:attribute name="numcp"><dia:int val="1"/></dia:attribute>
      <dia:attribute name="line_width"><dia:real val="{width}"/></dia:attribute>
      <dia:attribute name="line_style"><dia:enum val="{style}"/></dia:attribute>
      {ea}{sa}
    </dia:object>'''); return i
def text(x,y,s,h=0.9,align=0):
    i=oid(); s=s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"); objs.append(f'''
    <dia:object type="Standard - Text" version="1" id="{i}">
      <dia:attribute name="obj_pos"><dia:point val="{x},{y}"/></dia:attribute>
      <dia:attribute name="obj_bb"><dia:rectangle val="{x-.05},{y-.05};{x+len(s)*h*0.55},{y+h}"/></dia:attribute>
      <dia:attribute name="text"><dia:composite type="text">
        <dia:attribute name="string"><dia:string>#{s}#</dia:string></dia:attribute>
        <dia:attribute name="font"><dia:font family="sans" style="0" name="Helvetica"/></dia:attribute>
        <dia:attribute name="height"><dia:real val="{h}"/></dia:attribute>
        <dia:attribute name="pos"><dia:point val="{x},{y+h*0.8}"/></dia:attribute>
        <dia:attribute name="color"><dia:color val="#000000ff"/></dia:attribute>
        <dia:attribute name="alignment"><dia:enum val="{align}"/></dia:attribute>
      </dia:composite></dia:attribute>
      <dia:attribute name="valign"><dia:enum val="0"/></dia:attribute>
    </dia:object>'''); return i

D=2.0; X0=2; DX=4.5
def node(col,y,label,tlab=None,dlab=None):
    x=X0+col*DX; ell(x,y,D)
    text(x+0.55,y+0.5,label,0.9)
    if tlab: text(x+0.1,y-1.1,tlab,0.8)
    if dlab: text(x+0.1,y+D+0.2,dlab,0.8)
    return x
def edge(c1,c2,y,style=4):
    # from col c1 (child) to col c2 (parent), arrow at parent
    x1=X0+c1*DX; x2=X0+c2*DX+D; line(x1,y+D/2,x2,y+D/2,style,22)

# ---------- (A) ----------
yA=3.5
text(0.5,0.3,"(A) local order with consensus time t (days); now t=10, window 7 days",0.9)
for c,(l,t) in enumerate([("gen","t=0"),("a","t=1"),("b","t=2"),("c","t=8"),("d","t=9"),("e","t=10")]):
    node(c,yA,l,t)
for c in range(1,6): edge(c,c-1,yA, 0 if c==3 else 4)
box(X0-0.8, yA-1.7, 3*DX-0.9, 6.0); text(X0-0.5, yA+D+1.0, "frozen (t <= 3)", 0.9)
box(X0+3*DX-0.8, yA-1.7, 3*DX-0.9, 6.0); text(X0+3*DX-0.5, yA+D+1.0, "loose (t > 3)", 0.9)

# ---------- (B) ----------
yB=12.4
text(0.5,8.6,"(B) losing branch forking at c (t=8): age = 10 - 8 = 2 < 7, accepted",0.9)
text(0.5,9.6,"    appended after the tip: declared d=2..5 ignored, consensus t=10, loose",0.9)
for c,(l,t,d) in enumerate([("c","t=8",None),("d","t=9",None),("e","t=10",None),("x","t=10","d=2"),("y","t=10","d=5")]):
    node(c+1,yB,l,t,d)
for c in range(2,6): edge(c,c-1,yB, 0 if c==4 else 4)
box(X0+4*DX-0.8, yB-1.7, 2*DX-0.9, 6.6); text(X0+4*DX-0.5, yB+D+1.9, "loose, refutable", 0.9)

# ---------- (C) ----------
yC=21.2
text(0.5,17.6,"(C) winning branch forking at a (t=1): age = 10 - 1 = 9 >= 7, rejected",0.9)
text(0.5,18.6,"    it would reorder frozen b..e: hard fork",0.9)
for c,(l,t) in enumerate([("gen","t=0"),("a","t=1"),("b","t=2")]):
    node(c,yC,l,t)
for c in range(1,3): edge(c,c-1,yC)
text(X0+3*DX-1.0, yC+0.5, "... c, d, e", 0.9)
# branch p<-q below a
yP=yC+3.6
xp=node(2,yP,"p"); xq=node(3,yP,"q")
edge(3,2,yP)
xa=X0+1*DX
line(xp, yP+D/2, xa+D, yC+D/2+0.6, 4, 22)   # p -> a
text(X0+4*DX+0.3, yP+0.5, "rejected", 0.9)

hdr='''<?xml version="1.0" encoding="UTF-8"?>
<dia:diagram xmlns:dia="http://www.lysator.liu.se/~alla/dia/">
  <dia:diagramdata>
    <dia:attribute name="background"><dia:color val="#ffffffff"/></dia:attribute>
    <dia:attribute name="paper"><dia:composite type="paper">
      <dia:attribute name="name"><dia:string>#A4#</dia:string></dia:attribute>
      <dia:attribute name="is_portrait"><dia:boolean val="false"/></dia:attribute>
      <dia:attribute name="scaling"><dia:real val="1"/></dia:attribute>
      <dia:attribute name="fitto"><dia:boolean val="false"/></dia:attribute>
    </dia:composite></dia:attribute>
  </dia:diagramdata>
  <dia:layer name="Background" visible="true" connectable="true" active="true">'''
ftr='''
  </dia:layer>
</dia:diagram>
'''
with gzip.open("ctime.dia","wb") as f: f.write((hdr+"".join(objs)+ftr).encode())
print("ok", len(objs))

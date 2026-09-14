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


D=2.0
def node(x,y,label,sub=None,cross=False,subdx=-0.3,bold=False):
    if cross:
        line(x-0.3,y-0.3,x+D+0.3,y+D+0.3,0,0,0,0.15)
        line(x-0.3,y+D+0.3,x+D+0.3,y-0.3,0,0,0,0.15)
    ell(x,y,D)
    if bold: ell(x-0.15,y-0.15,D+0.3)
    text(x+0.55,y+0.5,label,0.9)
    if sub: text(x+subdx,y+D+0.15,sub,0.75)
    return x
def edge(x1,y1,x2,y2,style=4):
    line(x1,y1,x2,y2,style,22)

AX=8.6
X0=3.0; U=3.0
def hx(h): return X0+(h-7)*U
line(hx(7),AX,hx(17.6),AX,0,22)
for h in range(7,18):
    line(hx(h),AX-0.15,hx(h),AX+0.15,0,0)
    text(hx(h)-0.3,AX+0.3,str(h),0.7)
text(hx(17.6)+0.3,AX-0.35,"declared (h)",0.75)
# walls: tip chain time = 12, local clock = 15
LO=hx(11); HI=hx(16)
line(LO,1.0,LO,AX,1,0,0,0.1); line(HI,1.0,HI,AX,1,0,0,0.1)
line(LO,1.4,HI,1.4,4,7,7)
text((LO+HI)/2-2.6,0.4,"admission window",0.85)
text(LO-2.0,AX+1.1,"tip - 1h",0.75)
text(HI-1.6,AX+1.1,"clock + 1h",0.75)
line(hx(15),AX-0.5,hx(15),AX+0.5,0,0,0,0.25); text(hx(15)-1.6,AX+1.9,"local clock",0.75)
# chain: ... <- a <- tip
NY=3.8
a=node(hx(10)-D/2,NY,"a","c=10")
tip=node(hx(12)-D/2,NY,"tip","c=12",bold=True,subdx=-0.2)
text(hx(8.4)-1.2,NY+0.5,"...",0.9)
edge(a,NY+D/2,hx(8.4)+0.3,NY+D/2)
edge(tip,NY+D/2,a+D,NY+D/2)
# candidates, all pointing to the tip
x=node(hx(14)-D/2,NY,"x","accepted",subdx=-0.9)
z=node(hx(9.4)-D/2,NY-2.6,"z","too old",True,subdx=-2.6)
y=node(hx(17)-D/2,NY,"y","too new",True,subdx=-0.6)
edge(x,NY+D/2,tip+D+0.15,NY+D/2)
edge(z+D-0.1,NY-2.6+D-0.2,tip+0.4,NY-0.1)
edge(y+0.3,NY-0.1,tip+D-0.2,NY-0.1)
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
with gzip.open("times.dia","wb") as f: f.write((hdr+"".join(objs)+ftr).encode())
print("ok", len(objs))

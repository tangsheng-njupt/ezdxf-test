import ezdxf
# 创建一个新的DXF文档
doc = ezdxf.new('R2010')
# 定义绘制区域
msp = doc.modelspace()
# 步骤2：用默认线型Bylayer绘制长12000，宽9000的矩形，长平行于X轴，宽平行于Y轴
rect = msp.add_lwpolyline([(0, 0), (0, 9000), (12000, 9000), (12000, 0), (0, 0)])
# 步骤3：先加载新的线型，选用CENTER，绘制一条点划线，经过长的两个中点，超出矩形的边框两边各500，将矩形分为两半
if 'CENTER' not in doc.linetypes:
    doc.linetypes.new(name='CENTER', dxfattribs={
        'description': 'Center line',
        'pattern': 'A,.5,-.2,0,-.2'
    })
# 绘制一条点划线，经过长的两个中点，超出矩形的边框两边各500，将矩形分为两半
start_point = (6000, -500)
end_point = (6000, 9500)
msp.add_line(start_point, end_point, dxfattribs={'linetype': 'CENTER'})
# 步骤4：用图案填充命令填充被点划线分割后左侧的矩形
hatch = msp.add_hatch(color=5)
hatch.set_pattern_fill('AR-B816', scale=5)
hatch.paths.add_polyline_path([(0, 0), (0, 4500), (12000, 4500), (12000, 0)])
# 保存DXF文件
doc.saveas('modified.dxf')
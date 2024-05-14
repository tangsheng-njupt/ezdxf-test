import ezdxf

# 创建一个新的DXF文档
doc = ezdxf.new('R2010', setup=True)
msp = doc.modelspace()

# 添加矩形
msp.add_lwpolyline([(0, 0), (12000, 0), (12000, 9000), (0, 9000), (0, 0)], close=True)

# 添加分割线
msp.add_line((6000, 0), (6000, 9000), dxfattribs={'linetype': 'DASHED'})

# 添加填充的左侧部分
hatch = msp.add_hatch(color=8)
hatch.set_pattern_fill('AR-B816', scale=1.0)
hatch.paths.add_polyline_path([(0, 0), (6000, 0), (6000, 9000), (0, 9000), (0, 0)], is_closed=True)

# 保存DXF文件
doc.saveas('filled_rectangle.dxf')

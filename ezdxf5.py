import ezdxf

# 创建新的DXF文档
doc = ezdxf.new('R2010')
msp = doc.modelspace()

# 步骤2的点
points_step2 = [(0, 0), (6000, 0), (6000, 9000), (0, 9000)]

# 步骤3的点
points_step3 = [(0, -380), (5200, -380), (5500, -580), (6500, -580), (6500, -680), (5500, -680), (5200, -480), (0, -480)]

# 步骤4的点
points_step4 = [(0, 0), (6400, 0), (6400, -580)]

# 添加步骤2、3、4的线型
msp.add_lwpolyline(points_step2, close=True)
msp.add_lwpolyline(points_step3, close=True)
msp.add_lwpolyline(points_step4, close=False)

# 对称变换并添加对称图形
symmetric_points_step2 = [(-x, y) for x, y in points_step2]
symmetric_points_step3 = [(-x, y) for x, y in points_step3]
symmetric_points_step4 = [(-x, y) for x, y in points_step4]

msp.add_lwpolyline(symmetric_points_step2, close=True)
msp.add_lwpolyline(symmetric_points_step3, close=True)
msp.add_lwpolyline(symmetric_points_step4, close=False)

# 步骤7: 使用"HATCH"实体填充步骤2的对称图形
hatch = msp.add_hatch(color=5)
hatch.set_pattern_fill('AR-B816', scale=5)
hatch.paths.add_polyline_path(symmetric_points_step2, is_closed=True)

# 保存DXF文件
doc.saveas('output.dxf')
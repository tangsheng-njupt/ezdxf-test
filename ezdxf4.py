import ezdxf
from ezdxf.layouts import Modelspace
# 创建一个新的DXF图纸
doc = ezdxf.new()
# 获取modelspace，这是我们将添加线，形状和其他实体的地方
msp = doc.modelspace()
# 步骤2
points1 = [(0,0), (6000,0), (6000,9000), (0,9000)]
msp.add_lwpolyline(points1)
# 步骤3
points2 = [(0,-380), (5200,-380), (5500,-580), (6500,-580), (6500,-680), (5500,-680), (5200,-480), (0,-480)]
msp.add_lwpolyline(points2)
# 步骤4
points3 = [(0,0), (6400,0), (6400,-580)]
msp.add_lwpolyline(points3)
# 步骤5
msp.add_line((0, -800), (0, 9800))
# 步骤6, 首先定义一个矩阵来进行反射变换
mat = ezdxf.math.Matrix44.scale(sx=-1)
for entity in msp:
    entity.transform(mat)
# 步骤7
hatch = msp.add_hatch(color=5)
hatch.set_pattern_fill('AR-B816', scale=5)
doc.saveas('your_drawing.dxf')
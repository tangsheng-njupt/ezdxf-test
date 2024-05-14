# EZDXF包测试

### 一、安装ezdxf库

在Anaconda Prompt中输入

```
pip install ezdxf
```

安装ezdxf库。

### 二、代码测试

1.导入ezdxf库，使用下列代码创建一个矩形，使用分割线分成两部分，一部分使用特定纹理。

```
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
```

使用AutoCAD打开代码生成的dxf文件，如图所示。

![](image/image1.png)

2.利用自定义线性分割图像，图中点划线收到覆盖未能显示。

```
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
```

![](image/image2.png)

3.使用创建的点划线将矩形分隔为上下两部分。

```
import ezdxf

# 创建一个新的DXF文档
doc = ezdxf.new('R2010')

# 定义绘制区域
msp = doc.modelspace()

# 步骤2：用默认线型Bylayer绘制长12000，宽9000的矩形，长平行于X轴，宽平行于Y轴
rect = msp.add_lwpolyline([(0, 0), (12000, 0), (12000, 9000), (0, 9000), (0, 0)])

# 步骤3：先加载新的线型，选用CENTER，缩放比例因子设为10，绘制一条点划线，经过长的两个中点，超出矩形的边框两边各500，将矩形分为两半
if 'CENTER' not in doc.linetypes:
    doc.linetypes.new(name='CENTER', dxfattribs={
        'description': 'Center line',
        'pattern': 'A,.5,-.2,0,-.2'
    })

start_point = (-500, 4500)
end_point = (12500, 4500)
msp.add_line(start_point, end_point, dxfattribs={'linetype': 'CENTER', 'ltscale': 10})

# 步骤4：用图案填充命令填充被点划线分割后左侧的矩形
hatch = msp.add_hatch(color=5)
hatch.set_pattern_fill('AR-B816', scale=5)
hatch.paths.add_polyline_path([(0, 0), (6000, 0), (6000, 9000), (0, 9000), (0, 0)])

# 保存DXF文件
doc.saveas('modifie.dxf')
```

![](image/image3.png)

4.通过端点定义多边形，再通过定义一个缩放矩阵来反转坐标系。

```
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
```

![](image/image4.png)

5.将上述步骤进行融合，通过对称变换生成需要的图像并加以填充。

```
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
```

![](image/image5.png)
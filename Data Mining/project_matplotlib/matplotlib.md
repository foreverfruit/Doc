[TOC]

---

# Matplotlib初步应用



## 环境搭建

采用anaconda，自带各种科学计算的库，省去自己安装，版本适配的麻烦

---

## Numpy

Numpy是一种开源的扩展的数值计算库。

- ndarray，numpy的array对象。三种方法获得该对象：
  - nd_a = np.array(py_a) # python的数组a通过numpy.array方法转变为ndarray类型的数组
  - nd_b = np.arange(10) # arange函数生成ndarray对象
  - 读取数据库或文件：nd_c = np.loadtxt(parameters)，注意参数的作用。
- 索引和切片
  - ndarray和array一样，从0元素开始索引
  - 用name[start :end :step]方式切片
- numpy常用函数
  - min、max、median、mean（平均值）、var（方差）、sort

  - 函数的调用支持面向过程和面向对象两种方式，np.sort(ndarrayObj)和ndarrayObj.sort()效果一样，这里注意一个区别。

  - np.sort(ndarray)不会改变ndarray原数组对象，返回一个新的已排序的对象，而ndarray.sort()不会产生新对象，而是将自身排序。

  - random随机数生成、linspace(start,end,amount)生成等区间的离散列。

  - random.randn(count)生成count个均值为0方差为1的数组

  - 数据的导入：converters参数的使用。

    ```python
    # 这里将第0列日期数据的str型数据转换成float，且日期数据格式为‘12/01/1995’（1995-12-01）
    # 需要导入包
    import matplotlib.datas as matdata
    date,otherdata = np.loadtxt(..,converters={0:matdata.strpdata2num('%m/%d/%y')},..)
    # 显示的时候如果需要这个日期数据，用相应的画图函数
    plt.plot_date(date,otherdata)
    # 这个函数会识别float形式的日期数据
    ```

    ​

    ​

练习一：numpy生成100以内随机数组，存储数组到文件，读取文件，数组排序、求最大值、最小值、均值、方差

```python
import  numpy as np
# 产生100个元素的ndarray，[0,1000)之间
nd_a = np.random.randint(0,1000,100)

# 保存为文件，参数看文档
np.savetxt('arraydata.txt',nd_a,delimiter=',',header='my random data',footer='over',fmt='%d')

# 读取文件
nd_b = np.loadtxt('arraydata.txt',dtype=int,delimiter=',',skiprows=1,unpack=False,)

# 对比原数组和读取的数组元素个数是否一致
print('loaded-' + str(nd_b.size) + ',original-'+str(nd_a.__len__()))

# 排序
nd_c = np.sort(nd_b)

# 输出排序后的结果：排序产生的新数组和原数组
print(nd_c)
print(nd_b)

# 输出max
print('max:loaded-'+ str(np.max(nd_b)) + ',original-' + str(nd_a.max()))
# 输出min
print('min:loaded-'+ str(np.min(nd_b)) + ',original-' + str(nd_a.min()))
# 输出mean
print('mean:loaded-'+ str(np.mean(nd_b)) + ',original-' + str(nd_a.mean()))
#输出方差var
print('avriance:loaded-'+ str(np.var(nd_b)) + ',original-' + str(nd_a.var()))
```

练习二：Iris数据集的简单练习

```python
import  numpy as np
# 这里的路径是因为本py文件和数据文件不在一个目录下
import  os
pro_root = os.path.abspath('..')
sepal_length,sepal_width,petal_length,petal_width = np.loadtxt(pro_root+'\\dataset\\iris.data',
                  delimiter=',',
                  unpack=True,dtype=float,usecols=(0,1,2,3))

# 三种花的统计值，简单的统计
print(sepal_length[:50].mean())
print(sepal_length[:50].var())

print(sepal_length[51:100].mean())
print(sepal_length[51:100].var())

print(sepal_length[101:150].mean())
print(sepal_length[101:150].var())
```



---
## 散点图

scatter(xList,yList)函数

外观参数：用以区分不同类型数据。颜色-c，点大小-s，透明度-alpha，点形状-marker

```python
# 查看花的sepal的length和width的关系
import  numpy as np
import  matplotlib.pyplot as plt
import  os
pro_root = os.path.abspath('..')

sepal_length,sepal_width = np.loadtxt(pro_root+'\\dataset\\iris.data',
                  delimiter=',',
                  unpack=True,dtype=float,usecols=(0,1))

plt.scatter(sepal_width[:50],sepal_length[:50],marker='*',c='red',alpha=0.5,s=50)
plt.scatter(sepal_width[51:100],sepal_length[51:100],marker=',',c='green',alpha=0.5,s=50)
plt.scatter(sepal_width[101:150],sepal_length[101:150],marker='.',c='blue',alpha=0.5,s=50)
plt.show()

# 可以看到三种花的sepal的宽和长都是近似正相关的
```

---

## 折线图

plt.plot(xlist,ylist)、plt.plot_date(date,data,linestyle='.')(这个函数需要指定linestyle，否则画出的是点，而不是线)

练习一：[0,10]内的正弦图象

```python
# 0,10内正弦图象
import  numpy as np
import  matplotlib.pyplot as plt

# 只分成20份，能看到折线
xlist = np.linspace(0,10,20)
ylist = np.sin(xlist)
plt.plot(xlist,ylist,'b:')

# 分成100份，几乎是光滑曲线
alist = np.linspace(0,10,100)
blist = np.cos(alist)
plt.plot(alist,blist,'r--')

plt.show()

# plot函数的参数需要注意,'r--'这是一种组合的参数，r表示颜色red，--表示线的样式，具体的组合看文档
```

练习二：iris练习

```python
import  numpy as np
import  matplotlib.pyplot as plt
import  os
pro_root = os.path.abspath('..')
data = np.loadtxt(pro_root+'\\dataset\\iris.data',
                  delimiter=',',
                  unpack=False,dtype=float,usecols=(0,1,2,3))

for x in data[0:50]:
    plt.plot(x,'r--')
for x in data[51:100]:
    plt.plot(x,'g-')
for x in data[100:150]:
    plt.plot(x,'b-.')

# 对图做个加工
# x、y轴标签与图形标题
plt.xlabel('category')
plt.ylabel('value')
plt.title('iris\'s sepal and petal leagth and width')

# X轴上的标签
xticks=['sepal length','sepal width','petal length','petal width']
#设置x轴的刻度，将构建的xticks代入
plt.xticks(range(len(xticks)),xticks,rotation=0)

# 图中可以看出三种类型的折线图
plt.show()

```

---

## 条形图

np.bar(parameters)

练习：iris的两种条形图

```python
"""
累计条形图，stacked bar graph
"""
import numpy as np
import matplotlib.pyplot as plt
from src.utils import utils as tool

sepal_length,sepal_width,petal_length,petal_width = np.loadtxt(tool.getPath()+'/dataset/iris.data',
                  delimiter=',',
                  unpack=True,dtype=float,usecols=(0,1,2,3))

# data
sun_sepal_length = [np.sum(sepal_length[0:50]),np.sum(sepal_length[51:100]),np.sum(sepal_length[101:150])]
sun_sepal_width = [np.sum(sepal_width[0:50]),np.sum(sepal_width[51:100]),np.sum(sepal_width[101:150])]
sun_petal_length = [np.sum(petal_length[0:50]),np.sum(petal_length[51:100]),np.sum(petal_length[101:150])]
sun_petal_width = [np.sum(petal_width[0:50]),np.sum(petal_width[51:100]),np.sum(petal_width[101:150])]


# plot
left = np.arange(3)
width = 0.5
# 这里有大量重复的矩阵计算，需要优化
bar1 = plt.bar(left,sun_sepal_length,width,yerr=sun_sepal_length,align='center',color='red')
bar2 = plt.bar(left,sun_sepal_width,width,yerr=sun_sepal_width,bottom=sun_sepal_length,align='center',color='green')
bar3 = plt.bar(left,sun_petal_length,width,yerr=sun_petal_length,bottom=np.add(sun_sepal_length,sun_sepal_width),align='center',color='blue')
bar4 = plt.bar(left,sun_petal_width,width,yerr=sun_petal_width,bottom=np.add(np.add(sun_sepal_length,sun_sepal_width),sun_petal_length),align='center',color='black')
# 坐标轴美化
plt.ylabel('value')
plt.title('this is title')
plt.xticks(left,('typeA','typeB','typeC'))
# 图例标注
plt.legend((bar1[0], bar2[0],bar3[0],bar4[0]), ('sepal_length', 'sepal_width','petal_length','petal_width'))
plt.show()
```

```python
"""
并列对比条形图
"""
import numpy as np
import matplotlib.pyplot as plt
from src.utils import utils as tool

sepal_length,sepal_width,petal_length,petal_width = np.loadtxt(tool.getPath()+'/dataset/iris.data',
                  delimiter=',',
                  unpack=True,dtype=float,usecols=(0,1,2,3))

# data
sun_sepal_length = [np.sum(sepal_length[0:50]),np.sum(sepal_length[51:100]),np.sum(sepal_length[101:150])]
sun_sepal_width = [np.sum(sepal_width[0:50]),np.sum(sepal_width[51:100]),np.sum(sepal_width[101:150])]
sun_petal_length = [np.sum(petal_length[0:50]),np.sum(petal_length[51:100]),np.sum(petal_length[101:150])]
sun_petal_width = [np.sum(petal_width[0:50]),np.sum(petal_width[51:100]),np.sum(petal_width[101:150])]

x = np.arange(0,15,5)
width = 0.5

bar1 = plt.bar(x,sun_sepal_length,width,color='red')
bar2 = plt.bar(x+width+0.1,sun_sepal_width,width,color='green')
bar3 = plt.bar(x+width*2+0.2,sun_petal_length,width,color='blue')
bar4 = plt.bar(x+width*3+0.3,sun_petal_width,width,color='black')

plt.xticks(x+width*2,('A','B','C'))
plt.legend((bar1[0],bar2[0],bar3[0],bar4[0]),('sepal_length','sepal_width','petal_length','petal_width'),loc=2)

plt.show()
```

---

## 直方图

类似于条形图，但是通常是展示连续数据。

plt.hist(data,bins,color,normed)，bins表示的直方图的分段数量，normed决定y轴是频率还是计数

```python
# 随机生成数据做直方图
import numpy as np
import matplotlib.pyplot as plt

mean = 20
var = 0.5
data = mean+var*np.random.randn(100000)

# plt.hist(data,bins=50,normed=False,color='red')
# 当直方图的划分很大时，就是密度曲线
plt.hist(data,bins=500,normed=True,color='red')
plt.show()
```

```python
# 二维的直方图，用颜色表示联合密度
import numpy as np
import matplotlib.pyplot as plt

# xy均值分别为1和5，方差都为1
x = 1+np.random.randn(2000)
y = 5+np.random.randn(2000)

plt.hist2d(x,y,bins=40)
# 图通过颜色深浅表示概率，显然在(x,y)=(1,5)处密度最大，颜色最亮
plt.show()
```

---

## 饼状图

plt.pie(dataArray,labels,autopct='%d',explode,shadow)

- autopct用于格式化饼块的占比数据显示格式
- explode是一个集合，表示每一块饼距离中心的距离，用以强调突出某一个饼块
- shadow是boolean型数据指示是否给饼块添加立体阴影

```python
import matplotlib.pyplot as plt

data = (20, 10, 30, 25)
labels = 'SH', 'BJ', 'SZ', 'GZ'
colors = ('red', 'green', 'blue', 'yellow')
explode = (0, 0, 0.2, 0.05)

# 饼图中坐标x、y默认不是1比1的，所以图像会椭圆，需要指定坐标轴1:1以画出正圆
plt.axes(aspect=1)

plt.pie(x=data,labels=labels,colors=colors,explode=explode, autopct='%0.1f%%', shadow=True)
plt.show()

```

---

## 箱形图

plt.boxplot(data,sym,whis)

- sym表示异常点的显示样式，可同时指定颜色、样式等
- whis，whiskers，表示离群点的范围。箱形图会统计[最小值、四分位值Q1、中间值、四分之三分位值Q3、最大值，平均值，以及离群点]，这里最小值和最大值是排除离群点的，那么怎么确定离群点和最小值最大值之间的区分呢？用whis，$最小值=Q1-(Q3-Q1)*whis$，$最大值=Q3+(Q3-Q1)*whis$，即异常点的判定取决于箱长(Q3-Q1)和whis。whis默认为1.5

```python
import numpy as np
import matplotlib.pyplot as plt
from src.utils import utils as tool

sepal_length,sepal_width,petal_length,petal_width = np.loadtxt(tool.getPath()+'/dataset/iris.data',
                  delimiter=',',
                  unpack=True,dtype=float,usecols=(0,1,2,3))

# 画三种花的sepal_length的箱形图
x = sepal_length[:50],sepal_length[51:100],sepal_length[101:150]
labels = 'A','B','C'

plt.boxplot(x,labels=labels,whis=1,sym='bx')
plt.show()
```

```python
# test whis
import matplotlib.pyplot as plt

x = range(1,100,1)
# Q1=25 MID=50 Q3=75 boxLength=50, 如果whiskers=0.4,则上下都会有5个离群点
plt.boxplot(x,whis=0.4,sym='r.')
plt.show()
```

---

## 颜色和样式

调整颜色、线型、点型

- 字符表示八种内建颜色：red、green、blue、cyan、magenta、yellow、black、white，均可用首字母替代。还可以十六进制表示颜色，如#FF08AB，分别表示三个颜色通道值。还可以RGB元组表示，如（255,255,255）。还有一种灰度表示，color=‘0.5’，表示图像是一个灰色图像，值表示颜色程度。
- 点，直接在matplotlib的官网文档中找markers。matplotlib默认在显示不同marker时分配不同颜色（认为是不同的需要显示的对象）。
- 线：‘--‘虚线，’-‘实线，’-.‘点划线，’:‘点线。
- 样式字符串：可同时在字符串中包含以上三种样式信息，如'rx--'，表示红色，点为x，线为虚线

---

## 编程方式

pyplot、pylab和面向对象的方式

- pyplot：简单易用，底层定制能力不够。
- pylab：结合matplotlib和numpy的模块，模拟了matlab的环境，不推荐用了
- 面向对象：matplotlib的精髓，更基础和底层的方式。

推荐13两种方式根据实际情况综合使用

---

## 子图subplot

matplotlib绘图的三个层级：FigureCanvas 画布，Figure 图，Axes 坐标系。一张图上画多个对比图像，这其实不是多个Figure，而是一个Figure上建立多个Axes，每个Axes表达一个内容。

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1,10)

fig = plt.figure()

axe1 = fig.add_subplot(221)
axe2 = fig.add_subplot(222)
axe3 = fig.add_subplot(223)
axe4 = fig.add_subplot(224)

axe1.plot(x,[ i**3 for i in x])
axe2.scatter(x,x)
axe3.hist(x,bins=9)
axe4.plot(x,-x)

plt.show()
```



## 多图

```python
import matplotlib.pyplot as plt

f1 = plt.figure()
ax1 = f1.add_subplot(111)
ax1.plot([1,2],[1,2])

f2 = plt.figure()
ax2 = f2.add_subplot(222)
ax2.plot([1,2],[2,1])

# 一次弹出两个图框
plt.show()
```



## 网格

axe.grid()、plt.grid()



## 图例

画图的时候指定label，然后plt.legend()自动根据label显示图例

图例可以由plt显示，也可以由axe显示。同样label可以在不同的时机创建

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(10)
f = plt.figure()
ax = f.add_subplot(111)
ax.plot(x,x,label='$ y = x $',color='b')
ax.plot(x,x**2,label='$ y = x^2 $',color='g')
ax.plot(x,x**3,label='$ y = x^3 $',color='r')

ax.grid(linestyle='-.',color='y')

ax.legend()

# 调整坐标轴范围(x1,x2,y1,y2)
plt.axis([0,10,0,500])
```



## 坐标轴范围

plt.axis([x1,x2,y1,y2])

plt.xlim(),plt.ylim()



## 坐标轴刻度


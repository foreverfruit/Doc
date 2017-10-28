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


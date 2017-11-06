# ipython file 用于交互式输入输出
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# 导入时间模块
import datetime

# 创建两个时间对象
start = datetime.datetime(2015,11,6)
stop = datetime.datetime(2017,11,6)
# 创建时间间隔对象
delta = datetime.timedelta(days=1)
# 创建时间格式化器
date_format = mpl.dates.DateFormatter('%Y-%m-%d')

# 转换成matplotlib的时间序列对象
dates = mpl.dates.drange(start,stop,delta)

# 生成随机数据
y = np.random.randn(len(dates))

ax = plt.gca()
# 画时间折线图，实线，不给marker（不会突出数据点）
ax.plot_date(dates,y,linestyle='-',marker='')
# 将日期格式化对象应用到x轴上
ax.xaxis.set_major_formatter(date_format)

# 调整x轴日期标签自适应显示
plt.gcf().autofmt_xdate()

plt.show()
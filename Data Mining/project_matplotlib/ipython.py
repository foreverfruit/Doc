# ipython file 用于交互式输入输出
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

# plt.axis([0,10,0,500])

# plt.ylim([0,50])
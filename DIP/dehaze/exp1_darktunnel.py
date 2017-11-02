"""
实验一：输出图像文件的暗通道图
需要实现算法：求暗通道
"""
from PIL import Image
import imageAlgorithm as alg
import numpy as np

import os

# 默认路径为img目录
path = os.path.abspath('.')+'/img/'

# 加载图像，获得其像素矩阵
filename = 'haze2.jpg'
img = Image.open(path+filename)
if str(img.mode)=='RGB':
    imgArr = np.array(img)
    print('imageArr info: ',imgArr.shape,imgArr.dtype,imgArr.size)
else:
    print('error: image is not RGB mode')
    exit(0)

# 计算其dark tunnel矩阵
alg.getDarkTunnel(imgArr,patch=15)
# alg.getDarkTunnel2(imgArr)

# 输出结果
alg.showImage(imgArr)

# 保存暗通道图文件
img = Image.fromarray(imgArr)
img.save('dt_'+filename)
"""
本模块用于实现各类图像算法
"""
import matplotlib.pyplot as plt
from PIL import Image
import os

# 默认路径为img目录
path = os.path.abspath('.')+'/img/'

def getDarkTunnel(imgArr,patch=15):
    """
    计算图像矩阵相应的暗通道矩阵,matrix in-place update
    :param imgArr:图像矩阵
    :param patch: 暗通道窗口，默认15*15
    这里采用简化通道算法，粗粒度，通道图锯齿化严重
    固定窗口
    """

    # 1.遍历每个像素
    # 2.计算该像素点临近的15*15个像素，计算这225个像素点的三个通道值(RGB)
    #   每个点取的通道可以不同，取最小那个
    #   窗口怎么定？1、给15*15的窗口内的所有像素都取值为这个最低的通道
    #             2、给每个像素都计算一个属于它的窗口的暗通道值，但是要注意边界像素点
    # 3.计算出来的暗通道是1个值，该值应该赋值给这个像素点的哪个通道呢？其他通道取0？--三个通道都取这个暗通道值，否则会有其他颜色乱入
    #   采用方法1
    rows,cols,tunnels = imgArr.shape
    # print(rows,cols,tunnels)
    for i in range(0,rows,patch):
        for j in range(0,cols,patch):
            dt = 255
            # find dark tunnel
            for x in range(i,i+patch):
                for y in range(j,j+patch):
                    if x>=rows or y>=cols:
                        break;
                    wdt = min(imgArr[x,y,:])
                    if wdt<dt:
                        dt = wdt
            # set dark tunnel value for every pixel in patch
            for x in range(i,i+patch):
                for y in range(j,j+patch):
                    if x>=rows or y>=cols:
                        break;
                    # 这里在赋值暗通道的时候，赋值给所有通道
                    imgArr[x,y,:]=[dt,dt,dt]
    return imgArr

# TODO 存在问题，现象不符合
def getDarkTunnel2(imgArr,patch=15):
    """
    细粒度暗通道计算，给每个像素都计算一个属于它的窗口的暗通道值，但是要注意边界像素点
    滑动窗口
    """
    rows,cols,tunnels = imgArr.shape
    for i in range(rows):
        for j in range(cols):
            # current point(i,j)
            dt = 255
            # compute patch [xb,xe,yb,be] 对应begin和end的index
            xb= i-7
            xe = i+7
            if xb<0:
                xe = xe+(0-xb)
                xb = 0
            if xe>(rows-1):
                xb = xb-(xe-rows+1)
                xe = rows-1

            yb, ye = j - 7, j + 7
            if yb < 0:
                ye = ye + (0 - yb)
                yb = 0
            if ye > (cols - 1):
                yb = yb - (ye - rows + 1)
                ye = cols - 1

            # compute dark tunnel value of patch
            for x in range(xb,xe):
                for y in range(yb,ye):
                    wdt = min(imgArr[x, y, :])
                    if wdt<dt:
                        dt = wdt
             # reset point(i,j)'s tunnel value
            imgArr[i,j,:]=(dt,dt,dt)

    return imgArr

def showImage(matrix):
    """
    给定一个像素矩阵，作为图片输出
    :param matrix: 图片的像素矩阵
    """
    plt.figure("image")
    plt.imshow(matrix)
    plt.axis('off')
    plt.show()


def resizeImage(inname,outname,size=(500,500)):
    """
    改变图像大小到指定的size,默认为img目录
    :param inname: 原图像文件名
    :param outname: 输出文件名
    :param size: 输出图像大小，默认500*500
    """
    img = Image.open(path+inname)
    print(img.format, img.size, img.mode)
    img = img.resize(size)
    img.save(path+outname, 'jpeg')



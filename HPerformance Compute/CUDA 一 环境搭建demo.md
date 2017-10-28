[TOC]

---
## 环境搭建与CUDA概述
### Deepin15.4 CUDA环境搭建

- CPU：i5 7300HQ
- 显卡：gtx1050
- 系统：deepin15.4 x64

一、安装nvidia-bumblebee实现双显卡切换

```bash
sudo apt update
sudo apt install bumblebee bumblebee-nvidia nvidia-smi
```

一路yes安装下去，中间可能出现坑，安装过程中，明显听到显卡风扇疯狂转动，感觉电脑电脑爆炸了，无视之，安装完成后，重启，任然爆炸感，检查显卡情况。

```bash
lspci |grep VGA # 查看显卡
lspci |grep -i nvidia # 查看nvidia设备
```

发现nvidia独显是关闭状态的，但是风扇爆炸……关机（不是重启），再启动，正常了，不知道什么情况。

```bash
$ nvidia-smi
$ optirun nvidia-smi
# 以上两个命令查看驱动是否安装成功
# 第一个命令会显示一个启动失败的输出
#第二个命令实际是optimize run优化运行nvidia-smi，此时会输出nvidia显卡工作状态
```

二、安装CUDA开发工具，基于eclipse的nsight

由于cuda版本问题，需要将gcc降到4.8版本

```bash
# 安装4.8版本gcc和g++
sudo apt install g++-4.8 gcc-4.8
# 更改软连接
cd /usr/bin
sudo rm gcc g++
sudo ln -s g++-4.8 g++
sudo ln -s gcc-4.8 gcc
```

下载开发工具nsight

```bash
# 分别是开发环境、工具包、IDE、性能分析工具
sudo apt install nvidia-cuda-dev nvidia-cuda-toolkit nvidia-nsight nvidia-visual-profiler
```

```bash
$ optirun nsight
# 启动nsight集成开发环境，一定要optirun启动，否则编译通过无法启动独显运行
```

---

### 了解CUDA API

- 数据并行c++ Thrust API
- 可用于c和c++的Runtime API
- 可用于c和c++的Driver API

它们的区别与优缺点：

- Thrust API提供高性能、通用性和便捷性，可理解为距离应用开发层最近的上层接口，故开发快捷，可读性强，具有较高维护性。但这也决定了它屏蔽底层硬件，无法发挥硬件全部功能。
- Runtime API。当需要更多的底层功能以获得更好的性能的时候，可以选择放弃高层的Thrust API，选用Runtime API，它通过C语言语法扩展可获得GPGPU的所有可编程特性，因此简洁且高效。
- Driver API。位于最底层的接口，提供更加细致的控制，这种限制不局限于队列和数据传输。使用底层的API需要调用更多函数，指定更多参数，需要检查运行时错误和兼容性问题，即存在更多开发性问题。

> 程序中任意部分可以自由选择使用任意一种类型的API，即可交叉使用。

### 基本概念

- GPGPU：General Purpose Graphics Processing Unit（GPU），GPU作为独立设备外接在主机系统（Host）上，GPGPU与主机处理器并行运转，同时各自处理各自的计算任务。PCIe总线用来在设备间传输数据和命令。

- CUDA数据传输方式：

  - cudaMemcpy()进行显式数据传输（Thrust API中直接通过host的data和gpu的data直接赋值实现，`d_a = h_a;//host数据赋值给device数据`）
  - 通过页锁定内存的映射进行隐式数据传输。该接口维护主机内存区域和gpu设备内存区域，自动完成数据同步不需要人工干预。这种方式可以提高程序执行效率，可实现**零拷贝**操作（但是，这种映射的访问会触发IO的瓶颈吗？）。

- host和GPU device通过驱动程序driver通信，包括数据、命令的通信，以及内存映射、缓冲、队列和同步功能。

- GPGPU运行在一个和主处理器隔离的存储空间，GPGPU有独立的内存空间，且GPU的内存带宽远远高于CPU的内存带宽。CUDA为不同设备之间提供了一个统一虚拟编址UVA，使各设备的代码可通过一个指针访问其他设备的数据（在一个空间中寻址）。

- CUDAKernel。CUDAKernel是在host中调用而运行在CUDA设备上的子程序，它**没有返回值**，通过**\_\_global\_\_**来定义，kernel由主处理器调用。

- Kernel的调用是异步的，

  ​

  ​
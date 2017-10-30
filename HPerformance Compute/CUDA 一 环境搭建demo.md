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

```C
/**
 * Thrust API的并行实现
 */
#include <iostream>
using namespace std;

#include <thrust/reduce.h>
#include <thrust/sequence.h>
#include <thrust/host_vector.h>
#include <thrust/device_vector.h>

int main_thrust(int argc, char const *argv[])
{
	const int N = 50000;

	// 创建数组，GPU设备中
	thrust::device_vector<int> a(N);
	// 填充数组，First元素值为0
	thrust::sequence(a.begin(),a.end(),0);
	// 并行计算数组元素和
	int sumA = thrust::reduce(a.begin(),a.end(),0);
	// 串行计算0到N-1的和
	int sumB = 0;
	for(int i=0;i<N;i++){
		sumB += i;
	}
	// 结果检测
	if(sumA == sumB)
		cout<<"Test Succeeded!"<<endl;
	else{
		cerr<<"Test Failed!"<<endl;
		return 1;
	}
	
	return 0;
}

```

编译运行

```bash
$ nvcc seqCuda.cu -o seqCuda
$ optirun ./seqCuda
```



```c
/**
 * runtime API并行实现
 */

#include <iostream>
using namespace std;

#include <thrust/reduce.h>
#include <thrust/sequence.h>
#include <thrust/host_vector.h>
#include <thrust/device_vector.h>

/**
 * GPU代码，runtime API
 */
__global__ void fillKernel(int *a,int n){
	/**
	 * 计算线程id
	 * blockIdx.x=线程块序号
	 * blockDim.x=每个线程块内的或维度线程数量？？？
	 * threadIdx.x=用于定位该线程在线程块内的编号
	 */
	int tid = blockIdx.x*blockDim.x+threadIdx.x;
	// 可能分配的线程数量多于N，这里只操作N范围内的线程
	if(tid<n)
		a[tid] = tid;
}

/**
 * CPU代码，计算所需的资源，以执行配置形式传入GPUkernel函数中
 */
void fill(int *d_a,int n){
	// 定义每个线程块包含的线程数
	int nThreadsPerBlock = 512;
	// 确定需要的线程块的数量
	int nBlocks = n/nThreadsPerBlock + ((n%nThreadsPerBlock)?1:0);
	// 调用GPU Kernel程序代码，传入执行配置（线程块，线程数/每个线程块）
	fillKernel<<<nBlocks,nThreadsPerBlock>>>(d_a,n);
}

int main_runtime() {
	const int N = 50000;
	// 创建数组
	thrust::device_vector<int> a(N);
	// 填充数组，用runtime api
	fill(thrust::raw_pointer_cast(&a[0]),N);
	// 计算数组元素和，thrust api
	int sumA = thrust::reduce(a.begin(),a.end(),0);
	// 串行计算和
	int sumB = 0;
	for(int i=0;i<N;i++){
		sumB+=i;
	}
	// 检验
	if(sumA==sumB)
		cout<<"Test Succeed!"<<endl;
	else{
		cerr<<"Test Failed!"<<endl;
		return 1;
	}
	return 0;
}

```

编译运行

```bash
$ nvcc seqRuntime.cu -o seqRuntime
$ optirun ./seqRuntime
```



### 基本概念

- GPGPU：General Purpose Graphics Processing Unit（GPU），GPU作为独立设备外接在主机系统（Host）上，GPGPU与主机处理器并行运转，同时各自处理各自的计算任务。PCIe总线用来在设备间传输数据和命令。
- CUDA数据传输方式：

  - cudaMemcpy()进行显式数据传输（Thrust API中直接通过host的data和gpu的data直接赋值实现，`d_a = h_a;//host数据赋值给device数据`）
  - 通过页锁定内存的映射进行隐式数据传输。该接口维护主机内存区域和gpu设备内存区域，自动完成数据同步不需要人工干预。这种方式可以提高程序执行效率，可实现**零拷贝**操作（但是，这种映射的访问会触发IO的瓶颈吗？）。
- host和GPU device通过驱动程序driver通信，包括数据、命令的通信，以及内存映射、缓冲、队列和同步功能。
- GPGPU运行在一个和主处理器隔离的存储空间，GPGPU有独立的内存空间，且GPU的内存带宽远远高于CPU的内存带宽。CUDA为不同设备之间提供了一个统一虚拟编址UVA，使各设备的代码可通过一个指针访问其他设备的数据（在一个空间中寻址）。
- CUDAKernel。CUDAKernel是在host中调用而运行在CUDA设备上的子程序，它**没有返回值**，通过**\_\_global\_\_**来定义，kernel由主处理器调用。
- Kernel的调用是异步的，主机把GPU要执行的kernel顺序提交给GPGPU，然后不等待其执行完成，直接去执行后续的CPU代码，而GPGPU则同时开始并行执行kernel。这样需要一种同步机制给主调方（Host，CPU）和执行方（Device，GPU），CUDA提供两种同步方式：

  - 主机显式调用cudaThreadSynchronize()函数，使主机进入阻塞，等待所有提交的kernel执行完成。
  - 利用cudaMemory()实现阻塞式数据传输——实际在cudaMemory内部会调用cudaThreadSynchronize。
- GPU上基本运行单位是线程，各线程相隔离。***执行配置***定义执行kernel所需的线程数量，同时包含1D、2D或3D计算网格中各维度的分配。执行配置用<<< 配置 >>>包裹在函数名与参数之间。 
- CPU上最大可共享的内存区域称为全局内存，它是GB级别的RAM，但相比访问寄存器，访问全局内存的IO延时非常高，因此要注意数据的重用。
- 数据并行与任务并行。数据并行称为循环级并行，循环内操作数据的并行。任务并行是另一种并行方式，通过将多个任务并发执行来减少执行时间。


### GPGPU编程三条法则

- 交给GPGPU足够多的任务，让它繁忙，增加系统并行度。
- 将数据放入并始终存储于GPU，CPU和GPU之间的PCIe的传输速度相比GPU内部的内存访问速度要慢的太多。尽量避免运行中数据用于传输的损耗。
- 注重GPGPU上的数据重用，避免带宽限制。这里是避免内部全局内存的瓶颈。

需要了解GPU内存的分布、使用机制，了解GPU线程的机制，以及CPU和GPU之间数据同步的过程。

### CUDA和Amdahl定律

Amdahl是一种用以估算串行程序并行化之后的理想加速比，前提条件是并行化后问题尺度保持不变。

$$S(n)=\frac{1}{(1-p)+p/n}$$

其中，p为程序中可并行化的部分，分配给n个处理器上执行。

### 混合执行

同时使用CPU和GPU资源。多核处理器也是一种支持数据并行和任务并行的设备。OpenMP（open multi-processing）提供用于宿主处理器进行多线程程序开发的编程方式。nvcc编译器也支持OpenMP。

```c
/**
 * CPU/GPU异步执行源代码
 * 其中CPU代码通过openMP多核并行执行
 */
#include <iostream>
using namespace std;

#include <thrust/reduce.h>
#include <thrust/sequence.h>
#include <thrust/host_vector.h>
#include <thrust/device_vector.h>

int main(){
	const int N = 50000;
	// 创建数组
	thrust::device_vector<int> a(N);
	// 填充数组，thrust GPU并行
	thrust::sequence(a.begin(),a.end(),0);
	// OpenMP CPU并行计算和
	int sumB = 0;
#pragma omp parallel for reduction(+:sumB)
	for(int i=0;i<N;i++)
		sumB+=i;

	// GPU并行计算数组和
	int sumA = thrust::reduce(a.begin(),a.end(),0);
	// 结果检查
	if(sumA==sumB)
		cout<<"Test Success!"<<endl;
	else{
		cout<<"Test Failed!"<<endl;
		return 1;
	}
	return 0;
}

```

编译运行

```bash
$ nvcc -O3 -Xcompiler -fopenmp seqAsync.cu -o seqAsync
$ optirun ./seqAsync
```


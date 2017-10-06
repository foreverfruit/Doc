[TOC]

---

#  Flag Commit：Supporting Efficient Transaction Recovery in Flash-Based DBMSs



---

## 0. Abstract

- 研究在SLC闪存中运行的DBMSs如何高效得完成事务的恢复。
- 在传统的shadow-paging方式的基础上，提出了新的提交协议flagcommit，能利用flash的快速随机访问、异地更新、局部页编程的特性。
- 利用事务提交标志链内嵌事务状态到闪存页中以减少写log记录的需求。
- 设计了两种恢复协议：commit-based flag commit（CFC）和abort-based flag commit（AFC）。满足不同的性能需求。
- 基于TPC-C标准的测试，评估CFC和AFC性能优于已有的恢复协议。

---

## 1. Introduction

- Flash以其优良特性备受关注，本文研究在事务恢复中如何利用SLC的优点以提高基于闪存的DBMSs的性能。
- 事务恢复作用：保证原子性（一系列动作要么全部完成，要么都不完成）和持久性（提交的写得到保证）。事务恢复已有实现：WAL和Shadow Paging。WAL：以日志的方式持久化旧数据，再原地更新，写操作太频繁。SP：以磁盘上的shadow-page对数据页做异地更新，系统维护一张page ID到disk address的映射表，性能问题使它在磁盘中表现不佳，但是在闪存中确是可取的。
- 循环提交（cyclic commit）是一种根据影子页提出的提交机制。为提交的事务的每一个页维护一个循环链表，通过检查这个表的存在与否确定该事务是否提交。根据这一思想产生两种提交协议：SCC（simple cyclic commit）& BPCC（back pointer cyclic commit）。但是应用中存在一些问题，如高并发等。
- 本文提出一种新的基于影子页的提交机制flagcommit，利用闪存页局部可编程特性保持对事务状态的追踪，在每个shadow page中存储事务的状态标志。基于这种思想本文提出两种提交协议：CFC（commit-based flag commit）& AFC（abort-based flag commit）。它们适用与不同负载、具有不同性能。
- 本文主要工作：
  - 首次提出基于闪存的DBMSs快速高效事务恢复机制，flagcommit。
  - 根据flagcommit提出两种事务恢复协议，以及每个协议针对事务处理、垃圾回收、恢复的算法。
  - 扩展上文提出的两种协议对通用DBMS的支持。
  - 对本文提出的协议做性能评估，结果显示性能提升量巨大。

---

## 2. Background

本节主要内容：*研究背景、闪存特性、闪存转换层FTL*

### 2.1 闪存特性

* 物理特性：片－块（128k+4k）－页（2k+64byte），块为擦除单位，页为读写单位
* IO特性：高效随机访问、先块擦后页写、块擦除次数有限（故在FTL中实现异地更新）

### 2.2 闪存转换层FTL

- FTL的核心是在内存中维护一张逻辑地址到物理地址的映射表，闪存页的OOB区存储其逻辑地址，用以在启动时在FTL建立正向的映射表。
- 通过维护映射表实现异地更新。
- 维护一张空间表，拥有垃圾回收模块回收废弃的页。回收页：触发垃圾回收（如根据块中的废弃页数量）- 将块中有效页复制到空闲块中 - 擦除块 - 将该块挂接到空闲块表中。
- 利用分散写和擦除实现闪存的磨损均衡，以延长使用寿命。



ps：并没有像Introduction介绍的那样在本节介绍研究背景

---

## 3. Basic Flag Commit Protocols

为了系统恢复时确定事务该重做还是丢弃，需要保持对数据库的更新状态以及事务状态的跟踪。shadow paging利用日志进行异地更新以记录事务状态。本文提出的flagcommit基于shadowpaging的方法和循环提交的思想。

flagcommit在每个影子页的OOB区存储一个指向属于同一个事务的之前一个flash page的指针，同时存储状态标志、页版本、事务ID，通过这个链可以找到属于该事务的所有页，通过页中的状态标志可以检查该事务的提交状态。

### 3.1 Commit-Based Flag Commit

CFC协议采用标志指示已提交的事务，默认情况下页的事务标志置FALSE，当事务提交时，属于该事务的页链的最后一个页的事务标识被更新为TRUE。

> - CFC中当且仅当影子页中至少有一个页的事务标志为TRUE时，该事务为已提交事务。
> - 若更新该页的事务已提交，那么该页就是已提交页。

#### In-memory Tables

- 事务表Transaction Table：该表只维护正在执行或中止的事务。表属性包括事务ID、状态、页数、最后页指针。
- 脏页表Dirty Page Table：保持对正在执行的事务更新造成的每个脏页的物理地址的跟踪。
- 地址映射表Direct Mapping Table：维护逻辑地址到物理地址的映射关系。

#### Normal Processing

- 更新页：
  - 事务T提出要更新逻辑页P
  - FlashDisk分配影子页P'，并在该影子页的OOB中初始化LBA、Ver、Link、XID、CommitFlag。
  - 更新事务表Transaction Table，NPage加一、LastPage指向P'。
  - P页添加入脏页表Dirty Table。
  - 更新地址映射表。
- 提交事务：
  - 事务提交请求。
  - 在事务表中找到该事务表项，获得其最后一个影子页，更新其状态标志为TRUE。
  - 将该事务从事务表中删除。
  - 该事务更新的页从脏页表中删除，且其指向的上一个页标记为废弃页。（PS：事务T要更新页P，实际更新的是影子页P'，此时脏页表记录的是事务ID-T、LBA-P'、LastLBA-P，一旦事务T提交，影子页P'“扶正”，原页P标记为废弃）
- 事务中止：
  - 事务T中止
  - 撤销T造成的更新，将其更新的页P'标记为废弃页
  - 检查脏页表，找到P'的上一个页P，通过修改映射表恢复P页

#### Garbage Collection

垃圾回收通过空闲空间的阈值自动触发。回收废弃页或过时的已提交的页。被标记为废弃的页被回收时，其所属的事务还未提交的话，该事务的事务表项的NPage属性要减一。

回收废弃页不足为道，此处关注一下回收过时的已提交页，可能存在两种情况。

- 需要被回收的页是该事务的最后一个页P，即其事务状态标志为TRUE，则在回收前，通过其Link指针找到前一个页P1，然后置P1的状态标志为TRUE，再回收P，保证提交的事务的影子页链中至少存在一个页的事务状态为TRUE
- 需要被回收页是该事务的影子页链中间的页P，则在回收前，需要将P的前一个页P1的状态置为TRUE，这样回收P后，会出现两条影子页链，此时视这两条链属于两个事务，保证这两个事务的影子页链中都至少有一个页的事务状态为TRUE。

#### Recovery

通过扫描全部的页，根据页的 元数据，可以检测到事务是否提交、哪些页属于某一个影子页链（属于某一个事务）、哪些页是事务的最后一个页。根据这些信息，做事务的恢复。

由于影子页链采用的是物理页地址的链接指针，垃圾回收会导致一个事务的影子页链断裂成两个或多个子链。事务提交的时候这多个子链的最后一个页的事务状态标志都会被置TRUE，若是此时系统崩溃，会造成事务状态不一致，同原属于一个事务的子链有部分表现为事务已提交，有部分表现为未提交，此时需要恢复程序做相应的针对处理。一旦检测到上述情况（同一事务ID存在多个影子页链，且提交属性不同），判定此事务未提交（联系子链产生的规则，若事务提交，则影子页子链必定都是表现为已提交）。

### 3.2 Abord-Based Flag Commit

实际中，事务提交比率高于中止率，故在影子页中维护提交标志需要过多开销，若改用中止标志，则会减少开销。这就是AFC协议。两种协议互相弥补根据具体的事务中止率选用。

> AFC协议中，当且仅当所有影子页状态标志为TRUE时，事务状态判定为已提交。（即状态标志意味着“未中止”，一旦出现一个页的“未中止标志”值为FALSE，则该事务状态未终止。注：此处标志意义不能定义为“已提交标志”，“已提交”的TRUE或FALSE状态不等同于“未中止”的TRUE和FALSE状态）

与CFC不同，AFC协议中，事务状态通过对影子页链的第一个页的状态来决定，初始为FALSE，表示中止，一旦提交，首页状态改为TRUE，则没有一个页为FALSE（除了首页，所有页状态初始化为TRUE），表示此事务已提交。且即使垃圾回收将该链分断为多个部分，依然保持该状态。

在事务恢复时，CFC比AFC具有更好性能，取决于判定事务状态的方式不同。CFC不完全遍历影子页链，一旦出现TRUE表示该事务已提交。而AFC需要完全遍历影子页链，直到所有页标志都是TRUE（“未中止”标志）才判定该事务为已提交。

### 3.3 A Discussion Of CFC and AFC

- 通过公式分析AFC&CFC的IO开销：与abort ratio有关。
- 两者的其他两个区别：1）标志位，AFC需要两位标志状态，空间开销更大。2）AFC维护影子页链首，事务状态改变时对首页的修改不可避免，而CFC维护影子页链尾，事务状态改变时，最后一页可能存在与main memory buffer中，故可节省一次重编程改写标志操作。

### 3.4 Block-Based Flag Technique

基于块的标志技术的提出是为了在特定情况下节省页的重编程操作。通常情况下垃圾回收时需要对相应的页的状态标志做修改，需要在该页上重新编程。但是当需要被重编程的这个页正好处在当前需要被回收的块上时，可以采用本节提出的基于块的标志技术，节省页的重编程操作，直接在新块上修改标志。

## 4. Advanced Flagcommit Protocols

扩展Flagcommit协议，以支持采用no-force策略（事务可随时提交，更多的committed事务）的buffer管理，以及高并发控制。

### 4.1 Supporting No-Force Buffer Management

No-Force策略下，事务提交时，没必要立即将buffer中的影子页flush到storage中，因为No-Force策略允许任意commit，若立即flush，会造成写入阻塞，降低事务响应时间和系统吞吐量。（风险是：此时系统奔溃，无法重做已提交的事务，应该committed page没有被持久化到storage中）

为解决上述问题，可以采用将flagcommit协议联合重做日志机制（redo logging scheme）。

工作流程：

- 数据更新前，产生一个redo log record并存入log buffer中。log中保存事务ID、页ID、log记录ID、操作码（更新、删除、插入）、操作数据Data、本事务的前一个log记录的指针PrevLN。
- 当影子页从memory持久化到flash disk时，其对应的log record被移除。
- 当事务提交时，若该事务更新的pages还只是缓存在memory中，那么追加一条commit log record到log buffer中，然后将log buffer内容持久化到flash disk中。
- 事务中止时，回滚memory中被它更新的页，同时移除log record

### 4.2 Supporting Record-Level Concurrency Control

。。。。。。

### 4.3 Putting All Together

4.1与4.2的方案的结合

更新算法、中止算法、提交算法、垃圾回收、事务恢复（恢复算法）

。。。。。。

## 5. Performance Evaluation

基于TPC-C标准对flagcommit协议做性能测试，对比cyclic commit协议和WAL-Based commit协议。

### 5.1 Experiment Setup

- 实验标准：TPC-C
- 实验平台：windows xp + intel Quad CPU + SSD simulator + ...
- 实验对象：CFC\AFC（with block-based flag technique and their extensions）、SCC\BPCC（cyclic commit protocol）、WAL-based commit protocol
- 测量数据：throughtput、transaction execution time、commit response time、recovery cost、garbage collection overhead
- 实验时常：30m预热模拟器+4h实际评估时间

### 5.2 Comparison with Cyclic Commit Protocols





### 5.3 Evaluation of Advanced flagcommit Protocols



## 6. Related Work





## 7. Conclusions And Future Work





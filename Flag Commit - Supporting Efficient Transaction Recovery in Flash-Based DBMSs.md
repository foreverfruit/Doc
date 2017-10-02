[TOC]

---

#  基于闪存的数据库管理系统的高效事务恢复提交协议：Flag Commit

---

## Abstract

- 研究在SLC闪存中运行的DBMSs如何高效得完成事务的恢复。
- 在传统的shadow-paging方式的基础上，提出了新的提交协议flagcommit，能利用flash的快速随机访问、异地更新、局部页编程的特性。
- 利用事务提交标志链内嵌事务状态到闪存页中以减少写log记录的需求。
- 设计了两种恢复协议：commit-based flag commit（CFC）和abort-based flag commit（AFC）。满足不同的性能需求。
- 基于TPC-C标准的测试，评估CFC和AFC性能优于已有的恢复协议。

---

## Introduction

- Flash以其优良特性备受关注，本文研究在事务恢复中如何利用SLC的优点以提高基于闪存的DBMSs的性能。
- 事务恢复作用：保证原子性（一系列动作要么全部完成，要么都不完成）和持久性（提交的写得到保证）。事务恢复已有实现：WAL和Shadow Paging。WAL：以日志的方式持久化旧数据，再原地更新，写操作太频繁。SP：以磁盘上的shadow-page对数据页做异地更新，系统维护一张page ID到disk address的映射表，性能问题使它在磁盘中表现不佳，但是在闪存中确是可取的。
- ​
[TOC]

---

# 读文件

## 用户进程打开硬盘上存在的文件并读取内容

- 打开文件：`int fd = open("/mnt/user/user1/hello.txt",flag,mode);`
- 读取文件：`int size = read(fd,buffer,sizeof(buffer));`

### 打开文件

- 用户进程操作的文件：`*filp[20]`，PCB（struct task_struct,/inclue/linux/sched.h）中的这个域记录当前进程打开的文件指针，*故同时打开的文件次数不超过20次（重复也算）*
- 操作系统管理的所有进程打开的文件：`file_table[64]`
- 文件的i节点：记载文件属性的关键的数据结构

打开文件就是建立三者的关系：

- 用户进程task_struct的*filp[20]与内核中的file_table[64]挂接
- 通过文件名“/mnt/user/user1/hello.txt”找到该文件的i节点
- 将hello.txt的i节点在file_table[64]中登记

### 代码追踪打开文件操作

1. open()  -  sys_open()

   ```c
   // <unistd.h>
   static inline long open(const char * name, int mode, int flags)  
   {  
            return sys_open(name, mode, flags);  
   } 
   ```

   ```c
   // /fs/open.c
   // 1. 挂接 *filp[20] 和 file_table[64]
   int sys_open(const char * filename,int flag,int mode)
   {
   	struct m_inode * inode;
   	struct file * f;
   	int i,fd;

   	mode &= 0777 & ~current->umask;
     // 检查当前进程的filp[20]
   	for(fd=0 ; fd<NR_OPEN ; fd++)
   		if (!current->filp[fd])
   			break;
   	if (fd>=NR_OPEN)
   		return -EINVAL;
   	current->close_on_exec &= ~(1<<fd);
     // 检查内核的file_table	
     	f=0+file_table;
   	for (i=0 ; i<NR_FILE ; i++,f++)
   		if (!f->f_count) break;
   	if (i>=NR_FILE)
   		return -EINVAL;
     // 将两者挂接
   	(current->filp[fd]=f)->f_count++;
     
     .....
   }
   ```

2. 获取文件i节点：sys_open() - open_namei() - dir_namei() - get_dir() - find_entry() - iget() - read_inode()

   ```c
   // /fs/open.c
   // 获取inode
   int sys_open(const char * filename,int flag,int mode)
   {
   	......
   	if ((i=open_namei(filename,flag,mode,&inode))<0) 	 {
   		current->filp[fd]=NULL;
   		f->f_count=0;
   		return i;
   	}
       ......
   }
   ```

   ```c
   // /fs/namei.c
   int open_namei(const char * pathname, int flag, int mode,struct m_inode ** res_inode)
   {
   	const char * basename;
   	int inr,dev,namelen;
   	struct m_inode * dir, *inode;
   	struct buffer_head * bh;
   	struct dir_entry * de;
   	.....
        // 分析路径，获取枝梢i节点
   	if (!(dir = dir_namei(pathname,&namelen,&basename)))
   		return -ENOENT;
   	......
       // 通过枝梢i节点，找到目标文件的目录项
   	bh = find_entry(&dir,basename,namelen,&de);
   ```

   ```c
   // /fs/namei.c
   static struct m_inode * dir_namei(const char * pathname,
   	int * namelen, const char ** name)
   {
   	char c;
   	const char * basename;
   	struct m_inode * dir;

     	// 分析路径，获取i节点的执行函数
   	if (!(dir = get_dir(pathname)))
       /* 
       get_dir函数体中，循环遍历执行find_entry和iget函数，遍历目录树，依次获取硬盘根i节点，user目录i节点，最终到user1目录i节点（枝梢i节点）。
       iget函数会读取i节点，并载入inode_table[32]中
       */
   		return NULL;
   	basename = pathname;
       // 解析路径pathname
   	while (c=get_fs_byte(pathname++))
   		if (c=='/')
   			basename=pathname;
   	*namelen = pathname-basename-1;
   	*name = basename;
       // 返回枝梢节点，user1目录的i节点
   	return dir;
   }
   ```

   ----

   获取目标文件i节点：与枝梢目录i节点获取方式相同，也是find_entry和iget函数

   ```c
   // /fs/namei.c  open_name()
   // 根据user1目录文件i节点，获取hello.txt的目录项
   bh = find_entry(&dir,basename,namelen,&de);
   ...
   // 获取hello.txt文件的i节点
   if (!(inode=iget(dev,inr)))
     return -EACCES;
   ...
   // 将i节点传递给sys_open
   *res_inode = inode;
   ```

3. 文件i节点与file_table[64]挂接

   ```c
   // code block in sys_open()
   // f = 0+file_table，file指针
   f->f_mode = inode->i_mode;
   f->f_flags = flag;
   f->f_count = 1;
   f->f_inode = inode;
   f->f_pos = 0;
   return (fd); // 文件句柄返回给用户空间
   ```

4. 至此，fd就是当前文件hello.txt在file_table[64]中的偏移量，也就是“文件句柄”，此后进程传递该fd给操作系统，操作系统就能知道它对应的硬盘中的文件。

----

### 读取文件

确定当前读取内容的逻辑块号 - 创建读取数据的缓冲块 - request - do_hd读盘 - 进程挂起，schedule()到其他进程 - 硬盘读中断 - 中断服务程序：硬盘缓冲存入内存缓冲块 - 将缓冲块中的数据复制到用户空间的缓冲区buffer中。

1. read() - sys_read()

   ```c
   // /fs/read_write.c
   int sys_read(unsigned int fd,char * buf,int count)
   {
   	struct file * file;
   	struct m_inode * inode;

      // read操作可行性检查：fd、count、buffer是否合法
   	if (fd>=NR_OPEN || count<0 || !(file=current->filp[fd]))
   		return -EINVAL;
   	if (!count)
   		return 0;
   	verify_area(buf,count);
   	inode = file->f_inode;
   	if (inode->i_pipe)
   		return (file->f_mode&1)?read_pipe(inode,buf,count):-EIO;
   	if (S_ISCHR(inode->i_mode))
   		return rw_char(READ,inode->i_zone[0],buf,count,&file->f_pos);
   	if (S_ISBLK(inode->i_mode))
   		return block_read(inode->i_zone[0],&file->f_pos,buf,count);
   	if (S_ISDIR(inode->i_mode) || S_ISREG(inode->i_mode)) {
   		if (count+file->f_pos > inode->i_size)
   			count = inode->i_size - file->f_pos;
   		if (count<=0)
   			return 0;
          // 通过inode的mode检查文件类型，确定读取方式
   		return file_read(inode,file,buf,count);
   	}
   	printk("(Read)inode->i_mode=%06o\n\r",inode->i_mode);
   	return -EINVAL;
   }
   ```

2. file_read() - bmp() 确定指定文件数据块在外设上的逻辑块号

   ```c
   // fs/file_dev.c
   int file_read(struct m_inode * inode, struct file * filp, char * buf, int count)
   {
   	int left,chars,nr;
   	struct buffer_head * bh;

   	if ((left=count)<=0)
   		return 0;
   	while (left) {
         // 此处filp->fos为文件操作指针偏移量，BLOCK_SIZE=1024,块大小，相除得当前操作的数据块号，bmap函数根据数据块号确定其在外设上的逻辑块号
   		if (nr = bmap(inode,(filp->f_pos)/BLOCK_SIZE)) {
             // bread即block read 读取逻辑块
   			if (!(bh=bread(inode->i_dev,nr)))
   				break;
   		} else
   		......
       }     
   }
     
   // fs/inode.c
   int bmap(struct m_inode * inode,int block)
   {
   	return _bmap(inode,block,0);
   }

   // fs.inode.c
   // 该函数通过linux文件数据块管理机制，返回当前操作文件的操作数据块对应的逻辑块
   static int _bmap(struct m_inode * inode,int block,int create)
   // i节点通过i_zone结构管理文件数据块，i_zone[9]，前七个块对应7kb的数据块（每块1kb），文件大小超过7kb，则i_zone[7]作为一级间接块，类似于一种索引，它又链接着512个数据块，当文件超过 512+7 kb，i_zone[8]作为二级间接块，管理512*512个块，故最大可以管理(512*512+512+7)个数据块
   ```

3. bread函数将hello.txt文件的第一个数据块读入缓冲块。

   该过程很复杂，简要整理一下流程：

   - `bread(int dev,int block);// fs/buffer.c`指定设备及其数据块，在bread中调用`getblk(dev,block);// fs/buffer.c 在内存的缓冲区得到与dev、block相符合或空闲的缓冲块`函数
   - getblk函数会查找指定（dev，block）缓冲块，若没有就申请一个。查找会通过`get_hash_table(dev,block)// fs.buffer.c`函数，get_hash_table通过调用`find_buffer(dev,block)`查找缓冲块，此处会通过dev、block采用哈希查找。若没有查找到，返回getblk函数中，申请一个缓冲块（通过系统维护的缓冲区空闲表free_list），将这个缓冲块挂接到hash_table上。
   - 从getblk返回bread函数，此时内存中了读取数据用的缓冲块，需要将该缓冲块与请求项结构挂接（请求项管理结构request[32]是操作系统管理缓冲区中的缓冲块与块设备上逻辑块之间读写关系的数据结构），`ll_rw_block(int rw,struct buffer_head *bh)`函数调用`make_request`函数将这个缓冲块加锁，找空闲请求项，找不到就新建一个，然后初始化请求项，再将其通过`add_request`加载到当前的亲求队列中。
   - add_request中，调用设备的请求项处理函数（dev->request_fn，即do_hd_request()）给硬盘发送读盘命令。
   - do_hd_request函数通过`hd_out(dev,nsect,sec,cyl,WIN_READ,&read_intr)`下达读盘指令，同时为硬盘操作关联了一个中断服务函数read_intr。
   - bread中进入wait_on_buffer函数，调用sleep_on、schedule()函数将当前进程设置为不可中断等待状态，cpu切换到其他进程。
   - 之后某时刻硬盘读完一个扇区的数据到硬盘缓冲，产生硬盘中断，执行中断服务程序read_intr，将硬盘缓冲中的数据复制到之前准备好的内存中的缓冲块中。当数据全部读取完毕后，read_intr会调用end_request函数，将内存的缓冲块解锁，设置更新参数，唤醒被挂起的读进程。
   - 读进程进入就绪状态，当下一次schedule函数调度到该进程时，返回到bread函数中，检查缓冲块标志为已更新，直接返回到file_read中去进行下一步处理。

4. 将缓冲块中的数据复制到用户进程空间的buffer中

   ```c
   // fs/file_dev.c
   int file_read(struct m_inode * inode, struct file * filp, char * buf, int count)
   {
   	int left,chars,nr;
   	struct buffer_head * bh;

   	if ((left=count)<=0)
   		return 0;
   	while (left) {
   		if (nr = bmap(inode,(filp->f_pos)/BLOCK_SIZE)) {
   			if (!(bh=bread(inode->i_dev,nr)))
   				break;
   		} else
   			bh = NULL;
         	// 计算复制多少字节到用户空间
   		nr = filp->f_pos % BLOCK_SIZE;
   		chars = MIN( BLOCK_SIZE-nr , left );
   		filp->f_pos += chars;
   		left -= chars;
   		if (bh) {
   			char * p = nr + bh->b_data;
             // 将chars字节的数据复制到用户空间
   			while (chars-->0)
   				put_fs_byte(*(p++),buf++);
   			brelse(bh);
   		} else {
   			while (chars-->0)
   				put_fs_byte(0,buf++);
   		}
   	}
   	inode->i_atime = CURRENT_TIME;
   	return (count-left)?(count-left):-ERROR;
   }
   ```

----

## 用户进程新建文件并写入数据到文件


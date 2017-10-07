[TOC]

---

# chapter 2 快速入门

- python中未指定返回值的函数会自动返回None，等价于NULL

- python与大多数解释执行的脚本语言相同，使用语句输出（如很多shell脚本用echo输出程序结果）。

- 可以使用print显示变量的字符串表示，或者仅用变量名查看变量的原始值

  ```python
  >>>str = '''hello
  ... nihao
  ... wo ye hao'''
  >>> print str # 建议采用括号包裹参数，因为python3这样要求
  hello
  nihao
  wo ye hao
  >>> str
  'hello\nihao\nwo ye hao'
  # 用变量名输出时，字符串采用单引号括起来，这是为了让非字符串对象也能以字符串方式显示在屏幕上，它显示的是该对象的字符串表示，而不仅仅是字符串本身
  >>> a = 10
  >>> a
  10
  ```

- '_'下划线在解释器中有特别含义，表示最后一个表达式的值

  ```python
  >>> a = 'hello world'
  >>> a # 这才是最后一个表达式，上面那个声明语句并不是
  'hello world'
  >>> _
  'hello world'
  ```

- python的print语句，可以与字符串格式符号%结合使用，实现字符串的参数替代功能

  ```python
  >>> print("%s is number %d" % ('python',1))
  python is number 1
  # 在python3中，采用format()函数控制参数化格式输出

  ```

- print语句支持输出重定向到文件，用符号>>重定向

- 使用内建函数raw_input()获取用户输入，使用int()将字符串转换为整形。注：***python3中删除raw_input()，改用input()***

- 注释：单行注释：#；多行注释：'''x''' or """xx"""；文档注释：模块、函数或者类的第一行添加一个字符串，这就是它的文档

  ```python
  def foo():
  	" this is doc string for function foo."
  	return True	
  	
  ```

- 算数操作符： + - * / // % ** ps:(//表示浮点除法，对整数出发不做四舍五入，**表示乘方，可用于字符串)

- 关系操作符：< 、>、 <= 、>= 、==、 !=、 <>。(<>正被遗弃的不等关系符)

- 逻辑操作符：and、or、not；

  ```python
  >>> 3<4<5 #等价于 3<4 and 4<5
  ```

- python作为动态语言，不用预先申明变量类型，变量类型和值在赋值时就被初始化了。

- 数字：有符号整形（长整形、布尔值）、浮点值、复数

- 字符串：
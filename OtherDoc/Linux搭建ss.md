1、ssh连接远程系统

```bash
# -p表示端口，值为xx，root是用户名，ip是远程服务器ip地址
$ ssh -p xx root@ip
# 之后会让你输入登录密码，就是服务器的root账户的密码
# 可能是服务器自动生成的一串复杂密码，也可能是自己设置的
```

2、查看python版本

```bash
# 查看版本，一般系统都会自带python的，ubuntu下
$ python --version
# 安装并切换python版本，个人喜欢用python3,推荐用python2，不然后面加密库有坑
$ sudo apt-get install python3.5
$ sudo rm /usr/bin/python
$ sudo ln -s /usr/bin/python3.5 /usr/bin/python
# 现在再查看就是python3了
$ python --version
```

3、安装python pip

```bash
# 安装Pip，这里注意pip版本要和python版本匹配
# python2版本 sudo apt-get install python-pip
$ sudo apt-get install python3-pip
# 检查 pip 是否安装成功su
$ pip3 -V
```

4、通过pip安装shadowsocks

```bash
# 运行pip安装，可能会提示你升级pip，注意pip版本，这里pip链接的是pip3
$ sudo pip install shadowsocks
# 之后为了支持shadowsocks的加密方式，可能需要安装一个用于加密的库
$ apt–get install python–m2crypto
```

** 坑1

```bash
# 3\4步骤的时候，可能出现locale错误，报错如下
unsupported locale setting
# 这是语言环境错误，locale用于查看，会出现Cannot项
$ locale
# 修正
$ export LC_ALL=C
# 之后pip能正常使用了
```

5、设置shadowsocks

```bash
$ vim /etc/shadowsocks.json
```

```json
{
  "server":"ip",
  "local_address":"127.0.0.1",
  "local_port":1080,
  "server_port":8388,
  "port_password":{
      "8381":"pwd",
      "8382":"pwd",
      "8383":"pwd"
  },
  "timeout":300,
  "method":"aes-256-cfb",
  "fast_open":false
}
```

```bash
# 为该文件设置权限
$ sudo chmod 755 /etc/shadowsocks.json
```



6、启动shadowsocks

```bash
$ sudo ssserver -c /etc/shadowsocks.json -d start
```



7、配置开机自启动

```bash
# 编辑 /etc/rc.local 文件
$ sudo vi /etc/rc.local
# 在 exit 0 这一行的上边加入如下
$ /usr/local/bin/ssserver –c /etc/shadowsocks.json
```




















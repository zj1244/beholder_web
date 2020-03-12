# beholder 

**beholder**是一款简洁监控端口变化的系统，由 `beholder_scanner`， `beholder_web`  两个部分组成。**当前项目为 `beholder_web`部分**。

 `beholder_scanner`和`beholder_web`可以部署在一台机器上，也可以分开部署在不同的机器上。 

* **beholder_scanner**：对IP进行端口扫描、比较端口变化，可部署多个beholder_scanner来组成集群加快扫描速度。
* **beholder_web**：提供前端界面展示。

## 支持平台

* Linux
* Windows

## 安装指南（以下操作均在centos 7上进行）

[![Python 2.7](https://img.shields.io/badge/python-2.7-yellow.svg)](https://www.python.org/) 
[![Mongodb 3.x](https://img.shields.io/badge/mongodb-3.x-green.svg)](https://www.mongodb.com/download-center?jmp=nav)
[![Redis 3.x](https://img.shields.io/badge/redis-3.x-green)](https://redis.io/)

**依赖：项目运行依赖于mongodb和redis，所以需准备好mongodb和redis，mongodb和redis安装请参考：**

* [mongodb安装](./docs/mongodb.md)
* [redis安装](./docs/redis.md)

### 1. 安装python依赖库

```
# pip install -r requirements.txt
```

### 2. 安装nmap（已安装跳过）

```
# rpm -vhU https://nmap.org/dist/nmap-7.80-1.x86_64.rpm
# nmap -V //输出nmap版本号为成功
```

### 3. 添加mongodb认证

在mongodb服务器上添加db用户，这里的`scan`和`123456`需要更换为你的mongodb的账户和密码。

```
# mongo
> use admin
> db.createUser({user:'scan',pwd:'123456', roles:[{role:'readWriteAnyDatabase', db:'admin'}]})
> exit
```

### 4. 修改配置文件

首先将`config.py.sample`复制一份重命名为`config.py`
```
# cp scanner/config.py.sample scanner/config.py

```

然后按照自己的要求修改配置：

```
# coding=utf-8

# 1是ping发现主机，0是通过发送tcp syn包到指定端口来发现主机
FIND_HOST = 1

# redis配置，需按照实际情况修改
REDIS_IP = "192.168.1.1"
REDIS_PORT = "6379"
REDIS_PWD = "pwd"
VULSCAN_KEY = ""  # 用于后续扫描的队列，没后续扫描则保留为空

# db配置，需按照实际情况修改
MONGO_IP = "192.168.1.1"
MONGO_PORT = 27017
MONGO_USER = "scan"
MONGO_PWD = "123456"
# 可以保持默认
MONGO_DB_NAME = "portscan"
MONGO_TASKS_COLL_NAME = "tasks"
MONGO_RESULT_COLL_NAME = "scan_result"
MONGO_SETTING_COLL_NAME = "setting"


```

### 5. 导入数据库

进入`db`文件夹，执行如下命令：

```
# mongorestore -u scan -p 123456 --authenticationDatabase admin -d portscan .
```

### 6. 启动

在程序目录下执行如下命令：

```
# python main.py
```



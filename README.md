# beholder 

## 介绍

**beholder**是一款简洁而小巧的系统，主要作用是通过监控端口变化来发现企业内部的信息孤岛。例如：运维或开发新部署了一台机器未通知安全。

系统由 `beholder_scanner`、 `beholder_web`  两个部分组成。这两个部分可以部署在一台机器上，也可以分开部署在不同的机器上。**当前项目为 `beholder_web`部分**。

* **beholder_scanner**：对IP进行端口扫描、比较端口变化，可部署多个beholder_scanner来组成集群加快扫描速度。
* **beholder_web**：提供前端界面展示。

## 支持平台

* Linux
* Windows

## 安装指南（以下操作均在centos 7上进行）

[![Python 2.7](https://img.shields.io/badge/python-2.7-yellow.svg)](https://www.python.org/) 
[![Mongodb 3.x](https://img.shields.io/badge/mongodb-3.x-red.svg)](https://www.mongodb.com/download-center?jmp=nav)
[![Redis 3.x](https://img.shields.io/badge/redis-3.x-green)](https://redis.io/)

**依赖：项目运行依赖于mongodb和redis，所以需准备好mongodb和redis，mongodb和redis安装请参考：**

* [mongodb安装](./docs/mongodb.md)
* [redis安装](./docs/redis.md)

### 1. 安装python依赖库

```
# pip install -r requirements.txt
```

### 2. 修改配置文件

首先将`config.env.sample`复制一份重命名为`config.env`
```
# cp config.env.sample config.env
```

然后按照自己的要求修改配置：

```
# username and password
ACCOUNT="admin"
PASSWORD="admin"

# mongodb
MONGO_IP = '192.168.47.168'
MONGO_PORT = 27018
MONGO_USER = 'scan'
MONGO_PWD = '123456'
MONGO_DB_NAME = 'portscan'

# redis
REDIS_IP = "192.168.47.168"
REDIS_PORT = "6378"
REDIS_PWD = "pwd"
```

### 3. 启动

在程序目录下执行如下命令：

```
# python main.py
```



## Linux环境下安装指南（以下操作均在centos 7上进行）

### 1. 安装python依赖库

```
# pip install -r requirements.txt
```

### 2. 修改配置文件

首先将`config.env.sample`复制一份重命名为`config.env`
```
# cp config.env.sample config.env
```

然后按照自己的要求修改登陆用户名密码、mongodb和redis连接配置：

```
# username and password
ACCOUNT="admin"
PASSWORD="admin"

# databases
MONGO_IP = "192.168.47.169"
MONGO_PORT = 27017
MONGO_USER = "scan"
MONGO_PWD = "123456"
MONGO_DB_NAME = "portscan"

# redis
REDIS_IP = "192.168.47.169"
REDIS_PORT = "6379"
REDIS_PWD = "pwd"
```

### 3. 启动

在程序目录下执行如下命令：

```
# python main.py
```

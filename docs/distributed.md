## 部署mongodb和redis

* [mongodb安装](./mongodb.md)
* [redis安装](./redis.md)

## 部署 beholder_web和beholder_scanner

### 1. 构建镜像&&启动容器

使用 vi 新建一个名为docker-compose.yml的文件，文件内容如下：

```
# vi install_web_and_scanner.yml # 第一步，使用 vi 新建一个名为install_web_and_scanner.yml的文件，文件内容如下：
version: '3'
services:
  scanner:
    image: zj1244/beholder_scanner:latest
    restart: always
    environment:
      # 请修改以下redis和mongodb的配置
      REDIS_IP: 192.168.47.168
      REDIS_PORT: 6378
      REDIS_PWD: pwd
      MONGO_IP: 192.168.47.168
      MONGO_PORT: 27018
      MONGO_USER: scan
      MONGO_PWD: 123456
  web:
    build: .
    ports:
     - "8000:80"
    restart: always
    environment:
      # 请修改以下redis和mongodb的配置
      REDIS_IP: 192.168.47.168
      REDIS_PORT: 6378
      REDIS_PWD: pwd
      MONGO_IP: 192.168.47.168
      MONGO_PORT: 27018
      MONGO_USER: scan
      MONGO_PWD: 123456

# docker-compose up -d -f install_web_and_scanner.yml # 第二步，启动镜像
```

**或者**

请按照实际情况修改 install_web_and_scanner.yml 文件里关于redis和mongodb的信息。
```
# git clone https://github.com/zj1244/beholder_web.git
# cd beholder_web
# vi install_web_and_scanner.yml #需要修改redis和mongodb的配置信息
# docker-compose up -d -f install_web_and_scanner.yml
```

至此整套程序部署完毕，如果需要部署多个scanner可以参考以下步骤

## 部署单个 beholder_scanner

在多个主机上重复部署beholder_scanner提高扫描速度。

### 1. 构建镜像&&启动容器

使用 vi 新建一个名为docker-compose.yml的文件，文件内容如下：

```
# vi docker-compose.yml # 第一步，使用 vi 新建一个名为docker-compose.yml的文件，文件内容如下：
version: '3'
services:
  scanner:
    image: zj1244/beholder_scanner:latest
    restart: always
    environment:
      # 请修改以下redis和mongodb的配置
      REDIS_IP: 192.168.47.168
      REDIS_PORT: 6379
      REDIS_PWD: pwd
      MONGO_IP: 192.168.47.168
      MONGO_PORT: 27017
      MONGO_USER: scan
      MONGO_PWD: 123456
# docker-compose up -d # 第二步，启动镜像
```

**或者**

请按照实际情况修改 docker-compose.yml 文件里关于redis和mongodb的信息。
```
# git clone https://github.com/zj1244/beholder_scanner.git
# cd beholder_scanner
# vi docker-compose.yml #需要修改redis和mongodb的配置信息
# docker-compose up -d
```

### 2. 检查scanner是否正常启动
输入如下命令，如果输出`扫描开始`则表示启动成功
```
# docker logs $(docker ps | grep beholder_scanner | awk '{print $1}')
[2020-02-15 15:48:56,575] [INFO] 扫描开始
```
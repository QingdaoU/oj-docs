## 查看Docker容器运行状态
运行`docker ps -a`，可以看到以下输出。

```bash
CONTAINER ID        IMAGE                                                        COMMAND                  CREATED             STATUS                       PORTS                                         NAMES
645070877c6c        registry.cn-hangzhou.aliyuncs.com/onlinejudge/oj_backend     "/bin/sh -c 'sh /app…"   About an hour ago   Up About an hour (healthy)             0.0.0.0:443->1443/tcp, 0.0.0.0:80->8000/tcp   oj-backend
b6fc725b2417        registry.docker-cn.com/library/redis:4.0-alpine              "docker-entrypoint.s…"   About an hour ago   Up About an hour             6379/tcp                                      oj-redis
3402b59b96d3        registry.docker-cn.com/library/postgres:10-alpine            "docker-entrypoint.s…"   About an hour ago   Up About an hour             5432/tcp                                      oj-postgres
7c399af69344        registry.cn-hangzhou.aliyuncs.com/onlinejudge/judge_server   "/bin/sh -c '/bin/ba…"   About an hour ago   Up About an hour (healthy)   8080/tcp                                      judge-server


```

`CONTAINER_ID`就是容器的id，以后会经常用到。`STATUS`就是当前容器的运行状态，`Up xxx (healthy)`就是正常运行状态，`unhealthy`或`Exited (x) xxx`就是退出状态。

## 进入正在运行的容器

由`docker ps -a`得到CONTAINER_ID，然后运行`docker exec -it {CONTAINER_ID} /bin/sh`。

## 容器异常退出

容器`STATUS`显示为`Exited(x) xxx`，运行`docker logs {CONTAINER_ID}`，查看错误信息。

## No such file or directory

查看docker-compose.yml中文件映射的路径是否有误，冒号前面应该是服务器上实际的路径，冒号后面的不需要修改。

## 在启动容器的时候 ERROR: client and server don't have same version

请升级`docker-compose`至最新版

## Welcome to nginx

 - nginx配置中server_name和当前访问的域名是否一致

## 静态文件无法显示
 
 - 确认是否访问的是80端口，不要访问nginx proxy_pass的那个地址。

 - 确认nginx中代码路径是否正确。

## CentOS 常见问题

 - docker之间无法连通，尝试关闭防火墙或添加规则。
 - 访问网页无法限制静态文件，尝试关闭SELlinux或者添加规则。

## Invalid token

请查看`docker-compose.yml`内的`JUDGE_SERVER_TOKEN`与`TOKEN`是否一致

## 我的浏览器不显示数据或者显示异常

请使用 Chrome 或 Firefox 使用本OJ，如不能解决，请反馈问题
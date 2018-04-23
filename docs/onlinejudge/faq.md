## 有 docker hub 的镜像么

有 https://hub.docker.com/u/qduoj/

## smtp 配置不成功

 - OnlineJudge 不支持 ssl，请使用 tls，比如 qq 邮箱是 smtp.qq.com / tls / port 25
 - 部分邮箱 smtp 密码不是登录密码，而是单独的授权密码

## CentOS 上部署遇到问题

 - 检查 docker 版本是否太老
 - 关闭 SELinux
  
## 查看 Docker 容器运行状态

运行`docker ps -a`，可以看到以下输出。

```bash
CONTAINER ID        IMAGE                                                        COMMAND                  CREATED             STATUS                       PORTS                                         NAMES
645070877c6c        registry.cn-hangzhou.aliyuncs.com/onlinejudge/oj_backend     "/bin/sh -c 'sh /app…"   About an hour ago   Up About an hour (healthy)             0.0.0.0:443->1443/tcp, 0.0.0.0:80->8000/tcp   oj-backend
b6fc725b2417        registry.docker-cn.com/library/redis:4.0-alpine              "docker-entrypoint.s…"   About an hour ago   Up About an hour             6379/tcp                                      oj-redis
3402b59b96d3        registry.docker-cn.com/library/postgres:10-alpine            "docker-entrypoint.s…"   About an hour ago   Up About an hour             5432/tcp                                      oj-postgres
7c399af69344        registry.cn-hangzhou.aliyuncs.com/onlinejudge/judge_server   "/bin/sh -c '/bin/ba…"   About an hour ago   Up About an hour (healthy)   8080/tcp                                      judge-server
```

`NAMES`就是容器的名称，后面会经常用到。`STATUS`就是当前容器的运行状态，`Up xxx (healthy)`就是正常运行状态，`unhealthy`或`Exited (x) xxx`就是退出状态。

注意下面使用 `{CONTAINER_NAME}` 的地方，都使用对应的名字替换，需要去除大括号。

## 进入正在运行的容器

然后运行`docker exec -it {CONTAINER_NAME} /bin/sh`，比如 `docker exec -it oj-backend /bin/sh`。

## 容器异常退出

容器`STATUS`显示为`Exited(x) xxx`，运行`docker logs {CONTAINER_NAME}`，查看错误信息。

## docker-compose 启动的时候报错 'module' object has on attribute 'connection'

尝试运行 `pip install --upgrade pip && pip install -U urllib3`，然后再重试看看。

## Invalid token

请查看`docker-compose.yml`内的`JUDGE_SERVER_TOKEN`与`TOKEN`是否一致

## 80 或者 443 端口被占用导致 docker 无法启动

错误信息 `bind 0.0.0.0:80 failed, port is already allocated`

修改 docker-compose 中 `ports` 相关的配置，比如 `0.0.0.0:80:8080` 可以修改为 `0.0.0.0:8020:8080`，冒号后面的端口号不会冲突请勿改动。

## 我的浏览器不显示数据或者显示异常

请使用 Chrome 或 Firefox 使用本OJ，如不能解决，请反馈问题。
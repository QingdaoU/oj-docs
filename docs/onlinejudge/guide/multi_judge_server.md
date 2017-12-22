# 多个评测机

多个评测机只需确保两点即可正常运行:

 - JudgeServer Token 一致
 - 进行测试用例的多机同步

本OJ使用 `rsync` 进行同步，步骤如下:

### 在部署好的机器上开启测试用例同步 master 服务

在已经部署好的服务器上，修改 `OnlineJudgeDeploy` 里的 `docker-compose.yml` 文件

将下列代码合并进去(即添加一个service，注意缩进), 并运行`docker-compose up -d`:

```yaml
  oj-rsync-master:
    image: registry.cn-hangzhou.aliyuncs.com/onlinejudge/oj_rsync
    container_name: oj-rsync-master
    volumes:
      - $PWD/data/backend/test_case:/test_case:ro
      - $PWD/data/rsync_master:/log
    environment:
      - RSYNC_MODE=master
      - RSYNC_USER=ojrsync
      - RSYNC_PASSWORD=CHANGE_THIS_PASSWORD
    ports:
      - "0.0.0.0:873:873"
```

!> 请务必修改`RSYNC_PASSWORD`，否则会导致测试用例的泄露

### 在新的机器上配置 JudgeServer 和测试用例同步 slave 服务

在新的的机器上按照 `OnlineJudgeDeploy` 项目初始化环境，修改 `docker-compose.yml`，只需要保留 `judge-server` 一个 service，然后添加下面的 service 到文件中。

```yaml
  oj-rsync-slave:
    image: registry.cn-hangzhou.aliyuncs.com/onlinejudge/oj_rsync
    container_name: oj-rsync-slave
    volumes:
      - $PWD/data/backend/test_case:/test_case
      - $PWD/data/rsync_slave:/log
    environment:
      - RSYNC_MODE=slave
      - RSYNC_USER=ojrsync
      - RSYNC_PASSWORD=CHANGE_THIS_PASSWORD
      - RSYNC_MASTER_ADDR=YOUR_BACKEND_ADDR
```

!> 请同步修改 `RSYNC_PASSWORD`，并将 `RSYNC_MASTER_ADDR` 修改为运行了 `oj-rsync-master` 服务的地址，不需要端口号，如 `example.com` 或者 `192.168.1.10`。

然后给 JudgeServer 添加

```
  ports:
    - "0.0.0.0:80:8080"
```

的端口配置，同时还需要修改 

 - `SERVICE_URL` 为新的机器的地址
 - `BACKEND_URL` 的域名为已部署好的主机的地址
 - `TOKEN` 和已部署好主机 `TOKEN` 一致。

运行 `docker-compose up -d` 即可启动一台新的 JudgeServer，`tail -f data/rsync_slave/rsync_slave.log` 可以看到测试用例同步进度，在已部署好主机的后台可以看到新的 JudgeServer 的心跳状态。

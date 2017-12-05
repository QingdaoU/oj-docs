# 多个评测机

!>不建议在一台机器上运行多个评测服务， 因单个评测服务已经利用了多核计算,多个服务可能会导致判题性能降低

多个评测机只需确保两点即可正常运行:

+ JudgeServer Token一致
+ 进行test_case多机同步

本OJ使用`rsync`进行同步,大致步骤如下:

1. 修改OnlineJudgeDeploy里的`docker-compose.yml`文件

  将下列代码合并进去(即添加一个service), 并运行`docker-compose up -d`:

```yaml
version: "3"
services:
  oj-rsync-master:
    image: registry.cn-hangzhou.aliyuncs.com/onlinejudge/oj_rsync
    container_name: oj-rsync
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

!> 请务必修改`RSYNC_USER`和`RSYNC_PASSWORD`，否则会导致test_case的泄露

2. 新的JudgeServer配置

  在另外的机器上新建目录并创建`docker-compose.yml`，粘贴进如下代码:

```yaml
version: "3"
services:
  judge-server:
    image: registry.cn-hangzhou.aliyuncs.com/onlinejudge/judge_server
    container_name: judge-server
    read_only: true
    cap_drop:
      - SETPCAP
      - MKNOD
      - NET_BIND_SERVICE
      - SYS_CHROOT
      - SETFCAP
      - FSETID
    tmpfs:
      - /tmp
      - /judger_run:exec,mode=777
      - /spj:exec,mode=777
    volumes:
      - $PWD/data/test_case:/test_case:ro
      - $PWD/data/judge_server:/log
    environment:
      - service_url=http://judge-server:8080
      - service_discovery_url=http://oj-backend:12358/api/judge_server_heartbeat/
      - TOKEN=CHANGE_THIS
    ports:
      - "0.0.0.0:12358:8000"

  oj-rsync-slave:
    image: registry.cn-hangzhou.aliyuncs.com/onlinejudge/oj_rsync
    volumes:
      - $PWD/data/test_case:/test_case
      - $PWD/data/rsync_slave:/log
    environment:
      - RSYNC_MODE=slave
      - RSYNC_USER=ojrsync
      - RSYNC_PASSWORD=CHANGE_THIS_PASSWORD
```

  需要对`environment`里的变量根据实际情况进行修改:

  + `service_url`: 将`judge-server`改为OJ后台所在服务器的地址，默认为8080端口
  + `service_discovery_url`: 将`oj-backend`改为本地地址
  + `TOEKN`： 需要与后台的`JUDGE_SERVER_TOEKN`保持一致
  + `RSYNC_USER`和`RSYNC_PASSWORD`与上面的相同

  运行`docker-compose up -d`即可启动一台新的JudgeServer

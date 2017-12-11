# 代码升级说明

因为新版系统还处于快速升级迭代中，如果您部署或者正在使用OnlineJudge，建议watch一下本项目，这样每次发布新的release的时候就可以收到邮件提醒了。

# 升级步骤

!> 以下方法仅适用于用官方[部署脚本](https://github.com/QingdaoU/OnlineJudgeDeploy)搭建的OJ

如果对部署仓库代码有改动，请自行备份或`git stash`,然后在 OnlineJudgeDeploy目录运行下列命令即可完成升级：

```bash
git pull
docker-compose pull && docker-compose up -d
```

不过一般来说`Redis`和`Postgresql`的镜像无需更新,因此可对OJ相关镜像单独pull, 这样可以节约升级时间, 这和上述命令在大多数情况下达到的效果是一样的(除非大版本升级)：

```bash
git pull
docker pull registry.cn-hangzhou.aliyuncs.com/onlinejudge/judge_server
docker pull registry.cn-hangzhou.aliyuncs.com/onlinejudge/oj_backend
docker-compose up -d
```

如果还有任何问题，请提出issue。 

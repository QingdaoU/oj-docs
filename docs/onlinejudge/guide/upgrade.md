# 代码升级说明

因为新版系统还处于快速升级迭代中，如果您部署或者正在使用OnlineJudge，建议watch一下本项目，这样每次发布新的release的时候就可以收到邮件提醒了。

# 升级步骤

若您是按照[部署说明](https://github.com/QingdaoU/OnlineJudgeDeploy)搭建的，直接在`OnlineJudgeDeploy`运行`docker-compose pull`，之后运行`docker-compose up -d`启动容器即可。

一般来说`Redis`和`Postgresql`的镜像无需更新,可对Docker镜像单独pull, 只更新`judge_server`和`oj-backend`:

```bash
docker pull registry.cn-hangzhou.aliyuncs.com/onlinejudge/judge_server
docker pull registry.cn-hangzhou.aliyuncs.com/onlinejudge/oj_backend
```
之后运行`docker-compose up -d`即可 

如果还有任何问题，请提出issue。 
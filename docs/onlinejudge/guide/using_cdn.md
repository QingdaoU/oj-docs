# 使用内容分发网络(CDN)

OJ目前仅支持对 Javascript 和 CSS 使用 CDN 加速，即 API 和动态加载的组件依然会从源主机请求，配置很简单，只需修改 OnlineJudgeDeploy 下的 `docker-compose.yml` 文件，将`STATIC_CDN_HOST`设置为自己的 CDN 域名:

```
 - STATIC_CDN_HOST=cdn.oj.com
```

保存并运行 `docker-compose up -d`即可。
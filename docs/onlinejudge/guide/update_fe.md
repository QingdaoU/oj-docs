# 修改前端

参考 https://github.com/QingdaoU/OnlineJudgefe 进行开发和构建

然后 `npm run build` 就可以得到一个 dist 文件夹，文件结构如下

```
➜  OnlineJudgeFE git:(master) ✗ tree dist
dist
├── admin
│   └── index.html
├── index.html
└── static
    ├── css
    │   ├── admin.127f3da5b09451926728de2829ebb32e.css
    │   ├── loader.css
    │   ├── oj.0ba722f43ddbeb758cde2f9dc804455e.css
    │   └── vendor.f033d6c4c74b6b40e92ca86f168fd0be.css
    ├── fonts
    │   ├── KaTeX_AMS-Regular.3d8245d.woff2
    │   ├── KaTeX_AMS-Regular.ac1d46d.woff

....
....

```

将 `dist` 文件夹复制到服务器上某个目录下，比如 `/data/OnlineJudgeDeploy/data/backend/dist`，然后修改 `docker-compose.yml`，在 `oj-backend` 模块中的 `volumes` 中增加一行 `- /data/OnlineJudgeDeploy/data/backend/dist:/app/dist` （冒号前面的请修改为实际的路径），然后 `docker-compose up -d` 即可。

注意，这种修改方式将覆盖容器内的前端文件，未来发布新版本前端的时候，请自行使用相同的方式更新。
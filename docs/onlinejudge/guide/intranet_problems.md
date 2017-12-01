# 内网运行的问题

OJ的MathJax是从cdn加载的，因此若是在网络隔离的环境运行，将无法无法使用MathJax显示数学公式

> 为何不将Mathjax打包进OJ?
>
> 因为实在太大了。:(

如果确实需要使用呢？

+ 使用图片代替
+ 在本地安装Mathjax, 然后修改前端代码i将mathjax的请求地址改为本地，再重新build镜像，修改`docker-compose.yml`文件启动即可
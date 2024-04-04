# HTTPS 相关问题

OnlineJudge 强烈推荐使用 HTTPS 协议

  - 数据传输加密，提高安全性，防劫持
  - 可以使用 HTTP2，加快访问速度（默认配置）

OnlineJudge 的部署脚本默认情况下会生成一个自签名证书，浏览器会提示不信任，可以自己去申请对应域名的可信证书，OnlineJudge 也提供了下面两个特性方便 HTTPS 证书的申请和使用。

## 申请 HTTPS 证书

`/.well-known` 的 url 前缀，会自动使用 `data/backend/ssl/.well-known` 目录下面的文件，默认情况下 `data/backend/ssl/` 已经存在，所以可以手动的创建 `.well-known` 及其子文件夹，比如需要 url 为 `/.well-known/pki-validation/fileauth.txt` 的验证文件，就可以创建 `data/backend/ssl/.well-known/pki-validation/fileauth.txt` 文件，内容为指定的内容。

然后替换 `data/backend/ssl/` 下面的证书和私钥文件，之后 `docker exec -it oj-backend sh -c "cd /app/deploy; supervisorctl restart nginx"`。

## FORCE_HTTPS

如果 HTTPS 配置成功，为了增强安全性，推荐重定向 HTTP 流量到 HTTPS 流量，这时候可以取消注释 `docker-compose.yml` 文件中的 `FORCE_HTTPS=1` 这一行，然后 `docker-compose up -d` 重启即可。
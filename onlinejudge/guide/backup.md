# 数据备份和恢复

## 如何备份

为了保证数据安全，请定期备份。

OnlineJudgeDeploy 目录中的 `data` 文件夹是系统的所有的数据，包括日志，数据库，测试用例，上传的文件等，其中需要备份的数据为 `backend/public`，`backend/test_case` 两个目录。

**对于数据库，请不要使用复制数据库数据文件的方法**。在最新的 OnlineJudgeDeploy 中，`backup` 目录提供了数据库导出 sql 文件备份脚本，请每次备份后检查生成的 sql 文件的大小和内容，确保备份成功。

请不要把备份数据和 OnlineJudge 系统放在同一台机器上，这样数据丢失的风险仍然较高。

## 恢复备份

如果只是想不同机器之间迁移部署，`docker stop $(docker ps -aq)` 然后复制 `OnlineJudgeDeploy` 文件夹到新机器后重新 `docker-compose up -d` 即可。

如果要恢复数据，首先要保证已经新部署了一套 OnlineJudge，然后需要恢复数据和测试用例文件。

测试用例存储在 `data/backend/test_case` 文件夹中，覆盖即可。

在新的机器上执行下面的操作可以恢复数据库

 - `docker cp db_backup_xxxxxxx.sql oj-postgres:/root`
 - `docker exec -it oj-postgres bash`
 - `psql -U postgres` 然后运行 `drop database onlinejudge;` (**请一定注意！！！看清楚自己再哪台机器上**）
 - `\q` 退出，然后 `psql -f /root/db_backup_xxxxxxx.sql -U postgres`


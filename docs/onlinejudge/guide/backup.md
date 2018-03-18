# 数据备份

为了保证数据安全，请定期备份。

OnlineJudgeDeploy 目录中的 `data` 文件夹是系统的所有的数据，包括日志，数据库，测试用例，上传的文件等，其中需要备份的数据为 `backend/public`，`backend/test_case` 两个目录。

** 对于数据库，请不要使用复制数据库数据文件的方法 **，在最新的 OnlineJudgeDeploy 中，`backup` 目录提供了数据库导出 sql 文件备份脚本，请每次备份后检查生成的 sql 文件的大小和内容，确保备份成功。

请不要把备份数据和 OnlineJudge 系统放在同一台机器上，这样数据丢失的风险仍然较高。
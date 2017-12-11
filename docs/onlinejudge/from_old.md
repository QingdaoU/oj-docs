# 从旧版迁移

## 迁移说明

由于2.0版和旧版数据库结构差别很大，新版将无法完全兼容旧版数据。若您无法承受这样的变化，请调整下自己的心态或继续使用旧版。

仅可迁移`problem`, `problemtag`, `user`三张表，迁移后的数据改动为：

### user表

+ 被导入用户的 `ac_number`, `submition_number` 将被置为0
+ 之前是的用户权限依然保持，但admin的 `problem permission` 都被设为了 `own`
+ 如果用户的 `email` 是无效的(一般是临时生成的比赛用户)，将不会被导入
+ 与已有用户重名的将不会被导入

### problemtag表

将会被全部正常导入

### problem表

+ 被导入的problem的统计信息都是初始状态
+ 被导入的problem `languages`被设置为了`["C", "C++"]`
+ 被导入的problem的`difficulty`都被设置为了`Mid`
+ problem的创建时间，创建者等信息保持不变
+ 导入过程需要输入一个前缀,这个前缀是导入的problem的Display ID的前缀，比如输入`old`,则导入的problem的Display ID将为`old1`、`old2`、`old2`...
+ 与已有的`Display ID`重复的problem不会被导入

!> 请务必仔细阅读上述迁移情况并做好数据备份，做好数据备份，做好数据备份！！！

## 迁移过程:

!> 本教程仅针对使用官方 `OnlineJudgeDeploy` 搭建的OJ，其他方式搭建的请自行迁移

一下教程要求新版和旧版均能正常使用，且新版更新到了最新版本,否则可能导致导入失败

### 备份2.0的数据库

备份数据库最简单的就是直接备份数据库文件: 在2.0的`OnlineJudgeDeploy`目录下, 运行

```bash
cp -r data data_bak
```

这样就完成了备份，当导入出现问题时，可以将`data`目录删除，再将`data_bak`复制回去就行了

### 准备1.0数据

+ 数据库数据
    在1.0的机器上运行
    ```bash
    docker exec -it oj_web_server python manage.py dumpdata problem account.user --indent 2 > old_data.json
    ```

    正常情况下，你就会在本目录看到一个名为`old_data.json`的文件。下面的步骤均需要使用的该文件。

+ test_cases

    在1.0的`OnlineJudgeDeploy`目录下的 `/data/test_case`存放的是所有1.0的测试用例数据，你需要手动将所有测试用例复制到新版的`OnlineJudgeDeploy/data/backend/test_case`下，可以使用
    ```bash
    zip -r test_case.zip test_case
    ```
    打包成zip方便复制，确保进行下面的步骤前已经移动完成

### 运行导入脚本

将上述`old_data.json` 复制到2.0的机器上，确保当前目录下有`old_data.json`这个文件，然后依次运行:

```bash
docker cp old_data.json oj-backend:/app/utils/ 
docker exec -it oj-backend /bin/sh
cd utils
python3 migrate_data.py old_data.json
```

然后根据脚本提示导入即可完成导入，导入后可进入后台查看导入情况

如有问题，请issue或在讨论群寻求帮助

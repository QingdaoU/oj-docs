# 修改编译选项

```
docker exec -it oj-backend sh

python3 manage.py shell

from options.options import *
print(SysOptions.languages)
```

这是系统使用的语言和编译器信息和编译选项，是 `judge/languages.py` 的拷贝，如果只修改 py 文件，是不会生效的。需要运行 

```
SysOptions.reset_languages()
```

更新数据库。

这样以后系统更新了，py 文件可能会被覆盖，但是数据库的值还是修改过的。所以还请自行备份修改过的配置。

这个配置文件的内容和格式要怎么修改请先自行探索或者询问开发者，文档以后再写。

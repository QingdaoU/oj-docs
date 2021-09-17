# 导入用户

目前仅支持的`csv`格式的文件导入, csv文件既可以用文本编辑器创建，也可以用Excel等软件来辅助创建

要求csv文件不带头, 共四列: 用户名，密码，邮箱，真实姓名。不带头的意思是第一列不必写(用户名，密码这类词)
请保存为`UTF-8`编码的文件，否则中文可能会乱码

+ 使用文本编辑器

```bash
$ cat users.csv 
user1,password1,test@qduoj.com,李明
user2,passwd2,tt@qduoj.com,anonymous
```

这将创建两个用户， user1 密码为password1, 邮箱 test@qduoj.com； user2 密码passwd2,邮箱 tt@qduoj.com

**注意，真实姓名这一列是在 2021.08 的版本中支持的，在此版本中，缺少这一列将导致导入失败。**

+ 使用Excel等

只需按顺序填入数据，保存时保存为csv格式文件即可:
![users](https://user-images.githubusercontent.com/20637881/33434820-6faa6154-d61b-11e7-9198-4317a71afa43.png)

![save_users](https://user-images.githubusercontent.com/20637881/33434823-703de26c-d61b-11e7-8fd4-ddc7563471a0.png)

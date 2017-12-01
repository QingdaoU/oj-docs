# 测试用例格式

对于普通题目，测试用例文件包括`in`和`out`两种拓展名，对于Special Judge就只有`in`一种文件。

压缩时，请将文件都放在压缩包的根目录，而不是包含在某一个文件夹中，比如正确的格式是

```bash
➜  testcase pwd
/tmp/testcase
➜  testcase tree
.
├── 1.in
├── 1.out

0 directories, 2 files
```

下面是错误的，

```bash
➜  testcase pwd
/tmp/testcase
➜  testcase tree
.
├── 1
│   ├── 1.in
│   └── 1.out

1 directories, 2 files
```

然后压缩测试用例到一个zip中

```bash
➜  testcase zip testcase.zip ./{*.in,*.out}
  adding: 1.in (stored 0%)
  adding: 1.out (stored 0%)
```

查看压缩包的内容

```bash
➜  testcase unzip -v testcase.zip
Archive:  testcase.zip
 Length   Method    Size  Ratio   Date   Time   CRC-32    Name
--------  ------  ------- -----   ----   ----   ------    ----
       0  Stored        0   0%  04-28-16 16:27  00000000  1.in
       0  Stored        0   0%  04-28-16 16:27  00000000  1.out
--------          -------  ---                            -------
       0                0   0%                            2 files
```

如果是在图形界面下压缩，请选中需要压缩的文件，右键直接压缩就可以。

如果认为正确压缩了，但是还提示文件格式或者文件数量错误，请查看是否压缩进去了隐藏文件，Windows下可能是`$RECYCLE.BIN`等，Mac下是`.DS_Store`，Linux下可能是`1.in~`或者`.1.in.swp`文件。

同时建议尽量合并测试用例到一个文件中，减少测试用例组数，这会一定程度上提高判题性能，降低选手代码运行时间
# Testcase format

Each testcase directory contains its testcase files, the conetent of input files will be redirected to stdin, and stdout of process will be compared with output files(normal problem) or judged by your special judge code(special judge).

Testcase meta data is in `info` file.

## Normal problem

Both input and output files are required.

```
root@JudgeServer:~/test_case/normal# tree
.
|-- 1.in
|-- 1.out
`-- info

0 directories, 3 files
root@JudgeServer:~/test_case/normal# cat 1.in
1 2
root@JudgeServer:~/test_case/normal# cat 1.out
3
```

Example of `info` file

 - spj: for normal problem, it is `false`
 - test_cases: `name` - `data` dict
     - stripped_output_md5: md5 of output file which trailing empty characters has been removed
     - input_name and output_name: name of input and output file
     - input_size and output_size: size of input and output file

```js
{
    "spj": false,
    "test_cases": {
        "1": {
            "stripped_output_md5": "eccbc87e4b5ce2fe28308fd9f2a7baf3",
            "output_size": 2,
            "input_name": "1.in",
            "input_size": 4,
            "output_name": "1.out"
        }
    }
}

```

## Special Judge

You only need input files.

```
root@JudgeServer:~/test_case/spj# tree
.
|-- 1.in
`-- info

0 directories, 3 files
root@JudgeServer:~/test_case/normal# cat 1.in
1 2
```

Example of `info` file

 - spj: for special judge problem, it is `true`
 - test_cases: `name` - `data` dict
     - input_name: name of input file
     - input_size: size of input file

```js
{
    "spj": true,
    "test_cases": {
        "1": {
            "input_name": "1.in",
            "input_size": 4
        }
    }
}
```

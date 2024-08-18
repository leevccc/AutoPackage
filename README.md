# AutoPackage 自动打包

## 使用方法
**初始化**

拷贝项目到本地

```shell
git clone 
```

初始化 version.json 文件内容
```json
{
  "version": "0.0.0",
  "main": "GMSE",
  "feat": [],
  "update": [],
  "bug": [],
  "comment": "初始化客户端"
}
```

在项目根目录下创建两个文件夹
- data
- package

将客户端文件放入 data 目录

执行 package.py 即可

**后续使用**

客户端修改请在data目录下进行

更改客户端时，将更改记录写入到version.json相应位置，
打包时会根据version里的记录生成更新日志放在客户端中，并且会自动更新version版本号。

版本号由 主版本.子版本.修复数 组成。
- 填写main信息（留""视为未填），主版本+1；
- 填写feat/update记录，子版本增加（记录数）
- 填写bug记录，修复数增加（记录数）

**注意**

package目录里的data文件是用来比较文件是否发生变化用的，请勿删除或者修改，其他文件夹可自行删除。
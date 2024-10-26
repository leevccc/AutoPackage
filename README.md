# AutoPackage 自动打包

## 使用方法
**初始化**

1 拷贝项目到本地

```shell
git clone https://github.com/leevccc/AutoPackage.git
```

2 在项目根目录下创建 `data` 和 `package` 两个文件夹

3 将客户端文件放入 data 目录

4 **复制** version.demo 文件为 version.json

5 编辑 version.json 参考下文

6 编辑基本配置 参考下文

7 执行 package.py 进行初始化打包

**后续使用**

修改客户端，请在 `data` 目录下进行

更改客户端时，将更改记录写入到 `version.json` 相应位置，需要打包时，执行 package.py 即可

## 文件说明
### version.json

版本号由 主版本.子版本.修复数 组成，脚本会自动维护，如非必要请勿手动修改。
- **main** 字符串，如不为""，打包时主版本+1；
- **feat/update** 数组，可填写多条更新记录，打包时子版本+记录数
- **bug** 数组，可填写多条修复记录，打包时修复数+记录数
- **comment** 字符串，如为""，打包时，更新日志不会填写备注信息

**请注意**

如果 main/feat/update/bug 均无记录，则视为没有更新记录，不会进行打包。

每次打包完成后，脚本会自动更新 version 并清空 main/feat/update/bug/comment 记录

### data 目录
须自行创建，存放及修改客户端均在此目录进行

### package 目录
须自行创建，存放输出文件

package/data 存放上个版本的客户端文件，用来比较文件是否发生变化用的，请勿删除或者修改。**每次打包完成可自行压缩此文件夹进行发布**。

package下的其他文件夹为补丁文件夹，可自行压缩发布及删除。 

## 基本配置
在 package.py 中，有三个变量需配置

- `client_name` 客户端名称，仅开启压缩服务时有效
- `use_bandi_zip` 压缩服务，打包后自动生成压缩包，仅安装了 BandZip 程序时可用，如果没有安装请设置为 **False**
- `delete_patch_dir_after_zip` 压缩完成后自动删除补丁文件夹

## 文件过滤
重命名filter.demo为filter.json，然后自行填写需要过滤的文件名，只支持文件。
---
title: svn迁移到git
categories:
  - area
tags:
publish: true
date: 2025-07-08 14:15:43
lastmod: 2025-12-18 17:31:14
---
>操作环境：`Ubuntu 18`

# 1. 整理SVN和Git账号的关联关系

关联关系的格式为：
`SVN账号 = Git账号 <Git中的邮箱>`

整理之后，写入`user.txt`，如下：
```plaintext
zhangs = zhangsan <zhansan@gitlab.com>
li4 = li4 <li4@gitlab.com>
```


# 2. 在gitlab中建立相应的工程

建立空白工程后，得到对应远程仓库地址 [http://192.168.0.200/xxxx/test.git](http://192.168.0.200/xxxx/test.git)

# 3. Git-SVN
## 3.1. 安装Git-SVN

```bash
apt install -y git-svn
```

## 3.2. 拉取SVN至Git工程

```bash
git svn clone svn://xxx/test --no-metadata --authors-file=user.txt
```

# 4. 推送至远端Git仓库

```bash
cd test
git remote add origin http://192.168.0.200/xxxx/test.git
git push -u origin master
```
完事

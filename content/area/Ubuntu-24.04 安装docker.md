---
title: Ubuntu-24.04 安装docker
categories:
  - area
tags:
  - 工具折腾
  - linux
publish: true
date: 2024-09-04 17:32:22
lastmod: 2024-10-08 11:24:50
---
# 1. 安装

> 参考[清华源说明](https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce/)


## 1.1. 卸载老版本

```bash
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```



## 1.2. 首先安装依赖

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
```



## 1.3. 信任 Docker 的 GPG 公钥并添加仓库

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```



## 1.4. 安装

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin	
```



## 1.5. 启动docker

```bash
sudo systemctl enable docker
sudo systemctl start docker
```



# 2. 添加国内镜像源
> 参考：[CSDN博客](https://blog.csdn.net/tiffany_263/article/details/140288631)

## 2.1. 修改文件 /etc/docker/daemon.json

（如果不存在则创建）

```bash
sudo mkdir -p /etc/docker
```



## 2.2. 换源

```bash
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": [
 	"https://dockerpull.com",
	"https://docker.1panel.live",
	"https://dockerproxy.cn",
	"https://docker.hpcloud.cloud"
  ]
}
EOF
```



## 2.3. 重启

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```



## 2.4. 拉取镜像

```bash
sudo docker pull dockerpull.com/library/openjdk:8
```

> **说明：**`library`是一个特殊的命名空间，它代表的是官方镜像。如果是某个用户的镜像就把library替换为镜像的用户名
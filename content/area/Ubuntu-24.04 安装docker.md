---
title: Ubuntu-24.04 安装docker
categories:
  - area
tags:
  - linux
publish: true
date: 2024-09-04 17:32:22
lastmod: 2025-04-02 15:59:50
---
# 1. 安装

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


## 2.1. 修改文件 /etc/docker/daemon.json

（如果不存在则创建）

```bash
sudo mkdir -p /etc/docker
```



## 2.2. 换源

```bash
echo '{
  "registry-mirrors": [
    "https://docker.1ms.run",
    "https://docker.1panel.live",
    "https://docker.m.daocloud.io"
  ]
}' | sudo tee /etc/docker/daemon.json
```

重启生效

```bash
sudo systemctl restart docker
```

# 3. 参考

> 1. [Ubuntu 下 Docker安装 2024](https://blog.csdn.net/tiffany_263/article/details/140288631)
> 2. [国内 Docker 服务状态 & 镜像加速监控](https://status.1panel.top/status/docker)
> 3. [清华源说明](https://mirrors.tuna.tsinghua.edu.cn/help/docker-ce/)


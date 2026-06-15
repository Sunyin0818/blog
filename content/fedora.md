---
title: fedora
date: 2026-04-08 10:10:28
lastmod: 2026-06-15 16:49:06
publish: true
tags:
  - AIO
  - fedora
---
> 机型：`零刻 SER6 Pro VEST`
> 配置：`32G+2T`
> 镜像：`Fedora-Workstation-Live-43-1.6.x86_64.iso`

## 1. 基本配置

### 1.1. 镜像源

如果你的网络环境不太好/节省流量，可以使用 USTC（或 TUNA）的国内镜像源：

```bash
sudo sed -e 's|^metalink=|#metalink=|g' \
         -e 's|^#baseurl=http://download.example/pub/fedora/linux|baseurl=https://mirrors.ustc.edu.cn/fedora|g' \
         -i.bak \
         /etc/yum.repos.d/fedora.repo \
         /etc/yum.repos.d/fedora-updates.repo

# RPMFusion
sudo dnf install https://mirrors.ustc.edu.cn/rpmfusion/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://mirrors.ustc.edu.cn/rpmfusion/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm

# refresh cache
sudo dnf clean all
sudo dnf makecache

# flathub 缓存镜像源
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
sudo flatpak remote-modify flathub --url=https://mirrors.ustc.edu.cn/flathub
```

进行一次软件包更新

```bash
sudo dnf upgrade --refresh
```

### 1.2. 更改主机名

更改主机名为 `fedora`

```bash
sudo hostnamectl set-hostname fedora
```
### 1.3. `home`目录保持英文

> 否则在终端输入中文目录会很痛苦


```bash
export LANG=en_US
xdg-user-dirs-gtk-update
```
在询问是否将目录转化为英文的窗口中选择同意

然后使用命令将系统语言转化为中文

```bash
epxort LANG=zh_CN
xdg-user-dirs-gtk-update
```

提示是是否把英文目录转化为中文，选择不同意，并勾选不再提示。

### 1.4. 一些优化

让 NetworkManager 别等了：

```bash
sudo systemctl disable NetworkManager-wait-online.service
sudo systemctl mask NetworkManager-wait-online.service
```

软件中心别吵我：

```bash
gsettings set org.gnome.software download-updates false
gsettings set org.gnome.software download-updates-notify false
```

关闭资源管理器记住最近文件：

```bash
gsettings set org.gnome.desktop.privacy remember-recent-files false
```

### 1.5. 中文输入法

GNOME 默认自带中文输入法，勉强一用。这里使用 Fcitx5 输入框架和 Rime 输入引擎，输入方案选择 [雾凇拼音](https://github.com/iDvel/rime-ice) 。

```bash
sudo dnf install fcitx5 fcitx5-gtk fcitx5-qt fcitx5-rime librime-lua fcitx5-configtool
```

下载雾凇拼音输入方案

```bash
git clone https://github.com/iDvel/rime-ice.git ~/.local/share/fcitx5/rime --depth=1
```

添加中州韵输入法

```bash
fcitx5-configtool
```

PS：GNOME 需要安装插件 [kimpanel](https://extensions.gnome.org/extension/261/kimpanel/) 后，才能在状态栏正常显示托盘图标（包括输入法指示器）。

### 1.6. 针对频繁的权限弹窗

```bash
sudo tee /etc/polkit-1/rules.d/00-admin-override.rules <<EOF
polkit.addRule(function(action, subject) {
    if (subject.isInGroup("wheel")) {
        return polkit.Result.YES;
    }
});
EOF
sudo chmod 644 /etc/polkit-1/rules.d/00-admin-override.rules
```

这个操作本质上是**将图形界面的安全性下放到与 `sudo` 同等的水平**。注意良好的使用习惯，不安装不明来源的软件。不过，都用fedora了，我觉得也没必要提这个。


### 1.7. 更新固件

通过 LVFS (Linux Vendor Firmware Service) 更新硬件设备固件

```bash
fwupdmgr refresh --force
fwupdmgr get-updates
fwupdmgr update
```

### 1.8. 禁用网络连通性检测

开启了 Tun 模式后，会影响系统的网络连通性检测，表现为

![image-2bd6cd78-5097-4339-a2ea-5ac77aef491a.webp](Assets/image-2bd6cd78-5097-4339-a2ea-5ac77aef491a.webp)

不影响使用，但是看着很难受，所以把网络连通性检测关闭

```bash
sudo vim /etc/NetworkManager/conf.d/90-disable-connectivity.conf
```

添加

```toml
[connectivity]
enabled=false
```

重启 NetworkManager 服务

```bash
sudo systemctl restart NetworkManager
```

现在舒服多了

![image-206a7187-dab4-49fe-b4b2-66f27a540dd6.webp](Assets/image-206a7187-dab4-49fe-b4b2-66f27a540dd6.webp)

## 2. 美化调整

### 2.1. GNOME 插件和优化

```bash
sudo dnf install gnome-extensions-app gnome-tweaks
```

![image-be75faf4-37a9-465c-b569-31d571cf20e8.jpg](Assets/image-be75faf4-37a9-465c-b569-31d571cf20e8.jpg)


### 2.2. 安装字体

```bash
# 习惯使用starship 搭配食用
sudo dnf install cascadia-mono-nf-fonts
# 补充Inter
sudo dnf install rsms-inter-fonts
# 刷新字体缓存
fc-cache -fv
```

安装[`MapleMono-NF-CN`](https://github.com/subframe7536/maple-font/releases)，手动下载到 `~/Downloads`
```bash
# 安装MapleMono-NF-CN
unzip MapleMono-NF-CN*.zip -d MapleMono

# 2. 创建用户字体目录（如果不存在）
mkdir -p ~/.local/share/fonts/MapleMono

# 3. 将字体移动到该目录
cp MapleMono/*.ttf ~/.local/share/fonts/MapleMono/

# 4. 刷新系统字体缓存
fc-cache -fv
```

## 3. 安装常用软件

### 3.1. zsh
#### 3.1.1. 安装zsh
在 Fedora 终端执行以下命令，确保基础工具链完整：
```bash
sudo dnf install -y zsh git util-linux-user
chsh -s $(which zsh)
```

#### 3.1.2. Oh My Zsh

##### 3.1.2.1. 安装 

```Bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```
##### 3.1.2.2. 插件

```Bash
# 自动建议建议 (Suggestions)
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# 语法高亮 (Highlighting)
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# 深度补全 (Completions)
git clone https://github.com/zsh-users/zsh-completions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-completions
```

##### 3.1.2.3. starship

个人习惯使用[starship](https://starship.rs/zh-CN/guide/) ，各平台外观一致

```bash
dnf copr enable atim/starship
dnf install starship
```

##### 3.1.2.4. 配置文件 (~/.zshrc) 

请根据你的路径修改以下源码并覆盖至 ~/.zshrc：

```Bash
# --- [1] 初始化补全路径 (必须放在最前面) ---
fpath+=${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/zsh-completions/src

# --- [2] Oh My Zsh 路径设置 ---
export ZSH="$HOME/.oh-my-zsh"

# --- [3] 主题设置 (我使用starship) ---
# 推荐使用 Powerlevel10k 或 robbyrussell
# ZSH_THEME="robbyrussell"

# --- [4] 插件配置 (功能互补) ---
plugins=(
  git
  sudo               # 双击 Esc 自动加 sudo
  extract            # 万能解压: extract filename
  sdk                # SDKMAN 补全支持
  colored-man-pages  # 彩色帮助手册
  zsh-autosuggestions 
  zsh-syntax-highlighting 
  zsh-completions
)

source $ZSH/oh-my-zsh.sh

# --- [5] 环境变量迁移 (来自 .bashrc) ---
# 基础 PATH
export PATH="$HOME/.local/bin:$HOME/bin:/home/sunyin/.opencode/bin:$PATH"

# --- [6] Starship 初始化 ---
eval "$(starship init zsh)"
```

### 3.2. Google Chrome

```bash
sudo dnf config-manager setopt google-chrome.enabled=1
sudo dnf install google-chrome-stable
```
### 3.3. Clash Verge

手动下载 rpm包安装 [clash-verge-rev](https://github.com/clash-verge-rev/clash-verge-rev)

### 3.4. Docker

```bash
sudo dnf config-manager addrepo --from-repofile https://download.docker.com/linux/fedora/docker-ce.repo
sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
```

### 3.5. VSCode

```bash
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc &&
echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\nautorefresh=1\ntype=rpm-md\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null
sudo dnf check-update
sudo dnf install code
```

### 3.6. Antigravity

```bash
sudo tee /etc/yum.repos.d/antigravity.repo << EOL
[antigravity-rpm]
name=Antigravity RPM Repository
baseurl=https://us-central1-yum.pkg.dev/projects/antigravity-auto-updater-dev/antigravity-rpm
enabled=1
gpgcheck=0
EOL
sudo dnf makecache
sudo dnf install antigravity
```
### 3.7. Firewall GUI

这是 Fedora 官方推荐的防火墙可视化管理工具

```bash
sudo dnf install firewall-config
```
### 3.8. Flatpak

以下建议通过flatpak安装

+ **Linux QQ** -  QQ NT
	```bash
	flatpak install com.qq.QQ
	``` 
	
+ **WeChat** - WeChat NT
	```bash
	flatpak install com.tencent.WeChat
	```
	
+ **Telegram** 
	```bash
	flatpak install org.telegram.desktop
	```
	
+ **Obsidian**
    ```bash
    flatpak install md.obsidian.Obsidian
    ```
  
+ **LocalSend** - 局域网文件传输工具
	```bash
	flatpak install org.localsend.localsend_app
	```

# 参考

[Fedora Linux 安装配置记录](https://blog.dejavu.moe/posts/install-and-use-fedora-workstation/)


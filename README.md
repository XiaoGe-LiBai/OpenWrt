<div align="center">
<img width="768" src="https://cdn.jsdelivr.net/gh/JejzOne/Picture/OpenWrt-logo.png"/>
<h1>OpenWrt — Actions</h1>
</div>

-  [**群组**](https://t.me/Jejz_168)
-  🛑******最好全新刷机（加入快捷改IP的ssh命令：JejzWrt）******
-  ♨️【x86】Docker版（Kernel=32M，rootfs=5120M）和 无Docker版（Kernel=32M，rootfs=1668M）不通刷
-  本库x86为squashfs格式。
-  ext4 与squashfs 格式的区别： ext4 格式的rootfs 可以扩展磁盘空间大小，而squashfs 不能。 squashfs 格式的rootfs 可以使用重置功能（恢复出厂设置），而ext4 不能。
-  *必须要是本库最新才能使用。不然就会死翘翘。
-  升级方法：下载好对应的版本（.img.gz），然后（openwrt-系统-备份/升级） *直接选择，不用解压
# ==============================
## 项目说明 [![](https://img.shields.io/badge/-项目基本介绍-FFFFFF.svg)](#项目说明-)
- 固件来源：[![Lean](https://img.shields.io/badge/Lede-Lean-red.svg?style=flat&logo=appveyor)](https://github.com/coolsnowwolf/lede) 
- 项目使用 Github Actions 拉取 [Lean](https://github.com/coolsnowwolf/lede) [immortalwrt](https://github.com/immortalwrt/immortalwrt) [openwrt](https://github.com/openwrt/openwrt) 的 `Openwrt` 源码仓库进行云编译
- ♨️【x86】Docker版（Kernel=32M，rootfs=5120M）和 无Docker版（Kernel=32M，rootfs=1668M）不通刷
- 🔴arm 固件默认 IP 地址：`192.168.8.8` 默认密码：`password`
- 🔴x86 固件默认 IP 地址：`192.168.2.240` 默认密码：`无密码`
- 🔴x86[Docker] 固件默认 IP 地址：`192.168.2.240` 默认密码：`无密码`
- 🔴x86[个人版] 固件默认 IP 地址：`192.168.2.241` 默认密码：`无密码`
- 仓库编译的固件插件均为最新版本，最新版意味着可能有 BUG，如果之前使用稳定，则无需追新

## 插件预览 [![](https://img.shields.io/badge/-固件插件及功能预览-FFFFFF.svg)](#插件预览-)
- **标记为 (arm) 的菜单仅出现在 ARM 固件中**
<details>
<summary><b>菜单结构（与 disable_plugins.py 保持一致）</b></summary>

```text
实际顺序
├── 状态
│   ├── 概况（overview）
│   ├── 路由（routes）
│   ├── 防火墙（nftables）
│   ├── 系统日志（logs）
│   ├── 系统进程（processes）
│   ├── 实时信息（realtime）
│   ├── WireGuard状态（wireguard-status）
│   ├── WireGuard配置（wireguard-config）
│   └── 释放内存（ramfree）
├── 系统
│   ├── 系统（system）
│   ├── 管理权（admin）
│   ├── TTYD 终端（ttyd）
│   ├── 软件包（package-manager）
│   ├── 启动项（startup）
│   ├── 计划任务（crontab）
│   ├── 挂载点（mounts）
│   ├── 备份与更新（flash）
│   ├── 文件管理器（filemanager）
│   ├── 定时重启（autoreboot）
│   ├── Argon 设置（argon-config）
│   ├── KuCat 设置（kucat-config）
│   ├── 重启（reboot）
│   └── 关机（poweroff）
├── 服务
│   ├── PassWall（passwall）
│   ├── PassWall2 (arm)（passwall2-arm）
│   ├── HomeProxy（homeproxy）
│   ├── ShadowSocksR Plus+（shadowsocksr）
│   ├── 看门狗（watchdog）
│   ├── AdGuard Home（adguardhome）
│   ├── MosDNS（mosdns）
│   ├── 全能推送（pushbot）
│   ├── OpenClash（openclash）
│   ├── Lucky（lucky）
│   ├── 动态 DNS（ddns）
│   ├── DDNSTO 远程控制（ddnsto）
│   ├── SmartDNS（smartdns）
│   ├── 网络唤醒（wol）
│   ├── Nps 内网穿透（nps）
│   ├── 应用过滤（appfilter）
│   ├── Aria2（aria2）
│   ├── Frp 客户端（frpc）
│   ├── Frp 服务端（frps）
│   ├── Momo（momo）
│   ├── Nikki（nikki）
│   ├── OpenList（openlist2）
│   ├── uHTTPd（uhttpd）
│   ├── UPnP（upnp）
│   └── Vlmcsd KMS 服务器（vlmcsd）
├── Docker (arm)
│   ├── 概览（dockerman-overview）
│   ├── 容器（dockerman-containers）
│   ├── 镜像（dockerman-images）
│   ├── 网络（dockerman-network）
│   ├── 存储卷（dockerman-volumes）
│   ├── 事件（dockerman-events）
│   └── 设置（dockerman-settings）
├── 网络存储
│   ├── USB 打印服务器（usb_printer）
│   ├── 硬盘休眠（hd_idle）
│   ├── p910nd-打印服务器（p910nd）
│   ├── 网络共享（samba4）
│   └── FTP 服务器（vsftpd）
├── VPN
│   ├── IPSec VPN 服务器（ipsec-vpnd）
│   ├── SoftEther VPN 服务器（softethervpn）
│   ├── OpenVPN 服务器（openvpn-server）
│   ├── N2N VPN（n2n）
│   ├── Tailscale（tailscale）
│   └── ZeroTier（zerotier）
├── 网络
│   ├── 接口（network）
│   ├── 路由（routes-network）
│   ├── DHCP/DNS（dhcp）
│   ├── 网络诊断（diagnostics）
│   ├── 防火墙（firewall）
│   ├── Socat（socat）
│   ├── 多线多拨（syncdial）
│   ├── 网速控制（eqos）
│   └── MultiWAN 管理器（mwan3）
└── 带宽监控
    ├── 显示（display）
    ├── 配置（config）
    └── 备份（backup）
```

</details>

## 固件下载
**点击跳转到该设备固件下载页面**
- ♨️【x86】Docker版（Kernel=32M，rootfs=5120M）和普通（Kernel=32M，rootfs=1668M）不通刷
- [**X86下载地址**](https://github.com/JejzOne/OpenWrt/releases)
- [**Arm下载地址**](https://github.com/JejzOne/OpenWrt/releases/tag/ARMv8)

## 鸣谢 [![](https://img.shields.io/badge/-跪谢各大佬-FFFFFF.svg)](#鸣谢-)
| [ImmortalWrt](https://github.com/immortalwrt) | [coolsnowwolf](https://github.com/coolsnowwolf) | [P3TERX](https://github.com/P3TERX) | [Flippy](https://github.com/unifreq) | [haiibo](https://github.com/haiibo) | [Lenyu2020](https://github.com/Lenyu2020) |
| :-------------: | :-------------: | :-------------: | :-------------: | :-------------: | :-------------: |
| <img width="100" src="https://avatars.githubusercontent.com/u/53193414"/> | <img width="100" src="https://avatars.githubusercontent.com/u/31687149"/> | <img width="100" src="https://avatars.githubusercontent.com/u/25927179"/> | <img width="100" src="https://avatars.githubusercontent.com/u/39355261"/> | <img width="100" src="https://avatars.githubusercontent.com/u/85640068"/> | <img width="100" src="https://avatars.githubusercontent.com/u/59961153"/> |
| [Ophub](https://github.com/ophub) | [Jerrykuku](https://github.com/jerrykuku) | [QiuSimons](https://github.com/QiuSimons) | [IvanSolis1989](https://github.com/IvanSolis1989) | [DHDAXCW](https://github.com/DHDAXCW) | [breakings](https://github.com/breakings) |
| <img width="100" src="https://avatars.githubusercontent.com/u/68696949"/> | <img width="100" src="https://avatars.githubusercontent.com/u/9485680"/> | <img width="100" src="https://avatars.githubusercontent.com/u/45143996"/> | <img width="100" src="https://avatars.githubusercontent.com/u/44228691"/> | <img width="100" src="https://avatars.githubusercontent.com/u/74764072"/> | <img width="100" src="https://avatars.githubusercontent.com/u/25475074"/> |


# 访问量

![](https://komarev.com/ghpvc/?username=JejzOne&color=orange&style=for-the-badge)
# ==============================
# 🏖Special thanks（特别感谢）
- [GitHub Actions](https://github.com/features/actions)🎉🎉Thank you very much.🎉🎉



<a href="#readme">
<img src="https://img.shields.io/badge/-返回顶部-FFFFFF.svg" title="返回顶部" align="right"/>
</a>

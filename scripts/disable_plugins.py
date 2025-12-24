#!/usr/bin/env python3
"""\
批量禁用（或启用） OpenWrt defconfig 中的特定插件/依赖项，
并提供与实际 LuCI 界面一致的菜单顺序，便于核对 README。
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List

SECTION_DEFINITIONS = [
    {
        "name": "状态",
        "items": [
            # {
            #     "slug": "overview",
            #     "display": "概况",
            #     "description": "LuCI 概况仪表盘（核心功能，仅记录）。",
            # },
            # {
            #     "slug": "routes",
            #     "display": "路由",
            #     "description": "LuCI 路由信息（核心功能，仅记录）。",
            # },
            # {
            #     "slug": "nftables",
            #     "display": "防火墙",
            #     "description": "基于 nftables 的防火墙状态页（核心功能，仅记录）。",
            # },
            # {
            #     "slug": "logs",
            #     "display": "系统日志",
            #     "description": "系统/内核日志查看（核心功能，仅记录）。",
            # },
            # {
            #     "slug": "processes",
            #     "display": "系统进程",
            #     "description": "进程列表（核心功能，仅记录）。",
            # },
            # {
            #     "slug": "realtime",
            #     "display": "实时信息",
            #     "description": "CPU/内存/网络实时信息（核心功能，仅记录）。",
            # },
            {
                "slug": "wireguard-status",
                "display": "WireGuard状态",
                "description": "WireGuard VPN 状态面板及内核依赖。",
                "prefixes": [
                    "CONFIG_PACKAGE_wireguard-tools",
                    "CONFIG_PACKAGE_kmod-wireguard",
                ],
            },
            {
                "slug": "wireguard-config",
                "display": "WireGuard配置",
                "description": "WireGuard LuCI 前端配置界面。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-wireguard",
                    "CONFIG_PACKAGE_luci-i18n-wireguard-zh-cn",
                ],
            },
            # {
            #     "slug": "ramfree",
            #     "display": "释放内存",
            #     "description": "luci-app-ramfree 释放内存插件。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-ramfree",
            #         "CONFIG_PACKAGE_luci-i18n-ramfree-zh-cn",
            #     ],
            # },
        ],
    },
    {
        "name": "系统",
        "items": [
            # {
            #     "slug": "system",
            #     "display": "系统",
            #     "description": "系统设置（核心功能，仅记录）。",
            # },
            # {
            #     "slug": "admin",
            #     "display": "管理权",
            #     "description": "管理员密码等权限配置（核心功能，仅记录）。",
            # },
            # {
            #     "slug": "ttyd",
            #     "display": "TTYD 终端",
            #     "description": "luci-app-ttyd Web 终端。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-ttyd",
            #         "CONFIG_PACKAGE_luci-i18n-ttyd-zh-cn",
            #         "CONFIG_PACKAGE_ttyd",
            #     ],
            # },
            # {
            #     "slug": "package-manager",
            #     "display": "软件包",
            #     "description": "luci-app-opkg 软件包管理器。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-opkg",
            #         "CONFIG_PACKAGE_luci-i18n-opkg-zh-cn",
            #     ],
            # },
            # {
            #     "slug": "startup",
            #     "display": "启动项",
            #     "description": "启动项管理（核心功能，仅记录）。",
            # },
            # {
            #     "slug": "crontab",
            #     "display": "计划任务",
            #     "description": "计划任务管理（核心功能，仅记录）。",
            # },
            # {
            #     "slug": "mounts",
            #     "display": "挂载点",
            #     "description": "磁盘挂载（核心功能，仅记录）。",
            # },
            # {
            #     "slug": "flash",
            #     "display": "备份与更新",
            #     "description": "固件备份/升级（核心功能，仅记录）。",
            # },
            # {
            #     "slug": "filemanager",
            #     "display": "文件管理器",
            #     "description": "luci-app-filemanager Web 文件管理器。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-filemanager",
            #         "CONFIG_PACKAGE_luci-i18n-filemanager-zh-cn",
            #     ],
            # },
            # {
            #     "slug": "autoreboot",
            #     "display": "定时重启",
            #     "description": "luci-app-autoreboot 定时重启插件。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-autoreboot",
            #         "CONFIG_PACKAGE_luci-i18n-autoreboot-zh-cn",
            #     ],
            # },
            # {
            #     "slug": "argon-config",
            #     "display": "Argon 设置",
            #     "description": "Argon 主题及 luci-app-argon-config。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-argon-config",
            #         "CONFIG_PACKAGE_luci-theme-argon",
            #     ],
            # },
            # {
            #     "slug": "kucat-config",
            #     "display": "KuCat 设置",
            #     "description": "KuCat 主题及 luci-app-kucat-config。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-kucat-config",
            #         "CONFIG_PACKAGE_luci-i18n-kucat-config-zh-cn",
            #         "CONFIG_PACKAGE_luci-theme-kucat",
            #     ],
            # },
            # {
            #     "slug": "reboot",
            #     "display": "重启",
            #     "description": "重启路由（核心功能，仅记录）。",
            # },
            # {
            #     "slug": "poweroff",
            #     "display": "关机",
            #     "description": "luci-app-poweroff 关机按钮。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-poweroff",
            #         "CONFIG_PACKAGE_luci-i18n-poweroff-zh-cn",
            #     ],
            # },
        ],
    },
    {
        "name": "服务",
        "items": [
            # {
            #     "slug": "passwall",
            #     "display": "PassWall",
            #     "description": "PassWall 多协议代理套件。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-passwall",
            #         "CONFIG_PACKAGE_luci-i18n-passwall-zh-cn",
            #     ],
            # },
            # {
            #     "slug": "passwall2-arm",
            #     "display": "PassWall2 (arm)",
            #     "description": "PassWall 第二代插件（常见于 ARM）。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-passwall2",
            #         "CONFIG_PACKAGE_luci-i18n-passwall2-zh-cn",
            #     ],
            # },
            {
                "slug": "homeproxy",
                "display": "HomeProxy",
                "description": "HomeProxy 多场景代理前端。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-homeproxy",
                    "CONFIG_PACKAGE_luci-i18n-homeproxy-zh-cn",
                ],
            },
            {
                "slug": "shadowsocksr",
                "display": "ShadowSocksR Plus+",
                "description": "SS/SSR/Xray 等多协议管理。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-ssr-plus",
                    "CONFIG_PACKAGE_luci-i18n-ssr-plus-zh-cn",
                    "CONFIG_DEFAULT_luci-app-ssr-plus",
                ],
            },
            # {
            #     "slug": "watchdog",
            #     "display": "看门狗",
            #     "description": "luci-app-watchdog 进程守护。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-watchdog",
            #         "CONFIG_PACKAGE_luci-i18n-watchdog-zh-cn",
            #     ],
            # },
            # {
            #     "slug": "adguardhome",
            #     "display": "AdGuard Home",
            #     "description": "AdGuard Home 及其 LuCI 面板。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-adguardhome",
            #         "CONFIG_PACKAGE_luci-i18n-adguardhome-zh-cn",
            #         "CONFIG_PACKAGE_adguardhome",
            #     ],
            # },
            # {
            #     "slug": "mosdns",
            #     "display": "MosDNS",
            #     "description": "MosDNS 程序与 LuCI 前端。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-mosdns",
            #         "CONFIG_PACKAGE_luci-i18n-mosdns-zh-cn",
            #         "CONFIG_PACKAGE_mosdns",
            #     ],
            # },
            # {
            #     "slug": "pushbot",
            #     "display": "全能推送",
            #     "description": "luci-app-pushbot 推送通知。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-pushbot",
            #         "CONFIG_PACKAGE_luci-i18n-pushbot-zh-cn",
            #     ],
            # },
            # {
            #     "slug": "openclash",
            #     "display": "OpenClash",
            #     "description": "OpenClash CFW 管理界面。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-openclash",
            #         "CONFIG_PACKAGE_luci-i18n-openclash-zh-cn",
            #     ],
            # },
            # {
            #     "slug": "lucky",
            #     "display": "Lucky",
            #     "description": "Lucky 多功能工具箱。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-lucky",
            #         "CONFIG_PACKAGE_luci-i18n-lucky-zh-cn",
            #     ],
            # },
            {
                "slug": "ddns",
                "display": "动态 DNS",
                "description": "luci-app-ddns 与 ddns-scripts。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-ddns",
                    "CONFIG_PACKAGE_luci-i18n-ddns-zh-cn",
                    "CONFIG_PACKAGE_ddns-scripts",
                ],
            },
            {
                "slug": "ddnsto",
                "display": "DDNSTO 远程控制",
                "description": "DDNSTO 远程穿透服务。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-ddnsto",
                    "CONFIG_PACKAGE_luci-i18n-ddnsto-zh-cn",
                    "CONFIG_PACKAGE_ddnsto",
                ],
            },
            # {
            #     "slug": "smartdns",
            #     "display": "SmartDNS",
            #     "description": "SmartDNS 程序与管理界面。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-smartdns",
            #         "CONFIG_PACKAGE_luci-i18n-smartdns-zh-cn",
            #         "CONFIG_PACKAGE_smartdns",
            #     ],
            # },
            # {
            #     "slug": "wol",
            #     "display": "网络唤醒",
            #     "description": "luci-app-wol 网络唤醒工具。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-wol",
            #         "CONFIG_PACKAGE_luci-i18n-wol-zh-cn",
            #     ],
            # },
            # {
            #     "slug": "nps",
            #     "display": "Nps 内网穿透",
            #     "description": "nps 穿透服务与 LuCI 面板。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-nps",
            #         "CONFIG_PACKAGE_luci-i18n-nps-zh-cn",
            #         "CONFIG_PACKAGE_nps",
            #     ],
            # },
            # {
            #     "slug": "appfilter",
            #     "display": "应用过滤",
            #     "description": "OpenAppFilter 应用过滤套件。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-oaf",
            #         "CONFIG_PACKAGE_luci-i18n-oaf-zh-cn",
            #         "CONFIG_PACKAGE_open-app-filter",
            #     ],
            # },
            # {
            #     "slug": "aria2",
            #     "display": "Aria2",
            #     "description": "Aria2 下载器及 LuCI 配置。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-aria2",
            #         "CONFIG_PACKAGE_luci-i18n-aria2-zh-cn",
            #         "CONFIG_PACKAGE_aria2",
            #     ],
            # },
            # {
            #     "slug": "frpc",
            #     "display": "Frp 客户端",
            #     "description": "Frpc 客户端与 LuCI 前端。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-frpc",
            #         "CONFIG_PACKAGE_luci-i18n-frpc-zh-cn",
            #         "CONFIG_PACKAGE_frpc",
            #     ],
            # },
            # {
            #     "slug": "frps",
            #     "display": "Frp 服务端",
            #     "description": "Frps 服务端与 LuCI 前端。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-frps",
            #         "CONFIG_PACKAGE_luci-i18n-frps-zh-cn",
            #         "CONFIG_PACKAGE_frps",
            #     ],
            # },
            # {
            #     "slug": "momo",
            #     "display": "Momo",
            #     "description": "luci-app-momo 工具集合。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-momo",
            #         "CONFIG_PACKAGE_luci-i18n-momo-zh-cn",
            #         "CONFIG_PACKAGE_momo",
            #     ],
            # },
            # {
            #     "slug": "nikki",
            #     "display": "Nikki",
            #     "description": "luci-app-nikki 工具集合。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-nikki",
            #         "CONFIG_PACKAGE_luci-i18n-nikki-zh-cn",
            #         "CONFIG_PACKAGE_nikki",
            #     ],
            # },
            # {
            #     "slug": "openlist2",
            #     "display": "OpenList",
            #     "description": "OpenList / OpenList2 应用。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-openlist2",
            #         "CONFIG_PACKAGE_luci-i18n-openlist2-zh-cn",
            #         "CONFIG_PACKAGE_openlist2",
            #     ],
            # },
            # {
            #     "slug": "uhttpd",
            #     "display": "uHTTPd",
            #     "description": "uHTTPd Web 服务器管理。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-uhttpd",
            #         "CONFIG_PACKAGE_luci-i18n-uhttpd-zh-cn",
            #         "CONFIG_PACKAGE_uhttpd",
            #     ],
            # },
            # {
            #     "slug": "upnp",
            #     "display": "UPnP",
            #     "description": "miniUPnP 映射服务与 LuCI 面板。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-upnp",
            #         "CONFIG_PACKAGE_luci-i18n-upnp-zh-cn",
            #         "CONFIG_PACKAGE_miniupnpd",
            #     ],
            # },
            # {
            #     "slug": "vlmcsd",
            #     "display": "Vlmcsd KMS 服务器",
            #     "description": "Vlmcsd KMS 激活服务。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-vlmcsd",
            #         "CONFIG_PACKAGE_luci-i18n-vlmcsd-zh-cn",
            #         "CONFIG_PACKAGE_vlmcsd",
            #     ],
            # },
        ],
    },
    # {
    #     "name": "Docker (arm)",
    #     "items": [
    #         {
    #             "slug": "dockerman-overview",
    #             "display": "概览",
    #             "description": "luci-app-dockerman 总览页。",
    #             "prefixes": [
    #                 "CONFIG_PACKAGE_luci-app-dockerman",
    #                 "CONFIG_PACKAGE_luci-i18n-dockerman-zh-cn",
    #             ],
    #         },
    #         {
    #             "slug": "dockerman-containers",
    #             "display": "容器",
    #             "description": "Dockerman 容器列表。",
    #             "prefixes": [
    #                 "CONFIG_PACKAGE_luci-app-dockerman",
    #                 "CONFIG_PACKAGE_luci-i18n-dockerman-zh-cn",
    #             ],
    #         },
    #         {
    #             "slug": "dockerman-images",
    #             "display": "镜像",
    #             "description": "Dockerman 镜像管理。",
    #             "prefixes": [
    #                 "CONFIG_PACKAGE_luci-app-dockerman",
    #                 "CONFIG_PACKAGE_luci-i18n-dockerman-zh-cn",
    #             ],
    #         },
    #         {
    #             "slug": "dockerman-network",
    #             "display": "网络",
    #             "description": "Dockerman 网络管理。",
    #             "prefixes": [
    #                 "CONFIG_PACKAGE_luci-app-dockerman",
    #                 "CONFIG_PACKAGE_luci-i18n-dockerman-zh-cn",
    #             ],
    #         },
    #         {
    #             "slug": "dockerman-volumes",
    #             "display": "存储卷",
    #             "description": "Dockerman 存储卷管理。",
    #             "prefixes": [
    #                 "CONFIG_PACKAGE_luci-app-dockerman",
    #                 "CONFIG_PACKAGE_luci-i18n-dockerman-zh-cn",
    #             ],
    #         },
    #         {
    #             "slug": "dockerman-events",
    #             "display": "事件",
    #             "description": "Dockerman 事件日志。",
    #             "prefixes": [
    #                 "CONFIG_PACKAGE_luci-app-dockerman",
    #                 "CONFIG_PACKAGE_luci-i18n-dockerman-zh-cn",
    #             ],
    #         },
    #         {
    #             "slug": "dockerman-settings",
    #             "display": "设置",
    #             "description": "Dockerman 设置页面。",
    #             "prefixes": [
    #                 "CONFIG_PACKAGE_luci-app-dockerman",
    #                 "CONFIG_PACKAGE_luci-i18n-dockerman-zh-cn",
    #             ],
    #         },
    #     ],
    # },
    {
        "name": "网络存储",
        "items": [
            # {
            #     "slug": "usb_printer",
            #     "display": "USB 打印服务器",
            #     "description": "luci-app-usb-printer。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-usb-printer",
            #         "CONFIG_PACKAGE_luci-i18n-usb-printer-zh-cn",
            #     ],
            # },
            # {
            #     "slug": "hd_idle",
            #     "display": "硬盘休眠",
            #     "description": "hd-idle 磁盘休眠管理。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-hd-idle",
            #         "CONFIG_PACKAGE_luci-i18n-hd-idle-zh-cn",
            #         "CONFIG_PACKAGE_hd-idle",
            #     ],
            # },
            # {
            #     "slug": "p910nd",
            #     "display": "p910nd-打印服务器",
            #     "description": "p910nd 打印共享。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-p910nd",
            #         "CONFIG_PACKAGE_luci-i18n-p910nd-zh-cn",
            #         "CONFIG_PACKAGE_p910nd",
            #     ],
            # },
            # {
            #     "slug": "samba4",
            #     "display": "网络共享",
            #     "description": "Samba4 文件共享。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-samba4",
            #         "CONFIG_PACKAGE_luci-i18n-samba4-zh-cn",
            #         "CONFIG_PACKAGE_samba4-server",
            #     ],
            # },
            # {
            #     "slug": "vsftpd",
            #     "display": "FTP 服务器",
            #     "description": "vsftpd FTP 服务。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-vsftpd",
            #         "CONFIG_PACKAGE_luci-i18n-vsftpd-zh-cn",
            #         "CONFIG_PACKAGE_vsftpd",
            #     ],
            # },
        ],
    },
    {
        "name": "VPN",
        "items": [
            {
                "slug": "ipsec-vpnd",
                "display": "IPSec VPN 服务器",
                "description": "luci-app-ipsec-vpnd / strongSwan。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-ipsec-vpnd",
                    "CONFIG_PACKAGE_luci-i18n-ipsec-vpnd-zh-cn",
                    "CONFIG_PACKAGE_strongswan",
                    "CONFIG_PACKAGE_kmod-ipsec",
                    "CONFIG_PACKAGE_kmod-ipt-ipsec",
                ],
            },
            {
                "slug": "softethervpn",
                "display": "SoftEther VPN 服务器",
                "description": "luci-app-softethervpn 与 softethervpn5。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-softethervpn",
                    "CONFIG_PACKAGE_luci-i18n-softethervpn-zh-cn",
                    "CONFIG_PACKAGE_softethervpn5",
                ],
            },
            {
                "slug": "openvpn-server",
                "display": "OpenVPN 服务器",
                "description": "OpenVPN Server LuCI 前端。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-openvpn-server",
                    "CONFIG_PACKAGE_luci-i18n-openvpn-server-zh-cn",
                ],
            },
            {
                "slug": "n2n",
                "display": "N2N VPN",
                "description": "luci-app-n2n 与 n2n 内核。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-n2n",
                    "CONFIG_PACKAGE_luci-i18n-n2n-zh-cn",
                    "CONFIG_PACKAGE_n2n",
                ],
            },
            {
                "slug": "tailscale",
                "display": "Tailscale",
                "description": "Tailscale Mesh VPN。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-tailscale",
                    "CONFIG_PACKAGE_luci-i18n-tailscale-zh-cn",
                    "CONFIG_PACKAGE_tailscale",
                ],
            },
            # {
            #     "slug": "zerotier",
            #     "display": "ZeroTier",
            #     "description": "ZeroTier 自组网。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-zerotier",
            #         "CONFIG_PACKAGE_luci-i18n-zerotier-zh-cn",
            #         "CONFIG_PACKAGE_zerotier",
            #     ],
            # },
        ],
    },
    {
        "name": "网络",
        "items": [
            {
                "slug": "network",
                "display": "接口",
                "description": "接口配置（核心功能，仅记录）。",
            },
            {
                "slug": "routes-network",
                "display": "路由",
                "description": "路由表配置（核心功能，仅记录）。",
            },
            {
                "slug": "dhcp",
                "display": "DHCP/DNS",
                "description": "DHCP/DNS 管理（核心功能，仅记录）。",
            },
            {
                "slug": "diagnostics",
                "display": "网络诊断",
                "description": "网络诊断工具（核心功能，仅记录）。",
            },
            {
                "slug": "firewall",
                "display": "防火墙",
                "description": "luci-app-firewall 防火墙管理。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-firewall",
                    "CONFIG_PACKAGE_luci-i18n-firewall-zh-cn",
                ],
            },
            {
                "slug": "socat",
                "display": "Socat",
                "description": "luci-app-socat 端口转发。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-socat",
                    "CONFIG_PACKAGE_luci-i18n-socat-zh-cn",
                    "CONFIG_PACKAGE_socat",
                ],
            },
            # {
            #     "slug": "syncdial",
            #     "display": "多线多拨",
            #     "description": "luci-app-syncdial 多拨插件。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-syncdial",
            #         "CONFIG_PACKAGE_luci-i18n-syncdial-zh-cn",
            #     ],
            # },
            {
                "slug": "eqos",
                "display": "网速控制",
                "description": "luci-app-eqos 带宽控制。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-eqos",
                    "CONFIG_PACKAGE_luci-i18n-eqos-zh-cn",
                ],
            },
            # {
            #     "slug": "mwan3",
            #     "display": "MultiWAN 管理器",
            #     "description": "luci-app-mwan3 负载均衡。",
            #     "prefixes": [
            #         "CONFIG_PACKAGE_luci-app-mwan3",
            #         "CONFIG_PACKAGE_luci-i18n-mwan3-zh-cn",
            #         "CONFIG_PACKAGE_mwan3",
            #     ],
            # },
        ],
    },
    {
        "name": "带宽监控",
        "items": [
            {
                "slug": "display",
                "display": "显示",
                "description": "luci-app-nlbwmon 带宽显示。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-nlbwmon",
                    "CONFIG_PACKAGE_luci-i18n-nlbwmon-zh-cn",
                ],
            },
            {
                "slug": "config",
                "display": "配置",
                "description": "luci-app-nlbwmon 配置页面。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-nlbwmon",
                    "CONFIG_PACKAGE_luci-i18n-nlbwmon-zh-cn",
                ],
            },
            {
                "slug": "backup",
                "display": "备份",
                "description": "luci-app-nlbwmon 备份页面。",
                "prefixes": [
                    "CONFIG_PACKAGE_luci-app-nlbwmon",
                    "CONFIG_PACKAGE_luci-i18n-nlbwmon-zh-cn",
                ],
            },
        ],
    },
]

def _flatten_sections() -> List[dict]:
    groups: List[dict] = []
    for section in SECTION_DEFINITIONS:
        for item in section["items"]:
            groups.append(
                {
                    "section": section["name"],
                    "slug": item["slug"],
                    "display": item["display"],
                    "description": item.get("description", ""),
                    "exact_keys": item.get("exact_keys", []),
                    "prefixes": item.get("prefixes", []),
                }
            )
    return groups


MANAGED_PLUGIN_GROUPS = _flatten_sections()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="批量处理 OpenWrt defconfig 中的插件开关状态",
    )
    parser.add_argument(
        "--config-root",
        default="config",
        help="需要遍历的目录，默认是仓库下的 config 目录",
    )
    parser.add_argument(
        "--mode",
        choices=("disable", "enable"),
        default="disable",
        help="执行模式：disable=# CONFIG is not set，enable=写成 CONFIG=y",
    )
    parser.add_argument(
        "--enable-value",
        default="y",
        help="enable 模式下写入的值，默认 y，可改为 m",
    )
    parser.add_argument(
        "--extra-exact",
        action="append",
        default=[],
        help="额外追加需要精确匹配的 CONFIG 名称（可重复传入）",
    )
    parser.add_argument(
        "--extra-prefix",
        action="append",
        default=[],
        help="额外追加按前缀匹配的 CONFIG 名称（可重复传入）",
    )
    parser.add_argument(
        "--list-managed",
        action="store_true",
        help="列出脚本默认管理的插件清单并退出",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印将要修改的文件，不真正写回",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="打印每个被修改文件的详细信息",
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="指定要处理的单个 .config 文件；不传则遍历 config-root",
    )
    return parser.parse_args()


def iter_config_files(args: argparse.Namespace) -> List[Path]:
    if args.files:
        return [Path(p).resolve() for p in args.files]

    root = Path(args.config_root).resolve()
    return sorted(root.rglob("*.config"))


def build_managed_sets(
    extra_exact: Iterable[str], extra_prefix: Iterable[str]
) -> tuple[set[str], List[str]]:
    exact_keys: set[str] = set()
    prefixes: List[str] = []

    for group in MANAGED_PLUGIN_GROUPS:
        exact_keys.update(group.get("exact_keys", []))
        prefixes.extend(group.get("prefixes", []))

    exact_keys.update(extra_exact)
    prefixes.extend(extra_prefix)
    return exact_keys, prefixes


def list_managed_plugins() -> None:
    print("脚本默认管理以下插件/功能：\n")
    current_section = None
    for group in MANAGED_PLUGIN_GROUPS:
        if group["section"] != current_section:
            current_section = group["section"]
            print(f"[{current_section}]")
        print(f"- {group['display']} ({group['slug']})")
        print(f"  说明：{group['description']}")
        exact = group.get("exact_keys") or []
        prefixes = group.get("prefixes") or []
        if exact:
            print(f"  精确匹配：{', '.join(exact)}")
        if prefixes:
            print(f"  前缀匹配：{', '.join(prefixes)}")
        print()


def extract_key(stripped_line: str) -> str | None:
    if stripped_line.startswith("# ") and stripped_line.endswith(" is not set"):
        return stripped_line[2:].split(" ", 1)[0]
    if "=" in stripped_line:
        return stripped_line.split("=", 1)[0].strip()
    return None


def split_newline(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    if line.endswith("\r"):
        return line[:-1], "\r"
    return line, ""


def format_line(key: str, newline: str, mode: str, enable_value: str) -> str:
    if mode == "disable":
        return f"# {key} is not set{newline}"
    return f"{key}={enable_value}{newline}"


def match_target(key: str, exact_keys: set[str], prefixes: Iterable[str]) -> bool:
    if key in exact_keys:
        return True
    return any(key.startswith(prefix) for prefix in prefixes)


def process_file(
    path: Path,
    mode: str,
    enable_value: str,
    exact_keys: set[str],
    prefixes: List[str],
    dry_run: bool,
) -> bool:
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)
    new_lines: list[str] = []
    changed = False

    for line in lines:
        body, newline = split_newline(line)
        stripped = body.strip()
        key = extract_key(stripped)

        if key and match_target(key, exact_keys, prefixes):
            new_line = format_line(key, newline, mode, enable_value)
            if new_line != line:
                changed = True
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    if changed and not dry_run:
        path.write_text("".join(new_lines), encoding="utf-8")

    return changed


def main() -> None:
    args = parse_args()
    if args.list_managed:
        list_managed_plugins()
        return

    files = iter_config_files(args)
    if not files:
        raise SystemExit("未找到任何待处理的 .config 文件")

    exact_keys, prefixes = build_managed_sets(args.extra_exact, args.extra_prefix)

    touched = []
    for cfg in files:
        if not cfg.exists():
            continue
        if process_file(
            cfg, args.mode, args.enable_value, exact_keys, prefixes, args.dry_run
        ):
            touched.append(cfg)
            if args.verbose:
                print(f"[修改] {cfg}")

    summary = "dry-run 模式，未写回任何文件。" if args.dry_run else ""
    print(
        f"共检查 {len(files)} 个 .config 文件，其中 {len(touched)} 个发生变化。{summary}"
    )


if __name__ == "__main__":
    main()

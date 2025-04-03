# Home Assistant 雷池集成

- 这是一个由用户开发的关于 长亭雷池 的集成，主要用于收集显示雷池的大屏数据。

- 注意开发者与雷池官方无任何关联，本集成调用官方提供的API接口，不涉及对雷池配置内容的修改！

- 本集成仅用于学习研究，作者不承诺其稳定性，在使用过程中产生的风险与作者无关，即使作者已被告知相关损害。

## 安装

### 方法 1：通过 [HACS](https://hacs.xyz/) 商店安装

HACS > 右上角三个点 > Custom repositories > Repository: https://github.com/nkdns/safeline_plug.git & Category or Type: Integration > ADD > 点击 HACS 的 New 或 Available for download 分类下的 Safeline ，进入集成详情页  > DOWNLOAD。

### 方法 2：通过 [Samba](https://github.com/home-assistant/addons/tree/master/samba) 或 [FTPS](https://github.com/hassio-addons/addon-ftp) 手动安装

下载并将 `custom_components/safeline_plug` 文件夹复制到 Home Assistant 的 `custom_components` 文件夹下并重载 Home Assistant 。

## 配置

### 第一步-获取雷池API Token

进入雷池web > 系统设置 找到 `API Token` ，获取 `API Token`

### 第二步-配置集成

进入 `HomeAssistane` > 设置 > 设备与服务 > 集成 ，找到 `添加集成` ，搜索 `Safeline` 或 `雷池`

![image](https://github.com/user-attachments/assets/75787513-37ed-4336-bf18-a5dd9e584ca6)

并将获取到的信息填入即可，注意区分 `http` 与 `https` 协议。

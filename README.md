# Home Assistant 雷池集成

- 这是一个由用户开发的关于 长亭雷池 的集成，主要用于收集显示雷池的大屏数据。

- 注意开发者与雷池官方无任何关联，本集成调用官方提供的API接口，不涉及对雷池配置内容的修改！

- 本集成仅用于学习研究，作者不承诺其稳定性，在使用过程中产生的风险与作者无关，即使作者已被告知相关损害

## 安装

### 方法 1 通过 [HACS](https://hacs.xyz/) 商店安装

HACS > 右上角三个点 > Custom repositories > Repository: https://github.com/nkdns/safeline.git & Category or Type: Integration > ADD > 点击 HACS 的 New 或 Available for download 分类下的 Safeline ，进入集成详情页  > DOWNLOAD

### 方法 2 手动安装

custom_components/safeline 文件移动到 HomeAssistant 目录下 custom_components/ 文件夹中，并重载 HomeAssistant
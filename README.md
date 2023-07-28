# nonebot-yiyan

_百度文心一言对话平台_

</div>

### 简介：
基于zhenxun_bot平台开发的文心一言对话插件，稍加修改也可用在基于nonebot的各类机器人平台上通用。

### 可用功能:
+ [x] 调用文心一言数据模型进行对话；
+ [ ] 进行具有连续性的对话；

### 安装：
下载本插件后丢到plugin文件夹里（但凡是个人都知道怎么装）。

### 使用方法：
```bash
/wx 聊天内容
```

### 配置：
1.去[百度文心一言网站](https://yiyan.baidu.com)获取内测资格；</br>
2.申请[文心大模型](https://cloud.baidu.com/survey/qianfan.html)；</br>
3.申请成功后进入[文心千帆控制台](https://ai.baidu.com/wenxinworkshop/app/overview)，点击“直接使用”中的“去使用”按钮，按照引导步骤开通api；</br>
4.开通之后进入百度智能云控制台的[文心千帆应用列表](https://console.bce.baidu.com/ai/#/ai/wenxinworkshop/app/list)，点击创建应用。默认ERNIE-Bot-turbo等服务是自动勾选的，你只需配置应用名称、类型和描述，然后点击“立即创建”；</br>
5.创建完成后查看应用详情，记下API Key和Secret Key；</br>
6.打开__init__.py，分别在在client_id和client_secret中填入你的API Key和Secret Key；</br>
7.重启机器人。

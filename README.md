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

### 参数：
<table>
  <tr>
    <th>参数名称</th>
    <th>参数说明</th>
    <th>默认值</th>
    <th>范例</th>
  </tr>
  <tr>
    <td>client_id</td>
    <td>API Key</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>client_secret</td>
    <td>Secret Key</td>
    <td>/</td>
    <td>/</td>
  </tr>
  <tr>
    <td>history_path</td>
    <td>消息记录存放路径（绝对路径）</td>
    <td>/</td>
    <td>/home/history/</td>
  </tr>
  <tr>
    <td>history_numh</td>
    <td>最大消息记录保存数量</td>
    <td>10</td>
    <td>10</td>
  </tr>
</table>

### 使用方法：
```bash
对话：/wx 对话内容
删除当前账号聊天记录：/wx delete
删除所有账号聊天记录：/wx delete_all（仅限bot管理员）
```

### 配置：
[点击此处查看配置教程](https://github.com/barryblueice/nonebot_yiyan/wiki/%E5%A6%82%E4%BD%95%E9%85%8D%E7%BD%AE%E6%9C%BA%E5%99%A8%E4%BA%BA)

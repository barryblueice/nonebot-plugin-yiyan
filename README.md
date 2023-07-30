# nonebot-plugin-yiyan

_百度文心一言对话平台_

</div>

### 简介：
基于zhenxun_bot平台开发的文心一言对话插件，稍加修改也可用在各类基于nonebot的机器人平台上。

### 可用功能:
+ [x] 调用文心一言数据模型进行对话；
+ [x] 多轮对话；
+ [x] 角色扮演；

### 安装：
下载本插件后丢到插件文件夹里（但凡是个人都知道怎么装）。

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
    <td>client_id = "xxxxxxxxxxxxx"</td>
  </tr>
  <tr>
    <td>client_secret</td>
    <td>Secret Key</td>
    <td>/</td>
    <td>client_secret = "xxxxxxxxxxxxx"</td>
  </tr>
  <tr>
    <td>history_path</td>
    <td>消息记录存放路径（绝对路径）</td>
    <td>/</td>
    <td>history_path = "/home/history/"</td>
  </tr>
  <tr>
    <td>history_num</td>
    <td>最大消息记录保存数量</td>
    <td>50</td>
    <td>history_num = 50</td>
  </tr>
   <tr>
    <td>history_clear_time</td>
    <td>消息记录保留时间，以分钟为单位，时间一到就会自动清除消息记录</td>
    <td>5</td>
    <td>history_clear_time = 5</td>
  </tr>

  <tr>
    <td>waifu</td>
    <td>角色扮演模板</td>
    <td>角色扮演模板。若要添加新模板则需要同时修改wx_create模块中的相关内容</td>
    <td>1.猫娘</br>2.傲娇女主</td>
  </tr>
</table>

### 使用方法：
```bash
对话：/wx 对话内容
角色对话：/wx create 角色数字
删除当前聊天记录：/wx delete
删除所有聊天记录：/wx delete_all（仅限bot管理员）
```

### 配置：
[点击此处查看配置教程](https://github.com/barryblueice/nonebot_yiyan/wiki/%E5%A6%82%E4%BD%95%E9%85%8D%E7%BD%AE%E6%9C%BA%E5%99%A8%E4%BA%BA)

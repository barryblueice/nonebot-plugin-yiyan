from nonebot import on_command
from nonebot.adapters.onebot.v11 import *
import requests,json
from utils.manager import withdraw_message_manager
# from operator import length_hint

__zx_plugin_name__ = "文心对话"
__plugin_des__ = "文心对话"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["/wx"]
__plugin_settings__ = {
    "level": 1,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["/wx"],
}
__plugin_usage__ = """

功能：
    百度文心一言对话平台
用法：
    
"""

client_id = ""
client_secret = ""

wx = on_command("/wx ",block=True, priority=5)

url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

def get_access_token():
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

@wx.handle()
async def process(bot: Bot, event: MessageEvent):
    wx_ram = str(event.get_message()).strip()
    part = wx_ram.strip('/wx').lstrip().replace(" ","")
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": f"{part}"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    result = json.loads(response.text)
    await wx.send(result["result"])




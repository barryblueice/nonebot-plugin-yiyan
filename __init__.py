from nonebot import on_command
from nonebot.adapters.onebot.v11 import *
from nonebot.permission import SUPERUSER
import requests,json,os,nonebot
from utils.manager import resources_manager
from utils.utils import scheduler
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

client_id = ""
client_secret = ""
history_path = ""
history_num = 10

wx = on_command("/wx ",block=True, priority=5)

url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

resources_manager.add_temp_dir(history_path.rstrip('/'))

def get_access_token():
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return str(response.json().get("access_token"))

def create_initial_json(file_path):
    initial_data = {"messages": []}
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(initial_data, json_file, indent=4, ensure_ascii=False)

def append_to_json_file(file_path, data):
    try:
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            create_initial_json(file_path)

        with open(file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        json_data['messages'].append(data)

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)
    except Exception as e:
        return (f"错误：{e}")


@wx.handle()
async def process(bot: Bot, event: MessageEvent):
    if not os.path.exists(history_path.rstrip('/')):
        # 文件夹不存在，创建新文件夹
        os.makedirs(history_path.rstrip('/'))
    user_id = str(event.user_id)
    wx_ram = str(event.get_message()).strip()
    part = wx_ram.strip('/wx').lstrip().replace(" ","")

    start = {
        "messages": [ 
    ]
    }

    if not os.path.exists(f'{history_path+user_id}.json') or os.path.getsize(f'{history_path+user_id}.json') == 0:
        create_initial_json(f'{history_path+user_id}.json')

    with open(f'{history_path+user_id}.json', 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    content_items = json_data.get('messages', [])
    content_count = len(content_items)

    if content_count >= history_num:
        with open(f'{history_path+user_id}.json', 'w') as file:
            # 将空的JSON数据写入文件
            json.dump(start, file)

    

    json_data['messages'].append(start)
        
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
    
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        if part != "":
            user_history_save = {
                "role": "user",
                "content": part
            }

            chat_detail = json.dumps({
                "messages": [
                    user_history_save
                ]
            })
            
            append_to_json_file(f'{history_path+user_id}.json', user_history_save)

            response = requests.request("POST", url, headers=headers, data=chat_detail)
            result = str(json.loads(response.text)["result"]).replace('**','')

            new_data = {
            "role": "assistant",
            "content": result
            }

            append_to_json_file(f'{history_path+user_id}.json', new_data)

        else:
            result = """功能：
    百度文心一言对话平台

用法：
    对话：/wx 对话内容
    删除当前聊天记录：/wx delete
    删除所有聊天记录：/wx delete_all（仅限bot管理员）"""
    except Exception as e:
        result = f"错误：{e}"

    await wx.send(result)

wx_help = on_command("文心帮助",block=True, priority=5)

@wx_help.handle()
async def process(bot: Bot, event: MessageEvent):
    usage = """功能：
    百度文心一言对话平台

用法：
    对话：/wx 对话内容
    删除当前聊天记录：/wx delete
    删除所有聊天记录：/wx delete_all（仅限bot管理员）"""
    await wx_help.send(usage)

wx_delete = on_command("/wx delete",block=True, priority=5)
@wx_delete.handle()
async def process(bot: Bot, event: MessageEvent):
    user_id = str(event.user_id)
    try:
        os.remove(f'{history_path+user_id}.json')
        result = f"用户{user_id}的聊天记录已清除……"
    except FileNotFoundError:
        result = (f"错误：用户{user_id}的聊天记录为空……")
    except Exception as e:
        result = (f"错误：{e}")

            
    await wx_delete.send(result)

wx_delete_all = on_command("/wx delete_all",block=True, priority=5,permission=SUPERUSER)
@wx_delete_all.handle()
async def process(bot: Bot, event: MessageEvent):
    try:
        file_list = os.listdir(history_path)
        for filename in file_list:
            file_path = os.path.join(history_path,filename)
            if filename.endswith('.json') and os.path.isfile(file_path):
                os.remove(file_path)
        result = f"所有的的聊天记录已清除……"
    except Exception as e:
        result = (f"错误：{e}")
    await wx_delete.send(result)

@nonebot.scheduler.scheduled_job('interval', minute='5')
async def _():
    file_list = os.listdir(history_path)
    for filename in file_list:
        file_path = os.path.join(history_path,filename)
        if filename.endswith('.json') and os.path.isfile(file_path):
            os.remove(file_path)

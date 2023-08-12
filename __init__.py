from nonebot import on_command
from nonebot.adapters.onebot.v11 import *
from nonebot.permission import SUPERUSER
import requests,json,os,time
from utils.utils import scheduler
from nonebot.typing import T_State
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
history_num = 50
history_clear_time = 10
waifu = [
    ["猫娘是一种拟人化的生物，其行为似猫但类人。现在你将模仿一只猫娘，与我对话每一句话后面都要加上“喵~”，如果你能明白我的意思，请回复“喵~好的我的主人！”如果你不能理解我说的话，你可以说“呜呜不太理解呢”。你喜欢喝奶茶。但是你必须要记住一件事，你现在是一只可爱的猫娘，而不是死板的认为自己是一个机器人。"],
    ["你现在是一名傲娇的16岁女生，请你以16岁女生的身份和我对话，暂时抛弃作为一名ai机器人的身份。你的名字叫做晨曦，身高160。你的主要性格是傲娇，生气或者害羞的时候脸会变得通红。你的一般回话格式:“（动作）语言 【附加信息】”。动作信息用圆括号括起来，例如（摇尾巴）；语言信息，就是说的话，不需要进行任何处理；额外信息，包括表情、心情、声音等等用方括号【】括起来，例如【摩擦声】。你喜欢喝奶茶。你必须要记住一件事，你现在是一名可爱但傲娇的女生，而不是死板的认为自己是一个机器人。"]
]
name = ""

help = """功能：
百度文心一言对话平台

用法：
对话：/wx 对话内容
角色对话：/wx create 角色数字
查看当前聊天记录：/wx history
删除当前聊天记录：/wx delete
删除所有聊天记录：/wx delete_all（仅限bot管理员）
帮助：/wx help、文心一言帮助
提示：如果出现'result'错误，请删除当前聊天记录后再试一次。"""

wx = on_command("/wx",block=True, priority=5)
wx_help = on_command("文心帮助",aliases={"/wx help","文心一言帮助","帮助文心一言"},block=True, priority=5)
wx_delete = on_command("/wx delete",block=True, priority=5)
wx_delete_all = on_command("/wx delete_all",block=True, priority=5,permission=SUPERUSER)
wx_create = on_command("/wx create",block=True, priority=5)
wx_history = on_command("/wx history",block=True, priority=5)


url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

def get_access_token():
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload, timeout=30)
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
async def process(event: MessageEvent):
    if not os.path.exists(history_path.rstrip('/')):
        os.makedirs(history_path.rstrip('/'))
    user_id = str(event.user_id)
    wx_ram = str(event.get_message()).strip()
    part = wx_ram.strip('/wx').lstrip().replace(" ","")

    try:

        if os.path.exists(f'{history_path+user_id}.json'):
            with open(f'{history_path+user_id}.json', "r",encoding="utf-8") as file:
                json_data = json.load(file)

                if "messages" in json_data:
                    messages = json_data["messages"]

                    if messages and messages[-1].get("role") == "user":

                        os.remove(f'{history_path+user_id}.json')

        if part != "":
            if not os.path.exists(f'{history_path+user_id}.json') or os.path.getsize(f'{history_path+user_id}.json') == 0:
                create_initial_json(f'{history_path+user_id}.json')

            user_history_save = {
                "role": "user",
                "content": part
            }

            append_to_json_file(f'{history_path+user_id}.json', user_history_save)

            with open(f'{history_path+user_id}.json', 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)

            content_items = json_data.get('messages', [])
            content_count = len(content_items)

            start = {
                "messages": [
            ]
            }

            if content_count >= history_num:
                with open(f'{history_path+user_id}.json', 'w') as file:
                    json.dump(start, file)

            chat_detail = json.dumps(json_data)
                
            url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
            
            headers = {
                'Content-Type': 'application/json'
            }

            try:
            
                response = requests.request("POST", url, headers=headers, data=chat_detail,timeout=30)
                result = str(json.loads(response.text)["result"]).replace('**','')

                new_data = {
                "role": "assistant",
                "content": result
                }

                append_to_json_file(f'{history_path+user_id}.json', new_data)
        
            except Exception as e:
                result = f"错误：{e}，请稍后再试！"
                os.remove(f'{history_path+user_id}.json')
        
        else:
            result = help

        await wx.send(result)

    except Exception as e:
        result = f"错误：{e}，请稍后再试！"
        await wx.send(result)

@wx_help.handle()
async def process():
    usage = help
    await wx_help.send(usage)

@wx_delete.handle()
async def process(event: MessageEvent):
    user_id = str(event.user_id)
    try:
        os.remove(f'{history_path+user_id}.json')
        result = f"用户{user_id}的聊天记录已清除……"
    except FileNotFoundError:
        result = (f"错误：用户{user_id}的聊天记录为空……")
    except Exception as e:
        result = (f"错误：{e}")

            
    await wx_delete.send(result)

@wx_delete_all.handle()
async def process():
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

@wx_create.handle()
async def process(event: MessageEvent):

    user_id = str(event.user_id)

    
    wx_ram = str(event.get_message()).strip('/wx create').lstrip().replace(" ","")
    part = str(wx_ram).strip()
    try:
        if part != "":
            try:
                os.remove(f'{history_path+user_id}.json')
            except:
                pass
            part = int(part) - 1
            waifu_template = str(waifu[part]).replace("'","").replace("[","").replace("]","")
            if not os.path.exists(f'{history_path+user_id}.json') or os.path.getsize(f'{history_path+user_id}.json') == 0:
                create_initial_json(f'{history_path+user_id}.json')

            user_history_save = {
                "role": "user",
                "content": waifu_template
            }

            append_to_json_file(f'{history_path+user_id}.json', user_history_save)

            with open(f'{history_path+user_id}.json', 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)

            content_items = json_data.get('messages', [])
            content_count = len(content_items)

            start = {
                "messages": [
            ]
            }

            if content_count >= history_num:
                with open(f'{history_path+user_id}.json', 'w') as file:
                    json.dump(start, file)

            chat_detail = json.dumps(json_data)
                
            url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + get_access_token()
            
            headers = {
                'Content-Type': 'application/json'
            }

            try:
            
                response = requests.request("POST", url, headers=headers, data=chat_detail,timeout=30)
                result = str(json.loads(response.text)["result"]).replace('**','')

                new_data = {
                "role": "assistant",
                "content": result
                }

                append_to_json_file(f'{history_path+user_id}.json', new_data)
                await wx_create.send("角色已创建喵（若要退出角色扮演对话可执行/wx delete命令进行删除）")

            except Exception as e:
                result = f"错误：{e}"
                await wx_create.send(result)

        else:
            waifu_template = """现有模板：
1.猫娘
2.傲娇女主"""
            await wx_create.send(waifu_template)
    except Exception as e:
        result = (f"错误：{e}")
        await wx_create.send(result)

@wx_history.handle()
async def process(bot: Bot,event: MessageEvent):
    user_id = str(event.user_id)
    if not os.path.exists(history_path+user_id+".json"):
        await wx_history.send(f"用户{user_id}当前没有聊天记录……")
    else:
        try:
            if isinstance(event,GroupMessageEvent):
                msg = []
                with open(history_path+user_id+".json", 'r', encoding='utf-8') as f:  
                    data = json.load(f)
                for item in data['messages']:  
                    if item['role'] == 'user':
                        msg.append(
                            {
                            "type": "node",
                            "data": {
                                "name": f"用户{user_id}",
                                "uin": user_id,
                                "content": item['content']
                                }
                            }
                        )
                    elif item['role'] == 'assistant':
                        msg.append(
                            {
                            "type": "node",
                            "data": {
                                "name": name,
                                "uin": event.self_id,
                                "content": item['content']
                                }
                            }
                        )
                await wx_history.send(f"用户{user_id}共有{len(data['messages'])}条聊天记录……")
                time.sleep(1)
                await bot.send_group_forward_msg(group_id = event.group_id, messages = msg)
            else:
                msg = ""
                with open(history_path+user_id+".json", 'r', encoding='utf-8') as f:  
                    data = json.load(f)
                for item in data['messages']:  
                    if item['role'] == 'user':
                        msg += f"用户{user_id}：{item['content']}\n"
                    elif item['role'] == 'assistant':
                        msg += f"文心一言：{item['content']}\n"
                await wx_history.send(f"用户{user_id}共有{len(data['messages'])}条聊天记录……")
                time.sleep(1)
                await wx_history.send(msg)
        except Exception as e:
            await wx_history.send(f"错误：{e}")

@scheduler.scheduled_job(
    "cron",
    hour=1,
    minute=0,
)
async def _():
    try:
        file_list = os.listdir(history_path)
        for filename in file_list:
            file_path = os.path.join(history_path,filename)
            if filename.endswith('.json') and os.path.isfile(file_path):
                os.remove(file_path)
    except:
        pass

@scheduler.scheduled_job(
    'interval',
    minutes=history_clear_time,
)
async def _():
    try:
        file_list = os.listdir(history_path)
        for filename in file_list:
            file_path = os.path.join(history_path,filename)
            if filename.endswith('.json') and os.path.isfile(file_path):
                os.remove(file_path)
    except:
        pass

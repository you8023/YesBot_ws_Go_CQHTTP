import requests
import json
import os
from random import choice
import pymysql
from urllib.parse import quote
import jieba
# import pandas as pd
configuration = json.load(open("./config.json", encoding='utf-8'))
group = configuration["group"]
apikey= configuration["apikey"]
ban_words = configuration["ban_words"]
path = configuration["path"]
self_qq = configuration["self_qq"]

help_base = "这里是帮助菜单：\n"
help_base += "1.发送setu or 猫猫图返回一张图\n"
help_base += "2.私聊调教对话 例如aaa+bbb \n"
help_base += "那么发送aaa就会返回bbb啦~\n"
help_base += "可以发送rmaaa+bbb删除对话哦~\n"

def help_menu(msg):
    if msg[:4]!="help":
        return [False]
    if msg == "help":
        return [True,help_base]
def add_data(msg,all_data):
    if msg.count("+") != 1:
        return [False]
    if "/" in msg or "|" in msg:
        return [True,"不能含有/或|呀~"]
    if msg.split("+")[1]=="":
        return [False]
    msg = msg.split("+")
    if len(msg[0])< 1:
        return [True,"得有内容呀~"]
    for row in all_data:
        if msg[0] == row[0]:
            if msg[1] in row[1]:
                return [True,"这句话我已经会辣，不用再教我啦~"]
            row[1].append(msg[1])
            save_data(all_data)
            return [True,"yes酱记住啦~"]
    all_data.append([msg[0], [msg[1]]])
    save_data(all_data)
    return [True,"yes酱记住啦~"]

def save_data(all_data):
    f = open("./data/talk_data/words","w",encoding='UTF-8')
    for row in all_data:
        temp = row[0]+"|"+"".join([i+"/" for i in row[1]])
        f.writelines(temp+"\n")
    f.close()

def del_data(del_data,all_data):
    if del_data[:2] != "rm":
        return [False]
    msg = del_data[2:].split("+")
    for i in range(len(all_data)):
        if msg[0] == all_data[i][0]:
            if len(all_data[i][1]) == 1:
                all_data.pop(i)
                save_data(all_data)
                return [True,"已经删除啦~"]
            all_data[i][1].remove(msg[1])
            save_data(all_data)
            return [True,"已经删除啦~"]
    return [True,"删除出错啦~"]


def ghs_pic(msg):
    if msg in ["setu"]:
        try:
            req_url="https://api.lolicon.app/setu/"
            params = {"apikey":apikey}
            res=requests.get(req_url,params=params)
            setu_title=res.json()['data'][0]['title']
            setu_url=res.json()['data'][0]['url']
            setu_pid=res.json()['data'][0]['pid']
            setu_author=res.json()['data'][0]['author']
            local_img_url = "title:"+setu_title+"[CQ:image,file="+setu_url+"]"+"pid:"+str(setu_pid)+" 画师:"+setu_author
            return [True, local_img_url]
        except Exception as e:
            print(e)
            return [True, "阿这，出了一点问题"]
    return [False]

def hs_pic(msg):
    if msg in ["huangse"]:
        try:
            req_url="https://api.lolicon.app/setu/"
            params = {"apikey":apikey,"r18":"1"}
            print(req_url)
            res=requests.get(req_url,params=params)
            setu_title=res.json()['data'][0]['title']
            setu_url=res.json()['data'][0]['url']
            setu_pid=res.json()['data'][0]['pid']
            setu_author=res.json()['data'][0]['author']


            local_img_url = "title:"+setu_title+"[CQ:image,file="+setu_url+"]"+"pid:"+str(setu_pid)+" 画师:"+setu_author
            return [True, local_img_url]
        except Exception as e:
            print(e)
            return [True, "阿这，出了一点问题"]
    return [False]

def mao_pic(msg):
    if msg in ["来张猫猫图", "来张猫图", "猫图", "喵图", "maomao","猫猫图","猫"]:
        setu_list = os.listdir(path)
        local_img_url = "[CQ:image,file=file:///"+path+choice(setu_list)+"]"
        return [True, local_img_url]
    return [False]

def send_forward(msg, group_id, ws, sender):
    group_msg = []
    for item in msg:
        each_msg = {
            "type": "node",
            "data": {
                "name": "呜啦",
                "uin": self_qq,
                "content": item
            }
        }
        group_msg.append(each_msg)
    data = {
        'group_id':group_id,
        'messages':group_msg
    }
    # print(data)
    # cq_url = "ws://127.0.0.1:5700/send_group_forward_msg"
    # rev3 = requests.post(cq_url,data=data)
    # print(rev3.json())
    action = "send_group_forward_msg"
    post_data = json.dumps({"action": action, "params": data})
    rev = ws.send(post_data)
    # print(rev)
    returnStr = "[CQ:at,qq={sender}]".format(sender=sender)
    return returnStr

def send_private(msg, sender, ws):
    data = {
        'user_id':sender,
        'message':msg,
        'auto_escape':False
    }
    # cq_url = "ws://127.0.0.1:5700/send_private_msg"
    action = "send_private_msg"
    post_data = json.dumps({"action": action, "params": data})
    rev = ws.send(post_data)
    return rev

def add_friend(sender, msg, ws):
    # if sender in admin_qq:
    #     return [True, '']
    try:
        print('add_friends')
        if msg == '想要的答案':
            return [True, ""]
        else:
            return [False, ""]
        # print(result)
        # if result != ():
        #     return [True, ""]
    except Exception as e:
        print(e)
    return [False, '']

def detect_ban(msg,user_id,group_id, ws):
	if group_id not in group:
		return [False]
	if msg in ban_words:
		data = {
			'user_id':user_id,
			'group_id':group_id,
			'duration':60
		}
		# cq_url = "ws://127.0.0.1:5700/set_group_ban"
		# requests.post(cq_url,data=data)
		action = "set_group_ban"
		post_data = json.dumps({"action": action, "params": data})
		rev = ws.send(post_data)
		return [True,"不要说不该说的话啦~"]
	return [False]

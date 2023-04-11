# from receive import rev_msg
from send_message.send_message import send_message
from massage_flide import msg_talker
import websocket, time, json, logging

talker = msg_talker()
print("start")

ws_url = "ws://127.0.0.1:6700/ws"

# 日志设置
logging.basicConfig(level=logging.DEBUG, format='[%(funcName)s] %(asctime)s - %(levelname)s - %(lineno)d: %(message)s')
logger = logging.getLogger(__name__)

def recv_msg(_, message):
    try:
        rev = json.loads(message)
        # print(rev)
        if rev is None:
            return False
        if "post_type" not in rev.keys():
            return False
        else:
            if rev["post_type"] == "message":
                # print(rev) #需要功能自己DIY
                if rev["message_type"] == "private":  #私聊
                    talker.private_msg(rev, ws)
                elif rev["message_type"] == "group":  #群聊
                    talker.group_msg(rev, ws)
                else:
                    pass
            elif rev["post_type"] == "notice":
                if rev["notice_type"] == "group_upload":  # 有人上传群文件
                    pass
                elif rev["notice_type"] == "group_decrease":  # 群成员减少
                    pass
                elif rev["notice_type"] == "group_increase":  # 群成员增加
                    pass
                else:
                    pass
            elif rev["post_type"] == "request":
                if rev["request_type"] == "friend":  # 添加好友请求
                    talker.addFriends(rev, ws)
                    # pass
                if rev["request_type"] == "group":  # 加群请求
                    pass
            else:  # rev["post_type"]=="meta_event":
                pass
    except Exception as e:
        print(e)
        return False
        # continue
    # print(rev["post_type"])
    


if __name__ == '__main__':

    ws = websocket.WebSocketApp(
        ws_url,
        on_message=recv_msg,
        on_open=lambda _: logger.debug('连接成功......'),
        on_close=lambda _: logger.debug('重连中......'),
    )
    while True:
        ws.run_forever()
        time.sleep(5)

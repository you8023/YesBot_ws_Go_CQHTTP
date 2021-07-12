import websockets
import json

def send_message(msg,qq_id, ws,qq_type):
	if msg == "":
		return False
	if qq_type == "private":
		data = {
			'user_id':qq_id,
			'message':msg,
			'auto_escape':False
		}
		# cq_url = "ws://127.0.0.1:5700/send_private_msg"
		# with websockets.connect(cq_url) as websocket:
		# 	rev = websocket.send(json.dumps(data))
		action = "send_private_msg"
		post_data = json.dumps({"action": action, "params": data})
		# print(post_data)
		rev = ws.send(post_data)
	elif qq_type == "group":
		data = {
			'group_id':qq_id,
			'message':msg,
			'auto_escape':False
		}
		# cq_url = "ws://127.0.0.1:5700/send_group_msg"
		# with websockets.connect(cq_url) as websocket:
		# 	rev = websocket.send(json.dumps(data))
		action = "send_group_msg"
		post_data = json.dumps({"action": action, "params": data})
		rev = ws.send(post_data)
	elif qq_type == "friends":
		data = {
			'approve':msg['isOK'],
			'flag':msg['flag'],
			'remark':msg['friendsName']
		}
		action = "set_friend_add_request"
		post_data = json.dumps({"action": action, "params": data})
		rev = ws.send(post_data)
	else:
		return False
	# print(rev)
	if rev is None or rev['status'] == 'failed':
		return False
	else:
		# return ret['data']['message_id']
		# if json.loads(rev)['status'] == 'ok':
		return True
	return False
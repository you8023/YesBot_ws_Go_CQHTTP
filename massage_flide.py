import json
from data.load_data import read_file
from send_message.send_message import send_message
from send_message.talk_to_user import *
from random import randint
self_qq = json.load(open("./config.json", encoding='utf-8'))["self_qq"]
ban_words = json.load(open("./config.json", encoding='utf-8'))["ban_words"]
class msg_talker():
	def __init__(self):
		self.talk_data = read_file()

	def private_msg(self,rev, ws):
		if rev["sub_type"] != "friend":
			return send_message('你还不是我的好友呀',rev['user_id'], ws,"private")
		return send_message(talk_to_user(rev, self.talk_data, ws), rev["user_id"], ws, "private")

	def group_msg(self,rev, ws):
		if "[CQ:at,qq={}]".format(self_qq) in rev["raw_message"]:
			try:
				# print(rev)
				rev['raw_message']=rev['raw_message'].split("] ")[1]
			except Exception as e:
				print(e)
				pass
			return send_message(talk_to_group_user(rev, self.talk_data, ws), rev["group_id"], ws, "group")

		if randint(1,10)<4 or rev['raw_message'] in ban_words:	
			return send_message(talk_to_gourp(rev, self.talk_data, ws), rev["group_id"], ws, "group")
		return True
	def addFriends(self,rev, ws):
		return send_message(add_friends(rev, ws), rev["user_id"], ws, "friends")
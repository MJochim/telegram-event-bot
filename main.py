#!/usr/bin/python3

import sys
import time

from telepot import telepot
from telepot.telepot.delegate import pave_event_space, per_chat_id, create_open



if len(sys.argv) < 2:
	TOKEN = '<myDefaultToken>'
else:
	TOKEN = sys.argv[1]



class MessageCounter(telepot.helper.ChatHandler):
	def __init__(self, *args, **kwargs):
		super(MessageCounter, self).__init__(*args, **kwargs)
		self._count = 0

	def on_chat_message(self, msg):
		self._count += 1
		self.sender.sendMessage(self._count)



bot = telepot.DelegatorBot(TOKEN, [
	pave_event_space()(
		per_chat_id(), create_open, MessageCounter, timeout=10
	)
])

bot.message_loop(run_forever=True)

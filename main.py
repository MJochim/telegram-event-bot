#!/usr/bin/python3

from telepot import telepot
from telepot.telepot.delegate import include_callback_query_chat_id, pave_event_space, per_chat_id, create_open
from telepot.telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from EventChatHandler import EventChatHandler

TOKEN = ''

## Create the bot object, associate it with the handler class
bot = telepot.DelegatorBot(TOKEN, [
	include_callback_query_chat_id(pave_event_space()) (
		per_chat_id(), create_open, EventChatHandler, timeout=3600
	)
])

## Run the main loop
bot.message_loop(run_forever=True)

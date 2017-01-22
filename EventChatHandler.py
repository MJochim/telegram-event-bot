from telepot import telepot
from telepot.telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from Event import Event


legalPlaces = ['Osten', 'Westen']
legalDates = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']


class EventChatHandler(telepot.helper.ChatHandler):

	def __init__(self, *args, **kwargs):
		super(EventChatHandler, self).__init__(*args, **kwargs)
		
		self._events = []
		self._new_events = dict()


	## Overwrite _idle handler so that this instance only gets killed when
	## it holds no data
	def on__idle(self, event):
		if len(self._events) == 0:
			# The base-class on__idle() will terminate this instance
			# by raising an exception
			super(EventChatHandler, self).on__idle(event)


	def event_introduction(self, event):
		text = 'Juhu, wir gehen '
		if event and event.getDate() != '':
			text += 'am ' + event.getDate() + ' '
		if event and event.getPlace() != '':
			text += 'im ' + event.getPlace() + ' '
		text += 'zusammen klettern!'

		return text

		
	def new_event(self):
		event = Event()
		text = self.event_introduction(event)
		message = self.sender.sendMessage(text)
		message_id = telepot.message_identifier(message)
		
		self._new_events[message_id] = event
		
		self.ask_next_thing(message_id)

	
	def ask_next_thing(self, message_id):
		event = self._new_events[message_id]

		if event.getPlace() == '':
			self.ask_for_place(message_id)
		elif event.getDate() == '':
			self.ask_for_date(message_id)
		else:
			self.bot.editMessageText(message_id, self.event_introduction(event))
			self._events.append(self._new_events[message_id])
			del self._new_events[message_id]


	def ask_for_place(self, message_id): 
		event = self._new_events[message_id]
		text = self.event_introduction(event)

		text += "\n\nWo?"

		inline_keyboard = []
		for place in legalPlaces:
			inline_keyboard.append(
				[InlineKeyboardButton(text='Im '+place, callback_data='create_place='+place)]
			)
		markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

		self.bot.editMessageText(message_id, text=text, reply_markup = markup)


	def ask_for_date(self, message_id): 
		event = self._new_events[message_id]
		text = self.event_introduction(event)

		text += "\n\nWann?"

		inline_keyboard = []
		for day in legalDates:
			inline_keyboard.append(
				[InlineKeyboardButton(text='Am '+day, callback_data='create_date='+day)]
			)

		markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

		self.bot.editMessageText(message_id, text=text, reply_markup = markup)



	def on_callback_query(self, msg):
		# Evaluate data contained in the message
		origin = telepot.origin_identifier(msg)
		query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

		# Parse query_data, which is expected in the form
		# <command> <equality_sign> <parameter>
		command, sep, parameter = query_data.partition('=')
		
		if command == 'create_place' and parameter in legalPlaces:
			# Store place
			if origin not in self._new_events:
				self._new_events[origin] = Event()
			self._new_events[origin].setPlace(parameter)

			self.ask_next_thing(origin)

		elif command == 'create_date' and parameter in legalDates:
			if origin not in self._new_events:
				self._new_events[origin] = Event()
			self._new_events[origin].setDate(parameter)
			
			self.ask_next_thing(origin)

			


	def on_chat_message(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg)

		if content_type == 'text':
			text = msg['text'].lower()

			if text.startswith("/klettern"):
				self.new_event()
			elif text.startswith("/wann"):
				for i, v in enumerate(self._events):
					self.sender.sendMessage(self.event_introduction(v))

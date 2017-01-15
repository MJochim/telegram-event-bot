class Event:
	def __init__(self):
		self._date = ''
		self._place = ''
		self._participants = []

	def setDate(self, date):
		self._date = date

	def getDate(self):
		return self._date

	def setPlace(self, place):
		self._place = place
	
	def getPlace(self):
		return self._place

	def addParticipant(self, name):
		self._participants.push(name)

	def removeParticipant(self, name):
		self._participants.remove(name)

	def getParticipants(self):
		return self._participants

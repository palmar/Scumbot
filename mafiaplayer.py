import socket
import string
import sys

class mafiaplayer:

	def __init__(self):
		self.status = "Alive"
		self.votes = ""
		self.name = ""
		self.alignment = "Town"
		self.lynchvotes = 0

	def setplayername(self, string):
		self.name = string

	def addvote(self):
		self.lynchvotes = (self.lynchvotes + 1)
	def resetvote(self):
		self.lynchvotes = 0
	def votecount(self, votenumber):
		self.lynchvotes = votenumber
	def kill(self):
		self.status = "Dead"

	def setvotes(self, playername):
		self.votes = playername

	def setmafia(self):
		self.alignment = "Mafia"

	def getalignment(self):
		if self.alignment == "Mafia":
			print("Mafia")
		else:
			print("Town")

	def getstatus(self):
		if self.status == "Alive":
			print("Alive")
		else:
			print("Dead")

	def getname(self):
		return self.name

	def tostring(self):
		return "Player: " + self.name + " alignment: " + self.alignment + " status: " + self.status

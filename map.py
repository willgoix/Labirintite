import json
import os

class Map:

	def __init__(self, name, level, timeCounter, height, width, composition):
		self.name = name
		self.level = level
		self.timeCounter = timeCounter
		self.height = height
		self.width = width
		self.composition = composition

	def save(self):
		#Criar pasta \maps caso não exista
		if not os.path.isdir(os.getcwd() + "\\maps\\"):
			os.mkdir(os.getcwd() + "\\maps\\")

		file = open(os.getcwd() + "\\maps\\" + self.name.lower() +".json", 'w+')
		file.write(json.dumps(self.__dict__))
		file.close()

	def remove(self):
		if os.path.isdir(os.getcwd() + "\\maps\\"):
			os.remove(os.getcwd() + "\\maps\\" + self.name.lower() +".json")

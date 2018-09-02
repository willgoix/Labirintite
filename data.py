from json import loads, dumps
import os

playerData = None


def load_data():
	global playerData

	if os.path.isdir(os.getcwd() + "\\datas\\"):
		file = open(os.getcwd() + "\\datas\\datas.json", 'r+')

		jsonString = loads(file.read())

		player = PlayerData(
			jsonString['times']
		)

		playerData = player
		file.close()
	else:
		playerData = PlayerData({"1": -1})

def save_data():
	if not os.path.isdir(os.getcwd() + "\\datas\\"):
		os.mkdir(os.getcwd() + "\\datas\\")

	file = open(os.getcwd() + "\\datas\\datas.json", 'w+')
	file.write(dumps(playerData.__dict__))
	file.close()


class PlayerData:

	def __init__(self, times):
		self.times = times

	def unlock(self, map):
		self.times[str(map.level)] = -1

	def isLocked(self, map):
		return not str(map.level) in self.times


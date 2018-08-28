from os import system
from time import sleep
from libs.gui import *
from libs.thread import ThreadRepeat
import map_editor
import data


class Game:

	def __init__(self, map):
		self.map = map
		self.time = map.timeCounter
		self.moves = 0
		self.y = 0
		self.x = 0
		self.centralizerY = 0
		self.centralizerX = 0
		self.countersThread = None
		self.moveThread = None
		self.updatingCounters = False

		self.is_running = True
		self.is_winner = False

	def run(self):
		self.centralizerY = int(SCREEN_LINES / 2) - int(self.map.height / 2)
		self.centralizerX = int(SCREEN_COLUMNS / 2) - int(self.map.width / 1.3)

		for mapY in self.map.composition:
			for mapX in self.map.composition[mapY]:
				char = str(self.map.composition[mapY][mapX])
				mY = int(mapY) + self.centralizerY
				mX = int(mapX) + self.centralizerX

				if char == map_editor.SPAWN:
					self.y = mY
					self.x = mX
					console.setColorXY(mX, mY, ' ', Colors.BACKGROUND_RED)
				elif char == map_editor.FINAL:
					console.setColorXY(mX, mY, '*', Colors.FOREGROUND_GREEN)
				elif char == map_editor.WALL:
					console.setColorXY(mX, mY, ' ', Colors.BACKGROUND_YELLOW)
				else:
					console.setColorXY(mX, mY, ' ', Colors.BACKGROUND_BLACK | Colors.FOREGROUND_WHITE)

		console.setColor(Colors.BACKGROUND_BLACK | Colors.FOREGROUND_WHITE)
		console.setXY(int(SCREEN_COLUMNS / 2) + self.map.width, self.centralizerY, "Tempo restante: ")
		console.setXY(int(SCREEN_COLUMNS / 2) + self.map.width, self.centralizerY + 1, "Movimentos: ")
		self.countersThread = ThreadRepeat(self.updateCounters, 1)
		self.moveThread = ThreadRepeat(self.move, 0.1)
		self.countersThread.start()
		self.moveThread.start()

		#Forma encontrada para continuar o jogo, e conseguirmos finalizar esse while ao terminar
		while self.is_running:
			pass
		if self.is_winner:
			self.win()
		else:
			self.lose()

	def move(self):
		def validPosition(self, y, x):
			if not str(y) in self.map.composition or not str(x) in self.map.composition[str(y)] or self.map.composition[str(y)][str(x)] == map_editor.WALL:
				return False
			if self.map.composition[str(y)][str(x)] == map_editor.FINAL:
				self.is_winner = True
				self.is_running = False
				return False
			return True

		if self.updatingCounters:
			return

		key = console.getKeyword().lower()
		y = 0
		x = 0

		if key == 'up' or key == 'w':
			y -= 1
		elif key == 'down' or key == 's':
			y += 1
		elif key == 'right' or key == 'd':
			x += 1
		elif key == 'left' or key == 'a':
			x -= 1

		if y == 0 and x == 0:
			return

		if validPosition(self, self.y + y - self.centralizerY, self.x + x - self.centralizerX):
			self.moves += 1
			console.setColorXY(self.x, self.y, ' ', Colors.BACKGROUND_BLACK | Colors.FOREGROUND_WHITE)
			self.y += y
			self.x += x
			console.setColorXY(self.x, self.y, ' ', Colors.BACKGROUND_RED)

	def win(self):
		self.stop()

		record = False
		if self.map.name in data.playerData.times:
			if self.time > data.playerData.times[self.map.name]:
				record = True
				data.playerData.times[self.map.level] = self.time

				unlocked = map_editor.get_map_by_level(self.map.level + 1);
				if not unlocked == None:
					data.playerData.unlock(unlocked)

				data.save_data()
		else:
			record = True
			unlocked = map_editor.get_map_by_level(self.map.level + 1);
			if not unlocked == None:
				data.playerData.unlock(unlocked)

			data.playerData.times[self.map.level] = self.time
			data.save_data()

		banner = [" ",
				  " #     #                       #     #                                  #",
				  " #     #  ####   ####  ####    #     #  ####  #   #  ####  ####  #   #  #",
				  " #     # #    # #     #    #   #     # #    # ##  # #     #    # #   #  #",
				  "  #   #  #    # #     ######    #   #  ###### # # # #     ###### #   #  #",
				  "   # #   #    # #     #          # #   #      #  ## #     #      #   #   ",
				  "    #     ####   ####  ####       #     ####  #   #  ####  ####  #####  #",
				  " "]
		lines = int(SCREEN_LINES / 3)
		colums = int(SCREEN_COLUMNS / 5)

		console.setColorXY(colums, lines + len(banner) + 2, "                        Terminou em "+ str(self.map.timeCounter - self.time) +" segundos!", Colors.FOREGROUND_GREEN)
		if record:
			console.setColorXY(colums, lines + len(banner) + 3, "                    Você bateu seu record de tempo!", Colors.FOREGROUND_YELLOW)
		for yBanner in range(lines, lines + len(banner)):
			for xBanner in range(colums, colums + len(banner[yBanner - lines])):
				text = banner[yBanner - lines][xBanner - colums]

				if text == '#':
					console.setColorXY(xBanner, yBanner, ' ', Colors.BACKGROUND_GREEN | Colors.BACKGROUND_BOLD)

		sleep(3)
		from menu import play
		play()

	def lose(self):
		self.stop()
		banner = [" ",
				  " #     #                       ######                                   #",
				  " #     #  ####   ####  ####    #     #  ####  # ###     #  ####  #   #  #",
				  " #     # #    # #     #    #   #     # #    # ##     #### #    # #   #  #",
				  "  #   #  #    # #     ######   ######  ###### #     #   # ###### #   #  #",
				  "   # #   #    # #     #        #       #      #     #   # #      #   #   ",
				  "    #     ####   ####  ####    #        ####  #      ####  ####  #####  #",
				  " "]

		lines = int(SCREEN_LINES / 3)
		colums = int(SCREEN_COLUMNS / 5)
		for yBanner in range(lines, lines + len(banner)):
			for xBanner in range(colums, colums + len(banner[yBanner - lines])):
				text = banner[yBanner - lines][xBanner - colums]

				if text == '#':
					console.setColorXY(xBanner, yBanner, ' ', Colors.BACKGROUND_RED | Colors.BACKGROUND_BOLD)

		sleep(3)
		from menu import play
		play()

	def stop(self):
		self.countersThread.stop()
		self.moveThread.stop()
		del self.countersThread
		del self.moveThread

		console.setColorXY(0, 0, ' ', Colors.BACKGROUND_BLACK)

		#Vai atualizar com fundo preto
		system('mode con: cols={} lines={}'.format(SCREEN_COLUMNS - 1, SCREEN_LINES - 1))
		system('mode con: cols={} lines={}'.format(SCREEN_COLUMNS, SCREEN_LINES))

		for mapY in self.map.composition:
			for mapX in self.map.composition[mapY]:
				mY = int(mapY) + self.centralizerY
				mX = int(mapX) + self.centralizerX

				console.setColorXY(mX, mY, ' ', Colors.BACKGROUND_BLACK)

	def updateCounters(self):
		self.time -= 1

		if self.time <= 0:
			self.is_winner = False
			self.is_running = False
			return

		seconds = self.time
		minutes = 0
		while seconds >= 60:
			seconds -= 60
			minutes += 1

		#Counters e Move estão em Thread separadas, porém, ainda utilizam o mesmo sistema do setXY, então
		#os dois usando o método ao mesmo tempo pode acabar bugando
		self.updatingCounters = True
		console.setColor(Colors.BACKGROUND_BLACK | Colors.FOREGROUND_YELLOW | Colors.FOREGROUND_BOLD)
		console.setXY(int(SCREEN_COLUMNS / 2) + self.map.width + 16, self.centralizerY, str(minutes) +":"+ str(seconds) + " ")
		console.setXY(int(SCREEN_COLUMNS / 2) + self.map.width + 12, self.centralizerY + 1, str(self.moves) + " ")
		self.updatingCounters = False


SCREEN_COLUMNS = 120
SCREEN_LINES = 45

def run_game(map):
	try:
		system('mode con: cols={} lines={}'.format(SCREEN_COLUMNS, SCREEN_LINES))

		game = Game(map)
		game.run()
	except Exception as e:
		print("OCORREU UM ERRO NO JOGO: ", e)
		sleep(1000)

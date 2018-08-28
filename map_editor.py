from functools import partial
from random import shuffle, randrange
from time import sleep
from json import loads
from os import system
from map import Map
from libs import Colors, console
from libs.gui import *
import os

MAPS = []
LOADED = False

SPACE = ' '
WALL = '#'
SPAWN = 'S'
FINAL = 'F'


def load_maps():
	global LOADED
	if LOADED:
		return
	LOADED = True

	if os.path.isdir(os.getcwd() + "\\maps\\"):
		for fileName in os.listdir(os.getcwd() + "\\maps"):
			if fileName.endswith(".json"):
				file = open(os.getcwd() + "\\maps\\" + fileName, 'r+')

				jsonString = loads(file.read())

				map = Map(
					jsonString['name'],
					jsonString['level'],
					jsonString['timeCounter'],
					jsonString['height'],
					jsonString['width'],
					jsonString['composition']
				)

				MAPS.append(map)
				file.close()

"""
	Fonte: https://pt.stackoverflow.com/questions/70101/como-funciona-este-código-que-gera-um-labirinto
	Algorítmo adaptado.
"""
def generate_composition(height, width):
	height = int(height / 2)
	width = int(width / 2)
	composition = {}

	vis = [[0] * width + [1] for _ in range(height)] + [[1] * (width + 1)]
	ver = [[WALL + SPACE + SPACE] * width + [WALL] for _ in range(height)] + [[]]
	hor = [[WALL * 3] * width + [WALL] for _ in range(width + 1)]

	def walk(x, y):
		vis[y][x] = 1

		d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
		shuffle(d)
		for (xx, yy) in d:
			if vis[yy][xx]: continue
			if xx == x: hor[max(y, yy)][x] = WALL + SPACE * 2
			if yy == y: ver[y][max(x, xx)] = SPACE * 3
			walk(xx, yy)

	walk(randrange(width), randrange(height))

	lines = []
	for (a, b) in zip(hor, ver):
		lines.append(''.join(a))
		lines.append(''.join(b))

	for y in range(0, len(lines)):
		composition[y] = {}

		for x in range(0, len(lines[y])):
			composition[y][x] = lines[y][x]

	return composition

def get_map_by_name(map_name):
	for map in MAPS:
		if map.name == map_name.lower():
			return map

def get_map_by_level(map_level):
	for map in MAPS:
		if map.level == map_level:
			return map




#####################################




SCREEN_COLUMNS = 120
SCREEN_LINES = 55
gui = None

def run_editor():
	try:
		system('mode con: cols={} lines={}'.format(SCREEN_COLUMNS, SCREEN_LINES))
		load_maps()

		global gui
		gui = GUI(4, 0)

		gui.addButton(1, 0, GUIButton('blank', ["   W / S / A / D = Movimentar para cima/baixo/esquerda/direita"]))
		gui.addButton(2, 0, GUIButton('blank', ["   Enter = Clicar"]))
		gui.addButton(4, 0, GUIButton("Criar um Mapa", [" + Criar um Mapa"], lambda: create_map(), partial(select_map, None), Colors.FOREGROUND_WHITE, Colors.FOREGROUND_BLACK, Colors.BACKGROUND_GREEN, Colors.BACKGROUND_GREEN))

		i = 5
		for map in MAPS:
			i += 1
			gui.addButton(i, 0, GUIButton(map.name, ["   " + str(i - 5) + ". " + map.name + " [Nível: "+ str(map.level) +"] (y: " + str(map.height) + ", x: " + str(map.width) + ")"], partial(edit_map, map), partial(select_map, map)))

		gui.addButton(i + 2, 0, GUIButton("Voltar", [" < Voltar ao menu"], partial(back_to, "menu"), partial(select_map, None), Colors.FOREGROUND_WHITE, Colors.FOREGROUND_BLACK, Colors.BACKGROUND_RED, Colors.BACKGROUND_RED))
		gui.display()
	except Exception as e:
		print('OCORREU UM ERRO NO EDITOR DE MAPAS: ', e)
		sleep(1000)

SELECTED_HEIGHT = 0
SELECTED_WIDTH = 0

def select_map(map):
	global SELECTED_HEIGHT
	global SELECTED_WIDTH
	global gui
	spacerY = len(gui.buttons) + 3
	spacerX = 5

	for selY in range(spacerY, spacerY + SELECTED_HEIGHT):
		for selX in range(spacerX, spacerX + SELECTED_WIDTH):
			console.setColorXY(selX, selY, ' ', Colors.FOREGROUND_WHITE | Colors.BACKGROUND_BLACK)
	for editMessageX in range(0, len("Clique para editar!")):
		console.setColorXY(spacerX + editMessageX, spacerY - 2, " ", Colors.FOREGROUND_WHITE | Colors.BACKGROUND_BLACK)

	if not map == None:
		for y in map.composition:
			for x in map.composition[y]:
				console.setColorXY(int(x) + spacerX, int(y) + spacerY, map.composition[y][x], Colors.FOREGROUND_WHITE | Colors.BACKGROUND_BLACK)
		SELECTED_HEIGHT = map.height + 2 		 #Números não precísos pois a altura pode variar um pouco pra cima/baixo por conta do algorítmo de geração automática
		SELECTED_WIDTH = map.width * 2 + spacerX #Números não precísos pois a largura pode variar um pouco pra cima/baixo por conta do algorítmo de geração automática
		console.setColorXY(spacerX, spacerY - 2, "Clique para editar!", Colors.FOREGROUND_WHITE | Colors.BACKGROUND_BLACK)

def edit_map(map, startY = 0, startX = 0):
	global SELECTED_WIDTH
	global gui
	gui.stop()
	spacerY = 3 + (len(MAPS) + 8)
	spacerX = 5
	del gui

	gui = GUI(spacerY + startY, spacerX + startX)

	for y in map.composition:
		for x in map.composition[y]:
			gui.addButton(int(y) + spacerY, int(x) + spacerX, GUIButton("Map"+ str(y) + str(x), [map.composition[y][x]], partial(new_character, gui, map, y, x)))

	gui.addButton(spacerY, SELECTED_WIDTH, GUIButton("Voltar", ["   /\ Voltar /\\  "], partial(back_to, "editor"), None, Colors.FOREGROUND_WHITE, Colors.FOREGROUND_BLACK, Colors.BACKGROUND_RED, Colors.BACKGROUND_RED))
	gui.addButton(spacerY + 2, SELECTED_WIDTH, GUIButton("Deletar", ["> Deletar mapa"], partial(delete_map, map), None, Colors.FOREGROUND_WHITE, Colors.FOREGROUND_BLACK, Colors.BACKGROUND_RED, Colors.BACKGROUND_RED))
	gui.addButton(spacerY + 4, SELECTED_WIDTH, GUIButton("blank", ["Selecione e modifique clicando!"]))
	gui.addButton(spacerY + 5, SELECTED_WIDTH, GUIButton("blank", ["# = Parede"]))
	gui.addButton(spacerY + 6, SELECTED_WIDTH, GUIButton("blank", ["S = Spawn (Início)"]))
	gui.addButton(spacerY + 7, SELECTED_WIDTH, GUIButton("blank", ["F = Final (Chegada)"]))

	gui.display()

def new_character(gui, map, y, x):
	caracters = {SPACE: WALL, WALL: SPAWN, SPAWN: FINAL, FINAL: SPACE}
	newChar = caracters[map.composition[y][x]]

	map.composition[y][x] = newChar
	map.save()

	edit_map(map, int(y), int(x))

CREATING_MAP_NAME = ""
CREATING_MAP_HEIGHT = ""
CREATING_MAP_WIDTH = ""
CREATING_MAP_TIME = ""
CREATING_MAP_AUTO_GENERATION = ""
CREATING_MAP_THREAD = None

def create_map():
	global gui
	gui.stop()
	del gui

	gui = GUI(len(MAPS) + 12, 5)
	global CREATING_MAP_NAME
	global CREATING_MAP_HEIGHT
	global CREATING_MAP_TIME
	global CREATING_MAP_AUTO_GENERATION
	global CREATING_MAP_THREAD
	if not CREATING_MAP_THREAD is None:
		CREATING_MAP_THREAD.stop()
		CREATING_MAP_THREAD = None

	def clickInputName(buttonY, buttonX):
		global CREATING_MAP_THREAD

		def verifyName(buttonY, buttonX):
			for x in range(buttonX, buttonX + 10):
				console.setXY(x, buttonY, ' ')
			global CREATING_MAP_NAME
			console.setXY(buttonX, buttonY, CREATING_MAP_NAME)

			while True:
				keyword = str(console.getKeyword())

				if keyword == 'delete':
					console.setXY(buttonX + len(CREATING_MAP_NAME) - 1, buttonY, ' ')
					CREATING_MAP_NAME = CREATING_MAP_NAME[0:len(CREATING_MAP_NAME) - 1] if len(CREATING_MAP_NAME) > 1 else ""
					console.setXY(buttonX, buttonY, CREATING_MAP_NAME)
				elif keyword == 'enter':
					create_map()
					break
				else:
					CREATING_MAP_NAME += keyword
					console.setXY(buttonX, buttonY, CREATING_MAP_NAME)

		CREATING_MAP_THREAD = ThreadRepeat(partial(verifyName, buttonY, buttonX))
		CREATING_MAP_THREAD.run()

	def clickInputHeight(buttonY, buttonX):
		global CREATING_MAP_THREAD

		def verifyHeight(buttonY, buttonX):
			for x in range(buttonX, buttonX + 10):
				console.setXY(x, buttonY, ' ')
			global CREATING_MAP_HEIGHT
			console.setXY(buttonX, buttonY, CREATING_MAP_HEIGHT)

			while True:
				keyword = str(console.getKeyword())

				if keyword == 'delete':
					console.setXY(buttonX + len(CREATING_MAP_HEIGHT) - 1, buttonY, ' ')
					CREATING_MAP_HEIGHT = CREATING_MAP_HEIGHT[0:len(CREATING_MAP_HEIGHT) - 1] if len(CREATING_MAP_HEIGHT) > 1 else ""
					console.setXY(buttonX, buttonY, CREATING_MAP_HEIGHT)
				elif keyword == 'enter':
					create_map()
					break
				else:
					CREATING_MAP_HEIGHT += keyword
					console.setXY(buttonX, buttonY, CREATING_MAP_HEIGHT)

		CREATING_MAP_THREAD = ThreadRepeat(partial(verifyHeight, buttonY, buttonX))
		CREATING_MAP_THREAD.run()

	def clickInputWidth(buttonY, buttonX):
		global CREATING_MAP_THREAD

		def verifyWidth(buttonY, buttonX):
			for x in range(buttonX, buttonX + 10):
				console.setXY(x, buttonY, ' ')
			global CREATING_MAP_WIDTH
			console.setXY(buttonX, buttonY, CREATING_MAP_WIDTH)

			while True:
				keyword = str(console.getKeyword())

				if keyword == 'delete':
					console.setXY(buttonX + len(CREATING_MAP_WIDTH) - 1, buttonY, ' ')
					CREATING_MAP_WIDTH = CREATING_MAP_WIDTH[0:len(CREATING_MAP_WIDTH) - 1] if len(CREATING_MAP_WIDTH) > 1 else ""
					console.setXY(buttonX, buttonY, CREATING_MAP_WIDTH)
				elif keyword == 'enter':
					create_map()
					break
				else:
					CREATING_MAP_WIDTH += keyword
					console.setXY(buttonX, buttonY, CREATING_MAP_WIDTH)

		CREATING_MAP_THREAD = ThreadRepeat(partial(verifyWidth, buttonY, buttonX))
		CREATING_MAP_THREAD.run()

	def clickInputTime(buttonY, buttonX):
		global CREATING_MAP_THREAD

		def verifyTime(buttonY, buttonX):
			for x in range(buttonX, buttonX + 10):
				console.setXY(x, buttonY, ' ')
			global CREATING_MAP_TIME
			console.setXY(buttonX, buttonY, CREATING_MAP_TIME)

			while True:
				keyword = str(console.getKeyword())

				if keyword == 'delete':
					console.setXY(buttonX + len(CREATING_MAP_TIME) - 1, buttonY, ' ')
					CREATING_MAP_TIME = CREATING_MAP_TIME[0:len(CREATING_MAP_TIME) - 1] if len(CREATING_MAP_TIME) > 1 else ""
					console.setXY(buttonX, buttonY, CREATING_MAP_TIME)
				elif keyword == 'enter':
					create_map()
					break
				else:
					CREATING_MAP_TIME += keyword
					console.setXY(buttonX, buttonY, CREATING_MAP_TIME)

		CREATING_MAP_THREAD = ThreadRepeat(partial(verifyTime, buttonY, buttonX))
		CREATING_MAP_THREAD.run()

	def clickInputAutoGeneration(buttonY, buttonX):
		global CREATING_MAP_THREAD

		def verifyAutoGeneration(buttonY, buttonX):
			for x in range(buttonX, buttonX + 10):
				console.setXY(x, buttonY, ' ')
			global CREATING_MAP_AUTO_GENERATION
			if CREATING_MAP_AUTO_GENERATION == "NAO":
				console.setColorXY(buttonX + 1, buttonY, "SIM / ", Colors.BACKGROUND_BLACK | Colors.FOREGROUND_WHITE)
				console.setColorXY(buttonX + 7, buttonY, "NAO", Colors.BACKGROUND_RED)
			else:
				console.setColorXY(buttonX + 1 , buttonY, "SIM", Colors.BACKGROUND_GREEN)
				console.setColorXY(buttonX + 4, buttonY, " / NAO", Colors.BACKGROUND_BLACK | Colors.FOREGROUND_WHITE)
			option = "SIM"

			while True:
				keyword = str(console.getKeyword())

				if keyword == 'right' or keyword == 'd':
					option = "NAO"

					console.setColorXY(buttonX + 1, buttonY, "SIM / ", Colors.BACKGROUND_BLACK | Colors.FOREGROUND_WHITE)
					console.setColorXY(buttonX + 7, buttonY, "NAO", Colors.BACKGROUND_RED)
				elif keyword == 'left' or keyword == 'a':
					option = "SIM"

					console.setColorXY(buttonX + 1, buttonY, "SIM", Colors.BACKGROUND_GREEN)
					console.setColorXY(buttonX + 4, buttonY, " / NAO", Colors.BACKGROUND_BLACK | Colors.FOREGROUND_WHITE)
				elif keyword == 'enter':
					for x in range(buttonX, buttonX + 10):
						console.setColorXY(x, buttonY, ' ', Colors.BACKGROUND_BLACK | Colors.FOREGROUND_WHITE)
					CREATING_MAP_AUTO_GENERATION = option
					create_map()
					break

		CREATING_MAP_THREAD = ThreadRepeat(partial(verifyAutoGeneration, buttonY, buttonX))
		CREATING_MAP_THREAD.run()

	def confirm(gui):
		global CREATING_MAP_NAME

		if not get_map_by_name(CREATING_MAP_NAME) is None:
			console.setColorXY(5, len(MAPS) + 20, " >> Já existe um mapa com esse nome...", Colors.BACKGROUND_RED | Colors.FOREGROUND_WHITE)
		else:
			global CREATING_MAP_HEIGHT
			global CREATING_MAP_WIDTH
			global CREATING_MAP_TIME
			global CREATING_MAP_AUTO_GENERATION

			if CREATING_MAP_HEIGHT == "" or CREATING_MAP_WIDTH == "" or CREATING_MAP_TIME == "" or CREATING_MAP_AUTO_GENERATION == "":
				console.setColorXY(5, len(MAPS) + 20, " >> Um dos campos não foi preenchido...", Colors.BACKGROUND_RED | Colors.FOREGROUND_WHITE)
			elif not CREATING_MAP_HEIGHT.isdigit() or not CREATING_MAP_WIDTH.isdigit() or not CREATING_MAP_TIME.isdigit():
				console.setColorXY(5, len(MAPS) + 20, " >> O valor do campo Altura, Largura ou o Tempo não é um número válido...", Colors.BACKGROUND_RED | Colors.FOREGROUND_WHITE)
			else:
				composition = {}

				if CREATING_MAP_AUTO_GENERATION == "SIM":
					composition = generate_composition(int(CREATING_MAP_HEIGHT), int(CREATING_MAP_WIDTH))
				else:
					for y in range(0, int(CREATING_MAP_HEIGHT)):
						composition[y] = {}
						for x in range(0, int(CREATING_MAP_WIDTH)):
							if y == 0 or y == int(CREATING_MAP_HEIGHT) - 1 or x == 0 or x == int(CREATING_MAP_WIDTH) - 1:
								composition[y][x] = WALL
							else:
								composition[y][x] = SPACE

				map = Map(CREATING_MAP_NAME, len(MAPS) + 1, int(CREATING_MAP_TIME), int(CREATING_MAP_HEIGHT), int(CREATING_MAP_WIDTH), composition)
				map.save()
				MAPS.append(map)
				console.setColorXY(5, len(MAPS) + 20, " >> Mapa criado com sucesso!", Colors.BACKGROUND_GREEN | Colors.FOREGROUND_WHITE)
		sleep(3)
		gui.stop()
		del gui

		console.clear()
		run_editor()

	def cancel(gui):
		global CREATING_MAP_NAME
		global CREATING_MAP_HEIGHT
		global CREATING_MAP_WIDTH
		global CREATING_MAP_TIME
		global CREATING_MAP_AUTO_GENERATION
		global CREATING_MAP_THREAD

		CREATING_MAP_NAME = ""
		CREATING_MAP_HEIGHT = ""
		CREATING_MAP_WIDTH = ""
		CREATING_MAP_TIME = ""
		CREATING_MAP_AUTO_GENERATION = ""
		CREATING_MAP_THREAD = None

		console.clear()
		run_editor()

	prefixButtonName = "Nome: "
	prefixButtonHeight = "Altura: "
	prefixButtonWidth = "Largura: "
	prefixButtonTime = "Tempo (em segundos): "
	prefixButtonAutoGeneration = "Geracao automatica: "
	gui.addButton(len(MAPS) + 10, 5, GUIButton("blank", ["Selecione, clique e preencha os campos para criar o mapa!"]))
	gui.addButton(len(MAPS) + 11, 5, GUIButton("blank"))
	gui.addButton(len(MAPS) + 12, 5, GUIButton("inputName", [prefixButtonName + ("__________" if CREATING_MAP_NAME == "" else CREATING_MAP_NAME)], partial(clickInputName, len(MAPS) + 12, len(prefixButtonName) + 5)))
	gui.addButton(len(MAPS) + 13, 5, GUIButton("inputHeight", [prefixButtonHeight + ("__________" if CREATING_MAP_HEIGHT == "" else CREATING_MAP_HEIGHT)], partial(clickInputHeight, len(MAPS) + 13, len(prefixButtonHeight) + 5)))
	gui.addButton(len(MAPS) + 14, 5, GUIButton("inputWidth", [prefixButtonWidth + ("__________" if CREATING_MAP_WIDTH == "" else CREATING_MAP_WIDTH)], partial(clickInputWidth, len(MAPS) + 14, len(prefixButtonWidth) + 5)))
	gui.addButton(len(MAPS) + 15, 5, GUIButton("inputTime", [prefixButtonTime + ("__________" if CREATING_MAP_TIME == "" else CREATING_MAP_TIME)], partial(clickInputTime, len(MAPS) + 15, len(prefixButtonTime) + 5)))
	gui.addButton(len(MAPS) + 16, 5, GUIButton("inputAutoGeneration", [prefixButtonAutoGeneration + ("__________" if CREATING_MAP_AUTO_GENERATION == "" else CREATING_MAP_AUTO_GENERATION)], partial(clickInputAutoGeneration, len(MAPS) + 16, len(prefixButtonAutoGeneration) + 5)))
	gui.addButton(len(MAPS) + 17, 5, GUIButton("blank"))
	gui.addButton(len(MAPS) + 18, 5, GUIButton("confirm", ["Confirmar e Criar!"], partial(confirm, gui), None, Colors.FOREGROUND_WHITE, Colors.FOREGROUND_BLACK, Colors.BACKGROUND_GREEN, Colors.BACKGROUND_GREEN))
	gui.addButton(len(MAPS) + 18, 7, GUIButton("cancel", ["Cancelar!"], partial(cancel, gui), None, Colors.FOREGROUND_WHITE, Colors.FOREGROUND_BLACK, Colors.BACKGROUND_RED, Colors.BACKGROUND_RED))

	gui.display()

def delete_map(map):
	MAPS.remove(map)
	map.remove()
	back_to("editor")

def back_to(to):
	global gui
	gui.stop()
	del gui
	console.clear()

	if to == "menu":
		from menu import run_menu
		run_menu()
	elif to == "editor":
		run_editor()

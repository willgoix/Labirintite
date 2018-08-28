from time import sleep
from functools import partial
from os import system
from libs import Colors, console
from libs.gui import *
import map_editor
import data

SCREEN_COLUMNS = 100
SCREEN_LINES = 30

gui = None

def play():
	global gui
	if not gui == None:
		gui.stop()
	console.clear()

	banner = [" ",
			  " ",
			  " ###                                           ###",
			  "#      ##  #    ##   ## #  ##  #  #  ### # #   #    ### ###  ##",
			  " ###  #### #   #### #     #  # ## # #  # ##    ##  #  # ##  ####",
			  "    # #    #   #    #   # #  # # ## #  # #     #   #  #  ## #",
			  " ###   ##  ###  ##   ## #  ##  #  #  ### #     #    ### ###  ##"]
	for yBanner in range(0, len(banner)):
		for xBanner in range(0, len(banner[yBanner])):
			text = banner[yBanner][xBanner]

			if text == '#':
				console.setColorXY(xBanner + int(SCREEN_COLUMNS / 6), yBanner, ' ', Colors.BACKGROUND_YELLOW | Colors.BACKGROUND_BOLD)
	console.setColor(Colors.BACKGROUND_BLACK | Colors.FOREGROUND_WHITE)

	data.load_data()
	map_editor.load_maps()

	gui = GUI(10, 0)

	for mapIndex in range(0, len(map_editor.MAPS)):
		map = map_editor.MAPS[mapIndex]

		if data.playerData.isLocked(map):
			gui.addButton(mapIndex + 10, 0, GUIButton(map.name, ["     ?. ?????        Melhor tempo: --:--"], partial(play_map, map), colorBackSelected = Colors.BACKGROUND_RED, colorForeSelected = Colors.FOREGROUND_WHITE))
		else:
			timeString = ""
			if data.playerData.times[str(map.level)] == -1:
				timeString = "--:--"
			else:
				seconds = map.timeCounter - data.playerData.times[str(map.level)]
				minutes = 0
				while seconds >= 60:
					seconds -= 60
					minutes += 1

				timeString = str(minutes) +":"+ str(seconds)

			gui.addButton(mapIndex + 10, 0, GUIButton(map.name, ["     "+ str(mapIndex + 1) +". "+ map.name +"        Melhor tempo: "+ timeString], partial(play_map, map)))

	gui.addButton(len(map_editor.MAPS) + 11, 0, GUIButton("Voltar", ["     < Voltar ao menu"], lambda: back(), None, Colors.FOREGROUND_WHITE, Colors.FOREGROUND_BLACK, Colors.BACKGROUND_RED, Colors.BACKGROUND_RED))
	gui.display()

def play_map(map):
	if data.playerData.isLocked(map):
		return
	global gui
	if not gui == None:
		gui.stop()
	console.clear()

	from game import run_game
	run_game(map)

def back():
	global gui
	if not gui is None:
		gui.stop()
	console.clear()

	run_menu()

def run_map_editor():
	global gui
	gui.stop()
	del gui
	console.clear()

	from map_editor import run_editor
	run_editor()

def instructions():
	global gui
	if not gui == None:
		gui.stop()
	console.clear()


	banner = [" ",
			  " ",
			  "###",
			  " #  #  # ### ### # ## # #  ##  ##   ##  ###",
			  " #  ## # ##   #  ##   # # #   #  # #### ##",
			  " #  # ##  ##  #  #    # # #   #  # #     ##",
			  "### #  # ###  #  #    ###  ##  ##   ##  ###"]
	for yBanner in range(0, len(banner)):
		for xBanner in range(0, len(banner[yBanner])):
			text = banner[yBanner][xBanner]

			if text == '#':
				console.setColorXY(xBanner + int(SCREEN_COLUMNS / 6), yBanner, ' ',
								   Colors.BACKGROUND_YELLOW | Colors.BACKGROUND_BOLD)
	console.setColor(Colors.BACKGROUND_BLACK | Colors.FOREGROUND_WHITE)

	gui = GUI(len(banner) + 16, 0)

	gui.addButton(len(banner) + 5, 0, GUIButton('1', ["   Instruções:"]))
	gui.addButton(len(banner) + 7, 0, GUIButton('2', ["        W = Mover para cima"]))
	gui.addButton(len(banner) + 8, 0, GUIButton('3', ["        S = Mover para baixo"]))
	gui.addButton(len(banner) + 9, 0, GUIButton('4', ["        A = Mover para esquerda"]))
	gui.addButton(len(banner) + 10, 0, GUIButton('5', ["        D = Mover para direita"]))
	gui.addButton(len(banner) + 11, 0, GUIButton('6', ["        (ou, utilize as setas)"]))
	gui.addButton(len(banner) + 13, 0, GUIButton('7', ["    * Seu objetivo é encontrar a saída do labirinto (ponto VERDE)"]))
	gui.addButton(len(banner) + 14, 0, GUIButton('8', ["      dentro do tempo limite, para assim, liberar a próxima fase!"]))
	gui.addButton(len(banner) + 16, 0, GUIButton("Voltar", ["     < Voltar ao menu"], lambda: back(), None, Colors.FOREGROUND_WHITE, Colors.FOREGROUND_BLACK, Colors.BACKGROUND_RED, Colors.BACKGROUND_RED))

	gui.display()


def run_menu():
	try:
		system('mode con: cols={} lines={}'.format(SCREEN_COLUMNS, SCREEN_LINES))

		banner = [" ",
				  " ",
				  " ",
				  " ",
				  " ",
				  "#                   ",
				  "#      #####  #     #  # ##  #  ###    #    #   #     ####",
				  "#     #    #  ###      ##       #  #  ###      ###   #    #",
			      "#     #    #  #  #  #  #     #  #  #   #    #   #    ######",
				  "#     #    #  #  #  #  #     #  #  #   #    #   #    #",
				  "####   #####  ###   #  #     #  #  #    ##  #    ##   ####"]
		spacer = int(SCREEN_COLUMNS / 5)
		for yBanner in range(0, len(banner)):
			for xBanner in range(0, len(banner[yBanner])):
				text = banner[yBanner][xBanner]

				if text == '#':
					console.setColorXY(xBanner + spacer, yBanner, ' ', Colors.BACKGROUND_YELLOW | Colors.BACKGROUND_BOLD)
		console.setColorXY(spacer, len(banner) + 3, "          Criado por Willian Gois & Lucas Verona", Colors.FOREGROUND_YELLOW)

		global gui
		gui = GUI(20, int(SCREEN_LINES / 2))

		gui.addButton(20, int(SCREEN_LINES / 2), GUIButton("Jogar", ["         ",
												  "  Jogar  ",
												  "         "], lambda: play()))
		gui.addButton(20, int(SCREEN_LINES / 1), GUIButton("Editor de Mapas", ["                  ",
															"  Editor de Mapa  ",
															"                  "], lambda: run_map_editor()))
		gui.addButton(20, int(SCREEN_LINES / 0.65), GUIButton("Instruções", ["              ",
													   "  Instrucoes  ",
													   "              "], lambda: instructions()))
		gui.display()
	except Exception as e:
		print("ERRO GERAL: ", e)
		sleep(1000)

if __name__ == "__main__":
	run_menu()

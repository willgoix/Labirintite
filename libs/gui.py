from libs import Colors, console
from libs.thread import ThreadRepeat

class GUI:

	def __init__(self, startY = 0, startX = 0):
		self.y = startY
		self.x = startX
		self.buttons = {}
		self.paused = False
		self.thread = None

		self.lastY = 0
		self.lastsX = {}

	def stop(self):
		GUIButton.lastY = 0
		GUIButton.lastY = {}
		if not self.thread == None:
			self.thread.stop()

	def display(self):
		for y in self.buttons:
			for x in self.buttons[y]:
				self.buttons[y][x].adapt(y, self)
				
				#if not self.buttons[y][x].name == 'blank':
				self.buttons[y][x].update(self.y == y and self.x == x)

		# Evitar bugs caso o tamanho da janela do console seja mudado
		console.setColor(Colors.BACKGROUND_BLACK | Colors.FOREGROUND_WHITE)

		self.thread = ThreadRepeat(self.update)
		self.thread.run()

	def update(self):
		keyword = console.getKeyword().lower();
		r = ''

		if (keyword == 'up' or keyword == 'w'):
			r = 'up'
			self.up()
		elif (keyword == 'down' or keyword == 's'):
			r = 'down'
			self.down();
		elif (keyword == 'left' or keyword == 'a'):
			r = 'left'
			self.left();
		elif (keyword == 'right' or keyword == 'd'):
			r = 'right'
			self.right();
		elif (keyword == 'enter' or keyword == 's' or keyword == 'w'):
			r = 'click'
			self.click()

			# Evitar bugs caso o tamanho da janela do console seja mudado
		console.setColor(Colors.BACKGROUND_BLACK | Colors.FOREGROUND_WHITE)
			#return r

	def up(self):
		oldButton = self.buttons[self.y][self.x]
		oldButton.update(False)
		
		if self.y - 1 < 0 or self.y - 1 in self.buttons and not self.x in self.buttons[self.y - 1]:
			self.y = len(self.buttons) - 1
		else:
			self.y -= 1
		
		button = self.buttons[self.y][self.x]
		if button.name.lower() == 'blank':
			self.up()
		else:
			button.update(True)

	def down(self):
		oldButton = self.buttons[self.y][self.x]
		oldButton.update(False)

		if self.y + 1 >= len(self.buttons) or self.y + 1 in self.buttons and not self.x in self.buttons[self.y + 1]:
		#if not self.y + 1 in self.buttons:
			lower = 10000
			for y in self.buttons:
				if y < lower and self.x in self.buttons[y]:
					lower = y
			self.y = lower
		else:
			self.y += 1

		button = self.buttons[self.y][self.x]
		if button.name.lower() == 'blank':
			self.down()
		else:
			button.update(True)

	def right(self):
		oldButton = self.buttons[self.y][self.x]
		oldButton.update(False)

		if self.x + 1 >= len(self.buttons[self.y]):
			self.x = 0
		else:
			self.x += 1

		button = self.buttons[self.y][self.x]
		if button.name.lower() == 'blank':
			self.right()
		else:
			button.update(True)

	def left(self):
		oldButton = self.buttons[self.y][self.x]
		oldButton.update(False)

		if self.x - 1 < 0:
			self.x = len(self.buttons[self.y]) - 1
		else:
			self.x -= 1

		button = self.buttons[self.y][self.x]
		if button.name.lower() == 'blank':
			self.left()
		else:
			button.update(True)

	def click(self):
		selectedButton = self.buttons[self.y][self.x]
		selectedButton.click()

	# Y e X representam o posicionamento de uma matriz imaginaria dos botões.
	# Ambos podem ser editados simultaneamente na formação BOTH (ambos), onde você fica
	# livre para editar o posicionamento. (os posicionamentos que você não utilizar serão
	# preenchidos com um GUIButton('blank'), vazio)

	def addButton(self, Y, X, button):
		#if len(self.buttons) == 0:
		#	self.buttons[0] = {}

		#se y1 x5
		#preencher y0, x0, x1, x2, x3, x4
		#sabendo que len(button.composition) = 4

		for y in range(0, Y + 1):
			if not y in self.buttons:
				self.buttons[y] = {}

				if not y == Y:
					self.buttons[y][0] = GUIButton('blank')

#		for lineY in range(Y, Y + len(button.composition)):
		for x in range(0, X):
			if not x in self.buttons[Y]:
				composition = []
				for c in button.composition:
					composition.append(' ')

				self.buttons[Y][x] = GUIButton('blank', composition)


		self.buttons[Y][X] = button

	def getButton(self, name):
		for y in self.buttons:
			for x in self.buttons[y]:
				if self.buttons[y][x].name == name:
					return self.buttons[y][x]

class GUIButton:

	def __init__(self, name, composition = [" "],
				 clickFunction = None, selectFunction = None,
				 colorForeSelected = Colors.FOREGROUND_BLACK, colorForeUnselected = Colors.FOREGROUND_WHITE,
				 colorBackSelected = Colors.BACKGROUND_YELLOW, colorBackUnselected = Colors.BACKGROUND_BLACK):
		self.name = name
		self.clickFunction = clickFunction
		self.selectFunction = selectFunction
		self.colorForeSelected = colorForeSelected
		self.colorForeUnselected = colorForeUnselected
		self.colorBackSelected = colorBackSelected
		self.colorBackUnselected = colorBackUnselected
		self.composition = composition

	def adapt(self, Y, gui):
		adaptedComposition = {}

		for y in range(0, len(self.composition)):
			adaptedY = Y + y

			#if GUIButton.lastY + 1 >= len(gui.buttons):
			#	GUIButton.lastY += 1
			#	adaptedY = GUIButton.lastY
			#else:
			#	GUIButton.lastY += 1
			#	adaptedY = GUIButton.lastY

			adaptedComposition[adaptedY] = {}

			#ler letras da linha
			for x in range(0, len(self.composition[y])):
				adaptedX = 0

				if adaptedY in gui.lastsX:
					gui.lastsX[adaptedY] += 1
					adaptedX = gui.lastsX[adaptedY]
				else:
					gui.lastsX[adaptedY] = x
					adaptedX = x

				adaptedComposition[adaptedY][adaptedX] = self.composition[y][x]
		#GUIButton.lastY = Y + len(self.composition)
		self.composition = adaptedComposition

	def click(self):
		if not self.clickFunction is None:
			self.clickFunction()

	def update(self, selected):
		for y in self.composition:
			for x in self.composition[y]:
				console.setColorXY(x, y, self.composition[y][x], self.colorForeSelected | self.colorBackSelected if selected else self.colorForeUnselected | self.colorBackUnselected)

		if selected and not self.selectFunction is None:
			self.selectFunction()

from os import name

if name == 'nt': 
	from ctypes import windll, Structure, c_short, c_ushort, c_char_p, byref

	class COORD(Structure):
		_fields_ = [
			("Y", c_short),
			("X", c_short)
			]
			
	class SMALL_RECT(Structure):
		_fields_ = [
			("Left", c_short),
			("Top", c_short),
			("Right", c_short),
			("Bottom", c_short)
			]

	class CONSOLE_SCREEN_BUFFER_INFO(Structure):
		_fields_ = [
			("dwSize", COORD),
			("dwCursorPosition", COORD),
			("wAttributes", c_ushort),
			("srWindow", SMALL_RECT),
			("dwMaximumWindowSize", COORD)
			]

def setXY(x, y, value):
	if name == 'nt':
		#Windows

		h = windll.kernel32.GetStdHandle(-11)
		windll.kernel32.SetConsoleCursorPosition(h, COORD(x, y))

		x = value.encode("windows-1252")
		windll.kernel32.WriteConsoleA(h, c_char_p(x), len(x), None, None)
	else:
		#Others 

		print("%c[%d;%df" % (0x1B, y, x), end='')
		print(value)

def getKeyword():
	if name == 'nt':
		#Windows
		
		import msvcrt
		key = msvcrt.getch()

		if key == b'\b':
			return 'delete'
		elif key == b'\r':
			return 'enter'

		if msvcrt.kbhit() and key == b'\xe0': #kbhit() para identificar se contém mais de um byte sendo recebido (arrows tem dois, um dizendo que é uma arrow e outra dizendo a direção)
			arrows = {b'H': 'up', b'K': 'left', b'P': 'down', b'M': 'right'}
			return arrows.get(msvcrt.getch()) #Caso seja uma arrow, o segundo getch() irá retornar a direção

		return key.decode("utf-8") #Está em bytes, é preciso decodificar
	else:
		#Others
		
		import tty, sys, termios

		fd = sys.stdin.fileno()
		oldSettings = termios.tcgetattr(fd)

		try:
			tty.setcbreak(fd)
			answer = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

		return answer

def getColor():
	if name == 'nt':
		#Windows
		
		csbi = CONSOLE_SCREEN_BUFFER_INFO()
		windll.kernel32.GetConsoleScreenBufferInfo(windll.kernel32.GetStdHandle(-11), byref(csbi))
		return csbi.wAttributes

def setColor(color):
	if name == 'nt':
		#Windows
		
		windll.kernel32.SetConsoleTextAttribute(windll.kernel32.GetStdHandle(-11), color)
	else:
		print(color)
		
def setColorXY(x, y, value, color):
	setColor(color)
	setXY(x, y, value)

def clear():
	from libs import Colors
	from os import system

	setColor(Colors.BACKGROUND_BLACK | Colors.FOREGROUND_WHITE)
	system('cls' if name == 'nt' else 'clear')
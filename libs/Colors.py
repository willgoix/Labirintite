from os import name as os

#Bytes (Windows)	-	ASCII (Linux, etc)
FOREGROUND_BLACK 	  = 0x0000 if os == 'nt' else '\33[30m'
FOREGROUND_BLUE       = 0x0001 if os == 'nt' else ''
FOREGROUND_GREEN 	  = 0x0002 if os == 'nt' else '\33[32m'
FOREGROUND_CYAN 	  = 0x0003 if os == 'nt' else '\33[36m'
FOREGROUND_RED 	 	  = 0x0004 if os == 'nt' else '\33[31m'
FOREGROUND_MAGENTA    = 0x0005 if os == 'nt' else '\33[35m'
FOREGROUND_YELLOW 	  = 0x0006 if os == 'nt' else '\33[33m'
FOREGROUND_WHITE 	  = 0x0007 if os == 'nt' else '\33[37m'
FOREGROUND_BOLD 	  = 0x0008 if os == 'nt' else '\33[1m'

BACKGROUND_BLACK	  = 0x0000 if os == 'nt' else '\33[40m'
BACKGROUND_BLUE 	  = 0x0010 if os == 'nt' else '\33[44m'
BACKGROUND_GREEN 	  = 0x0020 if os == 'nt' else '\33[42m'
BACKGROUND_CYAN 	  = 0x0030 if os == 'nt' else '\33[46m'
BACKGROUND_RED        = 0x0040 if os == 'nt' else '\33[41m'
BACKGROUND_MAGENTA    = 0x0050 if os == 'nt' else '\33[45m'
BACKGROUND_YELLOW 	  = 0x0060 if os == 'nt' else '\33[43m'
BACKGROUND_WHITE 	  = 0x0070 if os == 'nt' else '\33[47m'
BACKGROUND_BOLD 	  = 0x0080 if os == 'nt' else ''

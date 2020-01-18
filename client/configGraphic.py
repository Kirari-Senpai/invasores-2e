import os
import sys

from core.config import *


if sys.platform.startswith("win"):
	plataforma = "Windows"
elif sys.platform.startswith("linux"):
	plataforma = "Linux"
elif sys.platform.startswith("darwin"):
	plataforma = "Mac"
else:
	plataforma = "Desconocida"


def banner_principal():

	print("""\033[0;36m

  
  ██▓ ███▄    █ ██▒   █▓ ▄▄▄        ██████  ▒█████   ██▀███  ▓█████   ██████ 
 ▓██▒ ██ ▀█   █▓██░   █▒▒████▄    ▒██    ▒ ▒██▒  ██▒▓██ ▒ ██▒▓█   ▀ ▒██    ▒ 
 ▒██▒▓██  ▀█ ██▒▓██  █▒░▒██  ▀█▄  ░ ▓██▄   ▒██░  ██▒▓██ ░▄█ ▒▒███   ░ ▓██▄   
 ░██░▓██▒  ▐▌██▒ ▒██ █░░░██▄▄▄▄██   ▒   ██▒▒██   ██░▒██▀▀█▄  ▒▓█  ▄   ▒   ██▒
 ░██░▒██░   ▓██░  ▒▀█░   ▓█   ▓██▒▒██████▒▒░ ████▓▒░░██▓ ▒██▒░▒████▒▒██████▒▒
 ░▓  ░ ▒░   ▒ ▒   ░ ▐░   ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░░ ▒░ ░▒ ▒▓▒ ▒ ░
  ▒ ░░ ░░   ░ ▒░  ░ ░░    ▒   ▒▒ ░░ ░▒  ░ ░  ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░  ░░ ░▒  ░ ░
  ▒ ░   ░   ░ ░     ░░    ░   ▒   ░  ░  ░  ░ ░ ░ ▒    ░░   ░    ░   ░  ░  ░  
  ░           ░      ░        ░  ░      ░      ░ ░     ░        ░  ░      ░  
                   ░                                                             	
\033[1;33m

                       Constructor cliente
                      	 
                 https://github.com/Kirari-Senpai
                      	 
                      	 \033[0;39m""")

	return


def cartelAyuda():
	print("""\033[0;39m

 \033[1;31m[-] Puedes tipear 'ayuda' para ver los comandos disponibles \033[0;39m

	""")
	return

def limpiar(plataforma):
	if (plataforma=="Windows"):
		os.system('cls')
	else:
		os.system('clear')
	return

def main():

	limpiar(plataforma)
	banner_principal()
	cartelAyuda()

	opcion = (input(" \033[0;39mInvasores (\033[0;31mConstructor\033[0;39m) --> \033[0;39m").lower()).replace(" ","")

	while (opcion!="salir"):

		if (opcion==""):
			pass
		elif (opcion=="limpiar"):
			limpiar(plataforma)
			banner_principal()
			cartelAyuda()
		elif(opcion==''):
			pass
		else:
			print('\n [\033[1;31mx\033[0;39m] Comando "' + (opcion).strip() + '" no encontrado.\n')

		opcion = (input(" \033[0;39mInvasores (\033[0;31mConstructor\033[0;39m) --> \033[0;39m").lower()).replace(" ","")

	return

if __name__ == '__main__':
	main()
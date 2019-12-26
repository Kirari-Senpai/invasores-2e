
# Creado por Kirari

import sys
import os
import pygame

from .utilidades.creador_ayuda import *

from .utilidades.banners import *


def menu_interactivo():

	COMANDOS = {

	"comenzar" : ["start","Dar comienzo a la partida"]

	}

	pygame.init()
	pygame.mixer.music.load(os.getcwd() + "/core/musica/main.mp3")
	pygame.mixer.music.play(loops=-1)

	os.system('clear')
	
	banner_principal()

	ayuda = """\033[0;39m

 \033[1;31m [-] Puedes tipear 'ayuda' para ver los comandos disponibles

	"""

	print(ayuda)

	opcion = (input(" \033[1;36mInvasores --> \033[0;39m").lower()).replace(" ", "")

	while(opcion!="salir"):

		if(opcion=="comenzar"):
			pygame.mixer.music.stop()
			os.system('python3 core/mothership.py')
			pygame.mixer.music.load(os.getcwd() + "/core/musica/main.mp3")
			pygame.mixer.music.play(loops=-1)
			os.system('clear')
			banner_principal()
			print(ayuda)
		elif(opcion=="ayuda"):
			comandos(COMANDOS,'Comandos generales')
			comandos_basicos('principal')
		elif(opcion=="limpiar"):
			os.system('clear')
			banner_principal()
			print(ayuda)
		elif(opcion==''):
			pass
		else:
			print('\n [\033[1;31mx\033[0;39m] Comando "', opcion, '" no encontrado.\n')

		opcion = (input(" \033[1;36mInvasores --> \033[0;39m").lower()).replace(" ", "")

	os.system('clear')
	sys.exit(0)
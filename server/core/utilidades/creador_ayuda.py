

# Permite crear espacios entre los comandos 

def crear_espacios(cadena,total_espacios=19):
	longitud = total_espacios-len(cadena)
	return (" "*longitud)

def comandos_basicos(etapa):

	COMANDOS = {

	"ayuda": ["Help","Despliega esto"],
	"limpiar": ["Clear","Limpiar pantalla"]

		}

	if etapa=="principal":
		COMANDOS["salir"] = ["exit","Permite terminar el programa principal"]
	elif etapa=="secundario":
		COMANDOS["volver"] = ["back","Volver al lugar anterior"]

	
	print ("\n Comandos basicos")
	print (" ================\n")

	print ("     Comando            Descripcion")
	print ("     --------           ------------")

	for comando,lista in sorted(COMANDOS.items()):
		print ('     '+comando+crear_espacios(comando)+lista[1])

	print('\n')


def comandos(COMANDOS,cadena):
	print ("\n {}".format(cadena))
	print (" {}\n".format("="*len(cadena)))

	print ("     Comando            Descripcion")
	print ("     --------           ------------")

	for comando,lista in sorted(COMANDOS.items()):
		print ('     '+comando+crear_espacios(comando)+lista[1])

	print('\n')
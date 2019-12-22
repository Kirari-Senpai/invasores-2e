<p align="center">
    <img src="logos/alien1.png" height="300" width="400">

[![HitCount](http://hits.dwyl.io/shauryauppal/Socket-Programming-Python.svg)](https://github.com/Kirari-Senpai/invasores-2/) [![MadeIn](https://img.shields.io/badge/MADE%20IN-PYTHON-darkblue.svg)](https://github.com/Kirari-Senpai/invasores-2/)[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

Se trata de un videojuego terminal. Tú eres un Furon (raza extraterrestre avanzada), una especie bélica, con tecnología extremadamente mortal. Por lo cual te diriges a la tierra para poder experimentar, manipular, atacar a otras especies, etc. Tú decides que hacer con ellos. Desde controlar a un simple humano para sacarle información, hasta utilizar un ejército completo para atacar a otros lugares (notorio de esta especie). Algo optativo, es que puedes evitar ser detectado por medio de una habilidad llamada Holobob, ya descubrirás como utilizarla, sólo sé paciente!. Este simple juego esta hecho para entornos reales (basada en el modelo Cliente-Servidor).

</p>


## Como descargar e instalar? ##

```
git clone https://github.com/Kirari-Senpai/invasores-2.git
cd invasores-2/
pip3 install -r requirements.txt
cd server/
```

## Empezar con la invasión ##

```
python3 invasores.py
```

## Persona curiosa ##

La curiosa persona se acerca a tu nave, pero todavía no sabe que le espera...

```
python3 humano.py <ip> <port>
```

## Que se puede hacer con invasores? ##

Antes de empezar, no podemos operar con alguien si no la abducimos, por tanto, se realizará lo siguiente:

- Abducción automática

Cuando hayamos raptado al individuo, podremos hacer diferentes cosas:

- Manejarlo a nuestro antojo medianta una shell
- Keylogger (en desarrollo)
- Grabar audio (en desarrollo)
- Screenshot (en desarrollo)
- Instalarse en el sistema (en desarrollo)
- Autoremoverse (en desarrollo)
- Ransomware (en desarrollo)


## Técnicas de captura de humanos ##

### Abducción automática ###

Tus compañeros de nave atraparán terrícolas, sin necesidad de que tu esperes por ellos. En pocas palabras, la tarea para aceptar conexiones, correrá en segundo plano.

### Abducción en vivo ###

Accediendo al menu de abducciones, podremos solicitar ver en vivo la captura de humanos.



## Laboratorio ##

### Ver a los individuos que hayas raptado ###

Simplemente con tipear "listar" podrás ver a todas las personas que hayas capturado en el camino.

```
 Invasores (Laboratorio) --> listar


 Lista de personas secuestradas

╒══════╤═══════════════╤═══════════╤══════════╤══════════════════════════╤══════════════════╤══════════╕
│   ID │ Terricola     │ Pais      │ Ciudad   │ Direccion IP (Privada)   │ IPv4 (Publica)   │   Puerto │
╞══════╪═══════════════╪═══════════╪══════════╪══════════════════════════╪══════════════════╪══════════╡
│    1 │ kirari        │ USA       │ NYC      │ 192.168.0.15             │ 196.167.98.41    │    56608 │
╘══════╧═══════════════╧═══════════╧══════════╧══════════════════════════╧══════════════════╧══════════╛

```

### Manipulación alienígena ###

Permite tomar el control de un cuerpo en específico para operar. Esto se hace mediante el comando: 

```
manipular <id>
```

### Asesinar basura humana ###

Una vez que la persona no te haga más falta, puedes eliminarla de tu lista con el siguiente comando: 

```
matar <id>
```

## Módulos para operar con el individuo ###

Estas están disponibles en el menú de "control total", una vez se haya ejecutado el comando de Manipulación alienígena.

### Shell ###

Devuelve una shell. Acá un ejemplo:

```
 (kirari)> ls -la

total 20
drwxr-xr-x 3 kirari kirari 4096 nov 20 22:32 .
drwxr-xr-x 5 kirari kirari 4096 nov 19 23:54 ..
-rw-r--r-- 1 kirari kirari 4665 nov 21 02:10 humano.py
drwxr-xr-x 3 kirari kirari 4096 nov 20 22:33 Modulos

 Comando utilizado: ls -la

 (kirari)> pwd

/home/kirari/Escritorio/

 Comando utilizado: pwd

 (kirari)> 

```
### Keylogger ###

Graba cualquier movimiento que la víctima haga mediante pulsaciones en el teclado. Toda la información se registrará en un archivo.

### Grabar audio ###

Si quieres mantenerte informado de lo que sucede alrededor del capturado, entonces activa este módulo, para escuchar todos sus movimientos.

### Screenshot ###

Si quieres pruebas de que la víctima no te engaña, tóma capturas de pantalla para corroborar sus acciones.

### Instalarse ###

Podrás copiarte en los registros del sistema para obtener persistencia.

### Remover ###

Una vez que hayas acabado con la víctima, puedes eliminar todo tipo de rastro del bicho implantado en el sistema.

### Ransomware ###

Si la víctima se resiste a darte lo que quieres, sólo tóma de rehénes a sus personas más cercanas. Entonces podrás pedir lo que quieras a cambio de liberarlas. (Se recomienda usar este módulo en un entorno controlado).

## Destrucción total ##

Elimina a todas las personas capturadas mediante el comando: 

```
destruirlos
```


Advertencia: el mismo está en pleno desarrollo, por lo tanto, puede presentar errores durante su ejecución.

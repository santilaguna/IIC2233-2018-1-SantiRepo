# Tarea 6

Alumno: Santiago Laguna

## Instrucciones de uso o archivo principal a ejecutar para correr la tarea

Los archivos principales corresponden a los main.py de la carpeta server y client respectivamente. Desde estos se deben ejecutar los programas.

## Librerías utilizadas

* PyQt5 (.Qt - .QtGui - .QtCore - .QtWidgets)
* re
* os
* sys
* socket
* threading
* json

## Información útil para la corrección

En el chat se avisa la conexión y desconexión de los usuarios.

Las variables HOST y PORT están al comienzo de los respectivos main.py

Para agregar un silencio sólo se debe indicar la duración y apretar el botón agregar silencio, los otros textos serán ignorados. 

El formato del silencio en pantalla es “silencio” + la duración de éste (en formato musical).

Cuando se desconecta el editor de la sala de edición, si hay espectadores en la sala, el primero en entrar pasa a ser el editor.

El programa funciona sólo con midis de un canal.

El servidor escucha por default hasta máximo cinco clientes, este parámetro puede ser cambiado, al igual que HOST y PORT al comienzo del main.py del directorio server.

Los prints del servidor imprimen: 

* 1) el cliente del que se recibe o al que se manda la información. 
* 2) el tipo de consulta o respuesta. 
* 3) información que se considera más relevante, junto con el largo del mensaje.

## Errores

Hay un print mal hecho cuando se pregunta por verificar usuario repetido, puesto que el print que aparece en pantalla es el de verificar canciones repetidas, (sólo el mensaje de recibir, el de enviar aparece correctamente, al igual que enviar y recibir de verificar canciones repetidas).

## Resumen modularización y aspectos generales

### Manejo de bytes

Todo el manejo de bytes es realizado por el servidor, el módulo convertidor_midi.py de cliente simplemente escribe el archivo midi con los bytes que le manda el servidor cuándo el cliente pide descargar una canción.

### Redes

El servidor está directamente en el módulo main.py del directorio server. Por otro lado, el cliente está implementado en el módulo cliente.py del directorio client.

### Interfaz

La ventana de inicio está implementada en el módulo main.py, mientras que la ventana de edición está implementada en el módulo edit_menu.py 

## Bonus

Se optó sólo por el bonus de chat.

## Meme de fin de semestre (mucho muy importante)

![alt text](https://i.pinimg.com/736x/e6/87/d3/e687d38aa5363d93a05296a4bede89e2--nursing-school-quotes-nurses-week-quotes.jpg)



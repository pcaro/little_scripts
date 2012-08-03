#!/bin/sh

# Las dependencias:
# Para las señales acústicas hace falta instalar beep
# Para las señales ópticas es necesario libnotify-bin

RUTA=`pwd`
notify-send --icon gnome-terminal -u critical "TAREA FINALIZADA" \
"Ha finalizado una tarea que estaba en ejecución
La tarea se ejecuta en:
    ${RUTA}
    " --expire-time 25000

for item in 1 2 3 4 5 6 7 8 9 0
do
    beep
    sleep 0.5
done    

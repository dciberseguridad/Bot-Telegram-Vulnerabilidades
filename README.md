# Bot Telegram Vulnerabilidades
Bot para Telegram de Vulnerabilidades de servicios utilizados, para no estar pendientes de entrar en la web de Mitre y buscar los CVE de nuestros programas

Para usar el BOT debes de seguir los siguientes pasos:

Modificar el archivo con los servicios y URLS y LOGS de los servicios que quieras buscar

Añadir el TOKEN_ID del bot de Telegram y el chat_id donde vas a parsear las vulnerabilidades

Una vez lo tengas todo, arranca el python. python3 cve_bot_vulneravilidades.py, cuando compruebes que esta funcionando tienes que generar el servicio, adjunto archivo. 

Copia el archivo a /etc/systemd/system/

chmod 777 nombre_del_servicio.service

systemctl enable nombre_del_servicio.service

systemctl start nombre_del_servicio.service

Con estos pasos ya tiene funcionando el aviso de vulnerabilidades 

Yo lo tengo funcinando en una maquina virtual con Ubuntu con 1 GB de RAM 25 GB de HD con otros 5 Bots mas y va perfecto.

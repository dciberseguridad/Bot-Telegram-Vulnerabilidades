#Este BOT te envia las vulnerabilidades de las APPS que uses a un grupo de Telegram
#Desarrollado por DCSeguridad (David Cuadrado Sánchez)
#https://dcseguridad.es

#Inicio del BOT
import requests
from bs4 import BeautifulSoup
import time
import os

# Cambiar esto por el token de tu bot de Telegram
bot_token = "tu_bot_token"
# Cambiar esto por el ID de chat de Telegram al que quieres enviar los mensajes
chat_id = "tu_chat_id"
URL = f"https://api.telegram.org/bot{bot_token}/sendMessage"

# URLs de búsqueda de vulnerabilidades
SERVICIO1_URL = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=servicio1"
SERVICIO2_URL = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=servicio2"
SERVICIO3_URL = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=servicio3"
SERVICIO4_URL = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=servicio4"

#Aquí sigue añadiendo servicios

# Archivos de registro de vulnerabilidades, recuerda que si cambias la carpeta, debes definirla aquí
SERRVICIO1_LOG_FILE = "/home/tuusuario/Bots_Telegram/cve_log_vulnerabilidades_servicio1.txt"
SERRVICIO2_LOG_FILE = "/home/tuusuario/Bots_Telegram/cve_log_vulnerabilidades_servicio2.txt"
SERRVICIO3_LOG_FILE = "/home/tuusuario/Bots_Telegram/cve_log_vulnerabilidades_servicio3.txt"
SERRVICIO4_LOG_FILE = "/home/tuusuario/Bots_Telegram/cve_log_vulnerabilidades_servicio4.txt"
#Aquí sigue añadiendo LOGS puedes poner todos los logs en un solo archivo, cve_log_vulnerabilidades.txt pero me parece mas limpio usar un log para cada servicio 


def send_telegram_message(text):
    """
    Envia un mensaje de texto a un grupo de Telegram
    """
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(URL, data=data)
    return response.json()

def check_cve(url, log_file):
    """
    Busca nuevas vulnerabilidades en la URL dada y envía una alerta a Telegram si se encuentra alguna nueva
    """
    
# Verificar a qué servicio pertenece la URL para reconocer el mensaje
    service_name = ""
    if url == SERVICIO1_URL:
        service_name = "servicio1"
    elif url == SERVICIO2_URL:
        service_name = "servicio2"
    elif url == SERVICIO3_URL:
        service_name = "servicio3"
    elif url == SERVICIO4_URL:
        service_name = "servicio4"
   
        
# Obtener la página HTML de la URL de búsqueda
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

# Buscar la tabla de resultados de CVE
    table = soup.find_all("table")[2]
    rows = table.find_all("tr")[1:]

# Leer el archivo de registro para verificar si ya se ha informado sobre alguna de las vulnerabilidades
    reported_cves = set()
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            for line in f:
                reported_cves.add(line.strip())

# Verificar cada fila de la tabla para buscar nuevas vulnerabilidades
    for row in rows:
        columns = row.find_all("td")
        cve_id = columns[0].text.strip()
        if cve_id in reported_cves:
            continue
        reported_cves.add(cve_id)
        cve_url = f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve_id}"
        description = columns[1].text.strip()

# Formato del mensaje de alerta
        message = f"Se ha encontrado una nueva vulnerabilidad en {service_name}:\n{cve_id}: {description}\n{cve_url}"

# Enviar el mensaje a Telegram
        send_telegram_message(message)

# Registrar la vulnerabilidad para evitar duplicados
        with open(log_file, "a") as f:
            f.write(f"{cve_id}\n")

if __name__ == "__main__":
    while True:
        check_cve(SERVICIO1_URL, SERVICIO1_LOG_FILE)
        check_cve(SERVICIO2_URL, SERVICIO2_LOG_FILE)
        check_cve(SERVICIO3_URL, SERVICIO3_LOG_FILE)
        check_cve(SERVICIO4_URL, SERVICIO4_LOG_FILE)

        time.sleep(3600)
# Esperar una hora antes de buscar nuevas vulnerabilidades
# Puedes definir el tiempo que quieras para búsqueda de vulnerabilidades, definido en segundos
        

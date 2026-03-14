import socket
import json
import threading
import mysql.connector
from mysql.connector import pooling # Ajout du pool
import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

# Configuration
HOST = '0.0.0.0'
PORT = 5000
DB_CONFIG = {
    'user': 'yousseph00',
    'password': 'bambaras00', 
    'host': 'localhost',
    'database': 'supervision_db'
}

# 1. CRITÈRE PROJET : Création du Pool de Connexion BD
try:
    db_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5, # Jusqu'à 5 connexions simultanées vers la BD
        **DB_CONFIG
    )
except mysql.connector.Error as err:
    print(f"Erreur lors de la création du pool : {err}")

# Configuration du journal (Logs)
logging.basicConfig(
    filename='supervision.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

node_status = {}

def save_to_db(data):
    try:
        # Utilisation du pool au lieu d'une nouvelle connexion
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        query = """INSERT INTO node_metrics 
                   (node_id, os_info, cpu_usage, mem_usage, disk_usage, uptime, status_services) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        values = (
            data['node_id'], data['os'], data['cpu'], 
            data['mem'], data['disk'], data['uptime'], 
            json.dumps(data['services'])
        )
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close() # La connexion retourne au pool, elle n'est pas détruite
    except Exception as e:
        logging.error(f"Erreur DB: {e}")

def handle_client(client_socket, addr):
    print(f"[+] Connexion de {addr}")
    try:
        while True:
            request = client_socket.recv(4096).decode('utf-8')
            if not request: break
            
            try:
                data = json.loads(request)
                node_id = data['node_id']
                node_status[node_id] = datetime.now()
                save_to_db(data)
                
                # Gestion des alertes > 90%
                if data['cpu'] > 90 or data['mem'] > 90:
                    msg = f"ALERTE : {node_id} charge excessive (CPU: {data['cpu']}%, RAM: {data['mem']}%)"
                    print(f"!!! {msg}")
                    logging.warning(msg)
                    
            except json.JSONDecodeError:
                print("[-] Format de message invalide")
    except Exception as e:
        print(f"Erreur client {addr}: {e}")
    finally:
        client_socket.close()

def check_for_failures():
    while True:
        now = datetime.now()
        for node, last_seen in list(node_status.items()):
            if now - last_seen > timedelta(seconds=90):
                msg = f"PANNE : Le nœud {node} ne répond plus"
                print(f"[!] {msg}")
                logging.error(msg)
                del node_status[node]
        threading.Event().wait(30)

def start_server():
    # Gestion multi-thread via pool (Critère du projet)
    executor = ThreadPoolExecutor(max_workers=20)
    
    threading.Thread(target=check_for_failures, daemon=True).start()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(10)
    print(f"[*] Serveur de supervision actif sur le port {PORT}...")

    while True:
        client, addr = server.accept()
        executor.submit(handle_client, client, addr)

if __name__ == "__main__":
    start_server()

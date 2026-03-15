import socket
import json
import psutil
import platform
import time

# Configuration
SERVER_IP = '192.168.48.128' 
SERVER_PORT = 5000
NODE_ID = "Agent-Ubuntu-Desktop-02" # Identifiant unique pour le rapport

def get_metrics():
    # 1. Collecte des métriques système
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    uptime = int(time.time() - psutil.boot_time())
    
    # 2. Statut des services (Processus)
    services_to_check = ["sshd", "apache2", "mysql", "firefox", "chrome", "putty"]
    services = {}
    # On parcourt les processus une seule fois pour l'efficacité
    running_procs = [p.name().lower() for p in psutil.process_iter(['name'])]
    for s_name in services_to_check:
        services[s_name] = "OK" if any(s_name in p for p in running_procs) else "KO"

    # 3. Statut des ports (Scanner local)
    ports_to_check = [22, 80, 443, 3306]
    ports = {}
    for port in ports_to_check:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            ports[str(port)] = "OPEN" if s.connect_ex(('127.0.0.1', port)) == 0 else "CLOSED"

    return {
        "node_id": NODE_ID,
        "os": f"{platform.system()} {platform.release()}",
        "cpu": cpu,
        "mem": mem,
        "disk": disk,
        "uptime": uptime,
        "services": services,
        "ports": ports
    }

def start_agent():
    print(f"[*] Agent {NODE_ID} démarré. Connexion vers {SERVER_IP}...")
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5)
                s.connect((SERVER_IP, SERVER_PORT))
                
                # Récupération et envoi des données
                data = get_metrics()
                s.sendall(json.dumps(data).encode('utf-8'))
                print(f"[+] Données envoyées : CPU {data['cpu']}% | RAM {data['mem']}%")
                
                # Attente de la commande du serveur (ex: UP_SSH)
                try:
                    response = s.recv(1024).decode('utf-8')
                    if response:
                        print(f"[*] Message du serveur : {response}")
                        if "UP" in response:
                            print(f"[!!!] Action requise : Activation demandée pour {response}")
                except socket.timeout:
                    pass # Pas de commande reçue, on continue
                
        except Exception as e:
            print(f"[-] Erreur : {e}. Nouvelle tentative dans 10s...")
        
        time.sleep(10)

if __name__ == "__main__":
    start_agent()
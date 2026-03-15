import threading
import socket
import json
import time
import random

def simulate_client(client_id):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('192.168.48.128', 5000))
            payload = {
                "node_id": f"Node_Simulated_{client_id}",
                "os": "Linux Sim",
                "cpu": random.uniform(5.0, 95.0),
                "mem": random.uniform(10.0, 80.0),
                "disk": 50.0,
                "uptime": 1000,
                "services": {"ssh": "OK"}
            }
            s.sendall(json.dumps(payload).encode('utf-8'))
    except Exception:
        pass

def run_test(nb_clients):
    print(f"Lancement du test avec {nb_clients} clients...")
    threads = []
    for i in range(nb_clients):
        t = threading.Thread(target=simulate_client, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    print("Test terminé.")

# Exécute successivement pour ton rapport
run_test(10)
time.sleep(2)
run_test(50)
time.sleep(2)
run_test(100)
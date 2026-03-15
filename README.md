 Network Monitoring System - M1 SRIV
Ce projet consiste en une solution de supervision réseau distribuée (Client-Serveur) permettant de monitorer en temps réel des métriques système sur un parc hétérogène (Windows & Linux).

📋 Fonctionnalités
Collecte multiplateforme : Agents Python pour Windows 10/11 et Ubuntu Desktop.

Métriques en temps réel : CPU, RAM, Disque, Uptime.

Surveillance de services : État des services critiques (SSH, Apache, MySQL).

Dashboard Web : Interface dynamique avec graphiques (Chart.js) et mises à jour via WebSockets (Socket.io).

Alerting : Détection des surcharges système et des pannes de nœuds (Heartbeat).

Persistance : Stockage centralisé dans une base de données MariaDB.

🛠 Architecture Technique
Backend : Python 3.10+, Flask, Socket.io.

Agents : Python (bibliothèque psutil).

Base de données : MariaDB / MySQL.

Communication : Sockets TCP, sérialisation JSON.

⚙️ Installation
1. Préparation du Serveur (Ubuntu)
Bash
# Cloner le projet
git clone https://github.com/votre-repo/supervision-reseau.git
cd supervision-reseau

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install flask flask-socketio mysql-connector-python psutil
2. Configuration de la Base de Données
Créez une base de données supervision_db et importez le schéma SQL fourni :

SQL
CREATE DATABASE supervision_db;
-- Importez votre fichier .sql ici
3. Lancer l'Agent (Côté Client)
Sur la machine à surveiller (Windows ou Ubuntu) :

Modifiez l'adresse SERVER_IP dans agent.py.

Lancez l'agent :

Bash
python agent.py
📊 Utilisation
Démarrez le serveur de réception : python server.py

Démarrez l'interface Web : python app_gui.py

Accédez au dashboard : http://localhost:8080 (ou IP du serveur)
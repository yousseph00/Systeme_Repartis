from flask import Flask, render_template
from flask_socketio import SocketIO
import mysql.connector
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="yousseph00",
        password="bambaras00",
        database="supervision_db"
    )

def fetch_metrics():
    """Récupère les dernières données et les convertit pour le JSON."""
    while True:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM node_metrics ORDER BY timestamp DESC LIMIT 10")
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # --- CORRECTION ICI ---
            # On transforme l'objet datetime en texte (ex: "10:15:30")
            for row in data:
                if 'timestamp' in row and row['timestamp']:
                    row['timestamp'] = row['timestamp'].strftime("%H:%M:%S")
            # ----------------------

            socketio.emit('update_metrics', data)
        except Exception as e:
            print(f"Erreur GUI: {e}")
        time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Lancement du thread de lecture de données
    threading.Thread(target=fetch_metrics, daemon=True).start()
    # Lancement du serveur Web sur le port 8080 (car le 5000 est pris par les sockets de ton agent)
    socketio.run(app, host='0.0.0.0', port=8080)

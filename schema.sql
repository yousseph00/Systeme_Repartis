-- Création de la base de données
CREATE DATABASE IF NOT EXISTS supervision_db;
USE supervision_db;

-- 1. Table des métriques (Stockage des données envoyées par les agents)
CREATE TABLE IF NOT EXISTS metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    node_id VARCHAR(50) NOT NULL,          -- Nom de l'agent (ex: Agent-Win10)
    os_info VARCHAR(100),                  -- OS détecté (ex: Windows 10)
    cpu_usage FLOAT NOT NULL,              -- % CPU
    ram_usage FLOAT NOT NULL,              -- % RAM
    disk_usage FLOAT NOT NULL,             -- % Disque
    uptime INT,                            -- Uptime en secondes
    status_services JSON,                  -- État des services au format JSON
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX (node_id),                       -- Index pour accélérer les recherches par agent
    INDEX (timestamp)                      -- Index pour les graphiques temporels
);

-- 2. Table des logs d'alertes (Pour l'historique des pannes et surcharges)
CREATE TABLE IF NOT EXISTS alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    node_id VARCHAR(50) NOT NULL,
    alert_type ENUM('WARNING', 'ERROR') NOT NULL, -- WARNING (Surcharge) ou ERROR (Panne)
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Exemple de requête pour voir les derniers états de chaque machine
-- SELECT * FROM metrics ORDER BY timestamp DESC LIMIT 10;
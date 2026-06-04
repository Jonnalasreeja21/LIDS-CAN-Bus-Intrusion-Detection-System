DROP TABLE IF EXISTS alerts;

CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    can_id TEXT NOT NULL,
    alert_type TEXT NOT NULL, 
    data_summary TEXT,
    is_anomaly BOOLEAN NOT NULL
);
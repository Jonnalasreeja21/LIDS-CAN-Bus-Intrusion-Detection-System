from flask import Flask, render_template, jsonify
import sqlite3
from lids.engine import LIDSEngine

app = Flask(__name__)
engine = LIDSEngine()

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    db = get_db()
    # Get counts of anomalies grouped by type
    rows = db.execute('''
        SELECT alert_type, COUNT(*) as count 
        FROM alerts 
        WHERE is_anomaly = 1 
        GROUP BY alert_type
    ''').fetchall()
    
    stats_dict = {row['alert_type']: row['count'] for row in rows}
    
    # Get total count for a summary header
    total_anomalies = sum(stats_dict.values())
    
    return render_template('dashboard.html', stats=stats_dict, total=total_anomalies)

@app.route('/reports')
def reports():
    db = get_db()
    # Fetch last 50 entries for the history table
    alerts = db.execute('SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 50').fetchall()
    return render_template('reports.html', alerts=alerts)

from flask import jsonify

@app.route('/api/data')
def api_data():
    db = get_db()
    
    # 1. Fetch CUMULATIVE statistics for the Network Overview cards/chart
    # This counts every anomaly ever recorded in the DB
    stats_rows = db.execute('''
        SELECT alert_type, COUNT(*) as count 
        FROM alerts 
        WHERE is_anomaly = 1 
        GROUP BY alert_type
    ''').fetchall()
    
    stats_dict = {row['alert_type']: row['count'] for row in stats_rows}
    
    # 2. Fetch the 15 most RECENT logs for the Live Threat Feed
    log_rows = db.execute('''
        SELECT timestamp, can_id, alert_type, is_anomaly 
        FROM alerts 
        ORDER BY timestamp DESC LIMIT 15
    ''').fetchall()
    
    logs_list = [dict(row) for row in log_rows]
    
    return jsonify({
        "stats": stats_dict,
        "recent_logs": logs_list
    })

if __name__ == '__main__':
    app.run(debug=True)

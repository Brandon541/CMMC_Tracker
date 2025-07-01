import sqlite3
import json
from datetime import datetime

import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'compliance.db')

def init_database():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Controls table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS controls (
            id TEXT PRIMARY KEY,
            name TEXT,
            description TEXT,
            domain TEXT,
            status TEXT,
            objectives TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # POAMs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS poams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            control_id TEXT,
            description TEXT,
            priority TEXT,
            due_date TEXT,
            assignee TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Artifacts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artifacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_name TEXT,
            file_size INTEGER,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            control_id TEXT,
            description TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def save_control(control_data):
    """Save or update a control in the database"""
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO controls 
        (id, name, description, domain, status, objectives, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        control_data['id'],
        control_data['name'],
        control_data['description'],
        control_data['domain'],
        control_data['status'],
        json.dumps(control_data.get('objectives', [])),
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()

def get_controls():
    """Retrieve all controls from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM controls')
    rows = cursor.fetchall()
    
    controls = []
    for row in rows:
        control = {
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'domain': row[3],
            'status': row[4],
            'objectives': json.loads(row[5]) if row[5] else [],
            'updated_at': row[6]
        }
        controls.append(control)
    
    conn.close()
    return controls

def save_poam(poam_data):
    """Save a new POAM to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO poams 
        (title, control_id, description, priority, due_date, assignee, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        poam_data['title'],
        poam_data['control'],
        poam_data['description'],
        poam_data['priority'],
        poam_data['dueDate'],
        poam_data['assignee'],
        poam_data['status']
    ))
    
    poam_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return poam_id

def update_poam(poam_id, poam_data):
    """Update an existing POAM in the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE poams 
        SET title=?, control_id=?, description=?, priority=?, due_date=?, assignee=?, status=?, updated_at=?
        WHERE id=?
    ''', (
        poam_data['title'],
        poam_data['control'],
        poam_data['description'],
        poam_data['priority'],
        poam_data['dueDate'],
        poam_data['assignee'],
        poam_data['status'],
        datetime.now().isoformat(),
        poam_id
    ))
    
    conn.commit()
    conn.close()

def delete_poam(poam_id):
    """Delete a POAM from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM poams WHERE id=?', (poam_id,))
    
    conn.commit()
    conn.close()

def get_poams():
    """Retrieve all POAMs from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM poams ORDER BY created_at DESC')
    rows = cursor.fetchall()
    
    poams = []
    for row in rows:
        poam = {
            'id': row[0],
            'title': row[1],
            'control': row[2],
            'description': row[3],
            'priority': row[4],
            'dueDate': row[5],
            'assignee': row[6],
            'status': row[7],
            'created_at': row[8],
            'updated_at': row[9]
        }
        poams.append(poam)
    
    conn.close()
    return poams

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'dance_events.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Events table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT,
        start_time TEXT,
        city TEXT,
        venue TEXT,
        organizer TEXT,
        website TEXT,
        source TEXT,
        raw_data TEXT,
        unique_hash TEXT UNIQUE
    )
    ''')
    
    conn.commit()
    conn.close()

def save_events(events_list):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for event in events_list:
        try:
            # Create a unique hash for deduplication within the same run or across runs
            # Hash components: Name, Date, City, Venue (basic)
            event_hash = f"{event.get('name')}|{event.get('date')}|{event.get('city')}|{event.get('venue')}"
            
            cursor.execute('''
            INSERT OR IGNORE INTO events 
            (name, date, start_time, city, venue, organizer, website, source, raw_data, unique_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event.get('name'),
                event.get('date'),
                event.get('start_time'),
                event.get('city'),
                event.get('venue'),
                event.get('organizer'),
                event.get('website'),
                event.get('source'),
                str(event),
                event_hash
            ))
        except Exception as e:
            print(f"Error saving event: {e}")
            
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")

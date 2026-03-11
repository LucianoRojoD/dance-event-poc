import sqlite3
import os
import json

def insert_manual_data():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dance_events.db')
    if not os.path.exists(db_path):
        print("Database not found. Run pipeline first.")
        return
    
    events = [
      {
        "name": "El Palacio Encuentro Milonguero",
        "date": "March 13–15, 2026",
        "city": "Perpignan",
        "venue": "France",
        "website": "https://www.facebook.com/groups/1437230420087388/",
        "source": "tangocat.net"
      },
      {
        "name": "NeoClassic Skånetangon",
        "date": "March 13–15, 2026",
        "city": "Lomma",
        "venue": "Sweden",
        "website": "https://www.facebook.com/events/25132175169723272/",
        "source": "tangocat.net"
      },
      {
        "name": "Brilloso Tango Marathon",
        "date": "March 13–15, 2026",
        "city": "Barcelona",
        "venue": "Spain",
        "website": "https://brillosotangomarathon.com/",
        "source": "tangocat.net"
      },
      {
        "name": "Royal Tango Weekend",
        "date": "March 13–15, 2026",
        "city": "Moszna",
        "venue": "Poland",
        "website": "https://www.facebook.com/events/26051630417761868/",
        "source": "tangocat.net"
      },
      {
        "name": "Nostos Tango Marathon",
        "date": "March 19–22, 2026",
        "city": "Alexandroupoli",
        "venue": "Greece",
        "website": "https://www.facebook.com/events/1041878150907720/",
        "source": "tangocat.net"
      }
    ]
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for event in events:
        event_hash = f"{event['name']}|{event['date']}|{event['city']}|{event['venue']}"
        cursor.execute('''
        INSERT OR IGNORE INTO events 
        (name, date, city, venue, website, source, unique_hash)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            event['name'],
            event['date'],
            event['city'],
            event['venue'],
            event['website'],
            event['source'],
            event_hash
        ))
    
    conn.commit()
    conn.close()
    print("Manual data inserted successfully.")

if __name__ == "__main__":
    insert_manual_data()

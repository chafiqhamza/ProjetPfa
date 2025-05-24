import sqlite3
import json

def initialize_database():
    conn = sqlite3.connect('profiles.db')
    cursor = conn.cursor()

    # Create profiles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profiles (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        bio TEXT,
        profile_url TEXT NOT NULL,
        featured_repo TEXT
    )
    ''')

    conn.commit()
    conn.close()

def insert_profiles_from_json(json_file):
    conn = sqlite3.connect('profiles.db')
    cursor = conn.cursor()

    with open(json_file, 'r', encoding='utf-8') as f:
        profiles = json.load(f)

    for profile in profiles:
        cursor.execute('''
        INSERT OR IGNORE INTO profiles (id, name, bio, profile_url, featured_repo)
        VALUES (?, ?, ?, ?, ?)
        ''', (profile.get('id'), profile.get('name'), profile.get('bio'), profile.get('profile_url'), profile.get('featured_repo')))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()
    insert_profiles_from_json('profiles.json')
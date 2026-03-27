import sqlite3

def init_db():
    conn = sqlite3.connect('ats_system.db')
    cursor = conn.cursor()

    # Table 1: Store the Job Requirements
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_title TEXT NOT NULL,
        required_skills TEXT NOT NULL,
        min_experience INTEGER,
        required_education TEXT
    )
    ''')

    # Table 2: Store Candidate Profiles and their Match Score
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER,
        name TEXT,
        email TEXT,
        skills TEXT,
        experience TEXT,
        education TEXT,
        match_score REAL,
        FOREIGN KEY(job_id) REFERENCES jobs(id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
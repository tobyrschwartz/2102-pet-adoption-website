"""
Utility module for initializing the SQLite3 database.

This file is not meant to be executed directly.
"""

import sqlite3
from enums import PetStatus

def init_db(db_name="petadoption.db", first_run=False):
    """Initialize the SQLite3 database."""
    connection = sqlite3.connect(db_name)
    connection.execute("PRAGMA foreign_keys = ON") # allows us to use foreign keys to link tables
    cursor = connection.cursor()

    if first_run:
        # Drop existing tables if first run
        cursor.execute('DROP TABLE IF EXISTS users')
        cursor.execute('DROP TABLE IF EXISTS pets')
        cursor.execute('DROP TABLE IF EXISTS applications')
        cursor.execute('DROP TABLE IF EXISTS questionaire_responses')
        cursor.execute('DROP TABLE IF EXISTS questions')
        cursor.execute('DROP TABLE IF EXISTS choices')

    # Create pets table
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS pets (
                    pet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    species TEXT NOT NULL,
                    breed TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    description TEXT,
                    status TEXT NOT NULL,
                    image_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    # Create users table
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    phone TEXT,
                    role INTEGER NOT NULL DEFAULT 1,
                    approved INTEGER NOT NULL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
    # Create applications table
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS applications (
                    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    pet_id INTEGER NOT NULL,
                    status TEXT NOT NULL DEFAULT 'Pending',
                    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP,
                    reviewed_at TIMESTAMP,
                    reviewer_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (pet_id) REFERENCES pets(pet_id)
                )
            ''')
    # Create questionaire_responses table
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS questionnaire_responses (
                    response_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    answer_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (question_id) REFERENCES questions(question_id)
                )
                ''')

    # Create questions table
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS questions (
                    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_text TEXT NOT NULL,
                    question_type TEXT NOT NULL,
                    is_required INTEGER NOT NULL DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
    # Create options table
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS choices (
                    choice_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER NOT NULL,
                    choice_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (question_id) REFERENCES questions(question_id)
                )
                ''')

    if first_run:
        # Insert mock data into pets table
        cursor.execute('''
                    INSERT INTO pets (name, species, breed, age, description, status, image_url)
                    VALUES
                    (?, ?, ?, ?, ?, ?, ?),
                    (?, ?, ?, ?, ?, ?, ?),
                    (?, ?, ?, ?, ?, ?, ?)
                    ''',
                    ('Larry', 'Dog', 'Golden Retriever', 3, 'Friendly and energetic.',
                        PetStatus.AVAILABLE.value, 'http://example.com/Larry.jpg',
                     'Barry', 'Cat', 'Siamese', 2, 'Loves to cuddle.', 
                        PetStatus.ADOPTED.value, 'http://example.com/Barry.jpg',
                     'Garry', 'Dog', 'Beagle', 4, 'Great with kids.', 
                        PetStatus.AVAILABLE.value, 'http://example.com/Garry.jpg'))

    connection.commit()
    connection.close()

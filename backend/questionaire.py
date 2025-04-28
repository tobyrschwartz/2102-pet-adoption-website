"""Questionnaire Management Module"""
import sqlite3
from enums import QuestionType
from flask import jsonify

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect('petadoption.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_questionaire():
    """
    Retrieve the current questionnaire.
    GET: Fetch all questions and their choices
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT questions.question_id, questions.question_text, questions.question_type, choices.choice_text
            FROM questions
            LEFT JOIN choices ON questions.question_id = choices.question_id
        ''')
        rows = cursor.fetchall()

        questions = {}
        for row in rows:
            question_id = row['question_id']
            if question_id not in questions:
                questions[question_id] = {
                    'id': question_id,
                    'text': row['question_text'],
                    'type': QuestionType(row['question_type']).name,
                    'options': []
                }
            if row['choice_text']:
                questions[question_id]['options'].append(row['choice_text'])

        questions_list = list(questions.values())

        return jsonify(questions_list), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

def set_questionaire(data):
    """
    Replace the entire questionnaire with new questions.
    POST: Reset and add all questions (requires ADMIN role)
    """
    if not data or 'questions' not in data:
        return jsonify({"error": "Invalid data"}), 400

    questions = data['questions']

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM choices')
        cursor.execute('DELETE FROM questions')

        for q in questions:
            cursor.execute('''
                INSERT INTO questions (question_text, question_type)
                VALUES (?, ?)
            ''', (q['text'], QuestionType[q['type'].upper()].value))
            question_id = cursor.lastrowid

            if q['type'].lower() == 'multiple_choice' and q.get('options'):
                for option in q['options']:
                    cursor.execute('''
                        INSERT INTO choices (question_id, choice_text)
                        VALUES (?, ?)
                    ''', (question_id, option))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
    return jsonify({"message": "Questions replaced successfully."}), 201

"""Questionnaire Management Module"""
import sqlite3
from enums import QuestionType
from flask import jsonify

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect('petadoption.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_questionnaire():
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

def set_questionnaire(data):
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

def answer_questionnaire(user_id, data):
    """
    Submit answers to the questionnaire.
    POST: Save user answers (requires USER role)
    """
    if not data or 'answers' not in data:
        return jsonify({"error": "Invalid data"}), 400

    answers = data['answers']

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if the user already has answers in the database
        cursor.execute('''
            SELECT COUNT(*) FROM questionnaire_responses WHERE user_id = ?
        ''', (user_id,))
        count = cursor.fetchone()[0]

        if count > 0:
            return jsonify({"error": "User has already submitted answers."}), 400

        # Insert new answers
        for answer in answers:
            cursor.execute('''
                INSERT INTO questionnaire_responses (user_id, question_id, answer_text)
                VALUES (?, ?, ?)
            ''', (user_id, answer['question_id'], answer['answer_text']))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
    return jsonify({"message": "Answers submitted successfully."}), 201

def get_answered_questionnaire(user_id):
    """
    Retrieve the answered questionnaire.
    GET: Fetch all answered questions and their choices
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT questions.question_id, questions.question_text, questions.question_type, questionnaire_responses.answer_text
            FROM questions
            LEFT JOIN questionnaire_responses ON questions.question_id = questionnaire_responses.question_id
            WHERE questionnaire_responses.user_id = ?
        ''', (user_id,))
        rows = cursor.fetchall()

        answered_questions = {}
        for row in rows:
            question_id = row['question_id']
            if question_id not in answered_questions:
                answered_questions[question_id] = {
                    'id': question_id,
                    'text': row['question_text'],
                    'type': QuestionType(row['question_type']).name,
                    'answer': row['answer_text']
                }

        answered_questions_list = list(answered_questions.values())

        return jsonify(answered_questions_list), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

def has_answered_questionnaire(user_id):
    """
    Check if the user has answered the questionnaire.
    GET: Check if the user has submitted answers
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT COUNT(*) FROM questionnaire_responses WHERE user_id = ?
        ''', (user_id,))
        count = cursor.fetchone()[0]
        return jsonify({"has_open": bool(count > 0)}), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()
